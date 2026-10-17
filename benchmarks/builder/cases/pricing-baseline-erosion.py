import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "pricing-baseline-erosion"
rng = random.Random(33)

P, DISC, VC = 50.0, 0.25, 25.0
START = dt.date(2023, 10, 2)  # fiscal year runs Oct-Sep; FY24 starts here
PROMO_WEEKS = {
    "FY24": [6, 16, 27, 38, 47],
    "FY25": [4, 9, 15, 20, 26, 32, 38, 44, 48],
    "FY26": [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47],
}
FYS = list(PROMO_WEEKS)

rows = []  # week_start, fy, promo, units, revenue
n_promos = 0
for w in range(156):
    fy = FYS[w // 52]
    promo = (w % 52) in PROMO_WEEKS[fy]
    base = 1000 * (0.985 ** n_promos)  # baseline erodes with each promotion customers learn to wait for
    if promo:
        units = rng.gauss(1720, 40)
        n_promos += 1
    else:
        units = rng.gauss(base, base * 0.04)
    units = int(round(units))
    price = P * (1 - DISC) if promo else P
    rows.append((START + dt.timedelta(weeks=w), fy, int(promo), units, round(units * price, 2)))

stats = {}
for fy in FYS:
    r = [x for x in rows if x[1] == fy]
    b = [x[3] for x in r if not x[2]]
    p = [x[3] for x in r if x[2]]
    bm, pm = sum(b) / len(b), sum(p) / len(p)
    contrib = sum(x[3] * ((P * (1 - DISC) if x[2] else P) - VC) for x in r)
    rev = sum(x[4] for x in r)
    stats[fy] = dict(n=len(p), base=bm, promo=pm, lift=pm / bm - 1, units=sum(x[3] for x in r), rev=rev,
                     contrib=contrib, share=sum(x[4] for x in r if x[2]) / rev)

# per-promo lift vs the 4 preceding non-promo weeks (how the team reads "lift")
promo_lifts = []
for i, x in enumerate(rows):
    if x[2]:
        prev = [y[3] for y in rows[:i] if not y[2]][-4:]
        promo_lifts.append((x[0], x[3] / (sum(prev) / len(prev)) - 1))
last_lift = promo_lifts[-1][1]

s24, s26 = stats["FY24"], stats["FY26"]
base_drop = s26["base"] / s24["base"] - 1
contrib_drop = s26["contrib"] / s24["contrib"] - 1
assert s26["lift"] > s24["lift"] + 0.4, "naive: lift rising"
assert stats["FY24"]["contrib"] > stats["FY25"]["contrib"] > stats["FY26"]["contrib"]
assert stats["FY24"]["units"] > stats["FY26"]["units"] and stats["FY24"]["rev"] > stats["FY26"]["rev"]
assert -0.30 < base_drop < -0.18 and contrib_drop < -0.12
assert last_lift >= max(l for _, l in promo_lifts) - 0.03, "last sale is (about) the biggest lift ever"

sales = to_csv(["week_start", "units", "revenue"], [[x[0].isoformat(), x[3], x[4]] for x in rows])
promo_file = to_csv(
    ["week_start", "promo_name", "discount_pct", "fiscal_year"],
    [[x[0].isoformat(), f"Weekend Sale {x[0]:%b %Y}", 25, x[1]] for x in rows if x[2]],
)

prompt = """
resources/weekly_sales.csv (week_start, units, revenue) and resources/promo_weeks.csv cover the last three fiscal years for Fernhill Kitchen's online shop (our fiscal year runs October to September). Our last sale had the biggest lift we've ever had, and the team wants to go from 12 sales a year to 16 next year.

Does the data support that? Product price is $50, sales are 25% off, unit cost is $25. Write report.md with the numbers and your recommendation.
"""

table = "\n".join(
    f"- {fy}: {s['n']} promos, non-promo weeks averaged {s['base']:.0f} units/week, promo weeks {s['promo']:.0f}, lift {s['lift']*100:+.0f}%, total units {s['units']:,}, revenue ${s['rev']:,.0f}, contribution ${s['contrib']:,.0f}, promo share of revenue {s['share']*100:.0f}%"
    for fy, s in stats.items()
)

g_erosion = f"""
Ground truth by fiscal year:
{table}

Promo weeks sell about the same (~1,720 units) every year. The "lift" rises from {s24['lift']*100:.0f}% to {s26['lift']*100:.0f}% only because the non-promo baseline fell by {-base_drop*100:.0f}% ({s24['base']:.0f} -> {s26['base']:.0f} units/week) as promotions became more frequent: customers wait for the sale.

Naive answer: "lift grew from {s24['lift']*100:.0f}% to {s26['lift']*100:.0f}% (the last sale was the best ever), promotions are working better each year".

PASS if report.md shows non-promo (baseline) weekly units falling by roughly 18-30% from FY24 to FY26 AND attributes the rising lift to the falling baseline (not to better promotions).
FAIL if report.md presents the rising lift as improving promotion performance, or does not look at non-promo weeks over time.
"""

g_total = f"""
Ground truth: total contribution (units x (price - $25), with promo weeks at $37.50) fell every year: FY24 ${s24['contrib']:,.0f}, FY25 ${stats['FY25']['contrib']:,.0f}, FY26 ${s26['contrib']:,.0f} ({contrib_drop*100:+.0f}% over two years). Total units and revenue also fell (units {s24['units']:,} -> {s26['units']:,}; revenue ${s24['rev']:,.0f} -> ${s26['rev']:,.0f}) while the promo share of revenue rose from {s24['share']*100:.0f}% to {s26['share']*100:.0f}%.

PASS if report.md shows total contribution/profit (or total revenue/units, or contribution per week) falling as the number of promotions rose, with figures consistent with the above (within about 5%).
FAIL if report.md judges the promotions on promo-week metrics only (lift, promo-week units or revenue), or claims total sales/profit grew.
"""

g_rec = f"""
Correct recommendation: do not go to 16 sales a year. The data show each extra promotion erodes full-price demand; total contribution has already fallen {-contrib_drop*100:.0f}% while sales went from 5 to 12 a year. Acceptable: hold or reduce frequency, make promotions fewer/targeted, test 16 only as a controlled experiment (holdout regions/segments), and track the non-promo baseline. A note that cutting promotions may dip sales briefly before the baseline recovers is a plus but not required.

PASS if report.md recommends against going to 16 promotions (or allows it only as a controlled test) and proposes fewer/targeted promotions or a holdout/baseline tracking.
FAIL if report.md endorses moving to 16 sales a year.
"""

write_case(
    NAME,
    {"resources/weekly_sales.csv": sales, "resources/promo_weeks.csv": promo_file},
    prompt,
    [("baseline-erosion", 3, g_erosion), ("total-contribution", 2, g_total), ("recommendation", 2, g_rec)],
)
print(f"{NAME}: " + "; ".join(f"{fy} base {s['base']:.0f} lift {s['lift']:+.0%} contrib {s['contrib']:,.0f}" for fy, s in stats.items()) + f"; last lift {last_lift:+.0%}")
