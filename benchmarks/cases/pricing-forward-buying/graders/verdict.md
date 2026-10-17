---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: settled units are -3.9% vs the pre-announcement baseline (397 -> 382/day) for a +10% price. Unit contribution rose from $12.00 to $14.40, so contribution/day went from $4,769 to $5,500 (+15.3%). The volume loss is well inside the 16.7% break-even loss for a 10% increase at a 50% margin.

Naive answer: "units down 49%, contribution down, roll back" (contribution on the naive windows would look like -38%).

PASS if report.md recommends keeping the increase (not rolling back), with a settled/underlying unit change between about -9% and 0% and contribution/profit up.
FAIL if report.md recommends rolling the price back or reports a ~49% volume drop as the effect of the price.
