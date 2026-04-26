# BioGuard Submission Surface

Code package for hackathon evaluation only.
The submission surface intentionally excludes long-form writing artifacts and keeps
the reproducible execution surface explicit.

Run: `make init`, `make check`, `make screen`, `make eval`.

## Scope

- `src/`: runtime package under `src/bioguard`
- `spec/`: protocol contracts and schemas
- `skills/`: SKILL blocks used in host interoperability demos
- `scripts/`: launch helpers for screen/evaluate and evidence assembly
- `artifacts/`: reproducibility manifests and output artifacts
- `pyproject.toml` and `Makefile`: execution contract for the local judge run

## Minimal run for hackathon demo

```bash
python3 -m bioguard init
python3 -m bioguard check
python3 -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/evidence/reproducibility.json
python3 -m bioguard evaluate --request artifacts/requests/eval_request.json --out artifacts/metrics/results.json
```

## Evidence expectations

- `submission_surface/submission_manifest.json` records command arguments and generated artifacts.
- `artifacts/metrics/results.json` contains experiment outcomes.
- `artifacts/evidence/bundle_manifest.json` records hashes and replay commands.
- `artifacts/docs/checklist` (if included) should include success/failure definitions before submission.

Keep this folder lean: no analysis notebooks, no internal scratch logs, and no
non-essential markdown.
