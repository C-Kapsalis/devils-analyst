# EVALS: pricing-promotions

Five case designs in the style of `benchmarks/cases/*/` (prompt.md,
scaffold.sh writing `resources/`, LLM graders on `report.md`, plus a
`skill-fired` tool_used grader matching `pricing-promotions|evidence-check`).
Every number below was produced by the prototype generator
`_work/sim.py` (fixed seeds); port each function into
`benchmarks/builder/cases/<name>.py` with asserts on the gap between naive and
correct answers, as `promo-pull-forward.py` does. The existing
`promo-pull-forward` case already covers the post-promo dip; these cases
cover the other traps.

---

## 1. elasticity-promo-confound

**Prompt.** "resources/ has two years of weekly sales for our best-seller,
the Ridge daypack (weekly_sales.csv: week_start, units, avg_selling_price)
and our marketing calendar (campaign_calendar.csv: week_start, campaign,
type). Unit cost landed in our warehouse plus fulfilment is $22. What is the
price elasticity, and should we change the regular price (now $40)? Write
report.md."

**Data.** 104 weeks. Regular price moves between $38 and $42 in 13-week
blocks. 25 promo weeks (about 22%) at 20 or 25% off; each promo week has a
row in campaign_calendar.csv ("Ridge sale email + homepage banner",
type=promo). True model: `ln units = ln 900000 - 2.0 ln price + 0.60 promo +
N(0, 0.06)`. The promo flag is only in the calendar file, not the sales file.

**Ground truth.** Log-log with a promo dummy: E = 1.88 (non-promo weeks
only: 1.87). `1/PV` at $40 = 40/18 = 2.22 > 1.88: underpriced. Constant
elasticity `P*` = 22 x 1.88 / 0.88 = $47.1, outside the observed $38-42
regular range, so the right action is a test step up (about $42-44); a move
to $42 changes contribution by about +1.4% under the controlled E.

**Naive answer.** Regress ln units on ln price only: E = 4.20 ("highly
elastic"), `1/PV` 2.22 < 4.2, "overpriced, cut to $28.87"; at E = 4.2 a move
to $42 would look like -9.5% contribution.

**Graders.**
- elasticity (w3): PASS if the report estimates E with promo weeks
  controlled (dummy, excluded, or joined from the calendar) and reports a
  value between 1.6 and 2.3. FAIL if it reports E above 3 as the regular
  price elasticity, or does not use the campaign calendar at all.
- decision (w3): PASS if it recommends holding or raising the regular price
  (ideally a tested step of 5-10%, noting `P*` is outside observed prices).
  FAIL if it recommends cutting the regular price.
- method (w1): PASS if it explains that promo weeks combine lower price with
  email/banner attention, which inflates the price-only estimate.

---

## 2. discount-subsidy-break-even

**Prompt.** "resources/daily_sales.csv is our Shopify export (date,
new_customer_orders, returning_customer_orders, gross_revenue,
discount_amount; gross revenue is before discounts). From 14 to 20 September
we ran 20% off everything for our email subscribers (code VIP20). Product
cost is 52% of full price and pick, pack and ship is $7 per order. Was it
worth it, and what discount should we use for the next one? Write report.md."

**Data.** 70 days (3 Aug - 11 Oct 2026). Normal days about 120 new and 180
returning orders, AOV about $64. Promo week: new x1.30, returning x1.38; 93%
of promo-week revenue carries the code discount. No post-promo dip (so the
trap is not pull-forward).

**Ground truth.** Orders +34%, net revenue +9.8%, but contribution per day
falls from $7,095 to $4,787: -$16,153 for the week. $33,622 of discounts
given; only about 713 of 2,805 promo-week orders were incremental, and 61% of
promo orders came from returning customers. Contribution margin at full
price is about 37%; break-even lift at 20% off = 0.37/0.17 = 117%; at 15%:
68%; at 10%: 37%. Recommendation: not 20% to everyone; a 10% offer or one
gated to new or lapsed customers, tested against a holdout.

**Naive answer.** "Orders +34%, revenue +10%, 2,600+ code redemptions: a
success, repeat at 20%" (revenue-based, or judges incremental orders without
the discount on would-buy-anyway orders).

**Graders.**
- contribution (w3): PASS if the report concludes the promo reduced
  contribution/profit, with a weekly loss roughly between -$24k and -$9k, or a
  clearly reasoned negative figure that counts the discount on baseline
  orders. FAIL if it calls it profitable or judges on revenue/orders.
- break-even (w2): PASS if it states the lift needed to break even at 20%
  (about 100-130%) or gives a break-even table by depth. FAIL if absent.
- subsidy and recommendation (w2): PASS if it notes most code users would
  have bought anyway (returning share or baseline netting) AND recommends a
  shallower or targeted offer and/or a holdout. FAIL if it recommends
  repeating 20% sitewide.

---

## 3. promo-baseline-erosion

**Prompt.** "resources/weekly_sales.csv (week_start, units, revenue) and
promo_weeks.csv cover our last three fiscal years. Our last sale had the
biggest lift we've ever had. The team wants to go from 12 sales a year to 16
next year. Does the data support that? Product price $50, sales are 25% off,
unit cost $25. Write report.md."

**Data.** 156 weeks, FY24-FY26. Promo weeks: 5, 9, 12 per year. Promo weeks
sell about 1,720 units regardless. Baseline weekly units erode 1.5% per
cumulative promo (1,000 -> about 740).

**Ground truth.**

| FY | Promos | Baseline units/wk | Lift over baseline | Promo share of revenue | Contribution |
|---|---|---|---|---|---|
| FY24 | 5 | 964 | +78% | 12% | $1,240,362 |
| FY25 | 9 | 863 | +98% | 24% | $1,119,600 |
| FY26 | 12 | 743 | +131% | 34% | $1,000,250 |

Lift rises only because baseline falls; total units and contribution fall
each year (-19% contribution over two years). More promos would continue the
erosion. Recommendation: fewer, targeted promos with a holdout, track
baseline; expect short-term revenue dip before recovery.

**Naive answer.** "Lift grew from 78% to 131%, promos are working better
every year: go to 16."

**Graders.**
- erosion (w3): PASS if the report shows the baseline (non-promo) weekly
  units falling (about -20% to -25% FY24 to FY26) and attributes the rising
  lift to that. FAIL if it presents rising lift as improving promo
  performance.
- total contribution (w2): PASS if it shows total contribution (or
  contribution per week) falling as promo count rose. FAIL if it judges on
  promo-week metrics only.
- recommendation (w2): PASS if it recommends against going to 16 (or only
  as a controlled test) and proposes fewer/targeted promos or a holdout.
  FAIL if it endorses 16.

---

## 4. price-increase-forward-buying

**Prompt.** "We sell coffee capsules. We emailed customers on 19 February
that prices go up 10% on 1 March ($24 to $26.40 per box). resources/
daily_units.csv (date, units, revenue) runs to 26 April. Unit cost is $12.
Units after the increase look terrible. Should we roll the price back? Write
report.md."

**Data.** Baseline about 400/day to 18 Feb; 19-28 Feb stock-up at x1.55; 1-21
March dip starting at about 60% of the settled level and recovering
linearly; from 22 March settled at 0.96 x baseline.

**Ground truth.** Baseline 397/day; settled level (from 29 March) 382/day:
-3.9% units for +10% price, E about 0.39. Break-even volume loss for +10% at
PV 50% is 16.7%. Contribution per day rose from $4,769 to $5,500 (+15.3%).
Keep the price; `E` < 1 even suggests further room, to be tested.

**Naive answer.** 14 days before (554/day, inflated by stock-up) vs 14 days
after (285/day): -48.6%, "E about 4.9, demand is very elastic, roll back."

**Graders.**
- stock-up (w3): PASS if the report identifies the pre-increase spike as
  stock-up/forward buying and the early-March dip as its after-effect, and
  measures against a baseline before 19 Feb and a settled post period. FAIL
  if it compares the weeks either side of 1 March.
- verdict (w3): PASS if it recommends keeping the increase with a settled
  unit change between about -8% and 0% and contribution up. FAIL if it
  recommends rolling back.
- elasticity (w1): PASS if it reports E below 1 (or a small volume loss
  below the 16.7% break-even).

---

## 5. channel-contribution

**Prompt.** "We sell a $34 water bottle in three channels: our Shopify store,
Amazon FBA and wholesale to outdoor retailers. resources/ has
channel_sales_sept.csv (channel, units, revenue, returns, ad_spend),
amazon_settlement_sept.csv and shopify_payouts_sept.csv (fees). Wholesale
price is $17, retailers get 4% co-op allowance, freight $0.80 per unit.
Landed cost is $9. Amazon is now our biggest channel. Where should we put
2027 growth money? Write report.md."

**Data (monthly).** Shopify: 5,200 units at $34, 5% returns, payment 2.9% +
$0.30/order (1.4 units/order), shipping $6.50/order, ads $31,000. Amazon:
9,800 units at $29.99 (below our own $34 and the retailers' shelf price), 9%
returns, referral 15%, FBA $5.60/unit, $0.45/unit other fees, ads $26,000.
Wholesale: 6,100 units at $17, 1% returns.

**Ground truth.**

| Channel | Revenue | Contribution/unit before ads | After ads | Monthly contribution |
|---|---|---|---|---|
| Shopify | $176,800 | $17.68 | $11.72 | $60,946 |
| Amazon | $293,902 | $8.15 | $5.49 | $53,845 |
| Wholesale | $103,700 | $6.39 | $6.39 | $39,009 |

Amazon leads on revenue but keeps the least per unit; Shopify keeps about 2x
per unit. Amazon's $29.99 undercuts both the own store and wholesale
partners (conflict risk). Growth money: own store first (with a marginal
test), fix Amazon price parity; do not prioritise Amazon on revenue.

**Naive answer.** "Amazon is 51% of revenue and growing: put growth into
Amazon ads and inventory" (revenue or platform ROAS ranking).

**Graders.**
- contribution ranking (w3): PASS if the report ranks channels on
  contribution after fees, returns and ads, showing Amazon lowest or near
  lowest per unit and Shopify highest. FAIL if it ranks by revenue or ROAS.
- conflict (w1): PASS if it flags that Amazon's price undercuts own store
  and/or retailers.
- recommendation (w2): PASS if growth is directed to the own store (or made
  conditional on contribution per extra unit / a test), not Amazon by
  revenue. FAIL if it recommends prioritising Amazon because it is biggest.

---

## Why these traps

| Case | What a strong model does unprompted | Why it is wrong |
|---|---|---|
| 1 | log-log on price alone, reads E=4.2, cuts price | promo attention moves with price; decision flips |
| 2 | counts redemptions and revenue lift | discount on would-buy-anyway orders exceeds the margin on extra orders |
| 3 | praises rising lift | lift rises because the baseline is eroding |
| 4 | compares two weeks either side of the change | stock-up and drought, not price response |
| 5 | ranks channels by revenue or ROAS | fees, returns and lower price leave Amazon the least per unit |
