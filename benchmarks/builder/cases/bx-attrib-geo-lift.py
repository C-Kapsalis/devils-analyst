"""Breadth benchmark, incrementality: Meta geo holdout readout (Pinecrest Pantry meal kits, Aug-Oct 2026).

Subtle problems (4): the agency compares test with control regions during the
test only, but test regions were already ~11% bigger in the pre-period; the
difference-in-differences lift is ~4-5%, iROAS well below break-even
(DECISION); a school autumn break in the control regions (14-18 Sep)
depressed control sales during the test; control regions were not fully dark
(Meta spend ~12% of normal leaked in); the readout gives a point estimate with
no uncertainty, while the 90% interval for iROAS sits entirely below
break-even.
Decoys (2): control revenue is lower in absolute terms (smaller regions);
Meta-reported purchase value in test regions far exceeds the measured
incremental revenue (expected)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
from datetime import date, timedelta

NAME = "bx-attrib-geo-lift"
rng = random.Random(60317)
MARGIN = 0.35
AOV = 61.0
M_EFFECT = 0.050         # true revenue lift from Meta at full spend
LEAK = 0.12              # share of normal Meta spend still running in control during the test
HOLIDAY = (date(2026, 9, 14), date(2026, 9, 18))
pre_days = [date(2026, 8, 10) + timedelta(d) for d in range(28)]
test_days = [date(2026, 9, 7) + timedelta(d) for d in range(28)]
BT, BC = 10400.0, 9370.0   # base daily revenue without Meta
SPEND_T, SPEND_C = 330.0, 300.0

rows = []
for period, days in (("pre", pre_days), ("test", test_days)):
    for d in days:
        season = 1 + 0.03 * math.sin(d.toordinal() / 7 * 2 * math.pi) + (0.02 if period == "test" else 0.0)
        wk = 1.12 if d.weekday() in (5, 6) else 1.0
        common = season * wk * rng.gauss(1, 0.025)
        # test regions
        rev_t = BT * (1 + M_EFFECT) * common * rng.gauss(1, 0.035)
        sp_t = SPEND_T * rng.uniform(0.95, 1.05)
        # control regions
        m_c = M_EFFECT if period == "pre" else M_EFFECT * LEAK
        hol = 0.86 if (period == "test" and HOLIDAY[0] <= d <= HOLIDAY[1]) else 1.0
        rev_c = BC * (1 + m_c) * common * hol * rng.gauss(1, 0.035)
        sp_c = SPEND_C * rng.uniform(0.95, 1.05) * (1 if period == "pre" else LEAK)
        for g, rev, sp in (("test", rev_t, sp_t), ("control", rev_c, sp_c)):
            orders = int(round(rev / (AOV * rng.uniform(0.98, 1.02))))
            rows.append([d.isoformat(), g, period, orders, round(rev, 2), round(sp, 2)])

# ---------- ground truth ----------
def tot(g, p, f=lambda d: True):
    rr = [r for r in rows if r[1] == g and r[2] == p and f(date.fromisoformat(r[0]))]
    return sum(r[4] for r in rr), sum(r[5] for r in rr), len(rr)
Tt, Tsp, _ = tot("test", "test"); Ct, Csp, _ = tot("control", "test")
Tp, Tpsp, _ = tot("test", "pre"); Cp, Cpsp, _ = tot("control", "pre")
be = 1 / MARGIN
# naive: during-test comparison
naive_lift = Tt / Ct - 1
naive_inc = Tt - Ct
naive_iroas = naive_inc / Tsp
# DiD on all days
did_all = (Tt / Ct) / (Tp / Cp) - 1
# DiD excluding the control-region holiday days
nohol = lambda d: not (HOLIDAY[0] <= d <= HOLIDAY[1])
Tt2, Tsp2, n2 = tot("test", "test", nohol); Ct2, _, _ = tot("control", "test", nohol)
did = (Tt2 / Ct2) / (Tp / Cp) - 1
inc = Tt - Tt / (1 + did)
iroas = inc / Tsp
leak_share = (Csp / 28) / (Cpsp / 28)
did_adj = did / (1 - leak_share)
iroas_adj = (Tt - Tt / (1 + did_adj)) / Tsp
# uncertainty from daily log ratios
lr_pre = [math.log(a[4] / b[4]) for a, b in zip([r for r in rows if r[1] == "test" and r[2] == "pre"], [r for r in rows if r[1] == "control" and r[2] == "pre"])]
tt_rows = [r for r in rows if r[1] == "test" and r[2] == "test" and nohol(date.fromisoformat(r[0]))]
cc_rows = [r for r in rows if r[1] == "control" and r[2] == "test" and nohol(date.fromisoformat(r[0]))]
lr_test = [math.log(a[4] / b[4]) for a, b in zip(tt_rows, cc_rows)]
mean = lambda x: sum(x) / len(x)
var = lambda x: sum((v - mean(x)) ** 2 for v in x) / (len(x) - 1)
d_log = mean(lr_test) - mean(lr_pre)
se = math.sqrt(var(lr_test) / len(lr_test) + var(lr_pre) / len(lr_pre))
lo, hi = math.exp(d_log - 1.645 * se) - 1, math.exp(d_log + 1.645 * se) - 1
iroas_lo = (Tt - Tt / (1 + lo)) / Tsp; iroas_hi = (Tt - Tt / (1 + hi)) / Tsp
# holiday dip in control
hol_c = mean([r[4] for r in rows if r[1] == "control" and r[2] == "test" and not nohol(date.fromisoformat(r[0]))])
oth_c = mean([r[4] for r in cc_rows])
pre_gap = Tp / Cp - 1
META_REPORTED_PURCHASES = 1190
meta_val = META_REPORTED_PURCHASES * AOV

assert 0.09 < pre_gap < 0.14 and naive_lift > 0.15 and naive_iroas > be * 1.4
assert 0.025 < did < 0.065 and iroas < 0.75 * be and iroas_adj < be
assert iroas_hi < be, (iroas_lo, iroas_hi)
assert hol_c < 0.92 * oth_c and 0.08 < leak_share < 0.16
assert meta_val > 3 * inc

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

design = f"""# Pinecrest Pantry: Meta geo holdout (test design, marketing team)

- Test regions: North West, Yorkshire, East Midlands, Wales. Control regions: North East, West Midlands, South West, Scotland.
- Pre-period: 10 Aug - 6 Sep 2026 (Meta live everywhere). Test period: 7 Sep - 4 Oct 2026 (Meta paused in control regions, unchanged in test regions).
- Gross margin per order: {pc(MARGIN, 0)}.
- Meta Ads Manager reports {META_REPORTED_PURCHASES:,} purchases in the test regions during the test period (7-day click, 1-day view).
"""
calendar = to_csv(["region_group", "event", "start_date", "end_date"], [
    ["control", "School autumn break (Scotland and North East)", HOLIDAY[0].isoformat(), HOLIDAY[1].isoformat()],
    ["test", "none", "", ""],
])
readout = f"""# Geo test readout (agency)

During the test period, test regions generated {eur(Tt)} in revenue vs {eur(Ct)} in control regions: +{pc(naive_lift)}.
Incremental revenue from Meta = {eur(naive_inc)} on {eur(Tsp)} of test-region Meta spend: iROAS {naive_iroas:.2f}x, above the {be:.2f}x break-even.
Recommendation: Meta is clearly incremental; keep spend and scale nationally by 25%.
"""

files = {
    "resources/geo_test_design.md": design,
    "resources/geo_test_readout_agency.md": readout,
    "resources/geo_test_daily.csv": to_csv(["date", "region_group", "period", "orders", "revenue", "meta_spend"], rows),
    "resources/regional_calendar.csv": calendar,
}

prompt = """
We're Pinecrest Pantry (meal kits, UK). We ran a geo holdout to see whether Meta ads actually drive sales. The test design, the agency's readout, the daily results by region group and a regional calendar are in resources/. What did the test show, and should we keep spending on Meta at this level? Write report.md with the numbers and your recommendation.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Raw comparison ignores the pre-period gap. Test regions were already {pc(pre_gap)} above control in the pre-period (Meta live everywhere). The agency's +{pc(naive_lift)} compares the groups during the test only. Difference-in-differences (test-period ratio over pre-period ratio, excluding the control holiday days) gives a lift of about {pc(did)}; incremental revenue about {eur(inc)}, iROAS about {iroas:.2f}x vs break-even {be:.2f}x (agency: {naive_iroas:.2f}x). Found if report.md uses the pre-period as a baseline (DiD or equivalent) and gets a lift within 2 points of {pc(did)} or an iROAS below break-even.
2. Control-region school holiday. The regional calendar shows a school autumn break in control regions 14-18 Sep; control revenue those days averaged {eur(hol_c)} vs {eur(oth_c)} on other test days. Found if report.md flags the holiday as depressing control (inflating the measured lift) and excludes/adjusts for it.
3. Control not fully dark. Control regions still had Meta spend during the test ({eur(Csp)}, about {pc(leak_share, 0)} of their pre-period daily level). Found if report.md notes the leaked spend (contamination; it slightly understates the effect: adjusted lift about {pc(did_adj)}, iROAS about {iroas_adj:.2f}x, still below break-even).
4. No uncertainty. The readout gives a point estimate only. From daily test/control log-ratios, the 90% interval for the lift is about {pc(lo)} to {pc(hi)}, i.e. iROAS about {iroas_lo:.2f}x to {iroas_hi:.2f}x, entirely below break-even. Found if report.md gives a confidence interval / significance assessment (any reasonable method) or states that the upper end stays below break-even.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: Meta at this spend level is NOT paying back. Measured lift is about {pc(did)} (iROAS about {iroas:.2f}x, at most about {iroas_hi:.2f}x at the top of a 90% interval) vs a break-even iROAS of {be:.2f}x. Do not scale; reduce Meta spend (or test a lower spend level / different setup) rather than keep or grow it.

Naive wrong answer: the agency's "iROAS {naive_iroas:.2f}x, keep spend and scale nationally by 25%".

PASS if report.md's main recommendation is to reduce, cut or not scale Meta (re-testing at lower spend is fine) because incremental return is below break-even.
FAIL if it recommends keeping spend unchanged as the main call, scaling, or accepts the agency's iROAS.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Control regions have lower revenue in absolute terms (pre-period {eur(Cp)} vs {eur(Tp)} in test regions). Groups of different size are fine; the comparison uses the ratio against the pre-period.
- D2. Meta reports {META_REPORTED_PURCHASES:,} purchases (about {eur(meta_val)}) in the test regions, far more than the measured incremental revenue (about {eur(inc)}). Expected: platform attribution counts purchases that would have happened anyway; that is why the test was run.

PASS if report.md does not call the size difference between groups a flaw that invalidates the test (noting it is handled by the pre-period comparison is fine), and does not treat the Meta-reported vs incremental gap as a tracking error.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: pre gap {pre_gap:.3f}; naive lift {naive_lift:.3f} iroas {naive_iroas:.2f}; DiD all {did_all:.3f} clean {did:.3f} iroas {iroas:.2f} "
      f"[{iroas_lo:.2f}, {iroas_hi:.2f}] adj {iroas_adj:.2f}; be {be:.2f}; leak {leak_share:.2f}; hol {hol_c:.0f} vs {oth_c:.0f}")
