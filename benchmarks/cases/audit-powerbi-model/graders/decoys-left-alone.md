---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three measures are correct and must not be flagged:
- D1. `Conversion Rate = DIVIDE(SUM(conversions), SUM(sessions))`: a ratio of sums (2.39% on the sample).
- D2. `Share of Spend` uses REMOVEFILTERS on channel in the denominator and its description says it is the share within all paid channels (Google Ads 35.9% of spend). That is the intended share-of-total pattern.
- D3. `Store ROAS = DIVIDE([Net Revenue], [Total Spend])` matches the agreed ROAS definition (4.30x).

PASS if report.md does not present D1, D2 or D3 as an error or something to change. Mentioning them as correct, or recommending Store ROAS as the replacement for Paid ROAS, is a PASS.
FAIL if it says any of D1, D2 or D3 is wrong or needs a different formula.
