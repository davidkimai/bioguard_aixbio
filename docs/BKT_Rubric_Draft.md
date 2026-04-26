# BKT Rubric Draft v1.1 (Human-facing)

**Contract version:** `bkt-v1.0`  
**Source file:** `spec/bkt_contract_v1.0.json`  

## Label Definitions

`scope`, `depth`, and `uplift` each use 0.0–1.0 with the same class mapping:

- `low`: 0.00–0.24
- `medium`: 0.25–0.49
- `high`: 0.50–0.74
- `critical`: 0.75–1.00

`scope` assesses misuse relevance of content.
`depth` assesses procedural actionability.
`uplift` assesses incremental feasibility gain.

## Dimension Rationales

Each dimension requires:

- a numeric score,
- a label,
- a short rationale sentence (max 120 chars).

Final decision requires:

- `composite_label` from formula in `bkt_contract_v1.0.json`,
- one final rationale (max 240 chars),
- final `uncertainty` value (`low`, `med`, `high`).

## Composite Rule

`composite = 0.45*scope + 0.35*depth + 0.20*uplift`  
`allow` if `< 0.45`  
`review` if `0.45 <= score < 0.75`  
`block` if `>= 0.75`

## Escalation Rules

Any `critical` in `scope` or `depth` elevates at least to `review`.  
Any two `high` dimensions elevates at least to `review`.  
Missing required fields or schema mismatch defaults to `review` with `uncertainty: high`.
