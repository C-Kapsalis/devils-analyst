"""Breadth benchmark, attribution: Q4 budget from last-click GA4 (Wrenfield Audio headphones, Q3 2026).

Subtle problems (4): YouTube and podcast are judged on last-click GA4 revenue
(a floor for upper-funnel lines) while the post-purchase survey names them as
first touch for ~30% of respondents; in podcast flight weeks direct revenue
jumps ~40% (podcast demand lands in Direct); in the same weeks brand-search
impressions rise ~30%, so brand search's ROAS of ~14 is partly harvesting
demand the podcast created; the agency's "Brand Search drives X% of revenue"
is computed on revenue excluding Unassigned.
DECISION: do not cut YouTube/podcast and move the money to brand search on
last-click ROAS; hold them and run a holdout/geo test first.
Decoys (2): GA4 revenue ~4% below Shopify; brand search CTR ~33% with the
lowest CPA."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-attrib-last-click-floor"
rng = random.Random(24680)
AOV = 128.0
weeks = [f"2026-W{w}" for w in range(27, 40)]
flight = {29, 30, 31, 35, 36, 37}

# weekly series
wk_rows = []
for i, w in enumerate(weeks):
    n = int(w[-2:]); f = n in flight
    pod = round(6600 * rng.uniform(0.95, 1.05), 2) if f else 0.0
    yt = round(4230 * rng.uniform(0.95, 1.05), 2)
    bimps = int(rng.gauss(28000, 1000) * (1.31 if f else 1.0))
    dsess = int(rng.gauss(14800, 600) * (1.36 if f else 1.0))
    drev = round(dsess * rng.uniform(1.12, 1.18) * (1.03 if f else 1.0), 2)
    wk_rows.append([w, "yes" if f else "no", pod, yt, bimps, dsess, drev])

# GA4 channel / campaign table (session-scoped last click)
spend = {"brand_search": 18200.0, "generic_search": 61500.0, "youtube_awareness": 55000.0, "podcast_sponsorships": 39600.0, "meta_prospecting": 70400.0}
direct_rev = sum(r[6] for r in wk_rows)
direct_sess = sum(r[5] for r in wk_rows)
GA = [
    ("Paid Search", "brand_search", 127500, spend["brand_search"] * 14.1),
    ("Paid Search", "generic_search", 57900, spend["generic_search"] * 3.0),
    ("Paid Video", "youtube_awareness", 17600, spend["youtube_awareness"] * 0.41),
    ("Paid Social", "meta_prospecting", 81300, spend["meta_prospecting"] * 2.35),
    ("Direct", "(direct)", direct_sess, direct_rev),
    ("Organic Search", "(organic)", 152000, 214000.0),
    ("Email", "newsletter", 33000, 61000.0),
    ("Referral", "(referral)", 12000, 19500.0),
    ("Unassigned", "(not set)", 34000, 162000.0),
]
ga_rows = []
for ch, camp, sess, rev in GA:
    rev = round(rev * (1 if camp == "(direct)" else rng.uniform(0.98, 1.02)), 2)
    pur = int(round(rev / (AOV * rng.uniform(0.98, 1.02))))
    ga_rows.append([ch, camp, int(sess), pur, rev])
ga_rev = sum(r[4] for r in ga_rows)
shop_rev = round(ga_rev / 0.958, 2)
shop_orders = int(round(sum(r[3] for r in ga_rows) / 0.958))

spend_rows = [
    ["brand_search", "Google Ads", spend["brand_search"], sum(r[4] for r in wk_rows), int(0.331 * sum(r[4] for r in wk_rows))],
    ["generic_search", "Google Ads", spend["generic_search"], 1310000, 61400],
    ["youtube_awareness", "Google Ads (YouTube)", spend["youtube_awareness"], 8400000, 19100],
    ["podcast_sponsorships", "Podcast networks (flat fee, promo URL wrenfield.com/listen)", spend["podcast_sponsorships"], "", ""],
    ["meta_prospecting", "Meta", spend["meta_prospecting"], 8100000, 88000],
]
survey = [["YouTube", 512], ["Podcast", 351], ["Friend or family", 588], ["Instagram / Facebook", 530], ["Google search", 610], ["Review site", 151], ["Other / don't remember", 205]]
resp = sum(s[1] for s in survey)

# ---------- ground truth ----------
lc = {r[1]: r[4] for r in ga_rows}
roas = {k: lc.get(k, 0.0) / v for k, v in spend.items()}
fl = [r for r in wk_rows if r[1] == "yes"]; nf = [r for r in wk_rows if r[1] == "no"]
mean = lambda x: sum(x) / len(x)
d_uplift = mean([r[6] for r in fl]) / mean([r[6] for r in nf]) - 1
b_uplift = mean([r[4] for r in fl]) / mean([r[4] for r in nf]) - 1
d_extra = (mean([r[6] for r in fl]) - mean([r[6] for r in nf])) * len(fl)
pod_spend_w = sum(r[2] for r in wk_rows)
surv_share = {s[0]: s[1] / resp for s in survey}
ua = lc["(not set)"]
brand_share_naive = lc["brand_search"] / (ga_rev - ua)
brand_share = lc["brand_search"] / ga_rev
gap = 1 - ga_rev / shop_rev
b_ctr = spend_rows[0][4] / spend_rows[0][3]
cpa_brand = spend["brand_search"] / [r for r in ga_rows if r[1] == "brand_search"][0][3]

assert roas["youtube_awareness"] < 0.5 and roas["podcast_sponsorships"] == 0 and roas["brand_search"] > 13
assert surv_share["YouTube"] + surv_share["Podcast"] > 0.28
assert d_uplift > 0.33 and b_uplift > 0.25 and abs(pod_spend_w - spend["podcast_sponsorships"]) < 0.05 * spend["podcast_sponsorships"]
assert brand_share_naive - brand_share > 0.02
assert 0.03 < gap < 0.05 and b_ctr > 0.3

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

plan = f"""# Wrenfield Audio: Q4 budget proposal (agency)

Return on ad spend by line, Q3 (GA4 revenue, spend from platforms):

| line | spend | GA4 revenue | ROAS |
|---|---|---|---|
""" + "".join(f"| {k} | {eur(v)} | {eur(lc.get(k, 0.0))} | {roas[k]:.2f} |\n" for k, v in spend.items()) + f"""
- Brand Search drives {pc(brand_share_naive)} of our revenue at ROAS {roas['brand_search']:.1f}.
- YouTube (ROAS {roas['youtube_awareness']:.2f}) and podcasts (no measurable revenue) do not pay back.
- Proposal: cut YouTube and podcasts entirely in Q4 and move the {eur(spend['youtube_awareness'] + spend['podcast_sponsorships'])} into Brand Search and Meta.
"""

files = {
    "resources/agency_q4_proposal.md": plan,
    "resources/ga4_revenue_by_campaign_q3.csv": to_csv(["session_default_channel_group", "session_campaign", "sessions", "purchases", "purchase_revenue"], ga_rows),
    "resources/media_spend_q3.csv": to_csv(["line", "platform", "spend", "impressions", "clicks"], spend_rows),
    "resources/weekly_trends_q3.csv": to_csv(["iso_week", "podcast_flight", "podcast_spend", "youtube_spend", "brand_search_impressions", "direct_sessions", "direct_revenue"], wk_rows),
    "resources/post_purchase_survey_q3.csv": to_csv(["answer_how_did_you_first_hear_about_us", "responses"], survey),
    "resources/shopify_totals_q3.csv": to_csv(["period", "orders", "total_sales"], [["2026-Q3", shop_orders, shop_rev]]),
}

prompt = """
We're Wrenfield Audio (premium headphones, online). The agency wants to change our Q4 media mix; their proposal and our Q3 data (GA4, spend, weekly trends, our post-purchase survey, Shopify totals) are in resources/. Where should next quarter's budget go? Write report.md with the numbers and your recommendation.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Last click is a floor for upper-funnel lines. YouTube's last-click ROAS {roas['youtube_awareness']:.2f} and podcast's 0 come from session last-click GA4 revenue; podcasts have no clicks at all. The post-purchase survey ({resp:,} responses) names YouTube ({pc(surv_share['YouTube'])}) and podcasts ({pc(surv_share['Podcast'])}) as where buyers first heard of the brand. Found if report.md says last-click undervalues YouTube/podcast and cites the survey (or another view-through/first-touch signal) with a number.
2. Podcast demand lands in Direct. In the six podcast flight weeks, weekly direct revenue averaged {pc(d_uplift)} more than in non-flight weeks (about {eur(d_extra)} extra over the flights vs {eur(pod_spend_w)} podcast spend). Found if report.md links the direct-revenue lift to podcast flight weeks with a number.
3. Brand search harvests created demand. Brand-search impressions are {pc(b_uplift)} higher in flight weeks, so part of brand search's ROAS {roas['brand_search']:.1f} is demand created by podcast/YouTube; brand ROAS is not incremental. Found if report.md says brand search's high ROAS depends on demand from other channels (brand impressions rising with flights) or is not incremental, and so is not where new money should go.
4. Share computed without Unassigned. The proposal's "{pc(brand_share_naive)} of revenue" excludes Unassigned ({eur(ua)}); on all GA4 revenue brand search is {pc(brand_share)}. Found if report.md notes the Unassigned exclusion or recomputes the share near {pc(brand_share)}.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: do NOT cut YouTube and podcasts on last-click ROAS and do NOT move their {eur(spend['youtube_awareness'] + spend['podcast_sponsorships'])} into Brand Search. Keep them (at or near current spend) and measure them properly first with a holdout/geo test or a pause test, using the flight-week evidence and the survey as reasons. Small trims while testing are fine.

Naive wrong answer: the agency's plan: cut YouTube and podcasts entirely and move the money into Brand Search (ROAS {roas['brand_search']:.1f}) and Meta.

PASS if report.md's main recommendation keeps YouTube and podcasts (no full cut) pending an incrementality test, and does not put the freed or new budget into Brand Search on its ROAS.
FAIL if it endorses cutting YouTube or podcasts entirely, or makes Brand Search the main destination for added budget.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. GA4 revenue ({eur(ga_rev)}) is about {pc(gap, 1)} below Shopify ({eur(shop_rev)}). Normal tracking loss (consent, blockers); Shopify is the revenue total.
- D2. Brand search CTR is about {pc(b_ctr)} with the lowest cost per purchase ({eur(cpa_brand)}). Normal for brand terms. (Saying brand ROAS is not incremental is correct and separate.)

PASS if report.md does not call the GA4-vs-Shopify gap a tracking failure that needs fixing, and does not call the brand CTR suspicious.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: roas yt {roas['youtube_awareness']:.2f} brand {roas['brand_search']:.1f}; survey yt+pod {surv_share['YouTube'] + surv_share['Podcast']:.2f}; "
      f"direct uplift {d_uplift:.2f} brand imps {b_uplift:.2f}; share naive {brand_share_naive:.3f} true {brand_share:.3f}; gap {gap:.3f}")
