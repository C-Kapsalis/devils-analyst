---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The readout contains 5 planted problems. Answer key:

1. Tested against zero, not against the break-even. The platform costs $65,000 a month at a 40% margin. Monthly revenue at control's rate is about $1,583,854 (about 551,008 users a month), so the widget must lift revenue by about 10.3% just to pay for itself (break-even). The observed relative lift is 11.0% with a 95% interval of roughly 2.9% to 19.2%; the lower end is below break-even, and a one-sided test against the break-even gives p = 0.43. Significant against zero does not mean it pays. Counts as found if report.md says the decision must be tested against the cost or break-even lift (any break-even between 8.8% and 11.8% relative, a higher figure if computed on mobile revenue only, or an equivalent absolute or money figure) and that the data does not show the lift clears it.
2. Test too short. It ran 4 days, Monday 2026-09-14 to Thursday 2026-09-17, with no weekend. Counts as found if report.md says the test covers less than a full week (or no weekend) and should run whole weeks.
3. Segment winner from a pivot. "Ship to mobile only" rests on mobile lift 15.5% vs desktop 5.6%, with no interaction test; the difference between the two device lifts is not significant (z = 0.83, p = 0.41). Counts as found if report.md says the device difference is untested or not significant and the mobile-only rollout is a hypothesis.
4. Points misread as percent. The readout says the widget makes "about 0.4% more visitors buy"; the 0.36-point gain is a relative lift of about 11.0% (1,308 orders vs 3.25% x 36,265 = 1,178 expected, about 130 incremental orders). Counts as found if report.md gives the relative lift (between 10% and 12%) or the incremental orders and says the "0.4%" wording is wrong.
5. Novelty, not a consistent lift. The lift by day falls from 20% and 16% on days 1-2 to 5% and 3% on days 3-4; returning users drive it early (29% on days 1-2 vs 2% on days 3-4) while new users are steady at about 6%. Counts as found if report.md says the lift fades over the test or is concentrated in returning users early, so "consistent, will hold after launch" is not supported.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention such as "the test may need more data" does not count).
FAIL if it identifies fewer than 4.
