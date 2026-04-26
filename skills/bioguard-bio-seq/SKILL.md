---
name: bioguard-bio-seq
description: Optional sequence-oriented extension for BioGuard. Use only for ablation or future extensions where extracted DNA or amino acid content needs a secondary risk pass.
---

# BioGuard Bio Seq

This skill is an optional extension module for sequence-based signals.

## Use this skill when

- sequence-like content has already been extracted from a conversation
- you test whether sequence-oriented scoring adds signal beyond BioTrace
- you run ablation studies for fellowship-scale validation

## Input

Provide JSON with:

- `sequence`
- optional metadata describing source conversation or turn

## Output

- `status`: `skip`, `ok`, or `error`
- `block`: `bioguard-bio-seq`
- `sequence_hash`: SHA-256 fingerprint of the submitted sequence
- optional `sequence_findings`
- `risk_profile`
- optional `notes`

When no sequence is provided, this block returns:

```json
{"status":"skip","reason":"no_sequence"}
```

## Invocation

```bash
python3 scripts/bioguard_skill_proxy.py --mode bio-seq --input artifacts/requests/skill_bio_seq_request.json
```

## Notes

- This module is optional and secondary to the protocol thesis.
- The hackathon submission should remain valid without this block succeeding.
