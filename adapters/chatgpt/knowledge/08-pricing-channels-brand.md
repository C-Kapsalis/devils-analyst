# Skill: pricing-promotions

---
name: pricing-promotions
description: >-
  Use this skill for any price or discount decision and any promotion read-out: "should
  we raise (or cut) prices", "is our price too high", "what's our price elasticity", "how
  deep should the discount be", "will 20% off pay for itself", "how much do sales need to
  go up", "was the sale / Black Friday / promo code worth it", "should we run it again",
  "we keep doing sales, is that a problem", "should we bundle", "good-better-best tiers",
  "free shipping threshold", "we raised prices and sales dropped, roll it back?", "Amazon
  vs our store vs wholesale, which channel makes money", retailer margin, markup, trade
  deals. It sets the objective, gets contribution margin right, estimates elasticity
  without promo and stock-up bias, computes break-even volume, nets out pull-forward and
  discounts given to people who would have bought anyway, spots baseline erosion from
  frequent promos, and compares channels on contribution, not revenue.
---

# pricing-promotions

Price is the lever that moves profit fastest, and the one most often judged on
the wrong number. Revenue is not profit, sales lift is not a win, and a price
"cut" that grows units can still lose money. Compute everything in code, on
contribution, over a window long enough to see what happened after.

## 0. What the human owns

Ask; do not assume. The user owns two things:

1. **The question and the objective.** Margin, share growth, trial of new
   customers, clearing stock, or protecting a premium image. The right price
   differs by objective. If not stated, ask once; if still unknown, show the
   answer for "maximise contribution" and say what would change under the others.
2. **The decision.** You give the verdict, the number and the risk. They choose.

## 1. Route the question

| The user asks | Type | Go to | Depth |
|---|---|---|---|
| "Is our price right / should we raise it / what's our elasticity" | Price level | 3A | elasticity-and-optimal-price (section "File: pricing-promotions/references/elasticity-and-optimal-price.md" in 08-pricing-channels-brand.md) |
| "We changed the price, did it work / roll back?" | Price change read-out | 3B | same |
| "How deep should the discount be / will X% off pay?" | Discount design | 3C | promo-evaluation (section "File: pricing-promotions/references/promo-evaluation.md" in 08-pricing-channels-brand.md) |
| "How did the sale / code / promo do, run it again?" | Promo read-out | 3D | same |
| "We run lots of sales / lift keeps growing / more promos next year?" | Promo frequency | 3E | same |
| "Bundle, tiers, free-shipping threshold, fees, how to show the price" | Price structure | 3F | price-structure-and-psychology (section "File: pricing-promotions/references/price-structure-and-psychology.md" in 08-pricing-channels-brand.md) |
| "Which channel makes money / Amazon vs store vs wholesale / retailer margin" | Channel economics | 3G | channel-margins (section "File: pricing-promotions/references/channel-margins.md" in 08-pricing-channels-brand.md) |

A read-out that claims a cause ("the sale worked") also goes through
`evidence-check`. This skill owns the promo and price arithmetic; evidence-check
owns tests, control groups and significance.

## 2. Data the answer needs

| Need | Minimum | If missing |
|---|---|---|
| Unit variable cost | product cost + pick/pack/ship + payment fees + channel fees per unit or order | Ask. Do not use a "gross margin %" without asking if it is margin or markup |
| Sales history | units and price per day or week, same product or basket | No elasticity: give the break-even table only (3C) |
| Promo calendar | start, end, depth, scope, and any email or homepage push | Infer from discount_amount > 0 and say so |
| Discount actually given | discount amount per day or order | Use depth x promo revenue, flag as estimate |
| Customer type | new vs returning per order | Cannot size subsidised buyers: caveat it |
| Post-period | at least as long as the repurchase cycle after the promo or price change (default 4 weeks if unknown) | Verdict is provisional: say so |

Refuse to give a profit verdict from revenue alone. Refuse an "optimal price"
far outside the prices actually observed: recommend a test step instead.

## 3. Procedures

### Core formulas (use exactly)

| Quantity | Formula |
|---|---|
| Contribution per unit | `m = P - VC` |
| Contribution-margin ratio | `PV = (P - VC) / P` |
| Margin from markup | `margin = markup / (1 + markup)`; markup = `margin / (1 - margin)` |
| Arc elasticity | `e = (dQ/Q) / (dP/P)`, `E = abs(e)` |
| Log-log elasticity | fit `ln Q = a + b ln P + c promo + controls`; `E = -b` |
| Price direction test | `1/PV > E`: underpriced, raise. `1/PV < E`: overpriced, cut. Equal: optimal |
| Optimal price, constant elasticity | `P* = VC x E / (E - 1)`, only if `E > 1` |
| Optimal price, linear demand `Q = A - B P` | `P* = A / (2B) + VC / 2` |
| Break-even lift for a discount `d` (share of price) | `lift = d / (PV - d)`; impossible if `d >= PV` |
| Break-even volume loss for a price rise `k` | `loss = k / (PV + k)` |
| Program break-even | `extra units needed = program cost / contribution per unit at the promo price` |
| Promo net incremental contribution | `sum(contribution, promo + post window) - baseline contribution per day x days in window - program costs` |
| Subsidy | discount given on orders that baseline says would have happened anyway |
| Channel contribution per unit | `net price after returns - VC - channel fees - fulfilment - ad spend per unit` |

### 3A. Is the price right?

1. Compute `PV` from cost lines, not from a quoted "margin".
2. Estimate `E` (method in the elasticity reference): log-log on weekly data with a
   promo dummy (and any email/feature flag), or on non-promo weeks only. Never
   price alone when promos coincide with low prices: that overstates `E`.
3. Compare `1/PV` with `E`. That decides the direction, whatever the demand shape.
4. Compute `P*`. If `P*` is outside the observed price range, do not recommend
   it: recommend a 5-10% step toward it as a test, and the break-even volume
   loss (or gain) that step must beat.
5. Check category vs brand level: a category can be inelastic while one
   brand's own demand is elastic.

### 3B. A price change already happened

1. Plot daily units from 4+ weeks before any announcement to 4+ weeks after.
2. Mark the announcement date. A spike before the change and a dip after it is
   stock-up (forward buying), not price response.
3. Baseline = before the announcement. Settled level = after the dip ends.
   Never compare the two weeks either side of the change.
4. `E` = settled % change in units / % change in price. Judge on
   contribution per day, settled vs baseline, against the break-even loss
   `k / (PV + k)`.

### 3C. How deep should the discount be?

1. Compute `PV` at full price. Build the table: depth 10/15/20/25/30% ->
   break-even lift `d / (PV - d)`.
2. Add program costs (ads, gifts, agency, fees) as extra units needed.
3. Compare with lift actually seen in past promos of that depth, after
   pull-forward (3D), not with hope.
4. Prefer the depth whose expected net incremental contribution is highest,
   and say who it should target: new or lapsed customers carry less subsidy.

### 3D. How did the promotion do?

1. Baseline: average daily contribution over the 4 weeks before (exclude other
   promos and holidays). Second baseline: same window last year, or pre plus
   recovered post period. Report both.
2. Window: promo days plus the post-period until daily orders recover.
3. Net incremental orders and contribution over the whole window (formula
   above). The promo-week lift alone is not the answer.
4. Subsidy: discount given to baseline orders. Split new vs returning: a code
   mostly used by returning customers bought little.
5. Add future value only if promo-acquired customers' repeat rate is measured
   and close to non-promo customers'. Otherwise say "unproven".
6. Verdict on net contribution. Then the redesign: depth, target, holdout.

### 3E. Promo frequency and baseline erosion

1. By year or quarter: number of promo weeks, baseline (non-promo) weekly
   units, promo-week units, lift over baseline, promo share of revenue, total
   contribution per week.
2. Rising lift with a falling baseline is erosion, not better promos: buyers
   learned to wait. Judge on total contribution per week, not lift.
3. Flag promo share of revenue above about 40% (heuristic from the notes).
4. Recommend fewer, targeted promos with a holdout, and track baseline
   quarterly. Expect short-term pain before the baseline recovers.

### 3F. Price structure, 3G. Channel economics

Follow the frameworks in the linked references. Musts: bundles only when
valuations differ across buyers and variable cost is low; tiers with clear
value jumps; free-shipping threshold just above current average basket;
all-in prices when trust matters; channels ranked by contribution per unit and
per month after fees, returns and ads, with price parity across channels
checked for conflict.

## 4. Adversary for every move

Run each check that applies. A move is done only when its check passes.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Set the objective | "Is this about margin, share, trial or stock? Who decides?" | User stated it, or you asked | Answer for contribution and list what changes under each objective |
| Get the margin | "Is 60% a margin or a markup? Does it include shipping, payment, returns, channel fees?" | Rebuild `PV` from cost lines; convert with `markup/(1+markup)` | Use the rebuilt `PV`; say the quoted one was wrong |
| Estimate elasticity | "Did promos, emails, season or stock-outs move with price?" | Refit with promo dummy, and on non-promo weeks only; compare `E` | Report the controlled `E`; show the naive one as biased |
| Choose the grain | "Is weekly data catching stockpiling, not price response?" | Re-estimate on monthly totals, or drop weeks next to price changes | Use the longer grain; caveat weekly `E` as an upper bound |
| Read a price change | "Was it announced? Did people stock up first?" | Daily plot around the change; spike before, dip after | Baseline before announcement, settled level after the dip |
| Recommend a price | "Is `P*` inside prices we have actually charged?" | `P*` within observed min-max | Recommend a 5-10% test step with its break-even volume |
| Set the baseline | "Would another baseline flip the sign?" | Pre-only vs last-year vs pre+recovery | If signs differ: inconclusive, propose a holdout |
| Count incremental sales | "Did the weeks after pay for the promo week?" | Window runs until orders recover | Extend the window; never report promo-week lift alone |
| Count the cost | "How many discounted orders would have happened anyway?" | Baseline orders x discount per order; new vs returning split | Report subsidy as a cost line |
| Judge profit | "Revenue rose; did contribution?" | Contribution per day in vs out of promo, after discount, cost, shipping, program costs | Verdict on contribution only |
| Claim future value | "Did promo buyers actually come back?" | Repeat rate of promo-acquired vs other new customers | Mark CLV "unproven", exclude it |
| Read lift trends | "Is lift rising because the baseline is falling?" | Baseline trend and contribution per week by year | Call it erosion; judge on total contribution |
| Rank channels | "Ranked by revenue or by money kept?" | Contribution per unit and per month after fees, returns, ads | Rank by contribution |
| Price across channels | "Does one channel undercut the others or our retailers?" | Compare shelf prices by channel | Flag conflict risk; propose parity or channel-specific products |
| Change structure | "Will the bundle or tier cannibalise full-price sales or feel unfair?" | Share of buyers moving down; hidden fees surfaced early | Mixed bundle, clearer tiers, all-in price |
| Recommend | "What does it cost if this is wrong? What would the CFO ask?" | Downside in money and a way to verify | Shrink the bet or turn it into a test with a holdout |

## 5. Output

```
Verdict: [raise / hold / cut price] or [promo paid / did not pay / inconclusive]
Deciding number: [e.g. "net incremental contribution -$16.2k over 4 weeks"
  or "E = 1.9 controlled vs 1/PV = 2.2: underpriced"]
Naive read and why it is wrong: [one line, with its number]
Action: [price, depth, target, cadence or channel move]
Risk if wrong: [money at stake] · How to verify: [test, holdout, window, metric]
```

Show the arithmetic as a short table (baseline, window, incremental, discount,
contribution) so the reader can redo it. State every assumption (cost lines,
baseline, window) next to the number it drives.

## 6. Score-and-probe gate before handover

1. Every applicable row in section 4 has passed. If not, fix it first.
2. Score the draft 0-100 on **clarity**, **relevance** (answers the user's
   question and objective), **depth** and **insightfulness**.
3. Any score below 80: write the probe question that would raise it (e.g.
   "Did returning customers use the code?"), answer it from the data, revise,
   re-score. At most 2 loops.
4. Hand over with the scores, and ask the user to confirm the objective and
   own the decision.

---

## File: pricing-promotions/references/channel-margins.md

# Channel and distribution economics

Loaded for: "which channel makes money", own store vs marketplace vs
wholesale, retailer margin and markup, trade terms, adding a channel.

## 1. Margin vs markup

| Term | Formula | Example (buy $10, sell $20) |
|---|---|---|
| Markup on cost | `(price - cost) / cost` | 100% |
| Margin on price | `(price - cost) / price` | 50% |

| Know | Need | Formula |
|---|---|---|
| cost, markup | price | `price = cost x (1 + markup)` |
| price, margin | cost | `cost = price x (1 - margin)` |
| markup | margin | `margin = markup / (1 + markup)` |
| margin | markup | `markup = margin / (1 - margin)` |

Retailers usually quote margin on their selling price. A retailer that wants
a 50% margin on a $34 shelf price pays $17, not $34 / 1.5.

## 2. Contribution per channel

Rank channels on what each unit leaves after the channel takes its share,
never on revenue.

```
contribution per unit = price x (1 - return rate)
                        - product cost (net of resaleable returns)
                        - channel fees (marketplace referral %, payment %, per-order fees)
                        - fulfilment (pick, pack, ship, marketplace fulfilment fee)
                        - allowances (co-op, slotting, display) per unit
contribution after ads = contribution per unit x units - channel ad spend
```

Steps:

1. Build one row per channel per month: units, revenue, returns, every fee
   line, fulfilment, ad spend. Fees often live in payout or settlement
   reports, not the sales export.
2. Compute contribution per unit and per month, before and after ads.
3. Rank by contribution per month, and by contribution per extra unit for
   growth decisions (average is not marginal: the next $ of ads usually earns
   less than the average).
4. Compare shelf prices across channels (see section 4).

## 3. Channel stack and double marginalisation

Each layer marks up: manufacturer cost -> wholesale price -> shelf price.
When each layer sets its own markup, the shelf price ends too high, volume
too low, and the whole channel earns less than a coordinated one would.

1. Map cost -> wholesale -> shelf and each layer's markup.
2. Test whether the shelf price is suppressing demand (elasticity at shelf).
3. Fixes: better wholesale terms, price ceilings, coordination, a direct
   channel for some buyers.

## 4. Adding or growing a channel: conflict check

Manufacturers want volume; retailers and distributors want margin. Conflict
rises when distribution goes from selective to intensive, when a brand adds
its own e-commerce to a retail network, or when one partner (a big
marketplace or retailer) becomes a large share of revenue. The notes flag
dependence once one customer is about 10% or more of revenue.

Before adding or growing a channel:

1. Will current partners see it as taking their volume?
2. Will price, assortment, service or product versions differ by channel?
   A marketplace price below your own store and your retailers' shelf price
   undercuts both.
3. Set equal-treatment rules in advance.
4. Decide what data is shared with whom.
5. Have an escalation path before complaints start.

Conflict fixes: exclusive territories or segments, channel-specific products
or bundles, different service bundles, fair process (a partner forum), clear
roles. If partners cannot make money on your product, support (display,
recommendation, feature ads) disappears; fix the economics, not the symptom.

## 5. Distribution intensity

| Intensity | Fits | Upside | Risk |
|---|---|---|---|
| Intensive (everywhere) | convenience, routine, impulse goods | reach | price wars between outlets, cannibalisation, weak control |
| Selective | shopping goods, comparison buying | partner fit, brand match | coverage gaps |
| Exclusive | prestige, specialty | scarcity, premium image, partner commitment | weak access if the partner underperforms |

Early in a product's life selective or exclusive coverage with premium
pricing often fits; later, broader coverage with lower prices. Broadening
distribution to discount outlets can lift sales short term and erode a
premium brand long term.

## 6. Cutting out the middle

Removing an intermediary does not remove its work (storage, assortment,
selling, financing, returns, service). Someone must do it, or the customer
does. Before going direct:

1. List the functions the intermediary performs.
2. Name who does each after removal, and the cost.
3. Check gains: freshness, margin, speed, customer data.
4. Check new problems: fulfilment, service, conflict with remaining partners.

## 7. Marketplace fulfilment dependence

Outsourced fulfilment (3PL, marketplace fulfilment) gives scale and speed and
creates dependence. Track fee changes, stock limits and the share of revenue
through one partner.

## 8. Legal flags (screen, not advice)

Exclusive dealing, exclusive territories and tying (must buy B to get A) can
be illegal when they shut out competition, especially from a strong
bargaining position. Resale price control is legally restricted in many
markets. Flag and refer to counsel.

---

## File: pricing-promotions/references/elasticity-and-optimal-price.md

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

---

## File: pricing-promotions/references/price-structure-and-psychology.md

# Price structure and price perception

Loaded for: bundles, tiers, product lines, free-shipping thresholds, fees,
how a price is shown, price increases, loss leaders and hero items.

## 1. Bundling

| Option | What it is |
|---|---|
| Pure components | each item sold alone |
| Pure bundle | only the bundle is sold |
| Mixed bundle | items alone or as a bundle |

Bundling pays when:

- buyers value the items differently (negatively correlated valuations: one
  buyer loves A and shrugs at B, another the reverse). Totals become more
  similar across buyers, so one bundle price captures more.
- variable cost is low. As unit cost rises, carrying low-value items inside
  the bundle gets expensive and the gain shrinks.
- it saves selling, packing or shipping cost.

Mixed bundling often beats both extremes: the bundle sells to the broad
middle, singles still earn full margin from buyers who want one item.

Method:

1. List components with standalone valuations (survey, or purchase data:
   who buys A only, B only, both).
2. Check whether valuations are negatively correlated across buyers.
3. Check unit variable cost of each component.
4. Compute contribution under pure components, pure bundle and mixed bundle.
5. Add operational savings. Check cannibalisation of full-price singles.

## 2. Product-line ladders (good-better-best)

1. Each tier has a clear value jump that buyers can see.
2. Price gaps big enough to matter, not so big the middle collapses.
3. Every tier has a reason to exist; remove middle items that only confuse.
4. Watch the share of buyers moving down after any change.

Context effects: a clearly dominated option makes the option that beats it
look better (attraction effect); adding an extreme option makes the middle
look safer (compromise effect). Use them honestly or not at all.

Each added pricing layer adds less profit than the last and more confusion.
Ask whether the next layer pays for itself.

## 3. Two-part and captive pricing

- Captive: base product plus repeat complements (razor and blades, printer
  and ink). Price the base and the refill as one system; test the risk of
  third-party substitutes for the complement and whether buyers find the
  system fair.
- Two-part: access fee plus usage (membership plus per-use, plan plus
  overage). Works only with churn under control. Overage charges feel
  punitive; buyers over-buy plans to avoid them, which can damage trust and
  CLV later.

## 4. Free-shipping threshold

1. Margin by order size; find where shipping can be covered.
2. Set the threshold just above the current average basket.
3. Test whether shoppers add profitable items to qualify.
4. Revise if it kills too many orders or gives shipping away on weak baskets.

## 5. Menus and cost-to-serve

When cost-to-serve differs (delivery vs pickup, high vs low usage), a small
menu lets buyers self-sort. Base price plus a service charge is easier to
defend than per-customer prices. In services, flat plans attract the
costliest users (adverse selection): use tiers, limits or deductibles.

## 6. Reference prices

Buyers judge a price against a reference: internal (memory of past prices,
recent ones weigh most) and external (list price, "was/now", competitor).
They hold an acceptable band, not one number. Inside the band the price is
accepted; far outside it is rejected.

- Frequent discounts lower the internal reference price: the "regular"
  price starts to feel expensive.
- A price rise above the reference hurts more than an equal cut below it
  pleases (loss aversion). A price that was low and then rose can feel worse
  than a higher price from day one.
- A deal frame adds satisfaction on top of the product's value (transaction
  utility), which is why "was/now" works, and why a fake "was" price backfires.

Advertised reference price audit: anchor source (own past price, MSRP,
competitor), truthful and defensible, easy to notice, believed by shoppers;
track lift and complaints.

## 7. How the number is shown

| Choice | Use when | Risk |
|---|---|---|
| Odd prices ($49.95) | bargain image, deal framing | cheapens a premium brand |
| Round prices ($50) | premium feel, gifts, simplicity | less "deal" signal |
| Partitioned ($624 + $75 delivery) | short-run conversion | buyers feel tricked at checkout; trust and abandonment |
| All-in ($699 delivered) | trust matters | lower headline appeal |

Price is also a quality cue when quality is hard to judge before buying, the
buyer lacks expertise, or status matters. Premium and luxury brands cannot
discount casually without damaging the image.

## 8. Fairness check before a price increase

1. State the reason plainly (higher cost, more value delivered).
2. Make the added value or cost visible.
3. Apply the rule consistently across customers and channels.
4. Show all fees early.
5. Give notice where possible (and expect stock-up: see 3B in SKILL.md).
6. Plan the message before the move, not after backlash.

Prices feel unfair when urgency is exploited, fees appear late, neighbours
get different prices with no visible reason, or a "sale" uses an inflated
regular price. Dynamic pricing needs a disclosed rule, caps on size and
frequency of changes, and monitoring of complaints and churn.

## 9. Hero items, loss leaders and price image

Shoppers remember the prices of a few items and judge the whole store from
them (key value items). Pricing those sharply can lift traffic, basket and
price image. Judge such an item on system profit:

`system profit = item contribution + spillover contribution from extra traffic and basket`

1. Confirm shoppers actually notice and compare this item.
2. Estimate how far below normal margin it runs.
3. Measure basket and traffic spillover (orders containing it: other items
   and margin per order).
4. Check for cherry-pickers who buy only the deal item.
5. Stop if spillover is weak or rivals copy it.

Price image also comes from non-price cues: promo frequency, service level,
site design, assortment. Fix cues that make you look expensive before
cutting prices broadly. Online, the list of items buyers compare changes
faster and differs by channel; review it often.

## 10. Long-run value

Some prices are right only because of later purchases: a low entry price,
a sample, a membership. Keep them only if retention, repeat margin and
discounted future profit are measured and cover the lost contribution now.
CLV also sets the ceiling on what to spend acquiring a customer.

---

## File: pricing-promotions/references/promo-evaluation.md

# Promotion design and evaluation

Loaded for: discount depth, "will X% off pay", promo read-outs, "run it
again", and promo frequency. This is the deep version of the promotions
check in `evidence-check` section 4.

## 1. What a promotion can buy, and what it costs

| Possible benefit | Possible cost |
|---|---|
| sales in the window | margin given on every discounted unit |
| trial by new buyers | discount given to buyers who would have paid full price |
| switching from rivals | admin, gift, display, ad and fee costs |
| stock-up (only good if it raises consumption) | sales pulled forward from later weeks |
| new loyal buyers (future CLV) | lower reference price, buyers trained to wait |
| | lower quality perception for premium brands |

Sales lift by itself is never the win condition. The test is net incremental
contribution after all of the right-hand column.

## 2. Before the promo: break-even depth

Equal-contribution condition for a discount `d` (share of price) at
contribution-margin ratio `PV`:

```
(P(1 - d) - VC) x Q1 = (P - VC) x Q0
required Q1/Q0 = PV / (PV - d)      break-even lift = d / (PV - d)
```

| PV \ depth | 10% | 15% | 20% | 25% | 30% |
|---|---|---|---|---|---|
| 30% | 50% | 100% | 200% | 500% | never |
| 40% | 33% | 60% | 100% | 167% | 300% |
| 50% | 25% | 43% | 67% | 100% | 150% |
| 60% | 20% | 33% | 50% | 71% | 100% |

Then add program costs: `extra units = program cost / (P(1-d) - VC)`.

Use `PV` per order including shipping, payment and channel fees. A quoted
"gross margin" that leaves out pick, pack and shipping makes every discount
look cheaper than it is.

Choose the objective first (trial, switching, stock-up, traffic, loyalty)
and the target. Approve only if most answers are yes:

1. Does it solve a named problem (trial, urgency, stock-up, retention, channel support)?
2. Will it create behaviour that would not happen anyway?
3. Can the margin take it (break-even lift is achievable)?
4. Is there a stop condition?
5. Will it avoid teaching customers to wait for the next deal?

## 3. After the promo: the read-out

### Step 1. Baseline

- Primary: average daily orders and contribution over the 4 weeks before the
  promo, excluding other promos, holidays and stock-outs.
- Cross-check: the same window last year scaled by the year-on-year trend,
  or pre-period plus the recovered post-period.
- If the baseline itself is falling over time, project the trend; do not
  freeze it.
- Report both baselines. If the verdict changes sign between them, it is
  inconclusive.

### Step 2. Window

Promo days plus the post-period until daily orders return to baseline. For
consumables and replenishable goods this is at least one repurchase cycle.

### Step 3. Incremental orders and contribution

```
contribution/day = net revenue after discount - product cost - shipping/fulfilment - fees
incremental contribution = sum(contribution over window) - baseline contribution/day x days - program costs
incremental orders = sum(orders over window) - baseline orders/day x days
```

A dip after the promo is pull-forward: buyers who would have bought later
bought during the deal. Net it out.

### Step 4. Subsidy

`subsidy = baseline orders in the promo days x average discount per order`.
These discounts bought nothing. Split promo orders new vs returning: a code
used mostly by returning customers on their normal cycle is mostly subsidy.

### Step 5. Future value

Count future CLV only if measured: repeat rate and margin of customers
acquired in the promo vs other new customers over the same horizon. If promo
buyers repeat less, or have not been observed long enough, mark it unproven.

### Step 6. Separate price effect from attention

A promo is a lower price plus emails, banners and urgency. A promo lift is
not a price elasticity. Do not convert one into the other without the promo
dummy logic in elasticity-and-optimal-price.

### Step 7. Verdict and redesign

| Finding | Redesign |
|---|---|
| Net contribution negative, pull-forward large | fewer, shorter promos; target lapsed or new customers |
| Subsidy is most of the discount cost | gate the offer (first order, lapsed 90+ days, cart threshold) |
| Lift below break-even for this depth | shallower depth, or a non-price offer (gift, bundle) |
| Inconclusive baseline | run it with a randomised holdout (see evidence-check) |

## 4. Promo frequency and baseline erosion

Frequent deals train buyers to wait and stockpile. The baseline (full-price)
sales fall, so lift over baseline rises, so each promo looks better than the
last. The cycle ends with deeper discounts, lower margins and a commoditised
brand. Competitors matching discounts cancel any share gain.

### Long-view check (quarterly or yearly)

| Metric | Erosion signal |
|---|---|
| Baseline (non-promo) units per week | falling |
| Lift over baseline per promo | rising |
| Response to regular price (elasticity) | rising |
| Promo share of revenue | rising; above about 40% the notes call it training deal-seekers (heuristic) |
| Total contribution per week | flat or falling while promo count grows |
| Repeat purchase at full price | falling |

Judge on total contribution per week across all weeks, never on promo lift.
The notes report that the long-run effect of a discount is about 80% of its
short-run effect (a 20% long-term penalty), while advertising's long-run
effect can exceed its short-run one by about 60% (Lodish and Mela). Use these
as directional, not as constants for a forecast.

Cutting promos usually costs revenue for a quarter or two before the baseline
recovers. Say so up front, and track baseline monthly to show recovery.

### EDLP vs high-low

| Choose EDLP when | Choose high-low when |
|---|---|
| a stable price image and clean forecasting matter | buyers respond strongly to deals and traffic spikes can be used |
| frequent promos are costly to run | promo fatigue and reference-price erosion are under control |
| basket trust matters more than weekly excitement | |

## 5. Specific promo types

| Type | Judge on | Watch |
|---|---|---|
| Sampling / free trial | repeat rate and later contribution of samplers vs sample cost per acquired buyer | free riders; stop if trial is high and repeat is weak |
| Coupons / codes | redemption, incremental sales, who redeemed | leakage to coupon sites, deal dependence |
| Rebates | claim rate, net incremental profit | many never claim; the sticker price stays high |
| BOGO / multi-buy | unit lift and time to next purchase | pantry loading without extra consumption |
| Gift with purchase / premium | basket size, repeat | margin erosion |
| Free shipping threshold | orders that add items to qualify, margin by order size | threshold set where it gives shipping away on weak baskets |
| Loyalty programme | repeat rate, retention, customer value | costly complexity with no habit change |
| Contests / sweepstakes | entries, opt-ins, follow-on sales | weak link to sales; sweepstakes must not require purchase |

## 6. Trade promotions (selling through retailers)

- Pass-through rate = share of the retailer's per-unit deal that reaches the
  shelf price. Under linear demand a per-unit off-invoice deal passes through
  about 50%. Never assume 100%.
- Allowances (display, slotting, co-op ads) pay for retailer behaviour;
  verify compliance (display actually up, feature actually ran) and judge on
  incremental sell-through, not sell-in. The risk is paying for what the
  retailer would have done anyway.
- Forward buying by the retailer during a deal is the trade version of
  pull-forward.

## 7. Fulfilment

A promo that sells more than the warehouse can ship creates stock-outs and
late deliveries, which cost trust and repeat purchase. Check stock and
fulfilment capacity against the expected peak before launch.

---

# Skill: channel-audit

---
name: channel-audit
description: >-
  Use this skill when a marketer asks whether a digital channel or tactic pays and what
  to change in it: "should we raise our Google Ads bids or budget", "we're losing
  impression share", "what's the most we can pay per click", "is our Quality Score
  hurting us", "is display worth it, the CTR is terrible", "which audience or day did the
  ad work for", "should we cap frequency", "are our influencers worth it", "should we
  work with bigger creators", "TikTok or Instagram", "do discount codes help", "which
  keywords should we target for SEO", "why don't we rank", "our pages compete with each
  other", "are our backlinks good", "why aren't we in the local map pack", "how do we
  get cited by ChatGPT or AI Overviews", "which attribution model should we use",
  "data-driven and last click show the same", "where do people drop out of checkout",
  "is our bounce or cart abandonment bad". It works per campaign, creator tier, keyword
  or segment with break-even maths on margin, and labels what attribution can and cannot
  prove.
---

# channel-audit

Account averages hide the losers. A Google Ads account with CPA under margin
can carry campaigns that lose money on every click; an influencer program can
look strong because big creators bring the most orders while each of their
posts loses money; a keyword list ranked by volume is mostly terms you cannot
move. Judge each unit (campaign, creator tier, keyword, segment) on margin,
then recommend.

**The human owns the question and the decision.** Restate the decision in one
line. Ask for what the data lacks: gross margin or margin per conversion,
the primary conversion, the target audience. Never assume margin = revenue.

## 1. Route

| Question | Read first | Reference |
|---|---|---|
| Bids, budget, impression share, max CPC, Quality Score | Section 2 | paid-search-economics.md (section "File: channel-audit/references/paid-search-economics.md" in 08-pricing-channels-brand.md) |
| Display or video value, ad lift test, which segment or frequency worked | Section 3 | ad-lift-segments.md (section "File: channel-audit/references/ad-lift-segments.md" in 08-pricing-channels-brand.md) |
| Influencers: tiers, platforms, codes, rebooking | Section 4 | influencer-roi.md (section "File: channel-audit/references/influencer-roi.md" in 08-pricing-channels-brand.md) |
| SEO keywords, cannibalization, on-page, backlinks, local, AI answers | Section 5 | seo-search-visibility.md (section "File: channel-audit/references/seo-search-visibility.md" in 08-pricing-channels-brand.md) |
| Attribution model, channel credit, cutting a channel | Section 6 | attribution-choice.md (section "File: channel-audit/references/attribution-choice.md" in 08-pricing-channels-brand.md) |
| Site engagement, checkout drop-off, bounce, conversion by site type | Section 7 | site-funnel.md (section "File: channel-audit/references/site-funnel.md" in 08-pricing-channels-brand.md) |

Basic test validity (sample ratio, power, novelty, Simpson's paradox,
holdout maths) lives in the `evidence-check` skill; metric formulas and grain
in `metric-definitions`. Use them; do not repeat them here.

## 2. Paid search: does the next click pay

Per campaign (never only the account):

```
CVR = conversions / clicks          CPC = cost / clicks
Margin per conversion = AOV x gross margin (or the user's figure)
Break-even CPC = margin per conversion x CVR
Profit = conversions x margin per conversion - cost
```

| Pattern | Reading | Action |
|---|---|---|
| CPC < break-even, IS lost to budget high | Profitable and capped | Add budget here first |
| CPC > break-even, IS lost to budget high | Losing money and capped | Do not add budget; lower bids, fix CVR or landing page, or pause |
| IS lost to rank high, low Quality Score | Quality problem | Fix ad relevance, expected CTR, landing page; raising bids buys rank at a higher CPC |
| High impressions, low CTR | Ad not attractive | Copy, extensions, targeting |
| High CTR, low CVR | Click wasted | Landing page, offer, audience match |

- ROAS above 1 is not profit: compare ROAS with 1 / gross margin (at 40%
  margin, ROAS must exceed 2.5 to break even before other costs).
- Ad Rank = bid x Quality Score; actual CPC = Ad Rank of the advertiser below
  / your QS + 0.01. QS 10 cuts CPC about 50%, QS 1 raises it about 400%.
- Brand campaigns look best on every metric; their incrementality is unknown
  until tested (pause test in `evidence-check`).

## 3. Display, video and ad lift tests

- Judge display on viewable impressions, view-through conversions and lift,
  not CTR (about 0.46% display vs 3.17% search is normal).
- Lift = (CVR_treatment - CVR_control) / CVR_control, user-level CVR over an
  impression-based window. Incremental conversions = treatment conversions -
  CVR_control x treatment users. Incremental profit = margin x incremental
  conversions. POAS = (incremental profit - ad cost) / ad cost.
- Inference needs n x p >= 5 and n x (1 - p) >= 5 in each group; balance
  checks on pre-exposure variables should give p > 0.05.
- **Segments:** a pivot of lift by day, device, new vs returning or exposure
  band is descriptive. Before cutting or shifting spend on a segment
  difference, test it: logistic regression with treatment x segment
  interaction; only a significant interaction proves the effect differs.
  Compare segments on lift %, not raw point gaps. Frequency usually shows an
  inverted U: too few and too many exposures both lose.

## 4. Influencers: profit per post, by tier

```
Engagement rate = engagements / followers x 100
CPA = fee / attributed orders
Profit per post = orders x margin per order - fee
POAS = profit / fee
```

- Group by platform x follower tier (nano < 10K, micro 10K-100K, macro
  100K-1M, mega > 1M) x code / no code. Rank groups by POAS and profit per
  post, never by orders per post: big creators bring more orders and can
  still lose money per post.
- Fees differ sharply by platform for the same follower count; compare
  per-post cost before comparing outcomes.
- Discount codes tend to lift orders most for small creators; check the code
  effect inside each tier (an interaction, not one average).
- Follower count and engagement rate move in opposite directions; do not put
  both, or post cost, into one regression as drivers.
- Orders tracked by code or link are attributed, not incremental; audit
  audience quality (suspicious followers) before rebooking.

## 5. Search visibility (SEO, local, AI answers)

Keyword focus, per keyword, in this order:
1. Intent matches a funnel stage you need (awareness, consideration, action).
2. Current rank 4-20: the zone where effort moves traffic. Rank 1-3:
   maintain. Rank 50+ or unranked on high-difficulty terms: not this quarter
   (long-tail versions instead).
3. Competition you can beat (difficulty vs your authority; who holds the top
   results).
4. Volume, as the tie-breaker among interchangeable terms.
5. One keyword, one URL. Two of your URLs ranking for one keyword is
   cannibalization: consolidate onto the page that should own it.

Top three organic positions take about two thirds of clicks; rank gains
inside page one matter more than gains on page five. Backlinks, local and
AI-answer checks are in the reference.

## 6. Attribution: credit is not cause

- Rule-based models see only converting paths. Data-driven attribution (GA4
  default) uses converting and non-converting paths but needs about 400
  conversions per key event in 30 days (plus enough multi-touch paths);
  below that GA4 silently falls back to last click. **Identical last-click
  and DDA numbers usually mean the fallback, not agreement.**
- Custom models need more: Markov about 2,000, Shapley about 5,000, full ML
  about 10,000 conversions a month.
- First- and last-click columns must each sum to total conversions or value.
  Google models exclude direct visits unless the whole path is direct.
- Before cutting a channel on credit, run a holdout or geo test; attribution
  divides credit, only an experiment shows what the channel caused.

## 7. On-site funnel

- Engaged session: over 10 seconds, or 2+ page views, or a key event. GA4
  bounce rate = share of sessions not engaged.
- Purchase CVR = purchases / sessions. Define the conversion by site type
  (purchase, lead, pageviews for ad-funded media, subscription).
- Cart abandonment benchmark about 70% (60% is very good). Read step by step
  (product view, add to cart, checkout, shipping, payment, purchase); fix the
  biggest step drop first and name its likely cause (hidden costs, forced
  account, long forms, missing payment method, trust).

## 8. Adversary for every move

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Frame the decision | Which decision, which conversion, which margin? | Decision restated; primary conversion and margin confirmed or asked | Ask; do not assume revenue is profit |
| Compute campaign economics | Is the account average hiding losers? | Break-even CPC and profit per campaign; totals recomputed two ways | Re-cut by campaign |
| Recommend budget or bids | Is the constraint budget or rank, and is the click profitable? | IS lost to budget vs rank, QS, CPC vs break-even | Move money only to profitable, budget-capped campaigns |
| Read an ad test | Is this lift or targeting? Is the segment gap real? | Randomised control, n x p >= 5, balance p > 0.05, interaction test | Label segment findings as hypotheses |
| Rank creators | Are we ranking by volume instead of profit? | POAS and profit per post by platform x tier x code | Re-rank by profit |
| Pick keywords | Can we move these, and do they compete with each other? | Rank band 4-20, intent, difficulty, one URL per keyword | Drop or consolidate |
| Read attribution | Did DDA actually run, and is credit being read as cause? | Monthly conversions per key event vs 400; columns sum to total | Say the comparison is uninformative; propose a holdout |
| Name the cause | What else produces the same pattern? | Data ruling out each rival (mix, season, tracking change) | Call it a hypothesis |
| Recommend | What does it cost if wrong, and what would the CFO ask? | Money at risk; the test or metric that confirms within weeks | Shrink the change; add a test |

## 9. Score-and-probe gate before handover

1. Every row in section 8 passes, or the answer says which could not and why.
2. Score the draft 0-100 on **clarity**, **relevance** (answers the decision
   asked), **depth** (per-unit numbers behind each claim) and
   **insightfulness** (what the account-level view hid).
3. Below 80 on any: write the probe question that would raise it, answer it
   from the data, revise, re-score. At most 2 loops; then hand over and note
   what stayed below 80.

## 10. Output

```
Verdict: <one line per unit: scale | hold | fix | cut | test first>
Number: <break-even vs actual CPC, POAS, lift with p, rank band, conversions vs 400>
Action: <specific change, sized in money or volume>
Verify: <metric and date, or the experiment that confirms it>
Caveats: <attribution limits, data gaps, what the user decides>
```

Show the per-unit table the verdict rests on.

---

## File: channel-audit/references/ad-lift-segments.md

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

---

## File: channel-audit/references/attribution-choice.md

# Attribution: choosing and reading a model

Attribution decides how conversion credit is split across touchpoints. It
drives budget, channel valuation, smart bidding and ROI claims, so a model
change changes every downstream number.

## Rule-based models

| Model | Credit | Fits | Blind spot |
|---|---|---|---|
| Last click (incl. direct) | 100% last touch | Short transactional cycles, closing campaigns | Ignores everything before |
| Last non-direct click | 100% last non-direct touch (Google default outside path reports) | Direct visits as already-won users | Same |
| Last Google Ads click | 100% last Ads click | Crediting Ads specifically | Same |
| First click | 100% first touch | Awareness, unknown brands, growth phase | Ignores closers |
| Linear | Equal | Long journeys, no stage believed stronger | Treats a weak touch like a decisive one |
| Time decay | Exponential, 7-day half-life default (credit proportional to 2^(-days/7)) | Short consideration, short promotions | Starves early discovery |
| Position (U) | 40% first, 40% last, 20% middle | Both demand creation and capture matter | Weights are a convention |
| W-shaped | 30% first, 30% lead creation, 30% last, 10% rest | B2B, long cycles | Same |

Conservative to growth-oriented: last click, time decay, linear, position,
first click. The same paths can make a channel worthless under one model and
the leader under another; no rule-based model can be shown most accurate.

Checks: each single-touch column sums to total conversions or value with one
winner per path; Google models give direct no credit unless the whole path is
direct.

## The core weakness and data-driven attribution

Rule-based models see only buyers' paths; most visitors never convert, so a
path that ends in a purchase half the time and in nothing the other half
looks like a pure win. Data-driven models use converting and non-converting
paths and assign credit by removal effect (how many fewer conversions without
this touch), via Shapley values (average marginal contribution across all
combinations) or Markov chains (removal from the transition graph).

GA4 DDA: default in GA4 and Google Ads; up to 50 touchpoints; 90-day lookback;
retrains continuously; adds a time-decay element. Needs about 400 conversions
per key event in 30 days and roughly 10,000 paths with 2+ interactions; below
that it silently uses last click. Custom builds need more: Markov 2,000+,
Shapley 5,000+, full ML 10,000+ monthly conversions; below these, a rule-based
model is safer than an overfit one. DDA is a black box run by the seller of
the ads it grades.

## Reading a model comparison

GA4: Advertising -> Attribution -> model comparison. Pick the key event, date
range and two models (last click vs DDA). Positive % change: the channel
assists more than it closes (last click underfunds it). Negative: it closes
journeys others started (last click overcredits it).

Diagnostics before believing the table:
1. Monthly conversions for that key event >= 400? If not, DDA fell back and
   identical columns are an artefact.
2. Unassigned rows: credit there is an artefact of paths GA4 could not
   connect, not a channel; it shrinks sharply under DDA.

## Credit is not causation

A channel with most last-click credit can be harvesting people who would have
bought anyway; a channel with little credit can create the demand others
close. Maturity needs three tools: attribution for allocation, experiments
(holdout, geo, lift) for whether a channel causes conversions, funnel reads
for where it leaks. Do not cut or scale a channel on attribution alone when
the decision is large; propose the test.

---

## File: channel-audit/references/influencer-roi.md

# Influencer ROI

Influencer posts read less like ads, and niche creators carry trust their
audience grants for that niche. That is why small creators often convert
better per follower than celebrities, whose audiences follow them for
entertainment.

## Tiers

| Tier | Followers |
|---|---|
| Nano | under 10K |
| Micro | 10K-100K |
| Macro | 100K-1M |
| Mega | over 1M |

Tools may cut tiers differently (one discovery tool uses micro 10K-50K, mid
50K-500K); state the cut you use.

## Metrics

| Metric | Formula | Stage |
|---|---|---|
| Reach | unique people who saw the post | Awareness |
| Impressions | times displayed | Awareness |
| Engagements | likes + comments + shares + reactions | Consideration |
| Engagement rate | engagements / followers x 100 | Consideration |
| Conversion | tracked purchases, leads, code redemptions, link clicks | Conversion |
| CPA | fee / conversions | Conversion |
| Profit per post | conversions x margin - fee | Decision |
| POAS | (margin x conversions - fee) / fee, equivalently (margin - CPA) / CPA | Decision |

Saves, meaningful comments, click-through and video completion signal more
intent than likes.

## Cost

Benchmarks run around $10-20 per post per 1,000 followers, varying by format
and platform. At similar follower counts, Instagram fees run several times
TikTok fees (published rate cards: TikTok micro $25-125, Instagram micro
$100-500 per post); YouTube and Facebook higher per piece. Compare cost per
post before outcomes.

## Analysis procedure

1. Build profit per post and POAS per creator from fee, attributed orders and
   margin per order (ask for margin).
2. Group by platform x tier x code. Rank groups by POAS (efficiency) and
   profit per post (absolute contribution). Orders per post alone favours big
   creators and misleads.
3. Code effect by tier: lift % in orders with vs without a code inside each
   follower band. A regression of orders on code, followers, platform and
   code x followers tests whether the code effect shrinks with size.
4. Engagement drivers: engagement rate on platform, followers, code. Avoid
   putting historical engagement rate together with followers or fee as
   regressors (strongly correlated).
5. Profit curves across follower bands are often inverted U; find the band
   where profit per post peaks per platform and where it turns negative.
6. Recommend: concentrate on the platform x tier x code cells with the best
   POAS; cut cells with negative profit; keep bigger creators only where the
   job is reach and is measured on reach.

## Caveats

- Code or link orders are attributed, not proven incremental, and miss buyers
  who saw the post but did not use the code.
- Audience quality: audit suspicious followers (audience quality scores);
  even very large accounts can carry a large share of suspicious followers.
- Check audience fit: follower demographics, psychographics, content style,
  values, engagement rate.
- Match content to funnel stage: hauls and hashtags for reach; tutorials and
  reviews for engagement; testimonials, offers and codes for sales.
- Long-term partnerships build trust that one-off posts do not; give
  creators creative room with review checkpoints.
- Measurement must scale with budget: UTMs, codes, landing pages.

## Social posting context

Median engagement by followers (RivalIQ 2024): TikTok 1.73%, Instagram 0.36%,
Facebook 0.04%, X 0.015%, falling across platforms. Reach counts people,
impressions count displays. Social is a channel serving an objective, not a
goal; platform choice follows where the audience is, the interaction wanted,
and whether you can produce native-quality content.

---

## File: channel-audit/references/paid-search-economics.md

# Paid search and PPC economics

PPC is a pricing and bidding mechanism, not a channel: it runs search, display,
video and remarketing. SEM = PPC (paid) + SEO (unpaid). Spending on ads does
not lift organic rank.

## The auction

- Every query runs an auction. Ad Rank = max CPC bid x Quality Score; the
  highest bidder does not always win.
- Quality Score (1-10) = expected CTR + ad relevance + landing-page
  experience. Roughly: QS 10 about 50% lower CPC; QS 1 about 400% higher
  CPC than the neutral middle.
- Actual CPC = (Ad Rank of the advertiser below / your QS) + 0.01. You pay
  enough to beat the next ad, usually well under your max bid; a higher QS
  lowers the price for the same position.

## Metrics by layer

| Layer | Metrics | Broken means |
|---|---|---|
| Visibility | impressions, impression share, top impression rate, IS lost to rank, IS lost to budget | Rank: quality or bid. Budget: money |
| Attractiveness | clicks, CTR | Copy, extensions, targeting, offer |
| Profitability | conversions, CVR, CPA, ROAS, POAS | Landing page, offer, audience-message match, price |

Universal: CTR = clicks / impressions; CVR = conversions / clicks; CPC = cost
/ clicks; CPA = cost / conversions. ROAS = conversion value / spend. POAS
uses profit (margin) instead of revenue and is the number that matters when
products carry different margins.

## Break-even maths

```
Break-even CPC = margin per conversion x CVR
Profit per campaign = conversions x margin per conversion - cost
Break-even ROAS = 1 / gross margin rate
```

Worked shape (not from a case): margin $30 per order, CVR 4% gives a
break-even CPC of $1.20; paying $1.50 loses $0.30 per click on average.

## Reading impression share

| IS lost to budget | IS lost to rank | CPC vs break-even | Do |
|---|---|---|---|
| High | Low | Below | Raise budget: profitable demand left on the table |
| High | Low | Above | Do not add budget; cut bids or fix CVR first |
| Low | High | Below | Improve QS (relevance, landing page); bid up only while CPC stays under break-even |
| Low | High | Above | Fix quality or pause; bidding up makes losses larger |

## Structure

Account -> campaigns (budget, geo, schedule, network; one goal each) -> ad
groups (one tight theme: related keywords, tailored copy, dedicated landing
page, negatives). Negative keywords block waste and stop your own ad groups
competing. One ad group with hundreds of unrelated keywords drags relevance,
QS and CPC.

## Assets

Headlines carry the keyword; descriptions = keyword + value proposition + call
to action; extensions (sitelinks, callouts, promotions) raise CTR and QS. The
platform rotates the combinations you supply.

## Benchmarks (WordStream 2024, ~17,000 campaigns)

Search CTR about 3.17%, display about 0.46%; average CVR near 7%; display CPC
around $0.63 vs several dollars on search. For buying-intent keywords, ads
take about 65% of clicks vs 35% organic.

## Brand keywords

Brand terms show low CPC and high QS, and look like the best campaign. A
well-known marketplace experiment found branded paid clicks largely
non-incremental (organic would have caught them). Arguments to keep them:
blocking competitors, message control. Verdict: test incrementality before
deciding (see `evidence-check` pause tests).

## Platforms

Google Ads (search, display, YouTube, shopping); Meta (interest and lookalike
targeting); Microsoft Ads (older, higher-income desktop audience, cheaper
clicks, fewer competitors); TikTok; LinkedIn (B2B job targeting); X.

---

## File: channel-audit/references/seo-search-visibility.md

# Search visibility: SEO, links, local, AI answers

Search engines crawl, index, then rank on two broad dimensions: relevance
(keywords on the page, on-site) and quality / popularity (user experience
on-site, links off-site). Four pillars: on-site, off-site, technical, local.
Top three organic results take about 68.7% of clicks (39.8%, 18.7%, 10.2%).
Organic is slow, compounding and unpaid per click; it often carries most site
traffic.

## Keyword selection ("pick your battle")

| Factor | Rule |
|---|---|
| Intent | Awareness ("what is", "how to"), consideration ("best X for", "A vs B", reviews), action ("sale", "discount", "near me"). Cover the funnel; action terms often go to paid search |
| Volume | Among interchangeable terms, higher volume wins |
| Competition | If the top results are mature, high-authority, optimised pages, a smaller site will not move; prefer long tail (about 70% of searches; easier to rank) |
| Current rank | 4-20: biggest return. 1-3: maintain. 50+: too far for this quarter |

Map each keyword to exactly one page; broad terms to top pages, specific
terms to deeper pages. Two of your pages ranking for one keyword is
cannibalization: pick the one page that should own it and re-target the other
page at a different keyword. Do not assign a
hard keyword to a weak new page.

## On-page

Keyword in six places: URL, title tag (heavily weighted, under about 60
characters), H1 and an H2, body (the course guidance is 3-5% density, 10% at
most; avoid stuffing), image alt text and file name, internal anchor text.
Quality signals: compelling meta description, fast pages, original fresh
substantial content, engagement, mobile-friendly, HTTPS.

## Off-site (links)

Popularity factors, roughly in order: number of backlinks, relevance of
linking domains, anchor text relevance, link neighbourhood (no spam
clusters), freshness (steady new links), diversity (many referring domains),
social sharing.

Audit: domain and page authority, linking domains, followed links, net
discovered vs lost links, spam score (1-30% low, 31-60% investigate, 61-100%
high: disavow spammy links), compare with 1-2 competitors. Link value:
editorial (earned; link bait such as original data, tools, infographics,
guides) > manual (directories with high authority and relevance, profiles,
partners, unlinked mentions) > manufactured (comment spam, link farms,
satellite sites: no value, risk of penalty).

## Local

Map results rank business profiles, not pages. Factors: Google Business
Profile (accurate primary category, name, linked landing page strength;
photos, posts, Q&A and hours drive conversion), NAP consistency (name,
address, phone identical on site, profile and directories, down to "St" vs
"Street"), structured citations (claimed listings on major general and
industry directories; accuracy, distribution, quality, relevance),
reviews (rating, recency, velocity, platform diversity, reviewer authority,
text over stars; respond to all), on-page local terms and NAP, local links,
behavioural signals (clicks to call, directions, site), proximity of the
searcher (uncontrollable). Negative: guideline violations including
duplicates others create, unanswered negative reviews, inconsistent NAP,
spam citations, abandoned profiles.

Diagnose "not in the map pack" against this list: category, NAP
consistency, unclaimed or duplicate listings, review recency and velocity,
profile landing page; then note that searcher proximity is outside your control.

## AI answers (GEO)

SEO earns a rank; GEO earns a citation, often with no click. Levers:
authority (earned third-party coverage beats owned content; named expert
quotes), community (presence in forums, reviews, Q&A threads), structure
(question-style headings matching how people ask, the direct answer in the
first 40-60 words of a section, bullets, a verifiable statistic every
150-200 words, schema, clean HTML, freshness). Pages that already rank are
the ones models tend to cite, so run GEO with SEO. AI-referred sessions grew
fast in 2025; measure them separately (see the diagnose emerging playbooks).

## SEO report metrics

Organic traffic and MoM change, average position, keywords in top 5,
followed backlinks, organic conversion rate, notable new links.

---

## File: channel-audit/references/site-funnel.md

# On-site funnel and conversion optimisation

Web analytics follows the journey in three acts: acquisition (who arrives,
from where), exploration (what they do), goal (did they convert). Always
optimise against the site's primary conversion.

## Definitions

| Term | Definition |
|---|---|
| Users | Distinct visitors (cookie-based) |
| New / returning | First visit in period vs seen before; the ratio shows acquisition vs retention balance |
| Session | Ends after 30 minutes inactive, at midnight, or on a return via a different source |
| Engaged session (GA4) | Over 10 seconds, or 2+ page views, or a key event |
| Engagement rate | engaged sessions / sessions |
| GA4 bounce rate | share of sessions not engaged (UA bounce was single-page sessions; not comparable) |
| Pageviews vs unique pageviews | every load vs sessions with the page at least once |
| Purchase conversion rate | purchases / sessions |

UA bounce benchmarks (ecommerce): 40% or lower good, 40-70% average, above 70%
high. Ecommerce conversion averages about 2.6% (Walmart about 5%; Amazon
non-Prime about 10%, Prime members far higher), so loyalty programmes move
the benchmark.

## Primary conversion by site type

Ecommerce: purchases. Lead generation: calls and form submissions. Media (ad
model): pageviews, time, visit duration. Media (subscription): paid sign-ups.
Revenue levers after conversion: AOV (upsell, cross-sell, bundles,
free-shipping thresholds, subscriptions, personalised recommendations).

## Traffic sources

Direct (typed URL, bookmarks, apps; strong brand), search (paid and organic),
referral (organic social, backlinks, earned media; paid display, social ads,
influencers, sponsored content). Not all visits are equal: judge sources on
engagement and conversion, not volume. Rising organic often lifts referral,
social and direct as knock-on effects.

## Funnel read

Steps: product view, add to cart, begin checkout, shipping, payment,
purchase. Cart abandonment benchmark about 70%; 60% would be very good.

1. Compute step-to-step completion; the largest absolute loss of would-be
   buyers is the first target.
2. Check whether the funnel is open (users can enter mid-way) or closed;
   step completion is not journey success.
3. Cut by device and channel before concluding (a mix shift moves blended
   rates; see `evidence-check` on Simpson's paradox).
4. Map causes to the step: hidden costs (shipping, tax), long or repeated
   forms, unexpected delivery time, security doubts, no guest checkout,
   complicated flow, missing payment method.
5. Every page fix is a hypothesis until tested (`evidence-check` for test
   reading).

CRO levers: landing page clarity, ad-to-page message match, speed, form and
checkout friction, trust signals, offer framing. More traffic is not a better
rate; landing-page clicks are not business value.

## Channel blend

Awareness: social, display, content. Consideration: search ads, retargeting,
email. Conversion: landing pages, checkout, remarketing to known contacts.

---

# Skill: brand-health

---
name: brand-health
description: >-
  Use this skill when the question is about the brand rather than one campaign: "is
  our brand getting stronger or weaker", "is our brand healthy", awareness,
  consideration or preference from a tracker or survey, brand search volume, direct
  traffic as a brand signal, share of voice or share of search, social mentions and
  sentiment, "are promotions hurting the brand", baseline sales, price premium or "can
  we raise prices", "should we cut brand ads and put it into performance", a flat
  brand score, NPS up but repeat purchase down, "should we launch [product] under our
  brand", line or category extension, sub-brand, repositioning, rebrand, "milk or kill
  this brand", brand valuation, and whether content is on-brand. It measures brand
  health from the data, separates short-term sales from long-term equity, checks per
  segment, and turns the result into a decision with a way to verify it.
---

# brand-health

Brand questions get answered with the wrong number more often than most:
a total that hides the segment that matters, a sales spike that hides a
falling baseline, a growing search volume that hides a shrinking share. This
skill measures brand health from data and turns it into a decision. Compute
every number in code. Volume next to every rate.

Related skills: the `diagnose` skill holds the qualitative brand-strategy
states (diagnose/references/brand-diagnostic.md); use it to name the state
after this skill has measured it. Use `metric-definitions` for formulas of
CLV, CAC, repeat rate and engagement rate, and `evidence-check` for
significance tests, holdouts and pull-forward.

## 0. The human owns the question and the decision

Before any analysis, confirm two things with the user. Do not assume them.

1. **The decision.** What will change depending on the answer (budget split,
   price, launch, discount calendar, rebrand)? If none, say the analysis is
   monitoring, not a decision.
2. **The frame.** Which competitors, which category terms, which customer
   segments, which period. A brand is healthy only relative to a frame.

If either is missing and cannot be read from the data, ask one short
question listing your default (for example "I will compare against the three
brands in the file and treat 2024 as the baseline year: right?").

## 1. Route the question

| The user asks | Go to | Depth in |
|---|---|---|
| Is the brand getting stronger or weaker? | §3 scorecard, then §5 | health-metrics (section "File: brand-health/references/health-metrics.md" in 08-pricing-channels-brand.md) |
| Are promotions or discounts hurting us? Promotions "work better than ever"? | §4 long view | long-view (section "File: brand-health/references/long-view.md" in 08-pricing-channels-brand.md) |
| Brand vs performance budget, cut brand ads? | §4, then `evidence-check` §4 | long-view (section "File: brand-health/references/long-view.md" in 08-pricing-channels-brand.md) |
| Brand score, NPS or preference flat or up, but sales or repeat down (or the reverse) | §5 per customer | per-customer-equity (section "File: brand-health/references/per-customer-equity.md" in 08-pricing-channels-brand.md) |
| Search, mentions, sentiment, share of voice moved | §3 rows 4 to 8 | health-metrics (section "File: brand-health/references/health-metrics.md" in 08-pricing-channels-brand.md) |
| Can we raise prices / is our premium safe? | §3 row 9, §4 | long-view (section "File: brand-health/references/long-view.md" in 08-pricing-channels-brand.md) |
| Is this content, claim or campaign on-brand? Is our positioning clear? | §6 | positioning-content (section "File: brand-health/references/positioning-content.md" in 08-pricing-channels-brand.md) |
| Extension, sub-brand, reposition, rebrand, milk/prune/sell, brand value | §7 | architecture-moves (section "File: brand-health/references/architecture-moves.md" in 08-pricing-channels-brand.md) |

## 2. What the data must contain

| Question | Minimum data | If missing |
|---|---|---|
| Health trend | the same metric at the same grain for at least two comparable periods, plus one competitor or category series | report levels only; say "no trend or benchmark, no verdict" |
| Promotions vs baseline | weekly (or daily) units or revenue with a promo flag or discount amount, 8+ quarters ideally, at least 4 | if no promo flag, infer promo weeks from discount_amount > 0 and say so |
| Survey / tracker | respondent-level rows with segment, wave, and the scores; n per wave | aggregate-only scores: report, but refuse a segment verdict |
| Share of voice / search | own and competitor mentions or brand-term volumes, same source and period | own-only volume cannot show share; say growth may be category-wide |
| Extension or reposition | intent or fit scores split by current customer vs not, and by segment | refuse a go/no-go from one average |
| Valuation | branded price, generic price, units, assumptions | refuse a single number; give a range |

Refuse or caveat: a causal claim from a tracker alone (attitudes do not
equal behaviour); a verdict on a survey change smaller than its sampling
error (test it as a proportion with `evidence-check` §1.2); a perceptual map
from fewer than about 100 respondents; direct traffic read as pure awareness
(it also counts bookmarks and app opens).

## 3. The brand health scorecard

Compute each row that the data allows, per period, own brand and benchmark.

| # | Metric | Formula | Healthy reading | Trap |
|---|---|---|---|---|
| 1 | Aided / unaided awareness | aware respondents / respondents, per wave | rising or stable vs competitors | awareness is potential, not equity |
| 2 | Funnel conversion | consideration / awareness, preference / consideration, repeat / trial | find the stage with the biggest drop: that is the bottleneck | comparing stage levels instead of stage ratios |
| 3 | Repeat rate without promotion | customers repeating at full price / customers | stable or rising | repeat driven by coupons is not loyalty |
| 4 | Share of search | own brand-term volume / (own + competitor brand-term volumes) | stable or rising | own volume up while share falls = category tide |
| 5 | Brand vs category demand | own brand-term volume / generic category-term volume | stable or rising | seasonal category swings |
| 6 | Share of voice | own mentions / all mentions (own + competitors), same tool | stable or rising | tagged mentions only; untagged and misspelled count too |
| 7 | Net sentiment | (positive - negative) / all mentions; plus negative mentions by topic tag | stable or rising; no topic driving negatives | volume growth read as "buzz" when it is complaints |
| 8 | Engagement quality | shares / reach and comments / reach, next to likes / reach | shares growing | likes are the cheapest signal; impressions are not reach |
| 9 | Price premium | own average paid price / category or private-label average price - 1 | stable or rising at stable volume | list price instead of paid price |
| 10 | Promo dependence | revenue in promo periods (or discounted orders) / total revenue | below 40% | above 40% the brand is training deal-seekers |
| 11 | Baseline sales | average non-promo-week sales per quarter | flat or rising | see §4 |
| 12 | Customer equity | sum of CLV across active customers (or active customers x CLV per segment) | rising | brand score up while this falls |

Read the scorecard as a whole: the verdict is the direction most rows agree
on, after §5 has checked that no segment reverses it.

## 4. Short term vs long term (the long view)

Run this whenever promotions, discounts or a brand-vs-performance budget
are in the question. Full method in long-view (section "File: brand-health/references/long-view.md" in 08-pricing-channels-brand.md).

1. Flag promo weeks (promo flag, or discount_amount > 0). Keep the 1 to 2
   weeks after each promotion separate (pull-forward, see `evidence-check`).
2. Per quarter: **baseline** = mean sales in non-promo weeks; **lift** =
   mean promo-week sales / that quarter's baseline; **promo share** = promo
   revenue / total revenue.
3. Trend each across quarters (slope, and first vs last quarter).
4. Read the pattern:

| Baseline | Lift | Reading | Action |
|---|---|---|---|
| falling | rising | customers trained to wait for deals; promotions look better because the base eroded | cut promo frequency and depth, protect baseline, expect a short dip first |
| falling | flat or falling | brand erosion or category decline | compare with category (§3 rows 4 to 6) before blaming promotions |
| flat or rising | stable | healthy | keep calendar; test one fewer promotion |
| rising | falling | equity building | do not add discounts |

5. Price sensitivity: estimate it on quarterly, not weekly, aggregates
   (weekly data overstate it several-fold because of stockpiling). Rising
   sensitivity over quarters means the premium is eroding.
6. Brand budget questions: a short attribution window misses most brand
   effects, and brand ads keep working after they stop. Do not cut brand
   spend on short-window ROAS; propose a geo or time holdout read on
   baseline sales and branded search over at least two quarters.
7. Remember the triangle: equity, share and short-term profit cannot all be
   maximised at once. Say which one the recommendation trades away.

## 5. Per customer, never only the average

A single brand score averaged over all respondents is true of nobody.

1. Split every survey or tracker metric by segment (customer vs
   non-customer, value tier, tenure, region) and by wave. Report n per cell
   and test each change for sampling error before calling it.
2. Weight by value, not headcount, before a verdict: weight each segment's
   score change by its share of CLV or revenue. A stable average with a
   falling high-CLV segment is a decline.
3. Check composition: if the respondent mix changed between waves, compare
   at a common mix (as in `evidence-check` §3).
4. Check behaviour against attitude: stated preference or NPS up while
   repeat rate or share of wallet falls means trust the behaviour.
5. Use rank or relative scores across brands, not absolute scale points
   (one person's 6 is another's 4).
6. Name which equity drives choice in this category (value, brand or
   relationship) before recommending a brand investment; see
   per-customer-equity (section "File: brand-health/references/per-customer-equity.md" in 08-pricing-channels-brand.md).

## 6. Positioning and content checks

Use positioning-content (section "File: brand-health/references/positioning-content.md" in 08-pricing-channels-brand.md) when the
question is "is this on-brand", "why are we known but not chosen", or a
claim review. In order:

1. **Frame:** does the customer place us in the intended category? (search
   queries, comparison sites, who we are compared with).
2. **Points of parity:** list the category must-haves; rate each 1 to 10
   (survey or reviews). Any below 7 is a disqualification risk: fix before
   promoting a difference.
3. **Points of difference:** relevant, distinctive ("only", not "best"),
   believable (one provable reason to believe), deliverable (feasible,
   profitable, hard to copy).
4. **Content:** score each piece against the brand's chosen personality
   dimension (sincerity, excitement, competence, sophistication, ruggedness)
   and archetype; flag pieces that express another one, claims without
   proof, and SEO targets that pull an off-brand audience.

## 7. Architecture and growth moves

Use architecture-moves (section "File: brand-health/references/architecture-moves.md" in 08-pricing-channels-brand.md). Decision rules:

| Move | Decide on | Rule |
|---|---|---|
| Extension | intent and fit split by current core customers vs others | same brand only if the extension's buyers resemble current customers; similar product but different customers fails; core-customer permission below 6/10 means sub-brand or new brand |
| Line vs category extension | cannibalization (share of extension sales taken from the core) vs incremental | line extensions: watch cannibalization; category extensions: watch permission and spillover risk |
| Reposition | trigger severity (blip, cyclical, structural, existential) | blips and cycles do not justify repositioning; move in steps inside the latitude of acceptance; identity brands use a sub-brand |
| Rebrand | evidence the experience has changed | a new name without new experience keeps the old associations |
| Decline | brand health x market health | strong/strong invest; strong brand, weak market milk; weak brand, strong market fix or sell; weak/weak prune; try reposition, extension and new markets before milking |
| Valuation | price-premium NPV with ranges | always show the sensitivity to discount rate, brand share of premium and growth |

## 8. Adversary for every move

Run the attack for each step you used. A step whose check fails is redone
or downgraded as the last column says.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Accept the question | Is this the decision the user is making, and the frame they mean? | §0 answers on record (decision, competitors, period, segments) | ask the one question; do not proceed on a guess |
| Compute a metric | Is the numerator and denominator from the same source, grain and period? | recompute one total two ways (sum of rows vs reported total) | fix the grain or join and recompute |
| Call a trend | Is the change larger than noise and not a season? | proportion test for survey changes; same period last year for search and sales | label "no detectable change" |
| Credit or blame the brand | Did the category or competitors move the same way? | share of search, share of voice, own vs category index (§3 rows 4 to 6) | reframe as category movement |
| Read an average | Does any segment, especially the high-value one, move the other way? | §5 split and CLV weighting | report the segment, change the verdict |
| Trust a survey | Does behaviour agree with the attitude? | repeat rate, share of wallet, baseline sales in the same period | trust behaviour; mark the attitude result as unconfirmed |
| Judge a promotion | Is the lift real growth or a falling base? | baseline and lift trend by quarter (§4) | rewrite the verdict around baseline |
| Read a mentions spike | Is the growth positive talk or complaints? | negative share and topic tags before vs after | report it as an issue, route to service or product |
| Name a cause | What else produces the same pattern? | list two rivals and the data that rules each out | label it a hypothesis and name the test |
| Approve an extension or reposition | Who exactly says yes: our customers or others? | intent split by current core vs non-customers; latitude check | recommend sub-brand, new brand, or a smaller step |
| Recommend | What does it cost if this is wrong, and what would the CFO ask? | downside in money or customers, and a verification test with a date | add a holdout or shrink the bet |
| Put a value on the brand | How much does the number move with the assumptions? | sensitivity table (discount rate, brand share of premium, growth) | give a range, not a point |

## 9. Score-and-probe gate before handover

1. Every adversary check in §8 for the steps used must pass (or be
   explicitly downgraded in the text). Do not score a draft that still
   has a failing check.
2. Score the draft 0 to 100 on four criteria: **clarity** (one verdict, plain
   words, numbers a reader can redo), **relevance** (answers the user's
   decision, in their frame), **depth** (benchmark, segments and long-term
   view covered where the data allows), **insightfulness** (says something
   the headline number did not).
3. If any score is below 80, write the probe question that would raise it
   (for example "which segment drives the flat score?"), answer it from the
   data, revise, and re-score. Maximum two loops; after that, ship and list
   what is still weak.
4. End by naming what the human must decide: the question and the
   decision stay theirs. State the trade-off they are choosing.

## 10. Output format

```
Verdict: [brand stronger / weaker / no detectable change / inconclusive]: [one line]
Deciding number: [e.g. "baseline sales -18% over 6 quarters while promo lift rose 1.3x -> 1.9x"]
What the headline number says and why it misleads: [one line]
Benchmark: [own vs category / competitors]   Segments: [the one that matters]
Action: [what to do] · Trade-off: [equity vs share vs short-term profit]
How to verify: [test, metric, date] · Your decision: [the choice left to the user]
```

Keep a short table of the computed checks under the verdict so the reader
can redo the arithmetic.

---

## File: brand-health/references/architecture-moves.md

# Architecture and growth moves

Contents: [Architecture](#arch) · [Extensions](#ext) · [Repositioning and rebranding](#repo) · [Portfolio roles and decline](#decline) · [Partners and licensing](#partners) · [Brand valuation](#value)

<a id="arch"></a>
## 1. Architecture

| Factor | Favour branded house (umbrella) | Favour house of brands |
|---|---|---|
| Marketing budget | limited | substantial |
| Brand meaning | broad, transferable | narrow, specific |
| Category similarity | high | low |
| Target overlap | high | low |
| Quality control across lines | strong | variable |
| Tolerance for spillover | can accept it | needs insulation |

Umbrella risk: one failure in one category hurts every category. House of
brands cost: each brand is built separately. Endorsed sub-brands sit in
between, and the endorsement can flow both ways over time.

Customer-centred rule: build brands around customer segments, keep brands
as narrow as is economic, and let customers move between the firm's brands
when that raises their CLV.

<a id="ext"></a>
## 2. Extensions

**Decide on customer similarity, not product similarity.**

| New product's customers vs ours | Product vs ours | Outcome |
|---|---|---|
| similar | similar | best case |
| similar | different | can work (shared customer identity carries the brand) |
| different | similar | fails: same product, wrong customers |
| different | different | treat as a new brand |

Data method:
1. Survey intent ("how likely to buy [extension] from [brand]", 0 to 10)
   and fit ("does this feel like [brand]") with customer status and segment.
2. Split by current core customers vs non-customers vs other segments.
   An average high only because non-customers like the idea is not brand
   permission. Core-customer intent below 6/10 means limited permission:
   use a sub-brand or a new brand.
3. Profile who says yes (demographics, needs, CLV tier) and compare with
   the current customer base.
4. Check parity points of the new category first (Nivea deodorant had to
   stop odour before "gentle" mattered).

| Type | Risk | Watch |
|---|---|---|
| Line extension (same category) | low | cannibalization: share of extension sales taken from the core; SKU confusion |
| Category extension (new category) | high | permission, capability, spillover of failure onto the parent |
| New brand / sub-brand | cost | needed when identity or status differs (Toyota to Lexus, Honda to Acura) |

Success metrics for an extension: incremental revenue (not gross), equity
transfer (awareness and associations in the new category), cannibalization
rate, and parent-brand health after launch.

<a id="repo"></a>
## 3. Repositioning and rebranding

**Is repositioning warranted?**

| Trigger | Severity | Action |
|---|---|---|
| temporary blip | low | wait and monitor |
| cyclical pattern | medium | tactical adjustment |
| structural shift (demographics, category disruption, competitors took the POD) | high | consider repositioning |
| existential threat | critical | reposition or exit |

Levers (one at a time where possible): target / occasion / place; value
claim (add, do not contradict); evidence; competitive frame.

Rules:
- Evolutionary steps with bridge positions; each message at the edge of
  the audience's latitude of acceptance. Messages in the rejection range
  backfire.
- Identity brands (gender, status, age, culture): ego involvement is
  highest and the acceptable range narrowest. Use a sub-brand, an endorsed
  brand or a separate brand rather than moving the core.
- Measure during the transition: retention of current customers,
  awareness and association shift in the new target, price premium.
- Rebranding (name, logo) without a changed experience leaves the old
  associations in place; reposition first, rebrand after, if at all.
- Erosion is unintended decline; repositioning is a chosen change. Do not
  call erosion a repositioning.

<a id="decline"></a>
## 4. Portfolio roles and decline

Roles: flagship (volume, funds the rest), premium flanker, fighter (blocks
low-price rivals without moving the flagship down), entry-level, prestige.

| Brand health | Market health | Action |
|---|---|---|
| strong | strong | invest |
| strong | weak | milk (cut support, protect margin) |
| weak | strong | fix or sell |
| weak | weak | prune |

- First decide brand decline vs category decline: compare with
  competitors and category demand.
- Try reposition, extension, new markets and fighter brands before milking;
  premature milking accelerates decline.
- Milking: set margin targets, cut support step by step, watch retention.
- Keep products that fail on their own P&L when they have strategic,
  symbolic, assortment or synergy value, or still cover overhead.
- No heroic measures for a dying brand: if customer equity rises when its
  customers move to other brands in the portfolio, retire it.
- Phase out gradually to migrate customers inside the portfolio; kill at
  once only when the bleeding outweighs the migration.

<a id="partners"></a>
## 5. Partners, licensing, co-branding

- Licensing and co-branding expose the brand to quality and scandal risk it
  does not control: require quality standards, approval rights, audits and
  exit clauses.
- Co-branding works best between equals in equity; check fit, target
  overlap and risk tolerance.
- Channel behaviour is brand behaviour: bait-and-switch or discount
  outlets damage meaning (Pioneer, Lacoste).

<a id="value"></a>
## 6. Brand valuation

Three methods: sale or auction (most objective, rare), goodwill from an
acquisition (mixed with other intangibles), price-premium NPV (most used,
most assumptions).

Price-premium NPV:
1. `premium per unit = branded price - generic price`
2. `incremental revenue = premium x units`
3. `brand revenue = incremental revenue x brand share of premium` (the
   share due to brand, not quality or distribution; often assumed 60 to 80%)
4. Project 5 to 10 years with a growth rate.
5. `NPV = sum(brand revenue_t / (1 + r)^t)`, r typically 8 to 12%.
6. `terminal value = final-year brand revenue x (1 + g) / (r - g)`,
   discounted back.

Always publish a sensitivity table: discount rate (8% vs 12% can move the
value by about 40%), brand share of premium, growth rate and horizon.
Professional valuers give very different numbers for the same brand for
exactly this reason. Brand value (money) is not brand equity (customer
minds); strong equity becomes value only if it is monetised as a premium
or volume.

---

## File: brand-health/references/health-metrics.md

# Brand health metrics: what to track, where it comes from, how it lies

Contents: [Buckets](#buckets) · [Survey metrics](#survey) · [Behavioural metrics](#behaviour) · [Search and traffic](#search) · [Social](#social) · [Price and money](#money) · [Tracking design](#tracking) · [Small-brand kit](#small)

<a id="buckets"></a>
## 1. The five buckets

A brand dashboard needs at least one metric from each bucket. A dashboard
that tracks only sales misses the early warnings.

| Bucket | Question it answers | Typical metrics |
|---|---|---|
| Awareness / salience | do people think of us at all? | aided and unaided awareness, recognition, entry into the consideration set, branded search |
| Attitudes / associations | what comes to mind, and is it ours? | association strength, perceived quality, uniqueness ("only brand that..."), sentiment |
| Behaviour | do they buy, repeat, recommend? | trial, repeat at full price, share of wallet, switching, advocacy |
| Relationship quality | is trust holding? | satisfaction, complaint volume and topics, NPS |
| Financial | does the brand earn money a generic would not? | price premium, promo dependence, CLV, customer equity, brand value trend |

Awareness signals potential; loyalty (repeat, share of wallet) signals
realised equity. A dashboard heavy on awareness and light on behaviour
over-reports health.

<a id="survey"></a>
## 2. Survey and tracker metrics

- **Awareness levels:** unaided recall (top of mind), aided recall,
  recognition. Report each as a share of respondents per wave with n.
- **Funnel ratios (Keller pyramid read as a funnel):** salience, meaning,
  response, resonance. Compute stage-to-stage ratios: consideration /
  awareness, preference / consideration, trial / preference, repeat / trial,
  advocacy / repeat. The bottleneck is the lowest ratio relative to a
  competitor's ratio at the same stage, not the lowest level.
- **Perceived quality and associations:** rate own and competitor brands
  on the same attributes; read relative position (rank or gap to the leader)
  rather than absolute scores, because scale use differs between people.
- **Significance:** a wave-to-wave change in a share (awareness 34% to 37%)
  is a two-proportion comparison; run the test in `evidence-check` §1.2 and
  call it "no detectable change" when it fails.
- **Attitude-behaviour gap:** people do not always act on their stated
  attitudes, even when they believe they would. Always pair a tracker with
  one behavioural series from the same period.
- **Survey fatigue:** long attribute batteries produce random answers;
  prefer 6 to 10 attributes.

<a id="behaviour"></a>
## 3. Behavioural metrics

- **Repeat purchase rate at full price:** customers with a second
  non-discounted order / customers with a first order, by cohort. Compute the
  cohort correctly (only cohorts old enough; see `metric-definitions` rule 17).
- **Share of wallet / share of customer:** own category spend / customer's
  total category spend (needs panel or survey data). Customer-centred brands
  manage this instead of share of market.
- **Promo dependence:** revenue from promo periods or discounted orders /
  total revenue. Above 40% means customers are being trained to buy only on
  deal.
- **Customer equity:** sum of CLV over active customers, across all the
  firm's brands. It can fall while brand scores rise (the base is shrinking
  or shifting to low-value customers).
- **CLV to CAC:** is acquisition sustainable; formulas in `metric-definitions`.

<a id="search"></a>
## 4. Search and traffic as brand signals

| Signal | Formula | What it tells you | Trap |
|---|---|---|---|
| Branded search volume | monthly searches for brand terms (Search Console impressions on brand queries, Keyword Planner, Trends) | people looking for you, not the category | volume grows with the whole category and with seasons |
| Share of search | own brand-term volume / sum of brand-term volumes for own + named competitors | your share of brand-seeking demand; the share-of-voice formula applied to search | competitor list must be the same every period |
| Brand vs category index | own brand-term volume / generic category-term volume | are you gaining or losing within your category's demand? | category terms must be fixed in advance |
| Direct traffic | GA4 direct sessions | partly brand recall | also includes bookmarks, app opens and untagged links; a new app or broken UTMs inflate it |

Read search in this order: own volume, then share of search, then index vs
category. If own volume rose but share fell, competitors rose faster: the
category grew, the brand did not. Compare the same months year on year
before reading a trend.

<a id="social"></a>
## 5. Social signals

- **Reach vs impressions:** reach = unique viewers; impressions = times
  shown. Never present impressions as audience size.
- **Engagement ladder:** clicks and likes are cheap; comments show
  interaction; shares put the brand in front of someone else's audience and
  are the strongest resonance signal. Engagement rate = engagements / reach,
  computed from summed parts.
- **Share of voice:** own mentions / all mentions (own + competitors) in
  the same listening tool and period. Include untagged and misspelled
  mentions; tagged-only counts miss most conversation.
- **Sentiment:** classify positive, negative, neutral; net sentiment =
  (positive - negative) / all. Track it over time and against competitors.
- **Topic tags:** tag mentions and inbound messages by topic (support issue,
  product feedback, pricing, delivery, feature request). Report tag volumes
  and trends: they show what drives negative vs positive sentiment.
- **Brand-specific or category-wide?** Only a competitor benchmark can tell.
  A rise in mentions that competitors share is a category event.

<a id="money"></a>
## 6. Price and money

- **Price premium:** own average paid price / generic or category average
  paid price - 1. Use paid (transaction) prices, not list prices.
- **Price sensitivity:** % volume change / % price change at regular price,
  estimated on quarterly data (see long-view.md). A rising trend means the
  premium is weakening.
- **Price test:** raise price 5 to 10% in a test cell or period and measure
  the volume lost; it is the cheapest direct read of brand strength.
- **MROI:** gross profit delivered by the product / marketing spent on it.
- **Brand value:** see architecture-moves.md §6; always a range.

<a id="tracking"></a>
## 7. Tracking-study design

| Design question | Why |
|---|---|
| What is the baseline period? | without it, change is vague |
| How often is it measured? | too sparse misses movement; too frequent is noise |
| Which segments are kept separate? | averages hide drift |
| Which touchpoints are included? | meaning forms across encounters, not ads alone |
| What action will each metric trigger? | a metric that triggers nothing is dead weight |

Keep raw data for years: brand trajectories need long series.

<a id="small"></a>
## 8. Small-brand kit (no paid tracker)

| Track | Free source | Tells you |
|---|---|---|
| Repeat rate without promotion | Shopify / POS / email purchase history | do customers come back without a deal? |
| % of revenue from promotions | own sales data | above 40% = training deal-seekers |
| Sentiment and user content | listening tools, reviews | is the story resonating, or only the price? |
| Direct traffic and branded search | GA4, Search Console | are people seeking you or the category? |
| Price elasticity | occasional 5 to 10% price tests | how much volume a price rise costs |
| CAC vs CLV | basic finance data | is growth sustainable? |

---

## File: brand-health/references/long-view.md

# The long view: promotions, baseline and brand budget

Contents: [Why short-term data mislead](#why) · [Baseline method](#method) · [Price sensitivity](#sensitivity) · [Brand vs performance budget](#budget) · [The triangle](#triangle) · [Patterns](#patterns)

<a id="why"></a>
## 1. Why short-term data mislead

Real-time sales data make promotions look very profitable: the spike is
visible this week, while the cost (lower future baseline, lower price
premium, competitor retaliation) arrives later and is hard to attribute.
Advertising works the other way: little shows this week, most arrives over
the following months. Three forces push managers short: abundant
short-term data, hard-to-measure long-term effects, and brand-manager
tenures shorter than the effects.

The vicious cycle: frequent discounts -> customers learn to wait and
stockpile -> baseline falls -> lift over baseline rises -> promotions look
even better -> more discounts -> premium erodes -> deeper discounts needed.

Published benchmarks (Lodish and Mela) are useful as stated assumptions,
never as facts about this brand: the long-run effect of a promotion is
about 80% of its short-term effect (a 20% penalty); the long-run effect of
advertising can be about 60% larger than its short-term effect; roughly
half of TV campaigns show no lift at all, so test.

<a id="method"></a>
## 2. Baseline and lift, step by step

Input: weekly units or revenue, a promo flag or discount amount.

1. Mark promo weeks. If no flag exists, treat weeks with discount_amount > 0
   (or average discount above a stated threshold) as promo weeks and say so.
2. Mark the 1 to 2 weeks after each promotion as "post-promo"; exclude them
   from the baseline and report them (pull-forward dip, see
   `evidence-check` §4).
3. For each quarter q:
   - `baseline_q = mean(sales in non-promo, non-post weeks of q)`
   - `lift_q = mean(sales in promo weeks of q) / baseline_q`
   - `promo_share_q = promo-week revenue / total revenue in q`
4. Trend: first quarter vs last quarter, and the slope of a simple
   regression of baseline on quarter index. Remove seasonality by comparing
   the same quarter year on year when there are 8+ quarters.
5. Total sales can be flat while baseline falls and promo share rises: the
   brand is replacing full-price demand with discounted demand.
6. Contribution check: compare full-price margin on baseline units with the
   margin left on promo units after discount; a rising promo share at a
   lower margin lowers profit even at flat revenue.

What to say: "promotions look more effective (lift 1.3x -> 1.9x) because
the base they are measured against fell 20%". The recommendation is fewer
and shallower promotions plus brand support, with a warning that the first
quarters may dip before the baseline recovers (the Clorox pattern:
revenue and profit dipped for two quarters after cutting discounts, then
baseline rose and lift fell).

<a id="sensitivity"></a>
## 3. Price and promotion sensitivity

- Estimate on quarterly aggregates. Weekly data overstate price
  sensitivity several-fold (about 7x in the source study) because they
  capture stockpiling and miss competitor reactions.
- Track the trend across years, not one estimate: rising sensitivity means
  the brand is losing differentiation.
- Also track response to regular price (willingness to pay full price),
  not only response to deals.

<a id="budget"></a>
## 4. Brand vs performance budget

- Short attribution windows count the last click; brand advertising mostly
  raises baseline, branded search and direct demand over months. A brand
  campaign judged on 7-day ROAS will always lose to search.
- Do not cut brand spend on short-window ROAS. Propose a test: hold out
  regions or a period, and read baseline sales, branded search share and
  new-customer volume over at least two quarters (incrementality method in
  `evidence-check` §4).
- Distribution and assortment also have long-term effects (Lacoste: cheap
  channels lifted sales short term and cost the brand its standing for
  years). Count them in the trade-off.
- Someone above the brand manager must own the long-term metrics; say who
  should review them.

<a id="triangle"></a>
## 5. The brand management triangle

| Objective | Raised by | Hurt by |
|---|---|---|
| Brand equity | higher price, advertising, selective distribution | discounting, cheap channels |
| Market share | lower price, quality, ad and promo spend | price rises, spend cuts |
| Short-term profit | price rises, cost and spend cuts | spend increases, discounts |

Every recommendation trades one of these. Name the one being traded.

<a id="patterns"></a>
## 6. Patterns and readings

| Pattern | Reading |
|---|---|
| Lift rising, baseline falling | trained deal-seekers; the promotion "improvement" is an artefact |
| Promo share above 40% and rising | brand depends on discounts; premium at risk |
| Baseline falling, competitors' too | category decline; check before blaming promotions |
| Brand ad cut, sales flat for a quarter | expected; effects lag; read baseline and branded search for 2+ quarters |
| Price premium stable, volume down | demand problem, not pricing power; look at funnel |
| Price sensitivity up year on year | differentiation eroding; check share of voice and associations |

---

## File: brand-health/references/per-customer-equity.md

# Measuring brand equity per customer

Contents: [Flaw of averages](#flaw) · [Method](#method) · [Three equities](#three) · [Customer equity](#ce) · [Attitude vs behaviour](#gap)

<a id="flaw"></a>
## 1. The flaw of averages

A brand-equity index averaged across all respondents ("our brand score is
7.1") describes nobody. A customer who rates awareness 9 and ethics 2 and
one who rates them 2 and 9 both average to 5.5, and any investment chosen
from 5.5 fits neither. The same flaw makes a stable average hide a falling
high-value segment when the respondent mix shifts.

Rule: compute per customer (or per segment), decide on that, and roll up
only at the end for portfolio reporting.

<a id="method"></a>
## 2. Method for a tracker or brand survey

1. Keep respondent-level rows: wave, segment, customer status, scores.
2. Per wave and segment: n, mean score, share of top scores.
3. Composition: compare each segment's share of respondents across waves.
   If the mix moved, recompute the total at a fixed mix (first wave's
   shares) so mix and score changes separate.
4. Value weighting: join segment CLV or revenue from the CRM; compute the
   value-weighted score change `sum(segment score change x segment share of
   CLV)`. This is the number for decisions.
5. Test each segment change for sampling error before calling it.
6. Verdict on the segment that carries the value, then the total.

Typical finding: the total is flat because a growing low-value segment
rates the brand higher while the core, high-CLV segment rates it lower.
That is a decline in the customers who pay for the brand.

<a id="three"></a>
## 3. The three equities

Brand choice is driven by three equities, measured per customer:

| Equity | What it is | Drivers |
|---|---|---|
| Value equity | objective judgement of what you get for what you pay | quality, price, convenience |
| Brand equity | subjective worth above objective value | awareness, attitude, brand ethics, corporate citizenship |
| Relationship equity | reluctance to switch | switching costs, loyalty programmes, community, personal relationships |

Their weights differ by category: low-involvement and luxury goods are
brand-led; airlines, rental cars and subscriptions are relationship-led;
B2B commodities and utilities are value-led. Step 1 is to establish which
leg drives choice here (key-driver analysis: regress choice or CLV on the
driver ratings per customer). Investing in the wrong leg (advertising in a
relationship-led business) wastes budget.

Brand-equity sub-drivers chosen for analysis must be tied to a spending
line, perceivable by customers, and ratable by them.

<a id="ce"></a>
## 4. Customer equity above brand equity

Customer equity = sum of CLV across all customers and all of the firm's
brands. Brand equity is one input into it. The two can diverge: brand
scores can rise while the customer base shrinks or shifts to lower value.
When they disagree, the customer number wins for decisions.

Consequences:
- A customer moving from one of our brands to another is not a loss.
- Judge retire, milk or extend decisions by the change in customer equity,
  not by the brand's own scores.
- Model a brand investment before spending: "raising perceived quality by
  X in segment Y lifts customer equity by Z; does Z exceed the cost?" and
  validate it afterwards.

<a id="gap"></a>
## 5. Attitude vs behaviour

Attitude models (multi-attribute scores, intention, social norms,
perceived control) explain why people feel as they do, but they predict
purchase poorly: habit, price, availability and competitors intervene.
Rules:
- Pair every attitude metric with a behavioural one for the same people or
  period (repeat rate, share of wallet, baseline sales).
- If they disagree, trust behaviour and report the attitude as unconfirmed.
- Use relative rankings, not absolute points; calibrate across people.
- High intention with low purchase can mean low perceived control (price,
  availability, effort): check the barriers before the message.

---

## File: brand-health/references/positioning-content.md

# Positioning and content checks

Contents: [Three questions](#three) · [POP and POD tests](#pod) · [3C requirements](#3c) · [Pitfalls](#pitfalls) · [Perceptual maps](#maps) · [Content audit](#content)

The `diagnose` skill's brand-diagnostic.md names positioning states (none,
not resonating, needs repositioning). This file is the checking method
behind those states.

<a id="three"></a>
## 1. Positioning is three questions, not one

1. **Is the frame established?** Does the target place the brand in the
   intended category or goal? Evidence: which queries bring people, which
   brands they compare us with, review-site categories. The frame can shift
   over the lifecycle; frame drift (new substitutes outside the category) is
   often the first sign a repositioning is coming.
2. **Are the points of parity met?** The must-haves of the frame. A brand
   missing a parity point is not considered, however strong its difference.
   An extension must prove the category's parity point (the deodorant stops
   odour) before its parent's difference matters.
3. **Is the point of difference compelling?** Within the frame, is there a
   reason to prefer us?

A strong difference without the frame and parity points is an incomplete
position.

<a id="pod"></a>
## 2. POP and POD tests

**Parity:** list the category must-haves; rate own performance on each 1 to
10 (survey, reviews, mystery shop). Any below 7 is a risk zone: fix it
before spending on the difference.

**Difference** passes only if all hold:

| Filter | Test | Fails when |
|---|---|---|
| Relevant | target customers rank it among purchase drivers | it is a feature nobody weighs (the "longer lasting" vs "faster relief" lesson) |
| Distinctive | no competitor can credibly claim it; "only", not "best" | it is a "best" claim on a shared attribute |
| Believable | one specific, verifiable reason to believe | the proof is vague ("customers love us") |
| Feasible | operations deliver it at every touchpoint | uncontrollable factors break it |
| Profitable | it can be sustained at the margin | it is costly to keep (free delivery that has to be withdrawn) |
| Defensible | hard to copy (patent, network, operations, authentic heritage) | cheapest, hippest, free delivery |

Types of difference: performance (checkable attributes), imagery (who uses
it and when), consumer insight (easiest to copy). Two benefits customers
see as opposites (cheap and best, healthy and tasty) need sequencing, an
outside credibility source, or a reframe that makes one support the other.

<a id="3c"></a>
## 3. The 3C requirements

| Side | Requirements | Check |
|---|---|---|
| Consumer (3 R's) | relevant, resonant, realistic | job-to-be-done match; claim level on the ladder (feature, benefit, value); proof present |
| Competitive (3 D's) | distinctive, defensible, durable | competitor claim map; barrier type; time horizon of the claim (feature claims last 1 to 3 years, core values 10+) |
| Company (3 F's) | feasible, favourable, faithful | can we deliver it, does it pay, is it true to our history and behaviour |

Laddering moves a claim from feature to benefit to value; value claims
resonate most and are hardest to copy, but must stay tied to a product
truth. New categories may need feature-level claims first.

<a id="pitfalls"></a>
## 4. The five positioning pitfalls

1. Building awareness before the position is clear.
2. Promoting attributes customers do not care about.
3. Investing heavily in differences that are easy to copy.
4. Walking away from a working position to chase a competitor.
5. Repeatedly trying to reposition when it is not possible.

<a id="maps"></a>
## 5. Perceptual maps

- Map customer perception, never the brand's intended position.
- Data: attribute ratings (PCA or factor analysis), pair similarity (MDS),
  or free associations (correspondence analysis). At least 100 to 200
  respondents from the target, better 300 to 500; check each brand has
  enough ratings.
- Choose attributes that drive choice and vary across brands.
- Close = substitutes; crowded clusters = price pressure; an empty space
  is an opportunity only if customers want it and it pays (it may be empty
  for a reason).
- Maps at several dates show drift; maps per segment show who sees you as
  intended.
- Maps do not show cause, profitability or feasibility.

**Centrality vs distinctiveness:** high centrality + high distinctiveness
(aspirational) supports premium and volume; high centrality + low
distinctiveness (mainstream) competes on price and availability; low
centrality + high distinctiveness (unconventional) is a loyal niche; low on
both (peripheral) is the vulnerable spot.

<a id="content"></a>
## 6. Content and campaign audit

1. Write the brand's position, its personality dimension and archetype in
   one line each before scoring content.
2. **Personality dimension (Aaker):** sincerity (honest, warm, unpretentious),
   excitement (daring, imaginative, up to date), competence (reliable,
   expert, evidence-backed), sophistication (refined, restrained, exclusive),
   ruggedness (tough, outdoorsy, direct). Score each piece for fit with the
   chosen one; flag pieces that express a different one.
3. **Archetype:** one of the twelve (innocent, explorer, sage, hero,
   outlaw, magician, regular person, lover, jester, caregiver, creator,
   ruler). Mixing archetypes across pieces confuses the meaning.
4. **Claims:** each claim needs its reason to believe; no superlatives
   without proof; no claims operations cannot deliver.
5. **Lifecycle fit:** awareness pieces give value without selling;
   consideration pieces answer evaluation criteria and objections; decision
   pieces reduce risk; retention and advocacy pieces reward and enable
   sharing.
6. **Search fit:** keywords that bring traffic but not the brand's audience
   dilute meaning; prefer terms that match the desired associations.
7. **Consistency over the calendar:** judge the month's content together
   for cumulative impact, not piece by piece. Same core, adapted execution
   per channel.
8. **Endorsers and partners:** a liked endorser who becomes disliked
   unbalances the relationship (multiply the three signs: customer-endorser,
   endorser-brand, customer-brand; a negative product means pressure to
   change); monitor and be ready to distance the brand.
9. **Activism and bold messages:** messages far from the audience's current
   view are rejected and can backfire; the more the topic touches identity,
   the narrower the acceptable range. Move in steps.
