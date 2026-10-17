"""Kestrel Nutrition (supplements, Shopify): last year's Black Friday / Cyber Monday
read-out, asked while planning this year's.

Planted subtle problems (6):
 P1 "60% margin" in the brief is a markup: cogs / gross_sales = 62.5%, so gross margin is
    37.5%; contribution after fulfilment and fees is ~25% of net sales, so 30% off loses money per order.
 P2 Pre-promo lull: the 17 Nov early-access email announced the sale; orders fell ~22% for
    the 10 days before it, so the week before is a depressed baseline.
 P3 Post-promo dip: replenishable product, orders ran ~25% below baseline for ~3 weeks (P2+P3 flip the verdict).
 P4 Returns: refunds on promo-day orders are ~15% of net sales vs ~6% normally.
 P5 Subsidy: ~70% of promo orders came from returning customers (their normal cycle).
 P6 Promo-acquired new customers repeat far less (90-day repeat 7% vs 19%), so the deck's
    "new customers will pay it back" is unproven.
Decoys (2): gross (pre-discount) order value is higher on promo days (basket building, real);
Thanksgiving Day (27 Nov) is the lowest order day of the period (US holiday).
Decision: do not repeat 25% sitewide (and not deeper): it lost contribution. Naive: repeat/deepen.
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-commerce-bfcm-repeat"
rng = random.Random(90517)

START, END = dt.date(2025, 10, 13), dt.date(2025, 12, 28)
ANNOUNCE = dt.date(2025, 11, 17)
THANKS = dt.date(2025, 11, 27)
P0, P1 = dt.date(2025, 11, 28), dt.date(2025, 12, 1)
DIP_END = dt.date(2025, 12, 21)
DEPTH = 0.25
COGS_RATIO = 0.625          # of full-price merchandise value (markup 60% on cost)
FULFIL, PAY, LABEL = 6.50, 0.029, 5.0
AD_SPEND = 18000.0
WDAY = [1.05, 1.03, 1.00, 0.99, 0.96, 0.95, 1.02]
PROMO_LVL = {P0: 3.1, P0 + dt.timedelta(1): 2.2, P0 + dt.timedelta(2): 1.9, P1: 2.8}

rows = []
d = START
while d <= END:
    lvl = 1.0
    promo = P0 <= d <= P1
    if ANNOUNCE <= d < P0:
        lvl = 0.78
    if d == THANKS:
        lvl = 0.78 * 0.62
    if promo:
        lvl = PROMO_LVL[d]
    if P1 < d <= DIP_END:
        k = (d - P1).days
        lvl = 0.66 + 0.34 * min(1.0, k / 20)
    orders = int(round(375 * WDAY[d.weekday()] * lvl * rng.gauss(1, 0.03)))
    ret_share = 0.70 if promo else 0.64
    returning = int(round(orders * rng.gauss(ret_share, 0.01)))
    new = orders - returning
    gpo = rng.gauss(88.0 if promo else 72.0, 1.2)
    gross = round(orders * gpo, 2)
    disc = round(gross * DEPTH * rng.uniform(0.965, 0.975), 2) if promo else round(gross * rng.uniform(0.010, 0.016), 2)
    net = round(gross - disc, 2)
    rr = rng.gauss(0.15, 0.006) if promo else rng.gauss(0.06, 0.004)
    refunds = round(net * rr, 2)
    returned_orders = int(round(orders * rr))
    cogs = round(gross * COGS_RATIO, 2)
    sessions = int(round(orders / (rng.gauss(0.041, 0.001) if promo else rng.gauss(0.026, 0.0008))))
    rows.append(dict(date=d, sessions=sessions, orders=orders, new=new, returning=returning, gross=gross,
                     disc=disc, net=net, refunds=refunds, ret_orders=returned_orders, cogs=cogs, promo=promo))
    d += dt.timedelta(1)

by = {r["date"]: r for r in rows}


def contrib(r):
    rshare = r["refunds"] / r["net"]
    return (r["net"] - r["refunds"] - r["cogs"] * (1 - rshare) - FULFIL * r["orders"]
            - PAY * r["net"] - LABEL * r["ret_orders"])


def rng_days(a, b):
    return [by[a + dt.timedelta(i)] for i in range((b - a).days + 1)]


base = rng_days(START, ANNOUNCE - dt.timedelta(1))          # 35 days, 13 Oct - 16 Nov
window = rng_days(ANNOUNCE, DIP_END)                         # 35 days, 17 Nov - 21 Dec
promo = rng_days(P0, P1)
lull = rng_days(ANNOUNCE, P0 - dt.timedelta(1))
post = rng_days(P1 + dt.timedelta(1), DIP_END)
assert len(base) == 35 and len(window) == 35

base_c = sum(contrib(r) for r in base) / len(base)
base_o = sum(r["orders"] for r in base) / len(base)
win_c = sum(contrib(r) for r in window)
net_incr = win_c - base_c * len(window) - AD_SPEND
promo_c_day = sum(contrib(r) for r in promo) / 4
incr_orders = sum(r["orders"] for r in window) - base_o * len(window)
promo_orders = sum(r["orders"] for r in promo)
promo_incr_orders = promo_orders - base_o * 4
lull_drop = 1 - (sum(r["orders"] for r in lull) / len(lull)) / base_o
post_first14 = rng_days(P1 + dt.timedelta(1), P1 + dt.timedelta(14))
post_drop = 1 - (sum(r["orders"] for r in post_first14) / 14) / base_o
post_lost = base_o * len(post) - sum(r["orders"] for r in post)

gross_all = sum(r["gross"] for r in rows)
cogs_ratio = sum(r["cogs"] for r in rows) / gross_all
margin_true = 1 - cogs_ratio
pv_order = sum(contrib(r) for r in base) / sum(r["net"] for r in base)  # contribution / net sales, normal days
ret_promo = sum(r["refunds"] for r in promo) / sum(r["net"] for r in promo)
ret_base = sum(r["refunds"] for r in base) / sum(r["net"] for r in base)
returning_share = sum(r["returning"] for r in promo) / promo_orders
subsidy = base_o * 4 * (sum(r["disc"] for r in promo) / promo_orders)
promo_new = sum(r["new"] for r in promo)
promo_disc = sum(r["disc"] for r in promo)
be_lift_true = DEPTH / (pv_order - DEPTH) if pv_order > DEPTH else float("inf")
be_lift_naive = DEPTH / (0.60 - DEPTH)

# naive: promo 4 days vs the week before, net sales x 60%
lull_week = rng_days(P0 - dt.timedelta(7), P0 - dt.timedelta(1))
lull_net_day = sum(r["net"] for r in lull_week) / 7
promo_net = sum(r["net"] for r in promo)
naive_lift_pct = (promo_net / 4) / lull_net_day - 1
naive_profit = (promo_net - lull_net_day * 4) * 0.60 - AD_SPEND
# also: correct window but 60% margin (cogs = 40% of gross)


def contrib_naive_margin(r):
    return r["net"] - r["refunds"] - 0.40 * r["gross"] - FULFIL * r["orders"] - PAY * r["net"]


net_incr_60 = (sum(contrib_naive_margin(r) for r in window)
               - sum(contrib_naive_margin(r) for r in base) / 35 * 35 - AD_SPEND)

# cohorts
cohorts = [
    ["2025-09 (no promo)", "first order 1-30 Sep 2025", 2310, 0.121, 0.192, 0.268, 71.4],
    ["2025-10 (no promo)", "first order 1-31 Oct 2025", 2385, 0.118, 0.187, 0.262, 70.9],
    ["2025-11 BFCM", "first order 28 Nov - 1 Dec 2025 (25% off)", promo_new, 0.041, 0.071, 0.108, 64.2],
    ["2025-12 (excl. BFCM)", "first order 2-31 Dec 2025", 1760, 0.109, 0.176, 0.249, 69.8],
]
bf_rep90, norm_rep90 = 0.071, (0.192 + 0.187) / 2

# ---------- asserts ----------
assert abs(cogs_ratio - 0.625) < 0.002
assert net_incr < -40000, net_incr
assert naive_profit > 60000, naive_profit
assert net_incr_60 < 0  # loses under either margin once the window is right
assert 0.18 < lull_drop < 0.26 and 0.18 < post_drop < 0.32
assert ret_promo > 2 * ret_base
assert returning_share > 0.66
assert promo_c_day < 0.25 * base_c
assert pv_order < 0.30
gross_aov_base = sum(r["gross"] for r in base) / sum(r["orders"] for r in base)
gross_aov_promo = sum(r["gross"] for r in promo) / promo_orders
net_aov_promo = promo_net / promo_orders
assert gross_aov_promo > gross_aov_base > net_aov_promo
assert min(rows, key=lambda r: r["orders"])["date"] == THANKS

usd = lambda x: ("-" if x < 0 else "") + f"${abs(x):,.0f}"
pc = lambda x, k=1: f"{100 * x:.{k}f}%"

shop = to_csv(
    ["date", "sessions", "orders", "new_customer_orders", "returning_customer_orders", "gross_sales", "discounts",
     "net_sales", "returns", "returned_orders", "cost_of_goods_sold"],
    [[r["date"].isoformat(), r["sessions"], r["orders"], r["new"], r["returning"], r["gross"], r["disc"], r["net"],
      r["refunds"], r["ret_orders"], r["cogs"]] for r in rows])

cal = to_csv(["date_start", "date_end", "activity", "details"], [
    ["2025-10-20", "2025-10-20", "email", "Newsletter: autumn routine guide (no offer)"],
    ["2025-11-03", "2025-11-03", "email", "Newsletter: product education (no offer)"],
    ["2025-11-17", "2025-11-17", "email + site banner", "Early access list: 'Black Friday 25% off everything starts Fri 28 Nov'"],
    ["2025-11-24", "2025-11-24", "email", "Reminder: 25% off starts Friday"],
    ["2025-11-28", "2025-12-01", "promotion", "BFCM: 25% off sitewide, automatic at checkout, excludes gift cards"],
    ["2025-11-28", "2025-12-01", "paid social", f"Incremental BFCM prospecting budget {usd(AD_SPEND)} (on top of always-on)"],
    ["2025-12-08", "2025-12-08", "email", "Newsletter: winter immunity (no offer)"],
])

coh = to_csv(["cohort", "definition", "new_customers", "repeat_rate_30d", "repeat_rate_90d", "repeat_rate_180d",
              "first_order_net_value"], cohorts)

deck = f"""# BFCM 2025 recap (shared in #growth, 3 Dec 2025)

- Net sales over the four days: **{usd(promo_net)}**, up **{pc(naive_lift_pct, 0)}** on the week before.
- {promo_orders:,} orders, {promo_new:,} new customers acquired.
- Conversion rate 4.1% vs 2.6% normal. Average gross basket {usd(gross_aov_promo)} vs {usd(gross_aov_base)}.
- At our 60% margin that is roughly {usd(naive_profit)} profit after the extra {usd(AD_SPEND)} of paid social.
- New customers will pay back many times over: our customers are worth ~$210 each over their lifetime.
- Proposal for 2026: same mechanics, 30% off, start the early-access emails two weeks out.
"""

files = {
    "resources/shopify_daily_sales_2025q4.csv": shop,
    "resources/marketing_calendar_2025q4.csv": cal,
    "resources/new_customer_cohorts_2025.csv": coh,
    "resources/bfcm_2025_recap.md": deck,
}

prompt = """
We're planning Black Friday for Kestrel Nutrition (we sell supplements through our Shopify store). Last year we ran 25% off everything from Friday 28 Nov to Cyber Monday. resources/ has the daily Shopify export for Q4 2025, the marketing calendar, new-customer cohort numbers, and the recap the team shared in December (bfcm_2025_recap.md). Our products have a 60% margin; pick, pack and shipping costs us about $6.50 an order and card fees are 2.9%.

How did last year's Black Friday do, and what should we do this year: same again, go deeper as the team proposes, or something else? Put the answer in report.md with the numbers behind it.
"""

recall = f"""
The data contains 6 planted problems. Answer key (all numbers computed from the files):

1. Margin vs markup. The brief says "60% margin", but cost_of_goods_sold / gross_sales = {pc(cogs_ratio)} in the Shopify export, so gross margin is {pc(margin_true)} (60% is the markup on cost). After fulfilment and card fees, contribution is about {pc(pv_order, 0)} of net sales on a normal day, and the break-even lift for 25% off is {"impossible" if be_lift_true == float("inf") else pc(be_lift_true, 0)} instead of {pc(be_lift_naive, 0)}. Found if the report says the 60% is not the real margin (cites the COGS ratio, a margin of 35-40%, or the markup conversion).
2. Depressed baseline before the sale. The 17 Nov early-access email announced the sale; orders from 17 to 27 Nov ran about {pc(lull_drop, 0)} below the 13 Oct - 16 Nov level, so comparing with "the week before" overstates the lift. Found if the report says the week before was depressed by the announcement (people waiting) and uses an earlier baseline.
3. Post-promo dip. Orders in the 14 days after Cyber Monday ran about {pc(post_drop, 0)} below the pre-announcement baseline (about {post_lost:,.0f} orders short over 2-21 Dec): supplements are replenished, so purchases were pulled forward. Found if the report identifies the December dip and nets it out (or says the window must include it).
4. Higher returns on promo orders. returns / net_sales on 28 Nov - 1 Dec = {pc(ret_promo)} vs {pc(ret_base)} on normal days. Found if the report notes promo-day returns are about double/much higher and deducts them.
5. Subsidy. {pc(returning_share, 0)} of promo-day orders came from returning customers; roughly {base_o * 4:,.0f} of the {promo_orders:,} promo orders (baseline volume) would have happened anyway, receiving about {usd(subsidy)} of discount. Found if the report says most discounted orders went to existing/returning customers or quantifies discount given on orders that would have happened anyway.
6. Promo-acquired customers repeat less. new_customer_cohorts_2025.csv: BFCM cohort 90-day repeat {pc(bf_rep90)} vs about {pc(norm_rep90)} for non-promo cohorts, so the recap's "new customers will pay back" ($210 lifetime value) is not supported. Found if the report flags the lower repeat rate of BFCM-acquired customers.

In your reasoning, list which of the 6 the report identifies with evidence (a number, a column or a quote).
PASS if at least 4 of the 6 are identified with evidence. FAIL otherwise. Vague mentions ("consider returns", "watch pull-forward") without tying them to the data do not count.
"""

decision = f"""
Ground truth (computed from the files): measured over the full effect window (17 Nov announcement to 21 Dec, when daily orders recovered) against the 35-day pre-announcement baseline, using the real cost of goods ({pc(cogs_ratio)} of gross sales), fulfilment, card fees, returns and the {usd(AD_SPEND)} extra paid social, BFCM 2025 changed contribution by about {usd(net_incr)} (a loss; any figure between {usd(net_incr * 1.4)} and {usd(net_incr * 0.6)} is within tolerance). The four promo days earned about {usd(promo_c_day)} contribution per day vs {usd(base_c)} on a normal day. At a true contribution of ~{pc(pv_order, 0)} of net sales, 25% off barely covers product and shipping costs; 30% off would lose money on every order.

The naive read (the team's recap) is: net sales up {pc(naive_lift_pct, 0)} vs the week before, ~{usd(naive_profit)} profit at "60% margin", so repeat it and go deeper (30%).

PASS if report.md's main recommendation is NOT to repeat a 25% sitewide discount and NOT to go deeper, because the event lost money (or at best broke even) once the real margin, pull-forward/baseline and costs are counted; acceptable alternatives include a much shallower or targeted offer (new or lapsed customers, bundles, gift with purchase, shorter or no pre-announcement) ideally with a holdout, or skipping a sitewide discount.
FAIL if the report recommends repeating 25% sitewide or going to 30%, calls last year profitable without qualification, or gives no clear recommendation.
"""

decoys = f"""
Two features of the data look unusual but are fine and must not be presented as problems:
- D1. Gross (pre-discount) order value is higher on promo days ({usd(gross_aov_promo)} vs {usd(gross_aov_base)}): customers built bigger baskets during the sale. This is real behaviour, not a data error or an inflated figure. (Saying net revenue per order fell because of the discount is correct and not a false alarm.)
- D2. Thanksgiving Day, 27 Nov 2025, has the lowest order count of the period ({by[THANKS]["orders"]} orders). It is a US public holiday inside the pre-sale wait; it is not a tracking outage or site problem.

PASS if report.md does not call D1 a data error/inflation/anomaly to fix and does not flag D2 as an outage, tracking gap or anomaly needing investigation. Mentioning either neutrally is fine.
FAIL if either is presented as an error or problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, recall), ("decision", 3, decision), ("no-false-alarms", 2, decoys)])
print(f"{NAME}: true net {net_incr:,.0f} vs naive {naive_profit:,.0f} (60%-margin correct window {net_incr_60:,.0f}); "
      f"cogs {cogs_ratio:.3f} pv {pv_order:.3f}; lull {lull_drop:.2f} post {post_drop:.2f}; returns {ret_promo:.3f}/{ret_base:.3f}; "
      f"returning {returning_share:.2f}; promo c/day {promo_c_day:,.0f} vs base {base_c:,.0f}")
