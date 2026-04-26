# BioGuard Operational Runbook

## Purpose

The runbook is the canonical execution layer for an ambitious hackathon submission and direct fellowship continuation. It assumes `spec/*` files are source of truth and that all changes stay within the documented artifact contracts.

## 0) Inputs

```text
PYTHON_VERSION >= 3.11
PYTHONPATH includes ./src
CONTRACT_VERSION == bkt-v1.0
```

Required files:

- `spec/bkt_contract_v1.0.json`
- `spec/bkt_event.schema.json`
- `spec/benchmark_manifest.schema.json`
- `spec/benchmark_manifest_v1.0.json`
- `spec/decision_envelope.schema.json`
- `spec/bioguard_api.openapi.yaml`
- `docs/BKT_Rubric_Draft.md`

## 1) Setup

1. Set working directory to `/Users/jasontang/bioguard`.
2. Run `make init` to create standard artifact directories and seed fixtures.
3. Confirm no unintended edits in `spec/*` and `docs/*` before freeze.

## 2) Evidence Path (Hackathon Winning-State Target)

1. **Gate-0 Spec Gate:** `python -m bioguard check`
2. **Gate-1 Screen Gate:** `python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl`
3. **Gate-1b Failure Gate:** `python -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl` and  
   `python -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl`
4. **Gate-1c Skill Gate:** `make skills`
5. **Gate-2 Evaluation Gate:** `python -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --splits test --seed 1 --out artifacts/metrics`
6. **Gate-3 Submission Gate:** `make submission-surface` and `make evidence` (requires Gate-0/1/2 evidence files complete)
7. **Gate-4 Portability Gate:** host-2 and host-3 parity or compatibility artifacts plus deviation notes
8. **Gate-5 Demo Gate:** operator replay path and concise demo script/video outline
9. **Gate-6 Informative-Failure Closure Gate:** explicit revision hypotheses required when outcome is not success.

Gate pass definition:

- Gate-0 writes `artifacts/checks/protocol_lock.json` with at least soft warnings and zero hard failures.
- Gate-1 writes deterministic good/malformed request traces under `artifacts/records/`.
- Gate-1c writes deterministic skill smoke outputs under `artifacts/records/skill_*.json`.
- Gate-2 writes `artifacts/metrics/results.json`, `artifacts/metrics/outcome.json`, `artifacts/metrics/case_summary.json`, and `artifacts/metrics/error_taxonomy.md`.
- Gate-3 writes `artifacts/evidence/bundle_manifest.json` and `artifacts/evidence/report_index.json` for reporting.
- Gate-3 also emits `artifacts/submission_surface/` via `make submission-surface` (docs excluded).
- Gate-4 writes host portability notes and conformance/deviation outputs.
- Gate-5 yields a replayable operator workflow plus demo narrative.
- Gate-6 requires three revision hypotheses in report (tier coverage, threshold calibration, fallback handling) if outcome is informative_failure.

## 3) Contract Validation Gate

Command:
- `python -m bioguard check`

Expected:
- `artifacts/checks/protocol_lock.json` with `"status": "ok"` or `"status": "warn"` when optional tooling is unavailable.
- `check` exits non-zero for hard failures (missing required files, schema parse errors, schema violations).

Pass criteria:
- All listed schema files parse.
- Manifest validates vs `benchmark_manifest.schema.json`.
- `protocol_lock.json` includes valid parse state for both contract and execution-state manifest.

## 4) Screen Smoke Gate

1. Run seeded screen:
   - `python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl`
2. Capture malformed case:
   - `python -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl`
   - `python -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl`

Pass criteria:
- Deterministic output on repeat runs with no environment changes.
- Every entry in `seed_screen.jsonl` includes:
  - `decision`
  - `request_id`
  - `conversation_id`
  - `bkt_events[0].composite_label`
  - `host_context`

## 5) Evaluation Gate

Run:
- `make eval`

Produces:
- `artifacts/metrics/results.json`
- `artifacts/metrics/bootstrap.csv`
- `artifacts/metrics/confusion_matrix.csv`
- `artifacts/metrics/hackathon_results.md`

Pass criteria:
- Baseline matrix includes `bioguard`, `keyword-filter`, `llama-guard-3`, `gpt54-zero-shot`, `pre-inference-only`, and `post-inference-only`.
- `artifacts/metrics/hackathon_results.md` is produced as the primary comparison table.
- `artifacts/metrics/ablation_results.md` is produced for pre/post checks.
- Includes `recall_at_fpr_5`, `ci95_low`, `ci95_high`, and `significant_vs_baseline`.
- One or more split rows are present (default `test`).
- `artifacts/metrics/outcome.json` exists with `status` in `success | partial | informative_failure`.
- `artifacts/metrics/case_summary.json` includes per-tier balance and label counts.
   - Target benchmark size is 500 multi-turn cases per split; any lower count must be justified, tier-balanced, and explicitly logged as fellowship debt if it affects power.
- At least one ablation comparison and one portability note are ready for report inclusion.
- If outcome is informative_failure, report must include a one-paragraph protocol revision map and top misses by tier.

### 5a) Live Critique Pass (Impact/Execution/Clarity)

Before closing Gate-5:

- **Impact check:** ensure the primary claim remains one sentence tied to conversation-boundary control.
- **Execution check:** rerun `make evidence` and confirm every major table/path maps to a source file in this runbook.
- **Clarity check:** verify the same one-sentence thesis appears in abstract, methods summary, and conclusion.

Failing check requires one line in `artifacts/checks/execution_state.json` `open_items` and a target fix in the next run.

## 5b) Skill Gate

Run:
- `make skills`

Pass criteria:
- `skills/*/SKILL.md` exist for `bioguard-bkt-scoring`, `bioguard-bio-trace`, `bioguard-bio-guard`, and `bioguard-bio-seq`.
- `artifacts/records/skill_bkt_scoring.json` exists and contains one BKT event.
- `artifacts/records/skill_bio_trace.json` and `artifacts/records/skill_bio_guard.json` validate the canonical decision path.
- `artifacts/records/skill_bio_seq.json` exists as an explicit optional-module result, even if placeholder findings are empty.

## 6) Execution State Gate

Run:
- `python -m bioguard state --state artifacts/checks/execution_state.json --note "pipeline refresh"`

Pass criteria:
- `artifacts/checks/execution_state.json` includes:
  - `counts.total`
  - `counts.done`
  - `completion_pct`
- Task records for each role in `spec/execution_state_manifest_v1.0.json` exist.

## 6b) Portability Gate

Pass criteria:
- one deep host path is working end to end
- two additional host demonstrations exist at smoke/parity or deeper level
- every non-default behavior is captured in explicit deviation notes
If any non-default behavior is `FALLBACK` or `MISSING`, include severity and mitigation in the same deviation row.

## 6c) Demo Gate

Pass criteria:
- operator can inspect decision, rationale, uncertainty, and trace in one replay flow
- demo can be delivered in 2-5 minutes without explaining the whole repository
- one memorable comparison figure or table is selected for presentation
For informative_failure, the demo must include one true positive control and one representative miss for operator interpretation.

## 7) Spec-Driven Scope Enforcement

No task is accepted unless it maps to one of:
- `spec/execution_state_manifest_v1.0.json` role outputs.
- `docs/AIxBio_Hackathon_Execution_Package.md` required submission content.
- `docs/Fellowship_Implementation_Plan.md` milestone milestones.

If a task falls outside these scopes, it is logged as `open_items` in `artifacts/checks/execution_state.json` with deferment reason.

## 8) Evidence and Submission Pack

Create two submission artifacts at end:
- `artifacts/evidence/bundle_manifest.json`
- `artifacts/evidence/report_index.json`
- `artifacts/submission_surface/` (portable code-only submission package)

Each evidence record should include:
- `path`
- `sha256`
- `generated_at_utc`
- `command`
- `contract_version`
- `notes`

Run:
- `make evidence`
- `make submission-surface`

## 9) Sign-off Template

Before any final release freeze, include:

- Primary outcome: `success` / `partial` / `informative_failure`.
- Top 5 false positives / false negatives (or nearest equivalent from seeded + full corpus).
- Portability gaps and expected remediation.
- Protocol revision note for any deviation from deterministic decision behavior.
- Demo path summary: what is shown, in what order, and what claim each step supports.

Recommended one-line outcome declaration:

`Outcome=[success|partial|informative_failure] at fixed 5% FPR; [primary finding]; [actionable protocol revision if applicable].`

## 10) Governance Constraints

- Keep sequence analysis secondary and labeled optional.
- Do not export raw biological sequences in public artifacts unless de-identified.
- Do not change `spec/bkt_contract_v1.0.json` without `docs/protocol_release_notes.md` update.
- If open-weight path is used, isolate behind `ablation_only` and keep protocol path untouched.
