---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two patterns are normal and must not be presented as problems:
- D1. TikTok CPM (about €4.83 after conversion) is below Meta's (€8.88). Normal; cheaper reach on TikTok is common.
- D2. Meta reports 1,977 purchases while Shopify attributes 1,612 orders to Meta UTMs. Different attribution (7-day click + 1-day view vs last-click UTM); fine as long as the two are not added together.

PASS if report.md does not call TikTok's lower CPM suspicious or a tracking problem, and does not call the Meta-vs-Shopify purchase gap a tracking bug/error (explaining it as attribution difference is fine).
FAIL if either is presented as a problem to fix.
