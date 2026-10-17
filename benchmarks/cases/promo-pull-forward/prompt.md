---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

The resources/ directory has our Shopify daily sales export for Lumen Home Goods, daily_orders.csv (date, orders, gross_revenue, discount_amount; gross_revenue is before discounts), and our promotions calendar, promo_calendar.csv. Our average cost per order (product cost plus pick, pack and shipping) is $30.

How did the Spring Sale perform? Should we run it again next quarter? Write report.md with the numbers and your recommendation.

Save report.md in the current working directory, not inside resources/.
