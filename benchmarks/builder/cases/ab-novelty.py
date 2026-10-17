import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "ab-novelty"
START = dt.date(2026, 9, 1)
DAYS = 28
BASE = {"new": (900, 0.030), "returning": (1500, 0.060)}  # users/day/arm, conv rate
RET_LIFT = [0.32, 0.13, 0.0, 0.0]  # by week, returning users in B
WDAY = [1.05, 1.08, 1.06, 1.02, 0.95, 0.88, 0.96]


def phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def ztest(c1, n1, c2, n2):
    p1, p2 = c1 / n1, c2 / n2
    p = (c1 + c2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se
    return p2 / p1 - 1, z, 2 * (1 - phi(abs(z)))


def binom(rng, n, p):
    return max(0, int(round(rng.gauss(n * p, math.sqrt(n * p * (1 - p))))))


def simulate(seed):
    rng = random.Random(seed)
    rows = []
    for d in range(DAYS):
        date = START + dt.timedelta(days=d)
        wk = d // 7
        for variant in ("A", "B"):
            for ut, (n0, p0) in BASE.items():
                n = int(round(rng.gauss(n0 * WDAY[date.weekday()], n0 * 0.04)))
                p = p0
                if variant == "B" and ut == "returning":
                    p = p0 * (1 + RET_LIFT[wk])
                rows.append([date.isoformat(), variant, ut, n, binom(rng, n, p)])
    return rows


def agg(rows, weeks=None, ut=None):
    out = {"A": [0, 0], "B": [0, 0]}
    for date, v, u, n, c in rows:
        wk = (dt.date.fromisoformat(date) - START).days // 7
        if weeks is not None and wk not in weeks:
            continue
        if ut is not None and u != ut:
            continue
        out[v][0] += n
        out[v][1] += c
    return ztest(out["A"][1], out["A"][0], out["B"][1], out["B"][0]), out


def check(rows):
    (pl, pz, pp), _ = agg(rows)
    (ll, lz, lp), _ = agg(rows, weeks={2, 3})
    (nl, nz, np_), _ = agg(rows, ut="new")
    w = [agg(rows, weeks={k})[0][0] for k in range(4)]
    rw = [agg(rows, weeks={k}, ut="returning")[0][0] for k in range(4)]
    ok = (pp < 0.001 and 0.08 <= pl <= 0.12 and lp > 0.4 and abs(ll) < 0.02
          and np_ > 0.3 and abs(nl) < 0.04 and w[0] > w[1] > max(w[2], w[3])
          and rw[0] > 0.22 and 0.06 < rw[1] < 0.18 and abs(rw[2]) < 0.05 and abs(rw[3]) < 0.05)
    return ok


seed = 101
while not check(simulate(seed)):
    seed += 1
rows = simulate(seed)

(pool_lift, pool_z, pool_p), pool = agg(rows)
(late_lift, late_z, late_p), late = agg(rows, weeks={2, 3})
(new_lift, _, new_p), _ = agg(rows, ut="new")
weekly = [agg(rows, weeks={k}) for k in range(4)]
weekly_ret = [agg(rows, weeks={k}, ut="returning")[0] for k in range(4)]
wk4 = weekly[3][0]

assert pool_p < 0.001 and late_p > 0.4
assert abs(pool_lift - late_lift) > 0.07

wl = ", ".join(f"week {k+1} {weekly[k][0][0]*100:+.1f}% (p={weekly[k][0][2]:.2g})" for k in range(4))
wr = ", ".join(f"week {k+1} {weekly_ret[k][0]*100:+.1f}%" for k in range(4))
pa = pool["A"][1] / pool["A"][0] * 100
pb = pool["B"][1] / pool["B"][0] * 100

prompt = """
We ran the new checkout page test for four weeks (1-28 September 2026): variant A is the current checkout, variant B is the new one, 50/50 split. The resources/ directory has the daily GA4 export, ab_daily.csv (date, variant, user_type, users, conversions).

Did B win, and should we roll it out? Write report.md with the result (the lift in conversion rate and whether it's real) and your recommendation.
"""

g_main = f"""
Ground truth (computed from ab_daily.csv; conversion rate = conversions / users):
- Pooled over all 4 weeks, B shows a {pool_lift*100:+.1f}% relative lift (A {pa:.2f}% vs B {pb:.2f}%, z={pool_z:.1f}, p={pool_p:.1g}). This pooled number is what a naive analysis reports as "B wins".
- But the lift decays week by week: {wl}.
- In weeks 3-4 combined (15-28 Sep) the lift is {late_lift*100:+.1f}% (z={late_z:.2f}, p={late_p:.2f}): no detectable effect. The early lift was a novelty effect among returning users ({wr}); new users show {new_lift*100:+.1f}% (p={new_p:.2f}) over the whole test.

Naive answer: "B wins with a ~{pool_lift*100:.0f}% significant lift; roll it out" without looking at the trend over time.

PASS if report.md shows that the lift shrinks over the test (week-by-week or early-vs-late split) AND states that in the later period (weeks 3-4, or week 4, or the last two weeks) the lift is about zero / not statistically significant (a reported late-period lift within {late_lift*100:+.1f}% +/- 3 percentage points of relative lift is fine), AND concludes the effect is not durable (novelty / wears off / no lasting lift).
FAIL if report.md presents the pooled ~{pool_lift*100:.0f}% lift as the effect of B without identifying the decay to ~0 in the later weeks, or if it never looks at the result over time.
"""

g_rec = f"""
The test's pooled lift ({pool_lift*100:+.1f}%) is driven by the first two weeks; weeks 3-4 show {late_lift*100:+.1f}% (p={late_p:.2f}). The correct recommendation is that B has not shown a durable win: do not roll it out on the expectation of a ~{pool_lift*100:.0f}% conversion gain. Acceptable variants: keep A / call it a no-difference result; roll out B only on other grounds (design, cost, maintenance) while expecting roughly zero conversion impact; extend or rerun the test (e.g. on new users only) before deciding.

PASS if the recommendation does not rely on, or forecast, a sustained ~{pool_lift*100:.0f}% conversion lift from B (any forecast of incremental conversions/revenue based on the pooled lift fails).
FAIL if report.md recommends rolling out B as a proven winner, or projects the pooled lift forward as the expected gain.
"""

g_seg = f"""
Over the whole test, new users show essentially no lift ({new_lift*100:+.1f}%, p={new_p:.2f}); the early lift is concentrated in returning users ({wr}).

PASS if report.md splits the result by user_type and notes that new users show no meaningful lift (or that the lift came from returning users and faded).
FAIL if report.md does not break the result down by user_type at all, or claims new users improved meaningfully.
"""

write_case(
    NAME,
    {"resources/ab_daily.csv": to_csv(["date", "variant", "user_type", "users", "conversions"], rows)},
    prompt,
    [("durable-effect", 3, g_main), ("recommendation", 2, g_rec), ("user-type-split", 1, g_seg)],
)
print(f"{NAME}: seed={seed} pooled {pool_lift*100:+.1f}% p={pool_p:.1g}; weeks3-4 {late_lift*100:+.1f}% p={late_p:.2f}; new {new_lift*100:+.1f}%")
