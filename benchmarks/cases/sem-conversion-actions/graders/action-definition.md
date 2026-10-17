---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

September purchase-only figures by campaign (CPA, ROAS): Search - Brand CPA 2.65, ROAS 17.02x; Search - Generic Coffee CPA 53.60, ROAS 0.81x; Search - Espresso Machines CPA 132.43, ROAS 2.28x; Shopping - All Products CPA 25.50, ROAS 2.17x; PMax - Catalog CPA 24.90, ROAS 2.02x.
Campaigns at or above 4x on purchases: Search - Brand.

PASS if report.md explains that newsletter_signup (and/or add_to_cart / all_conversions) should not be counted as sales when judging CPA/ROAS, AND gives a recommendation consistent with purchase-only ROAS being below 4x (e.g. cut or rebid the weakest campaigns by purchase ROAS, fix bidding to optimise on purchase value only, remove the lead value from the bidding goal).
FAIL if it treats newsletter signups or add-to-carts as sales, or recommends scaling spend on the grounds that the 4x target is met.
