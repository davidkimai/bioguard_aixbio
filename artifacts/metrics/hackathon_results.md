# Primary Comparison Table (Recall@5%FPR)

| Condition | Recall@5%FPR | CI95 | Precision | Specificity | FPR | Threshold | Threshold Note | Δ vs BioGuard | Significant vs Baseline |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
|bioguard|0.2888|0.2386-0.3448|1.0000|1.0000|0.0000|0.2380|selected threshold satisfies strict 5% FPR target|+0.0000|true|
|keyword-filter|0.0000|0.0000-0.0137|0.0000|1.0000|0.0000|1.0000|no threshold with FPR <= 0.05; using all-negative conservative operating point|-0.2888|true|
|gpt54-zero-shot|1.0000|0.9863-1.0000|0.9652|0.9552|0.0448|0.1800|selected threshold satisfies strict 5% FPR target|+0.7112|true|

Primary outcome: informative_failure
Informative failure: BioGuard did not improve recall@5%FPR versus the strongest baseline. This still supports protocol revision by tier/scenario.
