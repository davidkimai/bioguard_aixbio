# Limitations and Dual-Use Considerations

## Limitations

- **Seed corpus scope:** current BioSession split is a synthetic 500-case corpus per split for this state and is not representative of full operational distributions.
- **Heuristic scoring:** BKT currently uses keyword-based heuristics and does not perform deep biological model reasoning.
- **Host breadth state:** this stage includes a reference-host plus two additional compatibility profiles; full native-portability parity remains bounded by host-specific fallback behavior.
- **No model adapter calibration:** sequence analysis and human override controls are present in schema but minimal in implementation.

## Failure Interpretation

- If recall uplift is not observed at fixed FPR, the run still contributes an evidence boundary for:
  - missed failure mechanisms,
  - false-positive trade-offs,
  - contract revision priorities.

## Dual-Use Risk

- Public release artifacts avoid raw biological sequence data and include only synthetic or protocol metadata.
- The protocol and outputs can be reused by third parties; deployment documentation should include safe controls and clear escalation points.

## Responsible Disclosure

- If reproducibility reveals an unsafe bypass or high-risk false negative class, release should be delayed until mitigation is available.
- Report any external benchmark weaknesses to the fellowship sponsor with impact and confidence context.
