---
name: bioguard-bkt-scoring
description: Canonical BKT scoring contract adapter for BioGuard. Use when a host needs one event-level BKT score from a single turn or short prompt fragment.
---

# BioGuard BKT Scoring

This skill is the canonical event-scoring adapter for the BioGuard protocol.

## Use this skill when

- you need a BKT event from a single user or assistant turn
- you need contract-consistent `scope`, `depth`, and `uplift` scoring
- you are calibrating or testing host portability against the canonical BKT contract

## Input

Provide JSON with:

- `text`
- optional `actor`
- optional `turn_index`
- optional `conversation_id`
- optional `policy_profile`

## Output

Returns JSON with:

- `block`
- `status`
- `event`

The `event` must remain compatible with `spec/bkt_event.schema.json`.

## Invocation

```bash
python scripts/bioguard_skill_proxy.py --mode bkt-scoring
```

## Notes

- This skill is the smallest portable unit of the protocol.
- It does not own session aggregation or final operator action.
- Final policy decisions belong to `bioguard-bio-guard`.
