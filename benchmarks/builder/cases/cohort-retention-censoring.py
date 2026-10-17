import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "cohort-retention-censoring"
rng = random.Random(5521)

MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]  # Jan..Sep 2026, export 1 Oct 2026
N_OFF = 9  # offsets 0..8

rows = []
obs = {}  # (cohort_idx, offset) -> retention for observed cells
sizes = []
for i, cm in enumerate(MONTHS):
    size = int(round(1200 * (1.11 ** i) * rng.uniform(0.96, 1.04)))
    sizes.append(size)
    # later cohorts retain better: monthly survival rises with cohort index
    s1 = 0.62 + 0.012 * i   # month-1 retention
    decay = 0.88 + 0.006 * i  # month-over-month survival after month 1
    max_obs = len(MONTHS) - 1 - i
    active = size
    for k in range(N_OFF):
        if k == 0:
            r = 1.0
        else:
            r = s1 * decay ** (k - 1)
        if k <= max_obs:
            active = size if k == 0 else int(round(size * r * rng.uniform(0.98, 1.02)))
            obs[(i, k)] = active / size
            rows.append([cm, size, k, active])
        else:
            rows.append([cm, size, k, 0])


def weighted(k):
    cs = [i for i in range(len(MONTHS)) if (i, k) in obs]
    return sum(obs[(i, k)] * sizes[i] for i in cs) / sum(sizes[i] for i in cs), cs


def simple(k):
    cs = [i for i in range(len(MONTHS)) if (i, k) in obs]
    return sum(obs[(i, k)] for i in cs) / len(cs)


def naive(k, weighted_=False):
    vals = [(r[3] / r[1], r[1]) for r in rows if r[2] == k]
    if weighted_:
        return sum(v * w for v, w in vals) / sum(w for _, w in vals)
    return sum(v for v, _ in vals) / len(vals)


w3, c3 = weighted(3)
w6, c6 = weighted(6)
s3, s6 = simple(3), simple(6)
n3, n6 = naive(3), naive(6)
n3w, n6w = naive(3, True), naive(6, True)

m3_first, m3_last = obs[(c3[0], 3)], obs[(c3[-1], 3)]
m6_first, m6_last = obs[(c6[0], 6)], obs[(c6[-1], 6)]
m1_series = [obs[(i, 1)] for i in range(len(MONTHS) - 1)]

assert c3 == list(range(6)) and c6 == list(range(3))
assert m3_last > m3_first + 0.04 and m6_last > m6_first + 0.03
assert all(b > a - 0.01 for a, b in zip(m1_series, m1_series[1:]))
assert w3 - n3 > 0.12 and w6 - n6 > 0.2 and w3 - n3w > 0.12
assert w3 > s3 and w6 > s6
# weighted vs simple differ by <1pp here, so both are accepted; the trap is the censored zeros

fmt = lambda x: f"{x*100:.1f}%"
m3_list = ", ".join(f"{MONTHS[i]} {fmt(obs[(i, 3)])}" for i in c3)
m6_list = ", ".join(f"{MONTHS[i]} {fmt(obs[(i, 6)])}" for i in c6)
m1_list = ", ".join(f"{MONTHS[i]} {fmt(obs[(i, 1)])}" for i in range(len(MONTHS) - 1))

prompt = """
The resources/ directory has our subscriber cohort export from the Lumen Streaming billing system, cohorts.csv (cohort_month, cohort_size, month_offset, active_subscribers). It was exported on 1 October 2026.

What's our average month-3 and month-6 retention across cohorts, and is retention getting better or worse? Write report.md with the numbers and what you conclude.
"""

g_main = f"""
The export is a full grid: offsets a cohort has not reached yet by 1 Oct 2026 are filled with active_subscribers = 0. Those zeros are not churn and must be excluded. Month-3 retention is observed only for the Jan-Jun 2026 cohorts; month-6 only for Jan-Mar 2026.

Ground truth (observed cohorts only):
- Month-3 retention: {fmt(w3)} weighted by cohort size ({fmt(s3)} simple average of cohorts).
- Month-6 retention: {fmt(w6)} weighted by cohort size ({fmt(s6)} simple average of cohorts).

Naive answers (zeros for unreached months included): month-3 {fmt(n3)} (size-weighted {fmt(n3w)}), month-6 {fmt(n6)} (size-weighted {fmt(n6w)}).

PASS if report.md's month-3 figure is within 2 percentage points of {fmt(w3)} or {fmt(s3)} AND its month-6 figure is within 2 percentage points of {fmt(w6)} or {fmt(s6)}.
FAIL if either figure is missing, or is near the naive values ({fmt(n3)} / {fmt(n6)} or {fmt(n3w)} / {fmt(n6w)}), or report.md treats the 0 rows for recent cohorts as subscribers who churned.
"""

g_trend = f"""
Ground truth: retention is improving for newer cohorts. Month-3 retention by cohort: {m3_list}. Month-6: {m6_list}. Month-1: {m1_list}.

Naive answer: "retention is getting worse", because recent cohorts show 0 at month 3/6 (they have not reached those months yet), so the per-cohort line drops to zero.

PASS if report.md concludes retention is improving / newer cohorts retain better, based on comparing cohorts at the same month offset.
FAIL if report.md says retention is getting worse or declining, or cites 0% retention for Jul-Sep 2026 cohorts as evidence.
"""

write_case(
    NAME,
    {"resources/cohorts.csv": to_csv(["cohort_month", "cohort_size", "month_offset", "active_subscribers"], rows)},
    prompt,
    [("observed-only", 3, g_main), ("trend", 2, g_trend)],
)
print(f"{NAME}: m3 {fmt(w3)} (simple {fmt(s3)}, naive {fmt(n3)}), m6 {fmt(w6)} (simple {fmt(s6)}, naive {fmt(n6)})")
