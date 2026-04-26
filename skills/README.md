# BioGuard Skill Pack

This folder packages BioGuard as four portable Agent Skills. Each skill has one job and delegates to the same runtime and contracts used by the paper.

## Skills

- `bioguard-bkt-scoring`: score one text fragment into one BKT event.
- `bioguard-bio-trace`: screen a conversation window before or after model output.
- `bioguard-bio-guard`: run the full operator-facing guard and return one decision envelope.
- `bioguard-bio-seq`: optional sequence-oriented pass for ablations and future work.

## Design Rules

- Keep `SKILL.md` as the entrypoint.
- Keep folder names in kebab case.
- Put trigger conditions in frontmatter descriptions.
- Keep detailed protocol meaning in `spec/*`, not duplicated in prose.
- Include one smoke command and clear failure behavior per skill.

## Smoke Commands

```bash
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py --mode bkt-scoring --input artifacts/requests/skill_bkt_request.json
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json
PYTHONPATH=src python3 scripts/bioguard_skill_proxy.py --mode bio-seq --input artifacts/requests/skill_bio_seq_request.json
```

Or run all four:

```bash
make skills
```

## Contract Sources

- BKT event schema: `spec/bkt_event.schema.json`
- Decision envelope schema: `spec/decision_envelope.schema.json`
- API shape: `spec/bioguard_api.openapi.yaml`
- Human rubric: `docs/BKT_Rubric_Draft.md`
