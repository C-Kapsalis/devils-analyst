---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The readout and its exports contain 5 planted problems. Ground truth (computed from the files):

1. Shipping cost not counted (decision-changing). In B the company pays the $6.80 carrier cost and collects no $5.95 fee. Contribution per order: A $32.01 (= 48% x $68.46 + 5.95 - 6.80), B $24.08 (= 48% x $64.33 - 6.80). Contribution per user: A $1.180, B $0.951, a change of -19.4%. Orders per user would have to rise about 33% to break even; they rose 7.1%. Counts as found if report.md says free shipping loses money / lowers contribution or profit per user once shipping cost (or the lost shipping fee) and margin are counted, with a number (a contribution or profit figure, a break-even lift of roughly 25-40%, or a money loss).
2. Order value fell. AOV A $68 vs B $64 (-6.0%); merchandise revenue per user A $2.523 vs B $2.540 (0.7%), not a meaningful gain. The readout's $88,458 a month projection uses control AOV. Counts as found if report.md says B's average order value is lower, or revenue per user is about flat, so the revenue projection is overstated.
3. More than one change. B also added an express checkout (one-tap wallet) button on the cart page and a header bar. Counts as found if report.md says the lift cannot be attributed to free shipping alone because the express checkout (or other changes) were bundled in.
4. Wrong balance variables. In balance_check.csv, cart_adds_per_user and pages_per_session are measured "during test": they are outcomes the treatment can change, not evidence of imbalance. The pre-exposure variables (orders_prior_365d, sessions_prior_30d, share_mobile, share_new_visitor) all have p > 0.3. Counts as found if report.md says those two variables are post-exposure/outcome measures so they do not show a randomisation problem (and the 2.5-point discount is unjustified).
5. Session-level assignment. Assignment unit is session_id and 8.4% of users were in both arms (saw both $5.95 and free shipping), counted in both. Counts as found if report.md flags session-level assignment or the users in both arms as contamination/a unit-of-analysis problem.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 5, each with its substance (a number, column or quoted setting). FAIL otherwise.
