# Skill: whats-changed

---
name: whats-changed
description: >-
  Use this skill whenever a marketing number went up or down between two periods and you
  are about to explain why: it splits the change into drivers (sessions x conversion rate
  x order value), into mix versus rate for any percentage (did CTR fall, or did the
  audience shift?), and into contributions by channel, campaign or segment, and screens
  out noise. Triggers include "why did revenue drop", "what changed", month-over-month or
  week-over-week comparisons, and any report or dashboard that compares periods.
---

# whats-changed

The LLM narrates; the arithmetic decides. Before you write "revenue fell
because of paid social", the decomposition has to say so, with numbers that add
up to the change you are explaining.

## 1. Fix the comparison first

A wrong comparison makes every insight after it wrong.

- **Same length, same weekdays.** Week over week compares Monday-Sunday with
  Monday-Sunday. Month over month on daily data: compare equal day counts, or
  say the months differ in length.
- **Complete periods only.** Drop today. Drop the last 2-3 days of Search
  Console (it lags). Drop the conversion window still open for ad platforms
  (Google Ads keeps adding conversions for days after a click). Say what you
  dropped.
- **Seasonality.** If the business is seasonal or the period holds a promotion
  or holiday, add the same period last year as a second comparison and say which
  one the conclusion rests on.
- State the comparison in the dashboard subtitle: "Mar 1-31 vs Feb 1-28, 2025".

## 2. Pick the decomposition that matches the metric

| Metric shape | Example | Method |
|---|---|---|
| A sum | Revenue, sessions, spend, clicks | **Contribution**: change per channel / campaign / segment, as a share of the total change |
| A ratio | CTR, CVR, CPA, ROAS, open rate, CAC | **Mix vs rate** across the segments: did the rates inside segments move, or did the volume shift between segments? |
| A product of drivers | Revenue = sessions x CVR x AOV; email revenue = delivered x CTR x click-to-order x AOV | **Driver tree** (log decomposition): how much of the change each driver explains |

Most good answers use two: a driver tree for the headline number, then mix vs
rate or contribution on the driver that moved most. Formulas, edge cases and a
fully worked example are in section "File: whats-changed/references/decomposition.md" in 02-whats-changed-and-evidence.md.
Read it before computing; the formulas there are exact (the parts add up to the
change) and the naive alternatives are not.

## 3. Compute, then check it adds up

Compute in code (the analysis tool, a SQL query, or Python), never in your
head. Then check:

- contributions sum to the total change (to rounding);
- every rate you report has its volume beside it;
- each segment's change is tested against noise (section 4 of the reference).
  A change inside the noise band is reported as "no clear change", not as a
  finding.

## 4. Write the insight

Write by the `marketing-dashboard` skill's `references/writing.md`: answer first, one point per paragraph, plain words.

One finding per sentence. Number first, driver second, interpretation last, and
label interpretation as a hypothesis when the data cannot prove it.

> Account CTR rose 0.64 points to 4.6%, but 0.59 of those points are mix: a
> brand campaign (22% CTR) took a larger share of impressions. Within
> campaigns, only Shopping improved (+1.3 points, beyond noise). Generic search
> CTR dipped 0.4 points, which is within noise at this volume.

Not: "CTR improved thanks to better ads." Ad copy was not measured.

**Opens are a weak driver.** Privacy features and image prefetching fire
opens nobody made, so an open rate can move with no change in people. When a
driver tree or a cause runs through opens, say so beside the number ("opens,
inflated by privacy proxies, directional only"), prefer clicks per delivered
as the engagement step, and never make an open rate the metric an action is
verified on: verify on clicks, orders or revenue.

**A written report shows the arithmetic, not only the story.** Before the
findings, include the decomposition as a small table whose rows add up to the
headline change, with the check stated:

| Driver of revenue change (Mar to Apr) | Amount |
|---|---|
| Sessions | +$4,120 |
| Conversion rate | -$7,860 |
| Order value | +$1,340 |
| New channel (affiliates) | +$5,600 |
| **Total change** | **+$3,200** (= $61,700 - $58,500) |

For a rate, add the mix-vs-rate split as its own line: "CVR -0.20 pts =
+0.15 pts mix + (-0.35) pts within channels". A report that lists
before-and-after figures per segment without these two pieces has not
explained the change; it has described it.

## 5. In a dashboard

In a Claude Dashboard the decomposition is a dataset or a calculation, not text:
the mix-vs-rate and driver-bridge SQL in the `marketing-dashboard` skill's
`references/claude-dashboards.md` runs live, so the explanation refreshes with
the data and every number in it can be clicked. Elsewhere:


- Put the decomposition next to the headline it explains: a waterfall (bridge)
  from last period's value to this period's, one bar per driver or segment.
- Rates: a two-bar "mix" vs "rate" split, then the segments sorted by their
  contribution.
- Mark changes inside the noise band in a muted color, and say so in the legend.
- Hand the largest real movement to the `diagnose` skill for the likely cause
  and the next action.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Fix the comparison | "Are the periods equal and complete, and is seasonality in play?" | same length and weekdays; no open conversion window; last year's period if seasonal | change the comparison or state the limit |
| Decompose | "Do the parts add up to the change, exactly?" | sum of contributions = total change (to rounding) | use the exact method in the reference |
| Mix vs rate | "Did the audience shift, so a blended rate moved with no behaviour change?" | mix share vs within-segment share computed | lead with whichever dominates |
| Screen noise | "Would this change appear by chance at this volume?" | noise band per segment | report "no clear change" |
| Write the insight | "Is the interpretation proven, or a story?" | each cause tied to a measured driver | label it a hypothesis and say how to test it |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.

---

## File: whats-changed/references/decomposition.md

# Decomposition reference

Three methods, each exact: the parts add up to the change being explained.
Period 0 is the comparison period, period 1 the current one.

## 1. Contribution (sums)

For a total T = sum of T_i over segments i:

```
contribution_i  = T_i1 - T_i0
share_i         = contribution_i / (T_1 - T_0)
```

Shares can exceed 100% or be negative when segments move in opposite
directions; that is information, not an error. Report the top movers both ways
(largest gain, largest loss). If the total barely moved, do not report shares
(dividing by a near-zero change); report the absolute contributions.

## 2. Mix vs rate (ratios)

Any rate R = N / D (CTR = clicks / delivered, CVR = conversions / sessions,
CPA = spend / conversions) is a weighted average of segment rates:

```
R  = sum_i  w_i * r_i        where  w_i = D_i / D   and   r_i = N_i / D_i
```

So R can change because segment rates changed (**rate effect**) or because the
volume moved between segments with different rates (**mix effect**). The exact,
symmetric split, per segment:

```
R_bar   = (R_0 + R_1) / 2
r_bar_i = (r_i0 + r_i1) / 2
w_bar_i = (w_i0 + w_i1) / 2

rate_i  = (r_i1 - r_i0) * w_bar_i
mix_i   = (w_i1 - w_i0) * (r_bar_i - R_bar)

sum_i (rate_i + mix_i) = R_1 - R_0        (exact)
```

`mix_i` is positive when volume shifts toward a segment that converts above
average, negative when it shifts toward one below average.

**Segments that appear or disappear.** A segment with no volume in one period
has no rate there. Set its missing rate equal to its other-period rate, so all
of its effect is mix. Say so: "the new VIP segment adds 0.56 points of mix".

**Never average segment rates.** The average of 3.6% and 5.1% is not the
combined CTR. Always recompute R from summed numerators and denominators.

## 3. Driver tree (products)

When a metric is a product of drivers, M = d_1 x d_2 x ... x d_k, use the log
(LMDI) split:

```
L          = (M_1 - M_0) / ln(M_1 / M_0)           (logarithmic mean)
contrib_j  = L * ln(d_j1 / d_j0)
sum_j contrib_j = M_1 - M_0                         (exact)
```

Requirements: every driver positive in both periods. If M_1 = M_0, report each
driver's percent change instead (L is undefined).

Common marketing driver trees (check the identity holds on the data before
using it; if the product does not reproduce the metric, a definition is off):

| Metric | Drivers |
|---|---|
| E-commerce revenue | sessions x conversion rate x average order value |
| Email revenue | delivered x CTR x click-to-order x average order value |
| Paid conversions | spend / CPC x CVR (= clicks x CVR) |
| Paid revenue | spend x ROAS |
| Organic clicks (GSC) | impressions x CTR |
| Pipeline (CRM) | leads x lead-to-opportunity rate x average deal size |
| New customers | sessions x new-visitor share x new-visitor conversion rate |

## 4. Noise

A rate measured on a small denominator moves a lot by chance. For a proportion
p measured on n (clicks / delivered, conversions / sessions):

```
SE(p)            = sqrt( p * (1 - p) / n )
change is clear  if  |p_1 - p_0|  >  2 * sqrt( SE_0^2 + SE_1^2 )
```

This is a screen, not a test: it assumes independent trials, which email and
web data only approximate. Use it to keep noise out of the headline, not to
claim significance. For sums (revenue, sessions), compare the change with the
typical week-to-week swing over the last 8 periods; inside that swing, call it
"within normal variation".

Minimum volumes before reporting a rate change for a segment: about 100
conversions-or-clicks in the numerator, or 1,000 in the denominator. Below
that, fold the segment into "Other".

## 5. Worked example (email)

Previous period: Newsletter 14,000 delivered / 504 clicks (3.6%), Active 5,000 /
255 (5.1%), no VIP send. Current: Newsletter 14,500 / 464 (3.2%), Active 5,300 /
339 (6.4%), VIP 850 / 153 (18.0%).

Overall CTR: 759 / 19,000 = 3.99% to 956 / 20,650 = 4.63%, **+0.635 points**.

| Segment | Weight | CTR | Mix (pts) | Rate (pts) | Total (pts) |
|---|---|---|---|---|---|
| Newsletter | 0.737 to 0.702 | 3.6% to 3.2% | +0.032 | -0.288 | -0.256 |
| Active | 0.263 to 0.257 | 5.1% to 6.4% | -0.009 | +0.337 | +0.328 |
| VIP (new) | 0 to 0.041 | 18.0% | +0.563 | 0 | +0.563 |
| **Total** | | | **+0.586** | **+0.049** | **+0.635** |

Noise screen: Newsletter changed -0.40 points against a 2 x SE band of 0.43
points, so it is not a clear change. Active changed +1.30 points against 0.92,
so it is clear.

Insight: "CTR rose 0.64 points, almost all of it mix from the new VIP send.
Like for like, only Active customers clicked more."

Driver tree for revenue on the same sends: delivered 19,000 to 20,650, CTR
4.0% to 4.6%, click-to-order 12% to 10%, AOV $37 to $41. Revenue $3,374 to
$3,895, **+$520**:

| Driver | Change | Contribution |
|---|---|---|
| Delivered | +8.7% | +$302 |
| CTR | +15% | +$507 |
| Click to order | -17% | -$662 |
| AOV | +11% | +$372 |
| **Total** | | **+$520** |

Insight: "Revenue grew $520, but click-to-order fell from 12% to 10% and cost
$662. More people clicked; fewer of them bought. Check the landing page and the
offer before sending more traffic." Then hand "click-to-order declining" to the
`diagnose` skill.

---

# Skill: evidence-check

---
name: evidence-check
description: >-
  Use this skill before you say that something worked, won, caused, or should be scaled,
  cut or repeated: A/B and subject-line test results, "did B win", "should we roll it
  out", before/after a change (new ads, faster pages, a redesign), a promotion or sale,
  a holdout or lift study, a brand-search pause, ROAS that looks great, "which channel
  contributes least" or budget cuts across channels, "what makes our posts perform",
  "which landing page converts better", and any traffic drop someone wants blamed on
  SEO or a team. It checks the evidence (sample ratio, significance and power, novelty,
  control groups, seasonality, regression to the mean, Simpson's paradox, confounders,
  incrementality, pull-forward, category-wide shifts, attribution model) and says what
  the data can and cannot support.
---

# evidence-check

A correct number can still support the wrong decision. Before a verdict
("B won", "the rewrite worked", "double the budget", "cut YouTube", "SEO
broke"), run the checks that apply. Compute each in code. Write the verdict as
supported, not supported, or inconclusive, with the number that decides it.

## 1. A/B tests

Run these in order; stop at the first that fails.

1. **Sample ratio.** Compare observed users per arm with the planned split
   (chi-square goodness of fit, 1 degree of freedom for two arms:
   `sum((obs - exp)^2 / exp)`; above 10.8 means p < 0.001). A mismatch means
   assignment or logging is broken: the result cannot be trusted, whatever its
   p-value. Investigate before shipping.
2. **Significance.** Two-proportion z-test on conversions per user:
   `p = (x1 + x2) / (n1 + n2)`, `se = sqrt(p(1-p)(1/n1 + 1/n2))`,
   `z = (p2 - p1) / se`, two-sided p-value `= erfc(|z| / sqrt(2))`. 95%
   confidence interval for the difference: `(p2 - p1) ± 1.96 *
   sqrt(p1(1-p1)/n1 + p2(1-p2)/n2)`. Report the lift with its p-value and its
   interval, not the lift alone. Judge a finished test on these two numbers:
   - **Significant** (p below the planned alpha, interval excludes zero): the
     effect is real at that confidence. If it is smaller than the MDE the test
     was planned for, it is still significant, but a small test that only
     just cleared the bar tends to overstate the effect (the winner's curse).
     Report it with its interval and project revenue from the low end, not
     the point estimate.
   - **Not significant**: inconclusive, unless the interval is narrow enough
     to rule out every effect that would matter to the business; then say
     "no effect large enough to matter". Never say "no effect" on its own.
3. **Power (planning).** The minimum detectable effect (MDE) is set before
   the test, to size it; it is not a pass mark for the result. At 80% power,
   5% two-sided: `mde ≈ 2.8 * sqrt(2 p (1-p) / n)` per arm (absolute). Users
   needed per arm to detect an absolute lift `d`: `n ≈ 16 p (1-p) / d^2`. Use
   it to say whether the test was big enough to find the effect that matters,
   and, for an inconclusive test, how many users a real answer needs.
4. **Novelty.** Split the lift by week, and by new vs returning users. If the
   lift is concentrated in the first week(s) and in returning users and fades
   later, judge on the last stable weeks only.
5. **Segments.** A winner should hold within the main segments (device, new vs
   returning). Many segment cuts will produce one "significant" result by
   chance; do not report it as a finding.

## 2. Before and after a change

A before/after difference is not an effect until a comparison rules out what
would have happened anyway:

- **Control group.** Compare with comparable units that were not changed
  (difference in differences: change in treated minus change in control).
- **Regression to the mean.** Units chosen for being the worst (or best) last
  period improve (or worsen) on their own. Compare with untouched units chosen
  by the same rule in the same week.
- **Seasonality.** If the window crosses a holiday, a sale or a season, compare
  with the same window last year (ratio of this year's post/pre to last year's).
- **Category vs you.** Before blaming SEO, brand or a team for a drop, compare
  with category demand or competitors over the same period. If everyone fell
  by the same share, your share is flat: it is a demand change, not a failure.

## 3. Comparing groups with different mixes

- **Simpson's paradox.** When two pages, campaigns or channels have different
  device, country or audience mixes, compare rates within each segment and at a
  common mix (weight each segment's rate by the combined traffic) before naming
  a winner. The blended rate can rank them backwards.
- **Confounders in observational data.** "Posts with more hashtags engage
  more" may only mean videos use more hashtags. Re-check the relationship
  within the obvious grouping (format, channel, audience). If it vanishes, the
  grouping is the driver. Present any remaining pattern as a hypothesis to
  test, not a rule.

## 4. Incrementality: what the spend added

Platform ROAS counts people who would have bought anyway. When the data allows
it, measure what spend *added*:

- **Holdout or lift study.** Incremental conversions = test conversions -
  control conversion rate x test users. Incremental ROAS = incremental
  revenue / spend. Judge profit at margin: incremental revenue x margin -
  spend.
- **Pause tests (brand search).** Compare total clicks and orders (paid +
  organic) with ads on vs paused, adjusted by a control series (non-brand) for
  the trend. Organic usually recovers most paused brand clicks; cost per
  incremental order is what matters.
- **Promotions.** Baseline = typical sales before the promotion. Incremental =
  (promo period + the dip after it) minus baseline over the same days: buyers
  pulled forward are not new sales. Judge contribution after discount and cost
  of goods, including the discount given to people who would have bought at
  full price. Lift over a baseline that keeps falling is not a better promotion.
  For the full method (break-even depth, subsidy by new vs returning, baseline
  erosion across promos, price-change stock-up, elasticity with promo
  controls), use the `pricing-promotions` skill.

## 5. Attribution before cutting a channel

- Show credit under at least two models (last click and first touch or
  linear) from the paths when available. A channel with near-zero last-click
  credit that starts many converting paths is not "contributing least".
- GA4 data-driven attribution falls back to last click when conversion volume
  is low (roughly a few hundred per month per conversion type). If the
  "data-driven" column equals last click, say so.
- Do not recommend cutting a channel on attribution alone: propose a holdout.

## 6. Write the verdict

```
Verdict: [supported / not supported / inconclusive]: [claim]
Deciding number: [the check that decides it, e.g. "SRM chi-square 250, p < 0.001"]
What the naive read says and why it is wrong: [one line]
What to do: [action] · How to get a real answer: [test, sample size, data needed]
```

Keep the arithmetic in the report (a short table of the check), so the reader
can redo it.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Call a test | "Is the split what was planned, is the lift beyond chance, and what does the interval rule out?" | SRM, p-value and confidence interval computed; MDE checked against the planned size | verdict inconclusive or untrustworthy; a significant lift below the planned MDE is reported with its interval and a caution |
| Credit a change | "What would have happened anyway?" | a control group, last year, or untouched equally extreme units | difference in differences, or no claim |
| Pick a winner | "Does it win inside each segment and at a common mix?" | per-segment and standardised rates | report the within-segment result |
| Credit spend | "Would these buyers have bought anyway?" | holdout, pause test or baseline | report incremental, not attributed |
| Cut a channel | "Does a second attribution model, or a holdout, agree?" | credit under two models | propose a holdout before cutting |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.
