"""Breadth: a "record September" GA4 report before it goes to the CMO
(Thistle & Pine Outfitters, Jul-Sep 2026).

Planted problems (5): session timeout cut from 30 to 5 minutes on 18 Aug, so
sessions jump while users stay flat and engagement rate falls (DECISION, with
#2); purchase events double-fire from the 31 Aug theme release, so GA4
purchases run above store orders; the ESP changed utm_medium from "email" to
"newsletter" on 1 Sep, so email revenue moved to Unassigned and the report
calls email down; the Direct jump lines up with the QR-code catalogue mailed
7 Sep (untagged), read as brand strength; the "top content" ranking by views
crowns a post with ~8 views per user over one with far more readers.
Decoys (2): GA4 revenue a few percent under store revenue in July (before the
theme release); (not set) landing page under 1% of sessions."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-ga4-record-month"
rng = random.Random(81404)
AOV = 96.0

# ---------- weekly GA4 vs store ----------
weeks = [dt.date(2026, 7, 6) + dt.timedelta(days=7 * i) for i in range(13)]  # to 28 Sep
TIMEOUT = dt.date(2026, 8, 17)   # week containing 18 Aug
DUP = dt.date(2026, 8, 31)
CAT = dt.date(2026, 9, 7)
wk = []
for w in weeks:
    users = int(rng.gauss(30500, 500) * (1.04 if w >= CAT else 1.0))
    spu = rng.uniform(1.27, 1.31) * (1.36 if w >= TIMEOUT else 1.0)
    sessions = int(users * spu)
    er = rng.uniform(0.62, 0.65) * (0.84 if w >= TIMEOUT else 1.0)
    eng = int(sessions * er)
    orders = int(users * rng.uniform(0.0205, 0.0215))
    store_rev = round(orders * AOV * rng.uniform(0.98, 1.02), 2)
    track = rng.uniform(0.94, 0.965)
    ga_p = int(orders * track * (1.31 if w >= DUP else 1.0))
    ga_rev = round(store_rev * track * (1.31 if w >= DUP else 1.0), 2)
    wk.append([w.isoformat(), users, sessions, eng, ga_p, ga_rev, orders, store_rev])

def mon(m):
    return [r for r in wk if r[0][5:7] == m]
def tot(rows, i):
    return sum(r[i] for r in rows)
jul, sep = mon("07"), mon("09")
# per-week averages (months have different numbers of weeks)
avg = lambda rows, i: tot(rows, i) / len(rows)
sess_ch = avg(sep, 2) / avg(jul, 2) - 1
users_ch = avg(sep, 1) / avg(jul, 1) - 1
garev_ch = avg(sep, 5) / avg(jul, 5) - 1
store_ch = avg(sep, 7) / avg(jul, 7) - 1
er_jul = tot(jul, 3) / tot(jul, 2); er_sep = tot(sep, 3) / tot(sep, 2)
jul_gap = 1 - tot(jul, 5) / tot(jul, 7)
sep_ratio = tot(sep, 4) / tot(sep, 6)

# ---------- monthly source / medium ----------
def sm_rows(month, n_weeks, after_medium_change, after_catalogue):
    base = [
        ("google", "organic", 0.30, 1.0), ("(direct)", "(none)", 0.14, 1.1), ("google", "cpc", 0.17, 1.3),
        ("ristretto_esp", "email", 0.09, 1.9), ("facebook", "paid_social", 0.12, 0.7), ("instagram", "referral", 0.05, 0.5),
        ("bing", "organic", 0.03, 1.0), ("trailtalk.net", "referral", 0.02, 0.9), ("pinterest", "referral", 0.02, 0.4),
    ]
    out = []
    S = sum(r[2] for r in wk if r[0][5:7] == month[5:7])
    R = sum(r[5] for r in wk if r[0][5:7] == month[5:7])
    wsum = sum(sh * rp for _, _, sh, rp in base)
    for src, med, share, rpv in base:
        s = int(S * share * rng.uniform(0.97, 1.03))
        if src == "(direct)" and after_catalogue:
            s = int(s * 1.42)
        CH = {"organic": "Organic Search", "(none)": "Direct", "cpc": "Paid Search", "email": "Email", "paid_social": "Paid Social",
              "referral": "Referral", "newsletter": "Unassigned"}
        if med == "email" and after_medium_change:
            s_flow = int(s * 0.25)   # automated flows keep utm_medium=email; campaigns switched to newsletter
            r_all = R * share * rpv / wsum * rng.uniform(0.95, 1.05)
            for mm, ss in (("email", s_flow), ("newsletter", s - s_flow)):
                out.append([month, src, mm, CH[mm], ss, round(r_all * ss / s, 2)])
            continue
        rev = round(R * share * rpv / wsum * rng.uniform(0.95, 1.05), 2)
        out.append([month, src, med, CH[med], s, rev])
    return out
sm = sm_rows("2026-07", 4, False, False) + sm_rows("2026-08", 5, False, False) + sm_rows("2026-09", 4, True, True)
def ch_val(month, ch, i=5):
    return sum(r[i] for r in sm if r[0] == month and r[3] == ch)
email_jul = ch_val("2026-07", "Email"); email_sep_report = ch_val("2026-09", "Email")
unassigned_sep = ch_val("2026-09", "Unassigned")
sep_rev_total = sum(r[5] for r in sm if r[0] == "2026-09")
direct_jul_pw = ch_val("2026-07", "Direct", 4) / 4; direct_sep_pw = ch_val("2026-09", "Direct", 4) / 4
direct_share_jul = ch_val("2026-07", "Direct", 4) / sum(r[4] for r in sm if r[0] == "2026-07")
direct_share_sep = ch_val("2026-09", "Direct", 4) / sum(r[4] for r in sm if r[0] == "2026-09")

# ---------- landing pages incl (not set) ----------
lp = [["/", 61000], ["/collections/jackets", 22100], ["/collections/base-layers", 15800], ["/blog/winter-layering-guide", 9300],
      ["/blog/how-to-wax-a-jacket", 8800], ["/products/ridge-down-jacket", 7100], ["(not set)", 0]]
lp_total = int(sum(x[1] for x in lp) / 0.9)
lp.append(["(other)", lp_total - sum(x[1] for x in lp)])
lp[6][1] = int(lp_total * 0.0055)
notset_share = lp[6][1] / lp_total

# ---------- blog page views, September ----------
blog = [["/blog/winter-layering-guide", 18400, 2150], ["/blog/how-to-wax-a-jacket", 9100, 7900], ["/blog/best-hiking-socks", 6200, 5300],
        ["/blog/packing-list-weekend-hike", 5100, 4400], ["/blog/down-vs-synthetic", 4300, 3800]]
blog_rows = [[p, int(v * rng.uniform(0.98, 1.02)), int(u * rng.uniform(0.98, 1.02))] for p, v, u in blog]
top_v = max(blog_rows, key=lambda r: r[1]); top_u = max(blog_rows, key=lambda r: r[2])

changes = [
    ["2026-06-02", "Data stream", "Enhanced measurement: file downloads enabled", "j.ortega"],
    ["2026-07-21", "Property access", "User added: agency@northfold.example (Viewer)", "j.ortega"],
    ["2026-08-18", "Data stream", "Tag settings: session timeout changed from 30 min to 5 min", "web-dev"],
    ["2026-08-31", "Site release", "Theme 4.2 released (new order confirmation page)", "web-dev"],
    ["2026-09-03", "Property", "Audience created: cart abandoners 7d", "m.chan"],
]

# ---------- asserts ----------
assert sess_ch > 0.30 and abs(users_ch) < 0.06, (sess_ch, users_ch)
assert garev_ch > 0.25 and store_ch < 0.08, (garev_ch, store_ch)
assert er_sep < er_jul - 0.07
assert 0.03 < jul_gap < 0.07 and sep_ratio > 1.15, (jul_gap, sep_ratio)
assert email_sep_report < 0.4 * email_jul and unassigned_sep > 0.12 * sep_rev_total * 0.5
assert direct_sep_pw / direct_jul_pw > 1.3 and direct_share_sep > direct_share_jul + 0.03
assert top_v[0] != top_u[0] and top_v[1] / top_v[2] > 6
assert notset_share < 0.01

pc = lambda x, d=0: f"{100 * x:+.{d}f}%"
p0 = lambda x, d=1: f"{100 * x:.{d}f}%"
usd = lambda x: f"${x:,.0f}"

report = f"""# Thistle & Pine: September web performance (draft for the CMO)

## Our best month ever
- **Sessions per week up {pc(sess_ch)} vs July.** The new content plan is working.
- **GA4 revenue per week up {pc(garev_ch)} vs July.**
- Engagement rate slipped from {p0(er_jul)} to {p0(er_sep)}; we will review content quality.
- **Direct traffic up {pc(direct_sep_pw / direct_jul_pw - 1)} per week**: brand awareness is building.
- **Email revenue fell from {usd(email_jul)} in July to {usd(email_sep_report)} in September** in the channel report. We propose cutting email frequency to once a week and moving the saving to paid social.
- Top content in September: /blog/winter-layering-guide ({top_v[1]:,} views).

## Proposal
Raise Q4 targets by 25% on sessions and revenue, based on September's run rate.
"""

notes = f"""# Notes
- Thistle & Pine Outfitters sells outdoor clothing online.
- Our Autumn catalogue was mailed to 60,000 past customers on 7 September (it has QR codes to the site).
- Exports: GA4 weekly totals with store orders, GA4 traffic by source/medium per month, landing pages, September blog page views, and the GA4/site change history.
"""

files = {
    "resources/notes.md": notes,
    "resources/september_report_draft.md": report,
    "resources/ga4_weekly_with_store_orders.csv": to_csv(["week_start", "total_users", "sessions", "engaged_sessions", "purchases", "purchase_revenue", "store_orders", "store_revenue"], wk),
    "resources/ga4_source_medium_monthly.csv": to_csv(["month", "session_source", "session_medium", "session_default_channel_group", "sessions", "purchase_revenue"], sm),
    "resources/ga4_landing_pages_q3.csv": to_csv(["landing_page", "sessions"], lp),
    "resources/ga4_blog_pages_sep.csv": to_csv(["page_path", "views", "total_users"], blog_rows),
    "resources/change_history.csv": to_csv(["date", "area", "change", "changed_by"], changes),
}

prompt = """
Our analyst drafted the September web performance report for the CMO (resources/september_report_draft.md), with the GA4 and store exports behind it in resources/. I'm presenting it tomorrow. Is there anything I'm missing, and should we go ahead with the proposals in it? Please write your view in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Session timeout change. change_history.csv shows the session timeout cut from 30 to 5 minutes on 2026-08-18. From that week sessions per user jump (sessions per week {pc(sess_ch)} Sep vs Jul) while users change only {pc(users_ch, 1)}, and engagement rate falls ({p0(er_jul)} to {p0(er_sep)}) because the same visits are split into more, shorter sessions. Counts as found if report.md ties the sessions jump (or the engagement drop) to the timeout setting, or says users are flat so the sessions growth is not real.
2. Duplicate purchase events. From the week of 2026-08-31 (theme release) GA4 purchases exceed store orders (September GA4 purchases / store orders = {sep_ratio:.2f}); store revenue per week moved only {pc(store_ch, 1)} vs July against {pc(garev_ch)} in GA4. Counts as found if report.md says GA4 purchases or revenue run above the store (double counting / duplicate firing) since the release.
3. Email moved to Unassigned. From September the ESP rows carry utm_medium "newsletter", which GA4's default grouping puts in Unassigned ({usd(unassigned_sep)} in September), so the Email channel shows only {usd(email_sep_report)} (automated flows still tagged "email"). Counts as found if report.md says email revenue did not disappear but is under "newsletter"/Unassigned.
4. Direct jump is the untagged catalogue. Direct sessions per week rose about {pc(direct_sep_pw / direct_jul_pw - 1)} and Direct's share of sessions from {p0(direct_share_jul)} to {p0(direct_share_sep)} after the catalogue mailing on 7 September, whose QR codes are evidently not tagged; it is not brand awareness. Counts as found if report.md links the Direct rise to the catalogue/QR codes.
5. Top content by views. /blog/winter-layering-guide has {top_v[1]:,} views from {top_v[2]:,} users (about {top_v[1] / top_v[2]:.1f} views per user); {top_u[0]} reaches {top_u[2]:,} users. Counts as found if report.md says the ranking should use users (or that the views are inflated by repeat views) and names the other post as reaching more people.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence (a number, date or row).
FAIL if fewer than 3.
"""

g_decision = f"""
The correct verdict: September was not a record month. Users per week moved {pc(users_ch, 1)} and store revenue per week {pc(store_ch, 1)} vs July; the session and GA4 revenue growth comes from the session-timeout change and duplicate purchase events. So: do not raise Q4 targets by 25% on this basis (restore the timeout / fix purchase de-duplication, and set targets on users and store orders), and do not cut email frequency, because email revenue moved to Unassigned rather than falling.

Naive answer: present the month as a record and approve the proposals (25% higher targets; and/or cut email to fund paid social).

PASS if report.md recommends against raising targets on September's numbers because the growth is (mostly) a measurement artefact (timeout and/or duplicate purchases, or users and store revenue being roughly flat).
FAIL if report.md endorses the 25% target increase or presents September as a genuine record month. (Also FAIL if it endorses cutting email frequency on the basis of the channel report.)
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. In July (before the theme release) GA4 revenue is about {p0(jul_gap)} under store revenue. A gap of a few percent is normal (blockers, consent). Only the reversal after 31 August is a problem.
- D2. The (not set) landing page is {p0(notset_share, 2)} of Q3 sessions; under 1% is normal.

PASS if report.md does not present the July GA4-vs-store shortfall as a tracking problem to fix and does not flag the (not set) landing page share. Mentioning them as normal is fine.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: sessions {sess_ch:+.3f} users {users_ch:+.3f}; GA rev {garev_ch:+.3f} store {store_ch:+.3f}; ER {er_jul:.3f}->{er_sep:.3f}; "
      f"jul gap {jul_gap:.3f} sep ratio {sep_ratio:.2f}; unassigned sep {unassigned_sep:,.0f}; direct x{direct_sep_pw / direct_jul_pw:.2f}")
