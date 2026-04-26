---
name: bioguard-bio-trace
description: Context-aware BKT tracing for BioGuard. Use when screening a conversation window for dangerous biological knowledge transfer before or after model inference.
---

# BioGuard Bio Trace

This skill screens a conversation window for BKT events before and after inference.
It returns a contract-aligned decision envelope that follows
`spec/decision_envelope.schema.json`.

## Use this skill when

- you need pre-inference screening on the incoming user prompt
- you need post-inference screening on a model response
- you need a portable `SKILL.md` entrypoint that matches the BioGuard `/v1/screen` contract

## Input

Provide a BioGuard screen payload with:

- `request_id`
- `conversation_id`
- `turns`
- `policy_profile`
- `host_id`
- `contract_version`

## Output

Returns the canonical screen fields used by this project:

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
- optional `decision_hash`

## Invocation

```bash
python3 scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json
```

## Error and safe fallback

- If all turns are blank, this returns a typed invalid-request response.
- If contract validation fails, execution returns a typed failure record with `type`,
  `title`, and `detail`.

## Notes

- This is the main measurement surface for the protocol thesis.
- It is the primary skill used for one-host hackathon validation.
