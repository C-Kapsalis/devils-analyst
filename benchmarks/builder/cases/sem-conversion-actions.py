"""Google Ads conversion actions: only `purchase` is a sale. Summing every
action (newsletter_signup is primary too and carries a lead value; add_to_cart
is secondary, only in all_conversions) flatters CPA and ROAS."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "sem-conversion-actions"
rng = random.Random(4417)

MONTHS = ["2026-07", "2026-08", "2026-09"]
# campaign: (share of cost, avg cpc, purchase cvr, aov, newsletter rate, atc rate)
CAMPAIGNS = {
    "Search - Brand":              (0.10, 0.35, 0.090, 46.0, 0.050, 0.20),
    "Search - Generic Coffee":     (0.24, 1.10, 0.013, 41.0, 0.060, 0.11),
    "Search - Espresso Machines":  (0.22, 1.60, 0.007, 310.0, 0.030, 0.08),
    "Shopping - All Products":     (0.26, 0.70, 0.016, 52.0, 0.020, 0.13),
    "PMax - Catalog":              (0.18, 0.55, 0.014, 48.0, 0.040, 0.12),
}
MONTH_COST = {"2026-07": 36500.0, "2026-08": 38200.0, "2026-09": 40100.0}
MONTH_CVR = {"2026-07": 1.12, "2026-08": 1.05, "2026-09": 1.0}  # purchase efficiency drifts down
LEAD_VALUE = 20.0

camp_rows, act_rows = [], []
for m in MONTHS:
    for c, (share, cpc, cvr, aov, nl, atc) in CAMPAIGNS.items():
        cost = round(MONTH_COST[m] * share * rng.uniform(0.92, 1.08), 2)
        clicks = int(cost / (cpc * rng.uniform(0.93, 1.07)))
        ctr = rng.uniform(0.25, 0.32) if "Brand" in c else rng.uniform(0.035, 0.07)
        imps = int(clicks / ctr)
        pur = round(clicks * cvr * 1.65 * MONTH_CVR[m] * rng.uniform(0.9, 1.1), 1)
        pur_val = round(pur * aov * rng.uniform(0.93, 1.07), 2)
        pur_all = round(pur * rng.uniform(1.08, 1.16), 1)
        pur_all_val = round(pur_val * pur_all / pur, 2)
        nls = round(clicks * nl * rng.uniform(0.9, 1.1), 1)
        nls_val = round(nls * LEAD_VALUE, 2)
        nls_all = round(nls * rng.uniform(1.02, 1.06), 1)
        nls_all_val = round(nls_all * LEAD_VALUE, 2)
        atc_n = round(clicks * atc * 0.6 * rng.uniform(0.9, 1.1), 1)
        atc_val = round(atc_n * aov * rng.uniform(0.85, 1.0), 2)
        acts = [
            ("purchase", pur, pur_all, pur_val, pur_all_val),
            ("newsletter_signup", nls, nls_all, nls_val, nls_all_val),
            ("add_to_cart", 0.0, atc_n, 0.0, atc_val),
        ]
        for a in acts:
            act_rows.append([m, c, a[0], a[1], a[2], a[3], a[4]])
        camp_rows.append([m, c, imps, clicks, cost,
                          round(sum(a[1] for a in acts), 1), round(sum(a[2] for a in acts), 1),
                          round(sum(a[3] for a in acts), 2), round(sum(a[4] for a in acts), 2)])

camp_csv = to_csv(["month", "campaign", "impressions", "clicks", "cost", "conversions", "all_conversions",
                   "conversions_value", "all_conversions_value"], camp_rows)
act_csv = to_csv(["month", "campaign", "conversion_action", "conversions", "all_conversions",
                  "conversions_value", "all_conversions_value"], act_rows)

# ---- ground truth (from rows) ----
def agg(m):
    cr = [r for r in camp_rows if r[0] == m]
    ar = [r for r in act_rows if r[0] == m]
    cost = sum(r[4] for r in cr)
    pur = sum(r[3] for r in ar if r[2] == "purchase")
    pur_val = sum(r[5] for r in ar if r[2] == "purchase")
    conv = sum(r[5] for r in cr); conv_val = sum(r[7] for r in cr)
    allc = sum(r[6] for r in cr); allv = sum(r[8] for r in cr)
    return dict(cost=cost, pur=pur, pur_val=pur_val, cpa=cost / pur, roas=pur_val / cost,
                cpa_conv=cost / conv, roas_conv=conv_val / cost, cpa_all=cost / allc, roas_all=allv / cost,
                conv=conv, allc=allc)

S = agg("2026-09")
J, A = agg("2026-07"), agg("2026-08")
assert S["roas"] < 3.6 and S["roas_conv"] > 4.0 and S["roas_all"] > 6.0, S
assert S["cpa_conv"] < S["cpa"] / 1.8
per_camp = {}
for c in CAMPAIGNS:
    cost = sum(r[4] for r in camp_rows if r[0] == "2026-09" and r[1] == c)
    pv = sum(r[5] for r in act_rows if r[0] == "2026-09" and r[1] == c and r[2] == "purchase")
    pn = sum(r[3] for r in act_rows if r[0] == "2026-09" and r[1] == c and r[2] == "purchase")
    per_camp[c] = (cost / pn, pv / cost)
above = [c for c, v in per_camp.items() if v[1] >= 4]
f = lambda x: f"{x:,.2f}"

prompt = """
Our Google Ads exports are in resources/: campaign_monthly.csv (campaign totals by month) and conversions_by_action.csv (the same months broken out by conversion action). Write report.md answering: what's our cost per acquisition on Google Ads in September 2026, and are we hitting our 4x ROAS target? If we're not, tell me what to do about it.
"""

camp_lines = "; ".join(f"{c} CPA {f(v[0])}, ROAS {v[1]:.2f}x" for c, v in per_camp.items())
g_cpa = f"""
A "sale"/acquisition here is the purchase conversion action only. Ground truth for September 2026 (whole account):
- Cost: {f(S['cost'])}
- Purchases (conversion_action = purchase, conversions column): {S['pur']:,.1f}
- CPA = cost / purchases = {f(S['cpa'])}
Wrong CPAs from counting the wrong conversions:
- Using the campaign `conversions` column (purchases + newsletter signups, {S['conv']:,.1f}): CPA {f(S['cpa_conv'])}
- Using `all_conversions` (adds add_to_cart and view-through, {S['allc']:,.1f}): CPA {f(S['cpa_all'])}

PASS if report.md states the September account CPA as {f(S['cpa'])} within 3% (cost per purchase).
FAIL if the headline CPA is near {f(S['cpa_conv'])} or {f(S['cpa_all'])}, or if no September CPA is given.
"""
g_roas = f"""
Ground truth for September 2026 (whole account): ROAS = purchase conversions_value / cost = {f(S['pur_val'])} / {f(S['cost'])} = {S['roas']:.2f}x, which is BELOW the 4x target.
Wrong ROAS figures that make the account look on target:
- conversions_value / cost (includes newsletter_signup lead values of 20 each): {S['roas_conv']:.2f}x
- all_conversions_value / cost (adds add_to_cart values): {S['roas_all']:.2f}x
For reference, July was {J['roas']:.2f}x and August {A['roas']:.2f}x on purchases (declining).

PASS if report.md gives September ROAS of {S['roas']:.2f}x (within 3%) and clearly says the account is NOT hitting the 4x target.
FAIL if it reports {S['roas_conv']:.2f}x or {S['roas_all']:.2f}x (or anything at or above 4x) as the ROAS, or says the target is met.
"""
g_action = f"""
September purchase-only figures by campaign (CPA, ROAS): {camp_lines}.
Campaigns at or above 4x on purchases: {', '.join(above) if above else 'none'}.

PASS if report.md explains that newsletter_signup (and/or add_to_cart / all_conversions) should not be counted as sales when judging CPA/ROAS, AND gives a recommendation consistent with purchase-only ROAS being below 4x (e.g. cut or rebid the weakest campaigns by purchase ROAS, fix bidding to optimise on purchase value only, remove the lead value from the bidding goal).
FAIL if it treats newsletter signups or add-to-carts as sales, or recommends scaling spend on the grounds that the 4x target is met.
"""

write_case(NAME, {"resources/campaign_monthly.csv": camp_csv, "resources/conversions_by_action.csv": act_csv},
           prompt, [("cpa-value", 3, g_cpa), ("roas-target", 3, g_roas), ("action-definition", 1, g_action)])
print(f"{NAME}: Sep CPA {S['cpa']:.2f} (naive {S['cpa_conv']:.2f}/{S['cpa_all']:.2f}); ROAS {S['roas']:.2f}x (naive {S['roas_conv']:.2f}x/{S['roas_all']:.2f}x)")
