---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The data contains 6 planted problems. Answer key (all numbers computed from the files):

1. Margin vs markup. The brief says "60% margin", but cost_of_goods_sold / gross_sales = 62.5% in the Shopify export, so gross margin is 37.5% (60% is the markup on cost). After fulfilment and card fees, contribution is about 22% of net sales on a normal day, and the break-even lift for 25% off is impossible instead of 71%. Found if the report says the 60% is not the real margin (cites the COGS ratio, a margin of 35-40%, or the markup conversion).
2. Depressed baseline before the sale. The 17 Nov early-access email announced the sale; orders from 17 to 27 Nov ran about 25% below the 13 Oct - 16 Nov level, so comparing with "the week before" overstates the lift. Found if the report says the week before was depressed by the announcement (people waiting) and uses an earlier baseline.
3. Post-promo dip. Orders in the 14 days after Cyber Monday ran about 22% below the pre-announcement baseline (about 1,286 orders short over 2-21 Dec): supplements are replenished, so purchases were pulled forward. Found if the report identifies the December dip and nets it out (or says the window must include it).
4. Higher returns on promo orders. returns / net_sales on 28 Nov - 1 Dec = 15.3% vs 6.0% on normal days. Found if the report notes promo-day returns are about double/much higher and deducts them.
5. Subsidy. 70% of promo-day orders came from returning customers; roughly 1,505 of the 3,583 promo orders (baseline volume) would have happened anyway, receiving about $31,961 of discount. Found if the report says most discounted orders went to existing/returning customers or quantifies discount given on orders that would have happened anyway.
6. Promo-acquired customers repeat less. new_customer_cohorts_2025.csv: BFCM cohort 90-day repeat 7.1% vs about 18.9% for non-promo cohorts, so the recap's "new customers will pay back" ($210 lifetime value) is not supported. Found if the report flags the lower repeat rate of BFCM-acquired customers.

In your reasoning, list which of the 6 the report identifies with evidence (a number, a column or a quote).
PASS if at least 4 of the 6 are identified with evidence. FAIL otherwise. Vague mentions ("consider returns", "watch pull-forward") without tying them to the data do not count.
