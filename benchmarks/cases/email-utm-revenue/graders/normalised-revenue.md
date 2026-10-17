---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

PASS if report.md reports revenue for vip_reserve_preview within 5% of $10,815 AND revenue for summer_clearance_blast within 5% of $3,147. These figures require combining all spelling variants of each campaign name in ga4_sessions.csv.
FAIL if vip_reserve_preview revenue is shown near the exact-match-only figure $1,633 (or anything below $8,652), or if either figure is missing or outside 5%.
