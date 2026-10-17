---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: the config specifies a 50/50 allocation, but the results show A 52,000 users vs B 47,000 users (52.5% / 47.5%). A chi-square goodness-of-fit test against 50/50 gives chi-square = 253 (df=1), p = 7e-57, i.e. a sample ratio mismatch (SRM). With an SRM the assignment or tracking is broken, so the conversion comparison cannot be trusted.

Naive answer: B converts 3.24% vs A 3.00% = +8.0% lift, z = 2.17, p = 0.030, "statistically significant, B wins", with no mention of the user split.

PASS if report.md flags that the 52,000 vs 47,000 split is inconsistent with the planned 50/50 allocation (sample ratio mismatch / allocation imbalance / unexpected traffic split) AND says this makes the test result unreliable or invalid. A test statistic is not required, but if one is given it should be roughly chi-square ~253 or a p-value far below 0.001.
FAIL if report.md does not mention the unequal split, or mentions it only in passing (e.g. "slightly fewer users in B") while still treating the B lift as a valid result.
