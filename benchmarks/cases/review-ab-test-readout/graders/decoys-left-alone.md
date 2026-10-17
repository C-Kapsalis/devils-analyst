---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The readout contains two elements that are correct and must not be flagged:
- D1. The sample ratio check: control 36,236 vs treatment 36,265 users (49.98% / 50.02%), chi-square 0.01, p = 0.91. There is no sample ratio mismatch.
- D2. Conversion rate is defined per user (users who ordered / users exposed), matching the randomisation unit; control 3.25%, treatment 3.61% are computed correctly from the daily file.

PASS if report.md does not present D1 or D2 as an error or something to fix. Mentioning either as correct or fine is a PASS.
FAIL if it says there is a sample ratio mismatch or the split is a problem, or says the conversion rate definition or the two conversion rates are wrong.
