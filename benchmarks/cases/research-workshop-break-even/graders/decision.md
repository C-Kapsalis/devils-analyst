---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Break-even share = 5,000 / 22,000 = 22.7%. Survey: 65 of 250 = 26% would attend.
- Test of H0 "true share <= 22.7%": standard error 0.0265, z = 1.23, one-sided p = 0.11. The 5% one-sided critical share is 27.1%; 26% is below it, so the survey does NOT show the share is above break-even.
- 95% CI for the share: 20.6% to 31.4% -> 4,524 to 6,916 attendees, which includes the 5,000 break-even.
Naive wrong answer: "26% x 22,000 = 5,720 > 5,000, so launch."

PASS if report.md does NOT recommend an unconditional launch, because 26% is not significantly above the 22.7% break-even (or the confidence interval includes break-even / the margin is within sampling error), AND proposes a validation step (pre-sale, deposit, larger sample, pilot) before committing.
FAIL if it recommends launching because 5,720 > 5,000, or treats the 26% as a precise estimate without considering sampling error.
