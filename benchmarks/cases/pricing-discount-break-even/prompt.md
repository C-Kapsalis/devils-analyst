---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

resources/daily_sales.csv is the Shopify export for Northwind Coffee's online store (date, new_customer_orders, returning_customer_orders, gross_revenue, discount_amount; gross revenue is before discounts). From 14 to 20 September we ran 20% off everything for our email subscribers (code VIP20). Product cost is 52% of full price and pick, pack and ship is $7 per order.

Was it worth it, and what discount should we use for the next one? Write report.md with the numbers and your recommendation.

Save report.md in the current working directory, not inside resources/.
