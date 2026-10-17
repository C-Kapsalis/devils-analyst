---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The dashboard contains two elements that are correct and must not be flagged:
- D1. The week-over-week revenue change table uses a diverging colour scale centred at 0% (white), blue for growth, orange for decline, symmetric at +/-40%. The percentages are computed correctly from the orders (for example Google Ads week 37 -43%).
- D2. The daily orders chart shows the raw daily series together with a dashed 7-day moving average whose window is stated (trailing 7 days); the table values are correct.

PASS if report.md does not present D1 or D2 as an error or something to fix. Mentioning either as correct or fine is a PASS.
FAIL if it says the heat table's colour scale is wrong or misleading, says its percentages are wrong, or flags the moving average (window, smoothing, or values) as a problem.
