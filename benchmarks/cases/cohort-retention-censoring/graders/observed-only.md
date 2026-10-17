---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The export is a full grid: offsets a cohort has not reached yet by 1 Oct 2026 are filled with active_subscribers = 0. Those zeros are not churn and must be excluded. Month-3 retention is observed only for the Jan-Jun 2026 cohorts; month-6 only for Jan-Mar 2026.

Ground truth (observed cohorts only):
- Month-3 retention: 52.5% weighted by cohort size (52.0% simple average of cohorts).
- Month-6 retention: 34.9% weighted by cohort size (34.8% simple average of cohorts).

Naive answers (zeros for unreached months included): month-3 34.7% (size-weighted 29.6%), month-6 11.6% (size-weighted 8.3%).

PASS if report.md's month-3 figure is within 2 percentage points of 52.5% or 52.0% AND its month-6 figure is within 2 percentage points of 34.9% or 34.8%.
FAIL if either figure is missing, or is near the naive values (34.7% / 11.6% or 29.6% / 8.3%), or report.md treats the 0 rows for recent cohorts as subscribers who churned.
