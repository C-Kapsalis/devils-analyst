import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import statistics

NAME = "hybrid-sample-size"
rng = random.Random(1414)

DELTA = 0.2
CONFIG = "zs-demo-t03"  # zero-shot, demographic personas, temperature 0.3 (the pilot's set-up)

COUNTS = {"A": {2: 1, 3: 13, 4: 64, 5: 22}, "B": {3: 12, 4: 64, 5: 24}}  # synthetic answers cluster on 4
rows = []
for arm, cnt in COUNTS.items():
    vals = [v for v, c in cnt.items() for _ in range(c)]
    rng.shuffle(vals)
    rows += [[arm, v] for v in vals]


def var(x):
    m = sum(x) / len(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)


va = var([r[1] for r in rows if r[0] == "A"])
vb = var([r[1] for r in rows if r[0] == "B"])
v_syn = (va + vb) / 2
sd_syn = math.sqrt(v_syn)

# validation repository: past studies in the same category with human + synthetic fielded in parallel
repo = []
pi_ratios = [0.30, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.39, 0.40]
for k, ratio in enumerate(pi_ratios):
    vh = round(rng.uniform(0.85, 1.25), 2)
    study = f"PKG-{2023 + k // 4}-{k % 4 + 1:02d}"
    repo.append([study, CONFIG, "purchase_intent_5pt", vh, round(vh * ratio, 3)])
    vh2 = round(rng.uniform(0.7, 1.0), 2)
    repo.append([study, CONFIG, "liking_5pt", vh2, round(vh2 * rng.uniform(0.40, 0.55), 3)])
for k in range(4):
    vh = round(rng.uniform(0.9, 1.2), 2)
    repo.append([f"PKG-2026-{k + 5:02d}", "history-rag-t10", "purchase_intent_5pt", vh, round(vh * rng.uniform(0.78, 0.92), 3)])
rng.shuffle(repo)

ratios = sorted(r[4] / r[3] for r in repo if r[1] == CONFIG and r[2] == "purchase_intent_5pt")
med = statistics.median(ratios)
all_ratio_med = statistics.median(r[4] / r[3] for r in repo)  # wrong: pools items and configs
Z = (1.96 + 0.8416) ** 2 * 2  # 15.7, two-sided alpha .05, power .80
n_naive = math.ceil(Z * v_syn / DELTA ** 2)
n_naive_036 = math.ceil(16 * 0.36 / DELTA ** 2)
v_h = v_syn / med
n_true = math.ceil(Z * v_h / DELTA ** 2)
n_lo, n_hi = math.ceil(Z * v_syn / max(ratios) / DELTA ** 2), math.ceil(Z * v_syn / min(ratios) / DELTA ** 2)
n_pooled = math.ceil(Z * v_syn / all_ratio_med / DELTA ** 2)

assert 0.55 < sd_syn < 0.66, sd_syn
assert 0.33 < med < 0.37
assert n_true > 2.5 * n_naive and 330 < n_true < 480
assert n_pooled < n_lo, "pooling all items/configs gives a smaller (wrong) ratio-adjusted n"

notes = f"""# Packaging concept pilot - set-up

- 200 synthetic respondents (100 per concept), zero-shot, demographic personas, temperature 0.3.
- Configuration code in our validation repository: {CONFIG}.
- Item: purchase intent, 5-point scale.
- Planned human study: two independent cells (one concept each), two-sided test, alpha 0.05, power 80%.
"""

prompt = """
We piloted our two packaging concepts for Oakleaf Snacks with 200 synthetic respondents (resources/synthetic_pilot.csv and pilot_setup.md). Purchase intent SD came out around 0.6. resources/validation_repository.csv is our log of past studies.

How many real respondents per concept do we need to detect a 0.2-point difference in purchase intent? Put the number in report.md.
"""

g_n = f"""
Ground truth: the pilot's purchase-intent SD is {sd_syn:.2f} (variance {v_syn:.3f}), but synthetic variance is compressed. validation_repository.csv shows, for purchase-intent items run with the same configuration ({CONFIG}), synthetic/human variance ratios of {min(ratios):.2f}-{max(ratios):.2f} (median {med:.2f}). So the expected human variance is about {v_syn:.3f} / {med:.2f} = {v_h:.2f} (SD ~{math.sqrt(v_h):.2f}), and n per concept = 2 x (1.96 + 0.84)^2 x {v_h:.2f} / 0.2^2 = about {n_true} (range ~{n_lo}-{n_hi} across the repository ratios; the 16 x sigma^2 / delta^2 rule of thumb gives about the same).

Naive answer: plugging the synthetic SD straight in: 16 x 0.36 / 0.04 = {n_naive_036} per concept (exact formula with the pilot variance: {n_naive}); {2 * n_naive_036} in total. Also wrong: pooling every item and configuration in the repository (median ratio {all_ratio_med:.2f}) gives ~{n_pooled}.

PASS if report.md recommends a per-concept n between 340 and 500 AND explains that synthetic variance understates human variance, using the repository's purchase-intent ratio (~0.35) to inflate it.
FAIL if the recommended n is about {n_naive_036} per concept (or ~{2*n_naive_036} total), or {n_naive_036} with only a vague "add a buffer", or below 340 per concept.
"""

g_method = """
PASS if report.md shows the sample-size formula or a standard power calculation (e.g. n = 2(z_alpha/2 + z_beta)^2 sigma^2 / delta^2, or the 16 sigma^2 / delta^2 rule) with the inputs used.
FAIL if a number is given without any formula or power-calculation inputs.
"""

write_case(
    NAME,
    {
        "resources/synthetic_pilot.csv": to_csv(["arm", "purchase_intent_5pt"], rows),
        "resources/pilot_setup.md": notes,
        "resources/validation_repository.csv": to_csv(["study", "config", "item", "var_human", "var_synthetic"], repo),
    },
    prompt,
    [("inflated-n", 3, g_n), ("method", 1, g_method)],
)
print(f"{NAME}: synth SD {sd_syn:.3f}; PI ratio median {med:.3f} ({min(ratios):.2f}-{max(ratios):.2f}); n naive {n_naive} (rule {n_naive_036}); n true {n_true} ({n_lo}-{n_hi}); pooled-ratio n {n_pooled}")
