---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The exports contain two things that are normal and must not be flagged as problems:
- D1. (not set) campaign rows total 670 sessions, 0.51% of 131,507 September sessions. A share under 1% is normal noise.
- D2. GA4 shows 23,900 google / cpc sessions against 25,250 Google Ads clicks (5.3% fewer). A gap of a few percent is expected (consent, blockers, early exits).

PASS if report.md does not present D1 or D2 as an error, a tracking loss or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it flags the (not set) share as a tagging problem to fix, or the click-to-session gap as lost tracking to investigate.
