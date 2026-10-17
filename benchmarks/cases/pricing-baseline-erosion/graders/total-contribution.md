---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: total contribution (units x (price - $25), with promo weeks at $37.50) fell every year: FY24 $1,240,362, FY25 $1,119,600, FY26 $1,000,250 (-19% over two years). Total units and revenue also fell (units 53,910 -> 50,318; revenue $2,588,112 -> $2,258,200) while the promo share of revenue rose from 12% to 34%.

PASS if report.md shows total contribution/profit (or total revenue/units, or contribution per week) falling as the number of promotions rose, with figures consistent with the above (within about 5%).
FAIL if report.md judges the promotions on promo-week metrics only (lift, promo-week units or revenue), or claims total sales/profit grew.
