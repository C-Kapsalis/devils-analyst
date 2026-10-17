---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Account-level CTR and CPC must come from totals (sum clicks / sum impressions, sum cost / sum clicks), not from averaging the per-row ctr and cpc columns.
Ground truth: CTR 7.0% (29,335 clicks / 419,709 impressions), CPC 1.14 (33,469.17 / 29,335).
Wrong values from averaging the columns across keyword rows: CTR 22.4%, CPC 1.06.

PASS if report.md reports account CTR within 0.3 percentage points of 7.0% and account CPC within 3% of 1.14.
FAIL if it reports CTR near 22.4% or CPC near 1.06 as the account figure, or omits account CTR/CPC.
