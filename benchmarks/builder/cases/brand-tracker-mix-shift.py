import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "brand-tracker-mix-shift"
rng = random.Random(707)

N = 1200
SEGS = ["core", "occasional", "new_promo"]
CLV = {"core": 900, "occasional": 250, "new_promo": 60}
MIX = {1: {"core": 0.50, "occasional": 0.30, "new_promo": 0.20}, 2: {"core": 0.30, "occasional": 0.30, "new_promo": 0.40}}
MEAN = {1: {"core": 8.4, "occasional": 7.05, "new_promo": 5.55}, 2: {"core": 7.05, "occasional": 7.05, "new_promo": 7.85}}
REPEAT = {"core": (0.62, 0.51), "occasional": (0.34, 0.33), "new_promo": (0.12, 0.14)}
WAVES = {1: "2025", 2: "2026"}


def score(mu):
    return max(0, min(10, int(round(rng.gauss(mu, 1.5)))))


rows = []
rid = 0
for w in (1, 2):
    for s in SEGS:
        for _ in range(int(N * MIX[w][s])):
            rid += 1
            b = score(MEAN[w][s])
            rec = max(0, min(10, int(round(b + rng.gauss(-0.3, 1.0)))))
            rows.append([WAVES[w], f"R{rid:05d}", s, b, rec])
rng.shuffle(rows)
rows.sort(key=lambda r: r[0])


def m(xs):
    return sum(xs) / len(xs)


def sd(xs):
    mu = m(xs)
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))


seg = {(w, s): [r[3] for r in rows if r[0] == WAVES[w] and r[2] == s] for w in (1, 2) for s in SEGS}
tot = {w: m([r[3] for r in rows if r[0] == WAVES[w]]) for w in (1, 2)}
segm = {k: m(v) for k, v in seg.items()}
fixed_mix = {w: sum(MIX[1][s] * segm[(w, s)] for s in SEGS) for w in (1, 2)}
wts = {s: MIX[1][s] * CLV[s] for s in SEGS}
clv_w = {w: sum(wts[s] * segm[(w, s)] for s in SEGS) / sum(wts.values()) for w in (1, 2)}
a, b = seg[(1, "core")], seg[(2, "core")]
t_core = (m(a) - m(b)) / math.sqrt(sd(a) ** 2 / len(a) + sd(b) ** 2 / len(b))
core_value_share = wts["core"] / sum(wts.values())

assert round(tot[1], 1) == 7.3 and round(tot[2], 1) == 7.3, tot
assert segm[(1, "core")] - segm[(2, "core")] > 1.0 and t_core > 8
assert fixed_mix[1] - fixed_mix[2] > 0.12
assert clv_w[1] - clv_w[2] > 0.8

tracker = to_csv(["wave", "respondent_id", "segment", "brand_score", "would_recommend"], rows)
segments = to_csv(
    ["segment", "avg_clv_3yr", "active_customers_2026"],
    [["core", CLV["core"], 18400], ["occasional", CLV["occasional"], 41200], ["new_promo", CLV["new_promo"], 52900]],
)
repeat = to_csv(
    ["segment", "year", "repeat_purchase_rate"],
    [[s, y, REPEAT[s][i]] for s in SEGS for i, y in enumerate((2025, 2026))],
)

prompt = """
Our annual brand tracker for Saltmarsh Skincare is back. resources/tracker.csv has both waves (wave, respondent_id, segment, brand_score 0-10, would_recommend 0-10); resources/segments.csv has the average 3-year CLV per segment from our CRM, and resources/repeat_rates.csv has repeat purchase rates by segment.

The brand score was 7.3 last year and 7.3 this year. The board wants to know if the brand is healthy and whether we can keep next year's brand budget flat. Write report.md for the board.
"""

seg_txt = "; ".join(f"{s} {segm[(1, s)]:.2f} -> {segm[(2, s)]:.2f} (n {len(seg[(1, s)])} -> {len(seg[(2, s)])})" for s in SEGS)
g_mix = f"""
Ground truth: total brand score {tot[1]:.2f} (2025) -> {tot[2]:.2f} (2026), flat. By segment: {seg_txt}. The core segment fell about {segm[(1,'core')]-segm[(2,'core')]:.1f} points (t about {t_core:.0f}, clearly not noise). The respondent mix shifted from 50% core / 20% new_promo to 30% core / 40% new_promo, and new_promo respondents rate the brand higher this year, so the total stayed flat. Holding the 2025 mix fixed, the score falls {fixed_mix[1]:.2f} -> {fixed_mix[2]:.2f}.

Naive answer: "score stable at 7.3, the brand is healthy".

PASS if report.md splits the score by segment, reports the core segment's decline (about {segm[(1,'core')]:.1f} -> {segm[(2,'core')]:.1f}, within 0.2) AND explains the flat total as a change in respondent mix / growth of the new_promo segment.
FAIL if report.md concludes the brand is healthy or stable based on the total score, or does not report the core decline.
"""

g_value = f"""
Ground truth: the core segment carries most of the value (3-year CLV $900 vs $250 and $60; {core_value_share*100:.0f}% of CLV-weighted value at the 2025 mix). Weighting segment scores by 2025 share x CLV, the score falls {clv_w[1]:.2f} -> {clv_w[2]:.2f} ({clv_w[2]-clv_w[1]:+.2f}). Behaviour confirms it: core repeat purchase rate fell 62% -> 51%, while occasional (34% -> 33%) and new_promo (12% -> 14%) barely moved.

PASS if report.md weights by value (CLV or revenue) or otherwise states the core decline matters most because core customers carry most of the value, AND cites the core repeat-rate drop (62% -> 51%) as behavioural confirmation.
FAIL if report.md ignores CLV and repeat-rate data, or presents the repeat-rate data as reassuring.
"""

g_rec = """
Correct recommendation: the brand is NOT healthy among the customers who matter most. The board should not read the flat 7.3 as "keep budget flat, nothing to do": action should target core customers (research why they rate lower, retention / loyalty / service fixes, brand support aimed at them), and the budget decision should be framed as a trade-off with this risk stated.

PASS if report.md's recommendation targets the core segment (cause research, retention, brand support for core customers) and does not simply endorse "brand healthy, keep budget flat".
FAIL if report.md concludes the brand is healthy and the budget can stay flat with no core-segment action.
"""

write_case(
    NAME,
    {"resources/tracker.csv": tracker, "resources/segments.csv": segments, "resources/repeat_rates.csv": repeat},
    prompt,
    [("segment-mix", 3, g_mix), ("value-weighting", 2, g_value), ("recommendation", 1, g_rec)],
)
print(f"{NAME}: total {tot[1]:.2f}->{tot[2]:.2f}; {seg_txt}; fixed-mix {fixed_mix[1]:.2f}->{fixed_mix[2]:.2f}; CLV-w {clv_w[1]:.2f}->{clv_w[2]:.2f}; t_core {t_core:.1f}")
