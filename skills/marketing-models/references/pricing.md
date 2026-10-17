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
