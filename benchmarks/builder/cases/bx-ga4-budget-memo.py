"""Breadth: next quarter's budget from a GA4-based agency memo (Burrow & Bark Pet Supply, Q3 2026).

Planted problems (5): Meta ad URLs lost their UTMs from the week of 27 Jul,
so paid_social sessions collapse while l.facebook.com / m.facebook.com
referral sessions jump; GA4 "Meta ROAS" is understated (DECISION: do not move
Meta money on it); Google Ads ROAS is the platform's own claim while Meta is
GA4 last click (mixed sources); Google search blended ROAS hides non-brand
below break-even (margin 40% -> break-even ROAS 2.5); the memo treats any
ROAS above 1 as profitable; Microsoft Ads launched 10 Aug with no tagging, so
bing / cpc is empty while bing / organic jumps.
Decoys (2): retargeting ROAS far above prospecting; Direct steady around 15%."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-ga4-budget-memo"
rng = random.Random(81606)
MARGIN = 0.40
BE = 1 / MARGIN
weeks = [dt.date(2026, 6, 29) + dt.timedelta(days=7 * i) for i in range(13)]
BREAK = 4      # index of week 2026-07-27
MS = 6         # index of week 2026-08-10

# weekly spend
meta_p_spend = [round(rng.uniform(3300, 3700), 2) for _ in weeks]
meta_r_spend = [round(rng.uniform(1100, 1300), 2) for _ in weeks]
g_brand_spend = [round(rng.uniform(1300, 1500), 2) for _ in weeks]
g_gen_spend = [round(rng.uniform(5300, 5700), 2) for _ in weeks]
ms_spend = [0.0 if i < MS else round(rng.uniform(1150, 1300), 2) for i in range(13)]

rows = []
agg = {}
def add(i, src, med, camp, sess, rev):
    rows.append([weeks[i].isoformat(), src, med, camp, sess, round(rev, 2)])
    k = (src, med, camp)
    a = agg.setdefault(k, [0, 0.0]); a[0] += sess; a[1] += rev
meta_true = [0.0, 0.0]
for i in range(13):
    broken = i >= BREAK
    mp_s = int(meta_p_spend[i] / 0.62); mr_s = int(meta_r_spend[i] / 0.55)
    mp_rev = meta_p_spend[i] * rng.uniform(1.75, 1.95); mr_rev = meta_r_spend[i] * rng.uniform(5.6, 6.4)
    meta_true[0] += mp_rev + mr_rev
    if not broken:
        add(i, "facebook", "paid_social", "pros_q3_broad", mp_s, mp_rev)
        add(i, "facebook", "paid_social", "rtg_q3_7d", mr_s, mr_rev)
        add(i, "l.facebook.com", "referral", "(referral)", int(rng.uniform(300, 380)), rng.uniform(500, 700))
        add(i, "m.facebook.com", "referral", "(referral)", int(rng.uniform(250, 320)), rng.uniform(400, 600))
    else:
        add(i, "facebook", "paid_social", "pros_q3_broad", int(rng.uniform(15, 40)), rng.uniform(0, 90))
        add(i, "facebook", "paid_social", "rtg_q3_7d", int(rng.uniform(8, 25)), rng.uniform(0, 120))
        add(i, "l.facebook.com", "referral", "(referral)", int(rng.uniform(300, 380)) + int(mp_s * 0.55), rng.uniform(500, 700) + mp_rev * 0.55 + mr_rev * 0.5)
        add(i, "m.facebook.com", "referral", "(referral)", int(rng.uniform(250, 320)) + int(mp_s * 0.40) + mr_s, rng.uniform(400, 600) + mp_rev * 0.40 + mr_rev * 0.45)
    add(i, "google", "cpc", "brand_exact", int(g_brand_spend[i] / 0.35), g_brand_spend[i] * rng.uniform(16, 19))
    add(i, "google", "cpc", "generic_shopping_search", int(g_gen_spend[i] / 0.95), g_gen_spend[i] * rng.uniform(1.5, 1.75))
    add(i, "google", "organic", "(organic)", int(rng.gauss(14200, 300)), rng.uniform(31000, 34000))
    d_s = int(rng.gauss(7600, 150)); add(i, "(direct)", "(none)", "(direct)", d_s, rng.uniform(19000, 21000))
    b_org = int(rng.gauss(900, 40)) + (int(ms_spend[i] / 0.8) if i >= MS else 0)
    add(i, "bing", "organic", "(organic)", b_org, rng.uniform(1900, 2200) + (ms_spend[i] * rng.uniform(2.6, 3.0) if i >= MS else 0))
    add(i, "petpost_esp", "email", "weekly_letter", int(rng.gauss(3100, 120)), rng.uniform(9000, 10500))

S = lambda xs: sum(xs)
meta_spend = S(meta_p_spend) + S(meta_r_spend)
meta_ga4 = agg[("facebook", "paid_social", "pros_q3_broad")][1] + agg[("facebook", "paid_social", "rtg_q3_7d")][1]
meta_roas_ga4 = meta_ga4 / meta_spend
pre_spend = S(meta_p_spend[:BREAK]) + S(meta_r_spend[:BREAK])
pre_rev = sum(r[5] for r in rows if r[1] == "facebook" and r[0] < weeks[BREAK].isoformat())
meta_roas_pre = pre_rev / pre_spend
fb_ref_pre = sum(r[4] for r in rows if r[1] in ("l.facebook.com", "m.facebook.com") and r[0] < weeks[BREAK].isoformat()) / BREAK
fb_ref_post = sum(r[4] for r in rows if r[1] in ("l.facebook.com", "m.facebook.com") and r[0] >= weeks[BREAK].isoformat()) / (13 - BREAK)
brand_rev, gen_rev = agg[("google", "cpc", "brand_exact")][1], agg[("google", "cpc", "generic_shopping_search")][1]
brand_roas, gen_roas = brand_rev / S(g_brand_spend), gen_rev / S(g_gen_spend)
g_spend = S(g_brand_spend) + S(g_gen_spend)
g_blend_ga4 = (brand_rev + gen_rev) / g_spend
g_platform_value = (brand_rev + gen_rev) * 1.38      # platform claim, own window incl. view-through
g_roas_platform = g_platform_value / g_spend
ms_total = S(ms_spend)
bing_org_pre = sum(r[4] for r in rows if r[1] == "bing" and r[0] < weeks[MS].isoformat()) / MS
bing_org_post = sum(r[4] for r in rows if r[1] == "bing" and r[0] >= weeks[MS].isoformat()) / (13 - MS)
rtg_roas = agg[("facebook", "paid_social", "rtg_q3_7d")][1] / S(meta_r_spend)
pros_roas = agg[("facebook", "paid_social", "pros_q3_broad")][1] / S(meta_p_spend)
rtg_pre = sum(r[5] for r in rows if r[3] == "rtg_q3_7d" and r[0] < weeks[BREAK].isoformat()) / S(meta_r_spend[:BREAK])
pros_pre = sum(r[5] for r in rows if r[3] == "pros_q3_broad" and r[0] < weeks[BREAK].isoformat()) / S(meta_p_spend[:BREAK])
direct_share = [sum(r[4] for r in rows if r[0] == w.isoformat() and r[1] == "(direct)") / sum(r[4] for r in rows if r[0] == w.isoformat()) for w in weeks]

assert meta_roas_ga4 < 1.0 and meta_roas_pre > BE, (meta_roas_ga4, meta_roas_pre)
assert fb_ref_post > 4 * fb_ref_pre
assert gen_roas < BE < g_blend_ga4 and brand_roas > 12
assert g_roas_platform > g_blend_ga4 * 1.3
assert not any(r[1] == "bing" and r[2] == "cpc" for r in rows) and bing_org_post > 1.7 * bing_org_pre
assert rtg_pre > 2.5 * pros_pre
assert all(0.10 < x < 0.25 for x in direct_share) and max(direct_share) - min(direct_share) < 0.05

spend_rows = []
for i, w in enumerate(weeks):
    spend_rows += [[w.isoformat(), "meta", "pros_q3_broad", meta_p_spend[i]], [w.isoformat(), "meta", "rtg_q3_7d", meta_r_spend[i]],
                   [w.isoformat(), "google_ads", "brand_exact", g_brand_spend[i]], [w.isoformat(), "google_ads", "generic_shopping_search", g_gen_spend[i]]]
    if ms_spend[i]:
        spend_rows.append([w.isoformat(), "microsoft_ads", "generic_search_bing", ms_spend[i]])

usd = lambda x: f"${x:,.0f}"
memo = f"""# Q4 budget recommendation (agency memo)

Q3 return on ad spend, all figures from our reporting:

| Channel | Q3 spend | Revenue | ROAS | Source |
|---|---|---|---|---|
| Google Ads | {usd(g_spend)} | {usd(g_platform_value)} | {g_roas_platform:.1f} | Google Ads conversion value |
| Meta | {usd(meta_spend)} | {usd(meta_ga4)} | {meta_roas_ga4:.2f} | GA4, session source facebook / paid_social |
| Microsoft Ads | {usd(ms_total)} | $0 | 0.0 | GA4, bing / cpc |

Every channel above a ROAS of 1.0 pays for itself.

Recommendation for Q4:
1. Cut Meta prospecting and retargeting entirely; move the {usd(meta_spend)} to Google Ads, which returns {g_roas_platform:.1f}.
2. Stop Microsoft Ads (no revenue in GA4).
3. Organic Social (facebook.com referrals) has grown strongly since late July: add a part-time community manager.
"""

notes = f"""# Notes
- Burrow & Bark Pet Supply, online pet food and accessories. Gross margin about {MARGIN * 100:.0f}% of revenue.
- Q3 = 29 June to 27 September 2026. Spend from the ad platforms; sessions and revenue from GA4 (last click).
- Microsoft Ads campaigns started on 10 August.
"""

files = {
    "resources/notes.md": notes,
    "resources/agency_budget_memo_q4.md": memo,
    "resources/ad_spend_weekly_q3.csv": to_csv(["week_start", "platform", "campaign", "spend"], spend_rows),
    "resources/ga4_source_medium_weekly_q3.csv": to_csv(["week_start", "session_source", "session_medium", "session_campaign", "sessions", "purchase_revenue"], rows),
}

prompt = """
Our agency sent its Q4 budget recommendation (resources/agency_budget_memo_q4.md). I've exported our weekly ad spend and GA4 traffic for Q3 into resources/, plus some notes. Where should next quarter's budget go? Please write your recommendation in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Meta tracking broke from the week of {weeks[BREAK].isoformat()}. facebook / paid_social sessions fall to a few dozen a week while l.facebook.com and m.facebook.com referral sessions jump from about {fb_ref_pre:,.0f} to about {fb_ref_post:,.0f} a week, with Meta spend unchanged: the ads lost their UTMs. Before the break Meta's GA4 ROAS was about {meta_roas_pre:.1f}; the memo's {meta_roas_ga4:.2f} is a tagging artefact. Counts as found if report.md links the paid_social collapse to the facebook referral jump (UTMs lost) or says Meta's GA4 return is understated because of tracking.
2. Mixed sources. Google's {g_roas_platform:.1f} is the Google Ads platform's own conversion value; GA4 last click gives Google {g_blend_ga4:.1f}. Meta is measured in GA4. Counts as found if report.md says the channels are compared on different sources/attribution.
3. Brand hides non-brand. On GA4, brand_exact returns about {brand_roas:.1f} and generic_shopping_search about {gen_roas:.2f}, below the break-even ROAS of {BE:.1f} at {MARGIN * 100:.0f}% margin. Counts as found if report.md splits Google into brand and generic and says generic is below break-even (or the weakest line).
4. Wrong profitability line. With {MARGIN * 100:.0f}% gross margin, break-even ROAS is {BE:.1f}, not 1.0. Counts as found if report.md states the {BE:.1f} break-even (or that ROAS 1 loses money).
5. Microsoft Ads untagged. {usd(ms_total)} spent from 10 August; no bing / cpc rows exist, while bing / organic sessions rose from about {bing_org_pre:,.0f} to {bing_org_post:,.0f} a week. Counts as found if report.md says Microsoft Ads traffic is landing in bing / organic (untagged / auto-tagging off) rather than producing nothing.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct main recommendation: do not cut Meta and move its budget into Google on these numbers. Meta's GA4 figure is broken by lost UTMs (about {meta_roas_pre:.1f} ROAS before the break, above the {BE:.1f} break-even), and the extra Google money would go mostly to generic search at about {gen_roas:.2f}, below break-even. Fix the Meta (and Microsoft) tagging first; if anything is trimmed, it is generic search.

Naive answer: follow the memo, cut Meta (ROAS {meta_roas_ga4:.2f}) and move the {usd(meta_spend)} into Google Ads (ROAS {g_roas_platform:.1f}).

PASS if report.md's main recommendation keeps Meta (or holds the decision until tracking is fixed) and does not move Meta budget into Google generic search.
FAIL if report.md endorses cutting Meta and shifting its budget to Google, or recommends scaling Google generic search.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Meta retargeting ROAS (about {rtg_pre:.1f} before the tracking break) is far above prospecting (about {pros_pre:.1f}). That is expected; retargeting closes demand others created.
- D2. Direct is a steady {min(direct_share) * 100:.0f}-{max(direct_share) * 100:.0f}% of weekly sessions. That is normal.

PASS if report.md does not present the retargeting-vs-prospecting gap as an anomaly or as a reason to move prospecting money into retargeting, and does not flag the Direct share as a tracking problem. Mentioning either as normal is fine.
FAIL if either is presented as a problem, or if report.md recommends shifting prospecting budget to retargeting because of its higher ROAS.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: meta ga4 roas {meta_roas_ga4:.2f} pre {meta_roas_pre:.2f}; fb ref {fb_ref_pre:.0f}->{fb_ref_post:.0f}; google platform {g_roas_platform:.2f} ga4 {g_blend_ga4:.2f} "
      f"brand {brand_roas:.1f} generic {gen_roas:.2f}; bing org {bing_org_pre:.0f}->{bing_org_post:.0f}; rtg {rtg_pre:.1f} pros {pros_pre:.1f}")
