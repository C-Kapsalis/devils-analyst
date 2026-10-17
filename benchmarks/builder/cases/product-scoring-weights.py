"""Weighted scoring of three headphone concepts. Team workshop weights (25% on
style) make A the winner; customer-importance weights make B the winner; and
moving 10 points from comfort to style flips it back. Use customer weights,
and the lead is not robust: carry A and B forward or test."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "product-scoring-weights"
CRIT = ["comfort", "battery_life", "setup_ease", "unit_cost", "durability", "style"]
R = {"A": [3, 3, 4, 4, 3, 5], "B": [5, 4, 3, 3, 3, 2], "C": [4, 3, 3, 3, 4, 3]}
TEAM = [15, 15, 10, 20, 15, 25]
IMP = [7.5, 7.5, 4.5, 4.5, 4.5, 1.5]   # mean importance, 0-10 scale
N_RESP = 412
sm = to_csv(["criterion", "weight_pct", "weight_source", "concept_a_rating", "concept_b_rating", "concept_c_rating", "rating_scale"],
            [[c, TEAM[i], "team workshop", R["A"][i], R["B"][i], R["C"][i], "1-5 vs current model (3 = same)"] for i, c in enumerate(CRIT)])
ci = to_csv(["criterion", "mean_importance_0_10", "respondents", "survey"],
            [[c, IMP[i], N_RESP, "2026-08 customer survey"] for i, c in enumerate(CRIT)])

def score(w):
    s = sum(w)
    return {k: sum(v[i] * w[i] for i in range(6)) / s for k, v in R.items()}
team = score(TEAM)
cw = [x / sum(IMP) * 100 for x in IMP]
cust = score(cw)
alt = cw[:]; alt[0] -= 10; alt[5] += 10
flip = score(alt)
rank = lambda d: sorted(d, key=d.get, reverse=True)
assert rank(team)[0] == "A" and rank(cust)[0] == "B" and rank(flip)[0] == "A"
fmt = lambda d: ", ".join(f"{k} {d[k]:.2f}" for k in rank(d))
print(f"{NAME}: team {fmt(team)}; customer {fmt(cust)}; shifted {fmt(flip)}")

prompt = """
Our product team at Lumen Audio scored three headphone concepts in a workshop (resources/scoring_matrix.csv). We also have importance ratings from our customer survey (resources/customer_importance.csv). Which concept should we build? report.md please.
"""
g_w = f"""
Ground truth. The weights in scoring_matrix.csv came from the team workshop (style 25%, comfort 15%). Customers rate comfort and battery life as most important and style least. Converting customer mean importance to weights (importance / total) gives {", ".join(f"{c} {w:.0f}%" for c, w in zip(CRIT, cw))}.
- Team weights: {fmt(team)}.
- Customer weights: {fmt(cust)}.
Naive wrong answer: "A scores {team['A']:.2f} on the scoring matrix, build A" (uses the team's weights as given).

PASS if report.md rescores the concepts with customer-derived weights and reports B ahead under them (about {cust['B']:.2f} vs {cust['A']:.2f}, within 0.1).
FAIL if it picks A from the team weights without rescoring with the customer importance, or never uses customer_importance.csv to weight the criteria.
"""
g_r = f"""
Ground truth: B's lead under customer weights is fragile. Moving 10 points of weight from comfort to style (customer weights otherwise unchanged) gives {fmt(flip)}: A wins again. A one-point change in a single rating can also close the gap. A sound recommendation is not "build B, done": carry A and B forward, consider a hybrid (B's comfort and battery with A's style and setup), and/or test with customers before committing.

PASS if report.md runs a sensitivity check (changing a weight or rating) and says the result is close or not robust, recommending carrying two concepts forward, a hybrid, or a customer test before committing.
FAIL if it names a single winner with no sensitivity check.
"""
write_case(NAME, {"resources/scoring_matrix.csv": sm, "resources/customer_importance.csv": ci}, prompt,
           [("weights", 3, g_w), ("robust", 2, g_r)])
