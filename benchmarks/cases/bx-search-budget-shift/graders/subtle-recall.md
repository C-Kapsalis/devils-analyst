---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key (numbers computed from the files):

1. Grinders & Accessories loses money despite the best ROAS. Q3 ROAS 5.98x, but the grinders/accessories margin is 14%, so break-even ROAS is 7.14x; gross profit after ad cost is about €-1,639. Found if report.md says this campaign is below break-even / unprofitable once margin is applied (POAS or break-even ROAS).
2. Espresso Machines is profitable and budget-limited. ROAS 4.56x vs break-even 3.12x (profit about €10,631), and it loses about 47% of impression share to budget. Found if report.md says it is held back by budget and is profitable / should get more budget.
3. Grinders is rank-limited, not budget-limited: about 35% impression share lost to rank vs 4% to budget, so more budget buys little. Found if report.md notes the lost-to-rank vs lost-to-budget split for Grinders (or that added budget would not be spent productively there).
4. Quality Score average is misleading. The agency's 7.6 is a simple mean of keyword rows; impression-weighted QS is 5.9. The flagship keyword "espresso machine" (143,767 impressions, the largest) has QS 3 with a below-average landing page experience. Found if report.md flags the flagship keyword's low QS / below-average landing page OR recomputes a weighted QS near 5.9 (within 0.4).
5. Search-term waste understated. Zero-sale terms cost €2,336; the agency divides by all generic spend (€37,695) to get 6.2%, but the search-terms report only shows €20,273 (54% of spend). Within visible terms waste is 11.5%; the hidden part is unknown. Found if report.md says the search-terms report covers only part of spend (sample) or that waste is about 12% of visible spend, not 6.2%.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with its substance (a number or the specific element). A vague "review margins" or "check Quality Score" without the specific evidence does not count.
FAIL if fewer than 3.
