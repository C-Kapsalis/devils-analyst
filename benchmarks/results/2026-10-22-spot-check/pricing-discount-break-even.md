# pricing-discount-break-even

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/pricing-promotions/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/pricing-discount-break-even/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> resources/daily_sales.csv is the Shopify export for Northwind Coffee's online store (date, new_customer_orders, returning_customer_orders, gross_revenue, discount_amount; gross revenue is before discounts). From 14 to 20 September we ran 20% off everything for our email subscribers (code VIP20). Product cost is 52% of full price and pick, pack and ship is $7 per order.
> 
> Was it worth it, and what discount should we use for the next one? Write report.md with the numbers and your recommendation.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `break-even` | PASS | PASS | both +117% at 20% vs +33.5% actual |
| `contribution` | PASS | PASS | A -16,319 for the week; B -16,336 |
| `subsidy-recommendation` | PASS | PASS | A: 75% of discount on baseline orders, targeted offer + holdout; B: returning-customer share, 10% or less + holdout |

## Arm A answer (with skill)

````markdown
# VIP20 promotion read-out: Northwind Coffee online store

Scope: daily Shopify export, 3 Aug to 11 Oct 2026 (resources/daily_sales.csv). Promo: 20% off for email subscribers, code VIP20, 14 to 20 Sep 2026 (7 days). Baseline: 17 Aug to 13 Sep (4 weeks). Post-period: 21 Sep to 11 Oct (21 days; data ends before a full 4-week post-window). No house-rules folder was checked (no directory listing tool in this session).

## Verdict
**The promotion did not pay.** Net incremental contribution is **-$19.1k** over 28 days (promo days plus post-period) against the pre-period baseline. Revenue rose; contribution fell.
- Deciding number: net incremental contribution -$19.1k over 28 days; promo days alone -$16.3k.
- Naive read: "orders +33.5% and net revenue +9.4%, so it worked." Each extra order carried an $11.99 average discount; contribution per order fell from $23.72 to $11.95.

## Assumptions
- Gross revenue is full price; net = gross - discount_amount.
- Product cost = 52% of gross; pick/pack/ship = $7 per order. Contribution = 0.48 x gross - $7 x orders - discount.
- No program costs given (email, agency, payment fees, returns): set to $0. Any cost makes the result worse.
- Subscribers-only offer, store-wide export, no control group: the lift is a before/after comparison, cause unproven. The verdict holds even if the whole lift were caused by something else, since promo days already lost money against baseline.

## Numbers
| Period | Days | Orders | Orders/day | Gross | Discount | Contribution | Contribution/day |
|---|---|---|---|---|---|---|---|
| Baseline 17 Aug-13 Sep | 28 | 8,405 | 300.2 | $537,807 | n/a | $199,312 | $7,118 |
| Promo 14-20 Sep | 7 | 2,805 | 400.7 | $180,762 | $33,622 | $33,509 | $4,787 |
| Post 21 Sep-11 Oct | 21 | 6,177 | 294.1 | $395,730 | $0 | $146,711 | $6,986 |

Promo days vs baseline x 7:
- Baseline orders 2,101; promo 2,805; incremental +704 (+33.5%).
- Baseline gross $134,452; promo gross $180,762 (+34.4%).
- Promo net revenue $147,140 (+$12,688, +9.4% vs baseline net).
- Discount $33,622; program costs $0; promo contribution $33,509; baseline contribution for 7 days $49,828.
- Promo-days incremental contribution: **-$16,319**.

Full 28-day window (pre-period baseline):
- Contribution promo + post = $180,220; baseline 28 days = $199,312.
- Net incremental contribution: **-$19,092**.
- Incremental orders: 8,982 - 8,405 = +577 (+6.9%).
- Post-period dip: -127 orders; -$2,773 contribution.
- Second baseline (pre + recovered post, 49 days, $7,062/day): net **-$17.5k**. Same sign, so the verdict does not depend on baseline choice.

Segments (promo days):
- New: baseline 849, promo 1,097, incremental +248 (+29%), 35% of incremental.
- Returning: baseline 1,252, promo 1,708, incremental +456 (+36%), 65% of incremental.
- Returning share of promo orders 61% vs 60% of baseline: the code did not skew to returning customers.

## Subsidy
Subsidy = baseline orders in promo days x average discount = 2,101 x $11.99 = **$25.2k**, about 75% of the $33.6k discount (new ~$10.2k, returning ~$15.0k; assumes equal discount per order).

## Discount depth break-even
Full-price basket: $63.99 gross per order; product cost $33.27; pick/pack/ship $7.00; contribution $23.72 per order (PV 37.1%).

| Discount | Contribution per order | Lift needed to break even |
|---|---|---|
| 10% | $17.32 | +37% |
| 15% | $14.12 | +68% |
| 20% | $10.92 | +117% |
| 25% | $7.72 | +207% |
| 30% | $4.52 | +425% |

The code gave an effective 18.6% off, not 20% (discount = 18.6% of gross on every promo day). Break-even at 18.6% needs +98% orders; observed +33.5%.

## Recommendation
1. Do not run VIP20 at 20% to the whole subscriber list again. At every depth in the table, a sitewide-to-subscribers code needs lift this promo did not approach, and 75% of the discount went to orders that were coming anyway.
2. Target the offer. Lapsed subscribers (e.g. 90+ days since last order) or first-order buyers are the most likely to be incremental. For orders that would not otherwise happen, any depth under about 37% still earns positive contribution per order (at 20%, $10.92 each), and the subsidy disappears.
3. If you run it again, test first: 10-15% for lapsed subscribers only, with a randomised holdout of similar size; judge on net incremental contribution against the holdout, not on lift. Check break-even and power with the evidence-check skill before launch.
4. Confirm why the code gave 18.6% and not 20% (excluded products, a different discount base, or a setting). Hypothesis to check, not a finding.
5. Watch the baseline. Post-period ran about 2% below the pre-period average, inside normal weekly swing (pre weeks 294-306 orders/day). Track four weeks after the next promo; a lasting drop would mean buyers are learning to wait.

## Caveats
- Post-period is 21 of 28 days; a full four weeks needs data through 18 Oct.
- No control group or prior-year data: lift not proven caused by the code.
- Program costs, payment fees and returns are absent; all would lower the result.
- Post-period dip is at most 127 orders (about 18% of the promo lift) and within noise: no large pull-forward is visible.
- Future value of promo-acquired customers not measured; treated as unproven and excluded.

## Scores (before handover)
Clarity 88, relevance 92, depth 85, insightfulness 85.

To confirm with the user: the objective (this assumes maximising contribution; if the aim was trial of new customers, the +248 new-customer orders are the part to examine) and the decision on the next promotion.
````

## Arm B answer (without skill)

````markdown
# VIP20 promotion, 14 to 20 September 2026: was it worth it?

**Short answer: no.** The 20% offer added orders and net revenue, but it lost about $16.3k of contribution in the week. Do not repeat it at this depth. If you test again, use 10% or less against a holdout, and only keep it if orders rise by at least the break-even lift given below.

All figures were computed by hand from `resources/daily_sales.csv`. Currency is treated as dollars, as the brief says.

## Method

- **Promo week:** 14 to 20 September (7 days).
- **Baseline:** 31 August to 13 September (14 days, no discount in any row). I checked a second baseline, 21 September to 4 October (14 days, post-promo), and the conclusion does not change.
- **Revenue:** `gross_revenue` is before discounts, so net revenue = gross − discount.
- **Cost of goods:** 52% of full-price (gross) value, so it is the same whether or not a discount was applied.
- **Fulfilment:** $7 per order (orders = new + returning customer orders).
- **Contribution** = gross − discount − 52% of gross − $7 × orders.

## Results

| Measure | Baseline (7-day equivalent) | Promo week (actual) | Change |
|---|---|---|---|
| Orders | 2,101.5 | 2,805 | +703.5 (+33.5%) |
| New-customer orders | 854 | 1,097 | +243 (+28.5%) |
| Returning-customer orders | 1,247.5 | 1,708 | +460.5 (+36.9%) |
| Gross revenue | 134,489.43 | 180,761.62 | +46,272.19 |
| Discount given | 0 | 33,621.67 | −33,621.67 |
| Net revenue | 134,489.43 | 147,139.95 | +12,650.52 |
| Cost of goods (52% of gross) | 69,934.50 | 93,996.04 | +24,061.54 |
| Shipping and pick-pack ($7 per order) | 14,710.50 | 19,635.00 | +4,924.50 |
| **Contribution** | **49,844.43** | **33,508.91** | **−16,335.52** |

- Average gross per order is essentially unchanged: about $64.00 in the baseline and $64.44 in the promo week. The discount did not lift basket size.
- The discount was 18.6% of gross (33,621.67 / 180,761.62), not 20%. Either some items or orders were excluded, or the export nets something. Check this with Shopify before the next test.
- Every promo day (387 to 412 orders) was above every baseline day (279 to 327 orders), so the lift is well outside normal daily variation.
- Against the post-promo baseline (about 293.5 orders and $18,814 gross per day), the contribution loss is about $15.3k. The result holds with either baseline.

## Where the extra orders came from

Two-thirds of the incremental orders (460.5 of 703.5) came from returning customers, who grew faster (+36.9%) than new customers (+28.5%). That suggests many of the discounted orders were existing buyers who would have ordered anyway, so the discount subsidised them. The export has no subscriber flag, so this cannot be confirmed. Post-promo returning orders were about 1% below the pre-promo level (176.6 against 178.2 per day), so there is no clear pull-forward dip.

## Break-even: what lift would the next discount need?

Break-even order lift = baseline contribution per order ÷ contribution per order at the new discount. Baseline gross per order is $64.00 and baseline contribution per order is $23.72. Lift is measured against the current 2,101.5 orders per week.

| Discount on gross | Contribution per order | Break-even order lift |
|---|---|---|
| 5% | $20.52 | +16% |
| 10% | $17.32 | +37% |
| 15% | $14.12 | +68% |
| 18.6% (this promo) | $11.82 | +101% |
| 20% | $10.92 | +117% |

The promo produced +33.5%, well below the +101% it needed at its own depth.

## Recommendation

1. **Do not run VIP20 again at 20%.** It lost money even though it lifted volume by a third.
2. **If you test again, use 10% or less.** At 10%, the same +33.5% lift would still leave the week about $1.3k short of baseline, so you need roughly +37% orders to break even. At 5%, you need about +16%.
3. **Run it against a holdout**, for example half the subscriber list or a control week, so you can measure the true lift and separate new customers from existing ones. Decide before the test starts: keep the offer only if orders rise by at least the break-even lift for that depth.
4. **Consider offers that do not discount every order**, such as a minimum-spend threshold, which may lift basket size. The data here cannot test this, because basket size did not change in this promo.
5. **Confirm the real discount rate** (18.6% effective against a 20% offer) and whether the offer excluded any products.

## Limits

- One promotion at one depth. The lift at 5% or 10% is unknown and must be tested; the table above is the threshold, not a forecast.
- No subscriber flag, so existing-customer subsidy is inferred from the new/returning split only.
- Excludes payment fees, returns, email costs and any staff time. Each would make the promo look worse, not better.
- Assumes the 52% cost and $7 fulfilment cost hold at lower price points, and that the baseline week would have stayed flat.
````
