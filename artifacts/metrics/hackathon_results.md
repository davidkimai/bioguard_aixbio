# Primary Comparison Table (Recall@5%FPR)

| Condition | Recall@5%FPR | CI95 | Precision | Specificity | FPR | Threshold | Threshold Note | Δ vs BioGuard | Significant vs Baseline |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
|bioguard|0.2888|0.2386-0.3448|1.0000|1.0000|0.0000|0.2380|selected threshold satisfies strict 5% FPR target|+0.0000|true|
|keyword-filter|0.0000|0.0000-0.0137|0.0000|1.0000|0.0000|1.0000|no threshold with FPR <= 0.05; using all-negative conservative operating point|-0.2888|true|
|llama-guard-3|0.0000|0.0000-0.0137|0.0000|1.0000|0.0000|1.0000|no threshold with FPR <= 0.05; using all-negative conservative operating point|-0.2888|true|
|gpt54-zero-shot|0.0000|0.0000-0.0137|0.0000|1.0000|0.0000|1.0000|no threshold with FPR <= 0.05; using all-negative conservative operating point|-0.2888|true|

Primary outcome: success
Success: BioGuard outperformed best baseline by 28.88% on recall@5%FPR with significance support.
