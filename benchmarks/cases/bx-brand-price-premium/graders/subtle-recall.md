---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The board page has 4 planted problems. Answer key (computed from the data files):

1. Market share without its denominator. "#1 brand, 24% market share" is Larchwood's share of KG in the online_specialty channel in the 3 regions it serves (North, East, Central). Across all regions and channels Larchwood has 1.8% of revenue (1.1% of kg); in the served online channel its revenue share is 25.4%. Found if report.md says the 24% is a served-market / one-channel / unit share and gives or describes the much smaller national or all-channel share (anything under 8%), or demands the denominator be labelled.
2. Price premium uses list price. The +23% compares Larchwood's LIST price (EUR 38.00/kg) with the category's average PAID price (EUR 30.93/kg, served online specialty). Larchwood's average paid price in H1 2026 was EUR 33.05/kg (d2c_orders_by_quarter.csv: paid revenue / kg), a premium of 6.8% over the category (or 9.2% over competitors only). Found if report.md says the premium is list vs paid and gives a paid premium in the 3-11% range or the paid price around EUR 33-34/kg.
3. Promo dependence. Revenue from discounted orders rose from 23% (2024-Q4) to 47% (2026-Q3) of D2C revenue, above the ~40% level where customers are trained to wait for deals. Found if report.md computes or describes the rising discounted share (any figure from 40-50% for recent quarters, or the trend).
4. NPS up but full-price loyalty down. NPS rose 31 -> 38, and the slide's 90-day reorder rate "holds" (41.5% -> 42.0%), but 90-day full-price reorder fell every cohort from 34.0% (2025-Q1) to 25.5% (2026-Q2). Found if report.md points out the full-price repeat decline (or that repeat is increasingly discount-driven) as contradicting the loyalty story.

List which were found in your reasoning, with evidence.
PASS if at least 3 of the 4 are identified with evidence (a number, a column, a file). Vague remarks ("check the share definition") without the substance do not count.
FAIL if 2 or fewer.
