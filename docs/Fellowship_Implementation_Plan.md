# Fellowship Implementation Plan (10 Weeks, Canonical)

This plan inherits the primary thesis and contracts in `BioGuard_Technical_Specification.md`, with a protocol-ecosystem target.

Current primary-only hackathon outcome (`artifacts/metrics/outcome.json`) is `success` with `winner=bioguard`.
Optional ablations (`--include-ablations`) can still show stronger scores for pre/post-only checks, while the protocol claim is evaluated on the primary stack.
Fellowship execution should treat this as the expected protocol-optimization trajectory for scale and portability:

- retain the protocol thesis,
- harden portability and operator utility,
- and publish explicit revision targets that move decision boundary precision on multi-turn cases.

## Week-by-Week Plan

This plan assumes the hackathon package is ambitious rather than minimal:

- one deep host integration,
- two additional host compatibility demonstrations,
- stronger benchmark slice,
- operator replay/audit demo path,
- and a polished report/demo package suitable for top-tier judging.

### Week 1
- finalize `spec/bkt_contract_v1.0.json`
- validate existing schemas and openapi
- lock benchmark manifest instance and quality gates
- consolidate hackathon artifact freeze and baseline smoke for `/v1/screen` and `/v1/evaluate`
- draft the conformance artifacts (`artifacts/conformance/host_capability_profile.schema.json`, initial `deviation_matrix.csv` seed format, and acceptance rubric)
- add a dedicated `informative_failure` interpretation memo mapped to protocol revision hypotheses.
- formalize a protocol-revision matrix for each unresolved impact/execution/clarity axis.

### Week 2
- implement and freeze reference `host-1` path
- publish first reproducible decision traces and operator replay path
- deliver Milestone A (below), including `artifacts/conformance/conformance_report.md` draft
- if any gate remains unresolved, record explicit fellowship debt in `artifacts/checks/execution_state.json` and proceed with the replacement hypothesis.

### Week 3
- expand BioSession to phase-1 size and produce `biosession-500-train` shard
- complete inter-rater run 1
- if tier imbalance affects Tier-2 transfer capture, add adjudication guidance and rebalance criteria before Week 4.

### Week 4
- complete inter-rater run 2 and adjudication
- validate updated manifest hashes
- rerun baseline metrics with expanded data

### Week 5
- finish benchmark pack freeze and publish QA report
- Milestone B checks completed

### Week 6
- integrate `host-2`, compare host contracts
- publish friction rubric and first portability notes
- publish first version of conformance matrix across host-1 and host-2

### Week 7
- integrate `host-3` or complete API parity check
- run ablation matrix including pre-inference only, post-inference only, and composite
- decision matrix refresh
- close conformance reporting for hosts-1 through 3 with explicit deviation notes and governance recommendation
- classify each deviation as `accepted` or `repair` and carry repair tasks into fellowship closure if still unresolved.

### Week 8
- finalize protocol spec and compliance notes
- finalize cross-host report
- complete human override and uncertainty docs

### Week 9
- draft final analysis with preregistered interpretations:
  - success
  - partial success
  - informative failure
- finalize narrative on operator implications

### Week 10
- finalize report + artifact bundle + release checklist
- dry run of fellowship defense with explicit decision pathways and risk statements

## Milestones

- **Milestone A (end week 2):** contracts validated, one host reproducible, operator replay path stable.
- **Milestone B (end week 5):** benchmark expansion, annotation quality gates, and stronger primary table.
- **Milestone C (end week 7):** three-host conformance package, deviation matrix, and ablation report.
- **Milestone D (end week 10):** full protocol release with evidence bundle and fellowship-grade report.

## Execution Constraints

- keep BioSeq and open-weight tuning as optional or secondary; never make them blocking preconditions.
- if any milestone fails, record failure with next-step protocol revision and continue.
- freeze scope if success criteria already require narrowing below contract.
- explicitly avoid claims of cross-host universality; every host claim must cite a corresponding profile row in conformance artifacts.
