"""Core request handling and envelope construction."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

from .config import DEFAULT_HOST_ID
from .scoring import decision_from_dimensions, make_event, make_event_rationale
from .utils import deterministic_uuid, utcnow_iso


def _validate_screen_request(payload: Dict[str, Any]) -> List[str]:
    required = ["request_id", "conversation_id", "turns", "policy_profile", "host_id"]
    errors = []
    for key in required:
        if key not in payload:
            errors.append(key)
    if not isinstance(payload.get("turns"), list) or len(payload.get("turns", [])) == 0:
        errors.append("turns_nonempty")
    return errors


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


def screen(payload: Dict[str, Any], contract: Dict[str, Any], *, include_sequences: bool = False) -> Dict[str, Any]:
    missing = _validate_screen_request(payload)
    if missing:
        return {
            "type": "https://bioguard.invalid/request",
            "title": "Invalid request payload",
            "status": 400,
            "detail": f"missing_fields={','.join(missing)}",
            "instance": "/v1/screen",
        }

    turns = payload["turns"]
    request_id = payload["request_id"] or deterministic_uuid(payload["conversation_id"])
    contract_version = payload.get("contract_version", contract["contract_version"])
    if contract_version != contract["contract_version"]:
        return {
            "type": "https://bioguard.invalid/contract",
            "title": "Contract mismatch",
            "status": 422,
            "detail": f"unsupported_contract={contract_version}",
            "instance": "/v1/screen",
        }
    policy_profile = dict(payload.get("policy_profile", {}))
    policy_profile.setdefault("mode", "review")
    policy_profile.setdefault("threshold_allow", contract["scoring"]["thresholds"]["allow"])
    policy_profile.setdefault("threshold_review", contract["scoring"]["thresholds"]["review"])
    policy_profile.setdefault("include_bio_seq", bool(include_sequences))
    policy_profile.setdefault("include_session_context", True)

    selected_turns = turns[-4:] if len(turns) > 4 else turns
    event_ts = utcnow_iso()
    events = []
    for idx, t in enumerate(selected_turns, start=0):
        if not isinstance(t, dict):
            continue
        actor = t.get("actor", "user")
        text = str(t.get("text", ""))
        if not text.strip():
            continue
        turn_index = int(t.get("index", idx))
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

    last_event = events[-1]
    labels = [last_event["scope"]["label"], last_event["depth"]["label"], last_event["uplift"]["label"]]
    flags = []
    if "critical" in labels[:2]:
        flags.append("critical_scope_or_depth")
    if labels.count("high") >= 2:
        flags.append("two_high_dimensions")
    dims = (
        {"score": last_event["scope"]["score"], "label": last_event["scope"]["label"], "reason": last_event["scope"]["reason"]},
        {"score": last_event["depth"]["score"], "label": last_event["depth"]["label"], "reason": last_event["depth"]["reason"]},
        {"score": last_event["uplift"]["score"], "label": last_event["uplift"]["label"], "reason": last_event["uplift"]["reason"]},
        last_event["composite_score"],
        last_event["composite_label"],
        flags,
    )
    decision = decision_from_dimensions(contract, dims, unknown=False)
    event_reason = make_event_rationale(last_event, decision)

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
    # Placeholder for server-style compatibility with /v1/evaluate.
    result = evaluator(payload)
    return {
        "request_id": payload.get("request_id") or deterministic_uuid(str(payload)),
        "run_id": deterministic_uuid("run:" + str(payload)),
        "metrics": result,
        "artifact_paths": {
            "metrics_json": "artifacts/metrics/results.json",
            "confusion_table": "artifacts/metrics/confusion_matrix.csv",
            "plots": [],
        },
        "generated_at_utc": utcnow_iso(),
    }
