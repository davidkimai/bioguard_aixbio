# Ablation Comparison Table (Pre/Post Inference Checks)

| Condition | Recall@5%FPR | CI95 | Precision | FPR | Threshold | Threshold Note | Δ vs Protocol | Significant vs Protocol |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
|pre-inference-only|0.6354|0.5772-0.6899|1.0000|0.0000|0.2800|selected threshold satisfies strict 5% FPR target|+0.3466|true|
|post-inference-only|0.4224|0.3657-0.4812|1.0000|0.0000|0.1800|selected threshold satisfies strict 5% FPR target|+0.1336|true|

Primary protocol condition: `bioguard`.
Interpretation: pre/post-only ablations are evidence against or for the need for dual-pass screening.
