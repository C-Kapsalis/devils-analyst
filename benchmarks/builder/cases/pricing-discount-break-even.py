import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "pricing-discount-break-even"
rng = random.Random(22)

COST_SHARE, SHIP, AOV, DISC = 0.52, 7.0, 64.0, 0.20
START = dt.date(2026, 8, 3)
P0, P1 = dt.date(2026, 9, 14), dt.date(2026, 9, 20)

rows = []  # date, new, returning, gross, discount
for d in range(70):
    day = START + dt.timedelta(days=d)
    promo = P0 <= day <= P1
    new, ret = rng.gauss(120, 8), rng.gauss(180, 10)
    if promo:
        new *= 1.30
        ret *= 1.38
    new, ret = int(round(new)), int(round(ret))
    gross = round((new + ret) * rng.gauss(AOV, 1.0), 2)
    disc = round(gross * DISC * (0.93 if promo else 0), 2)  # 93% of promo-week revenue used the code
    rows.append((day, new, ret, gross, disc))


def contrib(r):
    return r[3] - r[4] - COST_SHARE * r[3] - SHIP * (r[1] + r[2])


promo = [r for r in rows if P0 <= r[0] <= P1]
base = [r for r in rows if not (P0 <= r[0] <= P1)]
pre = [r for r in rows if r[0] < P0]
post = [r for r in rows if r[0] > P1]
assert len(promo) == 7


def avg(rs, f):
    return sum(f(r) for r in rs) / len(rs)


orders = lambda r: r[1] + r[2]
net = lambda r: r[3] - r[4]
bo, po = avg(base, orders), avg(promo, orders)
bn, pn = avg(base, net), avg(promo, net)
bc, pc = avg(base, contrib), avg(promo, contrib)
week_delta = 7 * (pc - bc)
pre_c = avg(pre, contrib)
week_delta_pre = 7 * (pc - pre_c)
disc_total = sum(r[4] for r in promo)
incr_orders = 7 * (po - bo)
promo_orders = 7 * po
ret_share = sum(r[2] for r in promo) / sum(orders(r) for r in promo)
order_lift, net_lift = po / bo - 1, pn / bn - 1
base_aov = avg(base, lambda r: r[3] / orders(r))
margin = 1 - COST_SHARE - SHIP / base_aov
be = {d: margin / (margin - d) - 1 for d in (0.20, 0.15, 0.10)}
post_lift = avg(post, orders) / avg(pre, orders) - 1

assert order_lift > 0.25 and net_lift > 0.05, "naive read must look like a win"
assert week_delta < -10000 and week_delta_pre < -10000
assert abs(post_lift) < 0.04, "no post-promo dip in this case"
assert be[0.20] > 1.0 and order_lift < be[0.10], "achieved lift is below break-even even at 10% off"

daily = to_csv(
    ["date", "new_customer_orders", "returning_customer_orders", "gross_revenue", "discount_amount"],
    [[r[0].isoformat(), r[1], r[2], r[3], r[4]] for r in rows],
)

prompt = """
resources/daily_sales.csv is the Shopify export for Northwind Coffee's online store (date, new_customer_orders, returning_customer_orders, gross_revenue, discount_amount; gross revenue is before discounts). From 14 to 20 September we ran 20% off everything for our email subscribers (code VIP20). Product cost is 52% of full price and pick, pack and ship is $7 per order.

Was it worth it, and what discount should we use for the next one? Write report.md with the numbers and your recommendation.
"""

lo, hi = week_delta * 1.5, week_delta * 0.55
g_contrib = f"""
Ground truth (contribution = gross_revenue - discount_amount - 52% x gross_revenue - $7 x orders): baseline days outside the promo averaged ${bc:,.0f} contribution/day; promo week averaged ${pc:,.0f}/day, so the promotion cost about ${-week_delta:,.0f} of contribution over the week (using only the pre-promo days as baseline: ${-week_delta_pre:,.0f}). ${disc_total:,.0f} of discounts were given, mostly on orders that would have happened anyway: only about {incr_orders:,.0f} of {promo_orders:,.0f} promo-week orders were incremental.

Naive answers: "orders up {order_lift*100:.0f}%", "net revenue up {net_lift*100:.0f}%", or counting code redemptions, and calling the promo a success.

PASS if report.md concludes the promo REDUCED contribution / profit versus a normal week, with a weekly figure roughly between -${-lo:,.0f} and -${-hi:,.0f}, OR a clearly reasoned negative profit impact that accounts for the discount given on baseline (would-have-bought-anyway) orders.
FAIL if report.md calls the promo profitable or judges it on revenue, orders or redemptions only.
"""

g_be = f"""
Ground truth: contribution margin per order at full price is about {margin*100:.0f}% (1 - 52% product cost - $7 / ~${base_aov:.0f} AOV). The order lift needed to break even on contribution is margin / (margin - discount) - 1: about {be[0.20]*100:.0f}% at 20% off, {be[0.15]*100:.0f}% at 15%, {be[0.10]*100:.0f}% at 10%. The actual lift was {order_lift*100:.0f}%.

PASS if report.md states the lift needed to break even at 20% off as roughly 95%-140% (or more), or gives a break-even table by discount depth with values consistent with these, and compares it to the actual ~{order_lift*100:.0f}% lift.
FAIL if no break-even lift / required-volume figure is given, or the break-even figure is below 60% at 20% off.
"""

g_rec = f"""
Ground truth: {ret_share*100:.0f}% of promo-week orders came from returning customers, and about {promo_orders - incr_orders:,.0f} of the {promo_orders:,.0f} promo-week orders would have happened anyway, so most of the discount subsidised existing demand. The achieved lift ({order_lift*100:.0f}%) is below the break-even lift even at 10% off ({be[0.10]*100:.0f}%), so a deeper sitewide discount cannot pay.

PASS if report.md notes that most promo orders/discount went to customers who would have bought anyway (returning-customer share or baseline netting) AND recommends a shallower discount, a targeted offer (new or lapsed customers, threshold/bundle), no discount, and/or a holdout test for the next one.
FAIL if report.md recommends repeating 20% (or deeper) off for all subscribers / sitewide.
"""

write_case(
    NAME,
    {"resources/daily_sales.csv": daily},
    prompt,
    [("contribution", 3, g_contrib), ("break-even", 2, g_be), ("subsidy-recommendation", 2, g_rec)],
)
print(f"{NAME}: orders {order_lift:+.1%}, net rev {net_lift:+.1%}; contrib/day {bc:,.0f}->{pc:,.0f}, week {week_delta:+,.0f} (pre-only {week_delta_pre:+,.0f}); disc {disc_total:,.0f}; incr {incr_orders:.0f}/{promo_orders:.0f}; ret share {ret_share:.0%}; BE20 {be[0.2]:.0%} BE10 {be[0.1]:.0%}")
