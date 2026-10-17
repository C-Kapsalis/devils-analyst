"""NPV of future flows is positive (~+$1.1M) once the $1.4M already spent is
(correctly) excluded, but the plan needs 19-21% of the serviceable market from
a new entrant with 8% awareness among 6 competitors. At a realistic ~5% share
NPV is deeply negative; break-even needs ~11% of SAM. Not an unconditional go."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "product-npv-share-of-sam"
PRICE, VAR, FIXED_Y, SAM, SUNK = 140, 70, 1_200_000, 160_000, 1_400_000
PLAN = [30000, 32000, 34000]
r = 1.10 ** 0.25 - 1

def flows(units):
    out = []
    for q in range(1, 17):
        y = (q - 1) // 4 + 1
        if y == 1:
            out.append((0, 0, 0, -350_000))
        else:
            u = units[y - 2] / 4
            out.append((u, u * PRICE, -u * VAR, -FIXED_Y / 4))
    return out
def npv(units):
    return sum(sum(f[1:]) / (1 + r) ** q for q, f in enumerate(flows(units), 1))

rows = [["to_date", "2025-Q1..2026-Q4", "", "", "", "", -SUNK, -SUNK, "development_spent_to_date"]]
for q, (u, rev, vc, other) in enumerate(flows(PLAN), 1):
    y, qq = 2027 + (q - 1) // 4, (q - 1) % 4 + 1
    if q <= 4:
        rows.append([q, f"{y}-Q{qq}", 0, 0, 0, 0, other, other, "remaining development and launch"])
    else:
        rows.append([q, f"{y}-Q{qq}", int(u), int(rev), int(vc), int(other), 0, int(rev + vc + other), "plan"])
cf_csv = to_csv(["quarter_index", "period", "units", "revenue", "variable_cost", "fixed_cost",
                 "development_and_launch", "net_cash_flow", "note"], rows)
ue = to_csv(["item", "value"], [["price_to_retailer", PRICE], ["variable_cost_per_unit", VAR],
                                ["fixed_costs_per_year", FIXED_Y]])
mk = to_csv(["item", "value", "source"], [["SAM_units_per_year", SAM, "2026 market study, e-bike battery packs, our channels"],
                                          ["competitors", 6, "market study"], ["our_brand_awareness", 0.08, "2026 tracker"],
                                          ["leader_share_of_SAM", 0.31, "market study"]])

npv_plan = npv(PLAN); npv_sunk = npv_plan - SUNK
beq = FIXED_Y / (PRICE - VAR)
shares = [u / SAM for u in PLAN]
npv5 = npv([0.05 * SAM] * 3); npv10 = npv([0.10 * SAM] * 3)
lo, hi = 0, 60000
for _ in range(60):
    m = (lo + hi) / 2
    lo, hi = (lo, m) if npv([m] * 3) > 0 else (m, hi)
v0 = hi
assert 0.9e6 < npv_plan < 1.3e6 and npv_sunk < 0 and npv5 < -2e6 and min(shares) > 0.18
print(f"{NAME}: NPV {npv_plan:,.0f} (incl sunk {npv_sunk:,.0f}); BEQ {beq:,.0f} ({100*beq/SAM:.1f}% SAM); plan {[round(100*s,1) for s in shares]}%; NPV@5% {npv5:,.0f}; NPV0 at {v0:,.0f}/yr ({100*v0/SAM:.1f}%)")

prompt = """
Board meeting Thursday. resources/ has the cash-flow plan for the Ridgeline e-bike battery pack (cashflow_plan.csv, quarterly, 4 years), unit economics (unit_economics.csv) and the market study (market.csv). We've already put $1.4M into development. Hurdle rate is 10%. Should we go ahead? Write report.md with your recommendation.
"""
f0 = lambda x: f"{x:,.0f}"
g_npv = f"""
Ground truth: quarterly discount rate = 1.10^0.25 - 1 = {100*r:.2f}%. NPV of the plan's future cash flows (quarters 1-16) = about ${f0(npv_plan)}. The $1.4M already spent is sunk: it cannot be recovered whatever the board decides, so it must be excluded from the go/no-go NPV. Including it gives about ${f0(npv_sunk)} (negative), which would be a wrong reason to stop.

PASS if report.md reports an NPV of future cash flows excluding the $1.4M, between $0.9M and $1.3M, and does not use the sunk $1.4M in the NPV that drives the decision.
FAIL if the $1.4M is included in the NPV used for the decision, or the report says the project fails because of the money already spent.
"""
g_share = f"""
Ground truth. Contribution per unit = $140 - $70 = $70. Break-even volume = $1.2M / $70 = {f0(beq)} units a year = {100*beq/SAM:.1f}% of the 160,000-unit serviceable market (SAM). The plan assumes {', '.join(f0(u) for u in PLAN)} units in years 2-4 = {', '.join(f'{100*s:.1f}%' for s in shares)} of SAM, for a new entrant with 8% brand awareness against 6 competitors (a realistic new-entrant share is more like 1-5%). At 5% of SAM (8,000 units a year) NPV is about ${f0(npv5)}; at 10% about ${f0(npv10)}; NPV only turns positive above about {f0(v0)} units a year ({100*v0/SAM:.1f}% of SAM).
Naive wrong answer: "NPV +${npv_plan/1e6:.1f}M > 0, go."

PASS if report.md computes the break-even volume (about {f0(beq)} units, about {100*beq/SAM:.0f}% of SAM) or the plan's implied share of SAM (about {100*shares[0]:.0f}-{100*shares[-1]:.0f}%), says this exceeds what a new entrant can realistically capture, AND therefore does not recommend an unconditional go (conditional go with a pilot and kill criteria, rework the cost base, or no-go are all acceptable).
FAIL if it recommends going ahead on the positive NPV without testing the market share the plan requires.
"""
write_case(NAME, {"resources/cashflow_plan.csv": cf_csv, "resources/unit_economics.csv": ue, "resources/market.csv": mk},
           prompt, [("npv", 2, g_npv), ("share", 3, g_share)])
