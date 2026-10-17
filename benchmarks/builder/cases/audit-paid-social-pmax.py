"""Audit a Meta + Performance Max setup (Ridgeway Cycles, September 2026).

Planted problems (6): Meta + Google claimed revenue summed above Shopify's
total (MUST), PMax conversions mix newsletter sign-ups with purchases and most
PMax purchases come from brand queries with no brand exclusion (MUST), Meta ad
sets on different attribution settings compared on ROAS (the 1d_click
lookalike looks worst, is best like for like), CTR on all clicks instead of
link clicks, prospecting frequency climbing while link CTR falls (fatigue),
retargeting audience with 540-day membership, no purchaser exclusion, no cap.
Decoys: retargeting ROAS several times prospecting; CPM 6-12 and flat;
link CTR around 1-2%."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "audit-paid-social-pmax"
rng = random.Random(52093)
AOV = 118.0

# ---------- Meta ad sets ----------
# adset: (campaign, job, setting, spend, cpm, link ctr, all/link ratio, freq, cvr_1dclick per link click, claim multiplier)
A = {
    "Prospecting - Broad Interests": ("Prospecting", "prospecting", "7d_click_1d_view", 6200, 8.1, 0.0112, 2.9, 2.8, 0.0105, 2.15),
    "Prospecting - Lookalike 2%": ("Prospecting", "prospecting", "1d_click", 4800, 8.8, 0.0131, 2.7, 2.6, 0.0172, 1.0),
    "Prospecting - Video to Site": ("Prospecting", "prospecting", "7d_click_1d_view", 3900, 6.6, 0.0094, 3.4, 3.1, 0.0098, 2.3),
    "Retargeting - Site Visitors": ("Retargeting", "retargeting", "7d_click_1d_view", 2600, 11.2, 0.0205, 2.4, 4.4, 0.019, 1.9),
    "Retargeting - Cart Abandoners": ("Retargeting", "retargeting", "7d_click_1d_view", 1400, 11.9, 0.0232, 2.2, 3.9, 0.027, 1.8),
}
meta_rows, ms = [], {}
for adset, (camp, job, setting, spend0, cpm, lctr, ratio, freq, cvr1, mult) in A.items():
    spend = round(spend0 * rng.uniform(0.97, 1.03), 2)
    imps = int(round(spend / cpm * 1000))
    reach = int(round(imps / freq))
    link = int(round(imps * lctr))
    allc = int(round(link * ratio))
    p1 = int(round(link * cvr1))
    pur = int(round(p1 * mult))
    val = round(pur * AOV * rng.uniform(0.96, 1.04), 2)
    ms[adset] = dict(job=job, setting=setting, spend=spend, imps=imps, reach=reach, link=link, allc=allc, p1=p1, pur=pur, val=val)
    meta_rows.append([camp, adset, setting, spend, imps, reach, round(imps / reach, 2), allc, link,
                      round(100 * allc / imps, 2), pur, p1, val])

pros = [a for a in A if A[a][1] == "prospecting"]
retg = [a for a in A if A[a][1] == "retargeting"]
roas = {a: ms[a]["val"] / ms[a]["spend"] for a in A}
p1_per_k = {a: ms[a]["p1"] / ms[a]["spend"] * 1000 for a in A}   # 1d-click purchases per 1,000 spend
lal = "Prospecting - Lookalike 2%"
m_spend = sum(v["spend"] for v in ms.values())
m_val = sum(v["val"] for v in ms.values())
m_imps = sum(v["imps"] for v in ms.values())
m_all = sum(v["allc"] for v in ms.values())
m_link = sum(v["link"] for v in ms.values())
ctr_all = m_all / m_imps
ctr_link = m_link / m_imps
pros_roas = sum(ms[a]["val"] for a in pros) / sum(ms[a]["spend"] for a in pros)
retg_roas = sum(ms[a]["val"] for a in retg) / sum(ms[a]["spend"] for a in retg)
cpms = [ms[a]["spend"] / ms[a]["imps"] * 1000 for a in A]

# ---------- prospecting weekly (fatigue) ----------
weeks = ["2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21"]
freq_w = [1.9, 2.3, 2.8, 3.4, 4.0, 4.7, 5.3, 5.9]
ctr_w = [1.62, 1.55, 1.44, 1.31, 1.18, 1.04, 0.93, 0.84]
weekly = [[w, f, round(rng.uniform(7.6, 8.4), 2), c, round(3150 * rng.uniform(0.97, 1.03), 2)] for w, f, c in zip(weeks, freq_w, ctr_w)]

aud_rows = [
    ["Site Visitors 540d", "website visitors", 540, "no", "none", "Retargeting - Site Visitors"],
    ["Cart Abandoners 14d", "add_to_cart without purchase", 14, "yes", "3 per 7 days", "Retargeting - Cart Abandoners"],
]

# ---------- Google: Search + PMax ----------
pm_rows = []
PM = {"All Products": (0.66, 210), "E-Bikes": (0.58, 44), "Accessories": (0.71, 120)}
pm_pur = pm_brand = pm_signup = 0
pm_val = 0.0
for ag, (brand_share, pur) in PM.items():
    b = int(round(pur * brand_share)); nb = pur - b
    aov = 640 if ag == "E-Bikes" else (95 if ag == "Accessories" else 132)
    vb = round(b * aov * rng.uniform(0.97, 1.03), 2); vn = round(nb * aov * rng.uniform(0.97, 1.03), 2)
    su = int(round(pur * rng.uniform(1.6, 2.2)))
    pm_rows += [[ag, "Purchase", "brand", b, vb], [ag, "Purchase", "non_brand", nb, vn],
                [ag, "Newsletter signup", "all", su, 0]]
    pm_pur += pur; pm_brand += b; pm_signup += su; pm_val += vb + vn
pm_cost = 9800.0
pm_all = pm_pur + pm_signup
search_brand_val = round(212 * 121.0, 2)
search_gen_val = round(168 * 128.0, 2)
g_rows = [
    ["Brand Search", "SEARCH", 1450.0, 212, search_brand_val, "n/a"],
    ["Generic Search - Bikes", "SEARCH", 6100.0, 168, search_gen_val, "n/a"],
    ["PMax - Shop", "PERFORMANCE_MAX", pm_cost, pm_all, round(pm_val, 2), "none"],
]
g_val = search_brand_val + search_gen_val + pm_val
g_cost = 1450.0 + 6100.0 + pm_cost

# ---------- Shopify ----------
shop_rows = []
for d in range(1, 31):
    o = int(rng.gauss(30, 4)) + (7 if d % 7 in (5, 6) else 0)
    shop_rows.append([f"2026-09-{d:02d}", o, round(o * rng.uniform(140, 160), 2)])
shop_rev = sum(r[2] for r in shop_rows)
claims = g_val + m_val

# ---------- asserts ----------
assert claims > shop_rev * 1.2, (claims, shop_rev)
assert pm_signup > pm_pur and pm_brand / pm_pur > 0.6
assert roas[lal] == min(roas[a] for a in pros)
assert p1_per_k[lal] == max(p1_per_k[a] for a in pros)
assert ctr_all > 2.4 * ctr_link and 0.008 < ctr_link < 0.025
assert freq_w[-1] > 5 and ctr_w[-1] < 0.55 * ctr_w[0]
assert 1.8 * pros_roas < retg_roas < 12
assert all(5 < c < 13 for c in cpms)

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

notes = f"""# Ridgeway Cycles: paid media notes from the agency (September 2026)

- Goal: online bike and accessory sales. Gross margin about 35%.
- Meta: we report ROAS per ad set straight from Ads Manager. Our Meta CTR is {pc(ctr_all, 2)}, well above benchmark.
- Plan for October: pause "Prospecting - Lookalike 2%" because it has the lowest ROAS of the prospecting ad sets, and add its budget to Broad Interests.
- Google: Performance Max is our best campaign by conversions and CPA. Brand Search and Generic Search run alongside it.
- Combined Meta + Google revenue for September is our headline return figure for the board.
"""

files = {
    "resources/agency_notes_sep2026.md": notes,
    "resources/meta_adsets_sep2026.csv": to_csv(
        ["campaign_name", "adset_name", "attribution_setting", "amount_spent", "impressions", "reach", "frequency",
         "clicks_all", "link_clicks", "ctr_all_pct", "purchases", "purchases_1d_click", "purchase_conversion_value"], meta_rows),
    "resources/meta_prospecting_weekly.csv": to_csv(["week_start", "frequency_7d", "cpm", "link_ctr_pct", "amount_spent"], weekly),
    "resources/meta_custom_audiences.csv": to_csv(
        ["audience_name", "rule", "membership_days", "excludes_purchasers", "frequency_cap", "used_in_adset"], aud_rows),
    "resources/google_ads_campaigns_sep2026.csv": to_csv(
        ["campaign", "campaign_type", "cost", "conversions", "conv_value", "brand_exclusions"], g_rows),
    "resources/pmax_conversions_by_action_sep2026.csv": to_csv(
        ["asset_group", "conversion_action", "search_query_category", "conversions", "conv_value"], pm_rows),
    "resources/shopify_sales_daily_sep2026.csv": to_csv(["date", "orders", "total_sales"], shop_rows),
}

prompt = """
We're Ridgeway Cycles. Our agency runs Meta and Google (Search plus Performance Max) for us, and I'm not sure the setup is right. September exports, the agency's notes and our Shopify sales are in resources/. Can you audit the setup, tell me what's wrong and what to fix first? Put it in report.md.
"""

N, K = 6, math.ceil(0.8 * 6)
g_recall = f"""
The exports contain {N} planted problems. Answer key:

1. Stacked platform revenue. The headline "combined Meta + Google revenue" adds Meta's self-reported purchase value ({eur(m_val)}, mostly on a 7-day click + 1-day view window) and Google's conversion value ({eur(g_val)}) = {eur(claims)}, which is above Shopify's total sales for all channels ({eur(shop_rev)}). Counts as found if report.md says the platform revenues overlap or exceed the Shopify total and cannot be added.
2. PMax conversions are blended and brand-heavy. PMax "conversions" ({pm_all}) include {pm_signup} newsletter sign-ups; only {pm_pur} are purchases. Of the purchases, {pm_brand} ({pc(pm_brand / pm_pur, 0)}) came from brand queries, and brand_exclusions is "none". PMax CPA is {eur(pm_cost / pm_all)} on all conversions but {eur(pm_cost / pm_pur)} on purchases. Counts as found if report.md says PMax must be read on purchases only (sign-ups mixed in) OR says most PMax purchases are brand queries with no brand exclusion; full credit needs either point with its number.
3. Attribution settings differ. "Prospecting - Lookalike 2%" runs on 1d_click while the others use 7d_click_1d_view, so ROAS per ad set is not comparable; the agency plans to pause it for the lowest ROAS ({roas[lal]:.2f}x). On the shared purchases_1d_click column it has the most purchases per spend of the prospecting ad sets ({p1_per_k[lal]:.2f} per €1,000 vs {max(p1_per_k[a] for a in pros if a != lal):.2f} for the next best). Counts as found if report.md says the attribution windows differ so the ROAS comparison or the pause decision is invalid.
4. CTR on all clicks. The quoted Meta CTR {pc(ctr_all, 2)} uses clicks_all (likes, profile taps); link CTR is {m_link:,} / {m_imps:,} = {pc(ctr_link, 2)}. Counts as found if report.md says CTR should use link clicks, with a figure near {pc(ctr_link, 2)} (within 0.15 points) or the reason.
5. Creative fatigue. Prospecting weekly frequency rose from {freq_w[0]} to {freq_w[-1]} while link CTR fell from {ctr_w[0]}% to {ctr_w[-1]}%. Counts as found if report.md names rising frequency with falling link CTR (fatigue) and asks for creative rotation or a cap.
6. Retargeting audience. "Site Visitors 540d" keeps people 540 days, does not exclude purchasers and has no frequency cap. Counts as found if report.md flags at least the missing purchaser exclusion or the 540-day membership.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} problems, each with its substance (a vague mention such as "review your Meta setup" does not count).
FAIL if it identifies fewer than {K}.
"""

g_rank = f"""
Two problems are Must-fix (measurement integrity, which every return figure depends on):
- A. Meta + Google claimed revenue ({eur(claims)}) added together although it exceeds Shopify's total ({eur(shop_rev)}).
- B. PMax conversions mix newsletter sign-ups with purchases ({pm_signup} of {pm_all}) and {pc(pm_brand / pm_pur, 0)} of PMax purchases are brand queries with no brand exclusion.
The lesser problems are: CTR on all clicks, prospecting creative fatigue, and the retargeting audience settings. (The attribution-window mismatch may be ranked anywhere.)

PASS if report.md flags A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND the closing "fix first" line (or explicit first priority) names A, B, or the attribution-window mismatch.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the first priority named is one of the lesser problems.
"""

g_decoy = f"""
Three patterns in the exports are normal and must not be flagged:
- D1. Retargeting ROAS ({retg_roas:.2f}x) several times prospecting ROAS ({pros_roas:.2f}x). Expected: retargeting closes demand that prospecting created.
- D2. CPMs between €{min(cpms):.2f} and €{max(cpms):.2f}, and weekly prospecting CPM flat around €8: normal for Meta.
- D3. Link CTR around {pc(ctr_link, 1)} at account level: inside the normal 0.8-2.5% band.

PASS if report.md does not present D1, D2 or D3 as an error or something to fix. Mentioning them as normal is a PASS. Suggesting a holdout test before scaling retargeting is acceptable.
FAIL if it treats the retargeting-vs-prospecting ROAS gap as a problem in itself or recommends moving prospecting budget to retargeting because of it, calls the CPMs too high, or calls the link CTR weak.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: claims {claims:,.0f} vs shopify {shop_rev:,.0f}; pmax all {pm_all} purchases {pm_pur} brand {pm_brand}; "
      f"LAL roas {roas[lal]:.2f} (min) but 1d/k {p1_per_k[lal]:.2f} (max); ctr all {ctr_all:.4f} link {ctr_link:.4f}; retg {retg_roas:.2f} pros {pros_roas:.2f}")
