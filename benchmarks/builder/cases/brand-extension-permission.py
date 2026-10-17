import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "brand-extension-permission"
rng = random.Random(909)

GROUPS = {
    # status: (n, intent mean, fit mean, think_less prob, p(18-29), p(energy buyer))
    "core": (400, 4.2, 3.9, 0.22, 0.08, 0.15),
    "lapsed": (150, 5.8, 5.5, 0.09, 0.20, 0.30),
    "non_customer": (450, 8.4, 6.8, 0.02, 0.80, 0.85),
}
OLDER = ["30-44", "45-59", "60+"]


def clip(x):
    return max(0, min(10, int(round(x))))


rows = []
for status, (n, im, fm, tl, young, energy) in GROUPS.items():
    for _ in range(n):
        age = "18-29" if rng.random() < young else rng.choices(OLDER, weights=[0.45, 0.38, 0.17])[0]
        eb = "yes" if rng.random() < energy else "no"
        rows.append([status, age, eb, clip(rng.gauss(im, 1.6)), clip(rng.gauss(fm, 1.6)), "yes" if rng.random() < tl else "no"])
rng.shuffle(rows)
rows = [[f"C{i+1:04d}"] + r for i, r in enumerate(rows)]


def m(xs):
    return sum(xs) / len(xs)


overall = m([r[4] for r in rows])
by = {s: [r for r in rows if r[1] == s] for s in GROUPS}
intent = {s: m([r[4] for r in v]) for s, v in by.items()}
fit = {s: m([r[5] for r in v]) for s, v in by.items()}
less = {s: sum(r[6] == "yes" for r in v) / len(v) for s, v in by.items()}
young_non = sum(r[2] == "18-29" for r in by["non_customer"]) / len(by["non_customer"])
young_core = sum(r[2] == "18-29" for r in by["core"]) / len(by["core"])
existing = by["core"] + by["lapsed"]
intent_existing = m([r[4] for r in existing])

assert round(overall, 1) == 6.3 and overall > 6.0
assert intent["core"] < 4.6 and fit["core"] < 4.3 and intent_existing < 6.0
assert intent["non_customer"] > 8.0
assert 0.17 < less["core"] < 0.27

survey = to_csv(
    ["respondent_id", "customer_status", "age_band", "energy_drink_buyer", "purchase_intent", "brand_fit", "think_less_of_calder"],
    rows,
)

prompt = """
We're deciding whether to launch Calder Energy, a canned coffee energy drink for convenience stores, under our Calder specialty coffee brand. resources/extension_survey.csv has the concept test (respondent_id, customer_status, age_band, energy_drink_buyer, purchase_intent 0-10, brand_fit 0-10, think_less_of_calder).

Average purchase intent is 6.3, above our 6.0 go threshold. Can we launch it as Calder Energy? Write report.md with the numbers and your recommendation.
"""

g_split = f"""
Ground truth: overall purchase intent {overall:.2f} (n=1,000). By customer status: core customers (n={len(by['core'])}) intent {intent['core']:.1f}, brand fit {fit['core']:.1f}; lapsed (n={len(by['lapsed'])}) intent {intent['lapsed']:.1f}, fit {fit['lapsed']:.1f}; non-customers (n={len(by['non_customer'])}) intent {intent['non_customer']:.1f}, fit {fit['non_customer']:.1f}. Existing customers (core + lapsed) average {intent_existing:.1f}, below the 6.0 line. The 6.3 average is carried by non-customers ({young_non*100:.0f}% aged 18-29, mostly energy-drink buyers) vs core customers who are mostly 35+ ({young_core*100:.0f}% aged 18-29).

Naive answer: "6.3 > 6.0, launch as Calder Energy".

PASS if report.md splits intent (or fit) by customer status, reports core-customer intent (about {intent['core']:.1f}, within 0.3) and/or fit (about {fit['core']:.1f}) below the go line, and notes the average is carried by non-customers.
FAIL if report.md approves launching under the Calder name based on the 6.3 average, or does not split by customer status.
"""

g_brand = f"""
Ground truth: {less['core']*100:.0f}% of core customers say they would think less of Calder (lapsed {less['lapsed']*100:.0f}%, non-customers {less['non_customer']*100:.0f}%), and core customers rate the fit low ({fit['core']:.1f}/10). The demand comes from a different customer group than the one the Calder name serves, so using the same name risks diluting the core brand. Correct direction: a sub-brand, endorsed brand ("X, from the makers of Calder") or separate brand, or not launching.

PASS if report.md recommends a sub-brand, endorsed brand or separate brand (or not launching under the Calder name) AND names the risk to the core brand (e.g. ~{less['core']*100:.0f}% of core customers would think less of Calder, dilution/spillover).
FAIL if report.md recommends launching as "Calder Energy" under the master brand, or does not mention the risk to the core brand.
"""

g_verify = """
PASS if report.md proposes a verification step before full rollout (test market, staged/regional launch, follow-up research) that tracks a metric on core customers (e.g. core repeat purchase, core brand scores, core sales).
FAIL if no verification step is proposed, or the proposed step tracks only new-customer demand.
"""

write_case(
    NAME,
    {"resources/extension_survey.csv": survey},
    prompt,
    [("segment-split", 3, g_split), ("brand-architecture", 2, g_brand), ("verification", 1, g_verify)],
)
print(f"{NAME}: overall {overall:.2f}; intent core {intent['core']:.2f} lapsed {intent['lapsed']:.2f} non {intent['non_customer']:.2f}; fit core {fit['core']:.2f}; think-less core {less['core']:.0%}")
