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
