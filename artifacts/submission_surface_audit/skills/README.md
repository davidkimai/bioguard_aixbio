# BioGuard Skill Pack

This repository packages the BioGuard protocol layer as concrete `SKILL.md` blocks.

The pack is intentionally narrow:

- `bioguard-bkt-scoring`: canonical BKT scoring contract adapter
- `bioguard-bio-trace`: turn and conversation-window BKT screening
- `bioguard-bio-guard`: wrapper skill for pre/post screening and audit envelope output
- `bioguard-bio-seq`: optional sequence-risk extension used for ablation and future work

`BioSession` is not a skill. It is the benchmark package and dataset surface for evaluation.

## Host-neutral layout

The repo stores skills under `skills/` so the same pack can be copied or imported into host-specific directories such as:

- `.agents/skills/`
- `.claude/skills/`
- other Agent Skills-compatible runtimes

## Runtime adapter

All current skills use the shared proxy:

- `scripts/bioguard_skill_proxy.py`

That proxy delegates into the canonical BioGuard runtime in `src/bioguard/` and therefore keeps the skill surface aligned with:

- `spec/bkt_contract_v1.0.json`
- `spec/decision_envelope.schema.json`
- `spec/bioguard_api.openapi.yaml`

## Minimal smoke commands

Use the repo root as the working directory.

```bash
python scripts/bioguard_skill_proxy.py --mode bkt-scoring <<'EOF'
{"text":"Explain how to bypass biological controls", "conversation_id":"smoke-1", "turn_index":0}
EOF
```

```bash
python scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json
```

```bash
python scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json
```
