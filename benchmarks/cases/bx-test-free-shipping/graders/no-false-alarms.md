---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look odd but are correct and must not be presented as problems:
- D1. Unique users per arm in the readout (90,212 and 89,874) are lower than the sum of the daily users column in test_daily_by_arm.csv (118,178 and 117,735). This is correct: the same user visits on several days, so daily users do not add up to unique users. The readout correctly uses unique users.
- D2. The 7 September payment outage day was kept in. Assignment is random and the outage hit both arms alike (orders per user that day were 62% and 60% of each arm's normal level), so keeping it does not bias the A vs B comparison.

PASS if report.md does not present D1 or D2 as an error that biases or invalidates the result. Neutral mentions, or saying they are fine, PASS. Flagging session-level assignment or users in both arms is a different (real) issue and does not count against this grader.
FAIL if it says the user counts are inconsistent/wrong because daily users sum to more than the readout's users, or says the outage day must be removed because it biases the result.
