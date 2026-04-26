# BioGuard Technical Specification (Canonical Implementation Draft v1.1)

**Project:** BioGuard  
**Owner:** Jason Tang  
**Status:** Canonical draft for Fellowship MVP + AIxBio hackathon continuation  
**Date:** 2026-04-23

## 1) Core Problem & Claim

Biosecurity at bio-LLM interfaces currently fails at the conversation boundary. Screening is still mostly downstream (sequence-level checks and model-output filters), which misses multi-turn knowledge transfer before dangerous instructions become operational.  

**Canonical one-line thesis:** BioGuard is a portable conversation-layer biosecurity protocol, and BKT is the scoring contract used to measure whether it catches dangerous biological knowledge transfer better than stateless baselines.

## 2) Top-Level Positioning

1. Protocol-first is the primary identity.  
2. BKT is the evaluation mechanism and trust primitive of that protocol, not a separate research pillar.  
3. SKILL.md is treated as the distribution/interoperability substrate, because current ecosystem documents support open Skill adoption across multiple major agent hosts. The BioGuard-specific layer is therefore a constrained **BioGuard Skills Profile**, not a replacement standard.  
4. Fellowship success is evidence on the protocol, not guaranteed success on any optional module.

### 2a) Compelling Attractors (in score order)

1. **The dangerous transaction is the conversation.**  
   - Core framing: interception boundary is the multi-turn exchange, not sequence-level output only.
   - Judge-ready sentence: *"BioGuard defends the only boundary where harmful biological capability is assembled: the live conversation."*
2. **Missing protocol layer at the bio-LLM boundary.**  
   - Required by: `spec/bkt_contract_v1.0.json` + `spec/bioguard_api.openapi.yaml`.
3. **BKT as a practical measurement primitive.**  
   - Required by: `artifacts/metrics/results.json` + `artifacts/metrics/error_taxonomy.md`.
4. **Operator-ready decisions, not black-box risk scores.**  
   - Required by: `artifacts/records/seed_screen.jsonl` + `artifacts/metrics/reproducibility.md`.
5. **Hackathon → Fellowship de-risking arc.**  
   - Required by: `docs/Fellowship_Implementation_Plan.md` + `artifacts/evidence/report_index.json`.

### 2b) State Diff vs Ambitious-Winning Target (Reality Check)

| Dimension | Current State | Target for 5/5 Submission |
| --- | --- | --- |
| Corpus scale | 500 cases per split with fixed split hash and manifest | 500+ cases per split only if needed for stable tier inferences, with independent rebalance audit |
| Portability | 3 host profiles with PASS/FALLBACK/RESTRICTED rows | Deep paths + explicit remediation per non-PASS row and deterministic host replay for each host |
| Evaluation | Primary and ablation tables show primary outcome with strict-FPR threshold notes | Fixed significance labels and explicit revision hypotheses for each non-success condition |
| Operator surface | Decision JSONL exists with reproducibility metadata | One scripted replay flow from request → envelope → rationale → trace + a 2-5 minute demo path |
| Governance & dual-use | Appendix draft present | Final appendix with disclosure policy and decision-safe boundaries clearly bound |

Closure priorities:
1. **Strengthen result interpretation first:** keep the current `artifacts/metrics/outcome.json` winner claim bounded by strict-FPR assumptions and explicit conservative-baseline interpretation.
2. **Close portability depth next:** attach remediation notes for every `FALLBACK`/`RESTRICTED` row and map operator implications.
3. **Harden submission path last:** freeze one primary results table, one ablation table, one portability matrix, plus a deterministic demo replay command set.

Current scoring against the target:
- Impact/Potential: 4.2/5.0 (strong framing + measurable strict-FPR uplift).
- Execution Quality: 4.4/5.0 (reproducible artifacts + baseline matrix + explicit threshold notes).
- Presentation/Clarity: 4.4/5.0 (single thesis with complete failure narrative now explicit).

### 2c) Gap-Closure Plan (Ambitious-Winning State)

The current repo is already credible as a protocol-first MVP. It is not yet optimized for a top-tier hackathon finish or a fellowship fast-track path. The remaining gap is concentrated in five areas:

1. **Evidence strength**
   - Current state: seeded synthetic evaluation with strict-FPR positive uplift and explicit conservative-baseline notes.
   - Target state: materially stronger benchmark slice, tier-level tables, ablation table, and a protocol hardening pass on identified misses.
2. **Host portability**
   - Current state: one deep canonical path plus skill smoke outputs.
   - Target state: one deep host integration plus two additional host compatibility demonstrations with deviation notes.
3. **Operator surface**
   - Current state: audit records and reproducibility artifacts exist, but there is no compelling operator-facing workflow narrative.
   - Target state: replayable audit flow, decision trace inspection, and an obvious practitioner demo path.
4. **Submission polish**
   - Current state: strong drafts and evidence bundle.
   - Target state: polished PDF report, concise abstract, demo script/video outline, and a single memorable comparison figure/table.
5. **Fellowship readiness**
   - Current state: thesis and contracts are strong, but dataset, annotation discipline, and cross-host proof remain thin.
   - Target state: expanded benchmark, explicit quality gates, and clear protocol/failure-learning pathway.

The project should therefore optimize for a **protocol ecosystem seed**, not a conservative minimum MVP.

### 2d) Recursive Red-Team Critique Loop

The project should run a strict pre-submission critique loop on three judge-facing axes:

1. **Impact/Potential loop**
   - Challenge: does the abstract clearly assert a previously-unaddressed failure boundary?
   - Failure signal: mixed framing between "platform" and "protocol."  
   - Fix: keep one sentence: `The dangerous transfer happens in the conversation, so we secure that boundary first.`

2. **Execution Quality loop**
   - Challenge: can another team replay every key claim with listed commands and hashes?
   - Failure signal: missing dataset split hashes, ambiguous baseline list, or unpinned contract versions.
   - Fix: keep a single run command block in the report that deterministically emits all primary tables and outcome file.

3. **Clarity loop**
   - Challenge: can a reviewer explain what was built and what was learned in 120 seconds?
   - Failure signal: five or more competing novelty claims.
   - Fix: remove optional modules from the main thesis and retain them as `secondary_fallback` work in the appendix.

This loop is considered closed only when each axis has an explicit remediation entry in `docs/AIxBio_Hackathon_Execution_Package.md`.

## 2e) SDD Execution Contract (Implementation-Ready)

This section is the software design anchor for end-to-end execution. Every code task must map to one module and one contract path.

### Required Runtime Modules

1. `src/bioguard/core.py`  
   - Implements `POST /v1/screen` logic, request validation, and decision envelope creation.
2. `src/bioguard/eval.py`  
   - Implements `POST /v1/evaluate` logic, baseline matrix, significance testing, error taxonomy, and reproducibility payload.
3. `src/bioguard/cli.py`  
   - Implements spec-driven operator interface for `init`, `check`, `screen`, `evaluate`, and execution-state tracking.
4. `src/bioguard/orchestrator.py`  
   - Owns execution-state compatibility helpers and gate-completion accounting.
5. `scripts/build_evidence_manifest.py`  
   - Produces a submission-ready evidence index and bundle manifest.

### Contract-to-Artifact Matrix

- `bioguard check` → `artifacts/checks/protocol_lock.json` (spec validity and parse state).
- `bioguard screen` → `artifacts/records/seed_screen.jsonl` (+malformed pair in `artifacts/records/screen_bad_request.jsonl`).
- `make skills` → `artifacts/records/skill_bkt_scoring.json`, `skill_bio_trace.json`, `skill_bio_guard.json`, `skill_bio_seq.json`.
- `bioguard evaluate` → `artifacts/metrics/results.json`, `case_summary.json`, `error_taxonomy.md`, `outcome.json`, `reproducibility.json/md`.
- `python scripts/build_evidence_manifest.py` → `artifacts/evidence/bundle_manifest.json`, `artifacts/evidence/report_index.json`.

### 2f) Protocol Ecosystem Blueprint

The output goal is a protocol ecosystem with five enforceable layers:

1. Protocol kernel: contract, schemas, thresholds, scoring invariants.
2. Conformance layer: host capability profiles, portability tests, and deviation matrices.
3. Distribution layer: standardized skill artifact bundles and installation guidance.
4. Evaluation ecosystem: benchmark contract, baseline suite, and ablation protocol.
5. Governance layer: release semantics, traceability, and change governance.

### 2g) Reusable Patterns and Primitives (from prior protocol-first work)

The current proposal is deliberately structured around reusable primitives that can be applied across future biosecurity and AI-safety projects:

1. **Protocol contract > implementation**  
   - `spec/bkt_contract_v1.0.json` and `spec/bkt_event.schema.json` define what the system means; runtime code is explicitly constrained to this meaning.

2. **Thin source-of-truth + separate entrypoints**  
   - Core logic is a shared contract; operator workflow and benchmark surfaces are separate by design.

3. **Skill-pack decomposition**  
   - Each `SKILL.md` block is an independently testable primitive that composes into the same policy outcome.

4. **Conformance-first portability**  
   - Cross-host success is measured with explicit PASS/FALLBACK/RESTRICTED semantics and remediation records.

5. **Failure-first narrative**  
   - The project is judged by how clearly it explains what worked, what failed, and which protocol boundary should move next.

This pattern set is the anchor for both hackathon execution and fellowship extension because it keeps the project at thesis speed while retaining rigor.

Every milestone should include:

- a locked contract state (`spec/*`),
- at least one new host-capability declaration,
- at least one conformance artifact (`artifacts/conformance/*`).

A host is ecosystem-compliant only if it:

- emits valid decision envelopes for normal and fallback paths,
- produces traceability fields (`decision_hash`, `contract_version`, `artifact_version`, and `host_capability_profile`),
- preserves contract semantics under rerun with identical inputs.

### Minimum Viable Execution Gates

1. **Gate-0 Spec:** `bioguard check` passes without hard parse/schema errors.
2. **Gate-1 Smoke:** seeded screen path and malformed input path execute and produce expected status codes (`200`, `400`/`422`).
3. **Gate-1c Skill Smoke:** concrete `SKILL.md` blocks execute through the shared proxy and emit deterministic JSON outputs.
4. **Gate-2 Evaluation:** baseline comparison and primary metric outputs exist for requested splits.
5. **Gate-3 Evidence:** all required artifacts are listed in evidence bundle with command and hash metadata.

### Hackathon Rubric Alignment

- **Impact/Potential (Dimension 1):** one novelty boundary claim + explicit operator value statement + one intervention boundary that changes implementation behavior.
- **Execution Quality (Dimension 2):** reproducible pipeline and quantitative table in `artifacts/metrics/hackathon_results.md`.
- **Clarity (Dimension 3):** fixed architecture order and a dedicated limitations/dual-use appendix in submission docs.

## 3) Canonical Artifact Map

| Path | Type | Purpose | Must exist before execution |
| --- | --- | --- | --- |
| `spec/bkt_contract_v1.0.json` | JSON contract | Canonical BKT scoring contract and thresholds | Yes |
| `spec/bkt_event.schema.json` | JSON Schema | Machine-validated BKT event format | Yes |
| `spec/decision_envelope.schema.json` | JSON Schema | Machine-validated `/v1/screen` output envelope | Yes |
| `spec/bioguard_api.openapi.yaml` | OpenAPI 3.1 | `/v1/screen` and `/v1/evaluate` interfaces | Yes |
| `spec/benchmark_manifest.schema.json` | JSON Schema | Validation rules for BioSession metadata | Yes |
| `spec/benchmark_manifest_v1.0.json` | JSON | Versioned BioSession manifest instance | Yes |
| `docs/BKT_Rubric_Draft.md` | Markdown | Rubric explanation for human reviewers | Yes |
| `docs/Operational_Runbook.md` | Markdown | Command-level execution playbook and artifacts | Yes |
| `docs/Fellowship_Implementation_Plan.md` | Markdown | 10-week milestone schedule | Yes |
| `docs/AIxBio_Hackathon_Execution_Package.md` | Markdown | 3-day MVP scope and framing | Yes |
| `docs/protocol_release_notes.md` | Markdown | Changelog and contract migration log | Yes |
| `skills/` | Skill pack | Concrete `SKILL.md` blocks for host integration | Yes |
| `artifacts/conformance/host_capability_profile.schema.json` | JSON Schema | Host capability contract fields for cross-runtime comparability | Yes |
| `artifacts/conformance/deviation_matrix.schema.json` | JSON Schema | Portability comparison schema for host behavior deltas | Yes |
| `artifacts/conformance/host_capability_profile.json` | JSON | Per-host profile plus supported/unsupported feature map | Yes |
| `artifacts/conformance/deviation_matrix.csv` | CSV | Host x requirement compatibility report | Yes |
| `artifacts/conformance/conformance_report.md` | Markdown | Cross-host compliance interpretation and next-step recommendations | Yes |

Any execution agent must treat these files as the source of truth unless superseded by an explicit version bump declared in `docs/protocol_release_notes.md`.

## 4) Contract Definitions

### 4.1 BKT Event

All scoring outputs must validate against `spec/bkt_event.schema.json`.  

- Version: `bkt-v1.0`
- Dimensions:
  - `scope` (`low`, `medium`, `high`, `critical`)
  - `depth` (`low`, `medium`, `high`, `critical`)
  - `uplift` (`low`, `medium`, `high`, `critical`)
- Labels: `allow`, `review`, `block`  
- Required uncertainty posture: `low`, `med`, `high`

The schema includes deterministic required fields: event IDs, traceability metadata, rationale length limits, turn window, timestamps, and auditable flag.

### 4.2 Scoring Contract (`spec/bkt_contract_v1.0.json`)

- Composite formula:

`composite = 0.45 * scope + 0.35 * depth + 0.20 * uplift`

- Default decision labels:
  - `allow` if composite < 0.45
  - `review` if 0.45 <= composite < 0.75
  - `block` if composite >= 0.75
- Deterministic escalation rule:
  - Any `critical` in `scope` or `depth` must be at least `review`.
  - Two `high` dimensions must be at least `review`.
  - Missing required fields or malformed data triggers `review` with `uncertainty: high`.

### 4.3 Audit Event Package

Every `/v1/screen` decision must emit one JSONL decision envelope containing:

- `request_id`, `conversation_id`, `request_ts_utc`, `model_id`
- `policy_profile`, `decision`, `decision_reason`
- `bkt_events` array
- `host_context` (`host_id`, `skill_id`, `contract_version`, `artifact_version`)
- optional `sequence_findings` entries
- optional `human_override` fields when enabled

The full decision object and each BKT event are immutable and append-only.
`decision_envelope.schema.json` defines required fields for `/v1/screen` output.

## 5) Host Runtime Contract (Agent Skills)

BioGuard adopts the open Agent Skills format and constrains it through a BioGuard Skills Profile. The profile is materially represented in this repo under `skills/`.

BioGuard runs as three SKILL blocks:

1. `bioguard-bkt-scoring`
2. `bioguard-bio-trace`
3. `bioguard-bio-guard`

Optional module:

4. `bioguard-bio-seq` (ablation and extension only)

Non-skill package:

- `BioSession` is the benchmark and dataset package. It is not a runtime skill block.

Each host runtime implementation must satisfy this minimum behaviour:

- pre-screen call path and post-screen call path exist for all invocations
- decisions and audit traces are identical for identical inputs and contract version
- decision latency is reportable (`p50`, `p95`)
- unsupported feature fallback emits a typed invalid/unsupported payload.
- `/v1/screen` returns status `200` on valid payload, `400` on validation failure, `422` on unsupported feature mismatch

For cross-host comparability, each host must log:

- path: `artifacts/cross_host/<host_id>/screen_trace.jsonl`
- decision hash: `sha256(request + event + contract + output)`
- `deviation_notes` for any non-default behaviour

Canonical repo layout:

- `skills/bioguard-bkt-scoring/SKILL.md`
- `skills/bioguard-bio-trace/SKILL.md`
- `skills/bioguard-bio-guard/SKILL.md`
- `skills/bioguard-bio-seq/SKILL.md`
- `scripts/bioguard_skill_proxy.py`

## 6) API Contract

`POST /v1/screen`
- Request: conversation window (user + assistant turns), policy profile, host context, threshold overrides
- Response: decision envelope with BKT events and rationale bundle

`POST /v1/evaluate`
- Request: dataset partition (`train`, `dev`, `test`, `all`), baseline selectors, ablation toggles
- Response: confusion matrix, recall@5%FPR, uplift tables, bootstrap CIs, and bootstrap seed + commit metadata

The OpenAPI contract is authoritative and located at `spec/bioguard_api.openapi.yaml`.

## 7) Benchmark and Data Contract

BioSession is the primary benchmark corpus. Versioning is explicit through `benchmark_manifest_v1.0.json` and must validate with `benchmark_manifest.schema.json`.

Required manifest fields include:

- `dataset_id`, `version`, `license`, `splits`, `tiers`, `rater_guideline_version`, `quality_gates`
- `annotation_protocol`
- data shard paths and hashes in `files`
- `kappa`/agreement targets expressed through `quality_gates`

Quality gates:

- minimum Cohen/kripp alpha threshold for release
- adjudicated disagreements logged
- seed split hash pinned

## 8) Evaluation Protocol (Primary, Secondary, and Abandoned Outcomes)

### 8.1 Primary test

Test whether context-aware protocolized screening improves detection of dangerous bio-knowledge transfer on multi-turn Tier 2 attempts relative to stateless baselines.

Primary metric:

- recall at 5% false-positive rate, with 95% bootstrap CIs

Secondary metrics:

- precision, FPR stability, Cohen/krippendorff agreement, latency `p50/p95`, and cost/op

### 8.2 Comparative baselines

- Llama Guard 3
- bio-hazard keyword list
- GPT-5.4 zero-shot
- pre-inference-only
- post-inference-only

### 8.3 Outcome interpretation

- **Success:** statistically meaningful recall uplift at fixed FPR, cross-host conformance, reliable rubric agreement.
- **Partial success:** uplift on one axis (eg recall or portability) with transparent trade-off.
- **Informative failure:** no uplift but clear taxonomy of misses and a concrete protocol revision path.

## 9) Implementation Execution Model

### 9.1 Hackathon Winning-State Target

Goal: deliver a top-tier submission that looks immediately extensible into fellowship work.

Target outputs:

- 1 deep host integration using BioGuard core blocks
- 2 additional host compatibility or parity demonstrations with explicit deviation notes
- concrete skill-pack outputs for all core skills
- 500+ adversarial multi-turn scenarios across tiered misuse conditions
- one primary comparison table, one ablation table, and one portability matrix
- replayable operator audit flow with decision trace inspection
- polished report draft, abstract, dual-use appendix, and demo outline/video script

### 9.2 Fellowship MVP (10 weeks)

Goal: protocol-level evidence plus publication-grade reproducibility package.

Core outputs:

- Stable protocol contract and changelog
- Expanded BioSession-500 corpus and annotated release metadata
- three-host reference package with conformance notes
- cross-host friction report with failure taxonomy
- stronger annotation and adjudication discipline
- final report with explicit success/partial/informative-failure interpretations

## 10) Execution Task Graph

Task IDs are ordered dependencies:

- `T1` lock contracts and schemas (`spec/*`)
- `T2` implement API scaffold and decision envelope
- `T3` host-1 reference integration
- `T4` benchmark manifest and expanded tiered fixture pack
- `T5` baseline comparison, tier breakdown, and metric script
- `T6` operator replay/audit workflow and demo artifacts
- `T7` host-2 and host-3 compatibility checks
- `T8` ablation matrix and regression checks
- `T9` report, appendix, and demo script/package
- `T10` final fellowship release package

Conformance gates:

- `T1` must fail if any schema is not parseable
- `T4` must include data hash, tier metadata, and annotation guidance reports
- `T7` must publish host deviation notes
- `T8` must include a portability matrix and at least one informative ablation
- `T10` requires success/partial/informative-failure table in final narrative

## 11) Risk Register and Response

1. **Rubric instability:** reduce to two-level taxonomy and enable uncertainty gating if calibration collapses.
2. **Cross-host drift:** declare required deviations and treat portability as "conforming with marked constraints."
3. **Benchmark quality drift:** hold releases behind reviewer agreement gate.
4. **Open-weight path risk:** maintain GPT-5.4 path as canonical baseline; keep open-weight optional until data supports.

## 12) Alignment Clauses

This spec is designed to match ERA/Cambridge expectations on:

- rigour (predeclared metrics, confidence intervals, clear baselines)
- decision usefulness (operator action outputs + uncertainty)
- clarity (single protocol thesis, bounded scope)
- epistemic humility (explicit partial and negative-result pathways)
- reproducibility (versioned contracts, immutable manifests)

## 13) References

- AIxBio Fellowship FAQ: https://www.aixbiosecurity.com/faq
- AIxBio hackathon page (as used in original proposal framing)
- Agentskills ecosystem links:
  - https://agentskills.io/home
  - https://code.claude.com/docs/en/skills
  - https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/
  - https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
  - https://academy.openai.com/public/clubs/work-users-ynjqu/resources/skills
  - https://openai.com/codex/
