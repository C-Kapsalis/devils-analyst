"""Review a monthly paid media report (Kestrel Bikes, September 2026).

Planted problems (5): stacked platform revenue as blended ROAS (MUST), Google
CPA on all conversion actions incl. newsletter and account sign-ups (MUST),
Google CTR as the mean of campaign CTRs, "new creative drove Meta's growth"
while Meta spend rose faster than revenue, display cut on CTR.
Decoys (2): Google clicks vs GA4 google/cpc sessions gap called normal;
brand CTR ~40% and lowest CPA, correctly not scaled."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "review-paid-monthly"
rng = random.Random(41207)
TARGET_CPA = 30.0

# ---------- Google Ads: one row per campaign ----------
# name: (type, impressions, ctr, cpc, purchase cvr, newsletter cvr, account cvr, aov)
G = {
    "Brand - Kestrel Bikes": ("search", 9800, 0.41, 0.31, 0.112, 0.020, 0.015, 88),
    "Generic - Cycling Jackets": ("search", 61000, 0.054, 1.12, 0.027, 0.062, 0.034, 94),
    "Generic - Bike Lights": ("search", 48000, 0.061, 0.84, 0.024, 0.071, 0.030, 46),
    "Generic - Cycling Shoes": ("search", 39000, 0.049, 1.18, 0.026, 0.058, 0.031, 112),
    "Display - Autumn Prospecting": ("display", 1240000, 0.0038, 0.36, 0.0032, 0.024, 0.006, 79),
}
camp_rows, action_rows = [], []
gc = {}
for name, (typ, imps0, ctr, cpc, pcvr, ncvr, acvr, aov) in G.items():
    imps = int(imps0 * rng.uniform(0.95, 1.05))
    clicks = int(round(imps * ctr * rng.uniform(0.96, 1.04)))
    cost = round(clicks * cpc * rng.uniform(0.97, 1.03), 2)
    pur = max(1, int(round(clicks * pcvr * rng.uniform(0.92, 1.08))))
    nl = int(round(clicks * ncvr * rng.uniform(0.9, 1.1)))
    acc = int(round(clicks * acvr * rng.uniform(0.9, 1.1)))
    val = round(pur * aov * rng.uniform(0.95, 1.05), 2)
    allc = pur + nl + acc
    gc[name] = dict(typ=typ, imps=imps, clicks=clicks, cost=cost, pur=pur, nl=nl, acc=acc, val=val, allc=allc)
    camp_rows.append([name, "Display" if typ == "display" else "Search", imps, clicks, cost, allc, val])
    action_rows += [[name, "Purchase", pur, val], [name, "Newsletter signup", nl, 0], [name, "Account created", acc, 0]]

g_cost = sum(v["cost"] for v in gc.values())
g_clicks = sum(v["clicks"] for v in gc.values())
g_imps = sum(v["imps"] for v in gc.values())
g_all = sum(v["allc"] for v in gc.values())
g_pur = sum(v["pur"] for v in gc.values())
g_val = sum(v["val"] for v in gc.values())
gen = [n for n in G if n.startswith("Generic")]
gen_cost = sum(gc[n]["cost"] for n in gen)
gen_pur = sum(gc[n]["pur"] for n in gen)
gen_all = sum(gc[n]["allc"] for n in gen)
gen_clicks = sum(gc[n]["clicks"] for n in gen)
gen_imps = sum(gc[n]["imps"] for n in gen)
brand = gc["Brand - Kestrel Bikes"]
disp = gc["Display - Autumn Prospecting"]

cpa_all = g_cost / g_all            # planted
cpa_pur = g_cost / g_pur            # truth
gen_cpa_all = gen_cost / gen_all    # planted, used for "scale generic"
gen_cpa_pur = gen_cost / gen_pur    # truth
ctr_mean = sum(v["clicks"] / v["imps"] for v in gc.values()) / len(gc)   # planted
ctr_true = g_clicks / g_imps
gen_ctr = gen_clicks / gen_imps
disp_ctr = disp["clicks"] / disp["imps"]

# ---------- Meta ----------
M = {
    "Prospecting - Autumn Carousel": (310000, 0.0125, 8.4, 0.011, 96),
    "Prospecting - Video": (260000, 0.0098, 7.6, 0.009, 90),
    "Retargeting - Dynamic Product Ads": (95000, 0.019, 11.2, 0.045, 84),
}
meta_rows, mc = [], {}
for name, (imps0, lctr, cpm, cvr, aov) in M.items():
    imps = int(imps0 * rng.uniform(0.95, 1.05))
    reach = int(imps / rng.uniform(2.1, 3.4))
    lclicks = int(round(imps * lctr))
    spend = round(imps / 1000 * cpm, 2)
    pur = int(round(lclicks * cvr * 2.6))   # 7d click + 1d view claims
    val = round(pur * aov * rng.uniform(0.95, 1.05), 2)
    mc[name] = dict(spend=spend, pur=pur, val=val)
    meta_rows.append([name, "7d_click_1d_view", imps, reach, lclicks, spend, pur, val])
m_spend = sum(v["spend"] for v in mc.values())
m_val = sum(v["val"] for v in mc.values())
m_pur = sum(v["pur"] for v in mc.values())
# August (only in the report): spend grew faster than revenue
aug_m_spend = round(m_spend / 1.37, 2)
aug_m_val = round(m_val / 1.21, 2)
meta_rev_growth = m_val / aug_m_val - 1
meta_spend_growth = m_spend / aug_m_spend - 1
aug_roas, sep_roas = aug_m_val / aug_m_spend, m_val / m_spend

# ---------- Shopify daily (all channels) ----------
shop_rows = []
for d in range(1, 31):
    orders = int(rng.gauss(26, 4)) + (6 if d % 7 in (5, 6) else 0)
    rev = round(orders * rng.uniform(80, 92), 2)
    shop_rows.append([f"2026-09-{d:02d}", orders, rev])
shop_rev = sum(r[2] for r in shop_rows)
shop_orders = sum(r[1] for r in shop_rows)

# ---------- GA4 sessions (decoy: a few % below Google clicks) ----------
ga_cpc = int(round(g_clicks * 0.936))
ga_rows = [["google / cpc", ga_cpc], ["facebook / paid_social", int(sum(r[4] for r in meta_rows) * 0.91)],
           ["google / organic", 14210], ["(direct) / (none)", 9120], ["newsletter / email", 3880]]

paid_spend = g_cost + m_spend
claims = g_val + m_val
roas_stacked = claims / paid_spend
roas_store_cap = shop_rev / paid_spend

# ---------- asserts: traps bite, decoys hold ----------
assert claims > shop_rev * 1.15, (claims, shop_rev)
assert roas_stacked > roas_store_cap * 1.15
assert cpa_pur / cpa_all > 2.2, (cpa_pur, cpa_all)
assert gen_cpa_all < TARGET_CPA * 0.5 and gen_cpa_pur > TARGET_CPA * 1.15, (gen_cpa_all, gen_cpa_pur)
assert ctr_mean / ctr_true > 4, (ctr_mean, ctr_true)
assert meta_spend_growth > meta_rev_growth + 0.1 and sep_roas < aug_roas
assert 0.003 < disp_ctr < 0.0045
assert 0.9 < ga_cpc / g_clicks < 0.97
assert brand["clicks"] / brand["imps"] > 0.35 and brand["cost"] / brand["pur"] < min(gc[n]["cost"] / gc[n]["pur"] for n in gen)

eur = lambda x: f"€{x:,.0f}"
eur2 = lambda x: f"€{x:,.2f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

camp_table = "\n".join(
    f"| {n} | {eur(v['cost'])} | {v['clicks']:,} | {pc(v['clicks'] / v['imps'], 2)} | {v['allc']:,} | {eur2(v['cost'] / v['allc'])} |"
    for n, v in gc.items())

artefact = f"""# Kestrel Bikes: Paid Media Report, September 2026

Prepared by the performance marketing team. Period: 1-30 September 2026.

## Summary

- **Paid media drove {eur(claims)} in revenue in September on {eur(paid_spend)} of spend: a blended ROAS of {roas_stacked:.2f}x.**
- Google Ads delivered {g_all:,} conversions at a CPA of **{eur2(cpa_all)}**, far below our {eur(TARGET_CPA)} target.
- Google Ads CTR was **{pc(ctr_mean)}** across campaigns, a strong month.
- Meta revenue grew {pc(meta_rev_growth, 0)} on August, driven by the new Autumn Carousel creative.

## Google Ads

| Campaign | Cost | Clicks | CTR | Conversions | CPA |
|---|---|---|---|---|---|
{camp_table}
| **Total** | **{eur(g_cost)}** | **{g_clicks:,}** | **{pc(ctr_mean)}** | **{g_all:,}** | **{eur2(cpa_all)}** |

Google Ads revenue (conversion value): {eur(g_val)}.

The generic campaigns converted at a CPA of {eur2(gen_cpa_all)}, less than half our target. There is clearly room to scale.

Brand search had a {pc(brand['clicks'] / brand['imps'], 0)} CTR and the lowest cost per purchase in the account. That is normal for people searching our own name, and most of them would likely find us anyway, so we are keeping the brand budget flat rather than reading this as a reason to scale.

Google Ads recorded {g_clicks:,} clicks and GA4 recorded {ga_cpc:,} google / cpc sessions ({pc(1 - ga_cpc / g_clicks)} fewer). A gap of this size is normal: consent banners, ad blockers and people who leave before the page loads mean the two never match exactly. No tracking issue.

## Display

The Autumn Prospecting display campaign had a CTR of only {pc(disp_ctr, 2)}, against {pc(gen_ctr, 1)} on generic search. It is clearly not working.

## Meta

| | August | September | Change |
|---|---|---|---|
| Spend | {eur(aug_m_spend)} | {eur(m_spend)} | +{pc(meta_spend_growth, 0)} |
| Revenue (Meta reported) | {eur(aug_m_val)} | {eur(m_val)} | +{pc(meta_rev_growth, 0)} |

The new Autumn Carousel creative launched on 1 September and drove the {pc(meta_rev_growth, 0)} revenue growth. Meta now accounts for {eur(m_val)} of our revenue.

## Recommendations

1. Increase Google generic budgets by 30% from October: CPA {eur2(gen_cpa_all)} against a {eur(TARGET_CPA)} target.
2. Pause the display campaign and move its {eur(disp['cost'])} to Meta prospecting.
3. Keep the Autumn Carousel running through Q4 and brief two more carousel variants.
4. Keep brand search flat.
"""

files = {
    "resources/monthly_paid_report_sep2026.md": artefact,
    "resources/google_ads_campaigns_sep2026.csv": to_csv(
        ["campaign", "campaign_type", "impressions", "clicks", "cost", "conversions", "conv_value"], camp_rows),
    "resources/google_ads_conversions_by_action_sep2026.csv": to_csv(
        ["campaign", "conversion_action", "conversions", "conv_value"], action_rows),
    "resources/meta_ads_campaigns_sep2026.csv": to_csv(
        ["campaign_name", "attribution_setting", "impressions", "reach", "link_clicks", "spend", "purchases", "purchase_value"], meta_rows),
    "resources/shopify_sales_daily_sep2026.csv": to_csv(["date", "orders", "total_sales"], shop_rows),
    "resources/ga4_sessions_by_source_medium_sep2026.csv": to_csv(["session_source_medium", "sessions"], ga_rows),
}

prompt = """
Our September paid media report is in resources/monthly_paid_report_sep2026.md, and the exports it was built from are in resources/ too (Google Ads, Meta, Shopify and GA4). Can you check it before I send it to my boss on Monday? I want to know if it's OK to send and, if not, exactly what to fix. Write it up in report.md.
"""

g_recall = f"""
The report under review (monthly_paid_report_sep2026.md) contains 5 planted problems. Answer key:

1. Stacked platform revenue. It says paid media drove {eur(claims)} at a blended ROAS of {roas_stacked:.2f}x. That adds Google's conversion value ({eur(g_val)}) and Meta's self-reported purchase value ({eur(m_val)}, on a 7-day click + 1-day view window). Their sum is above Shopify's total revenue for all channels ({eur(shop_rev)}), so the same sales are claimed twice. Even giving paid media every Shopify sale, ROAS could be at most {roas_store_cap:.2f}x. Counts as found if report.md says the platform revenues overlap or exceed the store total and the {roas_stacked:.2f}x figure is overstated (any recomputation against Shopify's {eur(shop_rev)} is fine).
2. Conversions include micro actions. Google "conversions" ({g_all:,}) include Newsletter signup and Account created; only {g_pur:,} are purchases. Google CPA on purchases is {eur2(cpa_pur)}, not {eur2(cpa_all)}; generic search CPA on purchases is {eur2(gen_cpa_pur)} (above the {eur(TARGET_CPA)} target), not {eur2(gen_cpa_all)}. Counts as found if report.md says CPA must be on purchases and gives a purchase CPA within 5% of {eur2(cpa_pur)} (account) or {eur2(gen_cpa_pur)} (generic), or per-campaign purchase CPAs.
3. Averaged CTR. The Google CTR {pc(ctr_mean)} is the mean of the five campaign CTRs; total clicks / total impressions = {g_clicks:,} / {g_imps:,} = {pc(ctr_true, 2)}. Counts as found if report.md gives a CTR within 0.2 points of {pc(ctr_true, 2)} or explains the figure is an average of campaign rates that must be recomputed from totals.
4. Unsupported causal claim. "The new carousel drove the {pc(meta_rev_growth, 0)} growth": Meta spend rose {pc(meta_spend_growth, 0)} in the same month, faster than revenue, so Meta ROAS fell from {aug_roas:.2f}x to {sep_roas:.2f}x; there is no test or control. Counts as found if report.md challenges the claim citing the spend increase, the falling return, or the absence of a test or control.
5. Display judged on CTR. Display is called "not working" and cut because its CTR ({pc(disp_ctr, 2)}) is below search; a display CTR around 0.3-0.5% is normal and display should be judged on reach, viewable impressions or a holdout. Counts as found if report.md says CTR is the wrong yardstick for display or that the pause needs a test first.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention such as "double-check the numbers" does not count).
FAIL if it identifies fewer than 4.
"""

g_rank = f"""
Two of the problems are Must-fix because they change the decision in the report:
- A. Blended ROAS {roas_stacked:.2f}x built from Google + Meta self-reported revenue ({eur(claims)}) that exceeds total Shopify revenue ({eur(shop_rev)}).
- B. Google CPA {eur2(cpa_all)} counts newsletter and account sign-ups; the purchase CPA is {eur2(cpa_pur)} and generic purchase CPA {eur2(gen_cpa_pur)} is above the {eur(TARGET_CPA)} target, so "scale generic +30%" is wrong.
The lesser problems are: the averaged CTR, the carousel causal claim, and display judged on CTR.

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the report can be sent as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves sending the report unchanged.
"""

g_decoy = f"""
The report contains two statements that are correct and must not be flagged:
- D1. Google Ads clicks {g_clicks:,} vs GA4 google / cpc sessions {ga_cpc:,} ({pc(1 - ga_cpc / g_clicks)} fewer), called normal. A gap of a few percent between ad clicks and analytics sessions is expected (consent, blockers, early exits).
- D2. Brand search CTR {pc(brand['clicks'] / brand['imps'], 0)} with the lowest cost per purchase, kept flat because brand searchers would likely find the site anyway. A 30-50% brand CTR is normal and the decision not to scale brand on it is sound.

PASS if report.md does not present D1 or D2 as an error, a tracking problem, or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it flags D1 as a tracking loss or problem to investigate, or flags D2 (the brand CTR or the decision to keep brand flat) as wrong.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: claims {claims:,.0f} vs shopify {shop_rev:,.0f} (ROAS {roas_stacked:.2f} vs cap {roas_store_cap:.2f}); "
      f"CPA all {cpa_all:.2f} vs purchase {cpa_pur:.2f}; generic {gen_cpa_all:.2f} vs {gen_cpa_pur:.2f}; "
      f"CTR mean {ctr_mean:.3f} vs {ctr_true:.4f}; meta spend +{meta_spend_growth:.2f} rev +{meta_rev_growth:.2f}")
