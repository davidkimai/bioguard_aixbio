# BioGuard AXIOM: AIxBio Submission

This repository contains a protocol-first BioGuard MVP for the `Apart Research AIxBio` style submission workflow.

- `spec/`: protocol and API contracts
- `skills/`: `SKILL.md` blocks for host interoperability
- `src/`: screening runtime and evaluation helpers
- `scripts/`: skill proxy and submission build helpers
- `artifacts/`: evidence, manifests, runbooks, and metric outputs
- `docs/`: implementation specs and operating procedures
- `*.tex`: conference/workshop-style proposal drafts

## Quick start (judge/reviewer surface)

```bash
PYTHONPATH=src python3 -m bioguard check
PYTHONPATH=src python3 -m bioguard screen --request artifacts/requests/seed_request.json --out /tmp/seed_screen.jsonl
PYTHONPATH=src python3 -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --out /tmp/metrics.json
```

## Reproducibility metadata expected

Revisions should include:

- command log and parameters
- commit hash
- dataset split hash (or manifest hash)
- seed used for bootstrap/benchmark runs
- schema versions and manifest IDs

Run `python3 -m bioguard check` after every schema-touching change.
