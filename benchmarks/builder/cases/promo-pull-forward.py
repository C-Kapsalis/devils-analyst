import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "promo-pull-forward"
rng = random.Random(4417)

START = dt.date(2026, 3, 2)
PROMO_START, PROMO_END = dt.date(2026, 3, 30), dt.date(2026, 4, 5)
POST_END = PROMO_END + dt.timedelta(days=21)
END = dt.date(2026, 5, 10)
COGS = 30.0
DISC = 0.20
WDAY = [1.04, 1.02, 1.00, 1.01, 1.06, 0.95, 0.92]

rows = []
d = START
while d <= END:
    if PROMO_START <= d <= PROMO_END:
        level = 900
    elif PROMO_END < d <= POST_END:
        level = 380
    else:
        level = 500
    orders = int(round(rng.gauss(level * WDAY[d.weekday()], level * 0.045)))
    aov = rng.gauss(62.0, 1.2)
    gross = round(orders * aov, 2)
    disc = round(gross * DISC, 2) if PROMO_START <= d <= PROMO_END else 0.0
    rows.append([d.isoformat(), orders, gross, disc])
    d += dt.timedelta(days=1)


def m(x):
    return ("-" if x < 0 else "+") + f"${abs(x):,.0f}"


def in_range(r, a, b):
    x = dt.date.fromisoformat(r[0])
    return a <= x <= b


def contrib(r):
    return r[2] - r[3] - COGS * r[1]


pre = [r for r in rows if in_range(r, START, PROMO_START - dt.timedelta(days=1))]
promo = [r for r in rows if in_range(r, PROMO_START, PROMO_END)]
post = [r for r in rows if in_range(r, PROMO_END + dt.timedelta(days=1), POST_END)]
recov = [r for r in rows if in_range(r, POST_END + dt.timedelta(days=1), END)]
assert len(pre) == 28 and len(promo) == 7 and len(post) == 21 and len(recov) == 14

base_orders = sum(r[1] for r in pre) / len(pre)
base_contrib = sum(contrib(r) for r in pre) / len(pre)
base_net = sum(r[2] - r[3] for r in pre) / len(pre)
window = promo + post
n_win = len(window)

promo_excess = sum(r[1] for r in promo) - 7 * base_orders
post_deficit = sum(r[1] for r in post) - 21 * base_orders
incr_orders = promo_excess + post_deficit
incr_contrib = sum(contrib(r) for r in window) - n_win * base_contrib
promo_contrib_delta = sum(contrib(r) for r in promo) - 7 * base_contrib
post_contrib_delta = sum(contrib(r) for r in post) - 21 * base_contrib
incr_net_rev = sum(r[2] - r[3] for r in window) - n_win * base_net

# alternative baseline: pre + recovery period
alt = pre + recov
alt_orders = sum(r[1] for r in alt) / len(alt)
alt_contrib = sum(contrib(r) for r in alt) / len(alt)
alt_incr_orders = sum(r[1] for r in window) - n_win * alt_orders
alt_incr_contrib = sum(contrib(r) for r in window) - n_win * alt_contrib

# naive numbers
promo_daily = sum(r[1] for r in promo) / 7
naive_order_lift = promo_daily / base_orders - 1
naive_net_rev_lift = (sum(r[2] - r[3] for r in promo) / 7) / base_net - 1
post_daily = sum(r[1] for r in post) / 21
discount_total = sum(r[3] for r in promo)

assert 0.7 < naive_order_lift < 0.9
assert promo_contrib_delta > 0, "naive promo-week-only contribution must look positive"
assert abs(incr_orders) < 0.2 * promo_excess and abs(alt_incr_orders) < 0.25 * promo_excess
assert incr_contrib < -40000 and alt_incr_contrib < -40000
assert naive_net_rev_lift > 0.3

calendar = to_csv(
    ["promo_name", "start_date", "end_date", "discount_type", "discount_value", "scope", "status"],
    [
        ["Spring Sale 2026", PROMO_START.isoformat(), PROMO_END.isoformat(), "percentage", 20, "sitewide", "completed"],
        ["Summer Sale 2026", "2026-07-06", "2026-07-12", "percentage", 20, "sitewide", "planned"],
    ],
)

prompt = f"""
The resources/ directory has our Shopify daily sales export for Lumen Home Goods, daily_orders.csv (date, orders, gross_revenue, discount_amount; gross_revenue is before discounts), and our promotions calendar, promo_calendar.csv. Our average cost per order (product cost plus pick, pack and shipping) is ${COGS:.0f}.

How did the Spring Sale perform? Should we run it again next quarter? Write report.md with the numbers and your recommendation.
"""

g_main = f"""
Ground truth: baseline before the sale (2-29 Mar 2026) averaged {base_orders:.0f} orders/day. During the Spring Sale ({PROMO_START:%d %b}-{PROMO_END:%d %b}) orders averaged {promo_daily:.0f}/day ({promo_excess:+,.0f} orders vs baseline), but for the 21 days after the sale ({PROMO_END + dt.timedelta(days=1):%d %b}-{POST_END:%d %b}) orders fell to {post_daily:.0f}/day ({post_deficit:+,.0f} vs baseline) before recovering to ~500/day. Net incremental orders over the sale plus the following 3 weeks: {incr_orders:+,.0f} (using pre+recovery days as baseline: {alt_incr_orders:+,.0f}). Most of the sale's extra orders were pulled forward from the following weeks.

Naive answer: "orders up {naive_order_lift*100:.0f}% during the sale week ({promo_excess:+,.0f} orders)", treated as the sale's incremental impact, ignoring the post-sale dip.

PASS if report.md identifies the post-sale drop in orders as pull-forward / cannibalisation (or equivalent) AND reports that net incremental orders across the sale plus the post-sale period are small (any figure between {min(incr_orders, alt_incr_orders) - 350:+,.0f} and {max(incr_orders, alt_incr_orders) + 350:+,.0f} orders, or a clear statement that the dip offset roughly all/most of the sale-week gain).
FAIL if report.md reports the sale-week lift (~{naive_order_lift*100:.0f}% / ~{promo_excess:,.0f} orders) as the incremental effect without netting out the post-sale dip, or does not notice the dip.
"""

g_profit = f"""
Ground truth contribution (gross_revenue - discount_amount - ${COGS:.0f} x orders): the pre-sale baseline is ${base_contrib:,.0f}/day. Over the sale week plus the following 21 days, actual contribution was {m(incr_contrib)} vs the no-promo baseline (pre+recovery baseline: {m(alt_incr_contrib)}). The sale week alone looks positive ({m(promo_contrib_delta)}), but the 21-day dip costs {m(post_contrib_delta)}. The ${discount_total:,.0f} of discounts were mostly given to orders that would have happened anyway. Net revenue (after discounts) over the same 28 days was {m(incr_net_rev)} vs baseline.

Naive answers: "net revenue up {naive_net_rev_lift*100:.0f}% in the sale week" or "sale week contribution {m(promo_contrib_delta)}", i.e. profitable.

PASS if report.md concludes the Spring Sale lost money / reduced contribution or profit versus not running it, with a net figure roughly in the range {m(min(incr_contrib, alt_incr_contrib)*1.3)} to {m(max(incr_contrib, alt_incr_contrib)*0.7)} OR a clearly-reasoned negative net impact that accounts for the post-sale period and the discount cost.
FAIL if report.md says the sale was profitable or revenue-positive overall, or only evaluates the sale week itself.
"""

g_rec = f"""
Correct recommendation: do not repeat the Spring Sale as designed (sitewide 20% off for a week) for the planned Summer Sale; it mostly shifted demand in time and gave away margin. Acceptable: cancel it, or redesign it (smaller discount, targeted at new/lapsed customers, a holdout test to measure incrementality) with the reasoning that the current design did not pay off.

PASS if report.md recommends against repeating the sale in its current form, or recommends only a redesigned/tested version, AND the reasoning cites the post-sale dip or the net negative contribution.
FAIL if report.md recommends running the same sale again (e.g. because orders/revenue rose {naive_order_lift*100:.0f}% in the sale week).
"""

write_case(
    NAME,
    {
        "resources/daily_orders.csv": to_csv(["date", "orders", "gross_revenue", "discount_amount"], rows),
        "resources/promo_calendar.csv": calendar,
    },
    prompt,
    [("pull-forward", 3, g_main), ("net-contribution", 2, g_profit), ("recommendation", 2, g_rec)],
)
print(f"{NAME}: base {base_orders:.0f}/d, promo {promo_daily:.0f}/d (+{naive_order_lift*100:.0f}%), post {post_daily:.0f}/d; net incr orders {incr_orders:+.0f} (alt {alt_incr_orders:+.0f}); contrib {incr_contrib:+,.0f} (alt {alt_incr_contrib:+,.0f})")
