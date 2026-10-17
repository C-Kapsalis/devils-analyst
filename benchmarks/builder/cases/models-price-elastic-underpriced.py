"""A +10% price test loses 12% of units: demand is elastic (E ~1.2) and
revenue falls, so the naive call is 'keep $40'. But with a $28 landed cost,
contribution rises ~17% at $44 (1/PV = 3.3 > E: still underpriced). The
constant-elasticity optimum ($150+) is an extrapolation, not a launch price."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "models-price-elastic-underpriced"
rng = random.Random(4021)
COST = 28.0
ARMS = [("A", 40.0, 0.0500), ("B", 44.0, 0.0440)]
start = dt.date(2026, 9, 7)
rows = []
for d in range(28):
    day = start + dt.timedelta(days=d)
    wk = 1.15 if day.weekday() >= 5 else 0.94
    base = int(714 * wk * rng.uniform(0.9, 1.1))
    for arm, price, cvr in ARMS:
        vis = base + rng.randint(-15, 15)
        orders = max(0, int(round(rng.gauss(vis * cvr, math.sqrt(vis * cvr * (1 - cvr))))))
        units = orders + sum(1 for _ in range(orders) if rng.random() < 0.03)
        rows.append([day.isoformat(), arm, price, vis, orders, units, round(units * price, 2)])
csv_text = to_csv(["date", "variant", "price", "visitors", "orders", "units", "revenue"], rows)

def tot(arm, i): return sum(r[i] for r in rows if r[1] == arm)
vA, vB = tot("A", 3), tot("B", 3)
oA, oB = tot("A", 4), tot("B", 4)
uA, uB = tot("A", 5), tot("B", 5)
revA, revB = tot("A", 6), tot("B", 6)
upvA, upvB = uA / vA, uB / vB                      # units per visitor (arms differ slightly in size)
d_units = upvB / upvA - 1
E = -d_units / 0.10
cA, cB = oA / vA, oB / vB
pp = (oA + oB) / (vA + vB)
z = (cA - cB) / math.sqrt(pp * (1 - pp) * (1 / vA + 1 / vB))
pval = math.erfc(abs(z) / math.sqrt(2))
rpvA, rpvB = revA / vA, revB / vB
conA, conB = (40 - COST) * uA, (44 - COST) * uB
cpvA, cpvB = conA / vA, conB / vB
lift = cpvB / cpvA - 1
inv_pv_A, inv_pv_B = 40 / (40 - COST), 44 / (44 - COST)
p_star = COST * E / (E - 1)
assert 1.05 < E < 1.5 and z > 2 and rpvB < rpvA, (E, z)
assert lift > 0.12 and inv_pv_B > E, lift
assert p_star > 100
print(f"{NAME}: E {E:.2f} z {z:.2f}; rev/visitor {rpvA:.3f}->{rpvB:.3f}; contribution/visitor {cpvA:.3f}->{cpvB:.3f} (+{100*lift:.0f}%); P* {p_star:.0f}")

prompt = """
We sell the Trailhead insulated bottle in our online shop. Last month we ran a price test: half of visitors saw $40 and half saw $44. The daily results are in resources/price_test_daily.csv. Our landed cost is $28 a unit. Demand looks pretty elastic to me. Should we keep $40 or move? Write report.md with your recommendation and the numbers behind it.
"""

f0 = lambda x: f"{x:,.0f}"
g_dec = f"""
Ground truth (totals over the 28-day test, landed cost $28/unit):
- $40 arm: {vA:,} visitors, {uA:,} units, revenue ${f0(revA)}, contribution (40-28) x {uA:,} = ${f0(conA)} = ${cpvA:.3f} per visitor
- $44 arm: {vB:,} visitors, {uB:,} units, revenue ${f0(revB)}, contribution (44-28) x {uB:,} = ${f0(conB)} = ${cpvB:.3f} per visitor
- Units per visitor fall {100*-d_units:.1f}% for a +10% price: price elasticity about -{E:.2f} (elastic), and revenue per visitor falls {100*(1-rpvB/rpvA):.1f}%. The drop is real (conversion z about {z:.1f}).
- BUT contribution (profit) per visitor RISES about {100*lift:.0f}% at $44. Equivalently, 1/(percentage margin) = 40/12 = {inv_pv_A:.2f} at $40 and 44/16 = {inv_pv_B:.2f} at $44, both above the elasticity {E:.2f}: the product is underpriced.
Naive wrong reasoning: "demand is elastic (|E| > 1) and revenue fell, so keep $40."

PASS if report.md recommends moving to $44 (or testing a higher price) on profit/contribution grounds, e.g. citing contribution up about {100*lift:.0f}% (anywhere 10% to 25% is fine) or 1/margin above the elasticity.
FAIL if it recommends keeping $40 because demand is elastic or revenue fell, or never compares profit/contribution between the two prices.
"""
g_ext = f"""
Ground truth: only $40 and $44 were tested. Plugging elasticity {E:.2f} into the constant-elasticity optimal-price formula P* = cost x E/(E-1) gives about ${p_star:.0f}, far outside the tested range; elasticity is not constant over that range, so this is not a usable price. A sound report moves to $44 and/or tests a further step (e.g. $48 or $50) before going higher.

PASS if report.md either recommends no price above $50, or frames any higher price as a next test step rather than a launch.
FAIL if it recommends a price of $60 or more (for example the ${p_star:.0f} formula result) as the new price to launch without testing it first.
"""
write_case(NAME, {"resources/price_test_daily.csv": csv_text}, prompt,
           [("decision", 3, g_dec), ("no-extrapolation", 2, g_ext)])
