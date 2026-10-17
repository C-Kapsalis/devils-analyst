"""Meta reach is people, not events: it does not add across days, months,
campaigns or report levels. Q3 reach is the account-level row for the quarter;
frequency = impressions / that reach (high and rising, with CTR falling).
Summing reach makes frequency look like 1-3 and 'fine'."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
from datetime import date, timedelta

NAME = "fb-reach-frequency"
rng = random.Random(5521)

# campaign: (base daily impressions, CPM, monthly freq, quarter freq, ad sets)
CAMPAIGNS = {
    "Prospecting - Broad":     (9500, 8.8, 2.1, 6.4, ["Broad 25-54", "Broad 55+"]),
    "Prospecting - Interests": (6500, 9.6, 2.3, 6.9, ["Hiking & Camping", "Trail Running"]),
    "Retargeting - Engagers":  (4200, 12.5, 3.1, 9.8, ["Site Visitors 30d", "IG Engagers 60d"]),
    "Advantage+ Shopping":     (8000, 8.2, 2.0, 6.0, ["ASC - All Products", "ASC - New Arrivals"]),
}
MONTHS = [(7, 31), (8, 31), (9, 30)]
ACC_MONTH_F = {7: 4.0, 8: 4.9, 9: 5.9}   # account monthly frequency rises
ACC_Q_F = 10.2

daily = []
d0 = date(2026, 7, 1)
for i in range(92):
    d = d0 + timedelta(days=i)
    fatigue = i / 91
    for c, (base, cpm, fm, fq, _) in CAMPAIGNS.items():
        imps = int(base * rng.uniform(0.85, 1.15))
        reach = int(imps / rng.uniform(1.12, 1.28))
        spend = round(imps / 1000 * cpm * (1 + 0.25 * fatigue) * rng.uniform(0.95, 1.05), 2)
        ctr = (0.0165 - 0.0075 * fatigue) * (1.3 if "Retargeting" in c else 1.0) * rng.uniform(0.9, 1.1)
        clicks = int(imps * ctr)
        daily.append([d.isoformat(), c, reach, imps, spend, clicks])

mon_rows = []
def agg(rr):
    return sum(r[3] for r in rr), round(sum(r[4] for r in rr), 2), sum(r[5] for r in rr)

for m, nd in MONTHS:
    s, e = f"2026-{m:02d}-01", f"2026-{m:02d}-{nd}"
    mr = [r for r in daily if r[0][5:7] == f"{m:02d}"]
    imps, spend, clicks = agg(mr)
    mon_rows.append(["account", s, e, "", "", int(imps / (ACC_MONTH_F[m] * rng.uniform(0.98, 1.02))), imps, spend, clicks])
    for c, (_, _, fm, _, adsets) in CAMPAIGNS.items():
        cr = [r for r in mr if r[1] == c]
        ci, cs, cc = agg(cr)
        fmm = fm * (1 + 0.12 * (m - 7)) * rng.uniform(0.97, 1.03)
        mon_rows.append(["campaign", s, e, c, "", int(ci / fmm), ci, cs, cc])
        split = rng.uniform(0.55, 0.65)
        for k, a in enumerate(adsets):
            sh = split if k == 0 else 1 - split
            ai, asp, ac = int(ci * sh), round(cs * sh, 2), int(cc * sh)
            mon_rows.append(["ad_set", s, e, c, a, int(ai / (fmm * 0.85)), ai, asp, ac])

qi, qs, qc = agg(daily)
q_rows = [["account", "2026-07-01", "2026-09-30", "", "", int(qi / ACC_Q_F), qi, qs, qc]]
for c, (_, _, _, fq, _) in CAMPAIGNS.items():
    ci, cs, cc = agg([r for r in daily if r[1] == c])
    q_rows.append(["campaign", "2026-07-01", "2026-09-30", c, "", int(ci / fq), ci, cs, cc])
mon_rows = q_rows + mon_rows

reach_csv = to_csv(["report_level", "date_start", "date_stop", "campaign_name", "adset_name", "reach",
                    "impressions", "spend", "inline_link_clicks"], mon_rows)
daily_csv = to_csv(["date", "campaign_name", "reach", "impressions", "spend", "inline_link_clicks"], daily)

# ---- ground truth ----
acc_q = q_rows[0]
R, I = acc_q[5], acc_q[6]
freq = I / R
assert I == sum(r[3] for r in daily)
is_q = lambda r: r[1] == "2026-07-01" and r[2] == "2026-09-30"
acc_m = {r[1][5:7]: (r[5], r[6]) for r in mon_rows if r[0] == "account" and not is_q(r)}
mf = {k: v[1] / v[0] for k, v in sorted(acc_m.items())}
ctr_m = {}
for m, _ in MONTHS:
    mr = [r for r in daily if r[0][5:7] == f"{m:02d}"]
    ctr_m[m] = sum(r[5] for r in mr) / sum(r[3] for r in mr)

naive_daily = sum(r[2] for r in daily)
naive_camp_month = sum(r[5] for r in mon_rows if r[0] == "campaign" and not is_q(r))
naive_all_monthly = sum(r[5] for r in mon_rows)
naive_acc_months = sum(v[0] for v in acc_m.values())
naive_camp_q = sum(r[5] for r in q_rows if r[0] == "campaign")
naives = {"sum of daily campaign reach": naive_daily,
          "sum of monthly campaign rows": naive_camp_month,
          "sum of every row in the reach file": naive_all_monthly,
          "sum of the three monthly account rows": naive_acc_months,
          "sum of the four quarterly campaign rows": naive_camp_q}
for k, v in naives.items():
    assert v > 1.4 * R, (k, v, R)
assert freq > 9 and I / naive_daily < 1.3 and I / naive_camp_month < 3.5
assert mf["07"] < mf["08"] < mf["09"] and ctr_m[7] > ctr_m[9] * 1.4

f0 = lambda x: f"{x:,.0f}"
naive_lines = "\n".join(f"- {k}: reach {f0(v)}, frequency {I / v:.2f}" for k, v in naives.items())
mf_line = ", ".join(f"{m}: {v:.1f}" for m, v in zip(["July", "August", "September"], mf.values()))
ctr_line = ", ".join(f"{m}: {100 * ctr_m[k]:.2f}%" for m, k in zip(["July", "August", "September"], [7, 8, 9]))

prompt = """
Our Meta Ads exports for Q3 2026 are in resources/: meta_reach_report.csv (reach and delivery at account, campaign and ad set level) and meta_campaign_daily.csv (daily delivery by campaign). How many people did our Meta ads reach in Q3, and how often did they see them? Is our frequency too high? Write report.md with the numbers and what you'd change.
"""

g_reach = f"""
Reach counts unique people and cannot be added across days, months, campaigns or report levels. The Q3 answer is the single account-level row covering 2026-07-01 to 2026-09-30.
Ground truth Q3 2026:
- Reach: {f0(R)} people
- Impressions: {f0(I)}
- Frequency = impressions / reach = {freq:.2f}
Wrong answers from adding reach up:
{naive_lines}

PASS if report.md gives Q3 reach of {f0(R)} (within 2%) and Q3 frequency of {freq:.2f} (within 5%).
FAIL if the reach figure is any of the summed values above (or any other figure more than 2% away from {f0(R)}), or if the frequency is below 8.
"""

g_verdict = f"""
Ground truth: Q3 frequency is {freq:.2f} (each person reached saw the ads about {freq:.0f} times in the quarter). Account frequency by month rose ({mf_line}) while link click-through rate fell ({ctr_line}), a classic ad-fatigue signal.

PASS if report.md concludes frequency is high / too high or showing fatigue (e.g. cites the rising monthly frequency and/or falling CTR) and recommends at least one concrete fix (frequency cap, creative refresh, broaden or exclude audiences, shift budget from saturated retargeting/prospecting sets, etc.).
FAIL if it says frequency is low, healthy or fine, or bases its verdict on a frequency below 4.
"""

write_case(NAME, {"resources/meta_reach_report.csv": reach_csv, "resources/meta_campaign_daily.csv": daily_csv},
           prompt, [("reach-frequency", 3, g_reach), ("fatigue-verdict", 2, g_verdict)])
print(f"{NAME}: Q3 reach {R} freq {freq:.2f}; naive daily-sum reach {naive_daily} freq {I / naive_daily:.2f}; "
      f"monthly-campaign sum freq {I / naive_camp_month:.2f}; monthly freq {mf}")
