"""Who gets a $15 retention credit? The naive rule is 'churn probability
above 0.5' (or top decile). With a 40% save rate and ~$180 margin, a missed
churner costs ~$72 and a wasted credit $15, so the cut-off is c/(1+c) ~0.17:
about five times as many subscribers as the 0.5 rule."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "models-churn-offer-threshold"
rng = random.Random(7)
N = 2000
CREDIT, SAVE = 15.0, 0.40
rows = []
for i in range(N):
    p = rng.betavariate(1.2, 4)
    m = rng.gammavariate(4, 45)
    rows.append([f"S{20001 + i}", round(p, 3), round(m, 2)])
csv_text = to_csv(["customer_id", "churn_probability", "annual_margin"], rows)
hold = to_csv(["quarter", "group", "high_risk_subscribers", "cancelled"],
              [["2026-Q2", "credit_offered", 1200, 360], ["2026-Q2", "holdout_no_credit", 1200, 600]])

ps = [r[1] for r in rows]
avg_m = sum(r[2] for r in rows) / N
def cnt(t): return sum(p >= t for p in ps)
c1 = CREDIT / (SAVE * 180); t1 = c1 / (1 + c1)
c2 = CREDIT / (SAVE * (180 - CREDIT)); t2 = c2 / (1 + c2)
t3 = CREDIT / (SAVE * 180)          # 'offer if p*0.4*m >= 15' (credit cost to everyone offered)
n1, n2, n3 = cnt(t1), cnt(t2), cnt(t3)
n_pc = sum(r[1] * SAVE * r[2] >= CREDIT * (1 - r[1]) for r in rows)
n_pc3 = sum(r[1] * SAVE * r[2] >= CREDIT for r in rows)
n50 = cnt(0.5)
n_dec = N // 10
lo, hi = min(n1, n2, n3, n_pc, n_pc3), max(n1, n2, n3, n_pc, n_pc3)
lo_ok, hi_ok = int(lo * 0.9), int(hi * 1.1)
assert n50 < 0.3 * lo and n_dec < 0.5 * lo, (n50, lo)
print(f"{NAME}: thresholds {t1:.3f}/{t2:.3f}/{t3:.3f} -> {n1}/{n2}/{n3} (per-cust {n_pc}/{n_pc3}); >0.5: {n50}; avg margin {avg_m:.0f}")

prompt = f"""
Our data team scored all {N:,} Lumio subscribers with a churn model (resources/churn_scores.csv). We have a $15 retention credit. Last quarter's holdout (resources/holdout_summary.csv) showed the credit keeps about 40% of the people who would otherwise have cancelled. Average annual margin per subscriber is about $180. Who should get the credit? Write report.md with the rule and how many subscribers it covers.
"""
g_thr = f"""
Ground truth. Send the credit when expected margin saved beats the credit cost:
- Cost of a wasted credit (sent to someone who would have stayed) = $15. Cost of NOT sending to a churner = 0.40 save rate x $180 margin = $72.
- Cut-off probability = c/(1+c) with c = 15/72 -> {t1:.3f}; covers {n1:,} of {N:,} subscribers.
- Acceptable variants: netting the credit from the margin (cut-off {t2:.3f}, {n2:,} subscribers); 'offer if p x 0.4 x margin >= $15' (cut-off {t3:.3f}, {n3:,}); a per-customer rule using each row's annual_margin ({n_pc:,} or {n_pc3:,} subscribers).
Naive wrong answers: churn probability above 0.5 ({n50:,} subscribers), top decile ({n_dec:,}), or any cut-off chosen without the costs.

PASS if report.md's rule uses a probability cut-off between 0.15 and 0.22 (or an equivalent per-customer expected-value rule as above) AND the number covered is between {lo_ok:,} and {hi_ok:,}.
FAIL if the cut-off is 0.5, a top-N / top-decile / top-X% choice without cost logic, any cut-off above 0.3, or the count is below {lo_ok:,}.
"""
g_cost = """
Ground truth: the two errors have different costs. Sending a credit to someone who would stay wastes $15; missing a churner loses about 0.4 x $180 = $72 of expected margin. A 0.5 cut-off only makes sense if both errors cost the same.

PASS if report.md states both error costs (about $15 and about $72, or per-customer equivalents) and says that using 0.5 (or the model's default) assumes equal costs / is not right here.
FAIL if it does not state both costs explicitly.
"""
write_case(NAME, {"resources/churn_scores.csv": csv_text, "resources/holdout_summary.csv": hold}, prompt,
           [("threshold", 3, g_thr), ("costs-explicit", 1, g_cost)])
