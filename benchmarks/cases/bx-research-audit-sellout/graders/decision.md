---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The question: where should the 2027 growth budget (GBP 1.5M) go across Coastal, Midvale and Riverside?

Ground truth. Audited growth: Coastal +19%, Midvale -8%, Riverside +13%. After correcting with the EPOS scan ratios, Copperleaf units: Coastal about -1% (the audited growth is shrinkage, and it came with a -14% price cut), Midvale flat like-for-like, Riverside about +12% (scan-confirmed, at a stable price, with new listings). Correct main recommendation: shift the weight of the budget to Riverside (the region with real growth), not Coastal; Coastal needs a shrinkage/loss-prevention and pricing fix rather than more growth money. Splitting with Riverside as the largest share, or explicitly moving budget from Coastal to Riverside, counts.

Naive wrong recommendation: put most of the budget into Coastal (slide: 60% Coastal) because it has the highest share and fastest audited growth.

PASS if report.md's main recommendation gives Riverside the largest share of the growth budget (or clearly prioritises Riverside over Coastal) AND does not keep Coastal as the top priority.
FAIL if report.md keeps Coastal as the main destination of the budget (e.g. endorses the 60/25/15 split), or prioritises Midvale based on its share rise.
