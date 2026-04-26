# BioGuard Report Summary

## Abstract

BioGuard tests a simple biosecurity idea: risky biological know-how can be assembled across a conversation, so the conversation itself should be screened. The system scores biological knowledge transfer across turns and returns one replayable decision record.

In the current seeded benchmark, BioGuard outperforms the included stateless baselines at a fixed 5% false-positive operating point. The result is best read as prototype evidence. It shows that conversation state can add signal, and it gives a clear map of where the protocol still misses cases.

## What Was Built

- A BKT scoring contract for scope, depth, and uplift.
- A `/v1/screen` runtime that returns a decision envelope.
- Four portable skills for event scoring, conversation tracing, full guard operation, and optional sequence review.
- A seeded benchmark path with fixed manifest, seed, baselines, and output artifacts.

## Main Result

Latest included run:

- outcome: `success`
- winner: `bioguard`
- margin over strongest baseline: `+0.2888` recall at 5% FPR

Primary artifacts:

- `artifacts/metrics/hackathon_results.md`
- `artifacts/metrics/ablation_results.md`
- `artifacts/metrics/reproducibility.md`
- `artifacts/metrics/error_taxonomy.md`

## Interpretation

The result does not prove deployment readiness. The current corpus is synthetic, the scoring layer is heuristic, and host portability needs deeper independent replay.

The useful claim is narrower: BioGuard makes the conversation boundary measurable. When the system fails, the failure is tied to a contract, a turn window, and a reproducible artifact path.

## Next Revision Targets

1. Add independent label review for the benchmark.
2. Expand cases where intent is spread across benign-looking turns.
3. Improve threshold calibration while preserving the fixed-FPR operating point.
4. Deepen host replay so portability is tested beyond smoke checks.
5. Keep high-risk biological traces out of public artifacts unless separately reviewed.
