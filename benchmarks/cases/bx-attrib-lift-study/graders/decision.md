---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Correct main recommendation: do NOT switch to a weekday-only schedule (the weekday/weekend difference is not significant, p = 0.43) and do not double the budget on the readout's inflated numbers. Keep running on all days and add a frequency cap around the band where lift peaks (16-30 impressions per user), cutting the 51+ impressions that add nothing (32% of impressions).

Naive wrong answer: the agency's "switch to weekday-only and double the budget".

PASS if report.md's main recommendation rejects weekday-only scheduling AND recommends a frequency cap (or reallocating away from the high-frequency band) rather than doubling budget.
FAIL if it recommends weekday-only, endorses doubling the budget on the readout's POAS, or gives no clear recommendation.
