---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

PASS if report.md reports device-level conversion rates for both pages for at least mobile and desktop, each within 0.3 percentage points of: mobile /lp-a 1.52%, /lp-b 1.10%; desktop /lp-a 6.26%, /lp-b 5.05%.
FAIL if device-level rates are missing for either page or any of these four is off by more than 0.3 percentage points.
