"""Concept test: every respondent rated all three concepts. 30 screener fails
(not bike commuters) love concept B and flip the ranking if kept. Among the
150 qualified, A leads B; a paired test shows it is significant (p~0.02), an
independent two-sample test wrongly says 'tied'. And A's top-two-box (~51%)
is low in absolute terms: rework, not a straight go."""
import sys, random, math, statistics as st; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "product-concept-paired-test"
rng = random.Random(11)
def clip(x): return max(1, min(5, round(x)))
rows = []
for i in range(150):
    base = rng.gauss(3.3, 0.9)
    rows.append((1, clip(base + 0.22 + rng.gauss(0, 0.45)), clip(base + rng.gauss(0, 0.45)), clip(base - 0.4 + rng.gauss(0, 0.6))))
for i in range(30):
    rows.append((0, clip(rng.gauss(2.6, 0.8)), clip(rng.gauss(4.4, 0.5)), clip(rng.gauss(3, 0.8))))
rng.shuffle(rows)
out = [[f"R_{1000 + i}", "Yes" if r[0] else "No", r[1], r[2], r[3]] for i, r in enumerate(rows)]
csv_text = to_csv(["response_id", "q1_owns_bike_commutes", "pi_concept_a", "pi_concept_b", "pi_concept_c"], out)

def stats(rs):
    o = {}
    for k, i in (("A", 1), ("B", 2), ("C", 3)):
        v = [r[i] for r in rs]
        o[k] = (st.mean(v), st.stdev(v), sum(x == 5 for x in v) / len(v), sum(x >= 4 for x in v) / len(v))
    return o
pn = lambda z: math.erfc(abs(z) / math.sqrt(2))
q = [r for r in rows if r[0] == 1]
sq, sa = stats(q), stats(rows)
a = [r[1] for r in q]; b = [r[2] for r in q]; n = len(q)
d = [x - y for x, y in zip(a, b)]
tp = st.mean(d) / (st.stdev(d) / math.sqrt(n)); pp = pn(tp)
ti = (st.mean(a) - st.mean(b)) / math.sqrt(st.variance(a) / n + st.variance(b) / n); pi = pn(ti)
assert sq["A"][0] > sq["B"][0] > sq["C"][0] and sa["B"][0] > sa["A"][0]
assert pp < 0.05 and pi > 0.1 and sq["A"][3] < 0.6, (pp, pi)
print(f"{NAME}: qualified A {sq['A'][0]:.2f} B {sq['B'][0]:.2f} C {sq['C'][0]:.2f}; all-rows B {sa['B'][0]:.2f} A {sa['A'][0]:.2f}; paired p {pp:.3f}, indep p {pi:.2f}; A T2B {sq['A'][3]:.3f}")

prompt = """
We're Ridgeline Cycles. resources/concept_survey.csv is our Qualtrics export (numeric values) from the concept test of three bike-lock ideas. Respondents rated each concept on purchase intent (5 = definitely would buy). Which concept should we take into development? Write report.md with the numbers and your recommendation.
"""
f = lambda s, k: f"mean {s[k][0]:.2f}, top-two-box {100*s[k][3]:.1f}%, top-box {100*s[k][2]:.1f}%"
g_scr = f"""
Ground truth: 30 of 180 respondents answered "No" to the screener q1_owns_bike_commutes and are outside the target; they must be excluded.
- Qualified (n=150): A {f(sq,'A')}; B {f(sq,'B')}; C {f(sq,'C')}.
- All 180 rows (wrong): A mean {sa['A'][0]:.2f}, B mean {sa['B'][0]:.2f} (B top-two-box {100*sa['B'][3]:.0f}%): B appears to win only because of the screener fails.

PASS if report.md excludes the "No" screener respondents and reports A as the highest-scoring concept among qualified respondents (A about {sq['A'][0]:.2f} vs B about {sq['B'][0]:.2f}, within 0.05).
FAIL if B is named the leading concept, or all 180 rows are used for the comparison.
"""
g_pair = f"""
Ground truth: every respondent rated all three concepts (within-subject design), so A vs B must be tested with a paired test on each respondent's difference.
- Paired t-test (qualified, n=150): mean difference {st.mean(d):.3f}, t = {tp:.2f}, p about {pp:.3f}: A is significantly ahead of B.
- Independent two-sample test on the same columns (wrong test): t = {ti:.2f}, p about {pi:.2f}, which wrongly suggests "no difference".

PASS if report.md compares A and B with a paired / within-respondent test and reports the difference as significant (p below 0.05, about {pp:.3f}), or otherwise explains that the same respondents rated all concepts and treats the difference as significant.
FAIL if it calls A and B statistically tied / indistinguishable, or bases the comparison on an independent-samples test.
"""
g_lvl = f"""
Ground truth: A is the best of the three among qualified respondents, but only {100*sq['A'][3]:.0f}% rate it 4 or 5 (top-box {100*sq['A'][2]:.0f}%). Common go benchmarks for a favourable purchase-intent share are 80-90% top-two-box (or the company's own norms from past successful launches); {100*sq['A'][3]:.0f}% is well below that. Being the best of a weak set is not the same as being good enough.

PASS if report.md says A's absolute level of intent (top-two-box about {100*sq['A'][3]:.0f}%) is low or needs comparing against a benchmark/norm, and recommends improving, reworking or re-testing A rather than an unconditional go.
FAIL if it recommends taking A straight into development with no caveat about the absolute level of purchase intent.
"""
write_case(NAME, {"resources/concept_survey.csv": csv_text}, prompt,
           [("screener", 2, g_scr), ("paired", 3, g_pair), ("level", 2, g_lvl)])
