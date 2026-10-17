---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The model contains 6 planted problems. Answer key:

1. CTR averaged. `CTR = AVERAGE('Fact Ads Daily'[ctr])` averages daily row rates, so a Google day with about 3,000 impressions weighs as much as a Meta day with about 40,000. On the September sample it returns 3.77%; clicks / impressions = 20,250 / 1,268,907 = 1.60%. Fix: DIVIDE(SUM(clicks), SUM(impressions)). Counts as found if report.md says CTR must be a ratio of sums (or gives a figure within 0.1 points of 1.60%).
2. Email List Size summed. `SUM('Fact Email List Daily'[list_size])` adds a daily snapshot, so September shows 556,869 instead of the 18,699 subscribers on 30 September. Fix: closing value (LASTDATE / LASTNONBLANKVALUE). Counts as found if report.md says the snapshot must not be summed over days.
3. Revenue toggle default. `SELECTEDVALUE('Revenue Basis'[Basis], "Gross")` makes every page without a slicer show gross revenue (€91,066 in September) while the agreed definition is net (€67,162), 36% higher. Fix: default to "Net". Counts as found if report.md says the default (no selection) is Gross and should be Net.
4. Paid ROAS on platform claims. `Paid ROAS` divides the sum of Google's and Meta's reported conversion value (€105,959) by spend: 6.79x, while the claims exceed all net store revenue (€67,162); the agreed ROAS is net store revenue / spend = 4.30x (the existing Store ROAS measure). Counts as found if report.md flags Paid ROAS as double-counted platform claims or contrary to the agreed ROAS.
5. Two CACs. `CAC (Exec)`, used on the Executive page, counts reactivated customers as new: €26 vs the agreed CAC €38 (412 new customers vs 608). Counts as found if report.md flags the two CAC definitions or the reactivated customers in CAC (Exec).
6. Monthly Users summed. `SUM('Fact GA4 Daily'[active_users])` adds daily users: 62,987 for September vs GA4's monthly 36,532. Counts as found if report.md says users cannot be summed across days.

List which ones were found in your reasoning.
PASS if report.md identifies at least 5 of the 6 problems, each with its substance (a vague mention such as "review your measures" does not count).
FAIL if it identifies fewer than 5.
