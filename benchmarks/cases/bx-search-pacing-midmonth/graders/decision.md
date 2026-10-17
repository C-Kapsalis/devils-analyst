---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Correct main recommendation: shift budget from Generic - Apparel (projected about 120% of plan at the current rate, CPA about €70 vs €45) to Generic - Running Shoes (capped every day, CPA about €27, about 41% share lost to budget), e.g. raise the Running Shoes daily budget and lower Apparel's.

Naive wrong answers: "on track, no changes" (the agency's verdict based on the account total of 94% of plan), or spreading the apparent underspend across all campaigns, including Apparel.

PASS if report.md's main recommendation is to raise Running Shoes' budget AND fund it at least partly by cutting/reducing Apparel (or explicitly says Apparel should not get more).
FAIL if it agrees no change is needed, recommends raising budgets across the board, or raises Running Shoes while also keeping or raising Apparel's €650 budget.
