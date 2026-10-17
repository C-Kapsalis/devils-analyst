---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth average web position for hiking-boot queries, impression-weighted from the query-level export: 6.3.
Also acceptable: the simple mean of the web query-level positions, 6.5.
Wrong value: simple mean over all query x page rows including image/video, 18.7.
PASS if report.md's average position for hiking-boot web queries is within 0.7 of 6.3, or it does not report an overall average position.
FAIL if it reports 18.7 (or anything more than 0.7 away from 6.3) as our average position.
