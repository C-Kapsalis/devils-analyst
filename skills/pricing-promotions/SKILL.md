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
| "Is our price right / should we raise it / what's our elasticity" | Price level | 3A | [elasticity-and-optimal-price](references/elasticity-and-optimal-price.md) |
| "We changed the price, did it work / roll back?" | Price change read-out | 3B | same |
| "How deep should the discount be / will X% off pay?" | Discount design | 3C | [promo-evaluation](references/promo-evaluation.md) |
| "How did the sale / code / promo do, run it again?" | Promo read-out | 3D | same |
| "We run lots of sales / lift keeps growing / more promos next year?" | Promo frequency | 3E | same |
| "Bundle, tiers, free-shipping threshold, fees, how to show the price" | Price structure | 3F | [price-structure-and-psychology](references/price-structure-and-psychology.md) |
| "Which channel makes money / Amazon vs store vs wholesale / retailer margin" | Channel economics | 3G | [channel-margins](references/channel-margins.md) |

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
