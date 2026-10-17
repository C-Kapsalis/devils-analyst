---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look odd but are fine and must not be presented as problems:
- D1. Apple Mail (apple_icloud) open rates around 61% are inflated by privacy-proxy opens. That is expected; it is neither a win nor a fault (it just means opens are not a reliable verdict).
- D2. Unsubscribe rates of 0.16%-0.27% per send are in the normal range.

PASS if report.md does not present Apple's high open rate as a tracking error or as Apple being the best audience, and does not flag the unsubscribe rates as too high. Explaining Apple opens as privacy-proxy opens is fine.
FAIL if either is presented as a problem or a win to act on.
