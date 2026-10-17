---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: every respondent rated all three concepts (within-subject design), so A vs B must be tested with a paired test on each respondent's difference.
- Paired t-test (qualified, n=150): mean difference 0.147, t = 2.38, p about 0.017: A is significantly ahead of B.
- Independent two-sample test on the same columns (wrong test): t = 1.21, p about 0.23, which wrongly suggests "no difference".

PASS if report.md compares A and B with a paired / within-respondent test and reports the difference as significant (p below 0.05, about 0.017), or otherwise explains that the same respondents rated all concepts and treats the difference as significant.
FAIL if it calls A and B statistically tied / indistinguishable, or bases the comparison on an independent-samples test.
