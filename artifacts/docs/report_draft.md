# BioGuard Hackathon Report Draft (Submission Formatted)

## Abstract

BioGuard is a portable conversation-layer biosecurity protocol for bio-LLM interfaces. It tests one claim: whether a shared Biological Knowledge Transfer (BKT) scoring contract detects dangerous biological capability transfer in multi-turn conversations better than stateless baselines at fixed 5% false-positive risk.

The hackathon package is implementation-forward rather than platform-forward: a `SKILL.md`-driven contract surface, reusable `/v1/screen` API, seeded BioSession evaluation, and explicit reproducibility + portability artifacts (`spec/*`, `artifacts/*`, and manifest hashes). We report protocol-level evidence as success, partial success, or informative failure depending on recall uplift and the quality of the miss map.

## Why This Is Compelling for Judges

BioGuard’s strongest frame is the control-layer shift:

1. **Conversation is where risk is assembled.** Multi-turn exchanges can transfer dangerous design knowledge before any order request or sequence output appears.
2. **Protocol, not hype.** We define a portable contract first (`spec/bkt_contract_v1.0.json`) and use it across runtimes via SKILL.md primitives.
3. **Measurement is non-negotiable.** The thesis is accepted only through recall@5%FPR and significance-aware comparisons.
4. **Operators get usable outputs.** Decisions return risk rationale, uncertainty, and replayable traces instead of opaque model logits.
5. **Concreteness over claims.** Portability is presented as measurable conformance across three host profiles, with every `FALLBACK` and `RESTRICTED` row explicitly owned and mitigated.
6. **Persona-shift failure framing.** A key failure mode we expose is gradual context-driven misalignment (a safe-to-detect, high-stakes failure frontier).

The same package is already mapped to fellowship continuation: `docs/Fellowship_Implementation_Plan.md` for scale, benchmark hardening, and protocol revisions.

## 1. Introduction

Current safeguards are largely downstream and risk-aware at the sequence output layer. This creates a gap at the live bio-LLM conversation boundary where intent is assembled across turns before any downstream action is taken. BioGuard addresses this gap with a thin, portable protocol (not a monolith): BKT is the operational scoring contract, and `/v1/screen` implementations consume the same contract across interoperable runtimes.

## 2. Related Work

- Sequence-first screening workflows at synthesis providers.
- Static prompt hardening and post-inference filtering.
- Conversation-level safety policy and context-aware moderation.
- Open interoperability standards for agent skills and runtime portability.

## 3. Method

- Contract layer: `spec/bkt_contract_v1.0.json`.
- API/ schema layer: `spec/bioguard_api.openapi.yaml`, `spec/decision_envelope.schema.json`.
- Execution state: `spec/execution_state_manifest_v1.0.json`.
- Skill pack: `skills/bioguard-bkt-scoring`, `skills/bioguard-bio-trace`, `skills/bioguard-bio-guard`.
- Optional module: `skills/bioguard-bio-seq` for ablation.
- Data: seeded 500-case BioSession manifest in `spec/benchmark_manifest_v1.0.json`.
- Execution commands:
  - `make init`
  - `python -m bioguard check`
  - `python -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl`
  - `make skills`
  - `python -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --splits test --seed 1 --out artifacts/metrics`

## 4. Results

- Primary task: recall@5%FPR on multi-turn harmful intent detection.
- Baseline matrix was run for conditions: `bioguard`, `keyword-filter`, `llama-guard-3`, `gpt54-zero-shot`, `pre-inference-only`, `post-inference-only`.
- Primary artifact: `artifacts/metrics/results.json`.
- Primary table: `artifacts/metrics/hackathon_results.md`.
- Ablation table: `artifacts/metrics/ablation_results.md`.

Latest run outcome:
- `status`: `success`
- `winner`: `bioguard`
- `metric_deltas`: `bioguard` vs best baseline on recall@5%FPR was `+0.2888` (significant uplift under strict 5%FPR operating mode).

## 5. Error Taxonomy

- Top false positives and false negatives are exported in `artifacts/metrics/error_taxonomy.md`.
- On the latest seeded run: no top-level false positives above configured threshold; five highest-scoring false negatives included multi-turn covert transfer phrases and ambiguous “scaling/distribution” wording.

## 6. Reproducibility and Audit

- Reproducibility manifest: `artifacts/metrics/reproducibility.md`.
- Evidence index: `artifacts/evidence/bundle_manifest.json`.
- Command log + checksums: `artifacts/evidence/report_index.json`.
- Deterministic generation commands are anchored in `docs/Operational_Runbook.md`.

## 7. Discussion

BioGuard demonstrates a feasible protocol-first intervention with measurable, auditable outputs and reproducible failure-mode analysis. The seeded outcome now shows a strict-FPR uplift for BioGuard, while preserving the same protocol revision pathways for future robustness:
- Raise sensitivity in specific harmful intent channels.
- Expand multi-turn adversarial coverage in tier-2 and tier-3 cases.
- Pre-register a cross-host portability matrix in fellowship phase.

## 7a. Baseline Calibration Observation

Baseline conditions (`keyword-filter`, `llama-guard-3`, `gpt54-zero-shot`) did not produce any positive calls at the strict 5%FPR operating target. The evaluator now reports this explicitly as an `all-negative conservative operating point` to avoid false-positive interpretation. That is a protocol-strengthening signal: the same protocol scaffold is useful even when a baseline has low operating leverage under the same constraint.

## 7b. Failure and Revision Map

Primary outcome from `artifacts/metrics/outcome.json`:

- `status`: `success`
- `winner`: `bioguard`
- `winner margin`: 0.288809 recall@5%FPR

Remaining hypothesis-led revision path:

1. **Threshold calibration gap**: all-negative handling is now explicit, but tuning policy may improve recall while preserving FPR constraints.
   - Action: run a small calibration sweep and publish the threshold policy with reproducibility guardrails.
2. **Tier coverage gap**: failures cluster in higher-complexity tier-2 and tier-3 patterns.
   - Action: add more decomposed transfer examples and session-history-sensitive windows.
3. **Host fallback gap**: any `fallback` rows in conformance require explicit behavior tagging for operator transparency.
   - Action: declare fallback policy in deployment docs and maintain explicit host compatibility profile.

This map is the principal contribution of this run: it identifies where the protocol should change next while preserving the core thesis and architecture.

## 8. 120-Second Explanation

BioGuard targets the real risk surface in AI-supported biodesign: dangerous biological knowledge can be assembled across multiple turns before any explicit output is blocked.
We test that by freezing a portable BKT contract and implementing it as Agent Skills blocks (`SKILL.md`) with a single `/v1/screen` decision surface and explicit audit outputs.
The protocol checks not for a one-shot refusal failure, but for context-accumulation drift where intent and capability can silently shift over time.
In this stage, we run a seeded 500-case BioSession evaluation plus two host compatibility probes at strict 5%FPR, generating one primary table, one ablation table, and reproducible evidence commands.
BioGuard is a success in this run with `+0.2888` recall uplift over the strongest baseline under the same constraint; the remaining value is that every miss is mapped to a concrete contract revision path.

## 9. Limitations and Dual-Use Considerations

### Limitations
- Synthetic seed dataset (500 cases per split in this stage).
- Heuristic BKT scoring only; no deep model-based biological reasoner in this MVP.
- Current evidence includes 3 host compatibility profiles with explicit fallback notes, not full native parity.
- No inter-rater label calibration from external adjudicators yet.

### Failure Interpretation
- Any outcome remains operationally valuable if it identifies concrete contract revisions (for example, stronger session-window handling or escalation calibration).

### Dual-Use Risks
- Public methodology and corpus templates can be used by adversaries if misapplied.
- Releasing detailed bypass examples requires staged disclosure with sponsor review.

### Responsible Disclosure
- If a reproducible unsafe false-negative class is observed, defer broader artifact release until a mitigation is included.
- Route any high-risk bypass findings through sponsor safety review with confidence, evidence, and remediation timeline.

### Ethics
- The protocol is intended for defensive control, not surveillance or punitive use.
- Operator-facing decisions include uncertainty labels and audit trails for accountable escalation.
