---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth CLV: average monthly price of active subscribers $49.70 x 70% gross margin = $34.79 gross profit per month; with 6.4% monthly churn and a 10%/yr discount rate (0.80%/month), CLV = 34.79 / (0.0644 + 0.0080) = $481. Undiscounted margin CLV would be $540.

Wrong answers: revenue-based LTV with the naive churn, $50 / 0.028 = $1,772; margin-based with naive churn $1,241; revenue-based (no margin) with correct churn $772.

PASS if report.md's headline CLV is margin-based and between $409 and $583.
FAIL if the headline CLV is revenue-based (no 70% margin applied) or above $583 (e.g. $1,772, $1,241 or $772).
