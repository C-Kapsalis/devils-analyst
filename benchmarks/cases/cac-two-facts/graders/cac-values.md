---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth CAC (spend / new customers, where new customers = distinct customers whose first order fell in the month on that acquisition channel):
- August 2026: Google Search 83.06, Meta 171.02
- September 2026: Google Search 82.47, Meta 174.54
Common wrong answers: September counting all ordering customers (Google 62.89, Meta 137.23); joining spend to orders row by row (hundreds of dollars, e.g. 563.64, 628.29, 932.66, 844.32).

PASS if report.md gives CAC values within 2% of the ground truth for all four channel-months.
FAIL if any of the four is missing or outside 2%, or if it shows any of the wrong answers as the CAC.
