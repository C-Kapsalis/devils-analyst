---
id: HR-001
area: ecommerce-revenue
overrides: metric-definitions/catalog:ROAS
check: Every ROAS, MER and CAC uses finance net revenue after returns, not store gross revenue or platform-reported revenue.
where_to_look: Warehouse table finance.net_revenue_daily (column net_revenue_after_returns) against Shopify orders.total_price and the ad platforms' conversion value.
red_flag: A report or dashboard divides by Shopify total_price or platform conversion value, or its revenue is more than 5% above finance.net_revenue_daily for the same days.
why_it_costs_money: Returns run about 18% of gross in this business, so gross-revenue ROAS overstates every channel by about a fifth and paid social, which drives the most returned orders, gets budget it does not earn.
fix: Recompute with finance.net_revenue_daily aggregated to the report's grain, then divide. Show the gross figure only as a labelled reconciliation line.
source: Finance policy note "Revenue of record", Q2 2026 board pack (fictional).
owner: Head of Finance Analytics (fictional)
date: 2026-10-01
---

Fictional example for Fernhill Supply Co., an outdoor apparel shop that does
not exist. It shows a rule that replaces a shipped default: the catalog's
ROAS uses the revenue a source reports; this team decided its revenue of
record is finance net revenue.
