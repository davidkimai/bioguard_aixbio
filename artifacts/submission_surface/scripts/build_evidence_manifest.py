"""Builds evidence manifest files for a concrete submission run."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "artifacts" / "evidence"
COMMANDS = [
    "make init",
    "python -m bioguard check",
    "python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl",
    "python -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl",
    "python -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl",
    "make skills",
    "python -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --seed 1 --splits test --out artifacts/metrics",
    "python -m bioguard state --state artifacts/checks/execution_state.json",
]


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    generated_at_utc = utcnow_iso()
    bundle_manifest = {
        "bundle_version": "1.1",
        "contract_version": "bkt-v1.0",
        "generated_at_utc": generated_at_utc,
        "items": [
            "artifacts/checks/protocol_lock.json",
            "artifacts/records/seed_screen.jsonl",
            "artifacts/records/screen_bad_request.jsonl",
            "artifacts/records/screen_bad_contract.jsonl",
            "artifacts/records/skill_bkt_scoring.json",
            "artifacts/records/skill_bio_trace.json",
            "artifacts/records/skill_bio_guard.json",
            "artifacts/records/skill_bio_seq.json",
            "artifacts/metrics/results.json",
            "artifacts/metrics/bootstrap.csv",
            "artifacts/metrics/confusion_matrix.csv",
            "artifacts/metrics/case_predictions.jsonl",
            "artifacts/metrics/case_summary.json",
            "artifacts/metrics/outcome.json",
            "artifacts/metrics/reproducibility.json",
            "artifacts/metrics/reproducibility.md",
            "artifacts/metrics/hackathon_results.md",
            "artifacts/metrics/ablation_results.md",
            "artifacts/conformance/deviation_matrix.csv",
            "artifacts/conformance/deviation_matrix.json",
            "artifacts/conformance/conformance_report.md",
            "artifacts/conformance/host_capability_profile.json",
            "artifacts/conformance/host_capability_profile_host-2.json",
            "artifacts/conformance/host_capability_profile_host-3.json",
            "artifacts/checks/execution_state.json",
            "artifacts/docs/Limitations_DualUse.md",
            "artifacts/docs/report_draft.md",
        ],
    }

    entries = []
    for item in bundle_manifest["items"]:
        payload = {
            "path": item,
            "sha256": sha256_file(ROOT / item) if (ROOT / item).exists() else "",
            "size_bytes": (ROOT / item).stat().st_size if (ROOT / item).exists() else 0,
            "generated_at_utc": generated_at_utc,
            "command": None,
        }
        if item.endswith("artifacts/records/seed_screen.jsonl"):
            payload["command"] = "python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl"
        elif item.endswith("artifacts/records/screen_bad_request.jsonl"):
            payload["command"] = "python -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl"
        elif item.endswith("artifacts/records/screen_bad_contract.jsonl"):
            payload["command"] = "python -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl"
        elif item.endswith("artifacts/records/skill_bkt_scoring.json"):
            payload["command"] = "python scripts/bioguard_skill_proxy.py --mode bkt-scoring --input artifacts/requests/skill_bkt_request.json --out artifacts/records/skill_bkt_scoring.json"
        elif item.endswith("artifacts/records/skill_bio_trace.json"):
            payload["command"] = "python scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json --out artifacts/records/skill_bio_trace.json"
        elif item.endswith("artifacts/records/skill_bio_guard.json"):
            payload["command"] = "python scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json --out artifacts/records/skill_bio_guard.json"
        elif item.endswith("artifacts/records/skill_bio_seq.json"):
            payload["command"] = "python scripts/bioguard_skill_proxy.py --mode bio-seq --input artifacts/requests/skill_bio_seq_request.json --out artifacts/records/skill_bio_seq.json"
        elif item.startswith("artifacts/metrics/"):
            payload["command"] = "python -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --seed 1 --splits test --out artifacts/metrics"
        elif item == "artifacts/conformance/deviation_matrix.json":
            payload["command"] = "Manual portability matrix capture for host conformance."
        elif item == "artifacts/conformance/deviation_matrix.csv":
            payload["command"] = "Manual portability matrix capture for host conformance."
        elif item == "artifacts/conformance/conformance_report.md":
            payload["command"] = "Manual portability report synthesis from profile and matrix artifacts."
        elif item.startswith("artifacts/conformance/host_capability_profile"):
            payload["command"] = "Manual host capability profile capture."
        elif item.startswith("artifacts/checks/protocol_lock"):
            payload["command"] = "python -m bioguard check"
        elif item.startswith("artifacts/checks/execution_state"):
            payload["command"] = "python -m bioguard state --state artifacts/checks/execution_state.json"
        elif "docs" in item:
            payload["command"] = "manual"
        entries.append(payload)

    bundle_payload = {
        "bundle_version": bundle_manifest["bundle_version"],
        "contract_version": bundle_manifest["contract_version"],
        "generated_at_utc": generated_at_utc,
        "items": entries,
    }
    (EVIDENCE / "bundle_manifest.json").write_text(json.dumps(bundle_payload, indent=2) + "\n", encoding="utf-8")

    report_index = {
        "path": "artifacts/docs/report_draft.md",
        "index_version": "1.1",
        "commands": COMMANDS + ["python3 scripts/build_evidence_manifest.py"],
        "evidence_records": [entry["path"] for entry in entries],
    }
    (EVIDENCE / "report_index.json").write_text(json.dumps(report_index, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
