---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (1–14 Sep with brand ads on vs 15–28 Sep with brand ads off):
- Brand campaign cost in the 14 days it ran: 2,384.81; Google-reported conversion value 29,321.87, platform ROAS 12.3x (this is the naive answer; it is not incremental).
- Organic brand clicks rose from 20,970 to 33,264 while paid brand clicks (14,030) disappeared: organic recaptured about 84% of the paid brand clicks.
- Non-brand organic clicks (control) moved +1.6% between the two fortnights.
- Shop orders: 4,687 -> 4,636; revenue 177,805.33 -> 176,385.79.
- Incremental revenue from brand ads over 14 days: 4,232.13 trend-adjusted (pre revenue x non-brand ratio minus pause revenue), or 1,419.54 as a simple before/after difference. Incremental ROAS = 1.77x (adjusted) or 0.60x (simple). Incremental orders about 125 (adjusted) or 51 (simple).

PASS if report.md estimates the incremental value of brand ads from the pause comparison (shop orders/revenue before vs during the pause, optionally trend-adjusted) and arrives at an incremental ROAS roughly between 0.2x and 2.2x, or equivalent incremental revenue between 0.00 and 5,732.13, for 2,384.81 of cost.
FAIL if it evaluates the campaign on the platform ROAS of about 12.3x (or on Google-reported conversions/value) as its main evidence, or does not quantify incrementality from the pause.
