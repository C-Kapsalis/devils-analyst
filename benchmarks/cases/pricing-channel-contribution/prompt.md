---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Tidepool Bottles sells one product, a $34 insulated water bottle, in three channels: our Shopify store, Amazon FBA, and wholesale to outdoor retailers (who sell it at our $34 list price). resources/ has channel_sales_sept.csv (channel, units, orders, revenue, returns, ad_spend), amazon_settlement_sept.csv and shopify_payouts_sept.csv for September 2026.

Wholesale price is $17 per unit, retailers get a 4% co-op allowance, and freight is $0.80 per unit. Shopify orders cost us $6.50 each to ship. Landed cost is $9 per bottle, and returned bottles are refunded and written off.

Amazon is now our biggest channel. Where should we put our 2027 growth money? Write report.md with the numbers by channel and your recommendation.

Save report.md in the current working directory, not inside resources/.
