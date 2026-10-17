---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth by fiscal year:
- FY24: 5 promos, non-promo weeks averaged 964 units/week, promo weeks 1718, lift +78%, total units 53,910, revenue $2,588,112, contribution $1,240,362, promo share of revenue 12%
- FY25: 9 promos, non-promo weeks averaged 863 units/week, promo weeks 1707, lift +98%, total units 52,466, revenue $2,431,250, contribution $1,119,600, promo share of revenue 24%
- FY26: 12 promos, non-promo weeks averaged 743 units/week, promo weeks 1718, lift +131%, total units 50,318, revenue $2,258,200, contribution $1,000,250, promo share of revenue 34%

Promo weeks sell about the same (~1,720 units) every year. The "lift" rises from 78% to 131% only because the non-promo baseline fell by 23% (964 -> 743 units/week) as promotions became more frequent: customers wait for the sale.

Naive answer: "lift grew from 78% to 131% (the last sale was the best ever), promotions are working better each year".

PASS if report.md shows non-promo (baseline) weekly units falling by roughly 18-30% from FY24 to FY26 AND attributes the rising lift to the falling baseline (not to better promotions).
FAIL if report.md presents the rising lift as improving promotion performance, or does not look at non-promo weeks over time.
