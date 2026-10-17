"""Meta attribution windows are nested (1d click is inside 7d click, which is
inside 28d click; 1d view inside 7d view). Adding the window columns together
counts the same purchase several times, more purchases than the store sold,
and the heavy view-through on the video campaign makes it look cheapest."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "fb-attribution-windows"
rng = random.Random(9031)


def poisson(lam):
    if lam > 60:
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1


def binom(n, p):
    return sum(1 for _ in range(n) if rng.random() < p)


# campaign: (id, daily spend, CPM, link CTR, 7d-click CPA, 1dc share of 7dc, 28dc/7dc, 1dv/7dc, 7dv/7dc)
CAMPAIGNS = {
    "Prospecting - Broad":             ("120210443", 450.0, 9.5, 0.011, 38.0, 0.68, 1.22, 0.40, 0.70),
    "Prospecting - Lookalike 2%":      ("120210447", 350.0, 10.5, 0.012, 42.0, 0.70, 1.20, 0.35, 0.60),
    "Retargeting - Site Visitors 30d": ("120210452", 250.0, 11.5, 0.021, 26.0, 0.80, 1.06, 0.35, 0.60),
    "Video - Brand Awareness":         ("120210458", 300.0, 4.5, 0.008, 95.0, 0.65, 1.25, 14.00, 18.00),
    "Advantage+ Shopping":             ("120210461", 600.0, 8.5, 0.014, 30.0, 0.75, 1.12, 0.30, 0.50),
}
AOV = 68.0
WIN = ["1d_click", "7d_click", "28d_click", "1d_view"]  # Meta removed 7d/28d view windows in Jan 2026

rows = []
for d in range(1, 31):
    date = f"2026-09-{d:02d}"
    for c, (cid, sp, cpm, ctr, cpa, r1, r28, rv1, rv7) in CAMPAIGNS.items():
        spend = round(sp * rng.uniform(0.85, 1.15), 2)
        imps = int(spend / cpm * 1000 * rng.uniform(0.93, 1.07))
        clicks = int(imps * ctr * rng.uniform(0.9, 1.1))
        c7 = poisson(spend / cpa)
        c1 = binom(c7, r1)
        c28 = c7 + poisson(c7 * (r28 - 1) + 0.05)
        v1 = poisson(c7 * rv1 + spend / cpa * rv1 * 0.2)
        v7 = v1 + poisson(max(0.0, (rv7 - rv1)) * (c7 + 0.3))
        counts = [c1, c7, c28, v1]  # v7 still drawn above to keep the seed stream stable
        vals = [round(n * AOV * rng.uniform(0.9, 1.1), 2) for n in counts]
        rows.append([date, cid, c, spend, imps, clicks, "purchase"] + counts + vals)

header = (["date_start", "campaign_id", "campaign_name", "spend", "impressions", "inline_link_clicks", "action_type"]
          + [f"n_{w}" for w in WIN] + [f"value_{w}" for w in WIN])
conv_csv = to_csv(header, rows)

# backend orders (all channels) for September
orders_rows = []
for d in range(1, 31):
    o = int(rng.gauss(140, 9))
    gs = round(o * rng.uniform(70, 76), 2)
    orders_rows.append([f"2026-09-{d:02d}", o, gs, round(gs * rng.uniform(0.9, 0.93), 2)])
orders_csv = to_csv(["date", "orders", "gross_sales", "net_sales"], orders_rows)

# ---- ground truth ----
IX = {w: 7 + i for i, w in enumerate(WIN)}
spend_tot = sum(r[3] for r in rows)
tot = {w: sum(r[IX[w]] for r in rows) for w in WIN}
store_orders = sum(r[1] for r in orders_rows)
p7 = tot["7d_click"]
cpa7 = spend_tot / p7
default = tot["7d_click"] + tot["1d_view"]  # Meta default setting (7d click + 1d view)
sum_all = sum(tot.values())
sum_click = tot["1d_click"] + tot["7d_click"] + tot["28d_click"]
cpa_all = spend_tot / sum_all

camp = {}
for c in CAMPAIGNS:
    rr = [r for r in rows if r[2] == c]
    s = sum(r[3] for r in rr)
    n7 = sum(r[IX["7d_click"]] for r in rr)
    na = sum(sum(r[IX[w]] for w in WIN) for r in rr)
    nd = n7 + sum(r[IX["1d_view"]] for r in rr)
    camp[c] = dict(spend=s, n7=n7, cpa7=s / n7, cpa_all=s / na, cpa_def=s / nd)

best7 = min(camp, key=lambda c: camp[c]["cpa7"])
worst7 = max(camp, key=lambda c: camp[c]["cpa7"])
best_naive = min(camp, key=lambda c: camp[c]["cpa_all"])
assert best_naive == "Video - Brand Awareness" == worst7, (best_naive, worst7)
assert best7 != best_naive
assert sum_all > 1.5 * store_orders and sum_all > 3 * p7, (sum_all, store_orders, p7)
assert sum_click > store_orders > default > p7, (sum_click, store_orders, default, p7)

f = lambda x: f"{x:,.2f}"
camp_lines = "\n".join(
    f"- {c}: spend {f(v['spend'])}, 7d-click purchases {v['n7']}, cost per purchase {f(v['cpa7'])} "
    f"(wrong, all windows summed: {f(v['cpa_all'])})" for c, v in camp.items())

prompt = """
resources/ has our Meta Ads purchase export for September 2026 by campaign and day (meta_purchases_sep.csv) and our store's daily orders (shop_orders_daily.csv). How many purchases did Meta bring in September, and what did each one cost? Break it down by campaign and tell me which campaign is the most cost-efficient place to put extra budget. Write the answer up in report.md.
"""

g_total = f"""
The n_1d_click, n_7d_click, n_28d_click and n_1d_view columns are overlapping attribution windows for the SAME purchases (1d click is inside 7d click, which is inside 28d click; 1d view purchases overlap the click windows). Only one window may be used; the standard comparable count is 7-day click.
Ground truth, September 2026, all campaigns:
- Spend: {f(spend_tot)}
- Purchases on 7-day click: {p7:,}; cost per purchase = {f(cpa7)}
- Store orders from ALL channels in September: {store_orders:,}
Acceptable alternative ONLY if explicitly labelled as Meta's default "7-day click + 1-day view" setting: {default:,} purchases, cost {f(spend_tot / default)}.
Wrong answers from adding windows together:
- all five windows summed: {sum_all:,} purchases, cost {f(cpa_all)} (more than the store's {store_orders:,} total orders)
- 1d + 7d + 28d click summed: {sum_click:,} purchases, cost {f(spend_tot / sum_click)}

PASS if report.md's headline Meta purchase count is {p7:,} (within 2%) with cost per purchase {f(cpa7)} (within 3%), or is the explicitly labelled 7d-click + 1d-view figure {default:,} (within 2%).
FAIL if the headline count is a sum of several windows (e.g. near {sum_all:,} or {sum_click:,}), if it reports a Meta purchase count higher than the store's {store_orders:,} orders without rejecting it, or if no single total is given.
"""

g_camp = f"""
Ground truth cost per purchase by campaign on 7-day click (spend / n_7d_click):
{camp_lines}
On 7-day click the cheapest campaign is "{best7}" ({f(camp[best7]['cpa7'])}) and the most expensive is "{worst7}" ({f(camp[worst7]['cpa7'])}).
The trap: "{best_naive}" gets most of its credit from view-through windows, so summing windows makes it look like the cheapest campaign ({f(camp[best_naive]['cpa_all'])}).

PASS if report.md's per-campaign cost per purchase figures match the 7-day-click values above within 5% (or, if the report uses the labelled 7d-click + 1d-view setting, are consistent with that), AND it does NOT recommend "{best_naive}" as the most cost-efficient campaign for extra budget.
FAIL if it ranks "{best_naive}" as the cheapest/most efficient campaign, or recommends it for extra budget on cost-per-purchase grounds, or the per-campaign costs come from summed windows.
"""

g_recon = f"""
Reconciliation check. Store orders in September (all channels): {store_orders:,}. Meta 7-day-click purchases: {p7:,} ({100 * p7 / store_orders:.0f}% of store orders). Summing all window columns gives {sum_all:,}, which is {sum_all / store_orders:.1f}x everything the store sold, so the windows cannot be added.

PASS if report.md compares Meta's purchase count to the store order total (or otherwise explains that the window columns overlap / are nested and must not be summed).
FAIL if it neither mentions the overlap of the windows nor sanity-checks against store orders, or if it presents a Meta purchase count above {store_orders:,} as real.
"""

write_case(NAME, {"resources/meta_purchases_sep.csv": conv_csv, "resources/shop_orders_daily.csv": orders_csv},
           prompt, [("purchase-total", 3, g_total), ("campaign-cpa", 2, g_camp), ("store-reconciliation", 1, g_recon)])
print(f"{NAME}: 7dc purchases {p7} CPA {cpa7:.2f}; naive all-windows {sum_all} CPA {cpa_all:.2f}; store orders {store_orders}; "
      f"best 7dc {best7}, naive best {best_naive}")
