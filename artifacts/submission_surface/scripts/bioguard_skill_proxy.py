#!/usr/bin/env python3
"""Skill adapter entrypoints for BioGuard Agent Skills blocks."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from bioguard.config import DEFAULT_CONTRACT, ROOT as REPO_ROOT
from bioguard.core import screen as core_screen
from bioguard.scoring import make_event
from bioguard.utils import read_json


def _load_contract(path: str | None) -> dict:
    if path:
        try:
            return read_json(path)
        except Exception:
            pass
    return read_json(str(DEFAULT_CONTRACT))


def _read_payload(file_path: str | None = None) -> dict:
    if file_path:
        return read_json(file_path)
    return json.loads(sys.stdin.read() or "{}")


def cmd_bkt_scoring(payload: dict, contract_path: str | None = None) -> dict:
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"status": "error", "detail": "missing required field: text"}
    contract = _load_contract(contract_path)
    event = make_event(
        turn_index=int(payload.get("turn_index", 0)),
        actor=payload.get("actor", "user"),
        turns=[int(payload.get("turn_index", 0))],
        turn_text=text,
        contract=contract,
        conversation_id=str(payload.get("conversation_id", "bioguard-session")),
        policy_profile=payload.get("policy_profile"),
        event_ts_utc=None,
    )
    return {
        "block": "bioguard-bkt-scoring",
        "status": "ok",
        "event": event,
    }


def cmd_bio_trace(payload: dict, contract_path: str | None = None) -> dict:
    contract = _load_contract(contract_path)
    include_sequences = bool(payload.get("include_sequences", False))
    return core_screen(payload, contract, include_sequences=include_sequences)


def cmd_bio_guard(payload: dict, contract_path: str | None = None) -> dict:
    contract = _load_contract(contract_path)
    include_sequences = bool(payload.get("include_sequences", False))
    return core_screen(payload, contract, include_sequences=include_sequences)


def cmd_bio_seq(payload: dict) -> dict:
    sequence = payload.get("sequence", "")
    if not sequence:
        return {
            "status": "skip",
            "block": "bioguard-bio-seq",
            "reason": "no_sequence",
            "detail": "bio-seq block is optional and currently emits placeholder findings.",
        }
    return {
        "status": "ok",
        "block": "bioguard-bio-seq",
        "sequence_hash": f"sha256:{hashlib.sha256(str(sequence).encode('utf-8')).hexdigest()}",
        "findings": [],
        "risk_profile": "placeholder",
        "notes": "Optional ablation module not yet wired to a dedicated toxicity model.",
    }


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bioguard_skill_proxy.py")
    parser.add_argument("--mode", required=True, choices=["bkt-scoring", "bio-trace", "bio-guard", "bio-seq"])
    parser.add_argument("--input", help="Path to JSON payload (defaults to stdin).")
    parser.add_argument("--contract", help="Optional path to alternate BKT contract JSON.")
    parser.add_argument("--out", help="Optional output file path.")
    return parser


def main() -> int:
    args = _make_parser().parse_args()
    payload = _read_payload(args.input)
    contract_path = args.contract

    if args.mode == "bkt-scoring":
        result = cmd_bkt_scoring(payload, contract_path=contract_path)
    elif args.mode == "bio-trace":
        result = cmd_bio_trace(payload, contract_path=contract_path)
    elif args.mode == "bio-guard":
        result = cmd_bio_guard(payload, contract_path=contract_path)
    else:
        result = cmd_bio_seq(payload)

    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0 if result.get("status", "ok") != "error" else 2


if __name__ == "__main__":
    raise SystemExit(main())
