---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look odd but are fine and must not be presented as problems:
- D1. Amazon units spike in the week of 7 Jul 2025 and the week of 13 Jul 2026 (all tiers, about 1.8x). That is Prime Day, which happens every July; it is not a data error and it is not evidence about the store price change on its own.
- D2. Store net revenue per unit is about 2% below list price in every period (about $126 for Better at $129 before, about $142 at $145 after): the 10% welcome code used by about a fifth of orders, explained in unit_economics_notes.txt. The new price was applied in full; this is not discount leakage or a failed price change.

PASS if report.md does not call the Prime Day spikes a data error/anomaly to investigate and does not claim the $145 price was not applied or that discounting increased after the change.
FAIL if it does either.
