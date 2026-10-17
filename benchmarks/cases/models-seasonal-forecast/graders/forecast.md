---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: January is the seasonal low (index about 0.68, roughly 30% below an average month). Trend level for January 2027 x January seasonal index gives about $97,132. Anything from $85,000 to $115,000 with a seasonal method (or e.g. January 2026 $85,920 grown by about 12%) is correct.
Naive wrong forecasts: 3-month moving average of Oct-Dec 2026 = $189,702; 12-month moving average of 2026 without putting January's dip back = $135,797; December x 1.4 = $343,662.

PASS if the January 2027 revenue plan in report.md is between $85,000 and $115,000.
FAIL if it is above $125,000 or below $75,000, or no single January number is given.
