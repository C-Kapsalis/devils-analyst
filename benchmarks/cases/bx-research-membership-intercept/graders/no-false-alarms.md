---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look questionable but are fine and must not be presented as problems:
- D1. The fieldwork note's margin of error, +/-3.9 points at 95% for n = 640, is computed correctly (1.96 x sqrt(0.25/640)). The sample size is adequate for that precision. (Saying the margin of error does not cover bias from who was interviewed is correct and is NOT a false alarm.)
- D2. Interviews per store are unequal (35 to 149) because they were set in proportion to each store's weekly footfall. That is a sound quota design, not a sampling flaw.

PASS if report.md does not call the margin of error miscalculated, does not say n = 640 is too small to use, and does not present the unequal interviews per store as a flaw.
FAIL if it does any of those.
