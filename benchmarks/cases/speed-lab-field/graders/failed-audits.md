---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

PASS if report.md shows awareness that some audit rows failed (is_audit_successful = false, recorded with 0 values) and excluded them, OR its numbers clearly come only from successful latest-run field rows (no 0 ms values used).
FAIL if it reports any page's LCP as 0 ms or treats 0 values as fast pages.
