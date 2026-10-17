"""Breadth benchmark, paid search: where should Q4 search budget go (Copperline Coffee Gear, Q3 2026).

Subtle problems (5): Grinders & Accessories has the best revenue ROAS but sits
below break-even ROAS at its 14% margin (loses money) (DECISION); Espresso
Machines is profitable at margin and loses ~47% impression share to budget
(the place for more money) (DECISION); Grinders loses share to rank, not
budget, so more budget buys little; the agency's "average Quality Score" is a
simple mean of keywords while the flagship keyword (most impressions) has QS 3
with a below-average landing page; "search-term waste is only X% of spend"
divides visible zero-sale cost by total spend although the visible terms are
only ~half of spend.
Decoys (2): brand CTR ~38% with the lowest CPA; exact match in Espresso
Machines carries the highest CPC but the lowest cost per sale."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-search-budget-shift"
rng = random.Random(41077)

MONTHS = ["2026-07", "2026-08", "2026-09"]
MSHARE = [0.32, 0.33, 0.35]
# campaign: product line, AOV, IS, lost budget, lost rank
CAMP = {
    "Brand - Copperline": ("mixed", 205.0, 0.94, 0.01, 0.05),
    "Generic - Espresso Machines": ("espresso_machines", 520.0, 0.38, 0.47, 0.15),
    "Generic - Grinders & Accessories": ("grinders_accessories", 152.0, 0.61, 0.03, 0.36),
    "Generic - Coffee Beans": ("coffee_beans", 46.0, 0.70, 0.04, 0.26),
}
MARGIN = {"espresso_machines": 0.32, "grinders_accessories": 0.14, "coffee_beans": 0.40, "mixed": 0.27}

# keywords: campaign -> list of (keyword, match, impressions, ctr, cpc, cvr, qs, lp_experience)
KW = {
    "Brand - Copperline": [
        ("copperline", "exact", 18800, 0.40, 0.38, 0.062, 10, "above_average"),
        ("copperline coffee", "phrase", 7600, 0.33, 0.44, 0.058, 9, "above_average"),
    ],
    "Generic - Espresso Machines": [
        ("espresso machine", "phrase", 140000, 0.052, 1.62, 0.0125, 3, "below_average"),
        ("[espresso machine with grinder]", "exact", 14800, 0.081, 2.35, 0.024, 8, "above_average"),
        ("[dual boiler espresso machine]", "exact", 9100, 0.088, 2.48, 0.026, 8, "above_average"),
        ("home espresso machine", "phrase", 21400, 0.064, 1.88, 0.016, 7, "average"),
        ("best espresso machine", "broad", 26800, 0.049, 1.41, 0.0105, 4, "average"),
        ("[lever espresso machine]", "exact", 3900, 0.077, 2.21, 0.022, 9, "above_average"),
        ("prosumer espresso machine", "phrase", 6100, 0.066, 1.95, 0.019, 8, "above_average"),
        ("[e61 espresso machine]", "exact", 2900, 0.083, 2.30, 0.025, 9, "above_average"),
    ],
    "Generic - Grinders & Accessories": [
        ("coffee grinder", "phrase", 64000, 0.071, 0.92, 0.031, 5, "average"),
        ("[burr grinder]", "exact", 22500, 0.094, 1.21, 0.042, 8, "above_average"),
        ("milk frothing jug", "phrase", 18800, 0.082, 0.66, 0.036, 8, "above_average"),
        ("espresso tamper", "broad", 24900, 0.069, 0.58, 0.029, 7, "average"),
        ("[knock box]", "exact", 6400, 0.090, 0.71, 0.041, 9, "above_average"),
        ("coffee scales", "phrase", 15600, 0.074, 0.69, 0.030, 8, "average"),
    ],
    "Generic - Coffee Beans": [
        ("espresso beans", "phrase", 31000, 0.083, 0.74, 0.044, 8, "above_average"),
        ("[specialty coffee beans]", "exact", 12400, 0.101, 0.92, 0.056, 9, "above_average"),
        ("coffee bean subscription", "broad", 14200, 0.071, 0.81, 0.038, 7, "average"),
        ("[single origin coffee]", "exact", 7200, 0.096, 0.88, 0.049, 8, "above_average"),
    ],
}

kw_rows, camp_tot = [], {c: dict(imps=0, clicks=0, cost=0.0, conv=0, val=0.0) for c in CAMP}
for c, kws in KW.items():
    aov = CAMP[c][1]
    for kw, mt, imps0, ctr, cpc, cvr, qs, lp in kws:
        imps = int(imps0 * rng.uniform(0.97, 1.03))
        clicks = int(round(imps * ctr * rng.uniform(0.97, 1.03)))
        cost = round(clicks * cpc * rng.uniform(0.98, 1.02), 2)
        conv = int(round(clicks * cvr * rng.uniform(0.95, 1.05)))
        val = round(conv * aov * rng.uniform(0.97, 1.03), 2)
        kw_rows.append([c, kw, mt, imps, clicks, cost, conv, val, qs, lp])
        t = camp_tot[c]; t["imps"] += imps; t["clicks"] += clicks; t["cost"] += cost; t["conv"] += conv; t["val"] += val

# campaign monthly rows (split keyword totals over months)
camp_rows = []
for c, (line, aov, isv, lb, lr) in CAMP.items():
    t = camp_tot[c]
    parts = {k: [] for k in ("imps", "clicks", "cost", "conv", "val")}
    for i, m in enumerate(MONTHS):
        for k in parts:
            if i < 2:
                v = t[k] * MSHARE[i] * rng.uniform(0.97, 1.03)
                v = round(v, 2) if k in ("cost", "val") else int(round(v))
            else:
                v = t[k] - sum(parts[k])
                v = round(v, 2) if k in ("cost", "val") else v
            parts[k].append(v)
    for i, m in enumerate(MONTHS):
        camp_rows.append([m, c, "Target ROAS" if c != "Brand - Copperline" else "Maximize clicks",
                          parts["imps"][i], parts["clicks"][i], parts["cost"][i], parts["conv"][i], parts["val"][i],
                          round(isv + rng.uniform(-0.02, 0.02), 2), round(lb + rng.uniform(-0.015, 0.015), 2),
                          round(lr + rng.uniform(-0.015, 0.015), 2)])

# ---------- search terms (only part of spend is visible) ----------
st_rows = []
TERMS = {
    "Generic - Espresso Machines": [
        ("how to descale espresso machine", 0), ("espresso machine repair near me", 0), ("espresso machine parts", 0),
        ("best espresso machine under 1000", 1), ("dual boiler espresso machine", 1), ("espresso machine with grinder", 1),
        ("espresso machine for home", 1), ("lever espresso machine", 1), ("second hand espresso machine", 0),
    ],
    "Generic - Grinders & Accessories": [
        ("burr grinder", 1), ("coffee grinder electric", 1), ("how to clean coffee grinder", 0), ("milk jug 600ml", 1),
        ("espresso tamper 58mm", 1), ("grinder burr replacement", 0), ("coffee scales with timer", 1),
    ],
    "Generic - Coffee Beans": [
        ("espresso beans", 1), ("specialty coffee beans", 1), ("coffee bean subscription", 1),
        ("coffee beans caffeine content", 0), ("single origin coffee", 1),
    ],
}
VIS = {"Generic - Espresso Machines": 0.52, "Generic - Grinders & Accessories": 0.56, "Generic - Coffee Beans": 0.58}
WASTE = {"Generic - Espresso Machines": 0.13, "Generic - Grinders & Accessories": 0.10, "Generic - Coffee Beans": 0.08}
for c, terms in TERMS.items():
    t = camp_tot[c]; vis_cost = t["cost"] * VIS[c]
    zero = [x for x in terms if x[1] == 0]; conv_terms = [x for x in terms if x[1] == 1]
    zero_cost = vis_cost * WASTE[c]; conv_cost = vis_cost - zero_cost
    wz = [rng.uniform(0.6, 1.4) for _ in zero]; wc = [rng.uniform(0.5, 1.5) for _ in conv_terms]
    cpc_avg = t["cost"] / t["clicks"]; cpa = t["cost"] / t["conv"]
    for (term, _), w in zip(zero, wz):
        cost = round(zero_cost * w / sum(wz), 2); clicks = int(round(cost / (cpc_avg * rng.uniform(0.85, 1.1))))
        st_rows.append([c, term, int(clicks / rng.uniform(0.04, 0.08)), clicks, cost, 0, 0])
    for (term, _), w in zip(conv_terms, wc):
        cost = round(conv_cost * w / sum(wc), 2); clicks = int(round(cost / (cpc_avg * rng.uniform(0.9, 1.15))))
        conv = max(1, int(round(cost / (cpa * rng.uniform(0.6, 0.9)))))
        st_rows.append([c, term, int(clicks / rng.uniform(0.05, 0.09)), clicks, cost, conv, round(conv * CAMP[c][1], 2)])

# ---------- ground truth ----------
gen = [c for c in CAMP if c.startswith("Generic")]
roas = {c: camp_tot[c]["val"] / camp_tot[c]["cost"] for c in CAMP}
be = {c: 1 / MARGIN[CAMP[c][0]] for c in CAMP}
profit = {c: camp_tot[c]["val"] * MARGIN[CAMP[c][0]] - camp_tot[c]["cost"] for c in CAMP}
cpa = {c: camp_tot[c]["cost"] / camp_tot[c]["conv"] for c in CAMP}
ctr = {c: camp_tot[c]["clicks"] / camp_tot[c]["imps"] for c in CAMP}
lb = {c: sum(r[9] for r in camp_rows if r[1] == c) / 3 for c in CAMP}
lr = {c: sum(r[10] for r in camp_rows if r[1] == c) / 3 for c in CAMP}
G, E, B = "Generic - Grinders & Accessories", "Generic - Espresso Machines", "Brand - Copperline"
qs_mean = sum(r[8] for r in kw_rows) / len(kw_rows)
qs_w = sum(r[8] * r[3] for r in kw_rows) / sum(r[3] for r in kw_rows)
flag = max(kw_rows, key=lambda r: r[3])
gen_cost = sum(camp_tot[c]["cost"] for c in gen)
st_cost = sum(r[4] for r in st_rows)
st_zero = sum(r[4] for r in st_rows if r[5] == 0)
waste_naive = st_zero / gen_cost
waste_vis = st_zero / st_cost
cov = st_cost / gen_cost
# match type cost per sale
mt = {}
for r in kw_rows:
    if r[0] != E: continue
    d = mt.setdefault(r[2], [0, 0.0, 0]); d[0] += r[4]; d[1] += r[5]; d[2] += r[6]
mt_cpc = {k: v[1] / v[0] for k, v in mt.items()}
mt_cps = {k: v[1] / v[2] for k, v in mt.items()}

assert roas[G] == max(roas[c] for c in gen) and roas[G] < be[G] and profit[G] < 0, (roas[G], be[G])
assert roas[E] > be[E] * 1.2 and profit[E] > 0 and lb[E] > 0.4
assert lr[G] > 0.3 and lb[G] < 0.06
assert qs_mean - qs_w > 1.5 and flag[1] == "espresso machine" and flag[8] == 3
assert waste_vis > 1.7 * waste_naive and cov < 0.6
assert cpa[B] == min(cpa.values()) and ctr[B] > 0.3
assert mt_cpc["exact"] == max(mt_cpc.values()) and mt_cps["exact"] == min(mt_cps.values())

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

notes = f"""# Copperline Coffee Gear: Q3 2026 search summary (agency)

- Account Quality Score is healthy: average QS {qs_mean:.1f} across our keywords.
- Search-term hygiene is good: zero-sale search terms cost {eur(st_zero)}, only {pc(waste_naive)} of generic spend.
- Best performer: Generic - Grinders & Accessories at {roas[G]:.1f}x ROAS (target 4.0x).
- Q4 proposal: +40% budget on Grinders & Accessories, the rest flat.
"""
margins = to_csv(["product_line", "gross_margin_pct"], [[k, round(100 * v)] for k, v in MARGIN.items() if k != "mixed"])

files = {
    "resources/agency_q3_summary.md": notes,
    "resources/google_ads_campaigns_q3.csv": to_csv(
        ["month", "campaign", "bid_strategy", "impressions", "clicks", "cost", "conversions", "conv_value",
         "search_impr_share", "search_lost_is_budget", "search_lost_is_rank"], camp_rows),
    "resources/google_ads_keywords_q3.csv": to_csv(
        ["campaign", "keyword", "match_type", "impressions", "clicks", "cost", "conversions", "conv_value",
         "quality_score", "landing_page_experience"], kw_rows),
    "resources/google_ads_search_terms_q3.csv": to_csv(
        ["campaign", "search_term", "impressions", "clicks", "cost", "conversions", "conv_value"], st_rows),
    "resources/product_margins.csv": margins,
}

prompt = """
I run marketing at Copperline Coffee Gear (we sell espresso machines, grinders, accessories and beans online). Our agency sent the Q3 Google Ads exports and their summary; it's all in resources/. Where should next quarter's search budget go? Write it up in report.md with the numbers behind your call.
"""

N = 5; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (numbers computed from the files):

1. Grinders & Accessories loses money despite the best ROAS. Q3 ROAS {roas[G]:.2f}x, but the grinders/accessories margin is {pc(MARGIN['grinders_accessories'], 0)}, so break-even ROAS is {be[G]:.2f}x; gross profit after ad cost is about {eur(profit[G])}. Found if report.md says this campaign is below break-even / unprofitable once margin is applied (POAS or break-even ROAS).
2. Espresso Machines is profitable and budget-limited. ROAS {roas[E]:.2f}x vs break-even {be[E]:.2f}x (profit about {eur(profit[E])}), and it loses about {pc(lb[E], 0)} of impression share to budget. Found if report.md says it is held back by budget and is profitable / should get more budget.
3. Grinders is rank-limited, not budget-limited: about {pc(lr[G], 0)} impression share lost to rank vs {pc(lb[G], 0)} to budget, so more budget buys little. Found if report.md notes the lost-to-rank vs lost-to-budget split for Grinders (or that added budget would not be spent productively there).
4. Quality Score average is misleading. The agency's {qs_mean:.1f} is a simple mean of keyword rows; impression-weighted QS is {qs_w:.1f}. The flagship keyword "espresso machine" ({flag[3]:,} impressions, the largest) has QS {flag[8]} with a below-average landing page experience. Found if report.md flags the flagship keyword's low QS / below-average landing page OR recomputes a weighted QS near {qs_w:.1f} (within 0.4).
5. Search-term waste understated. Zero-sale terms cost {eur(st_zero)}; the agency divides by all generic spend ({eur(gen_cost)}) to get {pc(waste_naive)}, but the search-terms report only shows {eur(st_cost)} ({pc(cov, 0)} of spend). Within visible terms waste is {pc(waste_vis)}; the hidden part is unknown. Found if report.md says the search-terms report covers only part of spend (sample) or that waste is about {pc(waste_vis, 0)} of visible spend, not {pc(waste_naive)}.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N}, each with its substance (a number or the specific element). A vague "review margins" or "check Quality Score" without the specific evidence does not count.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: put the extra Q4 search budget into Generic - Espresso Machines (profitable at its {pc(MARGIN['espresso_machines'], 0)} margin: ROAS {roas[E]:.2f}x vs break-even {be[E]:.2f}x, and losing about {pc(lb[E], 0)} impression share to budget). Grinders & Accessories should NOT get more budget (ROAS {roas[G]:.2f}x is below its break-even {be[G]:.2f}x and it is rank-limited); holding or cutting it is correct.

Naive wrong answer: follow the agency and add budget to Grinders & Accessories because it has the highest ROAS ({roas[G]:.2f}x).

PASS if report.md's main budget recommendation directs additional budget to Espresso Machines (alone or as the primary destination) and does not add budget to Grinders & Accessories.
FAIL if it recommends increasing Grinders & Accessories, endorses the agency's +40% plan, or makes no clear budget call.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Brand - Copperline has CTR {pc(ctr[B])} and the lowest CPA ({eur(cpa[B])}). High CTR and cheap conversions are normal for brand terms. (Saying brand should be read separately from generic, or that brand incrementality is untested, is fine.)
- D2. In Generic - Espresso Machines, exact-match keywords have the highest CPC ({eur(mt_cpc['exact'])} vs {eur(mt_cpc['phrase'])} phrase, {eur(mt_cpc['broad'])} broad) but the lowest cost per sale ({eur(mt_cps['exact'])} vs {eur(mt_cps['phrase'])} phrase, {eur(mt_cps['broad'])} broad). Precise matches cost more per click; cost per sale is the read.

PASS if report.md does not call the brand CTR/CPA an error or anomaly, and does not recommend cutting exact-match bids or moving budget away from exact match because its CPC is high.
FAIL if either decoy is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: G roas {roas[G]:.2f} be {be[G]:.2f} profit {profit[G]:.0f}; E roas {roas[E]:.2f} be {be[E]:.2f} lb {lb[E]:.2f}; "
      f"QS mean {qs_mean:.2f} w {qs_w:.2f}; waste naive {waste_naive:.3f} vis {waste_vis:.3f} cov {cov:.2f}")
