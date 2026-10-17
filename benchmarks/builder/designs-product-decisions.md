# product-decisions: eval case designs

Format follows benchmarks/cases/*/ (prompt.md with frontmatter, a
scaffold that writes resources/*.csv, graders as llm PASS/FAIL files plus a
`tool_used` grader for the Skill call). Every case: `max_turns: 40`,
`timeout_seconds: 900`, `allowed_tools: [Read, Glob, Grep, Skill, Write]`,
answer saved as report.md in the working directory. Generators with fixed
seeds are in `eval-data/` (pure Python, no numpy); the numbers below are what
they produce.

Skill-fired grader for all cases:
`input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(product-decisions|evidence-check|diagnose)"'`

---

## 1. concept-paired-test

**Prompt.** "We're Ridgeline Cycles. resources/concept_survey.csv is our
Qualtrics export (numeric values) from the concept test of three bike-lock
ideas. Respondents rated each concept on purchase intent (5 = definitely would
buy). Which concept should we take into development? Write report.md with the
numbers and your recommendation."

**Data.** `concept_survey.csv`, 180 rows: `response_id,
q1_owns_bike_commutes (Yes/No), pi_concept_a, pi_concept_b, pi_concept_c`.
150 Yes (target), 30 No (screener fails who strongly favour B). Every
respondent rated all three concepts. Generator: `eval-data/p1.py` (seed 11).

**Ground truth (150 qualified).**
- Means: A 3.48 (SD 1.08), B 3.33 (SD 1.01), C 2.87 (SD 1.07).
- Top-two-box: A 50.7%, B 44.0%, C 25.3%. Top-box: A 21.3%, B 12.7%.
- A vs B paired t = 2.38, p about 0.017: A significantly ahead.
- A two-sample test on the same columns gives t = 1.21, p about 0.23
  ("no difference"): wrong test for a within-subject design.
- A's top-two-box (51%) is far below the 80-90% favourable norm: A is the
  best of the set, not yet a go; rework before development.

**Naive answers.** (a) All 180 rows: B wins (B 3.52 vs A 3.32; B top-two-box
53%). (b) Qualified rows with a two-sample test: "A and B are statistically
tied". (c) "A wins, proceed to development" with no level check.

**Graders.**
- `screener.md` (weight 2): PASS if report.md excludes the 30 respondents who
  answered No to the screener and reports A as the highest mean among
  qualified respondents (A about 3.48 vs B about 3.33). FAIL if B is named the
  leading concept or all 180 rows are used.
- `paired.md` (weight 3): PASS if the A vs B comparison uses a paired
  (within-respondent) test and reports it significant (p below 0.05, about
  0.017), or otherwise explains that the same respondents rated all concepts
  and treats the difference as significant. FAIL if it calls A and B
  statistically indistinguishable, or uses an independent-samples test as the
  basis.
- `level.md` (weight 2): PASS if report.md says A's favourable share (top-two
  box about 51%) is low against a go benchmark (80-90%, or company history)
  and recommends improving or re-testing A rather than an unconditional go.
  FAIL if it recommends taking A straight into development with no caveat on
  the absolute level of intent.

---

## 2. forecast-calibration

**Prompt.** "We're launching the Ridgeline SmartLock at $89 next spring.
resources/ has the concept-test purchase-intent counts (pi_results.csv) and
our launch plan (launch_plan.csv). How many units should we plan to sell in
the first year? Put the forecast and how you got it in report.md."

**Data.** `pi_results.csv`: `answer,count` with definitely 43, probably 65,
might or might not 70, probably not 40, definitely not 22 (240 qualified).
`launch_plan.csv`: `item,value` with target_households 400000,
planned_aided_awareness 0.50, retail_distribution_coverage 0.60, price 89.
Durable product (one unit per buyer).

**Ground truth.** F_def = 17.9%, F_prob = 27.1%. With typical constants (0.4,
0.2): P = 0.126; A = 0.50 x 0.60 = 0.30; Q = 400,000 x 0.30 x 0.126 = about
15,100 units, revenue about $1.34M. Any calibration inside the documented
ranges (C_def 0.1-0.5, C_prob 0-0.25) gives Q between about 2,100 and 18,900.

**Naive answers.** Top-two-box as probability: 400,000 x 0.30 x 0.45 =
54,000 (or 180,000 ignoring A). Top-box as probability: 21,500.

**Graders.**
- `forecast.md` (weight 3): PASS if the base forecast is between 2,000 and
  19,000 units and is built from N x awareness x availability x a calibrated
  purchase probability that discounts "definitely" and "probably" answers.
  FAIL if it uses the raw top-box or top-two-box share as the purchase
  probability, omits awareness or availability, or forecasts above 19,000.
- `caveats.md` (weight 1): PASS if report.md gives a range or sensitivity and
  names at least one reason stated intent overstates buying (hypothetical
  money, wish to please, polished stimulus, no competitors shown). FAIL
  otherwise.

---

## 3. conjoint-segment-wtp

**Prompt.** "resources/partworths.csv is the individual part-worth export from
our conjoint study for the SmartLock (price levels $19, $24, $29; baseline
$24; plus a premium strap and a graphite colour). The premium strap costs us
$1.50 a unit. Should we add the strap to the product? Answer in report.md."

**Data.** 80 rows: `respondent_id, age_band, pw_strap_premium, pw_price_19,
pw_price_29, pw_color_graphite`. Three hidden groups: 39 love the strap
(part-worth about +1.5), 32 dislike it (about -0.9), 9 indifferent.
Generator: `eval-data/p3.py` (seed 5).

**Ground truth.** Aggregate exchange rate 0.159 utils per dollar; average WTP
for the strap about +$2.55, above the $1.50 cost. Per respondent: 49% have
WTP above cost (group mean about +$9.70), 46% negative WTP, 40% below
-$1.50 (group mean about -$5.50). The average describes almost nobody. The
decision is a strap option or a premium variant (the liking group bears
several dollars more), not a strap on the single product.

**Naive answer.** "Average WTP $2.55 > $1.50 cost, add the strap to every
unit."

**Graders.**
- `wtp.md` (weight 1): PASS if report.md computes WTP from part-worths and the
  price exchange rate (average about $2.4-2.7). FAIL if no WTP in dollars.
- `split.md` (weight 3): PASS if report.md shows that preferences split (a
  large share, about 40-46%, has negative WTP for the strap while about half
  value it well above cost) and recommends an optional strap, a premium
  variant, or targeting the segment that values it. FAIL if it recommends
  adding the strap to the standard product because average WTP exceeds cost.

---

## 4. npv-share-of-sam

**Prompt.** "Board meeting Thursday. resources/ has the cash-flow plan for the
Ridgeline e-bike battery pack (cashflow_plan.csv, quarterly, 4 years), unit
economics (unit_economics.csv) and the market study (market.csv). We've
already put $1.4M into development. Hurdle rate is 10%. Should we go ahead?
Write report.md with your recommendation."

**Data.** `unit_economics.csv`: price_to_retailer 140, variable_cost 70,
fixed_costs_per_year 1,200,000. `market.csv`: SAM_units_per_year 160,000,
competitors 6, our_brand_awareness 0.08. `cashflow_plan.csv`: quarters 1-4
outflow 350,000 each (remaining development and launch), years 2-4 unit
volumes 30,000 / 32,000 / 34,000 per year spread evenly by quarter, plus a
row `development_spent_to_date, -1,400,000` dated before quarter 1.
Generator: `eval-data/p4.py`.

**Ground truth.** Quarterly rate 2.41%. NPV of future flows about +$1.10M
(sunk $1.4M excluded; including it gives about -$0.30M, a wrong reason for a
no). Contribution margin $70; BEQ = 17,143 units a year = 10.7% of SAM. The
plan itself assumes 18.8-21.3% of SAM in years 2-4, far above the 1-5%
realistic for a new entrant. At 5% of SAM (8,000 units a year) NPV is about
-$2.8M; NPV turns positive only above about 25,200 units a year (15.7% of
SAM). Recommendation: not an unconditional go; conditional go (small pilot
with kill conditions) or no-go / rework the cost base.

**Naive answers.** (a) "NPV +$1.1M > 0, go." (b) "Including the $1.4M spent,
NPV is negative, kill it" (sunk-cost error).

**Graders.**
- `npv.md` (weight 2): PASS if report.md reports NPV of future cash flows
  excluding the $1.4M already spent, between $0.9M and $1.3M. FAIL if the
  $1.4M is included in the NPV used for the decision.
- `share.md` (weight 3): PASS if report.md computes break-even (about 17,100
  units a year, about 11% of SAM) or the plan's implied share of SAM (about
  19-21%) and says this exceeds what a new entrant realistically captures
  (around 5% of SAM), and therefore does not recommend an unconditional go.
  FAIL if it recommends go on the positive NPV without testing the share of
  SAM the plan requires.

---

## 5. scoring-weights-sensitivity

**Prompt.** "Our product team scored three headphone concepts in a workshop
(resources/scoring_matrix.csv). We also have importance ratings from our
customer survey (resources/customer_importance.csv). Which concept should we
build? report.md please."

**Data.** Ratings 1-5 vs reference (A: 3,3,4,4,3,5; B: 5,4,3,3,3,2;
C: 4,3,3,3,4,3 on comfort, battery, setup, cost, durability, style). Team
weights 15/15/10/20/15/25 (`weight_source = team workshop`). Customer
importance converted to weights 25/25/15/15/15/5.

**Ground truth.** Team weights: A 3.80, C 3.30, B 3.20. Customer weights:
B 3.70, A 3.40, C 3.40. Weights should come from customers, so B leads; but
moving 10 points of weight from comfort to style flips it back to A (3.60 vs
3.40), so the lead is not robust: carry A and B forward (or combine B's
comfort and battery with A's style and setup) and test with customers.

**Naive answer.** "A scores 3.80, build A."

**Graders.**
- `weights.md` (weight 3): PASS if report.md scores the concepts with the
  customer-derived weights and reports B ahead (about 3.70 vs 3.40). FAIL if
  it picks A from the team weights without rescoring with customer weights.
- `robust.md` (weight 2): PASS if report.md tests sensitivity (a weight or
  rating change) and says the result is close or not robust, recommending
  carrying two concepts forward, a hybrid, or a test before committing.
  FAIL if it names a single winner with no sensitivity check.
