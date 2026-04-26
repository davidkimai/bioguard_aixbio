# BioGuard

BioGuard is a small research prototype for screening biological AI conversations before risk is carried across turns. The core idea is simple: treat the conversation as the safety boundary, score each risky knowledge-transfer event with one shared rubric, and return a replayable decision record.

This repository is the public code and reproducibility surface for the AIxBio submission. It keeps the runnable code, benchmark manifests, skill pack, and evidence files together so reviewers can check the main claim without reading internal planning notes.

## What To Read First

- `docs/BioGuard_Technical_Specification.md`: plain-English system overview.
- `docs/BKT_Rubric_Draft.md`: human-readable scoring rubric.
- `docs/Operational_Runbook.md`: commands needed to reproduce checks and metrics.
- `skills/`: portable BioGuard skill pack.

## Reviewer Quick Start

Run from the repository root:

```bash
PYTHONPATH=src python3 -m bioguard check
PYTHONPATH=src python3 -m bioguard screen --request artifacts/requests/seed_request.json --out /tmp/seed_screen.jsonl
PYTHONPATH=src python3 -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --splits test --seed 1 --out /tmp/bioguard_metrics
```

The main result files are:

- `artifacts/metrics/hackathon_results.md`
- `artifacts/metrics/ablation_results.md`
- `artifacts/metrics/reproducibility.md`
- `artifacts/conformance/conformance_report.md`

## Repository Layout

- `src/bioguard/`: reference runtime for screening and evaluation.
- `spec/`: versioned contracts, schemas, API shape, and benchmark manifest.
- `skills/`: four `SKILL.md` blocks for agent-host integration.
- `artifacts/requests/`: small request fixtures.
- `artifacts/records/`: screen and skill smoke outputs.
- `artifacts/metrics/`: benchmark outputs and reproducibility metadata.
- `artifacts/conformance/`: host portability evidence.
- `scripts/`: evidence and skill proxy helpers.

Generated duplicate submission bundles and older narrative drafts were archived outside the repo at `/Users/jasontang/bioguard_aixbio_archive/20260427-publication-cleanup/`.

## Reproducibility Contract

Any externally reported result should name:

- the git commit,
- the command used,
- the benchmark manifest hash,
- the seed,
- the contract version,
- the output artifact path.

Run `PYTHONPATH=src python3 -m bioguard check` after any schema or contract change.
