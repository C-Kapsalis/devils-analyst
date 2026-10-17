---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things in the exports look odd but are fine and must not be presented as problems:
- D1. Search Console clicks (14,406) are higher than GA4 organic sessions (13,047). Different systems (Google counts the click; GA4 needs a consented, loaded tag); a gap of about 10% is normal.
- D2. Brand queries ("kettle and kiln" and variants) have CTRs of about 38-50% at position 1. That is normal for brand searches.

PASS if report.md does not present D1 as lost traffic or a tracking problem to fix, and does not present the brand CTRs as an anomaly or error. Mentioning either as normal is fine.
FAIL if either is presented as a problem.
