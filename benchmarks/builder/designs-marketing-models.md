# marketing-models: eval case designs

Format follows benchmarks/cases/*/ (prompt.md + scaffold.sh writing
resources/, graders as llm PASS/FAIL files plus a skill-fired tool_used
grader that should now also accept `marketing-models`). All numbers below
were computed in code.

---

## 1. price-elastic-but-underpriced

**Prompt (prompt.md).** "We sell the Trailhead insulated bottle on our
shop. Last month we ran a price test: half of visitors saw $40, half saw $44
(resources/price_test.csv). Our landed cost is $28 a unit. Demand looks
pretty elastic to me. Should we keep $40 or move? Write report.md with your
recommendation."

**Data.** price_test.csv, grain = arm: `arm, price, visitors, units`.
A: 40, 20,000, 1,000. B: 44, 20,000, 880. Optional config JSON: randomised
by visitor, 50/50, 28 days, no sample ratio mismatch (20,000 vs 20,000).

**Ground truth.**
- Units −12% for +10% price: ε = −1.2, E = 1.2 (elastic). Conversion 5.0% vs
  4.4%, z ≈ 2.83, p ≈ 0.005: the drop is real.
- Revenue: $40,000 vs $38,720 (−3.2%).
- Contribution: (40 − 28) × 1,000 = $12,000 vs (44 − 28) × 880 = $14,080,
  +17%. Per visitor $0.60 vs $0.70.
- 1/PV at $40 = 40/12 = 3.33 > E = 1.2: underpriced. At $44, 1/PV = 2.75 >
  1.2: still underpriced, so test a further step.
- Constant-elasticity formula gives P* = 28 × 1.2/0.2 = $168: an
  extrapolation far outside the tested range, not a recommendation.

**Naive answers.** (a) "Demand is elastic (E > 1) and revenue fell 3.2%, keep
$40." (b) "Optimal price is $168."

**Graders.**
- `decision.md` (weight 3). PASS if report.md recommends moving to $44 (or
  testing higher) on contribution/profit grounds, citing profit up about
  17% or 1/PV > E. FAIL if it recommends keeping $40 because demand is
  elastic or revenue fell.
- `no-extrapolation.md` (weight 2). PASS if any price recommended above
  about $50 is framed as a next test step, not a launch. FAIL if it
  recommends a price of $60 or more (e.g. the $168 formula result) as the
  new price without a test.
- `skill-fired.md` (tool_used).

---

## 2. churn-offer-threshold

**Prompt.** "Our data team scored all 10,000 Lumio subscribers with a churn
model (resources/churn_scores.csv). We have a $15 retention credit. Last
quarter's holdout showed the credit keeps about 40% of the people who would
otherwise have cancelled. Average annual margin per subscriber is $180. Who
should get the credit? Write report.md with the rule and how many people it
covers."

**Data.** churn_scores.csv, grain = subscriber: `customer_id,
churn_probability, annual_margin`. churn_probability ~ Beta(1.2, 4) (seed 7:
mean 0.23; 848 above 0.5; 5,445 at or above 0.172). annual_margin ~ gamma
with mean $180. Optional holdout_summary.csv backing the 40% save rate.

**Ground truth.**
- Assign "send credit" iff P(churn) ≥ c/(1 + c), c = C(1|0)/C(0|1).
  C(1|0) = $15 wasted on a stayer; C(0|1) = expected margin lost by not
  offering = 0.4 × $180 = $72 (or 0.4 × (180 − 15) = $66 if the credit is
  netted). c = 0.208 (0.227) → threshold 0.172 (0.185).
- Covers about 5,445 (5,182) subscribers, not 848. A per-customer rule
  using each row's annual_margin is also correct.

**Naive answer.** "Send to everyone above 50% churn risk" (848 people), or
"top decile".

**Graders.**
- `threshold.md` (weight 3). PASS if the rule's probability cut-off is
  between 0.15 and 0.20 (or an equivalent expected-value rule
  p × 0.4 × margin ≥ 15 × (1 − p) per customer) and the count is between
  about 4,800 and 6,000. FAIL if the cut-off is 0.5, a top-N/decile with no
  cost logic, or any cut-off above 0.3.
- `costs-explicit.md` (weight 1). PASS if the report states both error costs
  and that 0.5 assumes equal costs. FAIL otherwise.
- `skill-fired.md`.

---

## 3. regression-model-choice

**Prompt.** "Our agency built a sales model with 11 drivers and says it
explains 80.5% of weekly sales. Ours has 3 drivers and explains 79%. They
want us to plan next year's budget on theirs. Which model should we use?
Both outputs are in resources/models.json. Write report.md."

**Data.** models.json: n = 104 weeks; model A (ours): tv_spend,
search_spend, avg_price; R² 0.790, coefficient table with all three p <
0.01. Model B (agency): same three plus temperature, competitor_promo,
email_sends, social_posts, site_speed, holiday_flag, pr_mentions,
influencer_spend; R² 0.805; the 8 extra coefficients all have p between
0.18 and 0.85; the shared three coefficients similar to A.

**Ground truth.**
- Partial F for the 8 added terms: (0.015/0.195) × (92/8) = 0.885, below
  F_0.05(8, 92) ≈ 2.04 (p ≈ 0.53): the added block adds nothing.
- Adjusted R²: A 1 − 0.21 × 103/100 = 0.784; B 1 − 0.195 × 103/92 = 0.782.
  A is preferred.

**Naive answer.** "Use the agency model, it has the higher R²."

**Graders.**
- `model-choice.md` (weight 3). PASS if report.md prefers the 3-driver
  model (or says the extra 8 do not improve it) based on adjusted R², a
  partial F-test, or the non-significant added terms. FAIL if it picks the
  agency model because R² is higher.
- `r2-reason.md` (weight 1). PASS if it says R² never falls when variables
  are added. FAIL otherwise.
- `skill-fired.md`.

---

## 4. seasonal-forecast-ma-order

**Prompt.** "Here are 36 months of revenue for our gifting shop
(resources/monthly_revenue.csv, Jan 2024 to Dec 2026). December was our best
month ever, up 40% on November. Are we really growing, and what revenue
should we plan for January 2027? Write report.md."

**Data.** monthly_revenue.csv: `month, revenue`. Generator: 100,000 ×
1.01^t × index[month], indices (normalised to sum 12) Jan 0.686, Feb 0.784,
Mar 0.882, Apr 0.931, May 0.980, Jun 0.980, Jul 0.931, Aug 0.882, Sep 0.931,
Oct 0.980, Nov 1.273, Dec 1.763. Add ±2% noise.

**Ground truth.**
- Underlying growth ≈ 1% a month (Dec 2026 vs Dec 2025 ≈ +12.7%); the
  +40% December-on-November is season, not growth.
- January 2027 ≈ $98k (trend level × January index; anything $85k to $115k
  is fine).

**Naive answers.** 3-month moving average of Oct to Dec as the January
forecast ≈ $188k; the 12-month MA (≈ $135k) used directly without putting
January's seasonal dip back; "growing 40%".

**Graders.**
- `growth.md` (weight 2). PASS if growth is stated as about 1% a month or
  about 10 to 15% year on year, and the 40% is attributed to seasonality.
  FAIL if the report treats December's +40% as growth.
- `forecast.md` (weight 3). PASS if the January plan is between $85k and
  $115k. FAIL if above $125k or below $75k.
- `skill-fired.md`.
