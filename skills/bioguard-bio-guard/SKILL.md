---
name: bioguard-bio-guard
description: Runs the full BioGuard operator-facing screen. Use when a host needs pre/post conversation screening, BKT aggregation, a final allow/review/block decision, and one auditable decision envelope.
license: Apache-2.0
version: 1.0.0
compatibility: Agent Skills-compatible hosts with Python 3.11 and repo access.
---

# BioGuard Bio Guard

## Purpose

Use this skill as the main BioGuard entrypoint. It wraps the lower-level scoring and tracing behavior into one operator-facing result.

## Inputs

Provide a BioGuard screen payload:

- `request_id`: UUID
- `conversation_id`: string
- `turns`: structured conversation turns
- `policy_profile`: `mode`, `threshold_allow`, and `threshold_review`
- `host_id`: host label
- `contract_version`: optional contract selector
- `include_sequences`: optional boolean

## Workflow

1. Validate request fields and contract version.
2. Score BKT events across the conversation window.
3. Aggregate events under the policy thresholds.
4. Return one decision envelope for operator review or automated gating.
5. Keep optional sequence checks secondary to the conversation-level decision.

## Output

Returns a decision envelope with:

- request identifiers
- timestamps
- policy profile
- decision: `allow`, `review`, or `block`
- decision reason
- BKT events
- host context
- optional sequence findings
- optional human override fields
- decision hash

## Smoke Test

```bash
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py \
  --mode bio-guard \
  --input artifacts/requests/seed_request.json
```

Recommended full check:

```bash
PYTHONPATH=src python3 -m bioguard screen \
  --request artifacts/requests/seed_request.json \
  --out /tmp/seed_screen.jsonl
PYTHONPATH=src python3 -m bioguard check
```

## Failure Behavior

- Missing required fields return `Invalid request payload`.
- Unsupported contract versions return `Unsupported contract`.
- Empty turns return an invalid-request record.
- Successful runs always return a complete auditable envelope.

## Safety Notes

Use `review` rather than `allow` when the signal is ambiguous but biologically consequential. Do not expose raw high-risk biological content in public decision traces.
