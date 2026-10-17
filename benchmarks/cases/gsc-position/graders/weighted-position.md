---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (impression-weighted average position, and CTR = total clicks / total impressions):
- /coffee-subscription: position about 2.98, CTR about 5.49%
- /brewing-guide: position about 8.09, CTR about 2.26%
Wrong answer: a simple average of the position column (about 39.5 and 34.2).

PASS if report.md reports average positions within 0.3 of the ground truth for both pages (impression-weighted) and CTRs within 0.3 percentage points.
FAIL if it reports the simple averages (around 39.5 / 34.2) as the average position, or the values are otherwise outside tolerance.
