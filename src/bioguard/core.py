"""Core request handling and envelope construction."""

from __future__ import annotations

import hashlib
import json
from uuid import UUID
from typing import Any, Dict, List

from .config import DEFAULT_HOST_ID
from .scoring import decision_from_dimensions, make_event, make_event_rationale
from .utils import deterministic_uuid, utcnow_iso


SCREEN_REQUIRED_KEYS = {"request_id", "conversation_id", "turns", "policy_profile", "host_id"}
SCREEN_ALLOWED_KEYS = {
    "request_id",
    "conversation_id",
    "turns",
    "policy_profile",
    "host_id",
    "contract_version",
    "include_sequences",
    "skill_overrides",
}
SCREEN_ALLOWED_TURN_KEYS = {"actor", "text", "index", "ts_utc"}
SCREEN_ALLOWED_POLICY_KEYS = {
    "mode",
    "threshold_allow",
    "threshold_review",
    "include_bio_seq",
    "include_session_context",
}
SCREEN_ACTORS = {"user", "assistant", "system"}


def _is_uuid(value: Any) -> bool:
    try:
        UUID(str(value))
    except Exception:
        return False
    return True


def _problem(status: int, title: str, detail: str, *, instance: str) -> Dict[str, Any]:
    return {
        "type": f"https://bioguard.invalid/{title.lower().replace(' ', '-')}",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance,
    }


def _sanitize_policy_profile(payload: Dict[str, Any], *, contract_version: str) -> tuple[Dict[str, Any] | None, Dict[str, Any] | None]:
    policy_profile = payload.get("policy_profile")
    if not isinstance(policy_profile, dict):
        return None, _problem(
            422,
            "Unsupported feature",
            "policy_profile is required and must be an object.",
            instance="/v1/screen",
        )

    extras = set(policy_profile) - SCREEN_ALLOWED_POLICY_KEYS
    if extras:
        return None, _problem(
            422,
            "Unsupported feature",
            f"Unsupported policy_profile fields: {','.join(sorted(extras))}",
            instance="/v1/screen",
        )

    for required in {"mode", "threshold_allow", "threshold_review"}:
        if required not in policy_profile:
            return None, _problem(
                400,
                "Invalid request payload",
                f"Missing required policy_profile field: {required}",
                instance="/v1/screen",
            )

    mode = policy_profile.get("mode")
    if mode not in {"allow", "review", "block"}:
        return None, _problem(
            422,
            "Unsupported feature",
            f"Unsupported policy mode: {mode}",
            instance="/v1/screen",
        )

    try:
        threshold_allow = float(policy_profile["threshold_allow"])
        threshold_review = float(policy_profile["threshold_review"])
    except (TypeError, ValueError):
        return None, _problem(
            422,
            "Unsupported feature",
            "threshold_allow and threshold_review must be numbers.",
            instance="/v1/screen",
        )
    if not (0 <= threshold_allow <= 1 and 0 <= threshold_review <= 1 and threshold_review > threshold_allow):
        return (
            None,
            _problem(
                422,
                "Unsupported feature",
                "threshold_review must be > threshold_allow and both in [0,1].",
                instance="/v1/screen",
            ),
        )

    include_bio_seq = policy_profile.get("include_bio_seq", False)
    if include_bio_seq is not None and not isinstance(include_bio_seq, bool):
        return None, _problem(
            422,
            "Unsupported feature",
            "policy_profile.include_bio_seq must be a boolean.",
            instance="/v1/screen",
        )

    include_session_context = policy_profile.get("include_session_context", True)
    if include_session_context is not None and not isinstance(include_session_context, bool):
        return None, _problem(
            422,
            "Unsupported feature",
            "policy_profile.include_session_context must be a boolean.",
            instance="/v1/screen",
        )

    return {
        "mode": mode,
        "threshold_allow": threshold_allow,
        "threshold_review": threshold_review,
        "include_bio_seq": include_bio_seq,
        "include_session_context": bool(include_session_context),
    }, None


def _validate_turns(turns: Any) -> tuple[List[Dict[str, Any]] | None, Dict[str, Any] | None]:
    if not isinstance(turns, list) or len(turns) == 0:
        return None, _problem(
            400,
            "Invalid request payload",
            "turns must be a non-empty array.",
            instance="/v1/screen",
        )

    valid_turns: List[Dict[str, Any]] = []
    for position, turn in enumerate(turns):
        if not isinstance(turn, dict):
            return None, _problem(
                400,
                "Invalid request payload",
                f"turns[{position}] must be an object.",
                instance="/v1/screen",
            )
        extras = set(turn) - SCREEN_ALLOWED_TURN_KEYS
        if extras:
            return None, _problem(
                400,
                "Invalid request payload",
                f"turns[{position}] has unsupported fields: {','.join(sorted(extras))}",
                instance="/v1/screen",
            )
        actor = turn.get("actor")
        if actor not in SCREEN_ACTORS:
            return None, _problem(
                400,
                "Invalid request payload",
                f"turns[{position}].actor must be one of user|assistant|system.",
                instance="/v1/screen",
            )
        text = turn.get("text")
        if not isinstance(text, str):
            return None, _problem(
                400,
                "Invalid request payload",
                f"turns[{position}].text must be a string.",
                instance="/v1/screen",
            )
        index = turn.get("index")
        if not isinstance(index, int) or index < 0:
            return None, _problem(
                400,
                "Invalid request payload",
                f"turns[{position}].index must be a non-negative integer.",
                instance="/v1/screen",
            )
        valid_turns.append(turn)
    return valid_turns, None


def _envelope_hash(envelope: Dict[str, Any]) -> str:
    canonical = {
        "request_id": envelope["request_id"],
        "conversation_id": envelope["conversation_id"],
        "decision": envelope["decision"],
        "policy_profile": envelope["policy_profile"],
        "bkt_event_ids": [event["event_id"] for event in envelope["bkt_events"]],
        "host_context": envelope["host_context"],
    }
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _derive_event_flags(event: Dict[str, Any]) -> List[str]:
    labels = [event["scope"]["label"], event["depth"]["label"], event["uplift"]["label"]]
    flags: List[str] = []
    if "critical" in labels[:2]:
        flags.append("critical_scope_or_depth")
    if labels.count("high") >= 2:
        flags.append("two_high_dimensions")
    return flags


def _max_dimension(events: List[Dict[str, Any]], key_name: str) -> Dict[str, Any]:
    best = max(events, key=lambda event: event[key_name]["score"])
    return {
        "score": best[key_name]["score"],
        "label": best[key_name]["label"],
        "reason": best[key_name]["reason"],
    }


def screen(payload: Dict[str, Any], contract: Dict[str, Any], *, include_sequences: bool = False) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return _problem(
            400,
            "Invalid request payload",
            "request payload must be a JSON object.",
            instance="/v1/screen",
        )

    missing = sorted(k for k in SCREEN_REQUIRED_KEYS if k not in payload)
    if missing:
        return _problem(
            400,
            "Invalid request payload",
            f"Missing required request fields: {','.join(missing)}",
            instance="/v1/screen",
        )

    extra_keys = set(payload) - SCREEN_ALLOWED_KEYS
    if extra_keys:
        return _problem(
            400,
            "Invalid request payload",
            f"Unsupported request fields: {','.join(sorted(extra_keys))}",
            instance="/v1/screen",
        )

    if not _is_uuid(payload.get("request_id")):
        return _problem(
            400,
            "Invalid request payload",
            "request_id must be a valid UUID.",
            instance="/v1/screen",
        )
    if not isinstance(payload.get("conversation_id"), str) or not payload.get("conversation_id"):
        return _problem(
            400,
            "Invalid request payload",
            "conversation_id must be a non-empty string.",
            instance="/v1/screen",
        )
    if not isinstance(payload.get("host_id"), str) or not payload.get("host_id"):
        return _problem(
            400,
            "Invalid request payload",
            "host_id must be a non-empty string.",
            instance="/v1/screen",
        )

    contract_version = payload.get("contract_version", contract.get("contract_version"))
    if contract_version != contract.get("contract_version"):
        return _problem(
            422,
            "Unsupported contract",
            f"unsupported_contract={contract_version}",
            instance="/v1/screen",
        )

    turns, turn_err = _validate_turns(payload.get("turns"))
    if turn_err:
        return turn_err

    policy_profile, policy_err = _sanitize_policy_profile(payload, contract_version=contract_version)
    if policy_err:
        return policy_err

    turns = turns or []
    request_id = str(payload["request_id"])
    contract_thresholds = contract.get("scoring", {}).get("thresholds", {})
    policy_profile.setdefault("threshold_allow", contract_thresholds.get("allow", 0.45))
    policy_profile.setdefault("threshold_review", contract_thresholds.get("review", 0.75))
    policy_profile.setdefault("include_bio_seq", bool(include_sequences))
    policy_profile.setdefault("include_session_context", True)

    selected_turns = turns[-4:] if len(turns) > 4 else turns
    event_ts = utcnow_iso()
    events = []
    for idx, t in enumerate(selected_turns, start=0):
        actor = t.get("actor", "user")
        text = str(t.get("text", ""))
        if not text.strip():
            continue
        turn_index = t.get("index", idx)
        if not isinstance(turn_index, int) or turn_index < 0:
            return _problem(
                400,
                "Invalid request payload",
                f"turn index must be non-negative integer. received {turn_index!r}",
                instance="/v1/screen",
            )
        event = make_event(
            turn_index=turn_index,
            actor=actor,
            turns=[turn_index],
            turn_text=text,
            contract=contract,
            policy_profile=policy_profile,
            conversation_id=payload["conversation_id"],
            event_ts_utc=event_ts,
        )
        events.append(event)

    if not events:
        return {
            "type": "https://bioguard.invalid/request",
            "title": "No usable turns",
            "status": 400,
            "detail": "turn texts empty",
            "instance": "/v1/screen",
        }

    best_event = max(events, key=lambda event: event["composite_score"])
    flags = []
    for event in events:
        flags.extend(_derive_event_flags(event))
    dims = (
        _max_dimension(events, "scope"),
        _max_dimension(events, "depth"),
        _max_dimension(events, "uplift"),
        best_event["composite_score"],
        best_event["composite_label"],
        list(set(flags)),
    )
    decision = decision_from_dimensions(contract, dims, unknown=False)
    event_reason = make_event_rationale(best_event, decision)

    decision_reason = event_reason if len(event_reason) <= 240 else event_reason[:237] + "..."
    policy_profile["include_bio_seq"] = bool(include_sequences)
    policy_profile.setdefault("include_session_context", True)

    envelope = {
        "request_id": request_id,
        "conversation_id": payload["conversation_id"],
        "request_ts_utc": event_ts,
        "generated_at_utc": event_ts,
        "model_id": payload.get("model_id", "gpt-5.4"),
        "policy_profile": policy_profile,
        "decision": decision,
        "decision_reason": decision_reason,
        "bkt_events": events,
        "host_context": {
            "host_id": payload.get("host_id", DEFAULT_HOST_ID),
            "skill_id": payload.get("skill_id", "bioguard-bio-trace"),
            "contract_version": contract["contract_version"],
            "artifact_version": "mvp-0.1.0",
        },
    }
    if include_sequences:
        envelope["sequence_findings"] = []
    envelope["decision_hash"] = _envelope_hash(envelope)
    return envelope


def evaluate_metric_request(payload: Dict[str, Any], evaluator) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return _problem(400, "Invalid request payload", "request payload must be a JSON object.", instance="/v1/evaluate")

    allowed_keys = {
        "request_id",
        "dataset_manifest",
        "splits",
        "baselines",
        "include_bootstrap",
        "seed",
        "baseline_seed",
        "seeds",
        "bootstrap_reps",
    }
    extras = set(payload) - allowed_keys
    if extras:
        return _problem(400, "Invalid request payload", f"unsupported fields: {','.join(sorted(extras))}", instance="/v1/evaluate")

    if "request_id" not in payload:
        return _problem(400, "Invalid request payload", "request_id is required.", instance="/v1/evaluate")
    if not _is_uuid(payload.get("request_id")):
        return _problem(400, "Invalid request payload", "request_id must be a valid UUID.", instance="/v1/evaluate")

    if "dataset_manifest" not in payload:
        return _problem(400, "Invalid request payload", "dataset_manifest is required.", instance="/v1/evaluate")
    dataset_manifest = payload.get("dataset_manifest")
    if not isinstance(dataset_manifest, str) or not dataset_manifest:
        return _problem(
            400,
            "Invalid request payload",
            "dataset_manifest must be a non-empty string path.",
            instance="/v1/evaluate",
        )

    splits = payload.get("splits")
    valid_splits = {"train", "dev", "test", "all"}
    if splits is None:
        splits = ["test"]
    if not isinstance(splits, list) or not splits:
        return _problem(400, "Invalid request payload", "splits must be a non-empty array.", instance="/v1/evaluate")
    if any(s not in valid_splits for s in splits):
        return _problem(
            400,
            "Invalid request payload",
            "splits must be one of train, dev, test, all.",
            instance="/v1/evaluate",
        )

    baselines = payload.get("baselines")
    valid_baselines = {
        "bioguard",
        "llama-guard-3",
        "keyword-filter",
        "gpt54-zero-shot",
        "pre-inference-only",
        "post-inference-only",
    }
    if not isinstance(baselines, list) or not baselines:
        return _problem(400, "Invalid request payload", "baselines must be a non-empty array.", instance="/v1/evaluate")
    if any(baseline not in valid_baselines for baseline in baselines):
        return _problem(400, "Invalid request payload", "unsupported baseline in request.", instance="/v1/evaluate")
    if "request_id" in payload and not _is_uuid(payload["request_id"]):
        return _problem(400, "Invalid request payload", "request_id must be a valid UUID.", instance="/v1/evaluate")

    include_bootstrap = payload.get("include_bootstrap", True)
    if include_bootstrap is not None and not isinstance(include_bootstrap, bool):
        return _problem(400, "Invalid request payload", "include_bootstrap must be a boolean.", instance="/v1/evaluate")
    include_bootstrap = bool(include_bootstrap)

    seed = payload.get("seed", 1)
    if seed is not None and not isinstance(seed, int):
        return _problem(400, "Invalid request payload", "seed must be an integer.", instance="/v1/evaluate")
    baseline_seed = payload.get("baseline_seed", seed)
    if baseline_seed is not None and not isinstance(baseline_seed, int):
        return _problem(400, "Invalid request payload", "baseline_seed must be an integer.", instance="/v1/evaluate")
    seeds = payload.get("seeds")
    if seeds is not None:
        if not isinstance(seeds, list) or any(not isinstance(item, int) for item in seeds):
            return _problem(400, "Invalid request payload", "seeds must be an array of integers.", instance="/v1/evaluate")
    bootstrap_reps = payload.get("bootstrap_reps", 2000)
    if bootstrap_reps is not None and not isinstance(bootstrap_reps, int):
        return _problem(400, "Invalid request payload", "bootstrap_reps must be an integer.", instance="/v1/evaluate")

    result = evaluator(
        dataset_manifest,
        baselines,
        seed=seed if seed is not None else 1,
        splits=splits,
    )
    metrics = result.get("metrics", [])
    normalized_metrics = []
    for row in metrics:
        if not isinstance(row, dict):
            continue

        def _as_float(value: Any, fallback: float = 0.0) -> float:
            if value is None:
                return fallback
            try:
                return float(value)
            except (TypeError, ValueError):
                return fallback

        def _as_int(value: Any, fallback: int = 0) -> int:
            if value is None:
                return fallback
            try:
                return int(value)
            except (TypeError, ValueError):
                return fallback

        def _as_bool(value: Any, fallback: bool = False) -> bool:
            return bool(value) if isinstance(value, (bool, int)) else fallback

        normalized_metrics.append(
            {
                "condition": row.get("condition"),
                "recall_at_fpr_5": _as_float(row.get("recall_at_fpr_5"), 0.0),
                "ci95_low": _as_float(row.get("ci95_low"), 0.0),
                "ci95_high": _as_float(row.get("ci95_high"), 0.0),
                "ppv": _as_float(row.get("ppv"), 0.0),
                "specificity": _as_float(row.get("specificity"), 0.0),
                "fpr": _as_float(row.get("fpr"), 0.0),
                "samples": _as_int(row.get("samples"), 0),
                "seed": _as_int(row.get("seed"), payload.get("seed", 1) or 1),
                "tier": row.get("tier", ""),
                "significant_vs_baseline": _as_bool(row.get("significant_vs_baseline"), False),
                "latency_p95_ms": _as_float(row.get("latency_p95_ms"), 0.0),
            }
        )
    result = dict(result)
    result["metrics"] = normalized_metrics

    return {
        "request_id": payload.get("request_id") or deterministic_uuid(str(dataset_manifest)),
        "run_id": deterministic_uuid("run:" + str(dataset_manifest)),
        "metrics": normalized_metrics,
        "artifact_paths": {
            "metrics_json": "artifacts/metrics/results.json",
            "confusion_table": "artifacts/metrics/confusion_matrix.csv",
            "plots": [],
        },
    }
