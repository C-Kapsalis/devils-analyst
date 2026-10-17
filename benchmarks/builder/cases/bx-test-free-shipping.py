"""Free-shipping A/B test readout (Kestrel Tea Co., September 2026).

Planted subtle problems (5):
P1 (decision) B absorbs shipping: each B order earns less, so contribution per
   user falls even though conversion is up significantly vs zero.
P2 Guardrail: AOV falls in B, so merchandise revenue per user is flat (n.s.);
   the readout projects revenue from conversion lift x control AOV.
P3 Bundled change: B also added an express-checkout button; the lift cannot be
   credited to free shipping alone.
P4 Balance table: the two "imbalanced" variables are measured during the test
   (outcomes), the pre-period variables are balanced; the "discount" is wrong.
P5 Assignment unit = session: users in both arms (8.4%) saw both offers.
Decoys (2): unique users per arm below the sum of daily users (correct, users
return on several days); payment-outage day kept in both arms (randomised,
hit both arms equally)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-test-free-shipping"
rng = random.Random(51177)


def phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def binom(n, p):
    return max(0, round(rng.gauss(n * p, math.sqrt(n * p * (1 - p)))))


MARGIN = 0.48          # merchandise gross margin
SHIP_FEE = 5.95        # charged to control customers per order
SHIP_COST = 6.80       # what each order costs us to ship (both arms)

SEGS = {  # (device, visitor) -> (share of users, control CVR)
    ("mobile", "new"): (0.33, 0.018), ("mobile", "returning"): (0.25, 0.040),
    ("desktop", "new"): (0.20, 0.028), ("desktop", "returning"): (0.18, 0.055),
    ("tablet", "new"): (0.02, 0.020), ("tablet", "returning"): (0.02, 0.042),
}
N_ARM = {"A": 90212, "B": 89874}
LIFT = 1.10
AOV = {"A": 68.40, "B": 63.70}

seg_rows = []
tot = {v: {"users": 0, "conv": 0, "orders": 0, "rev": 0.0} for v in "AB"}
for v in "AB":
    left = N_ARM[v]
    keys = list(SEGS)
    for i, k in enumerate(keys):
        share, cr = SEGS[k]
        n = left if i == len(keys) - 1 else round(N_ARM[v] * share * rng.uniform(0.985, 1.015))
        left -= n
        c = binom(n, cr * (LIFT if v == "B" else 1))
        o = c + binom(c, 0.11)
        rev = round(o * AOV[v] * rng.uniform(0.97, 1.03), 2)
        seg_rows.append([v, k[0], k[1], n, c, o, rev])
        t = tot[v]; t["users"] += n; t["conv"] += c; t["orders"] += o; t["rev"] += rev

nA, nB = tot["A"]["users"], tot["B"]["users"]
cA, cB = tot["A"]["conv"], tot["B"]["conv"]
oA, oB = tot["A"]["orders"], tot["B"]["orders"]
rA, rB = tot["A"]["rev"], tot["B"]["rev"]
pA, pB = cA / nA, cB / nB
lift = pB / pA - 1
pp = (cA + cB) / (nA + nB)
z = (pB - pA) / math.sqrt(pp * (1 - pp) * (1 / nA + 1 / nB))
pval = 2 * (1 - phi(abs(z)))
aovA, aovB = rA / oA, rB / oB
rpuA, rpuB = rA / nA, rB / nB
rpu_change = rpuB / rpuA - 1
# revenue per user test (approximate: per-user revenue variance from order values ~ lognormal-ish; use orders as Poisson x AOV)
# conservative SE: var(rev per user) ~ E[orders] * AOV^2 * (1 + cv^2) / n, cv = 0.6
cv = 0.6
se_rpu = math.sqrt(oA / nA * aovA ** 2 * (1 + cv ** 2) / nA + oB / nB * aovB ** 2 * (1 + cv ** 2) / nB)
z_rpu = (rpuB - rpuA) / se_rpu
p_rpu = 2 * (1 - phi(abs(z_rpu)))
# contribution
contA_order = MARGIN * aovA + SHIP_FEE - SHIP_COST
contB_order = MARGIN * aovB - SHIP_COST
cpuA = oA / nA * contA_order
cpuB = oB / nB * contB_order
cpu_change = cpuB / cpuA - 1
orders_lift = (oB / nB) / (oA / nA) - 1
be_orders_lift = contA_order / contB_order - 1
monthly_users = 2 * (nA + nB) / 11 * 30 / 2  # all traffic per month (both arms -> sitewide)
monthly_users = (nA + nB) / 11 * 30
cont_month_delta = (cpuB - cpuA) * monthly_users
naive_rev_month = lift * pA * monthly_users * 1.11 * aovA  # readout-style projection (orders/user ~1.11)
naive_rev_month = (oB / nB - oA / nA) * monthly_users * aovA

# readout's arbitrary discount
disc_lift = lift - 0.025

# ---------- asserts ----------
assert pval < 0.01 and lift > 0.06, (pval, lift)
assert cpu_change < -0.15, cpu_change
assert abs(rpu_change) < 0.03 and p_rpu > 0.3, (rpu_change, p_rpu)
assert be_orders_lift > 0.25 and orders_lift < 0.12
assert aovB / aovA - 1 < -0.05

# ---------- daily file ----------
START = dt.date(2026, 9, 1)  # Tuesday
DAYS = 14
OUTAGE = 6  # 2026-09-07
wday = [1.04, 1.06, 1.05, 1.0, 0.92, 0.88, 1.05]  # Mon..Sun
weights = []
for d in range(DAYS):
    day = START + dt.timedelta(days=d)
    w = wday[day.weekday()] * (0.55 if d == OUTAGE else 1.0)
    weights.append(w)


def split(total, ws, integer=True):
    s = sum(ws)
    raw = [total * w / s * rng.uniform(0.96, 1.04) for w in ws]
    k = total / sum(raw)
    raw = [r * k for r in raw]
    if not integer:
        out = [round(r, 2) for r in raw]
        out[-1] = round(total - sum(out[:-1]), 2)
        return out
    out = [int(r) for r in raw]
    rem = total - sum(out)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - out[i], reverse=True)
    for i in order[:rem]:
        out[i] += 1
    return out


# conversion weights: outage hits orders more than users
conv_w = [w * (0.6 if d == OUTAGE else 1.0) for d, w in enumerate(weights)]
daily_rows = []
daily_users_sum = {}
outage_ratio = {}
for v in "AB":
    t = tot[v]
    users_d = split(round(t["users"] * 1.31), weights)  # users return on several days
    sess_d = [round(u * rng.uniform(1.38, 1.46)) for u in users_d]
    ord_d = split(t["orders"], conv_w)
    rev_d = split(round(t["rev"], 2), [o for o in ord_d], integer=False)
    daily_users_sum[v] = sum(users_d)
    for d in range(DAYS):
        day = START + dt.timedelta(days=d)
        fee = round(ord_d[d] * SHIP_FEE, 2) if v == "A" else 0.0
        cost = round(ord_d[d] * SHIP_COST, 2)
        daily_rows.append([day.isoformat(), v, users_d[d], sess_d[d], ord_d[d], rev_d[d], fee, cost])
    others = [ord_d[d] / users_d[d] for d in range(DAYS) if d != OUTAGE]
    outage_ratio[v] = (ord_d[OUTAGE] / users_d[OUTAGE]) / (sum(others) / len(others))
daily_rows.sort(key=lambda r: (r[0], r[1]))
assert daily_users_sum["A"] > nA * 1.2
assert abs(outage_ratio["A"] - outage_ratio["B"]) < 0.12

# ---------- balance file ----------
both_arms_share = 0.084
bal_rows = [
    ["orders_prior_365d", "365 days before first exposure", 0.612, 0.609, 0.74],
    ["sessions_prior_30d", "30 days before first exposure", 2.31, 2.33, 0.58],
    ["share_mobile", "at first exposure", 0.582, 0.579, 0.31],
    ["share_new_visitor", "at first exposure", 0.548, 0.551, 0.36],
    ["cart_adds_per_user", "during test", 0.214, 0.236, 0.0004],
    ["pages_per_session", "during test", 4.62, 4.71, 0.021],
]

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
usd = lambda x: f"${x:,.0f}"

readout = f"""# Free shipping test: readout

Kestrel Tea Co. growth team, draft for the leadership meeting

## Setup

| Item | Detail |
|---|---|
| Dates | 1 to 14 September 2026 (14 days) |
| Split | 50 / 50, tool: SplitWise, assignment unit: session_id |
| A (control) | Current site: $5.95 flat shipping on every order |
| B (variant) | Free shipping on all orders, "Free shipping, always" header bar, express checkout button (one-tap wallet pay) on the cart page |
| Primary metric | Conversion rate: converting users / users |

Note from the tool: 8.4% of users were assigned to both A and B on different sessions; they are counted in both arms.

## Result

| Arm | Users | Converting users | Conversion rate |
|---|---|---|---|
| A | {nA:,} | {cA:,} | {pc(pA, 2)} |
| B | {nB:,} | {cB:,} | {pc(pB, 2)} |

Lift: **+{pc(lift)}**, z = {z:.2f}, p = {pval:.4f}. Sample ratio check passed ({nA:,} vs {nB:,}, p = {2 * (1 - phi(abs((nA - nB) / math.sqrt((nA + nB) / 4) / 2))):.2f}).

Randomisation check: two of six variables are imbalanced (cart adds per user and pages per session, both higher in B, p < 0.05; see balance_check.csv). B seems to have drawn more engaged shoppers by chance, so to be conservative we discount the lift by 2.5 points to **+{pc(disc_lift)}**.

7 September: the payment provider had a 5-hour outage. Both arms were affected; we kept the day in.

## What it is worth

At the current order value ({usd(aovA)}) and our monthly traffic, the extra orders are worth about **{usd(naive_rev_month)} a month** in revenue.

## Recommendation

Roll out free shipping sitewide from 1 October. Free shipping is the single biggest conversion lever we have tested this year.
"""

files = {
    "resources/free_shipping_test_readout.md": readout,
    "resources/test_daily_by_arm.csv": to_csv(
        ["date", "variant", "users", "sessions", "orders", "merchandise_revenue", "shipping_charged", "shipping_cost"], daily_rows),
    "resources/test_segments_by_arm.csv": to_csv(
        ["variant", "device", "visitor_type", "users", "converting_users", "orders", "merchandise_revenue"], seg_rows),
    "resources/balance_check.csv": to_csv(["variable", "measured", "control_mean", "treatment_mean", "p_value"], bal_rows),
    "resources/unit_economics.md": (
        "# Unit economics (finance, FY2026)\n\n"
        f"- Merchandise gross margin: {int(MARGIN * 100)}% of merchandise revenue (product cost and packaging).\n"
        f"- Carrier cost per order shipped: ${SHIP_COST:.2f} (flat rate contract, all order sizes).\n"
        f"- Shipping fee charged to customers today: ${SHIP_FEE:.2f} per order.\n"
        "- Payment fees are already netted out of the margin figure.\n"
    ),
}

prompt = """
Our growth team ran a free shipping test in September and wrote it up in resources/free_shipping_test_readout.md; the exports behind it and finance's unit economics are also in resources/. Leadership decides on Thursday whether to switch to free shipping sitewide. What should we decide, and is there anything in the write-up I should fix before it goes to them? Put your answer in report.md.
"""

g_recall = f"""
The readout and its exports contain 5 planted problems. Ground truth (computed from the files):

1. Shipping cost not counted (decision-changing). In B the company pays the ${SHIP_COST:.2f} carrier cost and collects no ${SHIP_FEE:.2f} fee. Contribution per order: A ${contA_order:.2f} (= 48% x ${aovA:.2f} + 5.95 - 6.80), B ${contB_order:.2f} (= 48% x ${aovB:.2f} - 6.80). Contribution per user: A ${cpuA:.3f}, B ${cpuB:.3f}, a change of {pc(cpu_change)}. Orders per user would have to rise about {pc(be_orders_lift, 0)} to break even; they rose {pc(orders_lift)}. Counts as found if report.md says free shipping loses money / lowers contribution or profit per user once shipping cost (or the lost shipping fee) and margin are counted, with a number (a contribution or profit figure, a break-even lift of roughly 25-40%, or a money loss).
2. Order value fell. AOV A {usd(aovA)} vs B {usd(aovB)} ({pc(aovB / aovA - 1)}); merchandise revenue per user A ${rpuA:.3f} vs B ${rpuB:.3f} ({pc(rpu_change)}), not a meaningful gain. The readout's {usd(naive_rev_month)} a month projection uses control AOV. Counts as found if report.md says B's average order value is lower, or revenue per user is about flat, so the revenue projection is overstated.
3. More than one change. B also added an express checkout (one-tap wallet) button on the cart page and a header bar. Counts as found if report.md says the lift cannot be attributed to free shipping alone because the express checkout (or other changes) were bundled in.
4. Wrong balance variables. In balance_check.csv, cart_adds_per_user and pages_per_session are measured "during test": they are outcomes the treatment can change, not evidence of imbalance. The pre-exposure variables (orders_prior_365d, sessions_prior_30d, share_mobile, share_new_visitor) all have p > 0.3. Counts as found if report.md says those two variables are post-exposure/outcome measures so they do not show a randomisation problem (and the 2.5-point discount is unjustified).
5. Session-level assignment. Assignment unit is session_id and 8.4% of users were in both arms (saw both $5.95 and free shipping), counted in both. Counts as found if report.md flags session-level assignment or the users in both arms as contamination/a unit-of-analysis problem.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 5, each with its substance (a number, column or quoted setting). FAIL otherwise.
"""

g_decision = f"""
Correct main recommendation: do NOT roll out free shipping sitewide on this evidence. Although conversion rose {pc(lift)} (p = {pval:.4f}), contribution per user falls about {pc(-cpu_change, 0)} (A ${cpuA:.3f} vs B ${cpuB:.3f} per user, roughly {usd(-cont_month_delta)} less contribution a month at current traffic) because B absorbs ${SHIP_COST:.2f} shipping per order and baskets are smaller. Acceptable variants: keep the fee; test a free-shipping threshold (e.g. above the typical basket) or test express checkout on its own; rerun with user-level assignment. Any of these counts as long as the report does not recommend rolling out free shipping on all orders now.

Naive wrong answer: "Ship it: +{pc(lift)} conversion, p = {pval:.4f}, worth about {usd(naive_rev_month)} a month in revenue" (or the readout's discounted +{pc(disc_lift)}).

PASS if report.md's main recommendation is not to roll out sitewide free shipping as tested (hold, keep the fee, or test a threshold/redesigned test instead) and the reason given involves profit/contribution or shipping cost.
FAIL if it recommends rolling out free shipping on all orders (even "with monitoring"), or if it says hold only for reasons unrelated to profit (e.g. only "test too short").
"""

g_decoy = f"""
Two things look odd but are correct and must not be presented as problems:
- D1. Unique users per arm in the readout ({nA:,} and {nB:,}) are lower than the sum of the daily users column in test_daily_by_arm.csv ({daily_users_sum['A']:,} and {daily_users_sum['B']:,}). This is correct: the same user visits on several days, so daily users do not add up to unique users. The readout correctly uses unique users.
- D2. The 7 September payment outage day was kept in. Assignment is random and the outage hit both arms alike (orders per user that day were {pc(outage_ratio['A'], 0)} and {pc(outage_ratio['B'], 0)} of each arm's normal level), so keeping it does not bias the A vs B comparison.

PASS if report.md does not present D1 or D2 as an error that biases or invalidates the result. Neutral mentions, or saying they are fine, PASS. Flagging session-level assignment or users in both arms is a different (real) issue and does not count against this grader.
FAIL if it says the user counts are inconsistent/wrong because daily users sum to more than the readout's users, or says the outage day must be removed because it biases the result.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: lift {lift:.3f} p {pval:.4f}; contribution/user {cpuA:.3f}->{cpuB:.3f} ({cpu_change:.2%}); rev/user {rpu_change:.2%} p {p_rpu:.2f}; "
      f"AOV {aovA:.2f}->{aovB:.2f}; BE orders lift {be_orders_lift:.2%}")
