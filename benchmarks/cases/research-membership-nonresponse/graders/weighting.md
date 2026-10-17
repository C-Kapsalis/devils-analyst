---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. The email survey got 480 completes from 4,000 (response rate 12%). Email respondents are 65% very or somewhat interested; the phone follow-up of non-respondents (150 completes) finds only 18%. Non-respondents are 88% of customers, so the two groups must be weighted by the response rate:
0.12 x 65% + 0.88 x 18% = 23.6% interested (95% CI about 18% to 29%) -> about 9,456 of 40,000 customers (CI about 7,282 to 11,630).
Also acceptable: the same weighting using only "very interested" (9.5% -> about 3,812).
Naive wrong answers: email respondents only, 65% -> 26,000; pooling both waves unweighted, 53.8% -> 21,524.

PASS if report.md's headline interest share is between 8% and 29% (or an interested count between 3,240 and 11,700), obtained by weighting email respondents and non-respondents by the response rate.
FAIL if the headline share is 45% or more (e.g. 65% or 54%), or the planned figure is based on email respondents alone.
