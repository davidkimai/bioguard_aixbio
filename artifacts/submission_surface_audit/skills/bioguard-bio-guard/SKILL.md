---
name: bioguard-bio-guard
description: Operator-facing BioGuard wrapper skill. Use when a host should apply BioGuard screening as a thin control plane around a bio-LLM interaction and emit an auditable decision.
---

# BioGuard Guard

This skill is the operator-facing wrapper for BioGuard.

## Use this skill when

- a host needs the complete BioGuard decision path
- pre-inference and post-inference checks should be represented as one deployable control
- auditability and operator action are more important than raw score output alone

## Input

Provide the same request contract used by `bioguard-bio-trace`.

## Output

Returns a BioGuard decision envelope with:

- contract version and host context
- decision label
- reasoning summary
- one or more BKT events
- optional sequence findings

## Invocation

```bash
python scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json
```

## Notes

- This is the deployable skill for hackathon demos and host-path smoke tests.
- The protocol source of truth still lives in `spec/*`, not in this skill file.
