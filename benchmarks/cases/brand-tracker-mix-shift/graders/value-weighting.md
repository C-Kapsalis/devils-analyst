---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: the core segment carries most of the value (3-year CLV $900 vs $250 and $60; 84% of CLV-weighted value at the 2025 mix). Weighting segment scores by 2025 share x CLV, the score falls 8.01 -> 7.06 (-0.96). Behaviour confirms it: core repeat purchase rate fell 62% -> 51%, while occasional (34% -> 33%) and new_promo (12% -> 14%) barely moved.

PASS if report.md weights by value (CLV or revenue) or otherwise states the core decline matters most because core customers carry most of the value, AND cites the core repeat-rate drop (62% -> 51%) as behavioural confirmation.
FAIL if report.md ignores CLV and repeat-rate data, or presents the repeat-rate data as reassuring.
