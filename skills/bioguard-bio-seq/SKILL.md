---
name: bioguard-bio-seq
description: Optional BioGuard sequence-risk extension. Use only when extracted DNA or amino-acid-like content needs a secondary pass for ablation, future validation, or explicit sequence-safety review.
license: Apache-2.0
version: 1.0.0
compatibility: Agent Skills-compatible hosts with Python 3.11 and repo access.
---

# BioGuard Bio Seq

## Purpose

Use this skill only as a secondary check. BioGuard's main claim is conversation-level screening; this skill is for sequence-like content that has already been extracted and approved for review.

## Inputs

Provide JSON with:

- `sequence`: DNA, RNA, or amino-acid-like string
- optional source metadata, such as `conversation_id` or `turn_index`

## Workflow

1. Check whether a sequence was provided.
2. Hash the sequence instead of echoing it when possible.
3. Return sequence findings for ablation or future validation.
4. Do not override the main BioGuard conversation decision by default.

## Output

Returns:

- `status`: `skip`, `ok`, or `error`
- `block`: `bioguard-bio-seq`
- `sequence_hash`
- optional `sequence_findings`
- `risk_profile`
- optional notes

If no sequence is provided, return:

```json
{"status":"skip","reason":"no_sequence"}
```

## Smoke Test

```bash
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py \
  --mode bio-seq \
  --input artifacts/requests/skill_bio_seq_request.json
```

Expected result: either an `ok` payload with hashed sequence metadata or a clear `skip` result.

## Failure Behavior

- Missing sequence is not a hard failure; it is a `skip`.
- Invalid JSON returns a typed error.
- Public outputs should prefer hashes and summaries over raw sequence content.

## Safety Notes

Do not publish raw high-risk sequences or operational biological instructions from this skill without separate review.
