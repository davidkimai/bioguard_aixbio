---
name: bioguard-bkt-scoring
description: Scores one text fragment as a BioGuard Biological Knowledge Transfer event. Use when a host needs scope, depth, uplift, and rationale for a single conversation turn or extracted span.
license: Apache-2.0
version: 1.0.0
compatibility: Agent Skills-compatible hosts with Python 3.11 and repo access.
---

# BioGuard BKT Scoring

## Purpose

Use this skill to turn one text fragment into one BKT event. It is the smallest BioGuard unit. It does not make the final policy decision.

## Inputs

Provide JSON with:

- `text`: required string
- `actor`: optional, defaults to `user`
- `turn_index`: optional integer
- `conversation_id`: optional string
- `policy_profile`: optional object

## Workflow

1. Read the input JSON.
2. Score the text for BKT scope, depth, and uplift.
3. Return one event compatible with `spec/bkt_event.schema.json`.
4. Leave final aggregation to `bioguard-bio-guard`.

## Output

Returns:

- `status`: `ok` or `error`
- `block`: skill and contract provenance
- `event`: canonical BKT event

The output should not include a final `decision_hash`; that belongs to the guard skill.

## Smoke Test

```bash
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py \
  --mode bkt-scoring \
  --input artifacts/requests/skill_bkt_request.json
```

Expected result: one `ok` payload with an `event` object.

## Failure Behavior

- Missing or blank `text` returns `status: error`.
- Invalid JSON returns a typed tool error.
- Contract changes require `PYTHONPATH=src python3 -m bioguard check`.

## Safety Notes

Keep rationales short. Explain why a fragment was risky without adding new biological instructions.
