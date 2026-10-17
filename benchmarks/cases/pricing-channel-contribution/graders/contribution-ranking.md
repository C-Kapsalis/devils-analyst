---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (September 2026; contribution = net payout or revenue after refunds and channel fees, minus shipping/freight/co-op, minus $9 landed cost on every unit sold, minus ad spend):
- Shopify: revenue $177,038, units 5,207, contribution per unit before ads $17.41, after ads $11.46, monthly contribution $59,660
- Amazon: revenue $293,242, units 9,778, contribution per unit before ads $8.05, after ads $5.39, monthly contribution $52,688
- Wholesale: revenue $103,700, units 6,100, contribution per unit before ads $6.35, after ads $6.35, monthly contribution $38,735

Amazon is the biggest channel by revenue (51% of revenue) and has the best platform ROAS (11.3x vs Shopify 5.7x), but keeps the LEAST per unit ($5.39 after ads) because of the lower $29.99 price, 15% referral fee, FBA fees and ~9% returns. Shopify keeps about 2.1x as much per unit ($11.46).

Naive answers: ranking channels by revenue or ROAS (Amazon first).

PASS if report.md ranks or compares channels on contribution/profit after fees, returns, product cost and ads (per unit or in total), showing Shopify highest per unit and Amazon lowest (or near-lowest) per unit, with per-unit figures within about 15% of the ground truth.
FAIL if report.md ranks channels by revenue, units or ROAS, or does not deduct Amazon's fees and product cost.
