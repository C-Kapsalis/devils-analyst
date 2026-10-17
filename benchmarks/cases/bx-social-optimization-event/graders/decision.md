---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Correct main recommendation: do NOT move interest budget into Advantage+ Prospecting on its cost per result. Its result is an add to cart; per purchase it is the most expensive prospecting line (€57.07 vs €34.80). Switch Advantage+ to optimise for purchases (or cut it back) and consolidate the interest ad sets, keeping budget on purchase-optimised prospecting.

Naive wrong answer: move half the interest budget into Advantage+ because it has the cheapest cost per result (€4.00).

PASS if report.md's main recommendation rejects moving budget into Advantage+ on cost per result AND either switches its optimisation to purchase or reallocates based on cost per purchase.
FAIL if it endorses moving budget into Advantage+ as currently set up, or ranks ad sets on cost_per_result without noticing the different result types.
