"""Shared constants and defaults for the BioGuard MVP."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "spec"
ARTIFACT_DIR = ROOT / "artifacts"
REQUESTS_DIR = ARTIFACT_DIR / "requests"
RECORDS_DIR = ARTIFACT_DIR / "records"
CHECKS_DIR = ARTIFACT_DIR / "checks"
METRICS_DIR = ARTIFACT_DIR / "metrics"
DOCS_DIR = ARTIFACT_DIR / "docs"

DEFAULT_CONTRACT = SPEC_DIR / "bkt_contract_v1.0.json"
DEFAULT_DECISION_SCHEMA = SPEC_DIR / "decision_envelope.schema.json"
DEFAULT_API_SPEC = SPEC_DIR / "bioguard_api.openapi.yaml"
DEFAULT_MANIFEST = SPEC_DIR / "benchmark_manifest_v1.0.json"
DEFAULT_EXECUTION_MANIFEST = SPEC_DIR / "execution_state_manifest_v1.0.json"
DEFAULT_ORCHESTRATION_MANIFEST = DEFAULT_EXECUTION_MANIFEST
BENCHMARK_MANIFEST_SCHEMA = SPEC_DIR / "benchmark_manifest.schema.json"
BKT_EVENT_SCHEMA = SPEC_DIR / "bkt_event.schema.json"
EXECUTION_STATE_SCHEMA = SPEC_DIR / "execution_state_manifest.schema.json"
ORCHESTRATION_SCHEMA = EXECUTION_STATE_SCHEMA
DEFAULT_EXECUTION_STATE_PATH = CHECKS_DIR / "execution_state.json"

DEFAULT_HOST_ID = "bioguard-host-1"
DEFAULT_SKILL_ID = "bioguard-bio-trace"
