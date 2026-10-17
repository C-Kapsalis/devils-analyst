"""Google Ads account health: brand keywords (45% CTR, cents CPC) flatter the
blended account; per-row cpc/ctr columns averaged != totals; generic campaigns
lose impression share to rank, not budget (only one small campaign is
budget-limited), so 'add budget' is the wrong lever."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "sem-account-health"
rng = random.Random(9031)
AOV, MARGIN = 90.0, 0.40
BREAKEVEN = AOV * MARGIN

# campaign: (keywords, clicks range, ctr range, cpc range, cvr, IS, budget lost, rank lost)
BRAND_KW = ["harbor outdoor", "harbor outdoor shop", "harbor outdoor boots", "harbor outdoor jackets",
            "harbour outdoor", "harbor outdoors", "harbor outdoor discount code", "harbor outdoor returns",
            "harbor outdoor sale", "harbor outdoor tents", "harbor outdoor near me", "harbor outdoor uk",
            "harbor outdoor socks", "harbor outdoor rain jacket", "harbor outdoor hiking boots",
            "harbor outdoor store", "harbor outdoor reviews", "harbor outdoor delivery", "harbor outdoor mens",
            "harbor outdoor womens", "harbor outdoor kids", "harbor outdoor backpack", "www harbor outdoor",
            "harbor outdoor com", "harbor outdoor gift card", "harbor outdoor size guide",
            "harbor outdoor fleece", "harbor outdoor trail", "harbor outdoor black friday", "harboroutdoor"]
CAMPAIGNS = {
    "Brand - Harbor Outdoor": (BRAND_KW, (80, 700), (0.38, 0.52), (0.08, 0.22), 0.115, 0.94, 0.01, 0.05),
    "Generic - Hiking Boots": (["hiking boots", "waterproof hiking boots", "mens hiking boots", "womens hiking boots",
                                "best hiking boots", "lightweight hiking boots", "leather hiking boots",
                                "hiking boots wide fit", "goretex hiking boots", "hiking boots sale",
                                "trail boots", "walking boots"], (250, 900), (0.035, 0.065), (1.5, 2.4), 0.028, 0.38, 0.03, 0.59),
    "Generic - Rain Jackets": (["rain jacket", "waterproof jacket", "mens rain jacket", "womens rain jacket",
                                "packable rain jacket", "lightweight waterproof jacket", "hiking rain jacket",
                                "breathable rain jacket", "rain jacket with hood", "rain shell",
                                "waterproof jacket sale", "best rain jacket"], (200, 800), (0.03, 0.06), (1.4, 2.2), 0.030, 0.42, 0.04, 0.54),
    "Generic - Tents": (["2 person tent", "backpacking tent", "lightweight tent", "camping tent", "4 person tent",
                         "tent sale", "ultralight tent", "family tent", "pop up tent", "dome tent"],
                        (150, 650), (0.03, 0.055), (1.6, 2.6), 0.024, 0.35, 0.02, 0.63),
    "Generic - Trail Socks": (["hiking socks", "merino hiking socks", "trail running socks", "wool walking socks",
                               "blister free socks", "hiking socks women"], (60, 160), (0.05, 0.08), (0.45, 0.75), 0.045, 0.51, 0.42, 0.07),
}

rows = []
for camp, (kws, clr, ctrr, cpcr, cvr, iss, bl, rl) in CAMPAIGNS.items():
    for kw in kws:
        clicks = rng.randint(*clr)
        ctr = rng.uniform(*ctrr)
        imps = int(round(clicks / ctr))
        cpc = rng.uniform(*cpcr)
        cost = round(clicks * cpc, 2)
        purchases = max(0, int(round(clicks * cvr * rng.uniform(0.7, 1.3))))
        rows.append([camp, kw, imps, clicks, round(clicks / imps, 4), round(cost / clicks, 2), cost, purchases,
                     iss, bl, rl])
HEADER = ["campaign", "keyword", "impressions", "clicks", "ctr", "cpc", "cost", "purchases",
          "search_impression_share", "search_budget_lost_impression_share", "search_rank_lost_impression_share"]
csv_text = to_csv(HEADER, rows)

# ---- ground truth ----
def tot(rs):
    imps = sum(r[2] for r in rs); clicks = sum(r[3] for r in rs); cost = sum(r[6] for r in rs); pur = sum(r[7] for r in rs)
    return dict(imps=imps, clicks=clicks, cost=cost, pur=pur, ctr=clicks / imps, cpc=cost / clicks, cpa=cost / pur)
acct = tot(rows)
brand = tot([r for r in rows if r[0].startswith("Brand")])
gen = tot([r for r in rows if r[0].startswith("Generic")])
camp = {c: tot([r for r in rows if r[0] == c]) for c in CAMPAIGNS}
mean_ctr = sum(r[4] for r in rows) / len(rows)
mean_cpc = sum(r[5] for r in rows) / len(rows)
gen_big = [c for c in CAMPAIGNS if c.startswith("Generic") and c != "Generic - Trail Socks"]
gen_imps = sum(camp[c]["imps"] for c in gen_big)
gen_rank = sum(CAMPAIGNS[c][7] * camp[c]["imps"] for c in gen_big) / gen_imps
gen_budget = sum(CAMPAIGNS[c][6] * camp[c]["imps"] for c in gen_big) / gen_imps

assert acct["cpa"] < BREAKEVEN * 0.8, acct
assert gen["cpa"] > BREAKEVEN * 1.4, gen
assert all(camp[c]["cpa"] > BREAKEVEN for c in gen_big)
assert camp["Generic - Trail Socks"]["cpa"] < BREAKEVEN * 0.7
assert mean_ctr / acct["ctr"] > 2.8, (mean_ctr, acct["ctr"])
assert gen_rank > 10 * gen_budget

f = lambda x: f"{x:,.2f}"
pc = lambda x: f"{100 * x:.1f}%"
camp_lines = "\n".join(
    f"- {c}: cost {f(v['cost'])}, purchases {v['pur']}, CPA {f(v['cpa'])}, impression share {pc(CAMPAIGNS[c][5])}, "
    f"lost to budget {pc(CAMPAIGNS[c][6])}, lost to rank {pc(CAMPAIGNS[c][7])}" for c, v in camp.items())

prompt = """
Attached is our Google Ads keyword report for September 2026 (resources/google_ads_keywords_sep2026.csv). Our average order value is 90 and our gross margin is 40%. Is our Google Ads account healthy enough to increase budget, and where would extra budget go? Write report.md with the account's key numbers (CTR, CPC, CPA) and a clear recommendation.
"""

g_split = f"""
Context: average order value 90, gross margin 40%, so break-even CPA = {f(BREAKEVEN)}.
Ground truth (September 2026):
- Blended account: cost {f(acct['cost'])}, purchases {acct['pur']}, CPA {f(acct['cpa'])} (looks profitable, but is flattered by brand)
- Brand campaign: cost {f(brand['cost'])}, purchases {brand['pur']}, CPA {f(brand['cpa'])}
- All generic (non-brand) campaigns: cost {f(gen['cost'])}, purchases {gen['pur']}, CPA {f(gen['cpa'])} — ABOVE break-even
Per campaign:
{camp_lines}
The naive conclusion is "account CPA {f(acct['cpa'])} is below break-even {f(BREAKEVEN)}, so the account is healthy, scale it."

PASS if report.md separates brand from generic/non-brand and states that generic CPA (about {f(gen['cpa'])}, within 5%, or per-campaign generic CPAs matching the list above) is above the break-even CPA of about {f(BREAKEVEN)}, so the account is not healthy enough for a broad budget increase.
FAIL if it judges health on the blended CPA of {f(acct['cpa'])} alone, or concludes the account as a whole is healthy enough to scale budget across the board.
"""
g_budget = f"""
Impression share facts (campaign-level columns, identical on every row of a campaign):
- Large generic campaigns ({', '.join(gen_big)}) lose about {pc(gen_rank)} of impression share to RANK and only about {pc(gen_budget)} to BUDGET. More budget will not buy them more impressions; their limit is Ad Rank (quality score, ad relevance, landing page, bids), and they are unprofitable anyway.
- Generic - Trail Socks is the only budget-limited campaign: lost {pc(CAMPAIGNS['Generic - Trail Socks'][6])} to budget, CPA {f(camp['Generic - Trail Socks']['cpa'])} (below break-even {f(BREAKEVEN)}), but it is small (cost {f(camp['Generic - Trail Socks']['cost'])}).
- Brand already has {pc(CAMPAIGNS['Brand - Harbor Outdoor'][5])} impression share; extra budget there buys almost nothing.

PASS if report.md says extra budget should go only (or mainly) to Generic - Trail Socks because it is the one budget-limited, profitable campaign, AND says the other generic campaigns are limited by rank (not budget) so they need quality/relevance/bid/efficiency fixes rather than more budget.
FAIL if it recommends adding budget to Hiking Boots, Rain Jackets, Tents or Brand, or recommends a broad/account-wide budget increase, or does not use the lost-impression-share split at all.
"""
g_kpis = f"""
Account-level CTR and CPC must come from totals (sum clicks / sum impressions, sum cost / sum clicks), not from averaging the per-row ctr and cpc columns.
Ground truth: CTR {pc(acct['ctr'])} ({acct['clicks']:,} clicks / {acct['imps']:,} impressions), CPC {f(acct['cpc'])} ({f(acct['cost'])} / {acct['clicks']:,}).
Wrong values from averaging the columns across keyword rows: CTR {pc(mean_ctr)}, CPC {f(mean_cpc)}.

PASS if report.md reports account CTR within 0.3 percentage points of {pc(acct['ctr'])} and account CPC within 3% of {f(acct['cpc'])}.
FAIL if it reports CTR near {pc(mean_ctr)} or CPC near {f(mean_cpc)} as the account figure, or omits account CTR/CPC.
"""

write_case(NAME, {"resources/google_ads_keywords_sep2026.csv": csv_text}, prompt,
           [("brand-generic-split", 3, g_split), ("budget-vs-rank", 2, g_budget), ("account-kpis", 1, g_kpis)])
print(f"{NAME}: blended CPA {acct['cpa']:.2f}, generic CPA {gen['cpa']:.2f}, brand {brand['cpa']:.2f}, breakeven {BREAKEVEN:.0f}; "
      f"CTR {acct['ctr']:.3f} vs mean {mean_ctr:.3f}; CPC {acct['cpc']:.2f} vs mean {mean_cpc:.2f}; generic rank-lost {gen_rank:.2f} budget-lost {gen_budget:.2f}")
