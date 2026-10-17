import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "trial-cac-payback"
rng = random.Random(7741)
MARGIN = 0.70
SEP1, OCT1 = dt.date(2026, 9, 1), dt.date(2026, 10, 1)

# channel: (spend, trials, trial->paid rate, share on premium plan)
CH = {
    "meta": (19800.0, 380, 0.31, 0.35),
    "google_search": (15600.0, 240, 0.44, 0.50),
    "tiktok": (8400.0, 340, 0.115, 0.30),
}
PLANS = (14.99, 24.99)

trials = []
uid = 40000
for ch, (spend, n, conv, prem) in CH.items():
    for _ in range(n):
        uid += rng.randint(1, 9)
        start = SEP1 + dt.timedelta(days=rng.randrange(30))
        price = PLANS[1] if rng.random() < prem else PLANS[0]
        converted = None
        if rng.random() < conv:
            day = 14 if rng.random() < 0.82 else rng.randint(2, 13)
            converted = start + dt.timedelta(days=day)
        trials.append([f"u{uid}", start, ch, converted, price])
trials.sort(key=lambda r: (r[1], r[0]))

spend_rows = [[ch, v[0]] for ch, v in CH.items()]

res = {}
for ch, (spend, *_rest) in CH.items():
    t = [r for r in trials if r[2] == ch]
    paid = [r for r in t if r[3] is not None]
    paid_sep = [r for r in paid if r[3] < OCT1]
    arpu = sum(r[4] for r in paid) / len(paid)
    cac = spend / len(paid)
    res[ch] = dict(
        trials=len(t), paid=len(paid), paid_sep=len(paid_sep), conv=len(paid) / len(t),
        cpt=spend / len(t), cac=cac, arpu=arpu, payback=cac / (arpu * MARGIN),
        cac_sep=spend / len(paid_sep), payback_sep=spend / len(paid_sep) / (arpu * MARGIN),
    )

order_payback = sorted(res, key=lambda c: res[c]["payback"])
order_cpt = sorted(res, key=lambda c: res[c]["cpt"])
assert order_cpt[0] == "tiktok" and order_payback[-1] == "tiktok" and order_payback[0] == "google_search"
assert res["tiktok"]["cac"] > 1.3 * max(res["meta"]["cac"], res["google_search"]["cac"])
assert all(res[c]["cac_sep"] > 1.5 * res[c]["cac"] for c in res)
n_oct = sum(1 for r in trials if r[3] is not None and r[3] >= OCT1)
assert n_oct > 0.35 * sum(1 for r in trials if r[3] is not None)

rows = [[r[0], r[1].isoformat(), r[2], r[3].isoformat() if r[3] else None, r[4]] for r in trials]

def line(c, keys):
    r = res[c]
    return f"{c}: " + ", ".join(k.format(**r) for k in keys)

truth = "\n".join(
    "- " + line(c, ["spend ${:,.0f}".format(CH[c][0]), "{paid} paid from {trials} trials ({conv:.1%})", "CAC ${cac:,.2f}",
                     "avg price ${arpu:.2f}", "payback {payback:.1f} months"])
    for c in order_payback
)
naive_cpt = ", ".join(f"{c} ${res[c]['cpt']:.2f}" for c in order_cpt)
naive_sep = ", ".join(f"{c} ${res[c]['cac_sep']:,.2f} ({res[c]['paid_sep']} paid)" for c in order_payback)

prompt = """
The resources/ directory has our September 2026 paid-media spend for Lumen Streaming, spend_sep.csv (channel, spend), and our trial export, trials.csv (user_id, trial_start, channel, converted_at, monthly_price), pulled on 20 October 2026. converted_at is when the free trial turned into a paid subscription (blank = did not convert). Gross margin is 70%.

What's our CAC by channel for September, and which channel pays back fastest? Write report.md with CAC and payback by channel and where you'd shift budget.
"""

g_cac = f"""
Ground truth: CAC = September spend / paid subscribers from trials started in September (all conversions count, including those whose converted_at falls in October, since the 14-day trials of late-September starters convert in October). {n_oct} of the conversions are dated in October.
{truth}

Wrong answers:
- Cost per trial instead of CAC: {naive_cpt} (makes TikTok look cheapest).
- Counting only conversions dated in September: {naive_sep}.

PASS if report.md's CAC for each of the three channels is within 5% of the ground truth (meta ${res['meta']['cac']:,.2f}, google_search ${res['google_search']['cac']:,.2f}, tiktok ${res['tiktok']['cac']:,.2f}).
FAIL if any channel's CAC is missing or outside 5%, or report.md reports cost per trial or the September-dated-only figures as CAC.
"""

rev_pb = ", ".join(f"{c} {res[c]['cac'] / res[c]['arpu']:.1f} months" for c in order_payback)

g_pay = f"""
Ground truth payback (months) = CAC / (average monthly price of that channel's paid subscribers x 70% margin):
{truth}
Fastest payback: {order_payback[0]}; slowest: tiktok. (Using price without margin gives shorter paybacks, {rev_pb}; that ignores the 70% margin but keeps the same ranking.)

Naive answer: TikTok is the best channel because it has the lowest cost per trial (${res['tiktok']['cpt']:.2f} vs {', '.join(f"{c} ${res[c]['cpt']:.2f}" for c in order_cpt[1:])}), despite only {res['tiktok']['conv']:.0%} of its trials converting.

PASS if report.md identifies {order_payback[0]} as the fastest payback channel and TikTok as the slowest/worst, with payback figures within 15% of the ground truth (margin-based), or within 15% of the revenue-based paybacks ({rev_pb}) if the report clearly labels them as revenue-based.
FAIL if report.md calls TikTok the best or most efficient channel, or ranks channels by cost per trial.
"""

g_budget = f"""
Correct direction: shift budget away from TikTok (highest CAC ${res['tiktok']['cac']:,.0f}, slowest payback {res['tiktok']['payback']:.1f} months, {res['tiktok']['conv']:.0%} trial-to-paid) toward {order_payback[0]} (and/or meta). Caveats about saturation or testing the shift are fine.

PASS if report.md recommends moving budget from TikTok toward {order_payback[0]} or meta (or at least not increasing TikTok).
FAIL if report.md recommends increasing TikTok budget because trials are cheap.
"""

write_case(
    NAME,
    {
        "resources/spend_sep.csv": to_csv(["channel", "spend"], spend_rows),
        "resources/trials.csv": to_csv(["user_id", "trial_start", "channel", "converted_at", "monthly_price"], rows),
    },
    prompt,
    [("cac-cohort", 3, g_cac), ("payback-ranking", 2, g_pay), ("budget", 1, g_budget)],
)
print(f"{NAME}: " + "; ".join(f"{c} CAC ${res[c]['cac']:.0f} pb {res[c]['payback']:.1f}m cpt ${res[c]['cpt']:.0f} sepCAC ${res[c]['cac_sep']:.0f}" for c in order_payback))
