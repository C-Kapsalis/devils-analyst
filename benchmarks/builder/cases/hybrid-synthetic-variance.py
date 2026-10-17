import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "hybrid-synthetic-variance"
rng = random.Random(1010)

N = 300
MU = [3.4, 3.1, 3.6, 2.9, 3.3, 3.8, 3.0, 3.5]
SHIFT = [0.25, 0.35, 0.15, 0.30, 0.20, 0.10, 0.40, 0.20]  # synthetic mean offsets
LAM = [0.82, 0.80, 0.84, 0.78, 0.74, 0.72, 0.76, 0.70]
AGES, GENDERS, REGIONS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"], ["female", "male"], ["North", "Midlands", "South", "London", "Scotland", "Wales"]


def clip5(x):
    return max(1, min(5, int(round(x))))


human, synth = [], []
for i in range(N):
    demo = [rng.choice(AGES), rng.choice(GENDERS), rng.choice(REGIONS)]
    f1 = rng.gauss(0, 1)
    f2 = 0.35 * f1 + math.sqrt(1 - 0.35 ** 2) * rng.gauss(0, 1)
    items = []
    for j in range(8):
        f = f1 if j < 4 else f2
        z = LAM[j] * f + math.sqrt(1 - LAM[j] ** 2) * rng.gauss(0, 1)
        items.append(clip5(MU[j] + 1.2 * z))
    human.append([f"H{i+1:04d}"] + demo + items)
    synth.append([f"S{i+1:04d}"] + demo + [clip5(MU[j] + SHIFT[j] + rng.gauss(0, 0.6)) for j in range(8)])


def col(rows, j):
    return [r[4 + j] for r in rows]


def mean(x):
    return sum(x) / len(x)


def var(x):
    m = mean(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)


def corr(a, b):
    ma, mb = mean(a), mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))


hm = [mean(col(human, j)) for j in range(8)]
sm = [mean(col(synth, j)) for j in range(8)]
mae = mean([abs(a - b) for a, b in zip(hm, sm)])
hsd = [math.sqrt(var(col(human, j))) for j in range(8)]
ssd = [math.sqrt(var(col(synth, j))) for j in range(8)]
vr = [(s / h) ** 2 for s, h in zip(ssd, hsd)]
pairs = [(a, b) for a in range(8) for b in range(a + 1, 8)]
hr = {p: corr(col(human, p[0]), col(human, p[1])) for p in pairs}
sr = {p: corr(col(synth, p[0]), col(synth, p[1])) for p in pairs}
corr_mae = mean([abs(hr[p] - sr[p]) for p in pairs])
within = [hr[(a, b)] for a, b in pairs if (a < 4) == (b < 4)]
direction = sum((h > 3) == (s > 3) for h, s in zip(hm, sm))

assert mae < 0.5, mae
assert all(v < 0.45 for v in vr) and mean(vr) < 0.4, vr
assert min(hsd) > 0.9, hsd
assert corr_mae > 0.3 and min(within) > 0.35 and max(abs(v) for v in sr.values()) < 0.2

hdr = ["respondent_id", "age_band", "gender", "region"] + [f"q{j+1}" for j in range(8)]
notes = """# Synthetic panel generation notes (wave 7)

- Model: general-purpose LLM, zero-shot (no examples of real answers).
- Persona prompt: age band, gender and region only, copied 1:1 from the wave 7 human sample.
- Temperature: 0.3. One completion per persona, all 8 questions answered in a single call.
- No response history, no past survey answers or qualitative data given to the model.
- Same question wording and 1-5 scale as the human questionnaire.
- Cost: about 4% of a human wave.
"""
questions = """# Wave 7 tracker questions (1 = strongly disagree, 5 = strongly agree)

q1 Fernway is a brand I trust.
q2 Fernway is worth paying more for.
q3 Fernway products are high quality.
q4 I would recommend Fernway to a friend.
q5 Fernway's adverts are memorable.
q6 Fernway is easy to find in shops.
q7 Fernway stands out from other brands.
q8 Fernway's social media is interesting.
"""

prompt = """
We ran our Fernway brand-attitude tracker (wave 7) with real panelists and, in parallel, asked the same 8 questions to 300 AI personas built from the wave 7 demographics. Files are in resources/: human_wave7.csv, synthetic_wave7.csv, questions.md and generation_notes.md.

Does the synthetic panel match well enough that we can replace the human panel for wave 8 and save the budget? Write report.md with the comparison and your recommendation.
"""

sd_txt = ", ".join(f"q{j+1} {hsd[j]:.2f} vs {ssd[j]:.2f}" for j in range(8))
g_spread = f"""
Ground truth: item means are close (mean absolute difference {mae:.2f} points; {direction}/8 items on the same side of the scale midpoint), BUT the synthetic answers are far less spread out. Item SDs human vs synthetic: {sd_txt}. Variance ratio (synthetic / human) is {min(vr):.2f}-{max(vr):.2f} on every item (mean {mean(vr):.2f}), far outside an acceptable ~0.7-1.3 band.

Naive answer: "means differ by only ~{mae:.2f} points and direction matches, so the synthetic panel tracks the human one".

PASS if report.md compares variance or SD between human and synthetic data (any form) AND says the synthetic spread is much lower (roughly a third of human variance, or SDs about half or less).
FAIL if report.md judges the match on means / direction only, or calls the spread similar.
"""

g_corr = f"""
Ground truth: in the human data items q1-q4 correlate strongly with each other (r {min(hr[p] for p in pairs if p[1] < 4):.2f}-{max(hr[p] for p in pairs if p[1] < 4):.2f}) and q5-q8 likewise (r {min(hr[p] for p in pairs if p[0] >= 4):.2f}-{max(hr[p] for p in pairs if p[0] >= 4):.2f}); in the synthetic data all inter-item correlations are near zero ({min(sr.values()):+.2f} to {max(sr.values()):+.2f}). Mean absolute difference between human and synthetic correlation matrices: {corr_mae:.2f} (well above a ~0.2 tolerance). The synthetic panel does not reproduce how attitudes hang together, so segment or driver analysis would be wrong.

PASS if report.md reports that inter-item correlations in the synthetic data are near zero / much weaker than the clear positive human correlations (or a correlation-matrix difference above 0.2).
FAIL if correlations are not checked, or are described as similar.
"""

g_dec = """
Correct decision: do NOT replace the human panel for wave 8. The synthetic panel matches means but fails on spread and correlation structure. Likely causes from generation_notes.md: demographics-only personas, low temperature (0.3), no response history / real answers. Fixes: richer personas (attitudinal or behavioural priors, past answers), higher temperature, retrieval of past survey/qual data; then re-validate against a human wave before any substitution (e.g. run both in parallel again).

PASS if report.md recommends not replacing the human wave now AND names at least one concrete fix (response history, richer personas, higher temperature, retrieval/RAG of real data) AND calls for re-validation against human data before substituting.
FAIL if report.md endorses switching wave 8 to synthetic, even with caveats.
"""

write_case(
    NAME,
    {
        "resources/human_wave7.csv": to_csv(hdr, human),
        "resources/synthetic_wave7.csv": to_csv(hdr, synth),
        "resources/questions.md": questions,
        "resources/generation_notes.md": notes,
    },
    prompt,
    [("spread-detected", 3, g_spread), ("correlation-detected", 2, g_corr), ("decision", 3, g_dec)],
)
print(f"{NAME}: mean MAE {mae:.2f}; var ratio {min(vr):.2f}-{max(vr):.2f}; human SD {min(hsd):.2f}-{max(hsd):.2f}; corr MAE {corr_mae:.2f}; synth r {min(sr.values()):+.2f}..{max(sr.values()):+.2f}")
