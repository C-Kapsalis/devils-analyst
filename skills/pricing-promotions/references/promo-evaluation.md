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
