---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: Q3 frequency is 10.20 (each person reached saw the ads about 10 times in the quarter). Account frequency by month rose (July: 4.1, August: 4.8, September: 5.8) while link click-through rate fell (July: 1.58%, August: 1.32%, September: 1.06%), a classic ad-fatigue signal.

PASS if report.md concludes frequency is high / too high or showing fatigue (e.g. cites the rising monthly frequency and/or falling CTR) and recommends at least one concrete fix (frequency cap, creative refresh, broaden or exclude audiences, shift budget from saturated retargeting/prospecting sets, etc.).
FAIL if it says frequency is low, healthy or fine, or bases its verdict on a frequency below 4.
