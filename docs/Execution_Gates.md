# BioGuard Execution Gates

This document is the implementation-level contract for spec-driven execution.

## Core Execution Invariants

1. Follow `spec/*` first; use it as the acceptance surface for all implementation work.
2. Optimize for one thesis: **portable conversation-layer protocol + BKT evaluation proof**.
3. Optimize for ambitious vertical proof, not minimum scope reduction.
4. Keep report and auxiliary docs out of `make submission-surface`; only runtime artifacts are judge-run.
5. Evidence must remain valid for the same submission target under either success, partial, or informative_failure outcome.

Winning-state implication:
- if outcome is `informative_failure`, the revision map and portability implications must be explicit and action-oriented.

## Competitive Target by Dimension

For a top-tier hackathon result and fast-track fellowship transition:

- **Impact**: one strong protocol claim with portability evidence that changes operator posture.
- **Execution**: reproducible primary + ablation tables with significance and deterministic command+hash trail.
- **Clarity**: one repeated thesis sentence and one 120-second explanation in report-facing outputs.

## Workstream Topology and Ownership

- Lead: coordinates rubric-aligned decisions, scope control, and freeze gates.
- Protocol Lock: owns `spec/*`, `protocol_release_notes.md`, and `protocol_lock.json`.
- Runtime: owns `src/bioguard/*` screening path and deterministic trace output.
- Evaluation: owns `artifacts/metrics/*` and baseline matrices.
- Submission: owns report sections and limitations/dual-use appendix drafts.

## Mandatory Artifact Outputs

### Shared Required Files
- `artifacts/checks/protocol_lock.json`
- `artifacts/records/seed_screen.jsonl`
- `artifacts/metrics/results.json`
- `artifacts/metrics/bootstrap.csv`
- `artifacts/metrics/confusion_matrix.csv`
- `artifacts/metrics/case_summary.json`
- `artifacts/metrics/outcome.json`
- `artifacts/docs/Limitations_DualUse.md` (or equivalent)
- `artifacts/checks/execution_state.json`
- host deviation notes
- operator replay/demo outline

### Workstream Outputs
- Protocol Lock: `artifacts/checks/protocol_lock.json`, contract diffs in `docs/protocol_release_notes.md`
- Runtime: `artifacts/records/seed_screen.jsonl`, `artifacts/records/bootstrap.jsonl`, reproducible CLI commands
- Evaluation: `artifacts/metrics/results.json`, `artifacts/metrics/hackathon_results.md`, `artifacts/metrics/confusion_matrix.csv`, `artifacts/metrics/outcome.json`, `artifacts/metrics/case_summary.json`, `artifacts/metrics/case_predictions.jsonl`
- Submission: `artifacts/docs/report_draft.md`, `artifacts/docs/Limitations_DualUse.md`, and red-team closure notes.

## Command Map (Single Source for Agents)

- `make init`
- `python -m bioguard check`
- `python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl`
- `make skills`
- `python -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --seed 1 --splits test --out artifacts/metrics`
- `python -m bioguard state --state artifacts/checks/execution_state.json --note "state-refresh"`
- `make evidence`
- `make submission-surface`

## Spec-Driven Execution State Protocol

`artifacts/checks/execution_state.json` is the single status source:
- `status`: `active` / `blocked`
- `tasks`: list of `{task_id, role, status, updated_at_utc, open_items}`
- `counts` and `completion_pct` always present after state refresh
- `notes` logs rationale for task reassignments

Execution workflow:
1. Start with `python -m bioguard state --state artifacts/checks/execution_state.json`.
2. Set task completion with `--complete-task <task_id>`.
3. Add blockers to `open_items`.
4. Add one sentence to `notes` per decision checkpoint.
5. Run `state` again and proceed only when gate state is coherent.

Any `open_items` that are not execution blockers should not remain in this file; they must be moved to the fellowship plan with explicit owner and week.

## Success Gate Matrix

- Gate 0: contract and schema validation complete.
- Gate 1: deterministic seed screen run produces valid envelope + events.
- Gate 2: evaluation matrix produces all required baseline rows and CI.
- Gate 3: `artifacts/metrics/outcome.json` is present with outcome status and submission appendix includes an explicit outcome declaration (`success`, `partial`, or `informative_failure`) plus protocol-revision actions.
- Gate 4: recursive judge-facing critique loop is closed with explicit remediation notes for any unresolved axis.
- Gate 5: all open_items are either resolved or explicitly deferred as fellowship debt.
- Gate 6: portability evidence is complete (every non-PASS row has remediation and operator implication).
- For Gate 3 and Gate 4, informative_failure is acceptable only if it contains:
  - a tier-aware miss map from `artifacts/metrics/error_taxonomy.md`,
  - three explicit protocol-revision hypotheses,
  - and one portability implication linked to host conformance.
- For Gate 6, any `FALLBACK` or `RESTRICTED` row in `artifacts/conformance/deviation_matrix.csv` must include owner, reason, and decision consequence in a trace artifact.

### Gate-4 Red-Team Closure Criteria

- **Impact axis:** thesis text in abstract, method, and conclusion are identical in claim language.
- **Execution axis:** a reader can reproduce the primary tables from the listed command block and hashes.
- **Clarity axis:** one 120-second explanation exists in plain language and maps to all top-claim claims.
- Any miss on an axis remains in `execution_state.open_items` and maps to a named follow-up week in the fellowship plan.

### Gate-5 Artifact Quality Scoring

Map every mandatory artifact to judge dimensions before freeze:

1. **Impact**
   - Thesis and novelty framing consistent across report/abstract.
   - Interoperability claims supported by populated conformance rows.
2. **Execution**
   - Primary/ablation tables and confusion matrix regenerated from `make evidence` + command block.
   - Reproducibility header hashes present in metrics package.
3. **Clarity**
   - One 120-second explanation exists in `artifacts/docs/report_draft.md`.
   - Appendix includes limitations, dual-use, and responsible disclosure.

Pass Gate-5 only when 3/3 dimensions are complete and all unresolved misses are assigned `fellowship_debt`.

### Gate-6 Conformance Evidence

- Portability matrix must include trace IDs for every row in `deviation_matrix.csv` and `deviation_matrix.json`.
- `host_capability_profile_host-2.json` and `host_capability_profile_host-3.json` must include `decision_hash_supported`, `host_capability_profile`, and `deviation_tracking` fields.
- Every `RESTRICTED`/`FALLBACK` status must map to a host-specific mitigation sentence in `artifacts/conformance/conformance_report.md`.

## Milestone Cadence

### Day 0
- lock contract artifacts and initialize execution state.

### Day 1
- confirm seed trace and one smoke path.

### Day 2
- baseline matrix + top-miss taxonomy.

### Day 3
- report draft and submission execution state.
- if an axis miss remains, add it to `execution_state.json` as explicit fellowship debt and continue.

## Scope Discipline for Hackathon

Accept as core:
- one deep host-compatible `/v1/screen` implementation,
- two additional host compatibility demonstrations,
- one primary comparison table,
- one ablation table,
- one portability matrix,
- one complete appendix,
- one operator replay/demo path.

Defer only work that dilutes the protocol thesis:
- BioSeq as primary contribution,
- open-weight tuning as success precondition,
- broader CBRN platformization outside the conversation-layer thesis.
