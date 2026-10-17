---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: Q5 ("The app is fast and easy to use.") is double-barrelled: it asks about two different attributes (speed and ease of use) in one item, so an answer cannot be interpreted. Fix: split into two items (one on speed, one on ease of use).

PASS if report.md flags Q5 as asking two things at once (double-barrelled) and recommends splitting it.
FAIL otherwise.
