import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

# Brightwater Pools (fictional pool-supplies retailer). Organic clicks fall ~25% Q3 vs Q2,
# but impressions fall by the same amount, positions and CTR are flat, and competitors'
# estimated organic clicks fall ~24% too. Category demand fell; our share is flat.
NAME = "seo-category-decline"
rng = random.Random(4505)

Q2 = [dt.date(2026, 4, 6) + dt.timedelta(days=7 * i) for i in range(13)]   # week starts (Mondays)
Q3 = [dt.date(2026, 7, 6) + dt.timedelta(days=7 * i) for i in range(13)]
weeks = Q2 + Q3

def demand(i):  # category demand index: plateau in Q2, step down + slow fade through Q3
    return 1.0 if i < 13 else 0.81 - 0.01 * (i - 13)

gsc = []
for i, w in enumerate(weeks):
    d = demand(i) * rng.uniform(0.97, 1.03)
    for qt, imp0, ctr0, pos0 in (("brand", 61000, 0.36, 1.3), ("nonbrand", 405000, 0.031, 8.4)):
        imp = round(imp0 * d * rng.uniform(0.98, 1.02))
        pos = round(pos0 + rng.uniform(-0.15, 0.15), 2)
        clk = round(imp * ctr0 * rng.uniform(0.97, 1.03))
        gsc.append([w.isoformat(), qt, clk, imp, pos])

COMPS = [("Aqua Depot", 52000), ("PoolPro Supply", 38000), ("SplashMart", 24500)]
comp = []
for i, w in enumerate(weeks):
    for c, base in COMPS:
        comp.append([w.isoformat(), c, round(base * demand(i) * rng.uniform(0.95, 1.05) * (1.0 if i < 13 else 1.01))])

inq = lambda rows, Q: [r for r in rows if dt.date.fromisoformat(r[0]) in Q]
def tot(rows, idx): return sum(r[idx] for r in rows)
c2, c3 = tot(inq(gsc, Q2), 2), tot(inq(gsc, Q3), 2)
i2, i3 = tot(inq(gsc, Q2), 3), tot(inq(gsc, Q3), 3)
clk_chg, imp_chg = c3 / c2 - 1, i3 / i2 - 1
ctr2, ctr3 = c2 / i2, c3 / i3
def wpos(rows, qt):
    rs = [r for r in rows if r[1] == qt]
    return sum(r[3] * r[4] for r in rs) / sum(r[3] for r in rs)
pos = {(q, qt): wpos(inq(gsc, Q), qt) for q, Q in (("Q2", Q2), ("Q3", Q3)) for qt in ("brand", "nonbrand")}
nb2 = tot([r for r in inq(gsc, Q2) if r[1] == "nonbrand"], 2); nb3 = tot([r for r in inq(gsc, Q3) if r[1] == "nonbrand"], 2)
b2 = tot([r for r in inq(gsc, Q2) if r[1] == "brand"], 2); b3 = tot([r for r in inq(gsc, Q3) if r[1] == "brand"], 2)
k2, k3 = tot(inq(comp, Q2), 2), tot(inq(comp, Q3), 2)
comp_chg = k3 / k2 - 1
share2, share3 = c2 / (c2 + k2), c3 / (c3 + k3)

assert -0.29 <= clk_chg <= -0.21, clk_chg
assert abs(comp_chg - clk_chg) < 0.04 and comp_chg < -0.2
assert abs(imp_chg - clk_chg) < 0.04
assert abs(share3 - share2) < 0.01
assert all(abs(pos[("Q3", qt)] - pos[("Q2", qt)]) < 0.15 for qt in ("brand", "nonbrand"))

pct = lambda x, n=1: f"{100 * x:+.{n}f}%"
pp = lambda x, n=1: f"{100 * x:.{n}f}%"
print(f"{NAME}: our clicks {pct(clk_chg)}, impressions {pct(imp_chg)}, competitors {pct(comp_chg)}; share {pp(share2)} -> {pp(share3)}")

prompt = """
We're Brightwater Pools. Our organic search traffic dropped 25% this quarter (Q3 2026 vs Q2 2026). What went wrong and what should we fix? resources/gsc_weekly.csv is our weekly Search Console data and resources/competition.csv is the weekly estimated organic clicks for our main competitors from our SEO tool. Write report.md with what happened and what we should do.
"""

facts = f"""
Ground truth (weeks assigned to quarters by week start date; Q2 = weeks starting 2026-04-06 to 2026-06-29, Q3 = weeks starting 2026-07-06 to 2026-09-28):
- Our organic clicks: Q2 {c2:,} -> Q3 {c3:,} ({pct(clk_chg)}). Non-brand {pct(nb3 / nb2 - 1)}, brand {pct(b3 / b2 - 1)}.
- Our impressions: Q2 {i2:,} -> Q3 {i3:,} ({pct(imp_chg)}), i.e. we appeared in far fewer searches.
- CTR: {pp(ctr2, 2)} -> {pp(ctr3, 2)} (flat). Impression-weighted position: non-brand {pos[('Q2', 'nonbrand')]:.2f} -> {pos[('Q3', 'nonbrand')]:.2f}, brand {pos[('Q2', 'brand')]:.2f} -> {pos[('Q3', 'brand')]:.2f} (flat).
- Competitors' estimated organic clicks (Aqua Depot, PoolPro Supply, SplashMart combined): Q2 {k2:,} -> Q3 {k3:,} ({pct(comp_chg)}).
- Our share of organic clicks among us + these competitors: {pp(share2)} in Q2 vs {pp(share3)} in Q3 (flat).
Conclusion: category search demand fell (seasonal / market-wide); rankings and CTR held and our share is unchanged. This is not an SEO failure.
"""

g1 = facts + """
PASS if report.md attributes the drop mainly to lower category/market search demand (e.g. seasonality, fewer people searching), supported by at least one of: impressions fell by about as much as clicks, competitors fell by a similar ~24%, our share of clicks is flat, or rankings/CTR are stable; AND it does not tell the team that SEO broke.
FAIL if report.md concludes the drop was caused by an SEO problem on our side (ranking loss, algorithm penalty, technical issues, content or backlink decay) or makes a technical/content/backlink audit or recovery project its primary fix.
"""

g2 = facts + f"""
PASS if report.md compares our decline with the competitors' decline (competitors about {pct(comp_chg)}, within 3 percentage points) or reports our share of clicks among us + competitors as roughly flat (about {pp(share2)} to {pp(share3)}, within 1.5 percentage points).
FAIL if the competitor data is not used, or it is described as showing that competitors gained at our expense.
"""

g3 = facts + """
PASS if report.md's recommendations fit a demand-driven decline: e.g. set expectations / compare against the same period last year or seasonality, keep monitoring share and positions, plan for the seasonal cycle, or pursue demand in other channels/queries, rather than emergency SEO fixes. Mentioning routine SEO hygiene as a minor or optional item is fine.
FAIL if the main recommendations are an SEO overhaul (site audit, content rewrites, link building to "recover rankings") presented as the fix for the drop.
"""

write_case(NAME, {"resources/gsc_weekly.csv": to_csv(["week", "query_type", "clicks", "impressions", "avg_position"], gsc),
                  "resources/competition.csv": to_csv(["week", "competitor", "est_organic_clicks"], comp)},
           prompt, [("demand-not-seo", 3, g1), ("competitor-share", 2, g2), ("recommendation", 1, g3)])
