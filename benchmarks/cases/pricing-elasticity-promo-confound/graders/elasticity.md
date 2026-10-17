---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: regressing ln(units) on ln(avg_selling_price) WITH a promo-week indicator (promo weeks come from campaign_calendar.csv, type = promo; 25 of 104 weeks) gives an own-price elasticity of about 1.93. Using only non-promo weeks gives 1.96. Promo weeks combine a 20-25% lower price with an email and homepage banner, so price and promotion attention move together.

Naive answer: regressing units on price alone (ignoring the calendar) gives elasticity about 4.20 ("highly elastic"). Any price-only arc/point estimate that mixes promo and non-promo weeks lands well above 3.

PASS if report.md separates or controls for promo weeks (dummy variable, excluding promo weeks, or comparing only regular-price weeks across the $38-$42 price levels) AND reports an elasticity magnitude between 1.5 and 2.5 as the regular-price elasticity.
FAIL if report.md reports an elasticity above 3 (e.g. ~4.2) as the price elasticity, or never uses the campaign calendar / promo weeks in the estimate.
