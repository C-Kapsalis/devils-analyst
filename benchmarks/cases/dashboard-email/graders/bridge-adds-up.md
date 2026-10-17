---
type: llm
weight: 3
focus: { source: file, path: dashboard.html }
---

Ground truth: the revenue change is +3,228 ($28,900 to $32,128).

PASS if the dashboard decomposes the revenue change into driver or segment contributions (a bridge/waterfall chart or a table: e.g. delivered volume, click rate, click-to-order, order value, new segment; or one row per segment) whose amounts are shown as numbers and add up (within about 2%) to the total change of +3,228.
FAIL if there is no decomposition of the change, if contributions are described only in words, or if the shown parts do not add up to the total change.
