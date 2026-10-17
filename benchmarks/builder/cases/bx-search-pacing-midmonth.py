"""Breadth benchmark, paid search: mid-month pacing check (Fleetfoot Running, 1-20 October 2026).

Subtle problems (4): Generic - Running Shoes spends its full daily budget every
day, loses ~40% impression share to budget and runs at CPA ~28 vs target 45:
the under-delivering winner (DECISION); Generic - Apparel's budget was raised
on 13 October, so the agency's month-to-date-average projection says "on plan"
while the last-7-day run rate projects well over plan at CPA ~70 vs 45
(DECISION: move money from Apparel to Running Shoes); brand CPC jumped ~2.5x
from 9 October when a new competitor appeared in auction insights, with brand
clicks and conversions flat; DSA spends ~20% on /careers/ and /blog/ pages
with zero conversions.
Decoys (2): one day where DSA spent ~1.9x its daily budget (Google allows up
to 2x a day; only the month is capped); the last 3 days show fewer
conversions (reported by click date, still filling in)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-search-pacing-midmonth"
rng = random.Random(90213)
DAYS = 20; MONTH_DAYS = 31
dates = [f"2026-10-{d:02d}" for d in range(1, DAYS + 1)]
PLAN = {"Brand - Fleetfoot": 2600, "Generic - Running Shoes": 15000, "Generic - Apparel": 13000, "DSA - All Pages": 4600}
TARGET_CPA = 45.0
lag_mult = lambda d: {DAYS: 0.45, DAYS - 1: 0.62, DAYS - 2: 0.80}.get(d, 1.0)

rows = []
for i, dt in enumerate(dates):
    d = i + 1
    # Brand: CPC jumps from 9 Oct
    cpc = 0.42 * rng.uniform(0.95, 1.05) if d < 9 else 1.06 * rng.uniform(0.94, 1.06)
    clicks = int(rng.gauss(118, 8))
    cost = round(clicks * cpc, 2)
    imps = int(clicks / rng.uniform(0.36, 0.40))
    conv = int(round(clicks * 0.085 * rng.uniform(0.9, 1.1) * lag_mult(d)))
    rows.append([dt, "Brand - Fleetfoot", 200, imps, clicks, cost, conv, round(rng.uniform(0.0, 0.02), 2)])
    # Running shoes: capped from day 3
    budget = 400
    cost = round(budget * (rng.uniform(0.80, 0.9) if d < 3 else rng.uniform(0.985, 1.0)), 2)
    cpc = 1.15 * rng.uniform(0.96, 1.04); clicks = int(cost / cpc)
    conv = int(round(cost / (28 * rng.uniform(0.9, 1.1)) * lag_mult(d)))
    rows.append([dt, "Generic - Running Shoes", budget, int(clicks / rng.uniform(0.055, 0.065)), clicks, cost, conv,
                 round(rng.uniform(0.0, 0.05), 2) if d < 3 else round(rng.uniform(0.38, 0.45), 2)])
    # Apparel: budget raised on day 13
    budget = 300 if d < 13 else 650
    cost = round(budget * rng.uniform(0.95, 1.0), 2)
    cpc = 0.95 * rng.uniform(0.96, 1.04); clicks = int(cost / cpc)
    conv = int(round(cost / (71 * rng.uniform(0.88, 1.12)) * lag_mult(d)))
    rows.append([dt, "Generic - Apparel", budget, int(clicks / rng.uniform(0.045, 0.055)), clicks, cost, conv, round(rng.uniform(0.0, 0.04), 2)])
    # DSA: one 1.9x day
    budget = 150
    cost = round(budget * (1.9 if d == 16 else rng.uniform(0.82, 0.97)), 2)
    cpc = 0.78 * rng.uniform(0.95, 1.05); clicks = int(cost / cpc)
    conv = int(round(cost / (52 * rng.uniform(0.85, 1.15)) * lag_mult(d)))
    rows.append([dt, "DSA - All Pages", budget, int(clicks / rng.uniform(0.03, 0.04)), clicks, cost, conv, round(rng.uniform(0.0, 0.06), 2)])

# auction insights for brand campaign
ai_rows = []
for w, (s, e) in enumerate([(1, 4), (5, 8), (9, 12), (13, 16), (17, 20)]):
    new = w >= 2
    ai_rows.append([f"2026-10-{s:02d}", f"2026-10-{e:02d}", "Brand - Fleetfoot", "stridelab.com",
                    round(rng.uniform(0.44, 0.52), 2) if new else 0.0, round(rng.uniform(0.28, 0.34), 2) if new else 0.0])
    ai_rows.append([f"2026-10-{s:02d}", f"2026-10-{e:02d}", "Brand - Fleetfoot", "runnersdepot.com",
                    round(rng.uniform(0.08, 0.12), 2), round(rng.uniform(0.03, 0.06), 2)])

# DSA landing pages
dsa = [r for r in rows if r[1] == "DSA - All Pages"]
dsa_cost = sum(r[5] for r in dsa); dsa_conv = sum(r[6] for r in dsa)
PAGES = [("/running-shoes/", 0.31, 0.46), ("/trail/", 0.18, 0.24), ("/apparel/", 0.14, 0.12), ("/sale/", 0.16, 0.18),
         ("/careers/", 0.12, 0.0), ("/blog/how-to-tie-running-shoes", 0.05, 0.0), ("/blog/marathon-training-plan", 0.04, 0.0)]
lp_rows = []
acc_c = acc_v = 0
for j, (p, cs, vs) in enumerate(PAGES):
    if j < len(PAGES) - 1:
        c = round(dsa_cost * cs, 2); v = int(round(dsa_conv * vs))
    else:
        c = round(dsa_cost - acc_c, 2); v = dsa_conv - acc_v
    acc_c += c; acc_v += v
    clicks = int(c / 0.78)
    lp_rows.append(["DSA - All Pages", "https://www.fleetfootrunning.com" + p, clicks, c, v])

# ---------- ground truth ----------
def camp(c): return [r for r in rows if r[1] == c]
mtd = {c: sum(r[5] for r in camp(c)) for c in PLAN}
naive_proj = {c: mtd[c] / DAYS * MONTH_DAYS for c in PLAN}
t7 = {c: sum(r[5] for r in camp(c)[-7:]) / 7 for c in PLAN}
proj7 = {c: mtd[c] + t7[c] * (MONTH_DAYS - DAYS) for c in PLAN}
conv_mature = {c: sum(r[6] for r in camp(c)[:DAYS - 3]) for c in PLAN}
cost_mature = {c: sum(r[5] for r in camp(c)[:DAYS - 3]) for c in PLAN}
cpa = {c: cost_mature[c] / conv_mature[c] for c in PLAN}
plan_tot = sum(PLAN.values()); naive_tot = sum(naive_proj.values()); proj7_tot = sum(proj7.values())
R, A, Bd, D = "Generic - Running Shoes", "Generic - Apparel", "Brand - Fleetfoot", "DSA - All Pages"
capped_days = sum(1 for r in camp(R)[2:] if r[5] >= 0.98 * r[2])
lost_r = sum(r[7] for r in camp(R)[2:]) / (DAYS - 2)
b_pre = camp(Bd)[:8]; b_post = camp(Bd)[8:DAYS - 3]
cpc_pre = sum(r[5] for r in b_pre) / sum(r[4] for r in b_pre); cpc_post = sum(r[5] for r in b_post) / sum(r[4] for r in b_post)
clk_pre = sum(r[4] for r in b_pre) / len(b_pre); clk_post = sum(r[4] for r in b_post) / len(b_post)
dsa_waste = sum(r[3] for r in lp_rows if "/careers/" in r[1] or "/blog/" in r[1])
spike = camp(D)[15]
recent = sum(r[6] for r in rows if r[0] in dates[-3:]) / 3; earlier = sum(r[6] for r in rows if r[0] in dates[:-3]) / (DAYS - 3)

assert capped_days == DAYS - 2 and lost_r > 0.38 and cpa[R] < 0.7 * TARGET_CPA
assert naive_proj[R] < 0.9 * PLAN[R]
assert abs(naive_proj[A] / PLAN[A] - 1) < 0.05 and proj7[A] / PLAN[A] > 1.15 and cpa[A] > 1.4 * TARGET_CPA
assert 0.85 < naive_tot / plan_tot < 1.0
assert cpc_post > 2.2 * cpc_pre and abs(clk_post / clk_pre - 1) < 0.08
assert 0.17 < dsa_waste / dsa_cost < 0.25
assert spike[5] / spike[2] > 1.85 and recent < 0.75 * earlier

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

pacing = f"""# Fleetfoot Running: October pacing check (agency, as of 20 October)

Month-to-date spend {eur(sum(mtd.values()))} of a {eur(plan_tot)} October plan.
Projection (month-to-date daily average x 31 days): {eur(naive_tot)}, {pc(naive_tot / plan_tot)} of plan.

| campaign | plan | MTD spend | projected |
|---|---|---|---|
""" + "".join(f"| {c} | {eur(PLAN[c])} | {eur(mtd[c])} | {eur(naive_proj[c])} |\n" for c in PLAN) + """
Target CPA for all non-brand campaigns: €45. Conversions are reported by click date.
Verdict: pacing on track, slight underspend; no changes needed this month.
"""

files = {
    "resources/agency_pacing_note.md": pacing,
    "resources/google_ads_daily_oct2026.csv": to_csv(
        ["date", "campaign", "daily_budget", "impressions", "clicks", "cost", "conversions", "search_lost_is_budget"], rows),
    "resources/auction_insights_brand_oct2026.csv": to_csv(
        ["period_start", "period_end", "campaign", "display_domain", "overlap_rate", "outranking_share"], ai_rows),
    "resources/dsa_landing_pages_oct2026.csv": to_csv(["campaign", "landing_page", "clicks", "cost", "conversions"], lp_rows),
}

prompt = """
We're Fleetfoot Running and we're 20 days into October. Our agency says search pacing is fine; their note and the Google Ads exports are in resources/. Are we on track, and what should we change for the rest of the month? Put your answer and the numbers in report.md.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files; CPA uses 1-17 Oct because the last 3 days are still filling in):

1. Generic - Running Shoes is capped. It spent at least 98% of its €400 daily budget on {capped_days} of {DAYS - 2} days since 3 October, loses about {pc(lost_r)} impression share to budget, and its CPA is about {eur(cpa[R])} vs the €45 target; it projects to {eur(naive_proj[R])} vs a {eur(PLAN[R])} plan. Found if report.md says this campaign is budget-limited / under-delivering while beating target.
2. Generic - Apparel is over-pacing and over target. Its budget rose from €300 to €650 on 13 October; the month-to-date-average projection ({eur(naive_proj[A])}, about {pc(naive_proj[A] / PLAN[A])} of plan) hides that at the last-7-day rate it ends near {eur(proj7[A])} ({pc(proj7[A] / PLAN[A])} of plan). CPA about {eur(cpa[A])} vs €45. Found if report.md says Apparel will overspend at its current rate (budget change / trailing run rate) OR that its CPA is far above target; full substance needs either point with a number.
3. Brand CPC jump from a new competitor. Brand CPC went from about €{cpc_pre:.2f} before 9 October to about €{cpc_post:.2f} after, with daily clicks flat (about {clk_pre:.0f} vs {clk_post:.0f}); auction insights show stridelab.com appearing from 9 October with about 45-50% overlap. Found if report.md links the brand CPC rise to the new competitor / conquesting.
4. DSA spends on non-commercial pages. {eur(dsa_waste)} ({pc(dsa_waste / dsa_cost)} of DSA cost) went to /careers/ and /blog/ pages with zero conversions. Found if report.md flags these pages and suggests excluding them.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with their specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: shift budget from Generic - Apparel (projected about {pc(proj7[A] / PLAN[A])} of plan at the current rate, CPA about {eur(cpa[A])} vs €45) to Generic - Running Shoes (capped every day, CPA about {eur(cpa[R])}, about {pc(lost_r)} share lost to budget), e.g. raise the Running Shoes daily budget and lower Apparel's.

Naive wrong answers: "on track, no changes" (the agency's verdict based on the account total of {pc(naive_tot / plan_tot)} of plan), or spreading the apparent underspend across all campaigns, including Apparel.

PASS if report.md's main recommendation is to raise Running Shoes' budget AND fund it at least partly by cutting/reducing Apparel (or explicitly says Apparel should not get more).
FAIL if it agrees no change is needed, recommends raising budgets across the board, or raises Running Shoes while also keeping or raising Apparel's €650 budget.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. On 16 October DSA - All Pages spent {eur(spike[5])} against a €150 daily budget ({spike[5] / spike[2]:.1f}x). Google may spend up to 2x the daily budget on a given day; only the month (daily budget x 30.4) is capped.
- D2. The last three days (18-20 October) show fewer conversions per day (about {recent:.0f} vs {earlier:.0f} earlier). Conversions are reported by click date, so recent days are still filling in.

PASS if report.md does not call the 16 October DSA spend an overspend error/billing problem, and does not treat the last-3-day conversion dip as a real performance drop requiring action. Mentioning either as normal, or excluding the last days from CPA, is fine.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: R cpa {cpa[R]:.1f} proj {naive_proj[R]:.0f}/{PLAN[R]}; A cpa {cpa[A]:.1f} naive {naive_proj[A]:.0f} t7 {proj7[A]:.0f}/{PLAN[A]}; "
      f"tot {naive_tot:.0f}/{plan_tot}; brand cpc {cpc_pre:.2f}->{cpc_post:.2f}; dsa waste {dsa_waste / dsa_cost:.2f}")
