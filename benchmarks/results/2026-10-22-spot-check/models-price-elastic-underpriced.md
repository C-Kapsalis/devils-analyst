# models-price-elastic-underpriced

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/marketing-models/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/models-price-elastic-underpriced/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> We sell the Trailhead insulated bottle in our online shop. Last month we ran a price test: half of visitors saw $40 and half saw $44. The daily results are in resources/price_test_daily.csv. Our landed cost is $28 a unit. Demand looks pretty elastic to me. Should we keep $40 or move? Write report.md with your recommendation and the numbers behind it.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `decision` | PASS | PASS | both: move to $44, contribution +16% |
| `no-extrapolation` | PASS | PASS | A: textbook optimum rejected, test $48 next; B: $44 only |

## Arm A answer (with skill)

````markdown
# Trailhead bottle: keep $40 or move?

**Verdict:** Move to $44. At $40 you are underpriced. Demand is price-sensitive (elastic), but profit still rises with the price.

**Deciding number:** Contribution per visitor is $0.707 at $44 against $0.610 at $40, +15.9% (VC = $28). 28 days (2026-09-07 to 2026-10-04); 19,822 visitors at $40 and 19,840 at $44.

**Naive read and why it is wrong:** "Elastic demand, so raising the price hurts." Revenue does fall: revenue per visitor $2.034 to $1.945 (-4.4%); total revenue $40,320 to $38,588. But each unit keeps $16 of margin instead of $12, so profit rises.

**Action:** Set the price to $44 now. Then test one step further ($48) and re-measure; do not jump to a far-off "optimal" price. · **How to verify:** Weekly, track contribution per visitor against $0.61 and conversion against 4.3%. Keep a $44 holdout for a second period, or run a randomised $44 vs $48 split. Revert if contribution per visitor falls below $0.61.

## Inputs (summed)

| Measure | $40 (A) | $44 (B) |
|---|---|---|
| Visitors | 19,822 | 19,840 |
| Orders | 981 | 857 |
| Units | 1,008 | 877 |
| Revenue | $40,320 | $38,588 |
| Conversion | 4.95% | 4.32% |
| Units per visitor | 0.05085 | 0.04420 |
| Revenue per visitor | $2.034 | $1.945 |
| Margin per unit | $12 | $16 |
| Contribution | $12,096 | $14,032 |
| Contribution per visitor | $0.610 | $0.707 |
| PV = (P − 28)/P | 0.300 | 0.364 |
| 1/PV | 3.33 | 2.75 |

Checks: every daily revenue equals units × price. Units per order are about 1.03 in both arms.

## Is the conversion drop real?

Two-proportion z on orders: 4.95% vs 4.32%, z ≈ 2.98, p ≈ 0.003. Gap holds in both halves: days 1–14 A 4.84% vs B 4.25% (-12%); days 15–28 A 5.07% vs B 4.39% (-13%). No novelty fade.

## Elasticity

- Units per visitor change -13.1% for a +10% price move.
- E = 1.31 (base $40); E = 1.47 (midpoint).
- 95% interval, approximate (Poisson on orders; arm A daily order variance 32.4 vs mean 35.0, so no extra overdispersion): about 0.51 to 2.43. "Elastic" is a point estimate; the interval includes 1.

## Decision test: 1/PV against E

- At $40, 1/PV = 3.33 > E: underpriced, raise.
- At $44, 1/PV = 2.75: still above E, so the next step is also up.
- At the top of the interval (E ≈ 2.43), 3.33 still exceeds E. The raise call holds across the interval.

## Why not the textbook optimum

- Constant elasticity P* = VC·E/(E − 1): about $119 (E = 1.31), $88 (E = 1.47).
- Linear demand through the two points: P* ≈ $49.
- All far outside the tested $40–$44 range. The 1/PV test is local; move one step, re-measure, repeat.

## Robustness

- Break-even: B wins if units-per-visitor ratio exceeds 12/16 = 0.75. Observed 0.869; 95% lower bound about 0.79 (approximate); one-sided z ≈ 3.2.
- B stays ahead for any variable cost above $13.40. Higher costs (fees, shipping, returns) favour $44 more.
- Traffic split 19,822 vs 19,840 is consistent with 50/50.

## Assumptions and what flips the decision

- Visitors were randomly assigned. Not verified; confirm with whoever ran the test. Without random assignment, E and the conversion gap are not trustworthy.
- $28 landed cost is treated as the only variable cost. Only a VC below about $13.40 flips the contribution comparison, which is not realistic.
- Contribution per visitor counts only this test window: no repeat purchase, returns or future traffic effects, and no seasonality adjustment (both arms ran in parallel, so day effects cancel).
- The 95% statements use approximations; a daily-level test on contribution per visitor was not run.
````

## Arm B answer (without skill)

````markdown
Recommendation: move to $44. Over 28 days (2026-09-07 to 2026-10-04; the data covers 28 days, not a full month) the $44 arm earned about $1,936 more gross profit (+16%) than $40, despite lower units and revenue. Demand is elastic, but the unit margin rises from $12 to $16 (+33%), which more than covers the 13% unit loss. Watch weekly: $44 stops beating $40 on gross profit only if volume falls below 756 units per 28 days (about 27/day). The test averaged 31/day at $44.

Totals (summed from the daily CSV; revenue = units x price in every row):
- Visitors: $40 = 19,822; $44 = 19,840
- Orders: 981 vs 857 (-124, -12.6%)
- Units: 1,008 vs 877 (-131, -13.0%)
- Conversion (orders/visitors): 4.95% vs 4.32% (-12.7% relative); two-proportion z about 3.0, p about 0.003
- Revenue: $40,320 vs $38,588 (-$1,732, -4.3%)
- Revenue per visitor: $2.03 vs $1.94
- Gross profit at $28 landed cost: $12,096 vs $14,032 (+$1,936, +16.0%)
- Gross profit per visitor: $0.61 vs $0.71
- Unit margin: $12 vs $16

Elasticity: units -13.9% (midpoint) for price +9.5%, so about -1.46 (elastic). Break-even: 12,096 / 16 = 756 units at $44, which is 25% below the $40 volume and 13.8% below the observed $44 volume. Daily gross profit at $44 beat $40 on 18 of 28 days (10 days for $40).

Caveats: single 28-day window with no seasonality or promo data; online shop only; gross of payment fees, shipping and returns (not in the file); random assignment assumed but not shown in the data.

Next steps: move to $44 and track weekly units, conversion and gross profit against the 27/day threshold; optionally keep a small $40 holdout for 2-4 weeks; confirm margin after fees and shipping before a wider change.
````
