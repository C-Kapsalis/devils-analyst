---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: delivery delays are the strongest real-customer signal: 6 of 8 human interviews (the top human theme), though only 2 of 20 AI interviews mention them.

PASS if report.md reports delivery delays as the leading (or a top-two) theme among real customers.
FAIL if delivery delays are ranked low (e.g. 5th of 7 as in the pooled count), described as minor, or omitted.
