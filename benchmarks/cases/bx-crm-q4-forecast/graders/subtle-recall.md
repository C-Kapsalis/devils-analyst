---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key:

1. Win rate by count applied to value. 30% is the share of deals won; by value it is 20%. By deal size, value win rates are small 39%, mid 26%, large (100k+) 8%, and large deals are 63% of Q4-closing pipeline. Counts as found if report.md says the count-based win rate overstates expected bookings because large deals win less often (or uses a value or size-band win rate).
2. Stale pipeline. $2,222,000 (35%) of Q4-closing pipeline has no activity in 60+ days and its close date changed 3+ times. Counts as found if report.md flags stale / repeatedly pushed deals with a number or deal list.
3. Coverage includes 2027 deals. The 3.5x divides all open pipeline ($8,320,000) by the Q4 target; deals with a Q4 close date total $6,405,000 (2.7x), and about 1.7x without the stale deals. Counts as found if report.md recomputes coverage on Q4 close dates.
4. Pipeline generated summed from snapshots. $24,387,473 adds three month-end open-pipeline balances (a stock), so the same deals are counted up to three times; pipeline created in Q3 (deals with a Q3 create date) is about $4,752,000. Counts as found if report.md says the snapshots cannot be summed.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 4, each with evidence.
FAIL if fewer than 3.
