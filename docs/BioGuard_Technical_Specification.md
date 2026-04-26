# BioGuard Technical Specification

**Status:** public research prototype  
**Contract version:** `bkt-v1.0`  
**Primary paper:** `bioguard_aixbio_submission.tex`

## One-Sentence Summary

BioGuard screens biological AI conversations by tracking risky knowledge transfer across turns, then returns one decision record that can be audited and replayed.

## Problem

Many safeguards look at the final answer, a final sequence, or an ordering step. That is useful, but incomplete. In a real model conversation, a user can gather intent, method, and feasibility across several turns before a risky artifact exists.

BioGuard tests whether that conversation boundary can be made into a portable protocol.

## Core Claim

The main claim is not that BioGuard is a complete biosecurity system. The claim is narrower:

> A shared conversation-level scoring contract can make biological-risk screening more reproducible, more portable across hosts, and easier to improve than a stateless one-turn check.

## Key Terms

- **BKT event:** one observed unit of Biological Knowledge Transfer in a turn or short window.
- **Scope:** how relevant the content is to biological misuse.
- **Depth:** how procedural or actionable the content is.
- **Uplift:** how much practical capability the content appears to add.
- **Decision envelope:** the full screening output, including identifiers, events, host metadata, decision, rationale, and replay fields.
- **Skill pack:** portable `SKILL.md` entrypoints that call the same BioGuard runtime.

## Architecture

BioGuard has five layers:

1. **Contract layer:** `spec/bkt_contract_v1.0.json`, event schema, decision schema, and API shape.
2. **Runtime layer:** `src/bioguard/`, which validates requests, scores events, creates decisions, and evaluates benchmark runs.
3. **Skill layer:** `skills/`, which packages the same behavior for agent hosts.
4. **Evidence layer:** `artifacts/metrics/`, `artifacts/records/`, and `artifacts/conformance/`.
5. **Docs layer:** this directory, kept secondary to the machine-readable contract.

## Runtime Flow

1. A host sends a screen request with conversation turns and a policy profile.
2. BioGuard validates the request and contract version.
3. Each non-empty turn is scored for BKT events.
4. Events are aggregated into a decision: `allow`, `review`, or `block`.
5. The system writes a decision envelope with enough metadata to replay the run.

## Evaluation Flow

The benchmark path compares BioGuard with stateless baselines at a fixed 5% false-positive operating point.

Primary command:

```bash
PYTHONPATH=src python3 -m bioguard evaluate \
  --manifest spec/benchmark_manifest_v1.0.json \
  --splits test \
  --seed 1 \
  --out artifacts/metrics \
  --include-ablations
```

Primary outputs:

- `artifacts/metrics/results.json`
- `artifacts/metrics/hackathon_results.md`
- `artifacts/metrics/ablation_results.md`
- `artifacts/metrics/error_taxonomy.md`
- `artifacts/metrics/reproducibility.md`

## Current Evidence Boundary

The current seeded run reports BioGuard as the winner at strict 5% FPR with a +0.2888 recall margin over the strongest baseline. Treat this as prototype evidence. It is useful because it is replayable and because the misses point to specific revision targets.

Known limits:

- synthetic seeded benchmark,
- heuristic scoring,
- limited host replay depth,
- no external inter-rater label calibration yet.

## Skill Pack Design

The skill pack follows current Agent Skills practice:

- concise frontmatter with specific triggers,
- one job per skill,
- progressive disclosure through the main `SKILL.md` plus repo-level contracts,
- smoke commands for each skill,
- explicit failure behavior.

The four skills are:

- `bioguard-bkt-scoring`: score one text fragment into one BKT event.
- `bioguard-bio-trace`: screen a conversation window.
- `bioguard-bio-guard`: orchestrate the full operator-facing screen.
- `bioguard-bio-seq`: optional sequence-oriented extension for ablation.

## Public Release Rules

- Keep sensitive biological instructions out of public artifacts.
- Do not report a metric without command, seed, manifest, and contract version.
- Do not change `spec/bkt_contract_v1.0.json` without a release-note entry.
- Keep generated duplicate submission bundles out of git; regenerate them only when needed.
