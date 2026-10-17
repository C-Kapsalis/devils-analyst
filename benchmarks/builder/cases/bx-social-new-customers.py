"""Breadth benchmark, paid social: where should Q4 paid social budget go (Kestrel & Rye apparel, Q3 2026).

Goal in the brief: new customers. Subtle problems (4): Meta Advantage+
Shopping has no existing-customer budget cap and about two thirds of its
Shopify orders come from returning customers, so per NEW customer it is the
most expensive line despite the best ROAS (DECISION: TikTok prospecting is the
cheapest per new customer); the TikTok export is in USD while Meta is in EUR,
and the agency compares the raw numbers; the agency's engagement-rate
comparison uses different denominators (TikTok per 6-second view, Meta per
reach); the "best creator" for Spark Ads was picked on 3 days and 11 purchases.
Decoys (2): TikTok CPM below Meta's; Meta reports more purchases than Shopify
attributes to Meta UTMs (different attribution, fine as long as not added)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-social-new-customers"
rng = random.Random(81233)
USD_EUR = 0.92
AOV = 74.0

# Meta campaigns (EUR): type, cap, spend, cpm, link ctr, platform purchases per spend, shopify orders, share new
META = {
    "ASC - All Products": ("ADVANTAGE_PLUS_SHOPPING", "none", 21000, 8.2, 0.0142, 1 / 15.5, 1080, 0.30),
    "Prospecting - Broad 25-44": ("MANUAL_SALES", "n/a", 9000, 9.6, 0.0118, 1 / 33.0, 236, 0.84),
    "Retargeting - Engagers 30d": ("MANUAL_SALES", "n/a", 4000, 12.4, 0.0175, 1 / 12.0, 280, 0.21),
}
# TikTok (USD)
TT = {
    "TT - Prospecting Spark Ads": (17400, 5.1, 0.0092, 1 / 34.0, 452, 0.88),
    "TT - Retargeting Video Viewers": (3300, 6.2, 0.0110, 1 / 21.0, 120, 0.40),
}
meta_rows, tt_rows, shop_rows = [], [], []
st = {}
for c, (typ, cap, sp, cpm, ctr, ppe, orders, new) in META.items():
    spend = round(sp * rng.uniform(0.98, 1.02), 2); imps = int(spend / cpm * 1000); reach = int(imps / rng.uniform(2.4, 3.6))
    link = int(imps * ctr); pur = int(round(spend * ppe * rng.uniform(0.96, 1.04))); val = round(pur * AOV * rng.uniform(0.97, 1.03), 2)
    eng = int(reach * rng.uniform(0.012, 0.016))
    meta_rows.append([c, typ, cap, "7d_click_1d_view", "EUR", spend, imps, reach, link, eng, pur, val])
    o = int(orders * rng.uniform(0.97, 1.03)); n = int(round(o * new * rng.uniform(0.97, 1.03)))
    shop_rows.append(["facebook", "paid_social", c, o, n, round(o * AOV * rng.uniform(0.97, 1.03), 2)])
    st[c] = dict(spend_eur=spend, imps=imps, reach=reach, pur=pur, val=val, orders=o, new=n, eng=eng)
for c, (sp, cpm, ctr, ppe, orders, new) in TT.items():
    spend = round(sp * rng.uniform(0.98, 1.02), 2); imps = int(spend / cpm * 1000); views = int(imps * rng.uniform(0.11, 0.13))
    clicks = int(imps * ctr); conv = int(round(spend * ppe * rng.uniform(0.96, 1.04))); val = round(conv * AOV / USD_EUR * rng.uniform(0.97, 1.03), 2)
    eng = int(views * rng.uniform(0.072, 0.086))
    tt_rows.append([c, "7d_click_1d_view", "USD", spend, imps, views, clicks, eng, conv, val])
    o = int(orders * rng.uniform(0.97, 1.03)); n = int(round(o * new * rng.uniform(0.97, 1.03)))
    shop_rows.append(["tiktok", "paid_social", c, o, n, round(o * AOV * rng.uniform(0.97, 1.03), 2)])
    st[c] = dict(spend_eur=spend * USD_EUR, spend_usd=spend, imps=imps, views=views, pur=conv, val_usd=val, orders=o, new=n, eng=eng)

creators = [
    ["@mila.styles", 30, 4200.0, 118], ["@thrift.with.tom", 30, 3900.0, 96], ["@outfitsbyjo", 3, 290.0, 11],
    ["@everydaydenim", 28, 3600.0, 88], ["@capsule.kate", 30, 4100.0, 101],
]
cr_rows = [[n, d, round(s * rng.uniform(0.98, 1.02), 2), p] for n, d, s, p in creators]

# ---------- ground truth ----------
ASC, MP, MR, TP, TR = "ASC - All Products", "Prospecting - Broad 25-44", "Retargeting - Engagers 30d", "TT - Prospecting Spark Ads", "TT - Retargeting Video Viewers"
allc = [ASC, MP, MR, TP, TR]
cpnc = {c: st[c]["spend_eur"] / st[c]["new"] for c in allc}
new_share = {c: st[c]["new"] / st[c]["orders"] for c in allc}
roas_meta = {c: st[c]["val"] / st[c]["spend_eur"] for c in [ASC, MP, MR]}
cpa_meta = {c: st[c]["spend_eur"] / st[c]["pur"] for c in [ASC, MP, MR]}
tt_cpa_usd = st[TP]["spend_usd"] / st[TP]["pur"]; tt_cpa_eur = tt_cpa_usd * USD_EUR
tt_er = st[TP]["eng"] / st[TP]["views"]; meta_er = sum(st[c]["eng"] for c in [ASC, MP]) / sum(st[c]["reach"] for c in [ASC, MP])
tt_er_imp = st[TP]["eng"] / st[TP]["imps"]; meta_er_imp = sum(st[c]["eng"] for c in [ASC, MP]) / sum(st[c]["imps"] for c in [ASC, MP])
cr_cpp = {r[0]: r[2] / r[3] for r in cr_rows}
best_cr = min(cr_cpp, key=cr_cpp.get)
pros_new = [ASC, MP, TP]
cheapest_new = min(pros_new, key=lambda c: cpnc[c])
meta_cpm = sum(st[c]["spend_eur"] for c in [ASC, MP, MR]) / sum(st[c]["imps"] for c in [ASC, MP, MR]) * 1000
tt_cpm_eur = sum(st[c]["spend_eur"] for c in [TP, TR]) / sum(st[c]["imps"] for c in [TP, TR]) * 1000
meta_pur = sum(st[c]["pur"] for c in [ASC, MP, MR]); meta_orders = sum(st[c]["orders"] for c in [ASC, MP, MR])

assert roas_meta[ASC] > roas_meta[MP] and cpa_meta[ASC] == min(cpa_meta[c] for c in [ASC, MP])
assert new_share[ASC] < 0.4 and cpnc[ASC] == max(cpnc[c] for c in pros_new) and cheapest_new == TP
assert cpnc[ASC] > 1.5 * cpnc[TP]
assert tt_er > 4 * meta_er and tt_er_imp < 2.5 * meta_er_imp
assert best_cr == "@outfitsbyjo"
assert tt_cpm_eur < meta_cpm and meta_pur > 1.15 * meta_orders

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x, d=0: f"€{x:,.{d}f}"

brief = f"""# Kestrel & Rye: paid social Q3 review (agency)

Our Q4 goal from the brief: grow new customers. Planning FX rate: 1 USD = {USD_EUR} EUR.

- Meta ASC is our most efficient acquisition campaign: ROAS {roas_meta[ASC]:.2f}x and cost per purchase {cpa_meta[ASC]:.2f}.
- TikTok Prospecting cost per purchase {tt_cpa_usd:.2f}, so TikTok is roughly {tt_cpa_usd / cpa_meta[ASC]:.1f}x as expensive per purchase as ASC.
- Engagement: TikTok engagement rate {pc(tt_er)} vs Meta {pc(meta_er, 2)}: TikTok content is far more engaging.
- Best creator for Spark Ads: @outfitsbyjo (cost per purchase {cr_cpp['@outfitsbyjo']:.2f}). Plan: give @outfitsbyjo the largest creator budget in Q4.
- Q4 proposal: +40% to Meta ASC, TikTok flat.
"""

files = {
    "resources/agency_q3_review.md": brief,
    "resources/meta_campaigns_q3.csv": to_csv(
        ["campaign_name", "campaign_type", "existing_customer_budget_cap", "attribution_setting", "currency", "amount_spent", "impressions",
         "reach", "link_clicks", "post_engagements", "purchases", "purchase_conversion_value"], meta_rows),
    "resources/tiktok_campaigns_q3.csv": to_csv(
        ["campaign_name", "attribution_setting", "currency", "spend", "impressions", "video_views_6s", "clicks", "engagements", "conversions",
         "conversion_value"], tt_rows),
    "resources/tiktok_spark_creators_q3.csv": to_csv(["creator_handle", "days_live", "spend_usd", "purchases"], cr_rows),
    "resources/shopify_orders_by_utm_q3.csv": to_csv(["utm_source", "utm_medium", "utm_campaign", "orders", "new_customer_orders", "total_sales_eur"], shop_rows),
}

prompt = """
We're Kestrel & Rye (womenswear, online only). Our agency runs Meta and TikTok for us; their Q3 review and the exports, plus our Shopify orders by UTM, are in resources/. Where should next quarter's paid social budget go? Write report.md with the numbers and your recommendation.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files; EUR at 1 USD = {USD_EUR} EUR):

1. ASC buys returning customers. "ASC - All Products" has no existing-customer budget cap and only {pc(new_share[ASC], 0)} of its Shopify orders are from new customers. Cost per new customer: ASC {eur(cpnc[ASC])}, Meta Prospecting {eur(cpnc[MP])}, TikTok Prospecting {eur(cpnc[TP])}. Found if report.md uses new-customer orders (or the missing existing-customer cap) and shows ASC is expensive per new customer.
2. Currency mismatch. TikTok spend and values are in USD; Meta in EUR. TikTok Prospecting cost per purchase is ${tt_cpa_usd:.2f} = {eur(tt_cpa_eur, 2)}; the agency compared ${tt_cpa_usd:.2f} directly with Meta's €{cpa_meta[ASC]:.2f}. Found if report.md notes the USD/EUR difference and converts.
3. Engagement rates on different denominators. TikTok's {pc(tt_er)} is engagements per 6-second video view; Meta's {pc(meta_er, 2)} is engagements per reach. Per impression they are {pc(tt_er_imp, 2)} (TikTok) and {pc(meta_er_imp, 2)} (Meta). Found if report.md says the two rates use different denominators and are not comparable (a per-impression recomputation is a bonus).
4. Creator picked on a tiny sample. @outfitsbyjo ran 3 days with 11 purchases ({cr_cpp['@outfitsbyjo']:.2f} USD per purchase); the others ran ~28-30 days with 88-118 purchases. Found if report.md says @outfitsbyjo's result is too small a sample to back with the largest budget.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation (goal: new customers): do not put the Q4 increase into Meta ASC on its ROAS/CPA. Move growth budget toward TikTok Prospecting, the cheapest line per new customer ({eur(cpnc[TP])} vs {eur(cpnc[MP])} Meta Prospecting and {eur(cpnc[ASC])} ASC), and/or cap ASC's existing-customer spend before adding anything to it.

Naive wrong answer: the agency's +40% to Meta ASC because of its best ROAS ({roas_meta[ASC]:.2f}x) and lowest cost per purchase, with TikTok flat.

PASS if report.md's main recommendation does not increase ASC as currently set up (an increase conditional on adding an existing-customer cap is acceptable only if the main new-customer budget still goes to TikTok Prospecting or the report shows ASC's capped cost per new customer would be competitive) AND it directs new-customer budget to TikTok Prospecting or explicitly reallocates on cost per new customer.
FAIL if it endorses +40% to ASC, ranks campaigns on platform ROAS/CPA for the budget call, or keeps TikTok flat while growing ASC.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. TikTok CPM (about {eur(tt_cpm_eur, 2)} after conversion) is below Meta's ({eur(meta_cpm, 2)}). Normal; cheaper reach on TikTok is common.
- D2. Meta reports {meta_pur:,} purchases while Shopify attributes {meta_orders:,} orders to Meta UTMs. Different attribution (7-day click + 1-day view vs last-click UTM); fine as long as the two are not added together.

PASS if report.md does not call TikTok's lower CPM suspicious or a tracking problem, and does not call the Meta-vs-Shopify purchase gap a tracking bug/error (explaining it as attribution difference is fine).
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: cpnc ASC {cpnc[ASC]:.0f} MP {cpnc[MP]:.0f} TP {cpnc[TP]:.0f}; new share ASC {new_share[ASC]:.2f}; roas ASC {roas_meta[ASC]:.2f}; "
      f"tt cpa usd {tt_cpa_usd:.2f} eur {tt_cpa_eur:.2f}; er tt {tt_er:.3f} meta {meta_er:.4f}; cpm tt {tt_cpm_eur:.2f} meta {meta_cpm:.2f}")
