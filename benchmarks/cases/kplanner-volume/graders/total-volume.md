---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The volume (related_kplanner_searches) is repeated on every SERP row (10 SERP result rows per keyword per month). Correct method: take the value once per keyword-month, average across the months each keyword has data (some keywords were tracked for fewer months), then sum across keywords.
Ground truth total average monthly search volume across the 16 tracked keywords: 132,086.
Per keyword average monthly volume:
- hiking boots: 20,765 (2 month(s) of data)
- rain jacket: 18,248 (4 month(s) of data)
- backpacking tent: 16,560 (1 month(s) of data)
- trail running shoes: 13,980 (1 month(s) of data)
- gore tex jacket: 11,858 (4 month(s) of data)
- waterproof hiking boots: 9,902 (4 month(s) of data)
- 2 person tent: 6,730 (4 month(s) of data)
- mens rain jacket: 6,688 (4 month(s) of data)
- trekking poles: 5,548 (4 month(s) of data)
- womens rain jacket: 5,415 (4 month(s) of data)
- packable down jacket: 4,358 (4 month(s) of data)
- camping stove: 3,583 (3 month(s) of data)
- merino hiking socks: 2,862 (4 month(s) of data)
- hiking backpack 30l: 2,412 (4 month(s) of data)
- sleeping bag 3 season: 1,858 (4 month(s) of data)
- hiking boots wide fit: 1,320 (4 month(s) of data)
Wrong totals:
- Summing the column over all rows: 3,770,200; divided by 4 months: 942,550
- Summing one value per keyword-month without averaging over months: 391,610
- Summing one value per keyword-month and dividing by 4 for every keyword (ignoring that some have fewer months): 97,902

PASS if report.md gives total monthly search volume within 3% of 132,086 (a total based on the latest month only, i.e. September 2026 values, is also acceptable if clearly labelled as such: 133,280).
FAIL if the total is near any of the wrong totals, or no total is given.
