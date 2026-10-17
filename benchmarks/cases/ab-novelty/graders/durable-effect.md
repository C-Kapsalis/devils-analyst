---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (computed from ab_daily.csv; conversion rate = conversions / users):
- Pooled over all 4 weeks, B shows a +9.5% relative lift (A 4.81% vs B 5.27%, z=3.8, p=0.0001). This pooled number is what a naive analysis reports as "B wins".
- But the lift decays week by week: week 1 +23.9% (p=2.5e-06), week 2 +11.5% (p=0.023), week 3 +2.1% (p=0.66), week 4 +0.8% (p=0.87).
- In weeks 3-4 combined (15-28 Sep) the lift is +1.5% (z=0.43, p=0.67): no detectable effect. The early lift was a novelty effect among returning users (week 1 +32.0%, week 2 +14.8%, week 3 +5.0%, week 4 +3.2%); new users show -3.0% (p=0.55) over the whole test.

Naive answer: "B wins with a ~10% significant lift; roll it out" without looking at the trend over time.

PASS if report.md shows that the lift shrinks over the test (week-by-week or early-vs-late split) AND states that in the later period (weeks 3-4, or week 4, or the last two weeks) the lift is about zero / not statistically significant (a reported late-period lift within +1.5% +/- 3 percentage points of relative lift is fine), AND concludes the effect is not durable (novelty / wears off / no lasting lift).
FAIL if report.md presents the pooled ~10% lift as the effect of B without identifying the decay to ~0 in the later weeks, or if it never looks at the result over time.
