import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "clv-churn-denominator"
rng = random.Random(6631)

EXPORT = dt.date(2026, 10, 1)
HAZARD = 0.068  # monthly cancel probability
LAMBDA = -math.log(1 - HAZARD) / 30.44
MARGIN = 0.70
D_MONTH = 1.10 ** (1 / 12) - 1
PRICES = [(29.0, 0.30), (49.0, 0.50), (79.0, 0.20)]


def month_start(y, m):
    return dt.date(y, m, 1)


def add_month(d):
    return dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)


subs = []
cid = 10000
m = month_start(2024, 1)
k = 0
while m < EXPORT:
    nxt = add_month(m)
    n = int(round(rng.gauss(36 + 0.35 * k, 3)))
    for _ in range(n):
        start = m + dt.timedelta(days=rng.randrange((nxt - m).days))
        life = rng.expovariate(LAMBDA)
        cancel = start + dt.timedelta(days=max(1, int(life)))
        x = rng.random()
        price = PRICES[0][0] if x < PRICES[0][1] else PRICES[1][0] if x < PRICES[0][1] + PRICES[1][1] else PRICES[2][0]
        cid += 1
        subs.append([f"C{cid}", start, cancel if cancel < EXPORT else None, price])
    m, k = nxt, k + 1
subs.sort(key=lambda r: r[1])

# --- ground truth: monthly churn = cancels during month among customers active at month start
months = []
m = month_start(2025, 10)
while m < EXPORT:
    months.append(m)
    m = add_month(m)
act_tot = canc_tot = 0
for ms in months:
    me = add_month(ms)
    active = [s for s in subs if s[1] < ms and (s[2] is None or s[2] >= ms)]
    canc = [s for s in active if s[2] is not None and s[2] < me]
    act_tot += len(active)
    canc_tot += len(canc)
churn = canc_tot / act_tot

active_now = [s for s in subs if s[2] is None]
arpu = sum(s[3] for s in active_now) / len(active_now)
gm = arpu * MARGIN
clv = gm / (churn + D_MONTH)
clv_undisc = gm / churn
clv_rev_true = arpu / churn

# --- naive
last = month_start(2026, 9)
canc_last = sum(1 for s in subs if s[2] is not None and last <= s[2] < EXPORT)
naive_churn = canc_last / len(subs)  # last month's cancels / all customers ever
naive_ltv = arpu / naive_churn
n_months_hist = len({(s[1].year, s[1].month) for s in subs})
total_canc = sum(1 for s in subs if s[2] is not None)
naive_churn2 = total_canc / n_months_hist / len(subs)
naive_ltv_margin = gm / naive_churn

CAC_NEW = 450.0
payback = CAC_NEW / gm
surv_payback = (1 - churn) ** payback
ratio = clv / CAC_NEW

# --- CAC by channel for Jul-Sep 2026, consistent with subscription starts
CH = [("meta", 0.42, 318.0), ("google_search", 0.36, 262.0), ("affiliate", 0.22, 141.0)]
cac_rows = []
cur_meta = []
for mo in (7, 8, 9):
    ms = month_start(2026, mo)
    n = sum(1 for s in subs if s[1].year == 2026 and s[1].month == mo)
    left = n
    for j, (ch, share, cac) in enumerate(CH):
        nc = left if j == len(CH) - 1 else int(round(n * share))
        left -= nc
        spend = round(nc * cac * rng.uniform(0.95, 1.05), 2)
        cac_rows.append([ms.isoformat()[:7], ch, spend, nc])
        if ch == "meta":
            cur_meta.append((spend, nc))
meta_cac = sum(a for a, _ in cur_meta) / sum(b for _, b in cur_meta)

assert 0.055 < churn < 0.08 and 0.02 < naive_churn < 0.04
assert naive_ltv > 2.5 * clv
assert 400 < clv < 560 and ratio < 1.25
assert naive_ltv / CAC_NEW > 3

rows = [[s[0], s[1].isoformat(), s[2].isoformat() if s[2] else None, s[3]] for s in subs]

prompt = f"""
The resources/ directory has our Lumen Streaming subscription export, subscriptions.csv (customer_id, start_date, cancel_date, monthly_price; exported 1 October 2026, blank cancel_date = still active), and our acquisition spend, cac_by_channel.csv (month, channel, spend, new_customers). Our gross margin is 70% and finance uses a 10% annual discount rate.

What's our customer lifetime value, and can we afford to let Meta CAC rise to $450? Write report.md with the CLV number, how you got it, and a clear yes/no on the $450 Meta CAC.
"""

g_churn = f"""
Ground truth monthly churn = cancellations during a month / customers active at the start of that month. Over Oct 2025-Sep 2026 this is {canc_tot:,} / {act_tot:,} = {churn*100:.1f}% per month (any figure from 5.5% to 8.0% computed this way is fine; a single recent month in that range is fine too).

Naive (wrong) churn figures, which divide by every customer who ever subscribed: {canc_last} September cancellations / {len(subs):,} customers ever = {naive_churn*100:.1f}% per month; or average monthly cancellations / all customers ever = {naive_churn2*100:.1f}%.

PASS if report.md uses a monthly churn rate between 5.5% and 8.0% for its CLV.
FAIL if report.md uses a churn rate around {naive_churn*100:.1f}% or {naive_churn2*100:.1f}% (or anything below 4.5%), or does not state a churn rate.
"""

g_clv = f"""
Ground truth CLV: average monthly price of active subscribers ${arpu:.2f} x 70% gross margin = ${gm:.2f} gross profit per month; with {churn*100:.1f}% monthly churn and a 10%/yr discount rate ({D_MONTH*100:.2f}%/month), CLV = {gm:.2f} / ({churn:.4f} + {D_MONTH:.4f}) = ${clv:,.0f}. Undiscounted margin CLV would be ${clv_undisc:,.0f}.

Wrong answers: revenue-based LTV with the naive churn, ${arpu:.0f} / {naive_churn:.3f} = ${naive_ltv:,.0f}; margin-based with naive churn ${naive_ltv_margin:,.0f}; revenue-based (no margin) with correct churn ${clv_rev_true:,.0f}.

PASS if report.md's headline CLV is margin-based and between ${clv*0.85:,.0f} and ${clv_undisc*1.08:,.0f}.
FAIL if the headline CLV is revenue-based (no 70% margin applied) or above ${clv_undisc*1.08:,.0f} (e.g. ${naive_ltv:,.0f}, ${naive_ltv_margin:,.0f} or ${clv_rev_true:,.0f}).
"""

g_dec = f"""
Ground truth: CLV is about ${clv:,.0f} (gross-margin, discounted), so a $450 Meta CAC gives CLV:CAC of about {ratio:.2f}:1 and a payback of {payback:.1f} months of gross profit, by which time only about {surv_payback*100:.0f}% of customers are still subscribed. That leaves almost no margin for overheads, so the answer is no (or "only at break-even / not profitably"). Current Meta CAC (Jul-Sep 2026) is about ${meta_cac:,.0f}.

Naive answer: "yes, LTV ${naive_ltv:,.0f} is {naive_ltv/CAC_NEW:.1f}x a $450 CAC."

PASS if report.md says no / not affordable / roughly break-even at best for a $450 Meta CAC, and the reasoning is consistent with a CLV near ${clv:,.0f}.
FAIL if report.md says yes, $450 is affordable or comfortably profitable.
"""

write_case(
    NAME,
    {
        "resources/subscriptions.csv": to_csv(["customer_id", "start_date", "cancel_date", "monthly_price"], rows),
        "resources/cac_by_channel.csv": to_csv(["month", "channel", "spend", "new_customers"], cac_rows),
    },
    prompt,
    [("churn-denominator", 3, g_churn), ("clv-value", 2, g_clv), ("decision", 2, g_dec)],
)
print(f"{NAME}: churn {churn*100:.1f}% (naive {naive_churn*100:.1f}%), CLV ${clv:,.0f} (naive ${naive_ltv:,.0f}), CLV/450={ratio:.2f}, meta CAC ${meta_cac:.0f}, rows {len(subs)}")
