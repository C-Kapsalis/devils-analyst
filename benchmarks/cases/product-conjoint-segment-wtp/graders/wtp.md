---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: price part-worths span $10 ($19 to $29), so the exchange rate is (pw_price_19 - pw_price_29)/10. Across the sample it is about 0.159 utils per dollar. Average strap part-worth / exchange rate = average WTP for the strap of about $2.55 (mean of individual WTPs about $2.53).

PASS if report.md converts the strap part-worth into a dollar willingness to pay using the price part-worths, with an average between $2.0 and $3.2 (or reports individual WTPs consistent with it).
FAIL if no dollar WTP is computed.
