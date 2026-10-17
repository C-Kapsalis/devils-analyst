"""Breadth: "record MQL quarter", should we hire another SDR? (Tallyfold, B2B SaaS, Apr-Sep 2026).

Planted problems (5): the MQL score threshold was lowered from 60 to 40 on
15 Jul; the surge is the 40-59 band, which converts to SQL at a few percent,
while SQLs are flat (DECISION: no SDR hire on this); an August list import
counted as new leads; cost per MQL fell while cost per SQL rose; the "MQL to
SQL fell" rate is this quarter's SQLs over this quarter's MQLs including
September MQLs too young to have been worked; SDR time-to-first-touch is flat,
so capacity is not the bottleneck.
Decoys (2): August lead dip matching August last year (seasonal); demo
requests that skip MQL counted as reaching MQL (stated convention)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-crm-mql-surge"
rng = random.Random(82212)
MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
SEAS = {"04": 1.0, "05": 1.03, "06": 0.98, "07": 0.97, "08": 0.80, "09": 1.04}
SPEND = 48000

leads, bands, sdr = [], [], []
for m in MONTHS:
    mm = m[5:]
    f = int(1500 * SEAS[mm] * rng.uniform(0.97, 1.03))
    leads.append([m, "form", f])
    ly = int(1450 * SEAS[mm] * rng.uniform(0.97, 1.03))
    leads.append([m.replace("2026", "2025"), "form", ly])
    imp = 2100 if m == "2026-08" else 0
    if imp:
        leads.append([m, "import", imp])
    # rule: 60+ always MQL; 40-59 MQL from 15 Jul (half of July)
    hi = int(f * rng.uniform(0.215, 0.23))
    mid_share = 0.0 if m < "2026-07" else (0.5 if m == "2026-07" else 1.0)
    mid = int(f * rng.uniform(0.19, 0.21) * mid_share) + (int(imp * 0.11) if imp else 0)
    demo = int(f * rng.uniform(0.028, 0.032))          # demo requests skip MQL, counted as reaching MQL
    age_frac = 0.75 if m == "2026-09" else 1.0         # September MQLs not yet fully worked
    hi_sql = int(hi * rng.uniform(0.37, 0.39) * age_frac)
    mid_sql = int(mid * rng.uniform(0.035, 0.05) * age_frac)
    demo_sql = int(demo * rng.uniform(0.80, 0.86))
    bands.append([m, "60_plus", hi, hi_sql]); bands.append([m, "demo_request", demo, demo_sql])
    if mid:
        bands.append([m, "40_59", mid, mid_sql])
    sdr.append([m, 4, round(rng.uniform(3.2, 4.4), 1), round(rng.uniform(0.88, 0.95), 2)])

def B(months, band=None, i=2):
    return sum(r[i] for r in bands if r[0] in months and (band is None or r[1] == band))
Q2, Q3 = MONTHS[:3], MONTHS[3:]
mql_q2, mql_q3 = B(Q2), B(Q3)
sql_q2, sql_q3 = B(Q2, i=3), B(Q3, i=3)
mql_ch = mql_q3 / mql_q2 - 1
sql_ch = sql_q3 / sql_q2 - 1
naive_conv_q2, naive_conv_q3 = sql_q2 / mql_q2, sql_q3 / mql_q3
hi_conv = {q: B(ms, "60_plus", 3) / B(ms, "60_plus") for q, ms in (("Q2", Q2), ("Q3_jul_aug", Q3[:2]))}
mid_conv = B(Q3[:2], "40_59", 3) / B(Q3[:2], "40_59")
mid_q3 = B(Q3, "40_59")
cpm_q2, cpm_q3 = SPEND * 3 / mql_q2, SPEND * 3 / mql_q3
cps_q2, cps_q3 = SPEND * 3 / sql_q2, SPEND * 3 / sql_q3
L = lambda ms, meth=None: sum(r[2] for r in leads if r[0] in ms and (meth is None or r[1] == meth))
leads_ch = L(Q3) / L(Q2) - 1
leads_ch_form = L(Q3, "form") / L(Q2, "form") - 1
aug26 = L(["2026-08"], "form"); jul26 = L(["2026-07"], "form")
aug25 = L(["2025-08"]); jul25 = L(["2025-07"])
ttft = [r[2] for r in sdr]

changes = [["2026-03-02", "Lead scoring", "Added +10 for webinar attendance", "revops"],
           ["2026-07-15", "Lead scoring", "MQL threshold changed from score >= 60 to score >= 40; +15 for pricing page visit", "revops"],
           ["2026-08-19", "Import", "Imported 2,100 contacts from the Northbridge partner list (lifecycle stage: lead)", "marketing ops"]]

assert mql_ch > 0.5 and abs(sql_ch) < 0.08, (mql_ch, sql_ch)
assert abs(hi_conv["Q2"] - hi_conv["Q3_jul_aug"]) < 0.03 and mid_conv < 0.06
assert naive_conv_q3 < naive_conv_q2 * 0.7
assert cpm_q3 < cpm_q2 * 0.7 and cps_q3 > cps_q2 * 0.98
assert leads_ch > 0.3 and abs(leads_ch_form) < 0.06, (leads_ch, leads_ch_form)
assert abs(aug26 / jul26 - aug25 / jul25) < 0.06
assert max(ttft) < 5

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=0: f"{100 * x:.{d}f}%"

wins = f"""# Q3 2026: marketing wins (for the leadership meeting)

- **MQLs up {pc(mql_ch)}** quarter on quarter ({mql_q2:,} in Q2, {mql_q3:,} in Q3). Best quarter ever.
- **Leads up {pc(leads_ch)}** ({L(Q2):,} to {L(Q3):,}).
- **Cost per MQL down {pc(1 - cpm_q3 / cpm_q2)}** ({usd(cpm_q2)} to {usd(cpm_q3)}) on flat spend.
- MQL to SQL conversion fell from {pc(naive_conv_q2)} to {pc(naive_conv_q3)} (Q3 SQLs / Q3 MQLs): the SDR team cannot keep up with the volume.
- Note: demo requests go straight to SQL; we count them as having reached MQL.
- August leads dipped from July, as usual over the summer.

Ask: approve a fifth SDR from November to work the extra MQLs.
"""

notes = """# Notes
- Tallyfold sells accounting automation software to mid-size firms. Marketing spend is about $48,000 a month, flat all year.
- mqls_by_score_band.csv: contacts by the month they became an MQL and the lead score band at that moment, with how many have since reached SQL (as of 10 October 2026).
- sdr_activity_monthly.csv: SDR headcount, median hours from MQL to first SDR touch, share of MQLs touched within 2 working days.
"""

files = {
    "resources/notes.md": notes,
    "resources/q3_marketing_wins.md": wins,
    "resources/leads_by_month.csv": to_csv(["create_month", "create_method", "new_leads"], sorted(leads)),
    "resources/mqls_by_score_band.csv": to_csv(["mql_month", "score_band", "mqls", "reached_sql"], bands),
    "resources/sdr_activity_monthly.csv": to_csv(["month", "sdr_headcount", "median_hours_to_first_touch", "share_touched_within_2_days"], sdr),
    "resources/crm_change_log.csv": to_csv(["date", "area", "change", "changed_by"], changes),
}

prompt = """
Marketing is presenting Q3 as a record quarter for MQLs (resources/q3_marketing_wins.md), and sales wants a fifth SDR to handle the volume. The CRM exports are in resources/. Was Q3 really that good, and should we approve the SDR? Please write your view in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. The MQL rule loosened. crm_change_log.csv shows the MQL threshold lowered from 60 to 40 on 2026-07-15. Q3 adds {mid_q3:,} MQLs in the 40-59 band, which reach SQL at about {pc(mid_conv, 1)} (July-August), while the 60+ band converts at {pc(hi_conv['Q2'])} in Q2 and {pc(hi_conv['Q3_jul_aug'])} in July-August (unchanged). SQLs moved only {pc(sql_ch, 1)} ({sql_q2:,} to {sql_q3:,}). Counts as found if report.md attributes the MQL surge to the threshold change (or to the 40-59 band) and notes SQLs are flat.
2. List import counted as leads. 2,100 contacts imported on 2026-08-19 are in the lead count; form leads changed only {pc(leads_ch_form, 1)} Q2 to Q3 against the claimed {pc(leads_ch)}. Counts as found if report.md flags the import inflating leads.
3. Cost per MQL down, cost per SQL not. Cost per MQL fell from {usd(cpm_q2)} to {usd(cpm_q3)}, but cost per SQL went from {usd(cps_q2)} to {usd(cps_q3)}. Counts as found if report.md says the efficiency gain disappears at SQL level.
4. Conversion rate mixes cohorts. The "{pc(naive_conv_q2)} to {pc(naive_conv_q3)}" divides all Q3 SQLs by all Q3 MQLs, mixing a looser MQL definition with September MQLs that have not yet been worked; by score band the 60+ conversion has not changed. Counts as found if report.md recomputes conversion by band or by cohort/age and shows the drop is definitional or immature, not SDR follow-up.
5. SDR capacity is not the bottleneck. Median hours to first touch stay at {min(ttft)}-{max(ttft)} and 88-95% of MQLs are touched within 2 days every month. Counts as found if report.md uses this to say the SDRs are keeping up.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct answer: Q3 was not a record quarter in substance. The MQL rise is the threshold change (and the list import); SQLs are flat ({pc(sql_ch, 1)}) and SDRs are touching MQLs as fast as before. Do not approve the fifth SDR on this basis (or defer until SQL volume rises); fix or report the MQL definition (e.g. restore 60, or report the bands separately) and judge marketing on SQLs or opportunities.

Naive answer: celebrate the {pc(mql_ch)} MQL growth and approve the SDR because conversion "fell" to {pc(naive_conv_q3)}.

PASS if report.md recommends not approving (or deferring) the SDR hire because the MQL growth is definitional and SQLs are flat.
FAIL if report.md approves the SDR, or presents Q3 as a genuine record quarter.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. August form leads dipped from July ({jul26:,} to {aug26:,}); August 2025 shows the same summer dip ({jul25:,} to {aug25:,}). Seasonal, not a problem.
- D2. Demo requests skip MQL and go straight to SQL; the team counts them as having reached MQL and says so. That is an acceptable, stated convention.

PASS if report.md does not present the August dip as a marketing problem and does not call the demo-request convention an error. Mentioning either as fine is OK.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: MQL {mql_q2}->{mql_q3} ({mql_ch:+.2f}); SQL {sql_q2}->{sql_q3} ({sql_ch:+.3f}); conv naive {naive_conv_q2:.3f}->{naive_conv_q3:.3f}; "
      f"hi {hi_conv}; mid {mid_conv:.3f}; CPM {cpm_q2:.0f}->{cpm_q3:.0f} CPS {cps_q2:.0f}->{cps_q3:.0f}; leads {leads_ch:+.2f} form {leads_ch_form:+.3f}")
