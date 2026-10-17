"""Agency model: 11 drivers, R2 higher by ~1.5 points. Ours: 3 drivers. R2 never
falls when you add variables; adjusted R2 favours ours and a partial F-test on
the 8 added drivers is far from significant (all 8 have p > 0.1)."""
import sys, random, math, json; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "models-regression-model-choice"
SEED = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 19
rng = random.Random(SEED)
N = 104
X3 = ["tv_spend_k", "search_spend_k", "avg_price"]
EXTRA = ["temperature_c", "competitor_promo", "email_sends_k", "social_posts", "site_speed_s",
         "holiday_flag", "pr_mentions", "influencer_spend_k"]
data = []
for w in range(N):
    tv = rng.uniform(20, 80); se = rng.uniform(10, 40); pr = rng.uniform(18, 24)
    ex = [rng.gauss(14, 7), rng.choice([0, 0, 0, 1]), rng.uniform(80, 160), rng.randint(3, 12),
          rng.uniform(1.6, 3.2), 1 if w % 52 in (46, 47, 50, 51) else 0, rng.randint(0, 25), rng.uniform(0, 15)]
    sales = 400 + 4.2 * tv + 6.0 * se - 22 * pr + rng.gauss(0, 58)
    data.append(([tv, se, pr], ex, sales))

def ols(Xrows, y):
    k = len(Xrows[0])
    XtX = [[sum(r[i] * r[j] for r in Xrows) for j in range(k)] for i in range(k)]
    Xty = [sum(r[i] * yy for r, yy in zip(Xrows, y)) for i in range(k)]
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(XtX)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(A[r][c])); A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]; A[c] = [v / pv for v in A[c]]
        for r in range(k):
            if r != c:
                f = A[r][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    inv = [row[k:] for row in A]
    beta = [sum(inv[i][j] * Xty[j] for j in range(k)) for i in range(k)]
    res = [yy - sum(b * x for b, x in zip(beta, r)) for r, yy in zip(Xrows, y)]
    sse = sum(e * e for e in res); ybar = sum(y) / len(y); sst = sum((yy - ybar) ** 2 for yy in y)
    s2 = sse / (len(y) - k)
    se_ = [math.sqrt(s2 * inv[i][i]) for i in range(k)]
    return beta, se_, 1 - sse / sst, sse

y = [d[2] for d in data]
XA = [[1.0] + d[0] for d in data]
XB = [[1.0] + d[0] + d[1] for d in data]
bA, sA, r2A, sseA = ols(XA, y)
bB, sB, r2B, sseB = ols(XB, y)
pfun = lambda t: math.erfc(abs(t) / math.sqrt(2))   # normal approx, df ~ 92-100
kA, kB = 3, 11
adjA = 1 - (1 - r2A) * (N - 1) / (N - kA - 1)
adjB = 1 - (1 - r2B) * (N - 1) / (N - kB - 1)
F = ((sseA - sseB) / 8) / (sseB / (N - kB - 1))
FCRIT = 2.04  # F_0.05(8, 92)
pB = [pfun(b / s) for b, s in zip(bB, sB)]
extra_p = pB[4:]
ok = (r2B > r2A + 0.008 and adjA > adjB and F < 1.3 and min(extra_p) > 0.12
      and all(pfun(b / s) < 0.01 for b, s in zip(bA[1:], sA[1:])) and 0.74 < r2A < 0.84)
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1].isdigit():
    print(SEED, ok, round(r2A, 3), round(r2B, 3), round(F, 2), round(min(extra_p), 2)); sys.exit()
assert ok, (r2A, r2B, adjA, adjB, F, extra_p)

def table(names, b, s):
    return [{"term": n, "estimate": round(bb, 3), "std_error": round(ss, 3), "t_value": round(bb / ss, 2),
             "p_value": round(pfun(bb / ss), 4)} for n, bb, ss in zip(names, b, s)]
models = {
    "dependent_variable": "weekly_sales_k", "n_weeks": N, "period": "2024-W40 to 2026-W39",
    "models": [
        {"model_id": "in_house_v2", "built_by": "Marketing analytics team", "method": "OLS",
         "r_squared": round(r2A, 3), "coefficients": table(["intercept"] + X3, bA, sA)},
        {"model_id": "agency_mmm_v5", "built_by": "Agency", "method": "OLS",
         "r_squared": round(r2B, 3), "coefficients": table(["intercept"] + X3 + EXTRA, bB, sB)},
    ],
}
js = json.dumps(models, indent=2)
print(f"{NAME}: R2 {r2A:.3f} vs {r2B:.3f}; adj {adjA:.3f} vs {adjB:.3f}; partial F {F:.2f}; min extra p {min(extra_p):.2f}")

prompt = f"""
Our agency built a weekly sales model with 11 drivers and says it explains {100*r2B:.1f}% of weekly sales. Ours has 3 drivers and explains {100*r2A:.1f}%. They want us to plan next year's budget on theirs. Which model should we use? Both model outputs are in resources/models.json. Write report.md with your recommendation.
"""
g_choice = f"""
Ground truth (n = {N} weeks):
- Our 3-driver model: R2 {r2A:.3f}, adjusted R2 = 1 - (1-{r2A:.3f}) x {N-1}/{N-kA-1} = {adjA:.3f}; all three drivers p < 0.01.
- Agency 11-driver model: R2 {r2B:.3f}, adjusted R2 = 1 - (1-{r2B:.3f}) x {N-1}/{N-kB-1} = {adjB:.3f}. The 8 extra drivers all have p-values between {min(extra_p):.2f} and {max(extra_p):.2f} (none significant).
- Partial F-test for the 8 added drivers: F = {F:.2f}, well below the 5% critical value of about {FCRIT} (8, {N-kB-1} df): they add nothing beyond chance.
Naive wrong answer: "use the agency model, it has the higher R2 ({r2B:.3f} vs {r2A:.3f})."

PASS if report.md recommends our 3-driver model (or says the agency's extra 8 drivers do not improve it and the simpler model should be used) based on adjusted R2, a partial F-test, and/or the non-significant added coefficients.
FAIL if it picks the agency model because its R2 is higher, or calls the two equivalent without using any of these checks.
"""
g_r2 = """
Ground truth: R2 can never go down when variables are added to an OLS model, even pure noise variables; that is why the agency's 11-driver model has a slightly higher R2. Adjusted R2 (or an F-test / information criterion) penalises the extra variables.

PASS if report.md says (in any wording) that R2 always rises or cannot fall when more variables are added, so a higher R2 with more drivers is not evidence of a better model.
FAIL otherwise.
"""
write_case(NAME, {"resources/models.json": js}, prompt, [("model-choice", 3, g_choice), ("r2-reason", 1, g_r2)])
