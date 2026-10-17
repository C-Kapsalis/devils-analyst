---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: a single-point forecast from stated intent is fragile. A good report gives a range or sensitivity (e.g. low/base/high calibration weights, or awareness/distribution scenarios) and explains why stated intent overstates purchases (hypothetical money, wish to please the interviewer, polished concept stimulus, no competing products shown, etc.).

PASS if report.md gives a range or sensitivity around the forecast AND names at least one reason stated intent overstates real buying.
FAIL otherwise.
