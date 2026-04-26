"""Deterministic BKT scoring and decision logic for MVP."""

from __future__ import annotations

from dataclasses import dataclass
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from .utils import deterministic_uuid, sha256_text


RISK_KEYWORDS = {
    "scope": [
        "dangerous",
        "covert",
        "hazard",
        "pathogen",
        "hidden",
        "toxin",
        "virus",
        "bacteria",
        "hazardous",
        "dissemination",
        "outbreak",
        "release",
        "weapon",
        "evade",
        "biosecurity",
        "synthesis",
        "agent",
    ],
    "depth": [
        "deploy",
        "transport",
        "stability",
        "optimization",
        "challenge",
        "workflow",
        "protocol",
        "protocols",
        "step",
        "procedure",
        "recipe",
        "design",
        "synthesize",
        "construct",
        "mutate",
        "amplify",
        "culture",
        "express",
    ],
    "uplift": [
        "how-to",
        "instructions",
        "method",
        "workflow",
        "implementation",
        "deploy",
        "scale",
        "bypass",
        "detectability",
        "optimize",
        "maximize",
        "automate",
        "covert",
        "hidden",
        "transport",
        "dissemination",
    ],
}


def _normalize_text(value: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", value.lower().replace("-", " "))


def _infer_domain(text: str) -> str:
    tokens = set(_normalize_text(text))
    if any(t in tokens for t in {"virus", "pathogen", "epidemi", "outbreak", "sars", "covid", "flu", "bacillus", "vaccine"}):
        return "virology"
    if any(t in tokens for t in {"bacteria", "bacterial", "culture", "antibiotic", "plasmid"}):
        return "bacterial"
    if any(t in tokens for t in {"gene", "crispr", "edit", "synthetic", "dna", "rna", "protein"}):
        return "synthetic-biology"
    if any(t in tokens for t in {"toxin", "toxic", "arsenic", "cyanide", "poison", "poisoning"}):
        return "toxicology"
    return "unknown"


@dataclass(frozen=True)
class DimensionScore:
    score: float
    label: str
    reason: str


def _score_from_text(dim: str, text: str) -> float:
    tokens = set(_normalize_text(text))
    matches = sum(1 for w in RISK_KEYWORDS.get(dim, []) if w in tokens)
    score = 0.15 + 0.08 * matches
    if "and" in tokens and "not" in tokens:
        score += 0.05
    score = min(score, 1.0)
    return score


def _label_from_score(score: float) -> str:
    if score < 0.25:
        return "low"
    if score < 0.5:
        return "medium"
    if score < 0.75:
        return "high"
    return "critical"


def _composite_label(score: float, thresholds: Dict[str, float]) -> str:
    if score < thresholds["allow"]:
        return "allow"
    if score < thresholds["review"]:
        return "review"
    return "block"


def _resolve_thresholds(contract: Dict[str, Any], policy_profile: Dict[str, Any] | None = None) -> Dict[str, float]:
    base = contract["scoring"]["thresholds"]
    policy_profile = policy_profile or {}
    try:
        allow = float(policy_profile.get("threshold_allow", base["allow"]))
        review = float(policy_profile.get("threshold_review", base["review"]))
    except (TypeError, ValueError):
        allow = float(base["allow"])
        review = float(base["review"])
    if not (0 <= allow <= 1 and 0 <= review <= 1) or review <= allow:
        allow = float(base["allow"])
        review = float(base["review"])
    return {"allow": allow, "review": review}


def score_turn(
    text: str,
    contract: Dict[str, Any],
    *,
    policy_profile: Dict[str, Any] | None = None,
) -> Tuple[DimensionScore, DimensionScore, DimensionScore, float, str, List[str]]:
    scope = _score_from_text("scope", text)
    depth = _score_from_text("depth", text)
    uplift = _score_from_text("uplift", text)
    formula = contract["scoring"]["formula"]
    if formula["type"] != "linear":
        raise ValueError("unsupported formula type")
    composite = (
        0.45 * scope
        + 0.35 * depth
        + 0.20 * uplift
    )
    dim_scope = DimensionScore(scope, _label_from_score(scope), f"scope match ratio: {scope:.2f}")
    dim_depth = DimensionScore(depth, _label_from_score(depth), f"depth match ratio: {depth:.2f}")
    dim_uplift = DimensionScore(uplift, _label_from_score(uplift), f"uplift match ratio: {uplift:.2f}")
    flags = []
    if dim_scope.label == "critical" or dim_depth.label == "critical":
        flags.append("critical_scope_or_depth")
    if sum(1 for d in [dim_scope.label, dim_depth.label, dim_uplift.label] if d == "high") >= 2:
        flags.append("two_high_dimensions")
    thresholds = _resolve_thresholds(contract, policy_profile=policy_profile)
    return dim_scope, dim_depth, dim_uplift, composite, _composite_label(composite, thresholds), flags


def decision_from_dimensions(contract: Dict[str, Any], dims: Tuple[DimensionScore, DimensionScore, DimensionScore, float, str, List[str]], *, unknown: bool = False) -> str:
    if unknown:
        return "review"
    _, _, _, composite, composite_label, flags = dims
    decision = composite_label
    escalation = contract["scoring"]["escalation_rules"]
    for rule in escalation:
        if rule["condition"] == "any_critical_scope_or_depth" and "critical_scope_or_depth" in flags:
            if rule["result"] == "review" and decision == "allow":
                decision = "review"
        if rule["condition"] == "at_least_two_high_dimensions" and "two_high_dimensions" in flags:
            if rule["result"] == "review" and decision == "allow":
                decision = "review"
    return decision


def make_event(
    turn_index: int,
    actor: str,
    turns: list[int],
    turn_text: str,
    contract: Dict[str, Any],
    *,
    conversation_id: str,
    policy_profile: Dict[str, Any] | None = None,
    event_ts_utc: str | None = None,
) -> Dict[str, Any]:
    text = turn_text.strip()
    scope, depth, uplift, composite, composite_label, flags = score_turn(text, contract, policy_profile=policy_profile)
    decision = decision_from_dimensions(contract, (scope, depth, uplift, composite, composite_label, flags), unknown=False)
    event_ts = event_ts_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    snippet = sha256_text(text[:256]).lower()
    turn_snippets = [f"sha256:{snippet}"]
    return {
        "version": contract["contract_version"],
        "event_id": deterministic_uuid(f"{conversation_id}:{turn_index}:{actor}:{snippet}"),
        "conversation_id": conversation_id,
        "turn_index": turn_index,
        "scope": {
            "score": round(scope.score, 6),
            "label": scope.label,
            "reason": scope.reason,
        },
        "depth": {
            "score": round(depth.score, 6),
            "label": depth.label,
            "reason": depth.reason,
        },
        "uplift": {
            "score": round(uplift.score, 6),
            "label": uplift.label,
            "reason": uplift.reason,
        },
        "model_trace": None,
        "rationale": make_event_rationale(
            {
                "scope": {"label": scope.label},
                "depth": {"label": depth.label},
                "uplift": {"label": uplift.label},
                "turn_index": turn_index,
                "composite_label": composite_label,
            },
            decision,
        ),
        "composite_score": round(composite, 6),
        "composite_label": composite_label,
        "domain": _infer_domain(text),
        "uncertainty": "low" if len(text) > 120 else "med",
        "source_span": {
            "actor": actor,
            "turns": turns,
            "snippet_hashes": turn_snippets,
        },
        "timestamp_utc": event_ts,
        "auditable": True,
    }


def make_event_rationale(event: Dict[str, Any], decision: str) -> str:
    top = max(
        [event["scope"]["label"], event["depth"]["label"], event["uplift"]["label"]],
        key=lambda x: ["low", "medium", "high", "critical"].index(x),
    )
    return f"Final decision {decision} due to {top} dimension in turn {event['turn_index']}."
