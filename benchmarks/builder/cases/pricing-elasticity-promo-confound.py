import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "pricing-elasticity-promo-confound"
rng = random.Random(11)

E_TRUE, PROMO_LIFT, VC, P_NOW = 2.0, 0.60, 22.0, 40.0
REGS = [38, 40, 42, 40, 38, 42, 41, 40]  # regular price per 13-week block; ends at $40
START = dt.date(2024, 10, 7)


def ols(X, y):
    k = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) for j in range(k)] + [sum(r[i] * yy for r, yy in zip(X, y))] for i in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [v / piv for v in A[c]]
        for r in range(k):
            if r != c:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [A[i][k] for i in range(k)]


rows = []  # week_start, units, price, promo, regular
for w in range(104):
    reg = REGS[w // 13]
    promo = 1 if rng.random() < 0.22 else 0
    disc = rng.choice([0.20, 0.25]) if promo else 0.0
    price = round(reg * (1 - disc), 2)
    lnq = math.log(9.0e5) - E_TRUE * math.log(price) + PROMO_LIFT * promo + rng.gauss(0, 0.06)
    rows.append((START + dt.timedelta(weeks=w), int(round(math.exp(lnq))), price, promo, reg))


y = [math.log(r[1]) for r in rows]
E_naive = -ols([[1, math.log(r[2])] for r in rows], y)[1]
E_ctrl = -ols([[1, math.log(r[2]), r[3]] for r in rows], y)[1]
reg_only = [r for r in rows if not r[3]]
E_reg = -ols([[1, math.log(r[2])] for r in reg_only], [math.log(r[1]) for r in reg_only])[1]
n_promo = sum(r[3] for r in rows)

inv_pv = P_NOW / (P_NOW - VC)
pstar_ctrl = VC * E_ctrl / (E_ctrl - 1)
pstar_naive = VC * E_naive / (E_naive - 1)


def contrib_change(e, p_new):
    return (p_new - VC) * (p_new / P_NOW) ** (-e) / (P_NOW - VC) - 1


d42_ctrl, d42_naive = contrib_change(E_ctrl, 42), contrib_change(E_naive, 42)
d44_ctrl = contrib_change(E_ctrl, 44)
dcut_naive = contrib_change(E_naive, pstar_naive)
dcut_ctrl = contrib_change(E_ctrl, pstar_naive)

assert 1.75 < E_ctrl < 2.25 and 1.6 < E_reg < 2.4
assert E_naive > 3.5, E_naive
assert E_ctrl < inv_pv < E_naive  # decision flips
assert pstar_ctrl > 42 and pstar_naive < 35
assert d42_ctrl > 0 and d42_naive < -0.05
assert dcut_ctrl < -0.1

sales = to_csv(["week_start", "units", "avg_selling_price"], [[r[0].isoformat(), r[1], r[2]] for r in rows])
cal = []
for r in rows:
    if r[3]:
        pct = round(100 * (1 - r[2] / r[4]))
        cal.append([r[0].isoformat(), f"Ridge sale {pct}% off - email + homepage banner", "promo"])
calendar = to_csv(["week_start", "campaign", "type"], cal)

prompt = """
resources/ has two years of weekly sales for our best-seller, the Ridge daypack from Harbor Outdoor (weekly_sales.csv: week_start, units, avg_selling_price) and our marketing calendar (campaign_calendar.csv: week_start, campaign, type). Unit cost landed in our warehouse plus fulfilment is $22.

What is the price elasticity of the Ridge, and should we change the regular price (now $40)? Write report.md with the elasticity and your pricing recommendation.
"""

g_el = f"""
Ground truth: regressing ln(units) on ln(avg_selling_price) WITH a promo-week indicator (promo weeks come from campaign_calendar.csv, type = promo; {n_promo} of 104 weeks) gives an own-price elasticity of about {E_ctrl:.2f}. Using only non-promo weeks gives {E_reg:.2f}. Promo weeks combine a 20-25% lower price with an email and homepage banner, so price and promotion attention move together.

Naive answer: regressing units on price alone (ignoring the calendar) gives elasticity about {E_naive:.2f} ("highly elastic"). Any price-only arc/point estimate that mixes promo and non-promo weeks lands well above 3.

PASS if report.md separates or controls for promo weeks (dummy variable, excluding promo weeks, or comparing only regular-price weeks across the $38-$42 price levels) AND reports an elasticity magnitude between 1.5 and 2.5 as the regular-price elasticity.
FAIL if report.md reports an elasticity above 3 (e.g. ~{E_naive:.1f}) as the price elasticity, or never uses the campaign calendar / promo weeks in the estimate.
"""

g_dec = f"""
Ground truth: at $40 with $22 unit cost the contribution margin is 45%, so the profit-maximising elasticity is 1/0.45 = {inv_pv:.2f}. The controlled elasticity (~{E_ctrl:.2f}) is below {inv_pv:.2f}, so the Ridge is somewhat UNDERPRICED: the constant-elasticity optimum is about ${pstar_ctrl:.0f}, outside the observed $38-$42 regular-price range, so the sensible action is a tested step up (e.g. $42-$44). Moving to $42 changes weekly contribution by about {d42_ctrl*100:+.1f}% under the controlled elasticity ($44: {d44_ctrl*100:+.1f}%).

Naive answer: with elasticity ~{E_naive:.1f} the product looks overpriced and the "optimal" price is about ${pstar_naive:.2f} (a cut); a $42 price would look like {d42_naive*100:+.1f}% contribution. Under the true elasticity, cutting to ${pstar_naive:.0f} would actually change contribution by about {dcut_ctrl*100:+.0f}%.

PASS if report.md recommends holding or raising the regular price (a raise or a tested step up is best; holding with a stated plan to test an increase is acceptable).
FAIL if report.md recommends cutting the regular price below $40.
"""

g_method = f"""
PASS if report.md explains why a simple price-vs-units fit overstates elasticity here: promo weeks combine the lower price with extra marketing attention (email, homepage banner), so part of the promo-week sales jump is the promotion, not the price. Any clear statement of this confound counts.
FAIL if report.md does not mention the promotion/marketing confound at all.
"""

write_case(
    NAME,
    {"resources/weekly_sales.csv": sales, "resources/campaign_calendar.csv": calendar},
    prompt,
    [("elasticity", 3, g_el), ("decision", 3, g_dec), ("method", 1, g_method)],
)
print(f"{NAME}: E naive {E_naive:.2f} (P* {pstar_naive:.2f}), controlled {E_ctrl:.2f} (P* {pstar_ctrl:.1f}), non-promo {E_reg:.2f}; 1/PV {inv_pv:.2f}; $42 contrib {d42_ctrl:+.1%} vs naive {d42_naive:+.1%}")
