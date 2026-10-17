"""Breadth benchmark, paid search: B2B lead gen quarter review before a CMO meeting (Fernhill CRM, Q3 2026).

Subtle problems (4): pricing_page_view became a primary Google conversion on
1 August, so the agency's "CPA down X% July to September" is an artefact; on
CRM demo requests cost per lead rose; the Microsoft Ads demo goal counts
"every" conversion, so Microsoft platform conversions are ~2x the unique
leads the CRM received from Bing (its "lowest CPA" is inflated); Generic -
Free CRM has the lowest cost per lead but an SQL rate near 3%, the worst cost
per SQL (DECISION); Germany is blended into a "within target" cost per SQL
while DE generic runs well above the EUR 900 ceiling.
Decoys (2): Microsoft CPC ~35% below Google's on the same campaigns (normal);
brand CTR ~40% with the lowest cost per SQL."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-search-b2b-leads"
rng = random.Random(66120)
MONTHS = ["2026-07", "2026-08", "2026-09"]
MAX_CPSQL = 900.0

# (engine, market, campaign): monthly cost, cpc, ctr, lead rate per click, sql rate
UNITS = {
    ("google", "UK", "Brand - Fernhill"): (2200, 2.20, 0.41, 0.080, 0.42),
    ("google", "UK", "Generic - CRM Software"): (9800, 6.20, 0.052, 0.034, 0.24),
    ("google", "UK", "Generic - Sales Pipeline Tool"): (5200, 5.10, 0.061, 0.037, 0.30),
    ("google", "UK", "Generic - Free CRM"): (6400, 2.40, 0.074, 0.060, 0.03),
    ("google", "DE", "Brand - Fernhill"): (700, 1.90, 0.38, 0.070, 0.36),
    ("google", "DE", "Generic - CRM Software"): (6900, 5.60, 0.047, 0.022, 0.12),
    ("google", "DE", "Generic - Sales Pipeline Tool"): (3100, 4.70, 0.053, 0.020, 0.11),
    ("microsoft", "UK", "Brand - Fernhill"): (500, 1.40, 0.43, 0.055, 0.40),
    ("microsoft", "UK", "Generic - CRM Software"): (2600, 4.00, 0.049, 0.022, 0.22),
    ("microsoft", "UK", "Generic - Sales Pipeline Tool"): (1500, 3.30, 0.058, 0.024, 0.27),
}
PRICING_PER_CLICK = 0.03   # pricing page views per click, counted as Google conversions from August
MS_DUP = 2.3                # Microsoft "every" counting multiplier
TREND = {"2026-07": 0.95, "2026-08": 1.0, "2026-09": 1.06}   # cost trend
LEAD_DRIFT = {"2026-07": 1.0, "2026-08": 0.93, "2026-09": 0.86}  # true lead rate drifts down

ads_rows, crm_rows = [], []
for m in MONTHS:
    for (eng, mk, c), (cost0, cpc, ctr, lr, sr) in UNITS.items():
        cost = round(cost0 * TREND[m] * rng.uniform(0.96, 1.04), 2)
        clicks = int(cost / (cpc * rng.uniform(0.96, 1.04)))
        imps = int(clicks / (ctr * rng.uniform(0.95, 1.05)))
        leads = max(1, int(round(clicks * lr * LEAD_DRIFT[m] * rng.uniform(0.92, 1.08))))
        sqls = int(round(leads * sr * rng.uniform(0.9, 1.1)))
        if eng == "google":
            conv = leads + (int(round(clicks * PRICING_PER_CLICK * rng.uniform(0.9, 1.1))) if m != "2026-07" else 0)
        else:
            conv = int(round(leads * MS_DUP * rng.uniform(0.95, 1.05)))
        ads_rows.append([m, eng, mk, c, imps, clicks, cost, conv])
        crm_rows.append([m, "google" if eng == "google" else "bing", "cpc", mk, c, leads, sqls])

goals = [
    ["google", "demo_request", "primary", "one", "2025-11-02", ""],
    ["google", "pricing_page_view", "primary", "one", "2026-08-01", "added as primary to give Smart Bidding more signal"],
    ["google", "newsletter_signup", "secondary", "one", "2025-11-02", ""],
    ["microsoft", "demo_request (UET)", "primary", "every", "2026-02-14", ""],
]

# ---------- ground truth ----------
def agg(rows, key, idx):
    out = {}
    for r in rows:
        k = key(r); out.setdefault(k, [0.0] * len(idx))
        for j, i in enumerate(idx): out[k][j] += r[i]
    return out
cost_m = agg(ads_rows, lambda r: r[0], [6, 7])
leads_m = agg(crm_rows, lambda r: r[0], [5, 6])
cpa_plat = {m: cost_m[m][0] / cost_m[m][1] for m in MONTHS}
cpl = {m: cost_m[m][0] / leads_m[m][0] for m in MONTHS}
cpa_drop = 1 - cpa_plat["2026-09"] / cpa_plat["2026-07"]
cpl_change = cpl["2026-09"] / cpl["2026-07"] - 1

eng_cost = agg(ads_rows, lambda r: r[1], [6, 7])
eng_crm = agg(crm_rows, lambda r: r[1], [5, 6])
ms_cpa = eng_cost["microsoft"][0] / eng_cost["microsoft"][1]
g_cpa = eng_cost["google"][0] / eng_cost["google"][1]
ms_ratio = eng_cost["microsoft"][1] / eng_crm["bing"][0]
ms_cpl = eng_cost["microsoft"][0] / eng_crm["bing"][0]
g_cpl = eng_cost["google"][0] / eng_crm["google"][0]

camp_cost = agg(ads_rows, lambda r: r[3], [6, 7, 5, 4])
camp_crm = agg(crm_rows, lambda r: r[4], [5, 6])
c_cpa = {c: camp_cost[c][0] / camp_cost[c][1] for c in camp_cost}
c_cpl = {c: camp_cost[c][0] / camp_crm[c][0] for c in camp_cost}
c_cpsql = {c: camp_cost[c][0] / camp_crm[c][1] for c in camp_cost}
c_sqlr = {c: camp_crm[c][1] / camp_crm[c][0] for c in camp_cost}
FREE, BRAND = "Generic - Free CRM", "Brand - Fernhill"
gen = [c for c in camp_cost if c.startswith("Generic")]
best_gen = min(gen, key=lambda c: c_cpsql[c])

mk_cost = agg(ads_rows, lambda r: r[2], [6]); mk_crm = agg(crm_rows, lambda r: r[3], [6])
mk_cpsql = {k: mk_cost[k][0] / mk_crm[k][0] for k in mk_cost}
de_gen_cost = sum(r[6] for r in ads_rows if r[2] == "DE" and r[3].startswith("Generic"))
de_gen_sql = sum(r[6] for r in crm_rows if r[3] == "DE" and r[4].startswith("Generic"))
de_gen_cpsql = de_gen_cost / de_gen_sql
tot_cpsql = sum(r[6] for r in ads_rows) / sum(r[6] for r in crm_rows)

# CPC decoy: Microsoft vs Google UK same campaigns
def cpc_of(eng):
    rr = [r for r in ads_rows if r[1] == eng and r[2] == "UK" and r[3] != "Generic - Free CRM"]
    return sum(r[6] for r in rr) / sum(r[5] for r in rr)
ms_cpc, guk_cpc = cpc_of("microsoft"), cpc_of("google")
b_ctr = camp_cost[BRAND][2] / camp_cost[BRAND][3]

assert cpa_drop > 0.2 and cpl_change > 0.08, (cpa_drop, cpl_change)
assert ms_cpa < 0.85 * g_cpa and 2.1 < ms_ratio < 2.5 and ms_cpl > 0.9 * g_cpl
assert c_cpl[FREE] == min(c_cpl[c] for c in gen) and c_cpa[FREE] == min(c_cpa[c] for c in gen)
assert c_cpsql[FREE] == max(c_cpsql.values()) and c_sqlr[FREE] < 0.06
assert tot_cpsql < MAX_CPSQL and de_gen_cpsql > 1.5 * MAX_CPSQL and mk_cpsql["UK"] < MAX_CPSQL
assert ms_cpc < 0.75 * guk_cpc
assert c_cpsql[BRAND] == min(c_cpsql.values()) and b_ctr > 0.35

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

summary = f"""# Fernhill CRM: paid search Q3 2026 (agency summary)

- Efficiency is improving: CPA fell from {eur(cpa_plat['2026-07'])} in July to {eur(cpa_plat['2026-09'])} in September ({pc(cpa_drop)} lower).
- Microsoft Ads delivers our lowest CPA ({eur(ms_cpa)} vs {eur(g_cpa)} on Google). Proposal: +50% Microsoft budget in Q4.
- Among generic campaigns, Generic - Free CRM has the lowest CPA ({eur(c_cpa[FREE])}). Proposal: +30% budget.
- Pipeline quality: blended cost per SQL {eur(tot_cpsql)}, within the €{MAX_CPSQL:,.0f} ceiling.
"""

files = {
    "resources/agency_q3_summary.md": summary,
    "resources/search_ads_monthly_q3.csv": to_csv(
        ["month", "engine", "market", "campaign", "impressions", "clicks", "cost", "conversions"], ads_rows),
    "resources/conversion_goals.csv": to_csv(["engine", "goal", "status", "count", "last_changed", "change_note"], goals),
    "resources/crm_leads_by_source_q3.csv": to_csv(
        ["month", "utm_source", "utm_medium", "market", "utm_campaign", "demo_requests", "sqls"], crm_rows),
}

prompt = """
I'm presenting our Q3 paid search results to the CMO tomorrow. We're Fernhill CRM (B2B software, UK and Germany). The agency's summary, the Google and Microsoft Ads export, the conversion goal settings and our CRM lead export are in resources/. Anything I'm missing? Tell me what to present and what you'd recommend for Q4 budget, in report.md.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. The CPA improvement is an artefact. pricing_page_view was added as a primary Google conversion on 2026-08-01, so August and September conversions include page views. Platform CPA fell {pc(cpa_drop)} ({eur(cpa_plat['2026-07'])} to {eur(cpa_plat['2026-09'])}), but cost per CRM demo request rose {pc(cpl_change)} ({eur(cpl['2026-07'])} to {eur(cpl['2026-09'])}). Found if report.md says the pricing_page_view goal change inflates conversions / invalidates the CPA trend.
2. Microsoft conversions double-count. The Microsoft demo goal counts "every"; Microsoft reported {eng_cost['microsoft'][1]:.0f} conversions vs {eng_crm['bing'][0]:.0f} demo requests in the CRM from Bing ({ms_ratio:.2f}x). Microsoft's platform CPA {eur(ms_cpa)} becomes {eur(ms_cpl)} per CRM lead (Google {eur(g_cpl)}). Found if report.md flags the count=every setting or that Microsoft conversions exceed CRM leads.
3. Free CRM is cheap leads, expensive pipeline. Generic - Free CRM has the lowest cost per lead among generic campaigns ({eur(c_cpl[FREE])}) but an SQL rate of {pc(c_sqlr[FREE], 1)}, giving the highest cost per SQL ({eur(c_cpsql[FREE])}) vs {eur(c_cpsql[best_gen])} for {best_gen}. Found if report.md judges Free CRM on SQLs/cost per SQL and says it is the worst or should not be scaled.
4. Germany is hidden in the blend. Blended cost per SQL is {eur(tot_cpsql)} (within the €{MAX_CPSQL:,.0f} ceiling), but DE generic campaigns run at {eur(de_gen_cpsql)} per SQL while UK is {eur(mk_cpsql['UK'])}. Found if report.md splits by market and says DE (generic) is above the ceiling.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation for Q4: do not scale on platform CPA. Specifically, do NOT give Generic - Free CRM +30% (worst cost per SQL, {eur(c_cpsql[FREE])}) and do NOT give Microsoft +50% on its inflated CPA; cut or cap Free CRM and move budget toward campaigns with the lowest cost per SQL (best generic: {best_gen}, {eur(c_cpsql[best_gen])} per SQL; brand is cheapest overall). Also acceptable as the main recommendation: re-basing all reporting on CRM demo requests/SQLs and, on that basis, cutting Free CRM and/or DE generic.

Naive wrong answer: follow the agency, scaling Microsoft +50% and Free CRM +30% because of their lowest CPA, and presenting the {pc(cpa_drop)} CPA improvement.

PASS if report.md's main Q4 recommendation rejects scaling Free CRM (recommends cutting, capping or not increasing it) and does not endorse +50% Microsoft on its platform CPA.
FAIL if it endorses scaling Free CRM or Microsoft on their CPA, or presents the CPA drop as a real efficiency gain.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Microsoft's CPC in the UK ({eur(ms_cpc)}) is about {pc(1 - ms_cpc / guk_cpc)} below Google UK's ({eur(guk_cpc)}) on the three campaigns both engines run (Brand, CRM Software, Sales Pipeline Tool). Microsoft Ads usually has cheaper clicks and fewer bidders. (Flagging Microsoft's conversion counting is correct and is a separate issue.)
- D2. Brand - Fernhill has CTR about {pc(b_ctr)} and the lowest cost per SQL ({eur(c_cpsql[BRAND])}). Normal for brand terms.

PASS if report.md does not present the lower Microsoft CPC as a data or tracking error, and does not call the brand CTR or brand cost per SQL suspicious.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: CPA drop {cpa_drop:.2f}, CPL change {cpl_change:+.2f}; MS ratio {ms_ratio:.2f} cpa {ms_cpa:.0f} vs g {g_cpa:.0f}, cpl {ms_cpl:.0f} vs {g_cpl:.0f}; "
      f"Free cpl {c_cpl[FREE]:.0f} cpsql {c_cpsql[FREE]:.0f}; best gen {best_gen} {c_cpsql[best_gen]:.0f}; DE gen {de_gen_cpsql:.0f} tot {tot_cpsql:.0f}")
