---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: retention is improving for newer cohorts. Month-3 retention by cohort: 2026-01 48.1%, 2026-02 48.9%, 2026-03 50.8%, 2026-04 52.4%, 2026-05 55.3%, 2026-06 56.5%. Month-6: 2026-01 33.0%, 2026-02 34.7%, 2026-03 36.8%. Month-1: 2026-01 62.6%, 2026-02 62.3%, 2026-03 64.2%, 2026-04 65.5%, 2026-05 65.9%, 2026-06 67.1%, 2026-07 70.2%, 2026-08 70.9%.

Naive answer: "retention is getting worse", because recent cohorts show 0 at month 3/6 (they have not reached those months yet), so the per-cohort line drops to zero.

PASS if report.md concludes retention is improving / newer cohorts retain better, based on comparing cohorts at the same month offset.
FAIL if report.md says retention is getting worse or declining, or cites 0% retention for Jul-Sep 2026 cohorts as evidence.
