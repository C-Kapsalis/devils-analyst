---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: Amazon sells at $29.99, below both our own store ($34) and the retailers' $34 shelf price, which undercuts our own store and our wholesale partners (channel conflict / price parity risk).

PASS if report.md flags that the Amazon price undercuts the own store and/or the retailers (channel conflict, price parity, MAP).
FAIL if report.md does not mention it.
