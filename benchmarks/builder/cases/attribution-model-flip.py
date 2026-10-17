"""Which channel 'contributes least' depends on the attribution model.
YouTube opens journeys and almost never closes them: ~0 on last click, large
on first touch / linear / Markov removal effect. GA4's data_driven column is
identical to last click (too few conversions for the model), so it is not
independent evidence. Paid Social is the low contributor under every
multi-touch view."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "attribution-model-flip"
rng = random.Random(8128)

N = 1000
MID = ["Organic Search", "Paid Search", "Email", "Direct", "Paid Social"]
MID_W = [0.25, 0.27, 0.25, 0.18, 0.05]
FIRST_NON_YT = ["Organic Search", "Paid Search", "Email", "Direct", "Paid Social"]
FIRST_W = [0.30, 0.28, 0.17, 0.13, 0.12]
CLOSE = ["Paid Search", "Email", "Direct", "Organic Search", "Paid Social"]
CLOSE_W = [0.34, 0.27, 0.19, 0.15, 0.05]

paths = []
for i in range(N):
    yt = rng.random() < 0.34
    tps = ["YouTube"] if yt else [rng.choices(FIRST_NON_YT, FIRST_W)[0]]
    for _ in range(rng.choice([0, 1, 1, 2, 2, 3])):
        tps.append(rng.choices(MID, MID_W)[0])
    ps = 0.07 if tps[0] == "Paid Social" else 0.0
    p_conv = (0.37 if yt else 0.14) + 0.03 * (len(tps) - 1) - ps
    conv = rng.random() < p_conv
    if conv and (tps[-1] not in CLOSE or len(tps) == 1 and yt):
        tps.append(rng.choices(CLOSE, CLOSE_W)[0])
    # collapse immediate repeats (GA4 path exploration shows distinct steps)
    dedup = [tps[0]] + [t for a, t in zip(tps, tps[1:]) if t != a]
    val = round(85 * math.exp(rng.gauss(0, 0.35)), 2) if conv else 0
    paths.append((f"j{i + 1:04d}", dedup, int(conv), val))

paths_csv = to_csv(["path_id", "touchpoints", "converted", "value"],
                   [[p, " > ".join(t), c, v] for p, t, c, v in paths])

CH = ["YouTube", "Paid Search", "Paid Social", "Email", "Organic Search", "Direct"]
PAID = ["YouTube", "Paid Search", "Paid Social", "Email"]
conv_paths = [p for p in paths if p[2] == 1]
tot_conv = len(conv_paths)

def credit(rule):
    c = {k: 0.0 for k in CH}
    for _, t, _, _ in conv_paths:
        for k, w in rule(t).items():
            c[k] += w
    return c

def lin(t):
    d = {}
    for k in t:
        d[k] = d.get(k, 0) + 1 / len(t)
    return d

last = credit(lambda t: {t[-1]: 1.0})
first = credit(lambda t: {t[0]: 1.0})
linear = credit(lin)

# Markov first-order removal effect
def p_conv(removed=None):
    trans = {}
    for _, t, c, _ in paths:
        seq = ["start"] + t + ["conv" if c else "null"]
        for a, b in zip(seq, seq[1:]):
            trans.setdefault(a, {}).setdefault(b, 0)
            trans[a][b] += 1
    v = {s: 0.0 for s in list(trans) + ["conv", "null"]}
    v["conv"] = 1.0
    for _ in range(300):
        for s, outs in trans.items():
            if s == removed:
                v[s] = 0.0
                continue
            tot = sum(outs.values())
            v[s] = sum(n * v[b] for b, n in outs.items()) / tot
    return v["start"]

base = p_conv()
rem = {k: 1 - p_conv(k) / base for k in CH}
rem_sum = sum(rem.values())
removal = {k: tot_conv * rem[k] / rem_sum for k in CH}

share = lambda d: {k: 100 * v / tot_conv for k, v in d.items()}
S = {"last click": share(last), "first touch": share(first), "linear": share(linear), "removal effect": share(removal)}
present = {k: 100 * sum(1 for _, t, _, _ in conv_paths if k in t) / tot_conv for k in CH}

least = {m: min(PAID, key=lambda k: s[k]) for m, s in S.items()}
assert least["last click"] == "YouTube" and S["last click"]["YouTube"] < 3, S["last click"]
for m in ("first touch", "linear", "removal effect"):
    assert least[m] == "Paid Social", (m, S[m])
    assert S[m]["YouTube"] > 2 * S[m]["Paid Social"], (m, S[m])
assert S["first touch"]["YouTube"] > 40 and S["linear"]["YouTube"] > 15 and rem["YouTube"] > 0.3, (S, rem)
second_last = sorted(PAID, key=lambda k: S["last click"][k])[1]
assert second_last == "Paid Social" and S["last click"]["Paid Social"] > S["last click"]["YouTube"] + 2

# GA4 attribution export: Sep = last click from these journeys; Jul/Aug similar. data_driven identical.
ga4_rows = []
for m in ["2026-07", "2026-08", "2026-09"]:
    for k in CH:
        if m == "2026-09":
            n = int(last[k])
            rev = round(sum(v for _, t, c, v in conv_paths if t[-1] == k), 2)
        else:
            n = max(0, int(round(last[k] * rng.uniform(0.88, 1.1))))
            rev = round(n * 85 * rng.uniform(0.95, 1.05), 2)
        ga4_rows.append([m, k, n, n, rev, rev])
ga4_csv = to_csv(["month", "default_channel_group", "last_click_conversions", "data_driven_conversions",
                  "last_click_revenue", "data_driven_revenue"], ga4_rows)
monthly = {m: sum(r[2] for r in ga4_rows if r[0] == m) for m in ["2026-07", "2026-08", "2026-09"]}
assert all(200 < v < 300 for v in monthly.values()), monthly

SPEND = {"YouTube": 9000, "Paid Search": 14500, "Paid Social": 11000, "Email": 1500}
spend_rows = []
for m in ["2026-07", "2026-08", "2026-09"]:
    for k, s in SPEND.items():
        spend_rows.append([m, k, round(s * rng.uniform(0.95, 1.05), 2)])
spend_csv = to_csv(["month", "channel", "spend"], spend_rows)
q3_spend = sum(r[2] for r in spend_rows)

fmt = lambda d: ", ".join(f"{k} {d[k]:.1f}%" for k in PAID)
model_lines = "\n".join(f"- {m}: {fmt(s)}" for m, s in S.items())

prompt = """
We need to cut 20% of our marketing budget. Which channel contributes least to sales? resources/ has customer journeys for September 2026 (paths.csv, one row per journey with the channels touched in order), our GA4 conversions by channel (ga4_attribution_export.csv), and monthly spend by paid channel (channel_spend.csv). Write report.md with your answer and what you'd cut.
"""

g_model = f"""
Share of September conversions credited to each paid channel ({tot_conv} converting journeys of {N}), computed from paths.csv:
{model_lines}
Markov removal effect (share of all conversions lost if the channel were removed from the journeys): {", ".join(f"{k} {100 * rem[k]:.0f}%" for k in PAID)}; the "removal effect" row above is these normalised to 100%.
YouTube appears in {present['YouTube']:.0f}% of converting journeys (almost always as the first touch) but is almost never the last touch.
So YouTube "contributes least" ONLY under last click; under first touch, linear and removal effect it is a substantial contributor (far above Paid Social), and Paid Social is the smallest paid contributor.

PASS if report.md shows that YouTube's contribution depends on the attribution model (e.g. reports YouTube's first-touch, linear, removal-effect, or path-presence credit as substantial, roughly matching any of the figures above within 5 percentage points; other reasonable multi-touch methods that give YouTube substantial credit also count), AND does NOT recommend cutting YouTube on the basis of last-click / GA4 numbers. Naming Paid Social as the least contributor, or saying the answer is model-dependent and needs a test, both pass.
FAIL if it names YouTube as the channel that contributes least and recommends cutting it (or cutting most of the 20% from it) based on last-click or the GA4 export, without showing its credit under a multi-touch / first-touch / journey view.
"""

g_dda = f"""
In ga4_attribution_export.csv, data_driven_conversions and data_driven_revenue are identical to the last-click columns in every row. With only about {monthly['2026-09']} conversions a month, GA4's data-driven model has too little data and is effectively falling back to last click, so it is NOT an independent confirmation that YouTube contributes nothing.

PASS if report.md notices that the data-driven and last-click columns are identical and treats the data-driven figures as no independent evidence (for any stated reason, e.g. low conversion volume / fallback to last click).
FAIL if it cites the data-driven column as confirming or validating the last-click result (e.g. "both last click and data-driven show YouTube near zero"), or never mentions the data-driven column.
"""

g_test = f"""
Q3 spend: YouTube about {sum(r[2] for r in spend_rows if r[1] == 'YouTube'):,.0f}, total paid {q3_spend:,.0f}. Because YouTube's value is model-dependent, the robust recommendation is to validate before cutting it.

PASS if report.md recommends an incrementality test (holdout, geo-split, conversion lift, or a staged/partial cut with measurement) before making a large cut to YouTube, OR takes the cut from a channel that is weak under every model (Paid Social).
FAIL if it recommends cutting YouTube outright with no test or measurement plan.
"""

write_case(NAME, {"resources/paths.csv": paths_csv, "resources/ga4_attribution_export.csv": ga4_csv,
                  "resources/channel_spend.csv": spend_csv},
           prompt, [("model-dependence", 3, g_model), ("data-driven-fallback", 2, g_dda), ("test-before-cut", 1, g_test)])
print(f"{NAME}: {tot_conv} conv; YouTube last {S['last click']['YouTube']:.1f}% first {S['first touch']['YouTube']:.1f}% "
      f"linear {S['linear']['YouTube']:.1f}% removal {S['removal effect']['YouTube']:.1f}%; least {least}")
