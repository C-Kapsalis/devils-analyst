---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things in the deck are correct and must not be presented as errors:
- D1. Win rate is computed as won / (won + lost), excluding open deals. That definition is correct (the problem is applying the count rate to value, not the definition).
- D2. The sales cycle is quoted as a median (59 days; the mean of won deals is 62). The median is the right typical value.

PASS if report.md does not say open deals should be in the win-rate denominator and does not say the cycle should be the mean.
FAIL if either is presented as a mistake.
