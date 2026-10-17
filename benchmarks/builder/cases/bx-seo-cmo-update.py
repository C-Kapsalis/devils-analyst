"""Breadth: organic search update before a CMO meeting (Hollowmere Running, Apr-Sep 2026).

Planted problems (5): total organic clicks flat only because brand clicks rose
while non-brand (the acquiring half) fell about a quarter (DECISION); the
agency's "impressions up" growth comes from countries Hollowmere does not ship
to; the count of new pages earning first impressions has run down to zero
while clicks hold; AI-assistant traffic reported as zero from a stale referrer
list (chat.openai.com / bard.google.com) while chatgpt.com, perplexity.ai and
gemini.google.com send sessions converting above organic; a new post crowned
"ranks #2" on a few dozen impressions.
Decoys (2): Search Console clicks above GA4 organic sessions; September clicks
a little under August because September has 30 days (per day flat)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-seo-cmo-update"
rng = random.Random(81202)
MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
DAYS = [30, 31, 30, 31, 31, 30]

BRAND = {"hollowmere running": 5200, "hollowmere": 2100, "hollowmere trail shoes": 900, "hollowmere running shoes": 750, "hollowmere discount code": 420, "hollowmere returns": 260}
NONBRAND = {
    "trail running shoes": (1900, 6.8), "best trail running shoes": (1500, 7.9), "waterproof trail shoes": (980, 8.6),
    "running shoes for wide feet": (870, 5.4), "zero drop running shoes": (760, 6.1), "stability running shoes": (720, 9.4),
    "carbon plate running shoes": (690, 10.2), "marathon training plan": (650, 4.2), "half marathon training plan": (610, 4.6),
    "how to choose running shoes": (560, 5.1), "running socks": (480, 7.3), "trail running vest": (450, 8.8),
    "running shoes for flat feet": (430, 6.6), "best running shoes for beginners": (410, 9.9), "how often replace running shoes": (380, 3.9),
    "running gaiters": (300, 7.7), "ultra running shoes": (290, 11.4), "recovery shoes": (270, 8.1),
    "running shoe sizing": (250, 5.5), "minimalist running shoes": (240, 9.1), "trail running for beginners": (230, 6.4),
    "hydration belt running": (200, 10.8), "running jacket waterproof": (190, 12.2), "heel drop explained": (170, 4.4),
}
# per-month multipliers on clicks; brand rises, non-brand falls
B_MULT = [1.00, 1.07, 1.15, 1.24, 1.32, 1.41]
N_MULT = [1.00, 0.96, 0.91, 0.86, 0.81, 0.76]

rows, mt = [], {m: dict(b=0, n=0, bi=0, ni=0) for m in MONTHS}
for i, m in enumerate(MONTHS):
    for q, base in BRAND.items():
        c = int(base * B_MULT[i] * rng.uniform(0.96, 1.04) * DAYS[i] / 30.5)
        imps = int(c / rng.uniform(0.40, 0.52))
        rows.append([m, q, c, imps, round(c / imps, 4), round(rng.uniform(1.0, 1.3), 1)])
        mt[m]["b"] += c; mt[m]["bi"] += imps
    for q, (base, pos) in NONBRAND.items():
        c = int(base * N_MULT[i] * rng.uniform(0.95, 1.05) * DAYS[i] / 30.5)
        p = round(pos + 0.45 * i + rng.uniform(-0.3, 0.3), 1)
        imps = int(c / max(0.012, 0.30 / p) * rng.uniform(0.95, 1.05))
        rows.append([m, q, c, imps, round(c / imps, 4), p])
        mt[m]["n"] += c; mt[m]["ni"] += imps
# make Aug->Sep total smaller only because of 30 vs 31 days: check per-day
tot = {m: mt[m]["b"] + mt[m]["n"] for m in MONTHS}
apr, sep, aug = tot["2026-04"], tot["2026-09"], tot["2026-08"]
total_change = sep / apr - 1
b_change = mt["2026-09"]["b"] / mt["2026-04"]["b"] - 1
n_change = mt["2026-09"]["n"] / mt["2026-04"]["n"] - 1
q3 = MONTHS[3:]; q2 = MONTHS[:3]
nb_q2 = sum(mt[m]["n"] for m in q2); nb_q3 = sum(mt[m]["n"] for m in q3)
b_q2 = sum(mt[m]["b"] for m in q2); b_q3 = sum(mt[m]["b"] for m in q3)
t_q2, t_q3 = nb_q2 + b_q2, nb_q3 + b_q3
aug_pd, sep_pd = aug / 31, sep / 30

# ---------- country x device, Q2 vs Q3 (unfiltered property) ----------
CD = [  # country, device, q2 imps, q3 imps, ctr, pos
    ("United States", "mobile", 412000, 405000, 0.034, 8.9),
    ("United States", "desktop", 228000, 221000, 0.041, 7.6),
    ("United States", "tablet", 21000, 20000, 0.030, 9.4),
    ("Canada", "mobile", 61000, 60000, 0.031, 9.8),
    ("Canada", "desktop", 34000, 33000, 0.038, 8.7),
    ("India", "mobile", 52000, 171000, 0.0028, 34.5),
    ("Philippines", "mobile", 18000, 64000, 0.0025, 37.2),
    ("United Kingdom", "mobile", 26000, 41000, 0.0060, 22.8),
    ("Australia", "mobile", 14000, 19000, 0.0070, 21.4),
]
cd_rows = []
for c, d, i2, i3, ctr, pos in CD:
    a2 = int(i2 * rng.uniform(0.98, 1.02)); a3 = int(i3 * rng.uniform(0.98, 1.02))
    cd_rows.append([c, d, "2026-Q2", int(a2 * ctr), a2, round(pos * rng.uniform(0.98, 1.02), 1)])
    cd_rows.append([c, d, "2026-Q3", int(a3 * ctr * rng.uniform(0.97, 1.0)), a3, round(pos * rng.uniform(0.99, 1.04), 1)])
served = {"United States", "Canada"}
imp = lambda q, s=None: sum(r[4] for r in cd_rows if r[2] == q and (s is None or (r[0] in served) == s))
prop_imps_change = imp("2026-Q3") / imp("2026-Q2") - 1
served_change = imp("2026-Q3", True) / imp("2026-Q2", True) - 1
unserved_add = imp("2026-Q3", False) - imp("2026-Q2", False)

# ---------- pages with first impression month ----------
NEW_PER_MONTH = [13, 10, 7, 4, 2, 0]
pg_rows = []
slugs = ["trail", "road", "gear", "training", "fit", "care", "racing", "beginners", "injury", "nutrition"]
for k in range(46):
    pg_rows.append([f"/blog/{slugs[k % 10]}-{k:02d}", "before 2026-04", int(rng.uniform(80, 2200)), 0, 0])
for i, m in enumerate(MONTHS):
    for j in range(NEW_PER_MONTH[i]):
        pg_rows.append([f"/blog/{slugs[(i + j) % 10]}-n{i}{j}", m, int(rng.uniform(10, 600) / (i + 1)), 0, 0])
star = "/blog/trail-shoe-rotation"
pg_rows.append([star, "2026-08", 3, 38, 2.0])
for r in pg_rows:
    if r[3] == 0:
        r[3] = int(r[2] / rng.uniform(0.015, 0.05)); r[4] = round(rng.uniform(5, 18), 1)
new_counts = {m: sum(1 for r in pg_rows if r[1] == m) for m in MONTHS}

# ---------- GA4 referrals and channels, Q3 ----------
ref = [
    ["chatgpt.com", "referral", 1240, 0.66, 0.041],
    ["perplexity.ai", "referral", 310, 0.69, 0.045],
    ["gemini.google.com", "referral", 180, 0.61, 0.036],
    ["copilot.microsoft.com", "referral", 70, 0.57, 0.029],
    ["runnersforum.net", "referral", 2100, 0.48, 0.008],
    ["strava.com", "referral", 1650, 0.52, 0.011],
    ["reddit.com", "referral", 1420, 0.45, 0.009],
    ["trailzine.com", "referral", 640, 0.55, 0.014],
]
ref_rows = []
for s, mdm, n, er, cvr in ref:
    n = int(n * rng.uniform(0.97, 1.03)); p = int(round(n * cvr))
    ref_rows.append([s, mdm, n, int(n * er), p, round(p * rng.uniform(118, 134), 2)])
gsc_q3 = sum(r[2] for r in rows if r[0] in q3)
org_sessions = int(gsc_q3 * rng.uniform(0.90, 0.93))
org_cvr = 0.019
org_p = int(org_sessions * org_cvr)
ch_rows = [["Organic Search", org_sessions, int(org_sessions * 0.58), org_p, round(org_p * 126.0, 2)],
           ["Direct", 41200, 23100, 1010, 131800.0], ["Paid Search", 52300, 30100, 1490, 181400.0],
           ["Email", 18800, 12400, 690, 80100.0], ["Referral", sum(r[2] for r in ref_rows), sum(r[3] for r in ref_rows),
                                                  sum(r[4] for r in ref_rows), round(sum(r[5] for r in ref_rows), 2)]]
ai = [r for r in ref_rows if r[0] in ("chatgpt.com", "perplexity.ai", "gemini.google.com", "copilot.microsoft.com")]
ai_s, ai_p = sum(r[2] for r in ai), sum(r[4] for r in ai)
ai_cvr = ai_p / ai_s

# ---------- asserts ----------
assert abs(total_change) < 0.05, total_change
assert n_change < -0.20 and b_change > 0.30, (n_change, b_change)
assert prop_imps_change > 0.10 and served_change < 0.0, (prop_imps_change, served_change)
assert new_counts["2026-09"] == 0 and new_counts["2026-04"] >= 10
assert ai_cvr > 1.8 * org_cvr and ai_s > 1500
assert sep < aug and abs(sep_pd / aug_pd - 1) < 0.04, (sep_pd, aug_pd)
assert gsc_q3 > org_sessions * 1.06

pc = lambda x, d=1: f"{100 * x:+.{d}f}%"
p0 = lambda x, d=1: f"{100 * x:.{d}f}%"

agency = f"""# Hollowmere Running: organic search update, Q3 2026 (agency)

## Summary
- **Organic is stable.** Organic clicks were {tot['2026-09']:,} in September against {tot['2026-04']:,} in April ({pc(total_change)}). September dipped slightly from August ({aug:,}), nothing to worry about.
- **Visibility is growing.** Property impressions rose {pc(prop_imps_change, 0)} from Q2 to Q3.
- **Content is working.** Our new post {star} now ranks #2 (position 2.0) and is a model for Q4 posts.
- **AI assistants are not a channel for us yet.** A GA4 filter on session source (chat.openai.com, bard.google.com) found 0 sessions in Q3.
- Search Console clicks in Q3: {gsc_q3:,}. GA4 Organic Search sessions: {org_sessions:,}.

## Plan for Q4
Keep the current plan: technical maintenance, two link-building campaigns, and monthly reporting. No change to the content budget.
"""

notes = """# Notes
- Hollowmere Running sells running shoes and gear online. We ship to the United States and Canada only.
- gsc_queries_monthly.csv is filtered to United States and Canada and to queries with 150+ monthly clicks in April.
- gsc_country_device_quarterly.csv is the whole property, all countries.
"""

files = {
    "resources/notes.md": notes,
    "resources/agency_update_q3.md": agency,
    "resources/gsc_queries_monthly.csv": to_csv(["month", "query", "clicks", "impressions", "ctr", "position"], rows),
    "resources/gsc_country_device_quarterly.csv": to_csv(["country", "device", "quarter", "clicks", "impressions", "position"], cd_rows),
    "resources/gsc_pages_first_impression.csv": to_csv(["page", "first_impression_month", "clicks_q3", "impressions_q3", "position_q3"], pg_rows),
    "resources/ga4_referrals_q3.csv": to_csv(["session_source", "session_medium", "sessions", "engaged_sessions", "purchases", "purchase_revenue"], ref_rows),
    "resources/ga4_channels_q3.csv": to_csv(["session_default_channel_group", "sessions", "engaged_sessions", "purchases", "purchase_revenue"], ch_rows),
}

prompt = """
I'm presenting our organic search results to the CMO tomorrow, using our agency's Q3 update (resources/agency_update_q3.md) plus the Search Console and GA4 exports in resources/. Anything I'm missing, and what should I tell her we do in Q4? Please put it in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Brand rise hides a non-brand fall. Total clicks moved {pc(total_change)} April to September, but brand queries (containing "hollowmere") rose {pc(b_change, 0)} while non-brand queries fell {pc(n_change, 0)} (Q2 to Q3: non-brand {nb_q2:,} to {nb_q3:,}). Counts as found if report.md splits brand and non-brand and states the non-brand decline (about 20-30% either monthly or about {abs(nb_q3 / nb_q2 - 1) * 100:.0f}% quarterly).
2. Impressions growth from countries Hollowmere does not ship to. Property impressions {pc(prop_imps_change, 0)} Q2 to Q3, but United States and Canada impressions changed {pc(served_change)}; the growth ({unserved_add:,} extra impressions) is India, Philippines, UK and Australia at positions 21-37 with CTR under 1%. Counts as found if report.md says the visibility growth is in unserved markets (or that served-market impressions did not grow).
3. New-page pipeline run dry. Pages earning their first impressions per month: {', '.join(str(new_counts[m]) for m in MONTHS)} (April to September). Counts as found if report.md notes the count falling to zero / no new pages earning impressions, i.e. clicks are held up by old pages.
4. AI-assistant traffic is not zero. The filter used old referrer names; GA4 shows chatgpt.com, perplexity.ai, gemini.google.com and copilot.microsoft.com with {ai_s:,} sessions, {ai_p} purchases, conversion rate about {p0(ai_cvr)} against Organic Search about {p0(org_p / org_sessions)}. Counts as found if report.md says the AI referral figure is wrong because of the filter (outdated domains) and gives the real sessions or conversion.
5. "Ranks #2" on tiny volume. {star} has position 2.0 on 38 impressions and 3 clicks in Q3; average position on so few impressions is noise, not a rank. Counts as found if report.md questions the "#2" claim because of the low impressions.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence (a number or named row).
FAIL if fewer than 3.
"""

g_decision = f"""
The correct main message for the CMO: organic is not stable where it matters. Non-brand clicks, the part that acquires new customers, fell about {abs(n_change) * 100:.0f}% April to September, masked by brand growth, and no new pages are earning impressions. The Q4 recommendation should therefore change the plan toward non-brand growth (restart or fund new content / non-brand pages, investigate the non-brand ranking losses), not "keep the current plan".

The naive message is the agency's: "organic is stable, visibility growing, keep the plan / link building".

PASS if report.md's headline or main recommendation says the non-brand (or new-customer) part of organic is declining and recommends changing the Q4 plan to address it (content pipeline, non-brand pages, ranking recovery or similar).
FAIL if report.md endorses "stable, keep the current plan", or leads with something else (for example AI traffic or link building) without stating the non-brand decline as the main issue.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Search Console clicks ({gsc_q3:,} in Q3) above GA4 Organic Search sessions ({org_sessions:,}). Different systems; a gap under about 10% is normal.
- D2. September clicks ({sep:,}) a little below August ({aug:,}). September has 30 days and August 31; per day they are about {sep_pd:,.0f} vs {aug_pd:,.0f}, essentially flat. (The non-brand decline is a separate, real issue; D2 is only about the month-on-month dip.)

PASS if report.md does not call the clicks-vs-sessions gap lost traffic or a tracking issue to fix, and does not treat the August-to-September total dip by itself as a new drop. Mentioning either as normal is fine.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: total {total_change:+.3f} brand {b_change:+.3f} nonbrand {n_change:+.3f}; imps prop {prop_imps_change:+.3f} served {served_change:+.3f}; "
      f"new pages {list(new_counts.values())}; ai {ai_s} sess cvr {ai_cvr:.3f} vs org {org_p / org_sessions:.3f}; aug/sep per day {aug_pd:.0f}/{sep_pd:.0f}")
