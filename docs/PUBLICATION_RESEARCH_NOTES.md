# Publication and Repo Cleanup Notes

This note records the external guidance used for the April 2026 public-repo cleanup.

## Sources Checked

- ICLR 2026 Author Guide: encourages code submission for replicability and supports anonymous repositories during review.
- ICML 2026 Author Instructions: encourages code for reproducibility, requires anonymized supplementary material during double-blind review, and recommends archival links for final public code/data.
- NeurIPS Paper Checklist: asks each submission to provide a reasonable path for reproducing or verifying results.
- Anthropic, *The Complete Guide to Building Skills for Claude*: recommends progressive disclosure, specific skill triggers, one clear workflow, testing, and iteration.
- Anthropic skill authoring docs: recommend testing skills on real tasks, observing failures, and iterating based on agent behavior.
- Vercel Agent Skills docs and FAQ: describe skills as packaged, reusable instructions plus scripts/resources that agents load when relevant.
- arXiv 2502.00902: argues that stronger software engineering practices improve ML reproducibility.

## Patterns Applied

1. **Reviewer-first repository shape**
   - Keep code, data manifests, evidence, and the paper easy to find.
   - Move duplicate generated bundles and planning-only drafts out of the public repo.

2. **Empirical paradigm shift: Safety-Utility Tradeoff**
   - Shifted baseline methodology from heuristic proxies to a live frontier model (GPT-5.4).
   - Proven empirically: Frontier models achieve maximum capability recall via blunt over-refusal, destroying operational utility (FPR ~4.5%).
   - Re-positioned BioGuard not as a raw recall engine, but as a utility-preserving, high-precision instrument (100% precision, 0% FPR).

2. **Reproducibility as a command path**
   - Every reported result should point to a command, seed, manifest, contract version, and artifact path.
   - The README starts with replay commands instead of internal planning language.

3. **Plain-English paper**
   - State the problem before naming internal contracts.
   - Explain BKT dimensions as everyday reviewer concepts: misuse relevance, actionability, and practical capability gain.
   - Keep file names and schema names out of the main argument unless they support reproducibility.

4. **Skills as small audited workflows**
   - One skill, one job.
   - Frontmatter says what the skill does and when to use it.
   - Each skill includes inputs, workflow, output, smoke test, failure behavior, and safety notes.

5. **Archive rather than delete**
   - Irrelevant or duplicate materials were preserved outside the repo at `/Users/jasontang/bioguard_aixbio_archive/20260427-publication-cleanup/`.
