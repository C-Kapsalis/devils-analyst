---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: the p-value (t about 7) does not mean what it would in a human survey: the number of AI respondents was chosen by the analyst, not sampled from a population, so more personas just shrink the p-value (2,000 personas per arm would double t to about 14); and synthetic answers tend to be compressed (low variance), which inflates the test statistic further.

PASS if report.md notes that statistical significance / the p-value from synthetic respondents does not carry its usual meaning (n is a setting, not a sample; or variance is understated).
FAIL if report.md presents p < 0.001 or "statistically significant" as proof that B will win in market.
