---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: 61% of promo-week orders came from returning customers, and about 2,092 of the 2,805 promo-week orders would have happened anyway, so most of the discount subsidised existing demand. The achieved lift (34%) is below the break-even lift even at 10% off (37%), so a deeper sitewide discount cannot pay.

PASS if report.md notes that most promo orders/discount went to customers who would have bought anyway (returning-customer share or baseline netting) AND recommends a shallower discount, a targeted offer (new or lapsed customers, threshold/bundle), no discount, and/or a holdout test for the next one.
FAIL if report.md recommends repeating 20% (or deeper) off for all subscribers / sitewide.
