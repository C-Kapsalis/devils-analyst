# research-design: eval case designs

Format follows benchmarks/cases/*/ (prompt.md, scaffold.sh writing
resources/, llm PASS/FAIL graders plus a skill-fired grader that should
accept `research-design`). Numbers computed in code.

---

## 1. membership-nonresponse

**Prompt.** "We emailed a survey about a paid membership ($59/yr) to 4,000
of our 40,000 active customers. Results are in
resources/survey_responses.csv. We also phoned a random sample of people
who didn't answer the email; their answers are in the same file (wave =
phone_followup). How many members should we plan for at launch? Write
report.md."

**Data.** survey_responses.csv, grain = respondent: `respondent_id, wave
(email | phone_followup), interested (very/somewhat/not)`. Email: 480 rows
(12% of 4,000), 312 very or somewhat interested (65%). Phone follow-up: 200
non-respondents called, 150 answered, 27 interested (18%).

**Ground truth.**
- Two strata weighted by the response rate: 0.12 × 0.65 + 0.88 × 0.18 =
  23.6%; SE 0.0277; 95% CI 23.6% ± 5.4 → 9,460 interested of 40,000 (CI
  about 7,300 to 11,600).
- Stated interest overstates sign-up: plan below 9,460 or validate with a
  pre-order or deposit test.

**Naive answers.** Email only: 65% × 40,000 = 26,000. Pooling both waves
unweighted: 339/630 = 53.8% → 21,500.

**Graders.**
- `weighting.md` (weight 3). PASS if the headline interest share is between
  19% and 29% (or a count between 7,500 and 11,700) from weighting
  respondents and non-respondents by the response rate. FAIL if it is 50%
  or more, or the email-only 65%.
- `intent-deflation.md` (weight 2). PASS if it says stated interest
  overstates actual sign-ups and plans below the interested count or
  proposes a pre-order/deposit test. FAIL if it plans members equal to the
  interested count with no caveat.
- `skill-fired.md`.

---

## 2. awareness-tracker-sample

**Prompt.** "Last quarter's brand tracker (n = 400, sent to our newsletter
list) put aided awareness at 38%, ±4.8 points. The board now wants ±2
points, and separate reads for the UK and Germany. We'll use the newsletter
list again. How many completes should we buy? Write report.md."

**Data.** tracker_q3.csv (optional): 400 rows, `country (UK 220 / DE 180),
aware_aided (0/1), heard_via (newsletter)`.

**Ground truth.**
- n per read = 1.96² × 0.38 × 0.62/0.02² = 2,262.7 → 2,263 per country,
  4,526 total (π = 0.5 worst case gives 2,401 each).
- Newsletter subscribers have all heard of the brand: the convenience factor
  is the measured quantity, so the 38% is biased upward, and more completes
  from the same list do not fix it. Sample from a panel or other source
  unrelated to the brand.
- Aided awareness should be reported as aided, after an unaided question.

**Naive answers.** Linear scaling 400 × 4.8/2 = 960; or 2,263 total split
across both countries; reusing the newsletter list.

**Graders.**
- `sample-size.md` (weight 3). PASS if the per-country requirement is about
  2,200 to 2,450 (total about 4,400 to 4,900). FAIL if the total is under
  2,500 or the per-country number is about 960 or 1,130.
- `sampling-bias.md` (weight 3). PASS if the report says the newsletter
  list biases awareness upward (subscribers already know the brand) and
  recommends a different sample source. FAIL if it accepts the newsletter
  list.
- `skill-fired.md`.

---

## 3. workshop-break-even-test

**Prompt.** "We're thinking of launching a paid in-person workshop. It
breaks even at 5,000 attendees, and we have 22,000 customers. We surveyed
250 randomly chosen customers and 26% said they'd attend
(resources/workshop_survey.csv). Should we go ahead? Write report.md."

**Data.** workshop_survey.csv: 250 rows, `customer_id, would_attend (0/1)`,
65 ones.

**Ground truth.**
- K = 5,000/22,000 = 22.7%. H0: π ≤ 0.227 (do not launch). SE under H0 =
  √(0.227 × 0.773/250) = 0.0265. Critical at 95% one-sided: 0.227 + 1.645 ×
  0.0265 = 0.271. 0.26 < 0.271: cannot reject; z = 1.23, p ≈ 0.11.
- 95% CI for π: 26% ± 5.4 points → 4,530 to 6,910 attendees, which straddles
  break-even; plus stated intent overstates attendance.
- Recommendation: not a clear go; run a pre-sale or deposit test, or a
  larger sample, before committing.

**Naive answer.** "26% × 22,000 = 5,720 > 5,000: launch."

**Graders.**
- `decision.md` (weight 3). PASS if report.md does not recommend an
  unconditional launch, because 26% is not significantly above the 22.7%
  break-even (or the CI includes it), and proposes a validation step. FAIL
  if it recommends launching because 5,720 > 5,000.
- `intent.md` (weight 1). PASS if it notes that "would attend" overstates
  real attendance. FAIL otherwise.
- `skill-fired.md`.

---

## 4. concept-survey-audit

**Prompt.** "Before we send this to 5,000 customers, can you check our
survey for a new refill subscription? It's in resources/draft_survey.md.
We'll use the yes share from Q6 to forecast subscribers. Write report.md
with what to change."

**Data.** draft_survey.md, with planted errors:
1. Cover email: "Help EcoFill shape its new refill subscription!" (names
   the brand and concept).
2. Q1: "Which of these refill brands have you heard of? EcoFill / BrandB /
   BrandC" asked before Q2 "Which refill brands come to mind?" (aided before
   unaided).
3. Q3: "How often do you buy cleaning products? 0-2 / 2-4 / 4 or more times
   a month" (overlapping).
4. Q4: "How satisfied are you with the price and scent of your current
   cleaner?" (double-barrelled).
5. Q5: "Given how much plastic waste refills save, how interested are you in
   EcoFill's subscription?" (leading, one-sided).
6. Q6: "Would you subscribe? Yes / No", used directly as a forecast
   (intent overstatement, politeness bias).
7. Q1 has no "none of these" option (does not apply to everyone).

**Ground truth.** Flags at least 5 of the 7 with a correct fix each:
remove the brand from the cover note; unaided before aided; fix overlapping
ranges; split Q4; neutral two-sided wording or counter-biasing sentence for
Q5; do not use raw yes share as a forecast (deflate, use a probability scale
or a pre-order test); add "none / don't know".

**Naive answer.** Copy-edits and tone tweaks; catches the double-barrel and
overlap, misses the ordering, cover-note sensitising and the forecast misuse.

**Graders.**
- `order-and-cover.md` (weight 3). PASS if the report flags both the brand
  named in the cover email and aided-before-unaided order as biasing later
  answers. FAIL if either is missed.
- `forecast-misuse.md` (weight 2). PASS if it says the Q6 yes share will
  overstate subscribers and proposes deflation or a behavioural test. FAIL
  otherwise.
- `coverage.md` (weight 1). PASS if at least 5 of the 7 planted errors are
  identified with a fix. FAIL otherwise.
- `skill-fired.md`.
