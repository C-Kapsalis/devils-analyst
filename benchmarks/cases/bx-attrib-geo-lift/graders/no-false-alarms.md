---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two patterns are normal and must not be presented as problems:
- D1. Control regions have lower revenue in absolute terms (pre-period €282,812 vs €317,490 in test regions). Groups of different size are fine; the comparison uses the ratio against the pre-period.
- D2. Meta reports 1,190 purchases (about €72,590) in the test regions, far more than the measured incremental revenue (about €9,737). Expected: platform attribution counts purchases that would have happened anyway; that is why the test was run.

PASS if report.md does not call the size difference between groups a flaw that invalidates the test (noting it is handled by the pre-period comparison is fine), and does not treat the Meta-reported vs incremental gap as a tracking error.
FAIL if either is presented as a problem to fix.
