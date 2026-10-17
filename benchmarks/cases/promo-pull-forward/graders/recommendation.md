---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Correct recommendation: do not repeat the Spring Sale as designed (sitewide 20% off for a week) for the planned Summer Sale; it mostly shifted demand in time and gave away margin. Acceptable: cancel it, or redesign it (smaller discount, targeted at new/lapsed customers, a holdout test to measure incrementality) with the reasoning that the current design did not pay off.

PASS if report.md recommends against repeating the sale in its current form, or recommends only a redesigned/tested version, AND the reasoning cites the post-sale dip or the net negative contribution.
FAIL if report.md recommends running the same sale again (e.g. because orders/revenue rose 78% in the sale week).
