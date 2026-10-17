---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Impression share facts (campaign-level columns, identical on every row of a campaign):
- Large generic campaigns (Generic - Hiking Boots, Generic - Rain Jackets, Generic - Tents) lose about 57.8% of impression share to RANK and only about 3.2% to BUDGET. More budget will not buy them more impressions; their limit is Ad Rank (quality score, ad relevance, landing page, bids), and they are unprofitable anyway.
- Generic - Trail Socks is the only budget-limited campaign: lost 42.0% to budget, CPA 12.76 (below break-even 36.00), but it is small (cost 370.18).
- Brand already has 94.0% impression share; extra budget there buys almost nothing.

PASS if report.md says extra budget should go only (or mainly) to Generic - Trail Socks because it is the one budget-limited, profitable campaign, AND says the other generic campaigns are limited by rank (not budget) so they need quality/relevance/bid/efficiency fixes rather than more budget.
FAIL if it recommends adding budget to Hiking Boots, Rain Jackets, Tents or Brand, or recommends a broad/account-wide budget increase, or does not use the lost-impression-share split at all.
