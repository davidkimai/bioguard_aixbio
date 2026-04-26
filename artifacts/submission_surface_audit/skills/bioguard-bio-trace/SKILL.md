---
name: bioguard-bio-trace
description: Context-aware BKT tracing for BioGuard. Use when screening a conversation window for dangerous biological knowledge transfer before or after model inference.
---

# BioGuard Bio Trace

This skill scores a conversation window for BKT events and returns a contract-aligned decision envelope.

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

Returns the same core screening payload as the canonical runtime:

- `decision`
- `decision_reason`
- `bkt_events`
- `host_context`
- optional `sequence_finding`

## Invocation

```bash
python scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json
```

## Notes

- This skill is the main measurement surface for the protocol thesis.
- It is the primary skill used for one-host hackathon validation.
