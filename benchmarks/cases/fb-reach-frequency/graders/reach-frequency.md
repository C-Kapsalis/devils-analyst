---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Reach counts unique people and cannot be added across days, months, campaigns or report levels. The Q3 answer is the single account-level row covering 2026-07-01 to 2026-09-30.
Ground truth Q3 2026:
- Reach: 253,983 people
- Impressions: 2,590,635
- Frequency = impressions / reach = 10.20
Wrong answers from adding reach up:
- sum of daily campaign reach: reach 2,165,682, frequency 1.20
- sum of monthly campaign rows: reach 1,053,084, frequency 2.46
- sum of every row in the reach file: reach 3,470,826, frequency 0.75
- sum of the three monthly account rows: reach 539,847, frequency 4.80
- sum of the four quarterly campaign rows: reach 385,000, frequency 6.73

PASS if report.md gives Q3 reach of 253,983 (within 2%) and Q3 frequency of 10.20 (within 5%).
FAIL if the reach figure is any of the summed values above (or any other figure more than 2% away from 253,983), or if the frequency is below 8.
