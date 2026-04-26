---
name: bioguard-bio-trace
description: Screens a BioGuard conversation window for dangerous biological knowledge transfer. Use for pre-inference or post-inference tracing when the host needs BKT events and a contract-aligned decision envelope.
license: Apache-2.0
version: 1.0.0
compatibility: Agent Skills-compatible hosts with Python 3.11 and repo access.
---

# BioGuard Bio Trace

## Purpose

Use this skill when the important object is the conversation window, not one isolated fragment. It detects BKT events across turns and returns the canonical BioGuard screen output.

## Inputs

Provide the same payload used by `/v1/screen`:

- `request_id`: UUID
- `conversation_id`: string
- `turns`: list of `{actor, text, index}`
- `policy_profile`: mode and thresholds
- `host_id`: host label
- `contract_version`: optional, defaults to the current contract

## Workflow

1. Validate the request shape.
2. Validate the contract version.
3. Score non-empty turns for BKT events.
4. Return a decision envelope compatible with `spec/decision_envelope.schema.json`.

## Output

Returns the canonical screen fields:

- request and conversation identifiers
- policy profile
- decision and decision reason
- BKT events
- host context
- optional sequence findings
- decision hash

## Smoke Test

```bash
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py \
  --mode bio-trace \
  --input artifacts/requests/seed_request.json
```

Expected result: one decision envelope with at least one `bkt_events` entry for the seeded request.

## Failure Behavior

- Empty or malformed turns return a typed invalid-request record.
- Unsupported contract versions return a typed unsupported-contract record.
- Schema or contract edits require `PYTHONPATH=src python3 -m bioguard check`.

## Safety Notes

Do not expand risky biological content in rationales. Preserve enough context for audit, but keep public traces defensive and minimal.
