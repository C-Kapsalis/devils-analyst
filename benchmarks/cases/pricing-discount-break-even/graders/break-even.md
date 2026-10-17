---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: contribution margin per order at full price is about 37% (1 - 52% product cost - $7 / ~$64 AOV). The order lift needed to break even on contribution is margin / (margin - discount) - 1: about 117% at 20% off, 68% at 15%, 37% at 10%. The actual lift was 34%.

PASS if report.md states the lift needed to break even at 20% off as roughly 95%-140% (or more), or gives a break-even table by discount depth with values consistent with these, and compares it to the actual ~34% lift.
FAIL if no break-even lift / required-volume figure is given, or the break-even figure is below 60% at 20% off.
