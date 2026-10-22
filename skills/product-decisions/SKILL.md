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
