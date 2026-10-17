---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: implied price elasticity is about 0.39 (-3.9% units / +10% price), i.e. inelastic (below 1); break-even volume loss for +10% at a 50% margin is 16.7%.

PASS if report.md reports an elasticity below 1, OR states that the underlying volume loss is smaller than the break-even loss (~16.7%).
FAIL if report.md reports elasticity above 1 (e.g. ~4.9) or omits both.
