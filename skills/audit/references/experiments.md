# Experiments and lift studies

The full tests (sample ratio chi-square, two-proportion z, power, novelty,
interaction) are in `evidence-check`. This list is what an audit of a testing
program looks for.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| X1 | Users per arm vs the planned split | Chi-square on assignment counts above 10.8 (p < 0.001) | Assignment or logging broken; results unreadable | Find the cause before reading outcomes | 1 |
| X2 | Null hypothesis vs the cost of the change | Lift tested against zero when the change has a cost | A lift can beat zero and still not pay | Convert the cost to a break-even lift; test against it | 1 |
| X3 | Duration | Under 7 days or partial weeks | Day-of-week effects | Whole weeks, usually 1-2 | 1 |
| X4 | Pre-registered minimum detectable effect and sample size | None; stopped when it "looked significant" | Noise wins shipped | Size before launch | 2 |
| X5 | Rows vs randomisation units | More rows than unique users, analysed per row | Inflated n fakes significance | Dedupe to the user | 1 |
| X6 | Balance checks | On variables measured after exposure | Treatment can move them | Balance on pre-period variables | 3 |
| X7 | Changes between A and B | Copy, layout and price changed together | Cannot attribute the result | One change, or a factorial design | 3 |
| X8 | Primary metric vs objective | "More orders" goal measured by product clicks | Optimising a proxy | A metric measurable, attributable, sensitive and timely in both arms | 2 |
| X9 | Segment winners | Rollout to a segment from a pivot table with no interaction test | Launching on noise | Interaction test; call it suggestive | 3 |
| X10 | Novelty | Lift concentrated in returning users early | Fades after launch | Split by new vs returning and by week | 3 |
| X11 | Lift study reporting | Raw point gap; no relative lift; no incremental count; cost on treatment impressions only | Misstated payoff | Lift = (T - C) / C; incremental = T conversions - C rate x T users; cost on control plus treatment impressions | 3 |
| X12 | Exposed vs unexposed comparisons | Sold as ad effect | Selection, not effect | Randomised holdout | 5 |
| X13 | Interventions on last month's worst units | Rebound claimed | Regression to the mean | Untreated equally extreme control | 5 |
| X14 | Surprising big lifts | Shipped with no rerun | A figure that looks too interesting is usually wrong | Replicate | 3 |
| X15 | A/A tests on new tooling | Never run | Unknown bias | Run periodically | 4 |
| X16 | Brand-lift pre-waves | Pre-wave names the brand | Sensitises only the exposed group | After-only design with a randomised control | 3 |

## Decoys

A 49.9 / 50.1 split; a non-significant result reported as "no evidence at
this confidence" (correct wording); tests of 14 days.
