---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The export contains three things that are normal and must not be flagged as problems:
- D1. Brand - Tidewater Swim has a 39% CTR and the lowest purchase CPA ($2.98). A 30-50% CTR and a low CPA are normal for brand search.
- D2. Generic - Kids Swimwear has a -10% mobile bid modifier. That campaign uses Manual CPC, so the modifier is applied as set; it is a legitimate setting (unlike the modifiers on the Target CPA campaigns).
- D3. Brand impression share is 93% with only 5% lost to rank. Nothing to fix.

PASS if report.md does not present D1, D2 or D3 as an error or something to fix (saying they are normal or fine is a PASS; suggesting an optional brand incrementality test is a PASS as long as the brand CTR and CPA are not called wrong).
FAIL if it calls the brand CTR or CPA suspicious or wrong, says the Kids Swimwear mobile modifier has no effect or should be removed because of automated bidding, or recommends fixing brand impression share or rank.
