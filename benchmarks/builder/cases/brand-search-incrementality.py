"""Brand search incrementality: platform ROAS on brand terms is ~12x, but when
brand ads were paused for 14 days organic brand clicks recovered ~85% of the
paid brand clicks and shop orders barely moved. Incremental return (pause vs
pre, adjusted by the non-brand trend) is below break-even at 40% margin."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "brand-search-incrementality"
rng = random.Random(6150)
MARGIN = 0.40
AOV = 38.0
START = dt.date(2026, 9, 1)
PAUSE_START = dt.date(2026, 9, 15)
DAYS = 28
WD = [1.05, 1.03, 1.0, 0.99, 0.95, 0.88, 1.10]  # Mon..Sun
TREND = 1.012            # small market lift during the pause fortnight
BRAND_CVR = 0.05         # brand visitors -> orders
RECAPTURE = 0.85
n = lambda: rng.gauss(1.0, 0.006)

gads, gsc, shop = [], [], []
for i in range(DAYS):
    d = START + dt.timedelta(days=i)
    paused = d >= PAUSE_START
    w = WD[d.weekday()]
    tr = TREND if paused else 1.0
    paid_brand_demand = 1000 * w * tr          # clicks the brand ad would get
    org_brand = 1500 * w * tr
    if paused:
        org_brand += RECAPTURE * paid_brand_demand
        paid_brand = 0
    else:
        paid_brand = paid_brand_demand
    paid_brand = int(paid_brand * n()) if paid_brand else 0
    org_brand = int(org_brand * n())
    org_nonbrand = int(2100 * w * tr * n())
    generic_clicks = int(900 * w * tr * n())
    # orders
    base_orders = 210 * w * tr                 # everything that isn't brand search
    brand_orders = BRAND_CVR * (paid_brand + org_brand)
    orders = int(round((base_orders + brand_orders) * rng.gauss(1.0, 0.008)))
    revenue = round(orders * AOV * rng.gauss(1.0, 0.01), 2)
    shop.append([d.isoformat(), orders, revenue])
    gsc.append([d.isoformat(), "brand", org_brand, int(org_brand / 0.62)])
    gsc.append([d.isoformat(), "nonbrand", org_nonbrand, int(org_nonbrand / 0.021)])
    if paid_brand:
        conv = round(paid_brand * BRAND_CVR * 1.1 * n(), 1)
        gads.append([d.isoformat(), "Brand - Exact", int(paid_brand / 0.41), paid_brand,
                     round(paid_brand * 0.17 * n(), 2), conv, round(conv * AOV * n(), 2)])
    gconv = round(generic_clicks * 0.018 * n(), 1)
    gads.append([d.isoformat(), "Generic - Coffee", int(generic_clicks / 0.052), generic_clicks,
                 round(generic_clicks * 0.95 * n(), 2), gconv, round(gconv * AOV * n(), 2)])

gads_csv = to_csv(["date", "campaign", "impressions", "clicks", "cost", "conversions", "conversions_value"], gads)
gsc_csv = to_csv(["date", "query_type", "clicks", "impressions"], gsc)
shop_csv = to_csv(["date", "orders", "revenue"], shop)

# ---- ground truth ----
is_pause = lambda s: dt.date.fromisoformat(s) >= PAUSE_START
def s(rows, idx, pause, pred=lambda r: True):
    return sum(r[idx] for r in rows if is_pause(r[0]) == pause and pred(r))
brand = lambda r: r[1] == "Brand - Exact"
brand_cost = s(gads, 4, False, brand)
brand_conv = s(gads, 5, False, brand)
brand_val = s(gads, 6, False, brand)
brand_clicks = s(gads, 3, False, brand)
naive_roas = brand_val / brand_cost

nb_pre = s(gsc, 2, False, lambda r: r[1] == "nonbrand"); nb_post = s(gsc, 2, True, lambda r: r[1] == "nonbrand")
trend = nb_post / nb_pre
ob_pre = s(gsc, 2, False, lambda r: r[1] == "brand"); ob_post = s(gsc, 2, True, lambda r: r[1] == "brand")
recapture = (ob_post - ob_pre * trend) / (brand_clicks * trend)
o_pre, o_post = s(shop, 1, False), s(shop, 1, True)
r_pre, r_post = s(shop, 2, False), s(shop, 2, True)

inc_orders_adj = o_pre * trend - o_post
inc_rev_adj = r_pre * trend - r_post
inc_orders_raw = o_pre - o_post
inc_rev_raw = r_pre - r_post
inc_roas_adj = inc_rev_adj / brand_cost
inc_roas_raw = inc_rev_raw / brand_cost
profit_adj = inc_rev_adj * MARGIN - brand_cost
be_roas = 1 / MARGIN

assert 10 < naive_roas < 15, naive_roas
assert 0.75 < recapture < 0.95, recapture
assert 0.8 < inc_roas_adj < 2.2, inc_roas_adj
assert inc_roas_raw < inc_roas_adj and inc_roas_raw < be_roas
assert profit_adj < 0
lo = min(inc_rev_raw, inc_rev_adj)
f = lambda x: f"{x:,.2f}"

prompt = """
We switched off our Google Ads brand campaign ("Brand - Exact") for two weeks, 15–28 September 2026, and turned it back on afterwards. In resources/ there's the Google Ads daily export (google_ads_daily.csv), Search Console clicks split by brand and non-brand queries (search_console_daily.csv), and our shop's daily orders and revenue (shop_daily.csv), covering the two weeks before and the two weeks off. Our gross margin is 40%. Is our brand search campaign worth what we pay for it? Write report.md with your numbers and a recommendation.
"""

g_inc = f"""
Ground truth (1–14 Sep with brand ads on vs 15–28 Sep with brand ads off):
- Brand campaign cost in the 14 days it ran: {f(brand_cost)}; Google-reported conversion value {f(brand_val)}, platform ROAS {naive_roas:.1f}x (this is the naive answer; it is not incremental).
- Organic brand clicks rose from {ob_pre:,} to {ob_post:,} while paid brand clicks ({brand_clicks:,}) disappeared: organic recaptured about {100*recapture:.0f}% of the paid brand clicks.
- Non-brand organic clicks (control) moved {100*(trend-1):+.1f}% between the two fortnights.
- Shop orders: {o_pre:,} -> {o_post:,}; revenue {f(r_pre)} -> {f(r_post)}.
- Incremental revenue from brand ads over 14 days: {f(inc_rev_adj)} trend-adjusted (pre revenue x non-brand ratio minus pause revenue), or {f(inc_rev_raw)} as a simple before/after difference. Incremental ROAS = {inc_roas_adj:.2f}x (adjusted) or {inc_roas_raw:.2f}x (simple). Incremental orders about {inc_orders_adj:.0f} (adjusted) or {inc_orders_raw:.0f} (simple).

PASS if report.md estimates the incremental value of brand ads from the pause comparison (shop orders/revenue before vs during the pause, optionally trend-adjusted) and arrives at an incremental ROAS roughly between {inc_roas_raw - 0.4:.1f}x and {inc_roas_adj + 0.4:.1f}x, or equivalent incremental revenue between {f(max(0.0, lo - 1500))} and {f(inc_rev_adj + 1500)}, for {f(brand_cost)} of cost.
FAIL if it evaluates the campaign on the platform ROAS of about {naive_roas:.1f}x (or on Google-reported conversions/value) as its main evidence, or does not quantify incrementality from the pause.
"""
g_decision = f"""
At 40% gross margin the break-even ROAS is {be_roas:.1f}x. Incremental gross profit from brand ads = {f(inc_rev_adj)} x 0.40 - {f(brand_cost)} = {f(profit_adj)} over 14 days (negative; with the simple before/after difference it is even worse: {f(inc_rev_raw * MARGIN - brand_cost)}).

PASS if report.md concludes that the brand campaign is not worth its current cost (loses money incrementally / below break-even at 40% margin) and recommends cutting, pausing, or sharply reducing it (e.g. lower bids/budget, keep only for competitor-conquesting defence or test further), while acknowledging organic picks up most brand clicks.
FAIL if it concludes the campaign is clearly worth it or should be kept/scaled because of the ~{naive_roas:.0f}x platform ROAS.
"""
g_recapture = f"""
Organic brand clicks (Search Console, query_type = brand) went from {ob_pre:,} to {ob_post:,} when paid brand clicks ({brand_clicks:,}) went to zero, i.e. organic recaptured roughly {100*recapture:.0f}% of paid brand clicks (accept 70–100%). Non-brand organic clicks were roughly flat ({100*(trend-1):+.1f}%), so the shift is not a general traffic change.

PASS if report.md uses the Search Console data to show that organic brand clicks rose to absorb most of the lost paid brand clicks (any recapture figure in the 70–100% range, or equivalent click numbers), and uses non-brand as a control or sanity check.
FAIL if it ignores Search Console or claims the paid brand clicks were simply lost.
"""

write_case(NAME, {"resources/google_ads_daily.csv": gads_csv, "resources/search_console_daily.csv": gsc_csv,
                  "resources/shop_daily.csv": shop_csv}, prompt,
           [("incremental-return", 3, g_inc), ("keep-or-cut", 2, g_decision), ("organic-recapture", 1, g_recapture)])
print(f"{NAME}: platform ROAS {naive_roas:.1f}x; incremental ROAS {inc_roas_adj:.2f}x adj / {inc_roas_raw:.2f}x raw; recapture {recapture:.0%}; "
      f"profit {profit_adj:,.0f} on cost {brand_cost:,.0f}")
