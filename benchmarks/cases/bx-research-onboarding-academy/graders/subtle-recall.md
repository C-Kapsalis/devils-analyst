---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The materials contain 5 planted problems. Answer key (computed from accounts_pilot.csv and the other files):

1. Graduates are self-selected. Completing a 4-week course selects engaged accounts: graduates averaged 9.4 Q1 logins vs 5.4 for invited non-graduates. The invitation was randomised, so the fair comparison is invited (300) vs not-invited at-risk accounts (300): renewal 70.0% vs 67.0%, +3.0 pts, not the +20 pts graduates vs other at-risk accounts. Counts as found if report.md says the graduate comparison is biased by self-selection/engagement AND gives the invited vs not-invited comparison (any figure between +0 and +6 pts, or the two renewal rates).
2. Health rebound is regression to the mean. The pilot picked the lowest Q1 health scores; the not-invited at-risk accounts also rose from 48 to 56 (+8) vs invited 48 to 56 (+8). Counts as found if report.md says the control group rose about as much, or names regression to the mean / selection on low scores, with a number.
3. CSAT question changed. Q1 asked satisfaction with "Quillstack overall"; Q2 asked about "the support you received this quarter". Not-invited accounts also rose (3.41 to 3.97). Counts as found if report.md notes the wording change or that the not-invited group rose similarly.
4. Enterprise 100% is 8 accounts. Counts as found if report.md flags the Enterprise claim as based on too few accounts (quotes the n, or says too small to act on).
5. Effect vs break-even. At GBP 150 per invited account and GBP 3,000 per renewal, the Academy pays only if it lifts renewal by at least 5 pts per invited account. The randomised lift is +3.0 pts (95% CI -4.4 to +10.4; p vs zero about 0.43), below break-even. Counts as found if report.md compares the invited-vs-not-invited lift (or its value per account) with the 5-pt break-even or with the GBP 150 cost.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 problems, each with evidence (a number, column or quote).
FAIL if fewer than 3 are identified with evidence.
