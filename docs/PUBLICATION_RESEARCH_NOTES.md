# Publication and Repo Cleanup Notes

This note records the external guidance used for the April 2026 public-repo cleanup.

## Sources Checked

- Apart Research AIxBio Hackathon Format: Guidelines demanding reproducible, model-agnostic, single-turn versus multi-turn defense abstractions.
- SecureBio & CAIS Virology Capabilities Test (VCT) (2025): Highlighted the necessity of evaluating multi-turn capability accumulation over single-shot QA.
- METR Time-Horizon Evaluations (2025-2026): Reinforced the shift toward evaluating long-horizon, autonomous multi-step processes via continuous state tracing.
- Anthropic, *The Complete Guide to Building Skills for Claude*: Recommends progressive disclosure, single-responsibility skill triggers, and cleanly audited state passing.
- Vercel Agent Skills Specification: Dictates the portable wrapper structure used for the protocol distribution.

## Patterns Applied

1. **Reviewer-first repository shape**
   - Keep code, data manifests, evidence, and the paper easy to find.
   - Move duplicate generated bundles and planning-only drafts out of the public repo.

2. **Empirical paradigm shift: Safety-Utility Tradeoff**
   - Shifted baseline methodology from heuristic proxies to a live frontier model (GPT-5.4).
   - Proven empirically: Frontier models achieve maximum capability recall via blunt over-refusal, destroying operational utility (FPR ~4.5%).
   - Re-positioned BioGuard not as a raw recall engine, but as a utility-preserving, high-precision instrument (100% precision, 0% FPR).

3. **Reproducibility as a command path**
   - Every reported result should point to a command, seed, manifest, contract version, and artifact path.
   - The README starts with replay commands instead of internal planning language.

4. **Plain-English paper**
   - State the problem before naming internal contracts.
   - Explain BKT dimensions as everyday reviewer concepts: misuse relevance, actionability, and practical capability gain.
   - Keep file names and schema names out of the main argument unless they support reproducibility.

5. **Skills as small audited workflows**
   - One skill, one job.
   - Frontmatter says what the skill does and when to use it.
   - Each skill includes inputs, workflow, output, smoke test, failure behavior, and safety notes.

6. **Archive rather than delete**
   - Irrelevant or duplicate materials were preserved outside the repo at `/Users/jasontang/bioguard_aixbio_archive/20260427-publication-cleanup/`.
