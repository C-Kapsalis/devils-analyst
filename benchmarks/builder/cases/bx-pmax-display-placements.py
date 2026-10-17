"""Breadth benchmark, display: where should next quarter's display budget go (Quillmark Stationery, Q3 2026).

Subtle problems (4): five open-web placements with CPM around EUR 0.3, over half
of Open Audience impressions, viewable rate under 20% and zero sessions
(made-for-advertising / invalid traffic pattern); mobile-app game placements
with CTR ~5% but almost no sessions per click (accidental clicks); Open
Audience's cheap CPM reverses once engaged sessions are used: Custom Intent
is cheapest per engaged session (Open Audience's CPM is cheap because of the
MFA and app inventory)
(DECISION); remarketing list with no frequency cap and no purchaser exclusion,
running at ~15 impressions per user per week.
Decoys (2): display CTR around 0.4% on the prospecting campaigns; Google Ads
clicks a few percent above GA4 sessions on normal website placements."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-pmax-display-placements"
rng = random.Random(77812)

# placements: campaign -> list of (placement, type, impressions, cpm, viewable rate, ctr, sessions per click, engaged share)
OA, CI, AF, RM = "Display - Open Audience", "Display - Custom Intent", "Display - Affinity Stationery Lovers", "Display - Remarketing 30d"
PL = {
    OA: [
        ("dailyquizhub.net", "website", 520000, 0.28, 0.14, 0.0021, 0.0, 0.0),
        ("top10-listicles.co", "website", 470000, 0.31, 0.17, 0.0019, 0.0, 0.0),
        ("viralnewsfeed.site", "website", 410000, 0.26, 0.12, 0.0024, 0.0, 0.0),
        ("recipes-daily-best.com", "website", 360000, 0.33, 0.19, 0.0018, 0.0, 0.0),
        ("celebgossiphub.info", "website", 300000, 0.30, 0.16, 0.0022, 0.0, 0.0),
        ("mobileapp::Block Puzzle Blast", "mobile_app", 420000, 1.10, 0.62, 0.051, 0.07, 0.10),
        ("mobileapp::Word Crush Daily", "mobile_app", 380000, 1.05, 0.60, 0.048, 0.09, 0.12),
        ("dailystylenews.com", "website", 260000, 2.60, 0.58, 0.0030, 0.95, 0.34),
        ("homeofficejournal.com", "website", 240000, 2.90, 0.61, 0.0031, 0.94, 0.38),
        ("craftandpaper.blog", "website", 210000, 2.70, 0.60, 0.0032, 0.95, 0.36),
    ],
    CI: [
        ("plannercommunity.com", "website", 180000, 4.30, 0.74, 0.0044, 0.95, 0.63),
        ("fountainpennetwork.org", "website", 150000, 4.60, 0.76, 0.0049, 0.96, 0.66),
        ("studytips-hq.com", "website", 140000, 3.90, 0.71, 0.0039, 0.94, 0.58),
        ("bulletjournal-ideas.com", "website", 160000, 4.10, 0.73, 0.0042, 0.95, 0.62),
        ("officesupplyreviews.net", "website", 120000, 4.40, 0.72, 0.0040, 0.95, 0.60),
    ],
    AF: [
        ("lifestylemag-online.com", "website", 260000, 2.80, 0.62, 0.0031, 0.94, 0.44),
        ("weekendreads.co", "website", 230000, 2.60, 0.60, 0.0029, 0.95, 0.42),
        ("giftguide-central.com", "website", 210000, 3.00, 0.64, 0.0034, 0.95, 0.47),
        ("youtube.com", "youtube", 300000, 3.40, 0.58, 0.0022, 0.92, 0.40),
    ],
    RM: [
        ("youtube.com", "youtube", 210000, 6.10, 0.66, 0.0060, 0.94, 0.55),
        ("newsportal-uk.com", "website", 260000, 5.80, 0.70, 0.0078, 0.96, 0.57),
        ("homeofficejournal.com", "website", 190000, 6.00, 0.71, 0.0081, 0.95, 0.60),
        ("plannercommunity.com", "website", 140000, 6.40, 0.73, 0.0085, 0.96, 0.62),
    ],
}
pl_rows = []
for camp, pls in PL.items():
    for name, typ, imps0, cpm, vr, ctr, spc, eng in pls:
        imps = int(imps0 * rng.uniform(0.96, 1.04))
        cost = round(imps * cpm / 1000 * rng.uniform(0.97, 1.03), 2)
        viewable = int(imps * vr * rng.uniform(0.97, 1.03))
        clicks = int(round(imps * ctr * rng.uniform(0.93, 1.07)))
        sess = int(round(clicks * spc * rng.uniform(0.97, 1.0)))
        engs = int(round(sess * eng * rng.uniform(0.95, 1.05)))
        pl_rows.append([camp, name, typ, imps, viewable, clicks, cost, sess, engs])

# campaign weekly reach/frequency for remarketing
freq_rows = []
for w, wk in enumerate(["2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21"]):
    reach = int(rng.uniform(13800, 14600)); f = round(rng.uniform(14.2, 16.4), 1)
    freq_rows.append([wk, RM, reach, int(reach * f), f])
lists = [
    ["All visitors 30d", RM, 30, "no", "none", 41200],
    ["Purchasers 540d", "(not used as exclusion)", 540, "n/a", "n/a", 9800],
    ["Newsletter subscribers", "(not used)", 0, "n/a", "n/a", 22300],
]

# ---------- ground truth ----------
def agg(camp, f=lambda r: True):
    rr = [r for r in pl_rows if r[0] == camp and f(r)]
    return [sum(r[i] for r in rr) for i in range(3, 9)]  # imps, viewable, clicks, cost, sess, engaged
mfa = lambda r: r[2] == "website" and r[6] / r[3] * 1000 < 0.5
app = lambda r: r[2] == "mobile_app"
oa = agg(OA); mfa_t = agg(OA, mfa); app_t = agg(OA, app)
mfa_imp_share = mfa_t[0] / oa[0]; mfa_vr = mfa_t[1] / mfa_t[0]
app_ctr = app_t[2] / app_t[0]; app_spc = app_t[4] / app_t[2]
web = lambda r: r[2] == "website" and not mfa(r)
prosp = [OA, CI, AF]
m = {c: agg(c) for c in [OA, CI, AF, RM]}
cpm = {c: m[c][3] / m[c][0] * 1000 for c in m}
vcpm = {c: m[c][3] / m[c][1] * 1000 for c in m}
c_eng = {c: m[c][3] / m[c][5] for c in m}
ctr = {c: m[c][2] / m[c][0] for c in m}
ctr_ci_af = (m[CI][2] + m[AF][2]) / (m[CI][0] + m[AF][0])
w_all = [r for r in pl_rows if web(r)]
sess_gap = 1 - sum(r[7] for r in w_all) / sum(r[5] for r in w_all)
avg_f = sum(r[4] for r in freq_rows) / len(freq_rows)

assert 0.45 < mfa_imp_share < 0.65 and mfa_vr < 0.2 and mfa_t[4] == 0
assert app_ctr > 0.04 and app_spc < 0.1
assert cpm[OA] == min(cpm[c] for c in prosp) and c_eng[CI] == min(c_eng[c] for c in prosp)
assert c_eng[OA] > 1.8 * c_eng[CI]
assert 0.003 < ctr_ci_af < 0.005 and 0.02 < sess_gap < 0.08 and avg_f > 14

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x, d=0: f"€{x:,.{d}f}"

camp_rows = []
for c in m:
    i, v, cl, co, s, e = m[c]
    camp_rows.append(["2026-Q3", c, "prospecting" if c != RM else "remarketing", i, v, cl, round(co, 2)])
notes = f"""# Quillmark Stationery: display Q3 2026 (agency)

- Open Audience is our most efficient reach: CPM {eur(cpm[OA], 2)} vs {eur(cpm[CI], 2)} on Custom Intent.
- Q4 plan: move half of the Custom Intent and Affinity budget into Open Audience to maximise reach for the gifting season.
- Remarketing keeps converting; we'll keep it as is.
"""

files = {
    "resources/agency_display_q3.md": notes,
    "resources/display_campaigns_q3.csv": to_csv(["quarter", "campaign", "role", "impressions", "viewable_impressions", "clicks", "cost"], camp_rows),
    "resources/display_placements_q3.csv": to_csv(
        ["campaign", "placement", "placement_type", "impressions", "viewable_impressions", "clicks", "cost", "ga4_sessions", "ga4_engaged_sessions"], pl_rows),
    "resources/remarketing_weekly_sep2026.csv": to_csv(["week_start", "campaign", "unique_users", "impressions", "avg_frequency"], freq_rows),
    "resources/audience_lists.csv": to_csv(["list_name", "used_in", "membership_days", "excludes_purchasers", "frequency_cap", "list_size"], lists),
}

prompt = """
I'm the marketing lead at Quillmark Stationery. Our agency wants to change the display mix for Q4 (gifting season is our big quarter). Their note and the Q3 Google Ads display exports are in resources/. Where should next quarter's display budget go? Write report.md with the numbers behind your answer.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Made-for-advertising / invalid-traffic placements. Five Open Audience websites (dailyquizhub.net, top10-listicles.co, viralnewsfeed.site, recipes-daily-best.com, celebgossiphub.info) have CPMs around €0.26-0.33, carry {pc(mfa_imp_share)} of Open Audience impressions, a viewable rate of {pc(mfa_vr)}, and zero GA4 sessions. Found if report.md flags these placements (as low-quality / MFA / invalid / to exclude) with evidence.
2. Accidental app clicks. The two mobile-app game placements have CTR {pc(app_ctr, 1)} (vs about 0.4% elsewhere) but only {app_spc:.2f} sessions per click. Found if report.md flags the app placements as accidental/low-quality clicks.
3. Cheap CPM is not cheap results. Open Audience CPM {eur(cpm[OA], 2)} vs Custom Intent {eur(cpm[CI], 2)}, but the low CPM comes from the MFA and app inventory; cost per engaged session is {eur(c_eng[OA], 2)} for Open Audience vs {eur(c_eng[CI], 2)} for Custom Intent ({eur(c_eng[AF], 2)} Affinity). Found if report.md compares cost per session or engaged session (or a quality-adjusted cost) and shows Open Audience is not the efficient option.
4. Remarketing settings. "All visitors 30d" has no frequency cap and does not exclude purchasers; September frequency averaged {avg_f:.1f} impressions per user per week. Found if report.md flags the missing cap/high frequency or the missing purchaser exclusion.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: do not move budget into Open Audience. Shift prospecting budget toward Custom Intent (lowest cost per engaged session, {eur(c_eng[CI], 2)} vs {eur(c_eng[OA], 2)} for Open Audience), and exclude the MFA sites and app placements from Open Audience (or cut Open Audience).

Naive wrong answer: follow the agency and move budget into Open Audience because of its lowest CPM ({eur(cpm[OA], 2)}).

PASS if report.md's main recommendation rejects moving budget into Open Audience and directs prospecting budget to Custom Intent (alone or as the main destination; Custom Intent plus Affinity with Custom Intent first is fine).
FAIL if it endorses shifting budget to Open Audience, recommends a mix led by Open Audience, or makes moving budget into Remarketing its main action (remarketing recaptures existing visitors; it is not prospecting reach).
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Display CTR around {pc(ctr_ci_af, 2)} on Custom Intent and Affinity. Normal for display (a reach channel); it is not a reason to cut. (Flagging the ~5% CTR on the app placements is correct and separate.)
- D2. On normal website placements, Google Ads clicks are about {pc(sess_gap, 1)} above GA4 sessions. Normal (blockers, consent, bounces before the tag fires).

PASS if report.md does not call the ~0.4% display CTR weak or a reason to cut, and does not treat the few-percent click-to-session gap on normal sites as a tracking problem.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: mfa share {mfa_imp_share:.2f} vr {mfa_vr:.2f}; app ctr {app_ctr:.3f} spc {app_spc:.2f}; cpm OA {cpm[OA]:.2f} CI {cpm[CI]:.2f}; "
      f"vcpm OA {vcpm[OA]:.2f} CI {vcpm[CI]:.2f} AF {vcpm[AF]:.2f}; c/eng OA {c_eng[OA]:.2f} CI {c_eng[CI]:.2f} AF {c_eng[AF]:.2f}; freq {avg_f:.1f}")
