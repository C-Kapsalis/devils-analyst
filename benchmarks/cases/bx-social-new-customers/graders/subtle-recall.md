---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files; EUR at 1 USD = 0.92 EUR):

1. ASC buys returning customers. "ASC - All Products" has no existing-customer budget cap and only 30% of its Shopify orders are from new customers. Cost per new customer: ASC €66, Meta Prospecting €46, TikTok Prospecting €41. Found if report.md uses new-customer orders (or the missing existing-customer cap) and shows ASC is expensive per new customer.
2. Currency mismatch. TikTok spend and values are in USD; Meta in EUR. TikTok Prospecting cost per purchase is $33.12 = €30.47; the agency compared $33.12 directly with Meta's €15.49. Found if report.md notes the USD/EUR difference and converts.
3. Engagement rates on different denominators. TikTok's 7.6% is engagements per 6-second video view; Meta's 1.33% is engagements per reach. Per impression they are 0.96% (TikTok) and 0.46% (Meta). Found if report.md says the two rates use different denominators and are not comparable (a per-impression recomputation is a bonus).
4. Creator picked on a tiny sample. @outfitsbyjo ran 3 days with 11 purchases (26.60 USD per purchase); the others ran ~28-30 days with 88-118 purchases. Found if report.md says @outfitsbyjo's result is too small a sample to back with the largest budget.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
