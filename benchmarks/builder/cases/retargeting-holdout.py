"""Retargeting reports ROAS ~8 because it claims purchases from people who
would have bought anyway. The conversion lift study shows control converts
almost as much: incremental ROAS < 1, profit negative even at the upper end of
the confidence interval. Don't double the budget."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "retargeting-holdout"
rng = random.Random(7311)

AOV = 76.0
MARGIN = 0.42
MONTHS = ["2026-07", "2026-08", "2026-09"]
# campaign: (objective, monthly spend, CPM, link CTR, reported ROAS)
CAMPAIGNS = {
    "Prospecting - Broad":           ("OUTCOME_SALES", 24000, 9.0, 0.011, 1.9),
    "Prospecting - Lookalike 3%":    ("OUTCOME_SALES", 16500, 10.2, 0.012, 2.2),
    "Retargeting - Cart & Site 14d": ("OUTCOME_SALES", 21000, 14.5, 0.022, 8.1),
    "Advantage+ Shopping":           ("OUTCOME_SALES", 30000, 8.6, 0.013, 2.6),
}
rows = []
for m in MONTHS:
    for c, (obj, sp, cpm, ctr, roas) in CAMPAIGNS.items():
        spend = round(sp * rng.uniform(0.94, 1.06), 2)
        imps = int(spend / cpm * 1000 * rng.uniform(0.95, 1.05))
        clicks = int(imps * ctr * rng.uniform(0.92, 1.08))
        value = round(spend * roas * rng.uniform(0.95, 1.05), 2)
        purchases = int(round(value / (AOV * rng.uniform(0.97, 1.03))))
        rows.append([m, c, obj, spend, imps, clicks, purchases, value])
camp_csv = to_csv(["month", "campaign_name", "objective", "spend", "impressions", "inline_link_clicks",
                   "purchases", "purchase_value"], rows)

# conversion lift study on the retargeting campaign, September (80/20 split)
NT, NC = 182400, 45600
PC, PT = 0.0230, 0.02415
def binom_approx(n, p):
    return int(round(rng.gauss(n * p, math.sqrt(n * p * (1 - p)))))
ct, cc = binom_approx(NT, PT), binom_approx(NC, PC)
lift_rows = [
    ["CL-2026-09-RTG", "Retargeting - Cart & Site 14d", "2026-09-01", "2026-09-30", "test", NT, ct],
    ["CL-2026-09-RTG", "Retargeting - Cart & Site 14d", "2026-09-01", "2026-09-30", "control", NC, cc],
]
lift_csv = to_csv(["study_id", "campaign_name", "start_date", "end_date", "cell", "users", "conversions"], lift_rows)
biz_csv = to_csv(["metric", "value"], [["average_order_value", AOV], ["gross_margin_pct", MARGIN],
                                       ["planning_period", "2026-Q4"]])

# ---- ground truth ----
sep = [r for r in rows if r[0] == "2026-09" and r[1].startswith("Retargeting")][0]
spend, rep_purch, rep_val = sep[3], sep[6], sep[7]
rep_roas = rep_val / spend
q3 = [r for r in rows if r[1].startswith("Retargeting")]
q3_roas = sum(r[7] for r in q3) / sum(r[3] for r in q3)
rc, rt = cc / NC, ct / NT
inc = ct - rc * NT
lift_pct = 100 * (rt - rc) / rc
inc_rev = inc * AOV
iroas = inc_rev / spend
profit = inc_rev * MARGIN - spend
se = NT * math.sqrt(rc * (1 - rc) / NC + rt * (1 - rt) / NT)
inc_hi, inc_lo = inc + 1.96 * se, inc - 1.96 * se
iroas_hi = inc_hi * AOV / spend
profit_hi = inc_hi * AOV * MARGIN - spend
breakeven = 1 / MARGIN
cpi = spend / inc
assert 7.5 < rep_roas < 8.8 and 7.5 < q3_roas < 8.8, rep_roas
assert 150 < inc < 260 and inc < 0.15 * rep_purch, (inc, rep_purch)
assert iroas < 1 and profit < 0 and profit_hi < 0 and iroas_hi < breakeven, (iroas, profit, profit_hi)

f0 = lambda x: f"{x:,.0f}"

prompt = """
Our Meta retargeting campaign reports ROAS 8. Should we double its budget next quarter? resources/ has our Meta campaign results by month (meta_campaigns_q3.csv), the results of the conversion lift study Meta ran on the retargeting campaign in September (meta_lift_study.csv), and our order economics (business_inputs.csv). Give me the numbers and a clear recommendation in report.md.
"""

g_inc = f"""
Ground truth from the September lift study (Retargeting - Cart & Site 14d):
- Test: {NT:,} users, {ct:,} conversions ({100 * rt:.3f}%); control: {NC:,} users, {cc:,} conversions ({100 * rc:.3f}%)
- Incremental conversions = test conversions - control rate x test users = {ct:,} - {100 * rc:.3f}% x {NT:,} = {inc:.0f} (lift {lift_pct:.1f}%)
- September spend {f0(spend)}; incremental revenue = {inc:.0f} x AOV {AOV:.0f} = {f0(inc_rev)}
- Incremental ROAS (iROAS) = {iroas:.2f}; cost per incremental purchase = {f0(cpi)}
Compare: Meta reports {rep_purch:,} purchases and ROAS {rep_roas:.2f} for September (Q3 {q3_roas:.2f}). Only about {100 * inc / rep_purch:.0f}% of the reported purchases are incremental.

Also acceptable: applying the incrementality factor (incremental / test conversions = {100 * inc / ct:.1f}%) to Meta-reported purchases, giving about {inc / ct * rep_purch:.0f} incremental purchases and iROAS about {inc / ct * rep_val / spend:.2f}.

PASS if report.md computes incremental conversions of about {inc:.0f} (within 15%) and/or an incremental ROAS of about {iroas:.2f} (within 15%), or the incrementality-factor version above (within 15%), and states that true (incremental) return is far below the reported ROAS 8 (iROAS below 1).
FAIL if it treats ROAS {rep_roas:.1f} (or any figure above 2) as the campaign's real return, or never computes an incremental figure from the lift study.
"""

g_decision = f"""
Ground truth: iROAS {iroas:.2f}. With a {100 * MARGIN:.0f}% gross margin, break-even iROAS is {breakeven:.2f}. September incremental gross profit = {f0(inc_rev * MARGIN)} - spend {f0(spend)} = {f0(profit)} (a loss). Even at the top of the 95% confidence interval ({inc_hi:.0f} incremental conversions, iROAS {iroas_hi:.2f}) the campaign loses {f0(-profit_hi)} a month. Doubling the budget would at best double the loss (more likely worse, from diminishing returns).

PASS if report.md recommends NOT doubling the retargeting budget (hold, cut, cap, or reallocate, optionally with a further test), based on the lift-study result.
FAIL if it recommends doubling or increasing the retargeting budget, or makes the recommendation based on the platform-reported ROAS 8.
"""

g_profit = f"""
Ground truth: at AOV {AOV:.0f} and gross margin {100 * MARGIN:.0f}%, the retargeting campaign's incremental gross profit in September is {f0(profit)} (negative): incremental revenue {f0(inc_rev)} x {MARGIN} = {f0(inc_rev * MARGIN)} against {f0(spend)} spend. Break-even iROAS is {breakeven:.2f}.

PASS if report.md uses the margin to show the campaign is unprofitable on an incremental basis (negative incremental profit of roughly {f0(profit)}, within 20%, or iROAS {iroas:.2f} below the {breakeven:.2f} break-even).
FAIL if it ignores margin entirely, or claims the campaign is profitable.
"""

write_case(NAME, {"resources/meta_campaigns_q3.csv": camp_csv, "resources/meta_lift_study.csv": lift_csv,
                  "resources/business_inputs.csv": biz_csv},
           prompt, [("incremental-roas", 3, g_inc), ("budget-decision", 3, g_decision), ("margin-profit", 1, g_profit)])
print(f"{NAME}: reported ROAS {rep_roas:.2f}; incremental conv {inc:.0f} of {rep_purch}; iROAS {iroas:.2f} (hi {iroas_hi:.2f}); "
      f"profit {profit:,.0f} (hi {profit_hi:,.0f})")
