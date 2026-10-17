---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key (computed from the files):

1. Not a randomised split. Both ads sat in one ad set, so Meta's delivery chose who saw what and gave UGC 81% of spend. Found if report.md says the set-up (ads in one ad set / uneven delivery) is not a valid A/B test.
2. Different dates and a sale. UGC started 1 September, studio 9 September; only UGC ran during the 5-8 September sale, which produced 35% of UGC's 1-day-click purchases. Found if report.md flags the different start dates and/or the sale days favouring UGC.
3. Winner picked on all-clicks CTR. CTR (all) 3.07% vs 1.75%, but link CTR is 1.34% vs 1.32% (about equal). Found if report.md says CTR should use link clicks and they are about the same.
4. View-through inflates UGC's ROAS. 62% of UGC's purchases are view-through (purchases vs purchases_1d_click) vs 21% for the studio ad. Found if report.md compares on 1-day click (or flags the view-through share).
5. Not significant on a fair comparison. On 9-28 September (both live, no sale), 1-day-click purchases per 1,000 impressions are 0.24 (UGC, 59 purchases) vs 0.28 (studio, 22 purchases); two-proportion test p = 0.47. Found if report.md says the difference on a like-for-like window is small / not statistically significant / inconclusive.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 with the specific evidence.
FAIL if fewer than 3.
