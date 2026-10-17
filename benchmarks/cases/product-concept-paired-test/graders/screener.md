---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: 30 of 180 respondents answered "No" to the screener q1_owns_bike_commutes and are outside the target; they must be excluded.
- Qualified (n=150): A mean 3.48, top-two-box 50.7%, top-box 21.3%; B mean 3.33, top-two-box 44.0%, top-box 12.7%; C mean 2.87, top-two-box 25.3%, top-box 8.7%.
- All 180 rows (wrong): A mean 3.32, B mean 3.52 (B top-two-box 53%): B appears to win only because of the screener fails.

PASS if report.md excludes the "No" screener respondents and reports A as the highest-scoring concept among qualified respondents (A about 3.48 vs B about 3.33, within 0.05).
FAIL if B is named the leading concept, or all 180 rows are used for the comparison.
