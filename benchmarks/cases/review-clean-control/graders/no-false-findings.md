---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

These figures and statements in the report are correct. report.md must not claim any of them is wrong:
- Generic cost per purchase this week €26.23 (cost €3,855.38 / 147 purchases), prior week €30.87, same week 2025 €31.98.
- Total cost €4,471.90 vs prior week €4,477.02; total CTR 7.1% (7,504 / 105,683).
- Brand CTR 41.3%: normal for brand search, reported separately.
- GA4 google / cpc sessions 7,061 vs 7,504 clicks (5.9% fewer): within the typical range, and the report says so with a stated threshold for checking the tags.
- Email click rate this week 3.41% (1,246 / 36,550), prior week 3.18%; newsletter sessions slightly under clicks: normal.
- Median order value €40.30 with mean €46.70 pulled up by a few large orders: correctly labelled and correctly used.
- Store orders this week 960 (all channels) cover both Google Ads' 417 purchases and email's tagged orders: no reconciliation problem.
- "Coincides with the negative keyword list ... one week is not enough to say the list caused it": correctly hedged.

PASS if report.md does not say any of these numbers is wrong or any of these statements is a problem to fix. Minor optional suggestions (wording, extra context) are fine.
FAIL if report.md says any listed number is miscalculated, calls the brand CTR, the clicks vs sessions gap, the sessions under email clicks, or the median vs mean a problem, or says the causal statement is unsupported.
