import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import json

NAME = "ab-srm"
rng = random.Random(2209)


def phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


nA, nB = 52000, 47000
cA = int(round(nA * 0.0300))
cB = int(round(nB * 0.0300 * 1.08))
aovA = 71.40 + rng.uniform(-0.5, 0.5)
aovB = 72.10 + rng.uniform(-0.5, 0.5)
revA = round(cA * aovA, 2)
revB = round(cB * aovB, 2)

pA, pB = cA / nA, cB / nB
lift = pB / pA - 1
pp = (cA + cB) / (nA + nB)
z = (pB - pA) / math.sqrt(pp * (1 - pp) * (1 / nA + 1 / nB))
p_conv = 2 * (1 - phi(abs(z)))
rpvA, rpvB = revA / nA, revB / nB
rpv_lift = rpvB / rpvA - 1

exp = (nA + nB) / 2
chi2 = (nA - exp) ** 2 / exp + (nB - exp) ** 2 / exp
p_srm = math.erfc(math.sqrt(chi2 / 2))  # chi-square df=1 survival
share_A = nA / (nA + nB)

assert p_conv < 0.05 and 0.06 < lift < 0.10
assert chi2 > 200 and p_srm < 1e-40

config = {
    "experiment_id": "hp_hero_2026_09",
    "name": "Homepage hero: lifestyle photo (B) vs product grid (A)",
    "site": "harboroutdoor.example",
    "start_date": "2026-09-07",
    "end_date": "2026-09-27",
    "unit": "user",
    "allocation": {"A": 0.5, "B": 0.5},
    "primary_metric": "purchase_conversion_rate",
    "secondary_metrics": ["revenue_per_user"],
    "targeting": "all desktop and mobile visitors landing on /",
}

results = to_csv(["variant", "users", "conversions", "revenue"], [["A", nA, cA, revA], ["B", nB, cB, revB]])

prompt = """
Here are the results of our homepage hero test for Harbor Outdoor. The test setup is in resources/experiment_config.json and the results export is resources/ab_results.csv (variant, users, conversions, revenue).

Which version should we go with? Write report.md with the result and your recommendation.
"""

g_srm = f"""
Ground truth: the config specifies a 50/50 allocation, but the results show A {nA:,} users vs B {nB:,} users ({share_A*100:.1f}% / {(1-share_A)*100:.1f}%). A chi-square goodness-of-fit test against 50/50 gives chi-square = {chi2:.0f} (df=1), p = {p_srm:.1g}, i.e. a sample ratio mismatch (SRM). With an SRM the assignment or tracking is broken, so the conversion comparison cannot be trusted.

Naive answer: B converts {pB*100:.2f}% vs A {pA*100:.2f}% = {lift*100:+.1f}% lift, z = {z:.2f}, p = {p_conv:.3f}, "statistically significant, B wins", with no mention of the user split.

PASS if report.md flags that the {nA:,} vs {nB:,} split is inconsistent with the planned 50/50 allocation (sample ratio mismatch / allocation imbalance / unexpected traffic split) AND says this makes the test result unreliable or invalid. A test statistic is not required, but if one is given it should be roughly chi-square ~{chi2:.0f} or a p-value far below 0.001.
FAIL if report.md does not mention the unequal split, or mentions it only in passing (e.g. "slightly fewer users in B") while still treating the B lift as a valid result.
"""

g_rec = f"""
Correct recommendation: do not ship B on the basis of this test. Investigate why B received fewer users than planned (assignment bug, redirect/loading failures, bot filtering, tracking loss on B) and rerun or repair the test before deciding. Keeping A as the default until the issue is resolved is fine.

Naive recommendation: "Go with B, it lifts conversion {lift*100:.0f}% (significant) and revenue per user {rpv_lift*100:+.0f}%."

PASS if report.md recommends investigating the traffic split / rerunning the test (or not deciding yet) rather than shipping B.
FAIL if report.md recommends shipping B (even with a caveat attached), or projects a revenue gain from B as if the result were valid.
"""

write_case(
    NAME,
    {
        "resources/experiment_config.json": json.dumps(config, indent=2) + "\n",
        "resources/ab_results.csv": results,
    },
    prompt,
    [("srm-detected", 3, g_srm), ("recommendation", 2, g_rec)],
)
print(f"{NAME}: B lift {lift*100:+.1f}% p={p_conv:.3f}; SRM chi2={chi2:.0f} p={p_srm:.1g}")
