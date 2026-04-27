# BioGuard Operational Runbook

This runbook gives the minimum commands needed to check the repo, run the screen path, test the skills, and reproduce the main benchmark artifacts.

Run all commands from the repository root.

## Requirements

- Python 3.11 or newer
- `PYTHONPATH=src`
- contract version `bkt-v1.0`

No external model API is required for the included deterministic smoke path.

## 1. Contract Check

```bash
PYTHONPATH=src python3 -m bioguard check
```

Expected output:

- `artifacts/checks/protocol_lock.json`

Pass condition:

- required spec files parse,
- benchmark manifest is readable,
- no hard schema or file-presence failure is reported.

## 2. Screen Smoke Test

```bash
PYTHONPATH=src python3 -m bioguard screen \
  --request artifacts/requests/seed_request.json \
  --out artifacts/records/seed_screen.jsonl
```

Expected output:

- `artifacts/records/seed_screen.jsonl`

The output should include a decision, request identifiers, BKT events, host context, and a decision hash.

## 3. Failure-Path Checks

```bash
PYTHONPATH=src python3 -m bioguard screen \
  --request artifacts/requests/bad_request.json \
  --out artifacts/records/screen_bad_request.jsonl

PYTHONPATH=src python3 -m bioguard screen \
  --request artifacts/requests/bad_contract.json \
  --out artifacts/records/screen_bad_contract.jsonl
```

Expected behavior:

- malformed requests return typed error records,
- contract mismatch returns a typed unsupported-contract record.

## 4. Skill Smoke Tests

```bash
make skills
```

Expected outputs:

- `artifacts/records/skill_bkt_scoring.json`
- `artifacts/records/skill_bio_trace.json`
- `artifacts/records/skill_bio_guard.json`
- `artifacts/records/skill_bio_seq.json`

Pass condition:

- each skill runs through `scripts/bioguard_skill_proxy.py`,
- the main guard and trace skills return the canonical decision path,
- the optional sequence skill either returns findings or an explicit skip result.

## 5. Benchmark Evaluation

Note: The full benchmark requires a live API key to evaluate the GPT-5.4 zero-shot proxy condition.

```bash
OPENAI_API_KEY="sk-..." PYTHONPATH=src python3 -m bioguard evaluate \
  --manifest spec/benchmark_manifest_v1.0.json \
  --splits test \
  --seed 1 \
  --out artifacts/metrics \
  --include-ablations
```

Expected outputs:

- `artifacts/metrics/results.json`
- `artifacts/metrics/hackathon_results.md`
- `artifacts/metrics/ablation_results.md`
- `artifacts/metrics/confusion_matrix.csv`
- `artifacts/metrics/bootstrap.csv`
- `artifacts/metrics/error_taxonomy.md`
- `artifacts/metrics/reproducibility.md`

Report any result with the command, seed, manifest path, manifest hash, and contract version.

## 6. Evidence Index

```bash
PYTHONPATH=src python3 scripts/build_evidence_manifest.py
```

Expected outputs:

- `artifacts/evidence/bundle_manifest.json`
- `artifacts/evidence/report_index.json`

## 7. Optional Code-Only Bundle

The public repo should not track generated duplicate bundles. If a venue asks for a code-only zip, generate it locally:

```bash
PYTHONPATH=src python3 scripts/build_submission_surface.py --out /tmp/bioguard_submission_surface
```

## 8. Release Checks

Before pushing a public update:

1. Run the contract check.
2. Run the screen smoke test.
3. Run `make skills`.
4. Run the benchmark command if any scoring, benchmark, or evaluation code changed.
5. Confirm the README and paper point to the same repository URL.
6. Confirm no generated duplicate bundle is staged under `artifacts/submission_surface*`.

## 9. Safety Constraints

- Keep raw high-risk biological instructions out of public artifacts.
- Keep sequence analysis optional unless separately reviewed.
- Keep uncertainty visible in decision records.
- Treat any high-confidence unsafe false negative as a disclosure issue before broad release.
