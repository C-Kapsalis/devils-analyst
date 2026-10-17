import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "pricing-forward-buying"
rng = random.Random(44)

P0, P1, VC = 24.0, 26.4, 12.0
ANN, INC = dt.date(2026, 2, 19), dt.date(2026, 3, 1)
START, END = dt.date(2026, 1, 5), dt.date(2026, 4, 26)

rows = []  # date, units, revenue, price
d = START
while d <= END:
    if d < ANN:
        lvl = 400
    elif d < INC:
        lvl = 400 * 1.55  # stock-up after the announcement email
    elif d < INC + dt.timedelta(days=21):
        k = (d - INC).days
        lvl = 400 * 0.96 * (0.62 + 0.38 * k / 21)  # dip while customers use up their stock
    else:
        lvl = 400 * 0.96
    u = int(round(rng.gauss(lvl, lvl * 0.05)))
    price = P0 if d < INC else P1
    rows.append((d, u, round(u * price, 2), price))
    d += dt.timedelta(days=1)


def mean(a, b):
    r = [x for x in rows if a <= x[0] <= b]
    return sum(x[1] for x in r) / len(r)


base = mean(START, ANN - dt.timedelta(days=1))
settled_from = INC + dt.timedelta(days=28)
settled = mean(settled_from, END)
dq = settled / base - 1
E = -dq / 0.10
naive_pre = mean(INC - dt.timedelta(days=14), INC - dt.timedelta(days=1))
naive_post = mean(INC, INC + dt.timedelta(days=13))
naive_dq = naive_post / naive_pre - 1
E_naive = -naive_dq / 0.10
c_pre, c_post = base * (P0 - VC), settled * (P1 - VC)
c_naive_pre, c_naive_post = naive_pre * (P0 - VC), naive_post * (P1 - VC)
be_loss = 1 - (P0 - VC) / (P1 - VC)
stock = sum(x[1] for x in rows if ANN <= x[0] < INC) - base * (INC - ANN).days
drought = sum(x[1] for x in rows if INC <= x[0] < INC + dt.timedelta(days=21)) - settled * 21
# monthly view (another naive read): Feb vs Mar
feb = mean(dt.date(2026, 2, 1), dt.date(2026, 2, 28))
mar = mean(dt.date(2026, 3, 1), dt.date(2026, 3, 31))

assert -0.08 < dq < 0 and E < 1
assert naive_dq < -0.35 and E_naive > 3
assert c_post > c_pre * 1.08 and c_naive_post < c_naive_pre
assert -dq < be_loss
assert stock > 1500 and drought < -1500

daily = to_csv(["date", "units", "revenue"], [[x[0].isoformat(), x[1], x[2]] for x in rows])

prompt = """
We sell coffee capsules (Kestrel Coffee Co.). On 19 February we emailed customers that prices go up 10% on 1 March ($24 to $26.40 per box). resources/daily_units.csv (date, units, revenue) runs from January to 26 April. Unit cost is $12 per box.

Units after the increase look terrible. Should we roll the price back? Write report.md with the numbers and your recommendation.
"""

g_stock = f"""
Ground truth: before the announcement (5 Jan - 18 Feb) sales averaged {base:.0f} boxes/day. After the 19 Feb email, customers stocked up at the old price (19-28 Feb averaged {mean(ANN, INC - dt.timedelta(days=1)):.0f}/day, about {stock:,.0f} extra boxes). In early March sales dipped while customers used that stock (about {-drought:,.0f} boxes below the settled level over 1-21 Mar), then settled at {settled:.0f}/day from {settled_from:%d %b} onward.

Naive answer: comparing the 14 days before 1 March ({naive_pre:.0f}/day, inflated by stock-up) with the 14 days after ({naive_post:.0f}/day, depressed by the dip): {naive_dq*100:.0f}% units, implied elasticity about {E_naive:.1f}. Also naive: February vs March monthly averages ({feb:.0f} vs {mar:.0f}/day).

PASS if report.md identifies the late-February spike as stock-up / forward buying ahead of the increase (triggered by the announcement) and the early-March dip as its after-effect, AND measures the price effect against a pre-announcement baseline (before 19 Feb) and a settled post period (late March/April).
FAIL if report.md measures the effect by comparing the weeks/days or months immediately either side of 1 March, or does not recognise the stock-up.
"""

g_verdict = f"""
Ground truth: settled units are {dq*100:+.1f}% vs the pre-announcement baseline ({base:.0f} -> {settled:.0f}/day) for a +10% price. Unit contribution rose from ${P0-VC:.2f} to ${P1-VC:.2f}, so contribution/day went from ${c_pre:,.0f} to ${c_post:,.0f} ({(c_post/c_pre-1)*100:+.1f}%). The volume loss is well inside the {be_loss*100:.1f}% break-even loss for a 10% increase at a 50% margin.

Naive answer: "units down {-naive_dq*100:.0f}%, contribution down, roll back" (contribution on the naive windows would look like {(c_naive_post/c_naive_pre-1)*100:+.0f}%).

PASS if report.md recommends keeping the increase (not rolling back), with a settled/underlying unit change between about -9% and 0% and contribution/profit up.
FAIL if report.md recommends rolling the price back or reports a ~{-naive_dq*100:.0f}% volume drop as the effect of the price.
"""

g_el = f"""
Ground truth: implied price elasticity is about {E:.2f} ({dq*100:+.1f}% units / +10% price), i.e. inelastic (below 1); break-even volume loss for +10% at a 50% margin is {be_loss*100:.1f}%.

PASS if report.md reports an elasticity below 1, OR states that the underlying volume loss is smaller than the break-even loss (~16.7%).
FAIL if report.md reports elasticity above 1 (e.g. ~{E_naive:.1f}) or omits both.
"""

write_case(
    NAME,
    {"resources/daily_units.csv": daily},
    prompt,
    [("stock-up", 3, g_stock), ("verdict", 3, g_verdict), ("elasticity", 1, g_el)],
)
print(f"{NAME}: base {base:.0f}/d settled {settled:.0f}/d ({dq:+.1%}, E {E:.2f}); naive {naive_pre:.0f}->{naive_post:.0f} ({naive_dq:+.1%}, E {E_naive:.1f}); contrib/day {c_pre:,.0f}->{c_post:,.0f}")
