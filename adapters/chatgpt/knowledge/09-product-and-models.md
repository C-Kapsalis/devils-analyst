# Skill: product-decisions

---
name: product-decisions
description: >-
  Use this skill when someone has survey, concept-test, conjoint or business-case
  numbers and must decide what to build, launch, price or kill: "which concept should
  we take forward", "did people like the new product idea", "how many will we sell",
  "is there demand for this", "what should we charge", "is this feature worth adding",
  "should we offer a premium version", "our scoring matrix says A, is that right",
  "how big is the market", "TAM SAM SOM", "is the business case positive", "NPV",
  "break-even", "should we keep funding this product", "we already spent a lot on it",
  "go or no-go", "can we test the concept with AI respondents". It calibrates purchase
  intent, turns conjoint part-worths into willingness to pay per segment, checks
  scoring-matrix robustness, sizes markets both ways, and runs NPV and break-even on a
  realistic share before recommending go, conditional go or no-go with kill
  conditions.
---

# product-decisions

Product data fails in a quiet way: the survey is real, the arithmetic is right,
and the decision is still wrong, because stated intent was read as buying, an
average customer was priced who does not exist, or a positive NPV rested on a
market share no new entrant gets. This skill puts a check on every move.

**The human owns two stages: the question and the decision.** Before any
number, restate the decision in one line (what is being chosen, between which
options, by whom). If the user has not given the hurdle rate, unit margin,
target segment, or calibration constants, ask; do not invent them. You
recommend; they decide.

## 1. Route the question

| The user asks | Do | Reference |
|---|---|---|
| Which concept wins, is there demand | Concept test read (section 2) | [concept-test.md](references/concept-test.md) |
| How many will we sell | Q = N x A x P forecast (section 3) | [concept-test.md](references/concept-test.md) |
| Which features, what price, premium version | Conjoint to WTP by segment (section 4) | [conjoint-wtp.md](references/conjoint-wtp.md) |
| Our scoring or screening matrix picked X | Weights and sensitivity (section 5) | [concept-selection.md](references/concept-selection.md) |
| Market size, NPV, break-even, keep funding, go/no-go | Business case (section 6) | [business-case.md](references/business-case.md) |
| Which opportunity to pursue, will people adopt it, AI respondents, usability or pilot test | Screening and adoption | [opportunity-and-adoption.md](references/opportunity-and-adoption.md) |

The data must contain: one row per respondent (survey), or one row per
respondent x part-worth (conjoint), or a dated cash-flow plan (business case).
Without it, say what is missing and stop.

## 2. Concept test: did people want it, and which one

1. **Clean first.** Drop respondents who fail the screener (they are not the
   target market), incomplete rows, values outside the scale, and rankings
   that repeat a rank. Report the count dropped. Fewer than 50 valid
   respondents: results are directional only.
2. **Check the coding.** Confirm which number means "definitely would buy"
   (some exports code it 1, not 5).
3. **Describe each concept:** mean purchase intent (PI), sample SD
   (`STDEV.S`, not population), top-box % (definitely), top-two-box %
   (definitely + probably), % ranked first.
4. **Test the gap with the right test.** Same respondents rated every concept
   (within-subject, the usual Qualtrics design): **paired t-test** on the
   per-person differences, `t = mean(d) / (sd(d) / sqrt(n))`, df = n - 1.
   Each respondent saw one concept (monadic): two-sample t-test. Using the
   two-sample test on paired data throws away the pairing and usually hides a
   real difference. Fix alpha before reading (0.05 default; say if you use
   0.10). Test top vs second and top vs third.
5. **Winner is not a green light.** A concept can beat its rivals and still be
   weak. Compare top-two-box with the user's own past tests first; without
   history, the published rule of thumb is 80-90% favorable (definitely +
   probably) to encourage further development, and the cross-category average
   "definitely" is about 19%. Below that: "best of this set, not yet a go".
6. **Same stimulus or no comparison.** Concepts shown in different formats or
   tones (words only vs words + visual, factual vs ad copy) cannot be ranked;
   adding a visual alone has lifted intent by about 20 points on average.
7. **Find what to fix:** attribute importance x attribute rating quadrant;
   important attributes rated poorly are the improvement list.

## 3. Forecast: stated intent is not purchase

```
P = C_def x F_def + C_prob x F_prob      (F = share answering definitely / probably)
Q = N x A x P                            (N = target buyers in period, A = awareness x availability)
```

- Calibration constants vary by category. Use the user's if given; otherwise
  typical values C_def = 0.4 (range 0.1-0.5), C_prob = 0.2 (range 0-0.25),
  and say so. Never use the raw top-box or top-two-box share as P.
- A is two plans multiplied: promotion (awareness) and distribution
  (availability). Ask for them; do not assume 100%.
- P measures **trial**, not repeat. For consumables, volume after trial needs a
  purchase-frequency question and repeat evidence; say the forecast covers
  trial only if that is all the data supports.
- Q is units. Market sizing (TAM/SAM/SOM) is revenue. Convert before comparing.
- Report a low / base / high range over N, A and the constants.

## 4. Features and price from conjoint

- Importance of an attribute = (max part-worth - min part-worth) / sum of all
  ranges. Attributes tested with more levels look more important; flag
  unequal level counts.
- Exchange rate = (PW(low price) - PW(high price)) / (high price - low price),
  using the price pair nearest the intended price. WTP for a level =
  part-worth / exchange rate.
- **Decide on the distribution, not the mean.** Compute WTP per respondent
  from individual part-worths. Report: share with WTP above the feature's unit
  cost, share with negative WTP, and segment means (by demographics, or
  k-means on part-worths, choosing k at the elbow of within-cluster sum of
  squares). If one group pays well above cost and another needs a discount,
  the answer is an option, a variant or a targeted version, not "add it for
  everyone because the average clears cost".
- Optimal profile = best level per attribute; then state where cost,
  feasibility or positioning makes you deviate.

## 5. Scoring and screening matrices

- Screening: +/0/- against a reference, equal weights, net = pluses - minuses;
  keep net > 0, drop net < 0, keep ties only to reach 3-5 concepts.
- Scoring: 1-5 against a reference (reference = 3, total 3.00), weighted
  total = sum(rating x weight). **Weights must come from customer importance
  data**, not the team. If customer weights exist, score with them.
- Sensitivity before naming a winner: shift the biggest weight by 10 points,
  move each uncertain rating by 1, apply each segment's weights. If the winner
  changes, the result is not robust: carry the top two forward, or pick the
  lower-uncertainty concept, and name the test that would separate them.
- Look for a transferable strength in losing concepts before discarding them.

## 6. Business case: should we fund it

1. **Size both ways.** TAM = customers x annual spend per customer; SAM = after
   geography and niche filters; SOM = realistic capture. Top-down and
   bottom-up within 2x: consistent. 10x apart: an assumption is wrong. Every
   number needs a source.
2. **SOM sanity.** A new entrant capturing 1-5% of SAM in years 1-3 is
   realistic; a plan that needs more than 5% of SAM early is a red flag, so
   compute the plan's implied share of SAM per year.
3. **NPV, future cash only.** `NPV = sum(CF_t / (1 + r)^t)`. Money already
   spent is sunk: exclude it. Quarterly flows use `r_q = (1 + r)^(1/4) - 1`.
   Use the firm's hurdle rate (most use 5-15%; ask).
4. **Break-even.** `BEQ = fixed costs / (price - variable cost per unit)`.
   Express BEQ as % of SAM (same units) and as time to reach it at the
   forecast ramp. Run price -10% and cost +20%.
5. **Decide.**

| Evidence | Recommendation |
|---|---|
| NPV > 0, BEQ inside a realistic SOM (<= 5% of SAM early), risks managed | Go |
| NPV > 0 but BEQ or the volume plan needs > 5% of SAM, or a key assumption untested | Conditional go: phased pilot with kill conditions |
| NPV < 0 at a realistic share, or BEQ above SOM | No-go or pivot (raise price only with elasticity evidence, cut cost, widen SAM) |

Also re-run NPV with volume set to 5% of SAM; if it turns negative, the case
depends on an unrealistic share.

6. **Kill conditions.** Pre-set, specific, time-bound thresholds across
   volume, satisfaction, repeat and money (for example: orders per week by
   week N, NPS above 40 for an early product, repeat rate above a set %,
   LTV:CAC at least 3:1). Miss them and the team pauses or pivots.

## 7. Adversary for every move

Run each check. A move is done only when its check passes.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Frame the decision | Is this the decision the user faces, and who makes it? | One-line restatement with options; missing margin, hurdle rate or segment asked for | Ask before computing |
| Clean the sample | Are non-target or broken responses in the counts? | Screener fails, out-of-range values, duplicate ranks counted and removed; n >= 50 | Drop them; below 50 label directional |
| Compare concepts | Is the gap noise, and does the test match the design? | Paired test if same respondents, two-sample if monadic; p vs pre-set alpha | Call it inconclusive; give n needed |
| Read the winner | Is it only the best of a weak set? | Top-two-box vs own history or the 80-90% norm; identical presentation | "Rework before go" |
| Forecast | Is stated intent being counted as sales? | Calibrated P, explicit A, trial vs repeat, units vs revenue | Recompute; show a range |
| Price a feature | Does the average customer exist? | Per-respondent WTP: share above cost, share negative, segment means | Recommend variant or option |
| Pick by scoring | Who set the weights, and does a small change flip it? | Customer-derived weights; weight and rating sensitivity | Carry two forward; name the test |
| Size the market | Would the two methods agree, and is SOM plausible? | Top-down / bottom-up ratio; implied % of SAM | Rebuild the weak assumption |
| Compute NPV | Are sunk costs or the wrong period rate inside? | Recompute without spent-to-date; rate and period stated | Redo the table |
| Break-even | Can the market supply that volume? | BEQ % of SAM <= 5% early; price and cost stress | Conditional go or no-go |
| Recommend | What does it cost if this is wrong, and what will the CFO ask? | Downside in money; cheapest test that would change the call; kill conditions | Shrink the bet to a pilot |

## 8. Score-and-probe gate before handover

1. Every row in section 7 passes. If one cannot pass with the data, say so in
   the answer.
2. Score the draft 0-100 on **clarity** (one reading, no ambiguity),
   **relevance** (answers the decision asked), **depth** (the method and
   numbers behind each claim) and **insightfulness** (something the user did
   not already see, such as the segment split or the share-of-SAM problem).
3. Any score below 80: write the probe question that would raise it, answer
   it from the data, revise, re-score. At most 2 loops; then hand over and
   note what stayed below 80.

## 9. Output

```
Verdict: <go | conditional go | no-go | inconclusive> on <decision>
Number: <the figure that decides it, with n, test and p, or NPV and BEQ % of SAM>
Action: <what to do next, including the variant, pilot or rework>
Verify: <kill conditions or the test that would confirm it, with a date>
Caveats: <data limits; what the user must decide>
```

Show the cleaning counts, the test used and why, and every assumption you did
not get from the user.

---

## File: product-decisions/references/business-case.md

# Business case: market size, NPV, break-even, recommendation

The business case is the last gate before major spending (engineering,
manufacturing, launch). The product lead recommends go, conditional go or
no-go; leadership decides go, conditional go, hold, kill or recycle.

## Market analysis

### Sizing

| Level | Definition | Estimate from |
|---|---|---|
| TAM | All potential customers x average annual revenue per customer | Census, industry reports |
| SAM | TAM after geography and niche filters | Constraints applied to TAM |
| SOM | Share of SAM realistically captured | Competition, budget, adoption; industry entry benchmarks (often 1-2% in year 1, range 1-10%) or concept-test P |

- Top-down: industry total x segment share. Good where data exists; inflates
  when categories are broad. Bottom-up: count customers x revenue each; more
  defensible because each number has a source. Do both. Within 2x:
  converging. Around 10x: re-examine assumptions.
- Concept-test forecasts are units and specific to your concept; SOM is
  revenue from benchmarks. If the two disagree a lot, find out why.
- Common errors: TAM quoted as a target, unsourced numbers, broad category
  data for a niche product, unrealistic adoption, math not shown. Data given
  that is irrelevant to the size (distractors) should be left out explicitly.
- Early-stage firms: 1-5% of SAM in years 1-3 is realistic; leaders reach
  20-40% over years. More than 5% early signals an unrealistic plan.

### Adoption (who buys first, how fast)

Adopter groups: innovators 2.5%, early adopters 13.5%, early majority 34%,
late majority 34%, laggards 16%. Launch targets the first two; the gap to the
early majority (the chasm) is crossed by winning one scalable niche with a
repeatable mainstream use case, then expanding. Rate the five product factors
H/M/L through the target segment's eyes: relative advantage, compatibility,
complexity (higher is slower), trialability, observability. Each low factor
gets a fix (quantify the gain, simplify or onboard, free trial or guarantee,
visible packaging or referral). A revenue ramp with no adoption story behind
it is the most common reason cases break.

### Industry attractiveness

Five forces, each H/M/L with a reason: rivalry, substitutes, new entrants
(horizontal); supplier power, buyer power (vertical). Highly competitive
markets need a defensible niche.

## Financial analysis

| Concept | Formula or rule |
|---|---|
| Present value | `PV = C / (1 + r)^t` |
| NPV | `sum over t of CF_t / (1 + r)^t`, outflows negative; t = 0 undiscounted |
| Quarterly rate | `(1 + r_annual)^(1/4) - 1` |
| Discount rate | Opportunity cost of capital; firms commonly use 5-15%; larger firms lower (cheaper capital, less risk on distant flows) |
| Sunk cost | Spent and unrecoverable: excluded. The only question is whether the next dollar creates value |
| Contribution margin | price - variable cost per unit (use the price the firm receives, after channel margins) |
| Break-even quantity | fixed costs / contribution margin |

Cash-flow table: one column per period (quarters for launches), rows for each
revenue and cost line (development, tooling, ramp-up, launch marketing,
ongoing marketing, unit production cost, overhead), period cash flow, period
PV, NPV. Early periods are all outflows.

NPV reading: well above 0 strong go; above 0 go; near 0 marginal or
conditional; below 0 no-go. NPV also depends on the rate: show the result at
the low and high end of the plausible rate.

Break-even checks:
1. Feasibility: BEQ as % of SAM (same units); within SOM? If not: raise price
   (only with elasticity evidence), cut cost, or widen SAM through more
   channels.
2. Timeline: time to BEQ at the adoption ramp vs funding runway.
3. Sensitivity: price -10%, costs +20%.

## Recommendation

| Outcome | When |
|---|---|
| Go | Demand validated, NPV > 0, BEQ achievable within SOM, risks mitigated |
| Conditional go | Promising, but a metric is borderline or a key assumption untested: phased pilot |
| No-go or pivot | Market too small, unit economics fail, risks unmanageable |

Five parts: the decision; the evidence (intent, WTP, SOM, NPV, BEQ); the risks
(market, operational, financial, technical, legal) on a likelihood x impact
grid (high-high is top priority, low-likelihood high-impact gets a
contingency, high-likelihood low-impact is monitored, low-low accepted); the
success criteria; next steps with dates.

Success criteria (they double as kill conditions): specific metric and
threshold, a deadline, tied to viability, spread across volume, satisfaction
(NPS above 40 typical for early products, above 50 strong), retention (repeat
rate) and money (LTV:CAC at least 3:1, break-even by a date). Agreed before
launch so that stopping is not an emotional decision.

## After the gate

Confidence builds through prototype (concept risk; not usable by customers),
MVP (demand risk), alpha (internal; technical risk), beta (external real use;
usability and fit risk), launch (scale risk). Post-launch, track adoption,
retention and revenue against the case's own projections.

---

## File: product-decisions/references/concept-selection.md

# Concept selection: screening and scoring matrices

The goal is to create the best concept, which may be a combination, not to
crown the best existing one. Structured selection keeps the team objective
and turns a personality clash into a criteria discussion.

## Preparing the matrix

- Criteria: 5-10, from customer needs plus enterprise needs (cost or ease of
  manufacture always included, since cost sets the floor on price). Chosen to
  differentiate concepts, independent of each other (three versions of
  "quality" triple-count one dimension), objective metrics where possible
  (part count as a proxy for assembly cost, number of steps for ease of use).
- Reference: an industry standard, best-in-class competitor, previous
  generation, or a simple concept everyone understands well. A different
  reference per criterion is allowed to avoid scale compression.
- Concepts at the same level of detail, labelled, with sketch and text.

## Screening (many to 3-5)

| Step | Rule |
|---|---|
| Rate | +, 0, - vs reference; rate all concepts on one criterion before the next; all criteria equal weight (no customer weights exist yet) |
| Score | net = count(+) - count(-) |
| Keep | net > 0 continue; net < 0 drop; net = 0 keep only to reach 3-5 |

## Scoring (few to winner)

| Step | Rule |
|---|---|
| Rate | 1 much worse, 2 worse, 3 same as reference, 4 better, 5 much better; use the full scale |
| Weight | % weights summing to 100, from customer importance research; a separate matrix per segment, same ratings, different weights |
| Score | sum(rating x weight); reference = 3.00; above 3 better overall |
| Improve | effort on high-weight criteria pays most: 3 to 4 on a 25% criterion adds 0.25, on a 5% criterion 0.05 |

## Combine and improve (the step teams skip)

Ask: which concept excels on a criterion, and can that feature move? Is a good
concept dragged down by one feature? Can two concepts merge, keeping pluses
and cancelling minuses? A low-ranked concept can carry one transferable
strength.

## Sensitivity (before selecting)

1. Move the largest weight by about 10 points (for example 25% to 15%).
2. Move each uncertain rating by 1.
3. Apply each segment's weights.
4. Any change of winner: decision not robust. Options: carry two concepts
   into prototyping and customer testing; choose a slightly lower-scoring
   concept with less uncertainty; investigate the uncertain criterion.

## Traps

- Team-set weights: the loudest voice sets them. Replace with customer data.
- "Best average" concepts: niche excellence often beats broad mediocrity when
  weights reflect the target market.
- Scale compression: everything rated 3-4; change the reference.
- Subjective criteria (aesthetics): narrow to 3-4 and ask target customers.
- A/B testing does not replace selection: tests compare what was built;
  selection decides what is worth building.

## Upstream: generating enough concepts

Teams that generate more concepts end up with better products. Search
externally (benchmarks, lead users, patents) before brainstorming; ideate
alone first, then as a group, then refine alone. A good final set holds both
incremental and breakthrough ideas. If only two or three concepts were ever
considered, say the selection is limited by the input.

---

## File: product-decisions/references/concept-test.md

# Concept test: method and interpretation

A concept test asks target customers to react to a product idea before it is
built. Its outputs are a choice between concepts, a list of fixes, and a unit
forecast. It replaces team judgment with customer data, so the data has to be
from the right people, shown the same way, and read without inflating intent.

## Design checks (ask about these before trusting the numbers)

| Element | What good looks like | Why it matters |
|---|---|---|
| Purpose | Written questions: like/dislike, fit to needs, which concept, how to improve, how many units, continue or pivot | Defines which measures are needed |
| Population | Mirrors the target market; screener questions end the survey for non-targets; each served segment sampled | Biased sample, biased forecast |
| Sample size | No formula; 10 for qualitative depth, 50+ for quantitative, up to ~1,000. Larger when late in development, when investment is high, or when few people are expected to value it | Below 50 a few heavy users can swing results |
| Format | Face-to-face for demos and many alternatives; structured online forms when questions are focused; email only to people with an existing relationship | Mode changes response |
| Stimulus | Same level of detail and same tone for every concept; positioning-style concepts predict behaviour better than bare core-idea statements; working prototypes risky (mistaken for the final product) | Words + visual raised intent ~20 points on average over words only; persuasive copy scores higher than factual |
| Price | Usually omit; ask open-ended price expectation instead. Include only if price is unusually high or low, performance needs a high price, or the category has no price reference | Early prices are guesses and steer preference |
| Competition | Show alternatives (and competitor products if possible), ask for choice | Enables share estimates; single concepts in a vacuum inflate intent |
| Scale | 5-point PI in fixed order: definitely, probably, might or might not, probably not, definitely not | The evidence-backed order |

## Four kinds of data to collect

1. Purchase measures: intent, expected frequency, units per purchase.
2. Overall diagnostics: uniqueness, believability, importance of the problem,
   interest, value for money (only if price was shown).
3. Attribute diagnostics: rating of each attribute and its importance.
   **Quadrant analysis**: plot importance against rating; the quadrant of high
   importance and poor rating is where improvement effort goes.
4. Profiling: current behaviour, category perception, switching barriers,
   role in the purchase decision.

## Cleaning sequence

1. Export numeric values (codes) and keep the label export as the codebook.
2. Remove header metadata rows; keep one header row.
3. Delete respondents failing any screener; delete mostly blank rows.
4. Range check every PI column; ranks must be unique and complete per person;
   remove implausible price expectations or fix obvious typos.
5. Report n before and after each step.

## Analysis

Summary table per concept: mean PI (2 decimals), sample SD, top-box %,
top-two-box %, % ranked first.

Significance:

| Design | Test | Statistic |
|---|---|---|
| Every respondent rated every concept | Paired t-test | `t = mean(d)/(sd(d)/sqrt(n))`, df = n - 1 |
| Each respondent saw one concept | Two-sample t-test | difference in means over pooled or Welch SE |

Run top vs second and top vs third. Report n, means, SDs, t, df, two-tailed p,
the alpha set beforehand, and one plain sentence. Course practice used alpha
0.10; say which you use.

Why pairing matters: respondents differ a lot in how generous they are with
any concept. The paired test removes that person-level spread, so a modest
but consistent preference shows up; the two-sample test leaves it in the
noise.

If metrics disagree (mean favours A, ranked-first favours B), state the
trade-off and choose with qualitative comments and feasibility in view.

## Interpreting the level, not just the ranking

- Benchmarks: own historical tests first, then research-firm databases, then
  published norms. Published: 80-90% favourable (definitely + probably)
  encourages development (experience across 100+ brands); average
  "definitely" about 19% across categories, varying widely by category.
- A concept that wins the set but sits far below the norm needs rework, not
  a go.

## Forecast

`Q = N x A x P`, `P = C_def x F_def + C_prob x F_prob`.

- N from secondary data (potential buyers in the period).
- A = awareness x availability; hard to estimate; tie to the promotion and
  distribution plans.
- Constants: C_def typically 0.4 (0.1-0.5), C_prob 0.2 (0-0.25); category
  specific. P is a probability, not a price.
- Example shape (not from any case): 15% definitely and 25% probably gives
  P = 0.06 + 0.05 = 0.11.

What inflates PI: no real money at stake, wish to please the researcher,
polished stimulus better than the product will be, captive audience, no
competitors shown. What moves real sales away from the forecast: promotion
levels, word of mouth (raises A after launch), product or price differing from
what was tested, competitor response.

Intent predicts trial much better than repeat (in a classic six-product
study, repeat-given-trial barely differed across intent levels). For
nondurables collect purchase frequency and treat volume beyond trial as
unknown until repeat is observed.

Reflect: were key benefits communicated? Is the forecast consistent with
sales of similar products? Run sensitivity on N, A and P.

## When skipping formal testing is defensible

Fast-moving software with a short market window, or testing costs above the
value of the information. Truly novel products are hard for respondents to
judge. Most firms still should test when development cost is high.

---

## File: product-decisions/references/conjoint-wtp.md

# Conjoint: from part-worths to features, price and segments

Conjoint treats a product as a bundle of attribute levels and decomposes
overall preference into part-worths. It beats direct importance questions
because people state that everything matters, cannot introspect their
weights, and rate on scales that are not comparable across items.

## Design audit (flag before trusting results)

| Rule | Violation to flag |
|---|---|
| 3-5 attributes, price included | More causes fatigue |
| Only attributes a decision depends on; tell respondents what to assume about must-haves | Testing table stakes |
| 2-4 levels per attribute, similar counts across attributes | Attributes with more levels get inflated importance |
| Levels specific, realistic, mutually exclusive, one dimension each | "Good", "$6-$8", "round or square", mixed units ($/month vs $/year) |
| No infeasible combinations | Profiles nobody could sell |
| Efficient fractional design (a subset of all combinations) | Full factorial too long |
| Rating survey: each profile rated 1-7, order randomised; 10+ respondents minimum, more for individual analysis | Too few rows per person for individual regressions |

## Estimation

- Dummy-code every non-baseline level; baseline part-worth = 0. Never include
  all levels of one attribute (perfect collinearity).
- Aggregate model: all respondents stacked in one regression, one set of
  average part-worths. Individual models: one regression per respondent,
  needed for WTP distributions and segments.
- Intercept = predicted rating of the all-baseline profile. Utility of any
  profile = intercept + its part-worths; the higher utility is predicted to
  be chosen.

## Derived numbers

| Output | Formula | Read |
|---|---|---|
| Preferred level | highest part-worth per attribute (baseline = 0) | Part-worth plot per attribute |
| Importance | range / sum of ranges | Which dimensions move choice |
| Exchange rate | (PW low price - PW high price) / (high - low price) | Utils per currency unit; use the pair nearest target price, or average pairs |
| WTP for a level | part-worth / exchange rate | Positive: will pay more; negative: needs a discount |
| Profit test | WTP vs unit cost of the upgrade | WTP > cost: profitable for that person or group |

## The averaging trap

An average WTP can clear cost while almost nobody sits near the average: one
group pays several times the cost, another needs a discount to accept the
feature. The average describes no customer and a single product built on it
pleases neither group.

Procedure:
1. Individual exchange rate and WTP per respondent (individual values can be
   far from the average: one respondent valuing a level many times more than
   the mean is normal, not an error).
2. Distribution: share above cost, share below zero, share near zero.
3. Segments: demographic groups (`AVERAGEIF` of part-worths) are easy to
   target but often do not align with preferences; k-means on part-worths
   finds preference groups; choose k at the elbow of within-cluster sum of
   squares; describe each cluster by its part-worths and then its
   demographics.
4. Segment WTP table. If segments disagree in sign, recommend variants (one
   per segment, priced from that segment's WTP), an add-on option, or
   targeting the segment that values it; show the price each could bear.
5. Optimal profile per segment, then check cost and feasibility.

## When not to trust conjoint

Attributes interact (the model assumes additive utility), levels are
unrealistic, or the sample skews away from buyers. Synthetic (LLM)
respondents should not be used for willingness-to-pay decisions without
calibration against human data: in published comparisons they skew
toward extreme ratings and compressed variance.

---

## File: product-decisions/references/opportunity-and-adoption.md

# Opportunity screening, needs, prototype tests and synthetic respondents

## Screening opportunities

An opportunity is a hypothesis about how value could be created. Process:
charter (goal, target user, context, stakeholders, kept broad) -> generate
many -> screen out the unlikely -> develop 3-5 -> select the exceptional few
-> reflect.

- Early screen uses one criterion only: is this worth a few days or weeks
  more investigation? Collect independent judgments (survey or workshop with
  multi-voting): at least 6, preferably more than 10.
- Develop the survivors by listing their biggest uncertainties, the task that
  would resolve each, and its cost; do the tasks that remove most
  uncertainty per unit of cost first.
- Final selection: Real (need, ability and willingness to buy, viable concept,
  acceptable risk to the customer), Win (sustainable advantage, resources,
  management commitment, market knowledge at least equal to rivals), Worth it
  (return at acceptable risk, cash and people, strategic fit). Name which of
  the three fails rather than giving an overall opinion.
- Desirable (people), viable (business), feasible (technical): all three are
  needed; two out of three still fails.
- Risk horizon: H1 known solution and known market (improvement, low risk);
  H2 new on one axis (adjacent technology or adjacent market, moderate);
  H3 new on both (high risk, breakthrough potential). Judge H3 ideas by H1
  payback rules and every exploration dies; keep a deliberate mix.
- Quality of the best opportunity rises with volume, mean quality, variance
  of ideas, and accuracy of evaluation. Customers are the single largest
  external source, then competitor products, then the sales force.

## Customer needs

- Explicit needs: table stakes. Unfulfilled needs: differentiation. Latent
  needs: breakthrough; found through lead users (heavy users who build
  workarounds), observation in the use environment, hacks and unintended
  uses, complaints about adjacent problems.
- Interviews per segment: at least 10, stop when two more rounds add no new
  needs; around 50 is usually too many. Cover purchasers and users when they
  differ.
- Need statements: what, not how; specific; positive; in product-attribute
  terms; no must/should. Organise into primary and secondary needs; weight
  importance by customer survey (1-5 importance plus a flag for
  unexpected or exciting features).

## Prototype and pilot tests as evidence

- Usability: about 5 users from the target audience uncover most usability
  issues (roughly 85%); 2-3 tasks, think-aloud, no help; issues seen in 3 or
  more of 5 users are real; rank critical (blocks the task), major (slows),
  minor (annoys).
- Service pilots: 1-2 scenarios, 5-10 target users, success criteria set in
  advance (for example share completing booking unaided), realistic setting,
  observer notes.
- Do not jump to high fidelity: each fidelity step filters bad ideas
  cheaply; a polished prototype can solve the wrong problem.
- Digital funnels designed around a pain point: map the core path in 5-8
  steps and mark drop-off points; the biggest drop is the first test target.

## Synthetic (LLM) respondents

Use for drafting the instrument, previewing results, spotting zero-variance
or redundant questions, and a first variance estimate for sample sizing.
Do not use as final evidence for launch or pricing.

Known behaviour versus human panels, from published hybrid-research work:

| Property | Zero-shot persona prompts | With response history | With history + retrieved prior research |
|---|---|---|---|
| Direction of means | Usually right | Same | Same |
| Level of means | More extreme, about 0.5-0.7 points on a 5-point scale | Not fixed | Not fixed |
| Variance | Too low | Improved | Improved |
| Correlations between items | Near zero | Positive, directional | Closest to human |

Recovery targets when comparing to a human benchmark: mean absolute error
below 0.5 on a 5-point scale, variance ratio 0.7-1.3, correlation error below
0.2, same winning concept, rank correlation at least 0.8. Avoid for
new-to-the-world products, culturally specific groups, PII, and vulnerable
populations. The research question and the design stay human.

---

# Skill: marketing-models

---
name: marketing-models
description: >-
  Use this skill when a marketer asks a question that needs a model, not just a
  metric: "what price should we charge", "are we underpriced", "what will sales be
  next month or next quarter", "is the business really growing under the seasonality",
  "how fast will unit cost fall as we scale", "what drives sales", "which regression
  should we trust", "does the effect differ by group", "who should get the retention
  offer", "which customers will churn or convert", "is the churn model any good",
  "segment our customers", "what do our survey ratings boil down to", "are these two
  things related", "is this investment worth it", "how much can we pay to acquire a
  customer". Picks the method (NPV and CLV, elasticity, forecasting, regression,
  chi-square, logit, factor and cluster analysis), runs it with exact formulas, checks
  it, and turns the numbers into a decision. Did a change cause a result: use
  evidence-check. Defining a metric: metric-definitions. Survey design:
  research-design.
---

# marketing-models

A right number can still lead to the wrong decision. This skill picks the
model that fits the question, runs it in code, and reads it the way the
decision needs: profit not revenue, cost-weighted thresholds not 0.5, fit
judged against a naive baseline, effects tested before they are sized.

Two rules run through every method:

- **Beat the naive baseline.** R² compares with the mean, the logit
  likelihood-ratio test with the intercept-only model, the lift curve with
  random picking. A model that does not beat its baseline says nothing.
- **Significance before size.** Test that an effect exists (F, chi-square,
  likelihood ratio, t) before you interpret how big it is.

## 0. What the human owns

The question and the decision are the user's. Before modelling, ask (do not
assume) what is unknown here:

| Ask | Why |
|---|---|
| What decision rides on this, and what does each kind of mistake cost? | Sets the classification threshold and the price objective (profit, not revenue) |
| Unit variable cost or margin per unit? | Price and CLV decisions are wrong without it |
| Discount rate and horizon? | NPV, IRR and CLV depend on both |
| Length of the seasonal cycle? | Sets the moving-average order |

If the user cannot answer, state the assumption you used and show how the
answer changes if it is wrong.

## 1. Pick the method

| The question | Dependent variable / data | Method | Reference |
|---|---|---|---|
| Is this investment worth it? Max acquisition cost? Minimum retention? | Cash flows over time | NPV, IRR, CLV | [valuing.md](references/valuing.md) |
| Is the price too high or too low? Best price? | Price, quantity, unit cost | Elasticity, PV ratio, P* | the `pricing-promotions` skill owns price and promotion decisions (promo controls, stock-up around price changes, test steps); use [pricing.md](references/pricing.md) only for the model fit itself |
| Next period's sales; trend under seasonality | Time series | Moving average of order = cycle | [forecasting.md](references/forecasting.md) |
| Constant % growth or decay (new product revenue, awareness after ads stop) | Series over time | Exponential, ln Y on t | [forecasting.md](references/forecasting.md) |
| Unit cost vs cumulative volume; constant elasticity demand | Two variables, % to % | Power model, ln Y on ln X | [forecasting.md](references/forecasting.md) |
| What drives a quantity? Does the effect differ by group? | Continuous Y | Linear regression, dummies, interactions, partial F | [regression.md](references/regression.md) |
| Are two categorical variables related? Equal rates across groups? | Cross-tab of counts | Chi-square | [regression.md](references/regression.md) |
| Will this case be 1 or 0, and what do we do? | Binary Y | Binary logit + cost-based classification + lift | [logit.md](references/logit.md) |
| Which of 3+ options will each segment choose? | Choice among >2 | Multinomial logit | [logit.md](references/logit.md) |
| Many correlated ratings; who belongs together | Ratings or part-worths per respondent | Factor analysis, then K-means on factor scores | [segmenting.md](references/segmenting.md) |
| Did B beat A? Did the change work? | Experiment or before/after | Not here: **evidence-check** | |

Several categorical predictors at once: logit, not a stack of chi-square
tests (separate cross-tabs can each look significant and vanish together).

## 2. Check the data before fitting

| Method | The data must contain | Refuse or caveat when |
|---|---|---|
| Pricing | Price, units at each price, unit variable cost | No variable cost: give elasticity only, no price advice |
| NPV / CLV | Cash flow per period (margin, not revenue), discount rate, retention | Revenue given instead of margin: say CLV is overstated |
| Moving average | At least 2 full cycles; cycle length | Fewer than n points: no MA exists yet (first MA at t = n) |
| Regression | n well above the number of coefficients; no duplicated rows | Duplicated rows inflate n and shrink standard errors |
| Chi-square | Counts (not percentages) per cell | Any expected count < 1, or < 80% of cells with expected ≥ 5 |
| Logit | One row per independent case; both outcomes present | Rows for related people repeated: likelihood assumption broken |
| Factor / cluster | Respondent x item matrix, items on comparable scales | Raw correlated items fed straight into K-means |

## 3. Run it: exact formulas

| Need | Formula |
|---|---|
| NPV | Σ V_t / (1 + I)^t |
| IRR | I such that Σ V_t / (1 + I)^t = 0 (exists, unique and positive only if V_0 < 0, later V_t > 0 and their sum > abs(V_0)) |
| CLV | Σ V_t R^t / (1 + I)^t − AQ = Σ V_t / (1 + ρ)^t − AQ, with ρ = (1 + I − R) / R. Use one form, never both |
| Max acquisition cost | AQ_max = Σ V_t R^t / (1 + I)^t |
| Minimum retention | R_min = (1 + I) / (1 + IRR), IRR of (−AQ, V_1..V_T) |
| Elasticity (two points) | ε = (ΔQ/Q) / (ΔP/P); E = abs(ε). Many points: slope of ln Q on ln P |
| PV ratio | PV = (P − VC) / P; a 1% price rise adds 1/PV % to unit margin and costs E % of volume |
| Optimal price | Constant elasticity, E > 1: P* = VC · E / (E − 1). Linear Q = A − BP: P* = A/(2B) + VC/2 |
| Moving average | MA_t = (X_t + ... + X_{t−n+1}) / n, n = cycle length; MA_t forecasts t+1; MA_t − MA_{t−1} = trend per period |
| Exponential | ln Y = ln A + b t; % change per period = e^b − 1 |
| Power / experience | ln Y = ln A − a ln X; cost after a doubling = 2^−a of before; a = −log2(learning rate); C = C_0 (Q/Q_0)^−a |
| R², adjusted R² | R² = 1 − SSE/SST; adj = 1 − (1 − R²)(n − 1)/(n − m − 1) |
| Partial F | F = [(R²_full − R²_restricted) / (1 − R²_full)] · (n − m − 1)/k vs F_α(k, n − m − 1) |
| Chi-square | E_ij = row_i · col_j / n; χ² = Σ (O − E)²/E; df = (R − 1)(C − 1) |
| Logit | I = b_0 + Σ b_j X_j; P(Y=1) = 1/(1 + e^−I); odds R = e^I; +1 unit of X_j multiplies odds by e^{b_j} |
| LR test | deviance_restricted − deviance_full vs χ²_α(k) |
| Classify | Assign 1 iff R ≥ c, c = C(1\|0)/C(0\|1); equivalently P(Y=1) ≥ c/(1 + c) |
| Multinomial | I_1 = 0; P_j = e^{I_j} / (1 + Σ_{k≥2} e^{I_k}) |
| Factors kept | Eigenvalue ≥ 1; variance explained = Σ kept eigenvalues / m; item belongs to a factor if abs(loading) ≥ 0.5 |
| K-means | Minimise Σ WCSS; choose K at the elbow of total WCSS vs K |

Compute in code. Show the table of inputs so the reader can redo it.

## 4. Decision rules

| Situation | Rule |
|---|---|
| Price | 1/PV < E: overpriced, cut. 1/PV > E: underpriced, raise. Equal: optimal. E < 1: raising price always raises profit |
| Elastic demand (E > 1) | Says revenue falls with price, **not** that profit falls. Decide on 1/PV vs E |
| Price move size | The 1/PV vs E test is local (about 1%). Move a step, re-measure E, repeat. Do not jump to P* far outside observed prices |
| Investment | Invest iff NPV ≥ 0; choose the highest NPV; customer: invest iff ρ ≤ IRR |
| Forecast with seasonality | MA order must equal the cycle; any other order leaves seasonality in |
| Model choice | Same Y only. Higher adjusted R², or a significant partial F for the added block. Never raw R² |
| Reading a regression | F-test first (stop if not significant), then R², then each coefficient |
| Dummy coefficient | A difference in group averages vs the base level, not "a one-point increase" |
| Interaction model | The main-effect coefficient is the effect for the base group only. Effect in group g = main + interaction |
| Classification | Threshold from costs, not 0.5. 0.5 assumes both errors cost the same |
| Logit coefficient | Changes log-odds; the probability effect depends on where the case sits on the S-curve |
| Model usefulness for targeting | Lift curve: actual positives in the top i ranked vs i · base rate; closer to the "all positives first" curve is better |
| Chi-square not significant | No evidence of a relationship, not evidence of none. Significance grows with n (double the counts, double χ²) |
| Segments | Factor analysis first, K-means on factor scores; factor scores are standardised, so 0 = average, not "none" |

## 5. Write the answer

```
Verdict: [decision in one line]
Deciding number: [the figure and the test that decides it]
Naive read and why it is wrong: [one line]
Action: [what to do now] · How to verify: [the test, data or re-measurement that confirms it]
Assumptions: [costs, rates, cycle length used, and what flips the decision]
```

## 6. Adversary for every move

Each step gets attacked before it stands. Run the check; if it fails, do the
fix before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Frame the decision | "Is this the user's decision, or one I invented?" | The decision and the error costs come from the user or are stated as assumptions | Ask the user; do not model yet |
| Pick the method | "Does the method match the type of Y?" | Section 1 table: continuous → regression, binary → logit, >2 → multinomial, two categoricals → chi-square | Switch method |
| Pick the method | "Is this really a causal question?" | Wording like "did it work", "caused", "after we changed" | Hand to evidence-check |
| Load the data | "Margin or revenue? Units or currency?" | Column definitions; VC or margin present | Ask for cost; caveat or stop the price/CLV advice |
| Fit the model | "Does it beat the naive baseline?" | F-test, LR test vs null deviance, or lift vs random | Report "no evidence the model helps"; stop |
| Size the effect | "Is the effect significant before I size it?" | p-value or test statistic vs critical value | Report as not established |
| Chi-square | "Is the table valid?" | All E ≥ 1 and ≥ 80% of E ≥ 5 | Merge neighbouring categories (keep ≥ 2x2), recompute |
| Choose a model | "Did fit rise only because I added variables?" | Adjusted R² and partial F on the added block | Keep the smaller model |
| Interaction | "Am I reading the base-group effect as the effect for all?" | Write each group's effect = main + interaction | Recompute per group |
| Price advice | "Am I deciding on revenue instead of profit?" | Contribution (P − VC) · Q at each price; 1/PV vs E | Redo on contribution |
| Price advice | "Is P* an extrapolation?" | P* inside or near the tested price range | Recommend a step and a re-test instead |
| Forecast | "Is seasonality leaking into the trend?" | MA order = cycle length; compare same season | Refit with order = cycle |
| Exponential fit | "Did I report b as the % change?" | % change = e^b − 1 | Correct it |
| CLV / NPV | "Did I count churn twice or use revenue?" | Only one of R^t or ρ; V_t is margin | Recompute |
| IRR | "Does a positive IRR even exist?" | Outflow first, inflows sum > outflow | Report NPV only |
| Classification | "Why this threshold?" | c = C(1\|0)/C(0\|1) from stated costs; threshold P ≥ c/(1 + c) | Recompute; show who changes group |
| Segments | "Are clusters built on duplicated items?" | Factors with eigenvalue ≥ 1, varimax, K from the elbow | Refit on factor scores |
| Recommend | "What does it cost if this is wrong, and what would the CFO ask?" | Downside in money and a way to verify (test, holdout, re-measure) | Add the test or shrink the bet |

## 7. Score-and-probe gate before handover

1. Confirm every adversary check above passed (or its fix was applied).
   Any open failure: fix it first; do not score.
2. Score the draft 0 to 100 on four dimensions (the moderation rubric of the
   user's hybrid-research notes):
   - **Clarity**: one reading gives the verdict, number and action.
   - **Relevance**: answers the user's decision, not a neighbouring one.
   - **Depth**: shows the deciding calculation and its assumptions.
   - **Insightfulness**: says what the naive read misses and what flips the decision.
3. Any score below 80: write the probe question that would raise it (for
   example "what happens to the decision if variable cost is 10% higher?"),
   answer it from the data, revise, and re-score. At most 2 loops; then hand
   over and name what is still weak.

---

## File: marketing-models/references/forecasting.md

# Forecasting trends and costs

## Which model

| Pattern in the data | Model | Confirm by |
|---|---|---|
| A shape that repeats every n periods | Moving average of order n | Same-season comparisons line up |
| Constant % change per period | Exponential Y = A e^{bt} | ln Y vs t is a straight line |
| Each % change in X gives a fixed % change in Y | Power Y = A X^{−a} | ln Y vs ln X is a straight line |

## Moving average (seasonal series)

1. Find the cycle length n (4 for quarters, 12 for months, 7 for days).
2. From t = n: MA_t = (X_t + ... + X_{t−n+1})/n. No MA exists before t = n.
3. MA_t is the forecast for t + 1.
4. Trend per period ≈ MA_t − MA_{t−1}.

Why the order must equal the cycle: write X_t = a·t + β_t with β_t = β_{t−n}.
Then MA_t − MA_{t−1} = (X_t − X_{t−n})/n = a: the seasonal terms cancel only
when the window spans exactly one cycle. A 3-month window on monthly data
with a December peak carries the peak into the trend and into January's
forecast.

For seasonal indices and deseasonalised growth (ratio to moving average) see
metric-definitions, "Seasonal index".

## Exponential growth or decay

1. Regress ln Y on t: slope b, intercept ln A.
2. Growth factor per period e^b; % change per period e^b − 1 (close to b only
   when b is small).
3. b > 0 growth (absolute steps get larger); b < 0 decay, such as awareness
   after advertising stops (absolute steps get smaller).

## Power model and experience curve

1. Regress ln Y on ln X: slope −a.
2. Experience curve: unit (marginal) cost after Q cumulative units.
   Learning rate = cost after a doubling / before = 2^−a; drop per doubling
   = 1 − 2^−a; a = −log2(learning rate).
3. Forecast from a known point: C = C_0 (Q/Q_0)^−a.

Illustration: 15% drop per doubling → learning rate 0.85, a = 0.234. From
$50 at 1,000 units, at 8,000 units (three doublings): 50 × 0.85³ = $30.71.

Constant-elasticity demand Q = A P^{−E} is a power model: see pricing.md.

## Pitfalls

- MA order different from the cycle.
- Reading b as the % change.
- Experience-curve C is the cost of the next unit, not the average cost.
- Successive observations depend on each other; these models describe a
  trend, not independent samples, so do not apply independent-sample tests.

## Write-up lines

- "Sales repeat every __ periods, so we use an MA of order __; the smoothed
  series moves about __ per period; the forecast for __ is __."
- "Fitted Y = __·e^{__t}: __% per period."
- "Unit cost falls __% per doubling of cumulative volume; at __ units we
  expect $__."

---

## File: marketing-models/references/logit.md

# Logit: predicting, classifying, ranking

## Binary logit

I = b0 + b1 X1 + ... + bm Xm; P(Y=1) = 1/(1 + e^{−I}); odds R = e^I;
P(Y=1) = R/(R + 1).

| I | P(Y=1) | R |
|---|---|---|
| 0 | 0.5 | 1 |
| > 0 | > 0.5 | > 1 |
| < 0 | < 0.5 | < 1 |

- Fitted by maximum likelihood; rows must be independent cases.
- Naive model: b0 = ln(p/(1 − p)), p = sample share of Y = 1.
- Two cases have the same probability iff they have the same I. Trade-off
  between predictors: Δ X1 equivalent to a dummy = b_dummy / b1.
- b_j changes log-odds by b_j; odds multiply by e^{b_j}. Several changes:
  R' = R · e^{Σ ΔX_j b_j}. The probability change depends on the starting
  point (S-curve), so never read b_j as a probability change.
- Logit separates cases better at the extremes; probit around the mean.

### Testing

Software reports deviance = −2 ln L (null deviance = naive model).

LR = deviance_restricted − deviance_full (always ≥ 0), compare with
χ²_α(k), k = coefficients set to 0. Whole model vs naive: use the null
deviance, k = m. ln L is not comparable across samples of different size;
use LR tests or lift.

## Classifying a case: the cost rule

1. Say in words what "assign to 1" and "assign to 0" mean as actions
   (send the offer / do not; call the lead / skip).
2. Costs: C(1|0) = cost of acting on a case that is truly 0; C(0|1) = cost
   of not acting on a case that is truly 1.
3. Assign 1 iff P(Y=0)·C(1|0) ≤ P(Y=1)·C(0|1), equivalently R ≥ c with
   c = C(1|0)/C(0|1), equivalently P(Y=1) ≥ c/(1 + c).
4. Sensitivity: the most a wrong "1" can cost and still justify acting is
   C(1|0) ≤ R·C(0|1).

A default 0.5 cut-off assumes the two errors cost the same. A cheap action
against an expensive miss pushes the threshold far below 0.5.

Illustration: retention credit $10; a churner who would be saved by it is
worth $90 of margin. c = 10/90 = 0.111; threshold P ≥ 0.111/1.111 = 0.10.
Every customer above a 10% churn probability gets the credit, not only those
above 50%. If the credit saves only some churners, C(0|1) is the expected
margin saved (save rate × margin).

## Is the model good enough to target with: the lift curve

1. Score every case (Î), sort from highest to lowest.
2. At each rank i: n1 = actual 1s among the top i; n2 = i × base rate (random
   picking).
3. Plot both. The ideal curve rises with slope 1 until all positives are in,
   then is flat. The closer n1 sits to it, and the farther above n2, the more
   the model is worth for targeting.

Report: "In the top __ ranked cases the model finds __ actual positives vs
__ by chance."

## Multinomial logit (more than two outcomes)

- Base outcome I_1 = 0; one indicator per other outcome with its own
  coefficients.
- P_1 = 1/(1 + Σ_{k≥2} e^{I_k}); P_j = e^{I_j}/(1 + Σ_{k≥2} e^{I_k}).
- Typical use: predicted brand shares by segment (evaluate each segment
  profile). Keep the minus signs in the exponents.
- "Does variable Z matter at all?": all of Z's coefficients across the
  non-base equations are 0, LR test with k = number of outcomes − 1.

## Pitfalls

- Assigning by P > 0.5 by default.
- Reading b as a probability change.
- LR statistic with the sign flipped.
- Repeated rows for related people (dependent observations).

---

## File: marketing-models/references/pricing.md

# Pricing from elasticity

## Inputs

| Input | Symbol | Note |
|---|---|---|
| Price | P | |
| Units at that price | Q | |
| Unit variable cost | VC | From margin: VC = P (1 − margin%/100) |
| Fixed cost | FC | Affects the profit level, never P* |
| Elasticity | ε < 0, E = abs(ε) | |

Profit = (P − VC) Q − FC.

## Steps

1. **Elasticity.** Two points: ε = (ΔQ/Q)/(ΔP/P). A series: regress ln Q on
   ln P; the slope is ε, the intercept indicates baseline demand (higher
   intercept and lower E across brands = premium positioning).
2. **PV ratio.** PV = (P − VC)/P. 1/PV = % gain in unit margin from a 1%
   price rise.
3. **Compare 1/PV with E.** This is profit's first-order test and does not
   depend on the shape of demand.

| Condition | A 1% price rise | Diagnosis | Move |
|---|---|---|---|
| 1/PV < E | margin gain < volume loss | overpriced | cut |
| 1/PV > E | margin gain > volume loss | underpriced | raise |
| 1/PV = E (E > 1) | no first-order change | optimal | hold |
| E < 1 | 1/PV > 1 > E always | underpriced | raise |

4. **Optimum.** Constant elasticity (E constant, E > 1): P* = VC·E/(E − 1),
   markup on VC = 1/(E − 1). Linear demand Q = A − BP: P* = A/(2B) + VC/2.
   With E ≤ 1 under constant elasticity there is no finite optimum.

## The trap: elastic is not "do not raise"

E > 1 means revenue falls when price rises. Profit can still rise, because
each unit keeps more margin. Decide on 1/PV vs E, or directly on
contribution (P − VC)·Q at each tested price.

Illustration: P = $20, VC = $15, E = 2.5. Revenue falls with a price rise
(E > 1), but 1/PV = 20/5 = 4 > 2.5: underpriced, raise.

## The second trap: jumping to P*

The 1/PV vs E test is local (about a 1% move). E measured between two nearby
prices says little about prices far away. If the formula P* lands far
outside the prices observed, do not recommend it: move one step in the right
direction, measure E again, and repeat. Recompute E after any large change
unless demand is known to be constant-elasticity.

## Measuring E

E must come from comparable conditions: a randomised price test, or price
variation not driven by promotions, season or competitor moves. Whether a
price test is valid (sample ratio, significance, novelty) is evidence-check's
job; run it there before trusting E.

## Write-up lines

- "A 1% price increase is associated with a __% fall in units (E = __)."
- "At P = $__ and VC = $__, 1/PV = __. Since 1/PV [> / <] E, the price is
  [too low / too high]; [raising / cutting] it raises contribution."
- "Recommended step: $__ → $__, then re-measure E."

---

## File: marketing-models/references/regression.md

# Regression, correlation and chi-square

## Correlation

- r in [−1, 1] measures linear association only. r = 0 rules out a straight
  line, not every relationship; independence implies r = 0, not the reverse.
- r² = R² only with one predictor. With several: R² ≥ the largest r²; R² =
  Σ r² only if the predictors are mutually uncorrelated.

## Linear regression

Use when Y is continuous and you need several X at once (quantitative,
dummies, interactions). Omitting a variable that moves with X and affects Y
biases the coefficients: that is why simple becomes multiple regression.

Assumptions: errors normal with mean 0; no serial correlation; errors
uncorrelated with the X; no multicollinearity (remedy: factor scores, see
segmenting.md).

### Read in this order

1. **F-test** vs the naive model Ŷ = mean(Y). Not significant: stop, the
   model explains nothing.
2. **R² = 1 − SSE/SST**: the share of the naive model's error removed.
3. **Coefficients**: sign, size, p-value. p > 0.05: "no evidence of a
   relationship, controlling for the rest", not "no effect".

### Dummies and interactions

| Model | Picture | Meaning |
|---|---|---|
| Y = b0 + b1 D | two flat lines | b1 = difference in group averages |
| + b2 X | two parallel lines | common slope b2 |
| + b3 X·D | two lines, different slopes | slope b2 (base), b2 + b3 (D = 1) |

- A categorical variable with c levels gets c − 1 dummies (c dummies are
  perfectly collinear with the intercept).
- Write each group's intercept and slope out before interpreting.
- In an interaction model the main coefficient is the base group's effect
  only. A non-significant main effect does not mean "no effect anywhere".

### Joint hypotheses: partial F

Fit the full model (m coefficients besides the intercept) and the restricted
model (k tested coefficients set to 0).

F = [(R²_full − R²_res)/(1 − R²_full)] · (n − m − 1)/k, compare with
F_α(k, n − m − 1).

Translate business questions into coefficient restrictions first, for
example "the price effect is the same at every advertising level" =
"all price × advertising-level interaction coefficients are 0".

### Choosing between models

- R² never falls when a variable is added, useful or not. Never pick a model
  on raw R².
- Use adjusted R² = 1 − (1 − R²)(n − 1)/(n − m − 1), or a significant
  partial F on the added block.
- Compare only models with the same dependent variable.

Illustration: n = 60. Small model m = 2, R² = 0.50; large model m = 7,
R² = 0.53. Partial F = (0.03/0.47)·(52/5) = 0.66, far below F_0.05(5, 52)
≈ 2.4. Adjusted R²: small 0.482, large 0.467. Keep the small model.

### Pitfalls

- Duplicated rows inflate n and fake significance.
- Reading a dummy as "a one-point increase".
- Picking models on R².

## Chi-square test of independence

For two categorical variables in a cross-tab.

1. H0: no relationship (every row has the same % breakdown).
2. E_ij = row_i total × col_j total / n.
3. Validity: every E ≥ 1 and at least 80% of cells E ≥ 5. Otherwise merge
   neighbouring categories that belong together (keep ≥ 2 x 2) and redo.
4. χ² = Σ (O − E)²/E; df = (R − 1)(C − 1); reject if χ² > χ²_α(df).
   Critical values: df 1: 3.84 (5%), 6.63 (1%); df 2: 5.99, 9.21; df 3: 7.81,
   11.34.
5. Equal proportions across groups (binary outcome) is the same test on an
   R x 2 table.

Reading:
- Rejected at 5% but not 1%: 0.01 < p < 0.05.
- Significance depends on n: doubling every count doubles χ² with identical
  proportions. Report the proportions, not only the p-value.
- Not significant = no evidence, not proof of independence.
- Two variables only. For several predictors at once, use logit.

---

## File: marketing-models/references/segmenting.md

# Segmenting: factor analysis, then K-means

## When

- Many correlated ratings per respondent (importance of features, Likert
  items) and you want a few interpretable dimensions.
- You want groups of customers with similar needs (benefit segments).
- A regression has multicollinearity: replace correlated regressors with
  uncorrelated factor scores.
- Checking whether a Likert summated scale is valid (one dominant factor =
  unidimensional attitude, the scale is fine).

## Factor analysis

1. Run on the m items.
2. Keep factors with eigenvalue ≥ 1 (each explains at least one item's worth
   of variance). Eigenvalues sum to m; share explained = Σ kept / m.
3. Rotate with varimax so each item loads clearly high or low on each factor.
4. Name each factor from items with abs(loading) ≥ 0.5 and their signs.
   Loading = correlation of item and factor.
5. Communality of an item = Σ squared loadings on kept factors = R² of the
   item on the factors. Low communality: the factors miss that item.
6. Save factor scores: mean 0, variance 1, uncorrelated.

## K-means on factor scores

1. Pick K; start from K random points; assign each respondent to the nearest
   centroid (Euclidean); recompute centroids; repeat until no change.
2. Total WCSS = Σ over clusters of squared distances to the centroid. It
   always falls as K rises; choose K at the elbow, where it stops falling
   sharply.
3. K-means is a heuristic that depends on the start: rerun with several
   starts before trusting one solution.

## Profiling

Read the cluster-means table (clusters x factors). Factor scores are
standardised: > 0 above average, < 0 below, 0 = average (not "none"). Mark
each cluster's highest and lowest factors, name the segment, give its size.

To explain original (often yes/no) items by the factors, regress (or logit)
each item on the factor scores and read significance and sign.

Conjoint route: cluster respondents on their individual part-worths; each
cluster's most important attribute is the one with the largest part-worth
range (see research-design, measures.md).

## Pitfalls

- Keeping factors with eigenvalue < 1.
- Naming factors from unrotated loadings.
- K-means on raw correlated items (near-duplicate items get double weight).
- Choosing K without the elbow, or trusting one run.

---

## File: marketing-models/references/valuing.md

# Valuing investments and customers: NPV, IRR, CLV

Metric definitions of CLV, CLV:CAC and payback live in metric-definitions
(catalog "Customer value"). This file covers the decision method.

## NPV

Put alternatives whose payoffs arrive at different times on one basis:
today's money.

1. List periods t and cash flows V_t (outflows negative). Say whether the
   investment sits at t = 0 or t = 1.
2. Discount factor 1/(1 + I)^t; keep 4+ decimals (rounded factors drift on
   large flows).
3. NPV = Σ V_t/(1 + I)^t. Invest iff NPV ≥ 0; between options, highest NPV.

## IRR

The compound rate at which NPV = 0: the highest rate at which the investment
still breaks even.

- Check existence first: the first flow is the outflow, later flows are
  inflows, and the inflows add up to more than the outflow. If the inflows
  sum to less, NPV is negative at every non-negative rate: no positive IRR,
  report NPV only.
- Solve numerically (bisection or a spreadsheet goal seek).

## CLV: NPV with churn risk

A customer's future margin arrives only if the customer is still active.

| Term | Meaning |
|---|---|
| R | retention: probability an active customer is active next period |
| R^t | survival to period t |
| V_t R^t | expected cash flow in t |
| ρ = (1 + I − R)/R | discount rate that adds churn risk to the time value of money; ρ = I when R = 1 |

CLV = Σ V_t R^t/(1 + I)^t − AQ = Σ V_t/(1 + ρ)^t − AQ.

Pitfalls:
- Discounting V_t R^t at ρ counts churn twice. Use one form.
- V_t must be margin (contribution), not revenue.
- AQ sits at t = 0 and is outside the sum.

Decision thresholds:

| Question | Answer |
|---|---|
| Most we can pay to acquire | AQ_max = Σ V_t R^t/(1 + I)^t (CLV = 0) |
| Is acquiring worth it | ρ < IRR of (−AQ, V_1..V_T): yes; ρ = IRR: indifferent; ρ > IRR: no |
| Minimum retention | R_min = (1 + I)/(1 + IRR) |

Levers (each ceteris paribus): higher AQ or higher I lower CLV; higher R
raises it.

### Worked method (illustrative numbers)

Margin $60 a year while active, R = 0.8, I = 0.05, 3-year horizon.
ρ = (1.05 − 0.8)/0.8 = 0.3125.
PVs: 60/1.3125 = 45.71; 60/1.3125² = 34.83; 60/1.3125³ = 26.54. Sum = 107.08.
AQ_max ≈ $107. At AQ = $90, CLV = $17; IRR of (−90, 60, 60, 60) ≈ 44.6%,
so R_min = 1.05/1.446 ≈ 0.726. Current R = 0.8 clears it.

## Write-up lines

- "At I = __, the NPV is $__; [invest / do not invest]."
- "With retention __ and rate __, ρ = __; future margin is worth $__, so
  acquisition can cost at most $__."
- "IRR of the customer's flows is __%; the investment holds for retention of
  at least (1 + I)/(1 + IRR) = __."
