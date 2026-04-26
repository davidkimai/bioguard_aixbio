---
name: bioguard-bio-guard
description: Operator-facing BioGuard orchestration layer. Use when a host needs pre/post screening and a single auditable decision envelope.
---

# BioGuard Guard

This is the operator-facing wrapper for BioGuard.
Use it when a host should apply the full protocol (pre- and post-inference),
return one auditable decision envelope, and keep decisions reproducible.

## When to use

- A host needs a consistent safety boundary before and after model output.
- Operators need one actionable output with rationale and uncertainty.
- You need protocol parity across hosts using the same contract version.

## Inputs

- `request_id`: UUID
- `conversation_id`: conversation context identifier
- `turns`: list of structured turns, each with `actor`, `text`, and `index`
- `policy_profile`:
  - `mode`: `allow`, `review`, or `block`
  - `threshold_allow`: numeric threshold
  - `threshold_review`: numeric threshold
- `host_id`: optional host label
- `contract_version`: optional override; defaults to current contract

If `contract_version` is missing or mismatched, this block returns a typed
contract failure.

## Output

Returns a BioGuard decision envelope with:

- `request_id`
- `conversation_id`
- `request_ts_utc`
- `generated_at_utc`
- `model_id`
- `policy_profile`
- `decision`
- `decision_reason`
- `bkt_events`
- `host_context`
- optional `sequence_findings`
- optional `human_override`
- optional `remediation_notes`
- optional `decision_hash`

## Decision policy

- `allow`: low-confidence or low-risk aggregation
- `review`: suspicious or uncertain transfer indicators
- `block`: high-confidence harmful transfer signal

## Error behavior

- Missing required fields: returns a typed request failure object.
- Unsupported contract: returns a typed contract failure object.
- Empty or invalid turns: returns a typed request failure object.
- Any successful run always returns a complete auditable envelope.

## Invocation

```bash
python3 scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json
```

Recommended smoke test:

```bash
python3 -m bioguard screen --request artifacts/requests/seed_request.json --out /tmp/seed_screen.jsonl
python3 -m bioguard check
```

## Notes and scope

- This is the deployable skill for hackathon demos and host-path smoke tests.
- The protocol source of truth is `spec/*`, not this file.
- Keep sequence checks as a secondary pass.
- Do not expose raw sequence content in unredacted artifacts.
