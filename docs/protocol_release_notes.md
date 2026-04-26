# Protocol Release Notes

## Unreleased Drafts

Current release: 
- `bkt-v1.0`
- `benchmark_manifest_v1.0`
- `execution_state_manifest_v1.0`

### Release note v1.1 (2026-04-23)

Summary:
- Completed protocol-first articulation with BKT as evaluation contract.
- Added SKILL/Agent Skills interoperability framing to protocol lock.
- Aligned default evidence + submission outputs with hackathon/fellowship requirements.
- Renamed internal orchestration surfaces to execution-state/gates to avoid conflating repo state tracking with agent coordination.
- Seeded deterministic fixture corpus and canonical evaluation baselines for recall@5%FPR reporting.
- Separated BioGuard Skill blocks from the BioSession benchmark package.

State-diff corrections applied in this draft:
- Repo-local Skill blocks now exist under `skills/` instead of being implied only in narrative text.
- Internal state-tracking surfaces now use `execution_state` naming by default.
- Fellowship and hackathon narratives now describe BioSession as a benchmark package rather than a runtime skill.

No backward-incompatible schema migrations in this release; implementation remains a v0.1 reference runtime while the submission target has moved to ambitious-winning state.

### Release note v1.2 (2026-04-23)

Summary:
- Added winner-oriented execution criteria for informative-failure states across hackathon docs.
- Added explicit judge-facing closure checks in `Execution_Gates.md` and `AIxBio_Hackathon_Execution_Package.md`.
- Added explicit protocol-revision mapping to `artifacts/docs/report_draft.md`.
- Updated `Operational_Runbook.md` with Gate-6 and mandatory revision-hypothesis outputs.

State-diff corrections applied in this draft:
- Clarified that submission packaging excludes docs and keeps judge-run artifacts under `make submission-surface`.
- Tightened failure interpretation so non-dominant outcomes remain publishable as protocol-learning evidence.

Before final freeze for any externally visible milestone:

- append an entry with timestamp, git ref, changed file paths, and rationale,
- include backward-compatibility status,
- document migration steps if any.
