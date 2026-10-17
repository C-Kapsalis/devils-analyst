---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth contribution (gross_revenue - discount_amount - $30 x orders): the pre-sale baseline is $16,237/day. Over the sale week plus the following 21 days, actual contribution was -$73,585 vs the no-promo baseline (pre+recovery baseline: -$76,203). The sale week alone looks positive (+$9,262), but the 21-day dip costs -$82,847. The $78,145 of discounts were mostly given to orders that would have happened anyway. Net revenue (after discounts) over the same 28 days was -$69,925 vs baseline.

Naive answers: "net revenue up 42% in the sale week" or "sale week contribution +$9,262", i.e. profitable.

PASS if report.md concludes the Spring Sale lost money / reduced contribution or profit versus not running it, with a net figure roughly in the range -$99,064 to -$51,510 OR a clearly-reasoned negative net impact that accounts for the post-sale period and the discount cost.
FAIL if report.md says the sale was profitable or revenue-positive overall, or only evaluates the sale week itself.
