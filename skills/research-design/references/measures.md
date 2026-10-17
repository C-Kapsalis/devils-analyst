# Customer measures and their traps

## Scale levels

| Level | Meaning | Allowed |
|---|---|---|
| Nominal | categories only | counts, mode, cross-tabs, chi-square; dummies in regression; Y in logit |
| Ordinal | order, gaps not comparable (ranks, ordered ranges) | + median, percentiles |
| Interval | equal units, no true zero | + mean, SD, correlation, regression |
| Ratio | equal units and a true zero | + ratios and % changes |

Rating scales with many points approximate interval well enough for means;
few ordered categories do not. Reliability = free of random error; validity =
free of random error and bias. A reliable measure can be consistently wrong.

## Awareness

| Measure | Question | Note |
|---|---|---|
| Top-of-mind | First brand named, no brand mentioned | Strictest |
| Unaided recall | Any brand named, no prompt | |
| Aided (recognition) | "Have you heard of X?" | Easiest; crowds near the ceiling, so it cannot separate strong brands |

- Record per respondent as 0/1; report the share of the sample, always with
  the measure named. "40% awareness" alone means nothing.
- Ask unaided first, then aided. Never let an earlier question or the cover
  note name the brand.
- A large aided-minus-unaided gap = known but not salient.
- Plant a fictitious brand in aided lists; its "yes" rate measures false
  recognition.
- Aided recall asked before a campaign sensitises respondents: see design.md.

## Attitude and feature importance

| Involvement | Tool |
|---|---|
| Low: product seen as a whole | One simple rating per object |
| High, emotional | Likert summated scale; valid if factor analysis of the items shows one dominant factor |
| High, rational | Semantic differential with importance weights, or conjoint |

Rating-scale choice by how finely respondents can distinguish: unfamiliar
respondents → itemized (about 5 categories); very familiar → graphic; able to
compare absolute sizes → constant sum (avoids the compression a low
reference causes in fractionation); rank order only if they use the same
criterion for every comparison.

Importance weights:
- Stated ("how important is...") underrates must-have attributes that people
  take for granted.
- Derived by regression of overall rating on attribute ratings pools everyone
  into one set of weights and assumes linear effects.
- Conjoint fixes both.

## Conjoint

1. Attributes that drive choice and that you control; 2 to 4 levels each,
   always including the extremes of the feasible range.
2. Hypothetical profiles from an orthogonal design (each level appears
   equally often and independently, e.g. a Latin square for 3 attributes of
   equal levels); add all-best and all-worst anchors, drop them before
   fitting.
3. Ask only an overall rating per profile.
4. Fit one dummy-coded regression per respondent (needs clearly more ratings
   than parameters). Part-worth = 0 at each attribute's lowest level.
5. Outputs: ideal profile (best level of each); importance_i = range_i/Σ
   ranges; share simulation (each respondent picks the highest-utility
   option, share = fraction choosing it, needs a sample representative of the
   market); benefit segments (cluster on part-worths).
6. Interpolate part-worths linearly between studied levels; never evaluate a
   level outside the studied range.

## Purchase intention

- Use it when there is no purchase history: new concepts, durables, rare
  purchases. Otherwise use actual usage data.
- Stated intent overstates purchase, and the errors do not cancel in
  aggregate. Never feed top-two-box or raw "yes" into a volume forecast:
  deflate with factors calibrated on past launches, or use a 0 to 10
  probability scale and average the probabilities; validate per category.
- Interest questions also carry politeness bias (questionnaire.md, B).

## Share, switching, loyalty

- Market share: state units or revenue (revenue share above unit share = a
  price premium) and served or total market (same numerator, different
  denominator).
- Share = penetration share × share of requirements × usage index: low
  penetration is a reach problem, low share of requirements a loyalty
  problem.
- Brand-switching matrix (needs the same buyers on two occasions, i.e. a
  panel): rows = first purchase, columns = next. X and Y do not compete only
  if both xy and yx are 0. Loyalty = diagonal / row total.
- Repeat rate rises with brand size; compare a brand's loyalty with what a
  brand of its size usually shows before crediting the brand team.
- Behavioural loyalty (repeat, share of wallet) and attitudinal loyalty
  (stated preference, recommend scores) often disagree; name which you report.

## Media habits

Reach = unique people exposed at least once; frequency = impressions/reach;
GRP = reach % × frequency. Channel reaches cannot be summed (people overlap).
See metric-definitions for the metric formulas.
