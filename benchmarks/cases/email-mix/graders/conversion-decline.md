---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: total orders fell slightly (740 to 724) and orders per click (click-to-order rate) fell from about 11.9% to 10.0%, even though revenue rose (28,900 to 32,128) and clicks rose.

PASS if report.md identifies that conversion after the click weakened (click-to-order rate, or orders per click, or orders falling while clicks rose).
FAIL if it reports only the revenue and click increases as good news without noticing the weaker conversion after the click.
