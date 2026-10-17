---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Average view duration must be weighted by views (estimated_minutes_watched * 60 / views) and long-form videos (video_type = video) must be reported separately from Shorts.
Ground truth, September 2026:
- Long-form AVD: 336 seconds (5:36)
- Shorts AVD: 34 seconds
Wrong answers:
- Simple average of the average_view_duration column over all rows: 279 s (4:39)
- Simple average of average_view_duration over long-form rows: 414 s (6:54)
- Weighted AVD with Shorts and long-form mixed together: 86 s (1:26)

PASS if report.md gives a long-form AVD of 336 s (within 5%, i.e. 320-353 s), reported separately from Shorts.
FAIL if the headline or long-form AVD is one of the wrong values above (or otherwise outside 5%), or if only a single blended Shorts + long-form figure is given.
