"""Breadth benchmark, incrementality: display conversion lift study readout (Marigold Pet Supply, September 2026).

Randomised 80/20 PSA test. Subtle problems (4): the readout's "incremental
conversions" subtract control converters from treatment converters without
scaling for the 80/20 split (should be treatment conversions minus control
rate x treatment users); the test cost counts only treatment impressions,
although the PSA impressions served to control were paid too; the
weekday-only recommendation rests on a pivot gap whose interaction test is not
significant; lift by frequency band rises then turns negative above 50
impressions, where about a third of impressions went (DECISION: keep all days
and cap frequency instead of going weekday-only).
Decoys (2): the 80/20 split (planned, not a sample ratio mismatch); balance
checks all with p > 0.05."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-attrib-lift-study"
rng = random.Random(13579)
CPM = 3.10
MARGIN_PER_CONV = 30.0
NT, NC = 400000, 100000
BANDS = [("01-05", 0.40, 3, 0.0090, 0.04), ("06-15", 0.28, 10, 0.0140, 0.17), ("16-30", 0.17, 22, 0.0200, 0.34),
         ("31-50", 0.09, 40, 0.0260, 0.22), ("51+", 0.06, 92, 0.0300, -0.03)]
DAY = {"weekday": (0.70, 1.15), "weekend": (0.30, 0.65)}

def binom(n, p):
    return max(0, int(round(rng.gauss(n * p, math.sqrt(n * p * (1 - p))))))

joint = []  # band, day, group, users, impressions, converters
for band, share, ipu, c_cvr, lift in BANDS:
    for day, (dshare, k) in DAY.items():
        for g, N in (("treatment", NT), ("control", NC)):
            users = int(round(N * share * dshare))
            imps = int(users * ipu * rng.uniform(0.97, 1.03))
            p = c_cvr * (1 + lift * k) if g == "treatment" else c_cvr
            joint.append([band, day, g, users, imps, binom(users, p)])

def sumby(keyf):
    out = {}
    for r in joint:
        k = keyf(r); o = out.setdefault(k, [0, 0, 0]); o[0] += r[3]; o[1] += r[4]; o[2] += r[5]
    return out
grp = sumby(lambda r: r[2])
by_band = sumby(lambda r: (r[0], r[2]))
by_day = sumby(lambda r: (r[1], r[2]))

summary_rows = [[g, grp[g][0], grp[g][2], grp[g][1], "display ad" if g == "treatment" else "PSA (charity ad)"] for g in ("treatment", "control")]
band_rows = [[b, g, by_band[(b, g)][0], by_band[(b, g)][1], by_band[(b, g)][2]] for b, *_ in BANDS for g in ("treatment", "control")]
day_rows = [[d, g, by_day[(d, g)][0], by_day[(d, g)][2]] for d in DAY for g in ("treatment", "control")]
balance = [["prior_90d_site_visits", 2.41, 2.43, 0.62], ["prior_90d_orders", 0.38, 0.37, 0.48], ["account_age_days", 412, 409, 0.71],
           ["share_mobile", 0.64, 0.64, 0.83], ["share_returning_customer", 0.31, 0.30, 0.29]]

# ---------- ground truth ----------
ut, it_, ct = grp["treatment"]; uc, ic, cc = grp["control"]
rt, rc = ct / ut, cc / uc
lift = rt / rc - 1
inc = ct - rc * ut
naive_inc = ct - cc
cost_t = it_ * CPM / 1000; cost_c = ic * CPM / 1000; cost_all = cost_t + cost_c
poas_naive = (naive_inc * MARGIN_PER_CONV - cost_t) / cost_t
poas = (inc * MARGIN_PER_CONV - cost_all) / cost_all
poas_t_only = (inc * MARGIN_PER_CONV - cost_t) / cost_t
# day segments and interaction (Woolf test on log odds ratios)
def seg(d):
    u1, _, c1 = by_day[(d, "treatment")]; u0, _, c0 = by_day[(d, "control")]
    l = (c1 / u1) / (c0 / u0) - 1
    lor = math.log((c1 / (u1 - c1)) / (c0 / (u0 - c0)))
    v = 1 / c1 + 1 / (u1 - c1) + 1 / c0 + 1 / (u0 - c0)
    return l, lor, v
lwd, lor_wd, v_wd = seg("weekday"); lwe, lor_we, v_we = seg("weekend")
z_int = (lor_wd - lor_we) / math.sqrt(v_wd + v_we)
p_int = math.erfc(abs(z_int) / math.sqrt(2))
# frequency bands
band_lift = {}
for b, *_ in BANDS:
    u1, i1, c1 = by_band[(b, "treatment")]; u0, _, c0 = by_band[(b, "control")]
    band_lift[b] = (c1 / u1) / (c0 / u0) - 1
imp51 = by_band[("51+", "treatment")][1] / it_
peak = max(band_lift, key=band_lift.get)
# SRM check for decoy: 80/20 planned
exp_t = (ut + uc) * 0.8
chi = (ut - exp_t) ** 2 / exp_t + (uc - (ut + uc) * 0.2) ** 2 / ((ut + uc) * 0.2)

assert 0.12 < lift < 0.22 and naive_inc > 4 * inc
assert poas_naive > 5 and poas < 0.6 * poas_t_only and poas > -0.5
assert lwd > 1.5 * lwe and p_int > 0.1, (lwd, lwe, p_int)
assert band_lift["51+"] < 0.02 and peak in ("16-30", "31-50") and 0.25 < imp51 < 0.4
assert chi < 3.84

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

readout = f"""# Marigold Pet Supply: display conversion lift study, September 2026 (agency readout)

Design: users randomly split 80% treatment (our display ads) / 20% control (charity PSA in the same slots), 1-30 September.

- Conversion rate: treatment {pc(rt, 2)} vs control {pc(rc, 2)}, lift {pc(lift)}.
- Incremental conversions: {ct:,} - {cc:,} = {naive_inc:,}.
- Campaign cost: {it_:,} impressions at €{CPM:.2f} CPM = {eur(cost_t)}. Incremental profit at €{MARGIN_PER_CONV:.0f} per conversion: {eur(naive_inc * MARGIN_PER_CONV)}. POAS {poas_naive:.1f}.
- Lift is {pc(lwd)} on weekdays vs {pc(lwe)} at weekends.

Recommendations: switch display to a weekday-only schedule and double the budget.
"""

files = {
    "resources/lift_study_readout.md": readout,
    "resources/lift_study_summary.csv": to_csv(["group", "users", "converters", "impressions", "creative"], summary_rows),
    "resources/lift_by_frequency_band.csv": to_csv(["impressions_per_user_band", "group", "users", "impressions", "converters"], band_rows),
    "resources/lift_by_day_type.csv": to_csv(["first_exposure_day_type", "group", "users", "converters"], day_rows),
    "resources/balance_checks.csv": to_csv(["pre_period_variable", "treatment_mean", "control_mean", "p_value"], balance),
}

prompt = """
We're Marigold Pet Supply. We ran a conversion lift study on our display campaign in September and the agency sent their readout. Everything is in resources/. What did the study show, and what should we do with display next quarter? Write report.md with your numbers and recommendation.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Incremental conversions miscounted. The readout subtracts control converters from treatment converters ({ct:,} - {cc:,} = {naive_inc:,}) although control is 20% of users and treatment 80%. Correct: treatment conversions - control rate x treatment users = {ct:,} - {pc(rc, 3)} x {ut:,} = {inc:,.0f}. Found if report.md recomputes incremental conversions within 10% of {inc:,.0f} or explains the scaling error.
2. Test cost leaves out the PSA. Control saw {ic:,} paid PSA impressions ({eur(cost_c)} at the same CPM). Full test cost {eur(cost_all)}; POAS on the corrected incremental conversions is {poas:.2f} (or {poas_t_only:.2f} counting only the display impressions, the cost of running the campaign without a test), not {poas_naive:.1f}. Found if report.md says the control's PSA impressions are a paid cost of the test (adds them to the test cost or POAS).
3. Weekday-only claim not supported. Lift {pc(lwd)} weekday vs {pc(lwe)} weekend, but the interaction test (difference in log odds ratios) gives z = {z_int:.2f}, p = {p_int:.2f}: no significant difference. Found if report.md says the weekday/weekend gap is not statistically significant / needs an interaction test or a follow-up test.
4. Frequency. Lift by impressions per user: {', '.join(f'{b}: {pc(v, 0)}' for b, v in band_lift.items())}. The 51+ band has no lift but takes {pc(imp51, 0)} of treatment impressions. Found if report.md flags the falling/negative lift at high frequency and suggests a frequency cap.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: do NOT switch to a weekday-only schedule (the weekday/weekend difference is not significant, p = {p_int:.2f}) and do not double the budget on the readout's inflated numbers. Keep running on all days and add a frequency cap around the band where lift peaks ({peak} impressions per user), cutting the 51+ impressions that add nothing ({pc(imp51, 0)} of impressions).

Naive wrong answer: the agency's "switch to weekday-only and double the budget".

PASS if report.md's main recommendation rejects weekday-only scheduling AND recommends a frequency cap (or reallocating away from the high-frequency band) rather than doubling budget.
FAIL if it recommends weekday-only, endorses doubling the budget on the readout's POAS, or gives no clear recommendation.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Treatment has {ut:,} users and control {uc:,} (80/20). This is the planned split; against 80/20 the chi-square is {chi:.2f} (no sample ratio mismatch).
- D2. Balance checks: all pre-period variables have p-values between 0.29 and 0.83, meaning no detectable imbalance (high p is good here).

PASS if report.md does not call the 80/20 split an imbalance or sample ratio mismatch, and does not read the balance-check p-values as a failure.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: lift {lift:.3f}; inc {inc:.0f} vs naive {naive_inc}; poas {poas:.2f} t-only {poas_t_only:.2f} naive {poas_naive:.1f}; "
      f"wd {lwd:.3f} we {lwe:.3f} p {p_int:.2f}; bands {', '.join(f'{b} {v:.2f}' for b, v in band_lift.items())}; 51+ imps {imp51:.2f}")
