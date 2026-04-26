---
name: bioguard-bkt-scoring
description: Use when a host needs a single context-to-context event score from one prompt fragment using the BioGuard Biological Knowledge Transfer (BKT) contract.
license: Apache-2.0
version: 1.0.0
---

# BioGuard BKT Scoring (Protocol Kernel)

This skill is the canonical event-scoring adapter for the BioGuard protocol.
It converts one text fragment into one BKT event object that is compatible with
`spec/bkt_event.schema.json`.

## Use this skill when

- you need a BKT event from a single user or assistant turn
- you need contract-consistent `scope`, `depth`, and `uplift` scoring
- you are calibrating host portability against the canonical BKT contract

Do not use this as a policy decision layer. It only provides one event-level
signal.

## Input

Provide JSON with:

- `text`
- optional `actor`
- optional `turn_index`
- optional `conversation_id`
- optional `policy_profile`

If `policy_profile` is absent, the host uses conservative defaults. If `text` is
missing or blank, the skill returns `{"status":"error"}`.

## Output

Returns JSON with:

- `status`: `ok` or `error`
- `block`: event block id and contract provenance
- `event`: canonical BKT event object compatible with `spec/bkt_event.schema.json`
- `decision_hash` is not returned by this block; it is added by the guard block.

## Invocation

```bash
python3 scripts/bioguard_skill_proxy.py --mode bkt-scoring
```

Expected behavior:

```bash
python3 scripts/bioguard_skill_proxy.py \
  --mode bkt-scoring \
  --input artifacts/requests/skill_bkt_request.json
```

Returns one event payload so host replay is deterministic.

## Validation

- Verify with: `python3 -m bioguard check`
- Execute smoke test after any contract change
- Keep the `event` schema stable for cross-host portability

## Notes

- This skill is the smallest portable unit of the protocol.
- It does not own session aggregation or final operator action.
- Final policy decisions belong to `bioguard-bio-guard`.
