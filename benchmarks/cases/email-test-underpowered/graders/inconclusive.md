---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (orders / delivered): A 60/2000 = 3.00%, B 72/2000 = 3.60%, relative lift +20%. Two-proportion z-test: z = 1.06, p = 0.29. 95% CI for the difference in order rate: -0.51 to +1.71 percentage points (includes zero). Clicks are also not significantly different (z = 0.50, p = 0.62). The test is inconclusive: there is no reliable evidence that B beats A.

Naive answer: "B wins with 20% more orders" with no uncertainty check.

PASS if report.md states that the difference between A and B is not statistically significant / could be noise / the test is inconclusive or underpowered (any of these is acceptable, with or without a p-value; if a p-value is given it should be roughly 0.2-0.4).
FAIL if report.md declares B the winner on the strength of the 20% lift without saying the result is inconclusive, or claims the result is significant.
