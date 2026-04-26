---
name: bioguard-bio-seq
description: Optional sequence-oriented extension for BioGuard. Use only for ablation or future extensions where extracted DNA or amino acid content needs a secondary risk pass.
---

# BioGuard Bio Seq

This skill is an optional extension module.

## Use this skill when

- sequence-like content has already been extracted from a conversation
- you are testing whether sequence-oriented scoring adds signal beyond BioTrace
- you are running ablations for fellowship-scale validation

## Input

Provide JSON with:

- `sequence`
- optional metadata describing source turn or source conversation

## Output

Returns:

- `status`
- `block`
- `sequence_hash`
- `findings`
- `risk_profile`

## Invocation

```bash
python scripts/bioguard_skill_proxy.py --mode bio-seq
```

## Notes

- This module is explicitly secondary in the current project scope.
- The hackathon submission should not depend on this skill succeeding.
