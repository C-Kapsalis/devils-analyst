---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The data contains 5 planted problems. Answer key (computed from the files):

1. Seasonality. Q3 is always weaker: in 2025, with no price change, store Better units in Q3 were 91% of Q2. The raw drop of -28% is about -21% after adjusting for that. Found if the report compares with the same quarters of 2025 (or otherwise adjusts for the seasonal Q3 dip) with a number.
2. Stock-outs. inventory_weekly.csv shows the store warehouse had Better in stock only 3 of 7 days in the week of 10 Aug and 2 of 7 in the week of 17 Aug (9 days out of stock). Adjusting for these and seasonality, the price-driven drop is about -12%. Found if the report names the stock-out days as part of the drop.
3. Amazon price not raised. Amazon Better is still $129 (list_price column; unit_economics list_price_amazon); Amazon Better units rose about +12% vs the 2025 Q2-to-Q3 pattern, so some buyers moved to Amazon, where a Better unit earns about $54 vs $81 on the store. Found if the report identifies the channel price gap / migration to Amazon.
4. Trade-down. Store Good units rose about +8% vs the 2025 pattern after the change: some Better buyers bought Good instead and were kept. Found if the report notes Good-tier gains (or judges all tiers together for that reason).
5. Margin definition. unit_economics.csv gross_margin_pct (62.8% at $129) is (price - landed cost) / price and leaves out store fulfilment ($9) and card fees (2.9%); the contribution margin at $129 after the welcome code is about 52%, so the break-even volume loss for +12.4% is about 19% (not 16%). Found if the report builds contribution from the cost lines (fulfilment and fees) rather than using gross_margin_pct as is.

In your reasoning list which of the 5 the report identifies with evidence (a number, a column or a quote).
PASS if at least 3 of the 5 are identified with evidence. FAIL otherwise.
