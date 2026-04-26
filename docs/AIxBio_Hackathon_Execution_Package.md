# AIxBio Hackathon Submission Package (Ambitious and Score-Optimized)

**Date:** 2026-04-23  
**Event:** [AIxBio Hackathon 2026 - San Francisco/online](https://luma.com/aixbio-hackathon-2026-sf), [APART sprint page](https://apartresearch.com/sprints/aixbio-hackathon-2026-04-24-to-2026-04-26)  
**Tracks:** 4 tracks (including Track 3: AI Biosecurity Tools)

Submission surface rule for this event: runtime and source-code artifacts are what judges run; narrative/report artifacts stay external to the `submission-surface` package.

## 1) Strategic Positioning

BioGuard should be submitted as a **protocol ecosystem seed** backed by BKT evaluation, not as a full platform build.

The non-negotiable thesis sentence for every judge-facing surface is:

- **BioGuard is a portable conversation-layer biosecurity protocol; BKT is the scoring contract used to evaluate whether it catches dangerous biological knowledge transfer better than stateless controls.**

### One-line sentence judges should remember

- `BioGuard is a portable conversation-layer biosecurity protocol; BKT is the scoring contract used to evaluate its effectiveness versus stateless controls.`

### Framing hierarchy

1. The dangerous transaction is the conversation.
2. Biosecurity has a missing control protocol layer at the bio-LLM boundary.
3. BKT is the practical measurement primitive.
4. BioGuard is thin, auditable, operator-friendly infrastructure (not a monolith).
5. Hackathon is the de-risking proof-of-concept, fellowship is protocol validation and transfer.

## 2) Event-grounded ambition

Based on the event page, the sprint is 3 days (April 24–26, 2026). Submission requirements you listed in the prompt (research report, abstract, optional repository/demo, dedicated appendix) are treated here as required for strong judging outcomes.

This document no longer optimizes for a conservative minimum MVP. It optimizes for the strongest submission BioGuard could plausibly support if implementation throughput is accelerated by autonomous coding agents and parallel workstreams.

Required submission elements you should include:

- project title and ≤150-word abstract
- author names and affiliations
- report PDF (recommended template structure)
- short result section with quantitative comparisons
- GitHub repository link if usable
- short demo (optional)
- dedicated appendix: **“Limitations and Dual-Use Considerations”**

## 3) Most compelling attractors and frames

These are the strongest narrative hooks given the criteria:

**Top attractor order (for judges):**

1. **Safety Boundary Shift (highest impact):** `Dangerous conversations are not filtered by sequence-only or downstream checks.`
2. **Interoperability Grounding (proof of novelty):** Current Agent Skills ecosystem enables deployable portability from day one.
3. **Measurement-Backed Protocol Claim:** Recall@5%FPR uplift on multi-turn attempts is the primary proof object.
4. **Operator Utility:** Decisions are auditable and uncertainty-aware, not just risk scores.
5. **De-risking Arc:** Hackathon proves feasibility; fellowship proves scale and portability.

Supporting frames:

- **Frame A: Safety boundary shift**
  - `Dangerous conversations are not filtered by sequence-only or downstream checks.`
- **Frame B: Real interoperability**
  - Position SKILL/Agent Skills as the distribution substrate, not a format preference.
  - Emphasize support evidence from major hosts instead of promises of perfect universality.
- **Frame C: Measurement-first science**
  - A protocol is only convincing if evaluation shows uplift on multi-turn cases at controlled false-positive risk.
- **Frame D: Decision utility**
  - `Every block returns a decision, uncertainty, and rationale for operators in minutes, not post hoc reports.`
- **Frame E: De-risking arc**
  - Hackathon proves evidence-backed feasibility; fellowship deepens reproducibility, scale, and portability.

### Current state against these frames

Current implementation evidence is already aligned to the attractor order:

- **Boundary shift:** implemented through `bio-trace` + `bio-guard` workflow in all host paths.
- **Interoperability grounding:** one deep reference + two compatibility hosts with a populated `deviation_matrix`.
- **Measurement-backed claim:** `recall@5%FPR` comparison tables exist and are tied to `artifacts/metrics/outcome.json`.
- **Operator utility:** decision envelopes, rationale, and traceability fields are present in seed fixtures.
- **De-risking:** results are informative rather than dominant, which is acceptable if paired with explicit revision pathways.

### Judge-facing frame-to-evidence map

- **Frame: boundary shift** → `artifacts/records/seed_screen.jsonl`, `artifacts/records/skill_bio_guard.json`.
- **Frame: interoperability** → `artifacts/conformance/host_capability_profile*.json`, `artifacts/conformance/deviation_matrix.csv`.
- **Frame: measurement-backed** → `artifacts/metrics/hackathon_results.md`, `artifacts/metrics/ablation_results.md`, `artifacts/metrics/confusion_matrix.csv`.
- **Frame: operator utility** → `artifacts/metrics/reproducibility.md`, `artifacts/metrics/reproducibility.json`, `artifacts/records/screen_success.jsonl`.
- **Frame: de-risking** → `docs/Fellowship_Implementation_Plan.md`, `docs/Operational_Runbook.md` and the outcome map below.

## 4) Scoring-to-execution plan (judge rubric to tasks)

The judging rubric in your prompt is strong and explicit. Convert it into concrete pass conditions:

### Dimension 1: Impact Potential & Innovation

Goal: score 4+ (Exceptional/Significant target).

- Novelty claim limited to one proposition: **portable conversation-layer protocol for bio-LLM interfaces**.
- Explicitly state what is *not* claimed: no replacement for downstream screening, no standalone sequence-security claim.
- Include one concrete cross-host interoperability claim and its reproducible evidence set.
- Include a concrete implication line: what this changes for operators in one paragraph.

### Dimension 2: Execution Quality

Goal: score 4+.

- Primary test: recall@5%FPR uplift against baselines on multi-turn attack data.
- Secondary checks: reproducibility (seed + command log), latency, uncertainty calibration, inter-annotator alignment.
- Keep the protocol contract locked (`spec/*`) and run an immutable validation pass before narrative writing.
- Publish exactly one clean primary comparison table and one ablation note; avoid scattershot claims.
- A non-dominant result is still high-quality if:
  - the protocol revision path is specific and tied to observed miss classes, and
  - the same evidence is reproducible from the exact command set in Section 8.

### Dimension 3: Presentation & Clarity

Goal: score 4+.

- Keep report to an 8-section core: intro, related work, method, results, discussion, limitations, dual-use, roadmap.
- Use the same one-sentence thesis in abstract, intro, system design, and conclusion.
- Add the required appendix at the end; do not bury failure modes in the main narrative.

### Dimension 4: Recursive Red-Team Closure for Top-Scores

Run this as a scripted adversarial pass in the final hour:

- **Impact:** answer the question in 60 seconds with one high-signal sentence.
- **Execution:** rerun core commands and reproduce the primary, ablation, and portability evidence from hashes.
- **Clarity:** explain outputs and operator implications in one 120-second walkthrough.

Pass condition: all three checks must be recorded in `artifacts/docs/report_draft.md` as a closure note and any miss must map to explicit fellowship remediation.

## 5) Ambitious Gap-Closure Plan

BioGuard is already coherent as a protocol thesis. The gap to a likely-winning submission is concentrated in evidence, portability, operator utility, and presentation.

### Priority 1: Stronger proof

- Replace the current synthetic-only impression with a larger adversarial benchmark slice.
- Promote one primary table with tier-specific results and one ablation table.
- Ensure the primary outcome is clearly one of:
  - positive uplift,
  - partial uplift with strong trade-off story,
  - or informative failure with a protocol revision path.

### Priority 2: More visible portability

- Keep one deep host integration as the main proof path.
- Add two additional host compatibility demonstrations, even if one or both are parity/smoke rather than full production depth.
- Publish a compact host deviation matrix instead of claiming seamless universality.

### Priority 3: Operator-grade demoability

- Add a replayable audit narrative:
  - request comes in,
  - BioGuard screens it,
  - operator sees decision + rationale + uncertainty + trace,
  - operator can replay and inspect why the decision was made.
- This should be demoable in 2-3 minutes without requiring explanation of the whole repo.

### Priority 4: Submission polish

- Promote one memorable figure/table.
- Produce a clean 150-word abstract, PDF report, and demo script.
- Keep the appendix strong enough that it signals fellowship-grade seriousness rather than hackathon-only enthusiasm.

Current status checkpoint:

- `artifacts/metrics/outcome.json` currently reports **success** (`winner=bioguard`) under strict-FPR comparison, with conservative-baseline threshold notes.
- Existing evidence now foregrounds measurable uplift plus constrained-precision interpretation.
- The highest-priority gap is now robustness: which miss classes remain under richer adversarial stress and where to harden next.
- The highest-signal corrective action is to keep the outcome proof bounded and explicit:
  - what was confirmed,
  - what remains under-tested,
  - what changes next.

## 6) Hackathon implementation (3 days, concurrent model)

Use a **parallel workstream model** to avoid bottlenecks and keep quality high.

### Role split

- **Chief integrator (lead):** thesis integrity, final rubric alignment, final freeze.
- **Workstream 1: Protocol lock**  
  - Confirm `spec/*` invariants and API contracts.
  - Produce checklist for required contract artifacts and version IDs.
  - Output: `artifacts/checks/protocol_lock.json` with pass/fail state and open items.
- **Workstream 2: Evaluation engineer**  
  - Produce fixtures, run baseline comparisons, and draft result tables/plots.
  - Output: `artifacts/metrics/hackathon_results.md` + `artifacts/metrics/bootstrap.csv`.
- **Workstream 3: Host/runtime integration**  
  - Deliver runnable host path and API smoke tests (`/v1/screen`, `/v1/evaluate`).
  - Output: `artifacts/records/screen_success.jsonl`, `artifacts/records/screen_bad_request.jsonl`, `artifacts/records/screen_bad_contract.jsonl`, `artifacts/conformance/host_capability_profile.json`, and `artifacts/conformance/deviation_matrix.csv`.
- **Workstream 4: Report engineer**  
  - Draft abstract, methods text, and the dual-use appendix.
  - Output: `artifacts/docs/report_draft.md` and `artifacts/docs/Limitations_DualUse.md`.

If direct parallel contributors are unavailable, sequence tasks with strict handoff times (every 90 minutes check-in).

Recommended workstream prompts:

- Protocol lock: `Validate that spec files parse, required fields are present, and `/v1/screen` output schema matches `decision_envelope.schema.json`; return a JSON pass/fail report only.`
- Evaluation engineer: `Run the baseline matrix on seeded multi-turn cases, compute recall@5%FPR and bootstrap CI, and return a compact metrics table with significance labels.`
- Integration engineer: `Create one deep `/v1/screen` and `/v1/evaluate` host path plus two additional host compatibility artifacts, including 200/400/422 examples, timing profile, and explicit deviation notes.`
- Report engineer: `Write 150-word abstract + limitations/dual-use appendix draft and a one-paragraph implication section from the operator perspective.`

### Day 0 (prep, same day before start)

- Finalize thesis in one paragraph.
- Freeze a 500-case adversarial multi-turn suite and baseline list by default; if constrained, fallback requires explicit tier-balance reason and a reproducibility note.
- Seed output folder and artifact manifest.
- Confirm two acceptance tests:
  - `/v1/screen` schema validation success.
  - one reproducible baseline metric script.

### Day 1 (protocol core)

- Lock `bkt-v1.0` contract and the BioGuard Skills Profile.
- Stand up one deep host path and begin two additional host parity paths.
- Export deterministic trace set and operator replay flow.
- Produce draft “Methods”, “Why this matters”, and “Portability” sections.
- Add a one-line `submission_surface` manifest note that code-only packaging excludes docs.

### Day 2 (evidence generation)

- Run baseline matrix with:
  - BioGuard (protocolized flow),
  - keyword-only baseline,
  - Llama Guard 3,
  - GPT-5.4 zero-shot, and
  - both pre- and post-inference-only baselines.
- Run ablations that include at least `pre-inference-only` and `post-inference-only` as a protocol-necessity check.
- Generate: latency summary, portability notes, top misses, and reviewer-safe explanations for false positives.

### Day 3 (finalization and submission integrity)

- Final report first full draft.
- Add quantitative results table + bootstrap CIs + significance labeling.
- Add required appendix:
  - limitations and edge cases,
  - dual-use risks,
  - responsible disclosure recommendations,
  - ethical considerations,
  - future work.
- Add short reproducibility box (contract versions, manifest IDs, model IDs, seeds, and command log hash).
- Add demo script or 3-5 minute video outline.
- Add portability matrix with explicit host deviations.
- Final scoring pass against Dimension matrix (Section 4).
- Insert explicit `Informative Failure Decision` paragraph using the schema in Section 7.

### Conformance Suite Workstream (required by all days)

Submission quality depends on a dedicated conformance suite, not only benchmark performance.

- `artifacts/conformance/host_capability_profile.schema.json` and per-host profile JSON files define supported features, output contracts, and host limitations.
- `artifacts/conformance/deviation_matrix.csv` logs each host against protocol requirements (`PASS`, `FALLBACK`, `MISSING`).
- `artifacts/conformance/conformance_report.md` turns the deviation matrix into operator- and judge-readable evidence.

A host path is accepted for the 3-day submission when it:

- produces valid schema-compliant decision envelopes,
- includes request/trace hashes for replay,
- reports explicit feature fallback instead of silently dropping unsupported checks,
- and preserves protocol output for identical inputs.

### 6b) Recursive Red-Team Critique Pass (required before final freeze)

Apply this red-team pass in the final 4-hour window and record results in
`artifacts/docs/report_draft.md`:

1. **Impact/Potential adversarial reviewer**
   - Ask: "If I don't care about biosecurity, why is this different from 'another AI filter'?"
   - Evidence required: one-sentence framing + one requirement artifact (`docs/AIxBio_Hackathon_Execution_Package.md` + `spec/bioguard_api.openapi.yaml`).
2. **Execution-quality adversarial reviewer**
   - Ask: "Can I rerun this and get the exact numbers shown in the primary table?"
   - Evidence required: command block + `artifacts/metrics/outcome.json` + `artifacts/evidence/report_index.json` in the appendix.
3. **Clarity adversarial reviewer**
   - Ask: "Can I explain what was tested and what was learned in 120 seconds?"
   - Evidence required: one paragraph in intro/conclusion that matches thesis + failure interpretation sentence.

If any item fails, include the weakness in the same submission as a `What we could not yet show yet what this proves` paragraph, with remediation in fellowship milestones.

## 7) Failure-First Closure Template (required for top-scores)

If `artifacts/metrics/outcome.json` is `informative_failure`, use this exact one-paragraph frame in abstract + discussion:

**"The primary contribution is a protocol failure map: BioGuard did not increase recall@5%FPR over the best baseline on this run, but it generated a reproducible ranking of misses that cleanly separates three contract revisions for future protocol gain: tier-2 conversation-window compression, decision threshold tuning for `uplift` under task decomposition, and host fallbacks where `bio-trace` coverage is unavailable."**

The paragraph is required to include:

- **What failed:** concise condition-by-condition miss class.
- **What to change:** one concrete revision hypothesis.
- **Why still strong:** what operators and standards builders can implement immediately.

## 7) Required artifacts for an ambitious-winning submission

Use this checklist to avoid missing any hard-to-spot requirement:

1. `make submission-surface` produces a code-only package containing only runtime + implementation surface (`src`, `spec`, `skills`, `scripts`, `Makefile`, `pyproject.toml`) and no docs.
2. `/v1/screen` contract outputs in `decision_envelope` schema on seeded fixtures.
3. Concrete `SKILL.md` blocks exist for `bioguard-bkt-scoring`, `bioguard-bio-trace`, and `bioguard-bio-guard`, with smoke outputs checked into `artifacts/records/`.
4. Deterministic run of 500 adversarial multi-turn tests by default; if lower, justify why and keep the tier balance explicit.
5. One deep host integration and two additional host compatibility demonstrations.
6. One primary results table, one ablation table, and one portability matrix.
7. One appendix of top misses / false positives with protocol revision notes.
8. Reproducibility snippet with exact versions:
   - `spec/bkt_contract_v1.0.json`
   - `spec/benchmark_manifest_v1.0.json`
   - `spec/bioguard_api.openapi.yaml`
   - commit hash + dataset split hash + seed
9. `Limitations and Dual-Use Considerations` appendix (non-optional for top scoring).
10. Demo script or short video showing operator utility.

## 8) Strong vs weak submission boundary

### What strong looks like

- One portable protocol claim with visible runtime substance.
- Stronger-than-baseline evidence or a deeply informative failure.
- Clear operator story, not just a classifier story.
- Portability evidence that is concrete but not overclaimed.
- Fellowship-grade appendix and reporting discipline.

### What still must not become the thesis

- Claims about BioSeq as a primary contribution.
- Open-weight fine-tuning as success precondition.
- General CBRN platformization beyond the bio-LLM conversation boundary.

Everything beyond this becomes fellowship debt, not hackathon debt.

## 9) Fellowship carry-through (explicit continuity plan)

The hackathon package maps directly to `docs/Fellowship_Implementation_Plan.md`:

- Day 0–3 outputs become **Milestone A** evidence in the fellowship plan.
- Fellowship expands to:
  - broader host compatibility,
  - benchmark growth and quality gates,
  - cross-host friction report,
  - final publication-grade report with protocol and governance sections.

Top submissions are tracked for fast-track in this sequence. The strategic value is to frame the fellowship as a protocol hardening phase rather than a project restart:

- **If accepted for top scores:** fellowship milestone mapping starts with `Milestone B` and `Milestone C` as direct extensions.
- **If informative-failure remains:** fellowship starts with protocol revision and host-friction reduction rather than raw metric re-optimization.

## 10) Required text templates

Use these verbatim where useful:

- **Abstract (≤150 words):**  
  `BioGuard is a portable conversation-layer biosecurity protocol for bio-LLM interfaces. It uses the Biological Knowledge Transfer (BKT) scoring contract to evaluate whether protocolized context-aware screening detects hazardous biological knowledge transfer better than stateless baselines. The hackathon package aims to show an ambitious but disciplined proof: a locked contract, a concrete Skill-based deployment surface, one deep host integration, additional host compatibility demonstrations, multi-turn adversarial evaluation, and a reproducibility trail across contract versions and baselines. We do not claim universal deployment readiness; we test whether the protocol meaningfully improves screening at the conversation boundary and report both uplift and failure modes to inform operational and standardization pathways.`
- **Failure interpretation sentence:**  
  `A result is useful even without full uplift, provided we can explain one mechanism-level failure mode and propose a revision path for a protocol-level boundary adjustment.`

## 11) Sources consulted

- APART event overview and track framing: [AIxBio Hackathon Sprint Page](https://apartresearch.com/sprints/aixbio-hackathon-2026-04-24-to-2026-04-26)
- Event listing details and schedule: [AIxBio Hackathon on Luma](https://luma.com/aixbio-hackathon-2026-sf)
- Fellowship alignment and programme expectations: [AIxBio Fellowship FAQ](https://www.aixbiosecurity.com/faq)
