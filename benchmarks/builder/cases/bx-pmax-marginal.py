"""Breadth benchmark, Performance Max: monthly review and October budget (Larchmont Home, Jul-Sep 2026).

Subtle problems (4): PMax conversion value includes modelled "Store visits"
(about a quarter of September value) although the question is online sales;
the August-to-September budget increase bought purchase value at a marginal
ROAS far below break-even (average ROAS still looks fine) (DECISION);
Standard Shopping lost about as many purchases as PMax gained, so combined
Shopping + PMax purchases barely moved while cost rose sharply
(cannibalisation); Display and YouTube take ~30% of PMax cost for ~3% of its
purchases (channel report).
Decoys (2): PMax CPA above Brand Search CPA; one small asset group with no
conversions on a few hundred euros of spend (sparsity)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-pmax-marginal"
rng = random.Random(30551)
MONTHS = ["2026-07", "2026-08", "2026-09"]
MARGIN = 0.38
AOV = 168.0
STORE_VISIT_VALUE = 22.0

# PMax monthly: cost, purchases (online), store visits
PM = {"2026-07": (9800, 252, 0), "2026-08": (14200, 338, 420), "2026-09": (21600, 372, 800)}
SH = {"2026-07": (11200, 262), "2026-08": (10800, 196), "2026-09": (10500, 151)}
BR = {"2026-07": (2100, 240), "2026-08": (2150, 236), "2026-09": (2200, 244)}

camp_rows, act_rows = [], []
pm = {}
for m in MONTHS:
    cost, pur, sv = PM[m]
    cost = round(cost * rng.uniform(0.99, 1.01), 2)
    pval = round(pur * AOV * rng.uniform(0.97, 1.03), 2)
    sval = round(sv * STORE_VISIT_VALUE, 2)
    clicks = int(cost / (0.71 * (1 + 0.18 * MONTHS.index(m)) * rng.uniform(0.97, 1.03)))
    imps = int(clicks / rng.uniform(0.011, 0.014))
    camp_rows.append([m, "PMax - All Products", "PERFORMANCE_MAX", cost, imps, clicks, pur + sv, round(pval + sval, 2)])
    act_rows += [[m, "PMax - All Products", "Purchase", pur, pval], [m, "PMax - All Products", "Store visits", sv, sval]]
    pm[m] = dict(cost=cost, pur=pur, pval=pval, sv=sv, sval=sval)
    c2, p2 = SH[m]; c2 = round(c2 * rng.uniform(0.99, 1.01), 2)
    cl2 = int(c2 / (0.62 * rng.uniform(0.97, 1.03)))
    camp_rows.append([m, "Shopping - All Products", "SHOPPING", c2, int(cl2 / rng.uniform(0.009, 0.012)), cl2, p2, round(p2 * AOV * rng.uniform(0.97, 1.03), 2)])
    act_rows.append([m, "Shopping - All Products", "Purchase", p2, camp_rows[-1][7]])
    c3, p3 = BR[m]; c3 = round(c3 * rng.uniform(0.99, 1.01), 2)
    cl3 = int(c3 / (0.38 * rng.uniform(0.97, 1.03)))
    camp_rows.append([m, "Brand Search", "SEARCH", c3, int(cl3 / rng.uniform(0.33, 0.38)), cl3, p3, round(p3 * AOV * rng.uniform(0.97, 1.03), 2)])
    act_rows.append([m, "Brand Search", "Purchase", p3, camp_rows[-1][7]])

# September channel report for PMax
sep = pm["2026-09"]
CH = [("Search", 0.36, 0.52), ("Shopping", 0.33, 0.45), ("Display", 0.17, 0.02), ("YouTube", 0.11, 0.01), ("Discover", 0.02, 0.0), ("Gmail", 0.01, 0.0)]
ch_rows = []; ac = ap = 0
for j, (ch, cs, ps) in enumerate(CH):
    if j < len(CH) - 1:
        c = round(sep["cost"] * cs, 2); p = int(round(sep["pur"] * ps))
    else:
        c = round(sep["cost"] - ac, 2); p = sep["pur"] - ap
    ac += c; ap += p
    imps = int(c / {"Search": 9.0, "Shopping": 6.5, "Display": 1.3, "YouTube": 4.2, "Discover": 3.0, "Gmail": 2.5}[ch] * 1000)
    clk = int(imps * {"Search": 0.06, "Shopping": 0.012, "Display": 0.0042, "YouTube": 0.003, "Discover": 0.006, "Gmail": 0.008}[ch])
    ch_rows.append(["2026-09", "PMax - All Products", ch, imps, clk, c, p])

# September asset groups (purchases only)
AG = [("Sofas & Chairs", 0.41, 0.46), ("Lighting", 0.27, 0.28), ("Rugs & Textiles", 0.305, 0.26), ("Outdoor Clearance", 0.015, 0.0)]
ag_rows = []; ac = ap = 0
for j, (g, cs, ps) in enumerate(AG):
    if j < len(AG) - 1:
        c = round(sep["cost"] * cs, 2); p = int(round(sep["pur"] * ps))
    else:
        c = round(sep["cost"] - ac, 2); p = sep["pur"] - ap
    ac += c; ap += p
    ag_rows.append(["2026-09", "PMax - All Products", g, c, p, round(p * AOV * rng.uniform(0.95, 1.05), 2)])

# ---------- ground truth ----------
def row(m, c): return [r for r in camp_rows if r[0] == m and r[1] == c][0]
P, S, Bn = "PMax - All Products", "Shopping - All Products", "Brand Search"
roas_rep = {m: row(m, P)[7] / row(m, P)[3] for m in MONTHS}
roas_pur = {m: pm[m]["pval"] / pm[m]["cost"] for m in MONTHS}
sv_share = sep["sval"] / (sep["pval"] + sep["sval"])
be = 1 / MARGIN
d_cost = pm["2026-09"]["cost"] - pm["2026-08"]["cost"]
d_val = pm["2026-09"]["pval"] - pm["2026-08"]["pval"]
mroas = d_val / d_cost
# combined PMax + Shopping purchases and cost
comb = {m: (row(m, P)[3] + row(m, S)[3], pm[m]["pur"] + row(m, S)[6], pm[m]["pval"] + row(m, S)[7]) for m in MONTHS}
comb_pur_chg = comb["2026-09"][1] / comb["2026-07"][1] - 1
comb_cost_chg = comb["2026-09"][0] / comb["2026-07"][0] - 1
pm_gain = pm["2026-09"]["pur"] - pm["2026-07"]["pur"]
sh_loss = row("2026-07", S)[6] - row("2026-09", S)[6]
comb_mroas = (comb["2026-09"][2] - comb["2026-07"][2]) / (comb["2026-09"][0] - comb["2026-07"][0])
dv_cost = sum(r[5] for r in ch_rows if r[2] in ("Display", "YouTube"))
dv_pur = sum(r[6] for r in ch_rows if r[2] in ("Display", "YouTube"))
pm_cpa = sep["cost"] / sep["pur"]; br_cpa = row("2026-09", Bn)[3] / row("2026-09", Bn)[6]
small = ag_rows[-1]

assert roas_rep["2026-09"] > 3.0 and 0.2 < sv_share < 0.3
assert mroas < 0.6 * be and roas_pur["2026-09"] > be * 0.95, (mroas, roas_pur)
assert comb_pur_chg < 0.06 and comb_cost_chg > 0.45 and 0.6 < sh_loss / pm_gain < 1.1 and comb_mroas < 1.0
assert 0.25 < dv_cost / sep["cost"] < 0.32 and dv_pur / sep["pur"] < 0.05
assert pm_cpa > 3 * br_cpa and small[4] == 0 and small[3] < 400

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

notes = f"""# Larchmont Home: Google Ads September update (agency)

- Performance Max ROAS {roas_rep['2026-09']:.2f}x in September, above our 3.0x target, with conversions up {pc(row('2026-09', P)[6] / row('2026-07', P)[6] - 1)} since July as we scaled budget.
- PMax is now our biggest Google campaign. Proposal for October: raise PMax to €26,000 (from {eur(sep['cost'])}).
- Standard Shopping is softening; we suggest pausing it in November and letting PMax take over.
- Gross margin on online orders is about {pc(MARGIN)}.
"""

files = {
    "resources/agency_update_sep2026.md": notes,
    "resources/google_ads_campaigns_monthly.csv": to_csv(
        ["month", "campaign", "campaign_type", "cost", "impressions", "clicks", "conversions", "conv_value"], camp_rows),
    "resources/google_ads_conversions_by_action.csv": to_csv(["month", "campaign", "conversion_action", "conversions", "conv_value"], act_rows),
    "resources/pmax_channel_report_sep2026.csv": to_csv(["month", "campaign", "channel", "impressions", "clicks", "cost", "purchases"], ch_rows),
    "resources/pmax_asset_groups_sep2026.csv": to_csv(["month", "campaign", "asset_group", "cost", "purchases", "purchase_value"], ag_rows),
}

prompt = """
We're Larchmont Home, an online furniture and homeware shop. How did Performance Max do last quarter, and should we approve the agency's October budget? Their update and the Google Ads exports are in resources/. Write report.md with the numbers and your recommendation.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Store visits in the value. PMax conv_value includes modelled "Store visits" ({sep['sv']} in September worth {eur(sep['sval'])}, {pc(sv_share)} of PMax value). Purchase-only ROAS in September is {roas_pur['2026-09']:.2f}x vs the reported {roas_rep['2026-09']:.2f}x. Found if report.md separates store visits from purchases and reads PMax on purchases.
2. Marginal return of the last increase. August to September PMax cost rose {eur(d_cost)} while purchase value rose {eur(d_val)}: marginal ROAS {mroas:.2f}x vs break-even {be:.2f}x at {pc(MARGIN)} margin, although the September average purchase ROAS is {roas_pur['2026-09']:.2f}x. Found if report.md computes the incremental/marginal return of the added budget (or says the extra spend returned far less than the average) with a number.
3. Cannibalisation of Standard Shopping. From July to September PMax purchases rose by {pm_gain} while Standard Shopping fell by {sh_loss}; combined PMax + Shopping purchases changed {pc(comb_pur_chg, 1)} while their combined cost rose {pc(comb_cost_chg)}. Found if report.md says PMax growth came largely from Shopping (overlap / shift) or reads the two together.
4. Display and YouTube inside PMax. In September Display + YouTube took {eur(dv_cost)} ({pc(dv_cost / sep['cost'])} of PMax cost) for {dv_pur} of {sep['pur']} purchases ({pc(dv_pur / sep['pur'])}). Found if report.md flags this spend share vs purchase share.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: do NOT approve the increase to €26,000. Hold PMax at or below its current level (pulling back toward the August level of about {eur(pm['2026-08']['cost'])} is the strongest answer), because the last increase returned a marginal purchase ROAS of {mroas:.2f}x (break-even {be:.2f}x) and mostly shifted purchases from Standard Shopping. Fixing the conversion setup (purchases only) before any scaling is consistent with this.

Naive wrong answer: approve or increase the PMax budget because reported ROAS ({roas_rep['2026-09']:.2f}x) beats the 3.0x target, and/or pause Standard Shopping.

PASS if report.md's main recommendation rejects the €26,000 increase (hold, cut, or freeze pending a test).
FAIL if it approves the increase or any PMax budget rise, or recommends pausing Standard Shopping as the main action.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. PMax CPA ({eur(pm_cpa)} per purchase in September) is far above Brand Search CPA ({eur(br_cpa)}). Brand terms are cheap by nature; this gap is not a PMax fault in itself.
- D2. Asset group "Outdoor Clearance" has no purchases on {eur(small[3])} of spend: too little spend to read (sparsity).

PASS if report.md does not present D1 as a reason PMax is failing (comparing it to brand as a problem) and does not recommend pausing Outdoor Clearance because it has zero conversions (noting it is too small to judge is fine).
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: rep roas {roas_rep['2026-09']:.2f} pur {roas_pur['2026-09']:.2f} sv {sv_share:.2f}; mroas {mroas:.2f} vs be {be:.2f}; "
      f"comb pur {comb_pur_chg:+.3f} cost {comb_cost_chg:+.2f} ({sh_loss}/{pm_gain}); dv {dv_cost / sep['cost']:.2f}")
