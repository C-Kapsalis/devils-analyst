"""Audit a GA4 property and its UTM tagging (Orchard Row Apparel, September 2026).

Planted problems (7): data retention left at 2 months while the team plans a
12-month funnel exploration (MUST); data-driven attribution selected while the
purchase outcome is split over two key events, each under ~400 a month (MUST);
scroll marked as a key event on 2026-08-12, stepping engagement rate up (MUST);
four spellings of the autumn_sale campaign key; utm_medium=facebook with
utm_source=paid_social; display spend with almost no display sessions while
Direct jumps the same weeks; site search off on a catalogue site.
Decoys (2): (not set) campaign under 1% of sessions; google / cpc sessions a few
percent under Google Ads clicks."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "audit-ga4-utm"
rng = random.Random(55129)
DDA_MIN = 400

# ---------- admin settings ----------
settings = [
    ["property_name", "Orchard Row Apparel - Web"],
    ["industry_category", "Apparel"],
    ["reporting_time_zone", "America/New_York"],
    ["currency", "USD"],
    ["data_retention_event_data", "2 months"],
    ["reset_user_data_on_new_activity", "on"],
    ["reporting_attribution_model", "Data-driven"],
    ["key_event_lookback_window_acquisition", "30 days"],
    ["key_event_lookback_window_other", "90 days"],
    ["google_signals", "on"],
    ["enhanced_measurement_page_views", "on"],
    ["enhanced_measurement_scrolls", "on"],
    ["enhanced_measurement_outbound_clicks", "on"],
    ["enhanced_measurement_site_search", "off"],
    ["enhanced_measurement_video_engagement", "on"],
    ["enhanced_measurement_file_downloads", "on"],
    ["google_ads_link", "linked"],
]

# ---------- key events ----------
p_web = rng.randint(232, 262)
p_app = rng.randint(171, 199)
key_rows = [
    ["purchase", "TRUE", p_web, "2023-04-18"],
    ["purchase_app_checkout", "TRUE", p_app, "2025-11-03"],
    ["sign_up", "TRUE", rng.randint(610, 690), "2023-04-18"],
    ["scroll", "TRUE", rng.randint(38000, 44000), "2026-08-12"],
    ["add_to_cart", "FALSE", rng.randint(2900, 3300), ""],
    ["begin_checkout", "FALSE", rng.randint(1150, 1300), ""],
    ["file_download", "FALSE", rng.randint(300, 420), ""],
]
p_sum = p_web + p_app

# ---------- engagement daily (step on 2026-08-12) ----------
eng_rows, before, after = [], [], []
for i in range(28):
    day = 29 + i  # July 29 .. Aug 25
    date = f"2026-07-{day:02d}" if day <= 31 else f"2026-08-{day - 31:02d}"
    sessions = int(rng.gauss(3900, 260))
    rate = rng.uniform(0.50, 0.545) if date < "2026-08-12" else rng.uniform(0.70, 0.745)
    eng = int(round(sessions * rate))
    eng_rows.append([date, sessions, eng, round(eng / sessions, 4)])
    (before if date < "2026-08-12" else after).append((sessions, eng))
rate_before = sum(e for _, e in before) / sum(s for s, _ in before)
rate_after = sum(e for _, e in after) / sum(s for s, _ in after)

# ---------- traffic acquisition, September ----------
def row(src, med, camp, sessions, rpv):
    return [src, med, camp, sessions, round(sessions * rpv * rng.uniform(0.9, 1.1), 2)]
ta = [
    row("google", "organic", "(organic)", 41200, 1.35),
    row("(direct)", "(none)", "(direct)", 23900, 1.55),
    row("google", "cpc", "brand_search", 9100, 2.4),
    row("google", "cpc", "generic_search", 14800, 1.1),
    row("newsletter", "email", "autumn_sale", 6100, 2.9),
    row("newsletter", "email", "Autumn_Sale", 2300, 2.8),
    row("instagram", "paid_social", "autumn-sale", 4200, 1.2),
    row("facebook", "paid_social", "autumn sale ", 3100, 1.3),
    row("facebook", "paid_social", "prospecting_sep", 9800, 0.7),
    row("paid_social", "facebook", "prospecting_sep", 5600, 0.7),
    row("paid_social", "facebook", "retargeting_sep", 2900, 2.1),
    row("instagram", "referral", "(referral)", 3300, 0.6),
    row("bing", "organic", "(organic)", 2600, 1.3),
    row("pinterest", "referral", "(referral)", 1900, 0.5),
    row("google", "display", "autumn_display", 37, 0.0),
    row("newsletter", "email", "(not set)", 410, 1.0),
    row("(not set)", "(not set)", "(not set)", 260, 0.4),
]
ta_sessions = sum(r[3] for r in ta)
variants = [r for r in ta if r[2].strip().lower().replace("-", "_").replace(" ", "_") == "autumn_sale"]
var_sessions = sum(r[3] for r in variants)
var_rev = sum(r[4] for r in variants)
top_variant = max(variants, key=lambda r: r[4])
swap = [r for r in ta if r[1] == "facebook"]
swap_sessions, swap_rev = sum(r[3] for r in swap), sum(r[4] for r in swap)
notset = sum(r[3] for r in ta if r[2] == "(not set)")
notset_share = notset / ta_sessions
gcpc_sessions = sum(r[3] for r in ta if r[0] == "google" and r[1] == "cpc")
gads_clicks = int(round(gcpc_sessions / rng.uniform(0.935, 0.95)))

# ---------- weekly display spend vs sessions ----------
wk_rows = []
for w in range(8):
    start = ["2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21"][w]
    on = w >= 4
    spend = round(rng.uniform(2100, 2500), 2) if on else 0
    disp = rng.randint(6, 14) if on else 0
    direct = int(rng.gauss(4150, 120) + (rng.uniform(1500, 1800) if on else 0))
    total = int(rng.gauss(27500, 500) + (direct - 4150))
    wk_rows.append([start, spend, disp, direct, total])
d_before = sum(r[3] for r in wk_rows[:4]) / 4
d_after = sum(r[3] for r in wk_rows[4:]) / 4
disp_spend = sum(r[1] for r in wk_rows)
disp_sess = sum(r[2] for r in wk_rows)
direct_share_before = sum(r[3] for r in wk_rows[:4]) / sum(r[4] for r in wk_rows[:4])

# ---------- asserts ----------
assert p_web < DDA_MIN and p_app < DDA_MIN and p_sum > DDA_MIN, (p_web, p_app)
assert rate_after - rate_before > 0.15, (rate_before, rate_after)
assert len({r[2] for r in variants}) == 4 and var_rev > top_variant[4] * 1.8
assert swap_sessions > 0.05 * ta_sessions
assert disp_spend > 8000 and disp_sess < 60 and d_after / d_before > 1.3
assert notset_share < 0.01, notset_share
assert 0.92 < gcpc_sessions / gads_clicks < 0.96
assert 0.1 < direct_share_before < 0.2, direct_share_before

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

notes = f"""# Orchard Row Apparel: notes for the GA4 audit

- Online clothing shop (web and an app that opens the web checkout). Goal: purchases.
- Exports: GA4 admin settings, key events (last 30 days, to 30 September 2026), September traffic acquisition, daily engagement for late July to late August, weekly display spend with GA4 sessions.
- Google Ads clicks in September: {gads_clicks:,} (brand and generic search combined).
- What we use GA4 for: monthly channel budget split (we read the data-driven attribution report), and for Q4 planning the team wants to build a 12-month funnel exploration comparing this autumn with last autumn.
- The content team says August engagement went up because of the new lookbook pages.
- An Autumn Sale display flight ran from 31 August with the agency's own banner links.
"""

files = {
    "resources/account_notes.md": notes,
    "resources/ga4_admin_settings.csv": to_csv(["setting", "value"], settings),
    "resources/ga4_key_events_last30d.csv": to_csv(["event_name", "is_key_event", "event_count_30d", "marked_as_key_event_on"], key_rows),
    "resources/ga4_engagement_daily.csv": to_csv(["date", "sessions", "engaged_sessions", "engagement_rate"], eng_rows),
    "resources/ga4_traffic_acquisition_sep2026.csv": to_csv(
        ["session_source", "session_medium", "session_campaign", "sessions", "purchase_revenue"], ta),
    "resources/display_spend_vs_ga4_sessions_weekly.csv": to_csv(
        ["week_start", "display_spend", "ga4_google_display_sessions", "ga4_direct_sessions", "ga4_total_sessions"], wk_rows),
}

prompt = """
I've just joined Orchard Row Apparel as marketing manager and I don't fully trust our GA4 numbers. I've exported the settings and reports I could find into resources/, with some notes. Can you audit our GA4 setup and tagging, tell me what's wrong and what to fix first? Please write it up in report.md.
"""

g_recall = f"""
The GA4 exports contain 7 planted problems. Answer key:

1. Data retention at 2 months (data_retention_event_data = "2 months"). Explorations cannot look back further, so the planned 12-month funnel exploration comparing this autumn with last autumn is impossible; the maximum is 14 months and the change is not retroactive. Counts as found if report.md says retention must be raised to 14 months (or names the 2-month limit as blocking the year-over-year exploration).
2. Data-driven attribution on too little volume. reporting_attribution_model = Data-driven, but the purchase outcome is split into two key events, purchase ({p_web}) and purchase_app_checkout ({p_app}) in 30 days, each under the roughly 400-a-month level data-driven needs, while together they are {p_sum}. GA4 falls back to last click without notice, so the budget split read from the "data-driven" report is last click. Counts as found if report.md says the data-driven model is likely not active (falls back to last click) because purchase volume per key event is too low; noting the split into two events (consolidate into one) is the full answer, either point alone counts.
3. Scroll marked as a key event on 2026-08-12. Engagement rate steps from about {pc(rate_before, 0)} before that date to about {pc(rate_after, 0)} after it, because any session with a key event counts as engaged. The content team's claim that the lookbook pages raised engagement is not supported. Counts as found if report.md links the engagement jump to scroll becoming a key event (and recommends un-marking it or annotating the change).
4. Campaign key split over four spellings: autumn_sale, Autumn_Sale, autumn-sale, "autumn sale " ({var_sessions:,} sessions, {usd(var_rev)} revenue in total; the largest single spelling has only {usd(top_variant[4])}). Counts as found if report.md flags the inconsistent utm_campaign values and recommends one naming convention.
5. Source and medium swapped: rows with session_source = paid_social and session_medium = facebook ({swap_sessions:,} sessions, {usd(swap_rev)} revenue), which breaks default channel grouping (likely Unassigned). Counts as found if report.md flags the swapped utm_source / utm_medium.
6. Untagged display banners. Display spend of {usd(disp_spend)} over four weeks brought only {disp_sess} google / display sessions, while Direct sessions rose from about {d_before:,.0f} to about {d_after:,.0f} a week in the same weeks. Counts as found if report.md says the display traffic is probably landing in Direct because banner links are untagged (or that display cannot be judged until tagged).
7. Site search tracking off (enhanced_measurement_site_search = off) on a catalogue site; search terms are lost and cannot be backfilled. Counts as found if report.md recommends turning site search on.

List which ones were found in your reasoning.
PASS if report.md identifies at least 6 of the 7 problems, each with its substance (a vague mention such as "check your attribution settings" does not count).
FAIL if it identifies fewer than 6.
"""

g_rank = f"""
Three problems are Must-fix because they make later GA4 numbers wrong or unrecoverable:
- A. Data retention at 2 months (blocks the planned 12-month exploration; not retroactive).
- B. Data-driven attribution selected while purchase ({p_web}) and purchase_app_checkout ({p_app}) are each under about 400 a month, so the model in effect is last click.
- C. Scroll marked as a key event on 2026-08-12, inflating engagement rate from about {pc(rate_before, 0)} to about {pc(rate_after, 0)}.
The lesser problems are: the untagged display banners and site search being off. (The campaign-name spellings and the swapped source/medium may sit in either group.)

PASS if report.md flags all of A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND its closing "fix first" line (or explicit first priority) names A, B or C.
FAIL if any of A, B or C is missing, labelled lower severity (Should fix, Nice to have, minor), listed after one of the lesser problems, or if the first fix named is something other than A, B or C.
"""

g_decoy = f"""
The exports contain two things that are normal and must not be flagged as problems:
- D1. (not set) campaign rows total {notset:,} sessions, {pc(notset_share, 2)} of {ta_sessions:,} September sessions. A share under 1% is normal noise.
- D2. GA4 shows {gcpc_sessions:,} google / cpc sessions against {gads_clicks:,} Google Ads clicks ({pc(1 - gcpc_sessions / gads_clicks)} fewer). A gap of a few percent is expected (consent, blockers, early exits).

PASS if report.md does not present D1 or D2 as an error, a tracking loss or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it flags the (not set) share as a tagging problem to fix, or the click-to-session gap as lost tracking to investigate.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: purchase {p_web}+{p_app}={p_sum}; engagement {rate_before:.3f}->{rate_after:.3f}; autumn_sale variants {var_sessions} sessions {var_rev:,.0f}; "
      f"swap {swap_sessions} sessions; display spend {disp_spend:,.0f} sessions {disp_sess}, direct {d_before:,.0f}->{d_after:,.0f}; "
      f"not set {notset_share:.4f}; cpc/clicks {gcpc_sessions / gads_clicks:.3f}")
