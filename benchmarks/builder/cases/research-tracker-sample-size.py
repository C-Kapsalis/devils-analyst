"""Margin of error scales with 1/sqrt(n), and the board wants separate country
reads: ~2,260 completes PER country (~4,500 total), not 400 x 4.8/2 = 960.
And the sample is the newsletter list, people who already know the brand:
more completes from it do not fix the upward bias."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "research-tracker-sample-size"
rng = random.Random(3807)
SPEC = {"UK": (220, 88), "DE": (180, 64)}   # completes, aided aware
rows, k = [], 1
for c, (n, aw) in SPEC.items():
    aware = [1] * aw + [0] * (n - aw); rng.shuffle(aware)
    for a in aware:
        unaided = 1 if a and rng.random() < 0.45 else 0
        rows.append([f"T{k:04d}", "2026-Q3", c, "newsletter_list", rng.choice(["18-34", "35-54", "55+"]), unaided, a]); k += 1
csv_text = to_csv(["respondent_id", "wave", "country", "sample_source", "age_band", "aware_unaided", "aware_aided"], rows)

n = len(rows); p = sum(r[6] for r in rows) / n
moe = 1.96 * math.sqrt(p * (1 - p) / n)
Z, E = 1.96, 0.02
n_req = math.ceil(Z ** 2 * p * (1 - p) / E ** 2)
n_half = math.ceil(Z ** 2 * 0.25 / E ** 2)
per = {c: sum(r[6] for r in rows if r[2] == c) / sum(1 for r in rows if r[2] == c) for c in SPEC}
n_c = {c: math.ceil(Z ** 2 * q * (1 - q) / E ** 2) for c, q in per.items()}
naive_lin = round(400 * moe * 100 / 2)
assert abs(p - 0.38) < 0.005 and abs(100 * moe - 4.8) < 0.15
assert 2 * n_req > 4 * naive_lin
lo_c = min(min(n_c.values()), n_req) - 60; hi_c = n_half + 50
print(f"{NAME}: p {p:.3f} moe {100*moe:.2f}; n per read {n_req} (0.5: {n_half}); per country {n_c}; naive {naive_lin}")

prompt = """
Last quarter's brand tracker for Lumen Streaming (n = 400, sent to our newsletter list) put aided awareness at 38%, plus or minus 4.8 points. The respondent file is resources/tracker_q3.csv. The board now wants plus or minus 2 points, and separate reads for the UK and Germany. We'll use the newsletter list again. How many completes should we buy? Write report.md with the number and your recommendation.
"""
g_n = f"""
Ground truth. Required n for a +/-2 point margin at 95% confidence = 1.96^2 x p(1-p) / 0.02^2.
- With p = {p:.2f}: {n_req:,} completes PER read. The board wants separate UK and Germany reads, so about {n_req:,} per country, {2*n_req:,} in total.
- Also acceptable: worst case p = 0.5 -> {n_half:,} per country ({2*n_half:,} total), or each country's own awareness (UK {100*per['UK']:.0f}% -> {n_c['UK']:,}; DE {100*per['DE']:.0f}% -> {n_c['DE']:,}).
Naive wrong answers: scaling linearly, 400 x 4.8/2 = {naive_lin:,}; or {n_req:,} in total split across the two countries (about {n_req//2:,} each).

PASS if report.md's per-country requirement is between {lo_c:,} and {hi_c:,} (total about {2*lo_c:,} to {2*hi_c:,}).
FAIL if the total is under 2,500, or the per-country figure is about {naive_lin:,} or about {n_req//2:,}.
"""
g_bias = """
Ground truth: the tracker sample is the brand's own newsletter list. Subscribers have, by definition, already heard of the brand, so aided awareness from this list is biased upward (the 38% overstates awareness in the market). Buying more completes from the same list only makes a biased number more precise. The tracker needs a sample source unrelated to the brand (e.g. a research panel / representative online panel with country quotas).

PASS if report.md says the newsletter list biases awareness upward (subscribers already know the brand / are not representative) and recommends a different sample source such as a panel.
FAIL if it accepts using the newsletter list again, or mentions representativeness only vaguely without recommending a different source.
"""
write_case(NAME, {"resources/tracker_q3.csv": csv_text}, prompt,
           [("sample-size", 3, g_n), ("sampling-bias", 3, g_bias)])
