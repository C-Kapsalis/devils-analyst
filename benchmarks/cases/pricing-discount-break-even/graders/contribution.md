---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (contribution = gross_revenue - discount_amount - 52% x gross_revenue - $7 x orders): baseline days outside the promo averaged $7,095 contribution/day; promo week averaged $4,787/day, so the promotion cost about $16,153 of contribution over the week (using only the pre-promo days as baseline: $16,532). $33,622 of discounts were given, mostly on orders that would have happened anyway: only about 713 of 2,805 promo-week orders were incremental.

Naive answers: "orders up 34%", "net revenue up 10%", or counting code redemptions, and calling the promo a success.

PASS if report.md concludes the promo REDUCED contribution / profit versus a normal week, with a weekly figure roughly between -$24,229 and -$8,884, OR a clearly reasoned negative profit impact that accounts for the discount given on baseline (would-have-bought-anyway) orders.
FAIL if report.md calls the promo profitable or judges it on revenue, orders or redemptions only.
