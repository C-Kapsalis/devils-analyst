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
