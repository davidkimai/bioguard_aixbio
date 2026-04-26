# BioGuard Conformance Report (Protocol Ecosystem Seed)

## Host Profile Set

- `artifacts/conformance/host_capability_profile.json` (reference profile)
- `artifacts/conformance/host_capability_profile_host-2.json` (codex-host)
- `artifacts/conformance/host_capability_profile_host-3.json` (github-copilot-host)
- `artifacts/conformance/deviation_matrix.csv` (human-readable status ledger)
- `artifacts/conformance/deviation_matrix.json` (schema-valid JSON ledger)
- Validation date: 2026-04-25
- Contract version: `bkt-v1.0`

## Status

- Protocol kernel: PASS
- Schema validation: PASS (reference default path)
- Host capability coverage: PASS for base requirements, with explicit fallback notes
- Host-1 replayability: PASS
- Portability measurement: PASS (`deviation_tracking` populated across 3 hosts)
- Remote audit export: FALLBACK on all current hosts

### Fallback Governance

- `reference-host/audit_hash_replay_supported`: owner=`core-implementation`, decision= `accepted`; reason=`host-native remote audit export not exposed`; remediation=`publish bounded replay contract and add host-native export hooks`.
- `codex-host/schema_validation`: owner=`protocol-engine`, decision= `accepted`; reason=`schema validator not exposed in probe`; remediation=`expose host-native schema validation`.
- `codex-host/audit_hash_replay_supported`: owner=`core-implementation`, decision= `accepted`; reason=`export API is probe-local only`; remediation=`attach replay artifact path in host metadata`.
- `github-copilot-host/post_inference`: owner=`core-implementation`, decision= `monitor`; reason=`manual fallback scoring path used`; remediation=`complete native post-inference path or designate partial-deployment profile`.
- `github-copilot-host/schema_validation`: owner=`protocol-engine`, decision= `repair`; reason=`host-native enforcement endpoint not exposed`; remediation=`document fallback contract and explicit warning`.
- `github-copilot-host/audit_hash_replay_supported`: owner=`core-implementation`, decision= `accepted`; reason=`no native replay export endpoint`; remediation=`provide seeded fixture replay guidance until export is native`.

## Host Matrix Summary

### Reference Host (`reference-host`)
- Core contract + API validation: PASS
- Pre/post inference screening: PASS
- Audit replay: FALLBACK (deterministic fixture replay only)

### Codex Host (`codex-host`)
- Contract/API parity: PASS
- Pre/post inference: PASS
- Native schema validation: FALLBACK
- Audit replay: FALLBACK

### GitHub Copilot Host (`github-copilot-host`)
- Contract/API parity: PASS
- Pre-inference: PASS
- Post-inference: FALLBACK (manual scoring path in this probe)
- Native schema validation: RESTRICTED
- Audit replay: FALLBACK

## Interpretation

The 3-host profile now demonstrates a measurable portability boundary instead of a single-host claim:
- contract semantics are preserved on the required core path,
- protocol behavior differs mainly in observability and post-inference enforcement support,
- and all deviations are explicitly declared for operator decisioning.

Priority for next release:
1. resolve `github-copilot-host` schema restrictions or mark them as bounded interoperability boundaries,
2. expose native audit export for all hosts to remove remaining `FALLBACK` status,
3. preserve evidence fidelity for each requirement in reusable host traces.
