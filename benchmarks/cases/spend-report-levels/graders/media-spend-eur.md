---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth Q3 2026 paid media spend in EUR (one report_level only, media platforms only, Google cost_micros / 1,000,000, Meta GBP converted at the monthly fx_rates.csv rate):
- By platform: google_ads 51,867.90, meta_ads 28,692.89, microsoft_ads 3,962.11
- Total: 84,522.90 EUR
(Meta native spend was 24,480.85 GBP.)
Common wrong totals:
- Summing every row across account + campaign + ad_group levels (and fees, no FX): 258,632.58
- Summing only the `spend` column (dropping Google, which is in cost_micros) across all levels: 103,028.88
- Right level but including manual_expenses (agency fee, contractor): 102,222.90
- Right level but leaving Meta in GBP: 80,310.86

PASS if report.md gives total Q3 paid media spend within 1.5% of 84,522.90 EUR AND per-platform figures within 2% of the values above.
FAIL if the total is near any of the wrong totals, or if Google spend is shown in micros (billions) or omitted.
