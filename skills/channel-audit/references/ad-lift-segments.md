# Display, video and ad lift tests: averages and segments

## Display and video

- Display reaches people who are browsing, not searching: its job is
  awareness and demand creation that search later harvests. Pricing leans on
  CPM (awareness), with CPC (traffic) and CPA (performance) options.
- Read display on viewable impressions (Google standard: at least 50% of
  pixels on screen for 1 second for display, 2 seconds for video), reach,
  view-through conversions (saw, did not click, converted within the window)
  and lift. Low CTR is normal.
- Targeting has two axes: who (demographics, affinity = long-term interest,
  in-market = active intent now, life events, custom intent, remarketing)
  and where (placements, contextual keywords, topics = broadest). Personas set
  the combination.
- Remarketing earns the highest CTR and CVR but only recaptures people you
  already reached; it does not discover. Exclude devices whose landing pages
  are not ready.
- Video: CPV = cost per qualifying view.

## The natural-buyer trap

Comparing people who saw the ad with people who did not measures targeting:
platforms aim ads at likely buyers. Only a randomised split of one audience
supplies the counterfactual. In display tests the control sees a neutral PSA,
which proves the control user was reachable.

## Main effect

| Quantity | Formula |
|---|---|
| CVR (user level) | converted users / users, over an impression-based window |
| Lift | (CVR_t - CVR_c) / CVR_c |
| Incremental conversions | conversions_t - CVR_c x users_t |
| Incremental profit | margin per conversion x incremental conversions |
| Ad cost | CPM x impressions / 1,000 (the test bill includes PSA impressions) |
| POAS | (incremental profit - ad cost) / ad cost |

Inference: chi-square on the 2x2 table is valid when n x p and n x (1 - p) are
at least 5 per group. Balance checks: t-tests (numeric) or chi-square
(categorical) on pre-exposure variables such as prior visits, prior
conversions, page depth, age, income; p > 0.05 means no detectable imbalance.
Report the lift as relative ("raised conversion by X%"), with p-value and the
direction.

## Heterogeneous effects

The A/B average is the average treatment effect over the tested audience. It
can hide a strong positive effect in one group and a null or negative effect
in another.

1. Descriptive: pivot users and conversions by the factor (visitor status,
   time of day, day of week, device, gender, exposure count); compute lift per
   level. Where is lift highest; where is it zero or negative? Use lift %,
   not raw point differences, and watch small cells.
2. Formal: logistic regression, conversion (1/0) on treatment, controls
   (impressions, prior visits) and treatment x factor. The interaction's
   p-value answers "does the ad effect differ by this factor". Controls
   reduce noise even in a randomised test.
3. Reading: a significant negative interaction means the ad works less at
   that level. A non-significant interaction means no evidence of a
   difference, even if the pivot looked dramatic; adding the interaction can
   also make the factor's main effect non-significant (variance split
   between terms). The effect at one level is b_treatment + b_interaction;
   test that sum, not just the interaction.
4. Frequency: lift by exposure band typically rises then falls (too few
   exposures unnoticed, too many read as spam or reach people already sold);
   set caps near the peak.

Decision rule: shift or cut spend by segment only on a significant
interaction or a confirmatory follow-up test; otherwise report the segment
pattern as a hypothesis and propose the test.
