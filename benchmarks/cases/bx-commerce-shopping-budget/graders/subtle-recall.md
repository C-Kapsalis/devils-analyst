---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth by product type, Q3 (computed from the files; pick/pack £2.40 per order, £6 per return):
- Kitchen: reported ROAS 2.96, ROAS on revenue ex VAT/delivery 2.34, margin 59%, return rate 5%, contribution after ad spend £3,663 (+0.24 per £1 of spend)
- Lighting: reported ROAS 3.74, ROAS on revenue ex VAT/delivery 2.96, margin 43%, return rate 10%, contribution after ad spend £705 (+0.04 per £1 of spend)
- Bedding: reported ROAS 4.04, ROAS on revenue ex VAT/delivery 3.22, margin 49%, return rate 26%, contribution after ad spend £352 (+0.02 per £1 of spend)
- Small Appliances: reported ROAS 4.50, ROAS on revenue ex VAT/delivery 3.61, margin 33%, return rate 8%, contribution after ad spend £45 (+0.00 per £1 of spend)
- Phone & Tech Accessories: reported ROAS 6.24, ROAS on revenue ex VAT/delivery 4.56, margin 25%, return rate 4%, contribution after ad spend -£2,774 (-0.33 per £1 of spend)

The data contains 5 planted problems:
1. Ranking on ROAS ignores margin. Accessories have the highest reported ROAS (6.24) but ~25% margin; Kitchen has the lowest ROAS (2.96) but ~59% margin and the best contribution per £ of spend. Found if the report ranks or judges product types on margin/profit (POAS, break-even ROAS, contribution) and shows accessories are weak or loss-making despite top ROAS.
2. Conversion value includes VAT and delivery. conversion_actions.csv says the Purchase value is "order total incl. VAT and delivery", while catalogue prices are ex VAT: reported revenue is about 27% higher than revenue ex VAT/delivery. Found if the report notes the VAT (and/or delivery) inclusion and adjusts or flags ROAS as overstated.
3. Returns differ by product type. Bedding returns ~26% vs accessories ~4%, so bedding's ROAS (4.04) overstates its profit (contribution +0.02 per £ vs Kitchen +0.24). Found if the report uses return_rate_90d to discount revenue or profit, naming bedding's high return rate.
4. Thin sample. LED strip 5m: ROAS 14.2 from 3 conversions and 64 clicks; the draft plan wants to scale it. Found if the report says this is too few conversions to act on.
5. Stock cover. The most profitable SKU, Floor lamp arc, has 25 units on hand vs ~23 sold per week (about one week of cover). Found if the report flags the low stock of this SKU before adding budget to it.

In your reasoning list which of the 5 the report identifies with evidence (a number, a column or a quote).
PASS if at least 3 of the 5 are identified with evidence. FAIL otherwise.
