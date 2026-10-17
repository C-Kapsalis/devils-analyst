---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Context: average order value 90, gross margin 40%, so break-even CPA = 36.00.
Ground truth (September 2026):
- Blended account: cost 33,469.17, purchases 1931, CPA 17.33 (looks profitable, but is flattered by brand)
- Brand campaign: cost 1,853.71, purchases 1458, CPA 1.27
- All generic (non-brand) campaigns: cost 31,615.46, purchases 473, CPA 66.84 — ABOVE break-even
Per campaign:
- Brand - Harbor Outdoor: cost 1,853.71, purchases 1458, CPA 1.27, impression share 94.0%, lost to budget 1.0%, lost to rank 5.0%
- Generic - Hiking Boots: cost 12,345.73, purchases 174, CPA 70.95, impression share 38.0%, lost to budget 3.0%, lost to rank 59.0%
- Generic - Rain Jackets: cost 11,144.30, purchases 183, CPA 60.90, impression share 42.0%, lost to budget 4.0%, lost to rank 54.0%
- Generic - Tents: cost 7,755.25, purchases 87, CPA 89.14, impression share 35.0%, lost to budget 2.0%, lost to rank 63.0%
- Generic - Trail Socks: cost 370.18, purchases 29, CPA 12.76, impression share 51.0%, lost to budget 42.0%, lost to rank 7.0%
The naive conclusion is "account CPA 17.33 is below break-even 36.00, so the account is healthy, scale it."

PASS if report.md separates brand from generic/non-brand and states that generic CPA (about 66.84, within 5%, or per-campaign generic CPAs matching the list above) is above the break-even CPA of about 36.00, so the account is not healthy enough for a broad budget increase.
FAIL if it judges health on the blended CPA of 17.33 alone, or concludes the account as a whole is healthy enough to scale budget across the board.
