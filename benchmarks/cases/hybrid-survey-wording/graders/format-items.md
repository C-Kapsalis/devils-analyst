---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: Q7 asks an attitude/behaviour as a yes/no (better as a 5- or 7-point frequency/agreement scale, and its relevance is unclear); Q9 is a 5-item forced ranking (hard on mobile, gives only relative order; better as an importance rating per feature or a top-pick question).

PASS if report.md flags at least one of Q7 (binary format for a graded attitude) or Q9 (ranking format) with a concrete fix.
FAIL if neither is flagged.
