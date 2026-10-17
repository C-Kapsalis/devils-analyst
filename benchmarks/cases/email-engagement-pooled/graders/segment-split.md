---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

PASS if report.md gives separate click rates for the weekly blast and the targeted campaigns that are each within 0.5 percentage points of the ground truth: blast 0.98%, targeted segments pooled 4.99% (individual segment rates between 4% and 6% are also acceptable in place of the pooled segment figure).
FAIL if no separate rates are given, or if they are off by more than 0.5 percentage points.
