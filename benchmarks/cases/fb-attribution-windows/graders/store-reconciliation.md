---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Reconciliation check. Store orders in September (all channels): 4,165. Meta 7-day-click purchases: 1,651 (40% of store orders). Summing all window columns gives 6,944, which is 1.7x everything the store sold, so the windows cannot be added.

PASS if report.md compares Meta's purchase count to the store order total (or otherwise explains that the window columns overlap / are nested and must not be summed).
FAIL if it neither mentions the overlap of the windows nor sanity-checks against store orders, or if it presents a Meta purchase count above 4,165 as real.
