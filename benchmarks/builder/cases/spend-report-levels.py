"""Cross-platform cost export: the same spend appears at account, campaign and
ad_group report_level; manual_expenses rows (agency fee, contractor) are not
media; Google cost is in cost_micros; Meta is billed in GBP while the business
reports in EUR."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "spend-report-levels"
rng = random.Random(2207)
MONTHS = ["2026-07-01", "2026-08-01", "2026-09-01"]
FX = {"2026-07-01": 1.1712, "2026-08-01": 1.1655, "2026-09-01": 1.1798}  # 1 GBP = x EUR

PLATFORMS = {
    "google_ads": ("812-445-1907", "EUR", {
        "Search - Brand": (["Brand Exact", "Brand Phrase"], 1800),
        "Search - Generic Coffee Beans": (["Whole Bean", "Ground Coffee", "Decaf"], 5200),
        "Shopping - All Products": (["Best Sellers", "Subscriptions", "Equipment"], 6100),
        "PMax - Catalog": (["All Assets"], 3900),
    }),
    "meta_ads": ("act_30918824177", "GBP", {
        "Prospecting - Broad": (["Adv+ Audience", "Lookalike 3%", "Interest Coffee"], 4800),
        "Retargeting - 30d": (["Site Visitors 30d", "Cart Abandoners"], 1500),
        "Subscriptions Launch": (["Video Views", "Static Offer"], 2200),
    }),
    "microsoft_ads": ("F1209337", "EUR", {
        "Search - Brand": (["Brand Exact"], 300),
        "Search - Generic": (["Whole Bean", "Ground Coffee"], 950),
    }),
}
MANUAL = [("Agency management fee", 3500.0), ("Freelance PPC contractor", 2400.0)]

rows = []
media = {p: {m: 0.0 for m in MONTHS} for p in PLATFORMS}   # native currency, one level
for m in MONTHS:
    for p, (acct, cur, camps) in PLATFORMS.items():
        acct_total = 0
        camp_rows = []
        for camp, (ags, base) in camps.items():
            ag_vals = []
            for ag in ags:
                v = round(base / len(ags) * rng.uniform(0.75, 1.25), 2)
                ag_vals.append((ag, v))
            ctot = round(sum(v for _, v in ag_vals), 2)
            acct_total += ctot
            camp_rows.append(("campaign", camp, "", ctot))
            camp_rows += [("ad_group", camp, ag, v) for ag, v in ag_vals]
        acct_total = round(acct_total, 2)
        media[p][m] = acct_total
        for lvl, camp, ag, v in [("account", "", "", acct_total)] + camp_rows:
            if p == "google_ads":
                rows.append([m, p, acct, lvl, camp, ag, cur, None, int(round(v * 1_000_000))])
            else:
                rows.append([m, p, acct, lvl, camp, ag, cur, v, None])
    for name, fee in MANUAL:
        rows.append([m, "manual_expenses", "finance", "account_service", name, "", "EUR", fee, None])

rows.sort(key=lambda r: (r[0], r[1], ["account", "campaign", "ad_group", "account_service"].index(r[3]), r[4], r[5]))
cost_csv = to_csv(["month", "platform", "account_id", "report_level", "campaign_name", "ad_group_name", "currency",
                   "spend", "cost_micros"], rows)
fx_csv = to_csv(["month", "from_currency", "to_currency", "rate"], [[m, "GBP", "EUR", FX[m]] for m in MONTHS])

# orders, daily
import datetime as dt
orows = []
d = dt.date(2026, 7, 1)
while d <= dt.date(2026, 9, 30):
    n = int(rng.gauss(72, 9)) + (10 if d.weekday() in (0, 6) else 0)
    orows.append([d.isoformat(), n, round(n * rng.uniform(36, 44), 2)])
    d += dt.timedelta(days=1)
orders_csv = to_csv(["date", "orders", "revenue_eur"], orows)

# ---- ground truth ----
def amount(r):
    return r[7] if r[7] is not None else r[8] / 1e6
def to_eur(r):
    return amount(r) * (FX[r[0]] if r[6] == "GBP" else 1.0)
media_rows = [r for r in rows if r[3] == "campaign"]
by_plat = {p: sum(to_eur(r) for r in media_rows if r[1] == p) for p in PLATFORMS}
total = sum(by_plat.values())
# check levels reconcile
for lvl in ("account", "ad_group"):
    alt = sum(to_eur(r) for r in rows if r[3] == lvl)
    assert abs(alt - total) < 1, (lvl, alt, total)
orders = sum(r[1] for r in orows)
cpo = total / orders
fees = sum(r[7] for r in rows if r[1] == "manual_expenses")
meta_gbp = sum(amount(r) for r in media_rows if r[1] == "meta_ads")

naive_all = sum(amount(r) for r in rows)                     # every row, every level, no FX
naive_spend_col = sum(r[7] for r in rows if r[7] is not None)  # ignores Google micros
naive_fees = total + fees                                    # right level, but fees counted as media
naive_nofx = total - by_plat["meta_ads"] + meta_gbp           # Meta left in GBP
naive_micros_raw = sum((r[7] if r[7] is not None else r[8]) for r in rows if r[3] == "campaign")
assert naive_all > 2.8 * total
assert naive_fees > 1.15 * total
assert abs(naive_nofx - total) > 1500

f = lambda x: f"{x:,.2f}"
plat_lines = ", ".join(f"{p} {f(v)}" for p, v in by_plat.items())

prompt = """
In resources/ you'll find our cross-platform cost export for Q3 2026 (ad_costs_q3.csv), the FX rates our finance team uses (fx_rates.csv) and our daily orders (orders_q3.csv). We report in EUR. What did we spend on paid media in Q3 in EUR, by platform, and what was our cost per order? Write report.md with the numbers and whether you think the cost per order is something we should worry about given our average order value.
"""

g_total = f"""
Ground truth Q3 2026 paid media spend in EUR (one report_level only, media platforms only, Google cost_micros / 1,000,000, Meta GBP converted at the monthly fx_rates.csv rate):
- By platform: {plat_lines}
- Total: {f(total)} EUR
(Meta native spend was {f(meta_gbp)} GBP.)
Common wrong totals:
- Summing every row across account + campaign + ad_group levels (and fees, no FX): {f(naive_all)}
- Summing only the `spend` column (dropping Google, which is in cost_micros) across all levels: {f(naive_spend_col)}
- Right level but including manual_expenses (agency fee, contractor): {f(naive_fees)}
- Right level but leaving Meta in GBP: {f(naive_nofx)}

PASS if report.md gives total Q3 paid media spend within 1.5% of {f(total)} EUR AND per-platform figures within 2% of the values above.
FAIL if the total is near any of the wrong totals, or if Google spend is shown in micros (billions) or omitted.
"""
g_cpo = f"""
Q3 2026 orders (sum of orders_q3.csv): {orders:,}.
Ground truth cost per order = paid media EUR / orders = {f(total)} / {orders:,} = {f(cpo)} EUR.
Wrong values: {f(naive_all / orders)} (every row summed), {f(naive_fees / orders)} (agency/contractor fees counted as media), {f(naive_nofx / orders)} (Meta left in GBP).

PASS if report.md states a media cost per order within 2% of {f(cpo)} EUR. A separate fully-loaded figure including the manual expenses ({f(naive_fees / orders)}) is fine as long as it is labelled as including fees and the media-only figure is also given.
FAIL if the only cost per order given is {f(naive_all / orders)}, {f(naive_fees / orders)} unlabelled, or another value more than 2% from {f(cpo)}.
"""
g_scope = f"""
The export contains rows that are not paid media: platform = manual_expenses, report_level = account_service ("Agency management fee", "Freelance PPC contractor"), totalling {f(fees)} EUR over Q3. It also repeats the same spend at account, campaign and ad_group report levels.

PASS if report.md explicitly explains that it used only one report_level (or otherwise de-duplicated levels) AND that it excluded (or reported separately) the manual_expenses / agency / contractor costs from paid media.
FAIL if it does not mention either point, or adds the {f(fees)} EUR of fees into paid media spend without labelling it.
"""

write_case(NAME, {"resources/ad_costs_q3.csv": cost_csv, "resources/fx_rates.csv": fx_csv,
                  "resources/orders_q3.csv": orders_csv}, prompt,
           [("media-spend-eur", 3, g_total), ("cost-per-order", 2, g_cpo), ("scope-explained", 1, g_scope)])
print(f"{NAME}: media EUR {total:,.2f} ({plat_lines}); CPO {cpo:.2f}; naive all-rows {naive_all:,.0f}, +fees {naive_fees:,.0f}, noFX {naive_nofx:,.0f}")
