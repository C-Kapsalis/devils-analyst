---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: Q6 ("Would you subscribe? Yes/No") plus the plan "forecast = yes share x 180,000" will overstate subscribers badly. Stated purchase intent overstates behaviour (hypothetical money, politeness, sensitised and self-selected respondents), and a yes/no question has no gradation. Fix: use a graded purchase-likelihood scale (definitely / probably / might / probably not / definitely not) and apply calibration/deflation factors, and/or validate with a behavioural test (pre-order, waitlist with deposit, smoke test).

PASS if report.md says the Q6 yes share will overstate subscribers AND proposes deflating/calibrating it, a graded likelihood scale with calibration, or a behavioural test.
FAIL if it accepts the raw yes share as the forecast or only suggests rewording Q6.
