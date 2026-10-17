# Elasticity and the optimal price

Loaded for: "is our price right", "what's our elasticity", "should we raise
prices", and read-outs of a price change already made.

## 1. Terms

| Term | Definition |
|---|---|
| Own-price elasticity `e` | % change in units for a 1% change in own price. Negative. Use `E = abs(e)` |
| Cross-price elasticity | % change in our units for a 1% change in another product's price. Positive: substitutes. Negative: complements |
| Elastic | `E > 1`: a price cut raises revenue, a rise lowers it |
| Inelastic | `E < 1`: a price rise raises revenue and, with any positive margin, profit |
| Contribution per unit | `P - VC` |
| PV ratio | `(P - VC) / P`, the contribution-margin ratio |
| `1/PV` | % gain in contribution per unit from a 1% price rise |

Revenue-maximising price sits where `E = 1`. With a positive variable cost,
the profit-maximising price is higher than the revenue-maximising price.
Fixed cost changes the profit level, never the profit-maximising price.

## 2. Before any data: screen for likely sensitivity

Score each driver. Mostly left column: expect higher `E`. Use as a prior, not
an estimate.

| Driver | Higher E when | Lower E when |
|---|---|---|
| Substitutes | many close ones | few believable ones |
| Loyalty | weak | strong |
| Switching cost | low | high |
| Need | discretionary | necessary |
| Share of budget | large | small |
| Price transparency | easy to compare (online, marketplaces) | hard to compare |

Level matters: a category can be inelastic while one brand inside it, facing
close rivals, sits on the elastic side of its own curve. Do not apply a
textbook category elasticity to a single brand or SKU.

## 3. Estimating E

### Routes, strongest first

| Route | Strength | Weakness |
|---|---|---|
| Randomised price test (customers, markets or time windows; price is the only thing changed) | causal | needs volume, fairness of different prices |
| Sales history regression (POS, Shopify, marketplace) | real behaviour | confounding: promos, ads, season, rival prices |
| Purchase-intention survey, calibrated with past conversion by answer bucket | cheap, pre-launch | stated, not revealed; top-2-box throws away information |
| WTP / reservation-price survey | quick demand curve | noisy, self-reported; validate with behaviour |

### Two observations (arc)

`e = (dQ/Q) / (dP/P)`. Only valid if nothing else changed between the two
points. Usually something did.

### Regression on sales history

1. Unit of analysis: SKU-week, store-week or market-week. One grain.
2. Variables: units, own price, promo flag (any feature, email, banner,
   sitewide sale), promo depth, rival price if known, season (month or week
   of year dummies), stock-out flag.
3. Form, chosen by the decision:

| Form | Coefficient means | Use for |
|---|---|---|
| `ln Q = a + b ln P` (log-log) | `b = e`, constant elasticity | comparing products, `P*` under constant elasticity |
| `ln Q = a + b P` (log-linear) | % change in units per $1 | semi-elasticity |
| `Q = a + b P` (linear) | units per $1 | local unit effects, linear `P*` |

4. **Promo contamination.** Low prices usually come with promo signage,
   emails and homepage slots. The sales jump is price plus attention. Leave
   the promo variable out and `E` comes out too high. Fit with a promo dummy,
   and separately on non-promo weeks only. If the two controlled estimates
   agree and the naive one is much larger, the naive one is biased.
5. **Stockpiling and grain.** Weekly data captures stock-up and the drought
   after it. The notes report price sensitivity measured weekly running about
   7x higher than the same data read quarterly. For a permanent price
   decision, prefer monthly totals or drop the weeks next to each price change.
6. **Other regression traps.** Omitted variables bias the price coefficient;
   collinear predictors make coefficients unstable; serial correlation makes
   standard errors too small. Judge extra variables with an F-test, not a rise
   in R-squared (R-squared never falls when you add variables).
7. Re-run by segment or channel if buyers differ (new vs returning,
   marketplace vs own store).

### Reading a log-log fit across brands

Higher intercept `a` = higher baseline demand at a given price. Lower `E` and
higher baseline together are the signature of premium positioning.

## 4. Deciding the direction: the 1/PV rule

A 1% price rise raises contribution per unit by `1/PV` % and cuts units by `E` %.

| Condition | Meaning | Action |
|---|---|---|
| `1/PV > E` | margin gain beats volume loss | underpriced: raise |
| `1/PV < E` | volume loss beats margin gain | overpriced: cut |
| `1/PV = E` | no first-order gain | at the optimum |
| `E < 1` | always `1/PV > 1 > E` | raise: profit rises with price |

This uses only the local elasticity, so it holds whatever the demand shape,
for small moves. Recompute `E` after a large move.

## 5. The optimal price

| Demand | `P*` | Condition |
|---|---|---|
| Constant elasticity `Q = A P^-E` | `VC x E / (E - 1)`; markup on VC = `1/(E-1)` | `E > 1`; with `E <= 1` there is no finite optimum |
| Linear `Q = A - B P` | `A / (2B) + VC / 2` | `0 <= P <= A/B` |

Guardrails before recommending `P*`:

- Is `P*` inside the range of prices actually observed? Outside it, the curve
  is extrapolated. Recommend a step of 5-10% toward `P*` as a test.
- State the break-even for the step: a rise `k` must lose less than
  `k / (PV + k)` of units; a cut `d` must gain more than `d / (PV - d)`.
- Fairness and reference price (see price-structure-and-psychology): a rise
  above the customer's reference price stings more than an equal cut pleases.
- Competition: who are the close substitutes (switching data, cross-price
  response), and will they follow? Price moves in concentrated markets are a
  strategic game, not only a curve.
- Long run: a lower price that improves retention can be right on CLV even
  if it lowers one-period contribution. Show it only with measured retention.

## 6. Reading a price change that already happened

Price rises are often announced (email, banner, "prices go up on the 1st").
Buyers stock up, then buy less until their stock runs down.

1. Daily units from 4+ weeks before the announcement to 4+ weeks after the
   change. Mark both dates.
2. Baseline = before the announcement. Settled level = after the post-change
   dip ends (units level off).
3. Settled `E` = (settled / baseline - 1) / (% price change), sign flipped.
4. Contribution per day: baseline x (P0 - VC) vs settled x (P1 - VC).
5. The naive read (two weeks before vs two weeks after) compares the stock-up
   peak with the drought: it can show a 40-50% drop where the settled drop is
   a few percent. Never roll back a price on that comparison.
6. If the post period has not settled yet, say the verdict is provisional and
   when it will be readable.

## 7. New products: skimming or penetration

| Lean skimming when | Lean penetration when |
|---|---|
| early buyers are insensitive, product is distinctive, novelty/patent/prestige | demand is elastic, market is big |
| a low price would signal low quality | scale or learning cuts cost |
| newer versions will follow anyway | rivals will enter fast; installed base or network effects matter |

Neither is permanent. Set the trigger for the first price review before
launch. Watch for maturity: rising cross-brand switching, private labels,
easier comparisons, shrinking willingness to pay for differences. When they
pile up, pricing freedom shrinks.

## 8. Pitfalls

- Sign: `e` is negative; every rule here uses `E = abs(e)`.
- Elasticity from promo weeks describes response to a temporary deal plus
  attention, not to a permanent regular price.
- Cost-plus prices ignore demand: compare any cost-plus result against `E`
  and willingness to pay before using it.
- A price that maximises revenue is not the one that maximises profit.
