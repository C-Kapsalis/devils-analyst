"""Meta conversion lift study with PSA control, read by segment (Ridgeline Running, Sep 2026).

Planted subtle problems (4):
P1 (decision) Incremental conversions computed as lift % x control conversions
   (control is the 30% cell), not test conversions - control rate x test users:
   understated ~2.3x, so the readout's POAS is negative when it is positive.
P2 Device pivot: "cut desktop, move to mobile" from lift by device with no
   interaction test; the difference is not significant.
P3 Thin cell: 65+ "+X% lift" rests on a handful of control conversions
   (n*p < 5): unreadable.
P4 Frequency: "10+ exposures convert best, raise the cap" reads conversion
   rates of heavily exposed users (natural buyers: the PSA control converts
   just as well at 10+); lift at 10+ is about zero while it holds ~1/3 of
   impressions.
Decoys (2): 70/30 split by design and observed matches; the 18-24 negative lift
   is read correctly as noise (kept in targeting)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-test-lift-segments"
SEED = 6
rng = random.Random(SEED)


def phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


N = {"test": 209874, "control": 90126}
MARGIN = 41.0   # contribution per conversion (EUR)
# exposure band: user share, control CVR, test lift, impressions per user (PSA impressions for control)
FREQ = [("1-2", 0.39, 0.0068, 0.14, 1.5), ("3-5", 0.29, 0.0105, 0.26, 4.0), ("6-9", 0.18, 0.0150, 0.21, 7.4), ("10+", 0.14, 0.0235, -0.04, 13.8)]
# device / age: user share, control CVR, test lift (last level is the residual)
DEV = [("mobile", 0.64, 0.0112, 0.18), ("desktop", None, None, None)]
AGE = [("18-24", 0.17, 0.0100, -0.05), ("65+", 0.006, 0.0074, 0.80), ("25-34", 0.27, 0.0120, 0.16),
       ("35-44", 0.25, 0.0122, 0.15), ("45-54", 0.18, 0.0115, 0.14), ("55-64", None, None, None)]

cells = {}
imps = {}
for arm in ("test", "control"):
    tu = tc = ti = 0
    for lvl, sh, cr, lf, ipu in FREQ:
        u = round(N[arm] * sh * rng.uniform(0.99, 1.01)) if lvl != "10+" else N[arm] - tu
        c = round(u * cr * ((1 + lf) if arm == "test" else 1) * rng.uniform(0.985, 1.015))
        im = round(u * ipu * rng.uniform(0.98, 1.02))
        cells[("exposure_band", lvl, arm)] = [u, c, im]
        tu += u; tc += c; ti += im
    cells[("total", "all", arm)] = [tu, tc, ti]
    imps[arm] = ti
    for dim, spec in (("device", DEV), ("age_band", AGE)):
        su = sc = si = 0
        for lvl, sh, cr, lf in spec:
            if sh is None:
                u, c, im = tu - su, tc - sc, ti - si
            else:
                u = round(N[arm] * sh * rng.uniform(0.99, 1.01))
                c = round(u * cr * ((1 + lf) if arm == "test" else 1))
                if lvl == "65+" and arm == "control":
                    c = 4
                im = round(u * ti / tu * rng.uniform(0.95, 1.05))
            cells[(dim, lvl, arm)] = [u, c, im]
            su += u; sc += c; si += im
AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]


def get(dim, lvl):
    t = cells[(dim, lvl, "test")]; c = cells[(dim, lvl, "control")]
    return t, c


def lift_stats(dim, lvl):
    t, c = get(dim, lvl)
    rt, rc = t[1] / t[0], c[1] / c[0]
    lift = rt / rc - 1
    var = 1 / t[1] - 1 / t[0] + 1 / c[1] - 1 / c[0]
    return rt, rc, lift, var


def interaction(dim, a, b):
    _, _, la, va = lift_stats(dim, a)
    _, _, lb, vb = lift_stats(dim, b)
    z = (math.log(1 + la) - math.log(1 + lb)) / math.sqrt(va + vb)
    return z, 2 * (1 - phi(abs(z)))


T, C = get("total", "all")
rt, rc, lift_all, var_all = lift_stats("total", "all")
z_all = math.log(1 + lift_all) / math.sqrt(var_all)
p_all = 2 * (1 - phi(abs(z_all)))
inc_true = T[1] - rc * T[0]
inc_naive = lift_all * C[1]
spend = round(inc_true * MARGIN / 1.45, 2)
cpm_eff = spend / imps["test"] * 1000
psa_cost = round(imps["control"] * cpm_eff / 1000, 2)
poas_true = (inc_true * MARGIN - spend) / spend
poas_naive = (inc_naive * MARGIN - spend) / spend
cpa_true = spend / inc_true
cpa_naive = spend / inc_naive

z_dev, p_dev = interaction("device", "mobile", "desktop")
lm = lift_stats("device", "mobile")[2]; ld = lift_stats("device", "desktop")[2]
t65, c65 = get("age_band", "65+")
l65 = lift_stats("age_band", "65+")[2]
l1824 = lift_stats("age_band", "18-24")
z1824 = math.log(1 + l1824[2]) / math.sqrt(l1824[3]); p1824 = 2 * (1 - phi(abs(z1824)))
f10 = lift_stats("exposure_band", "10+")
f12 = lift_stats("exposure_band", "1-2")
# 10+ vs all other bands pooled
lo = [cells[("exposure_band", b, arm)] for b in ("1-2", "3-5", "6-9") for arm in ("test",)]
lo_c = [cells[("exposure_band", b, "control")] for b in ("1-2", "3-5", "6-9")]
lo_t = [sum(x[i] for x in lo) for i in range(3)]; lo_cc = [sum(x[i] for x in lo_c) for i in range(3)]
l_lo = (lo_t[1] / lo_t[0]) / (lo_cc[1] / lo_cc[0]) - 1
v_lo = 1 / lo_t[1] - 1 / lo_t[0] + 1 / lo_cc[1] - 1 / lo_cc[0]
z_f = (math.log(1 + l_lo) - math.log(1 + f10[2])) / math.sqrt(v_lo + f10[3])
p_f = 2 * (1 - phi(abs(z_f)))
f10_imp_share = cells[("exposure_band", "10+", "test")][2] / imps["test"]
f10_ci = (math.exp(math.log(1 + f10[2]) - 1.96 * math.sqrt(f10[3])) - 1, math.exp(math.log(1 + f10[2]) + 1.96 * math.sqrt(f10[3])) - 1)
srm_chi = (T[0] - 0.7 * (T[0] + C[0])) ** 2 / (0.7 * (T[0] + C[0])) + (C[0] - 0.3 * (T[0] + C[0])) ** 2 / (0.3 * (T[0] + C[0]))

ASSERTS = [
    p_all < 0.01, poas_true > 0.15, poas_naive < -0.2,
    lm - ld > 0.08, p_dev > 0.15,
    c65[1] <= 4, l65 > 0.4,
    l1824[2] < -0.03, p1824 > 0.3,
    abs(f10[2]) < 0.06, p_f < 0.01, f10_imp_share > 0.3,
    f10[0] > 2.5 * f12[0], srm_chi < 3.84, 4 < cpm_eff < 12,
]
if __name__ == "__main__" and not all(ASSERTS):
    raise AssertionError(ASSERTS)

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"EUR {x:,.0f}"

seg_rows = []
for dim, lvls in (("total", ["all"]), ("device", [d[0] for d in DEV]), ("age_band", AGE_ORDER), ("exposure_band", [f[0] for f in FREQ])):
    for lvl in lvls:
        for arm in ("test", "control"):
            u, cv, im = cells[(dim, lvl, arm)]
            seg_rows.append([dim, lvl, arm, u, im, cv])

readout = f"""# Conversion lift study: Always-on prospecting, September 2026

Prepared by the paid social agency for Ridgeline Running. Study run on Meta, 1 to 28 September 2026.

## Design

- Audience split at random: 70% test (saw our ads), 30% control (saw a public service ad, PSA, in the same placements).
- Conversion = online purchase within the study window, any device.
- Weekly frequency cap during the study: 6 impressions per user per week.

## Headline

| Cell | Users | Converters | Conversion rate |
|---|---|---|---|
| Test | {T[0]:,} | {T[1]:,} | {pc(rt, 2)} |
| Control | {C[0]:,} | {C[1]:,} | {pc(rc, 2)} |

Lift: **+{pc(lift_all)}** (p = {p_all:.4f}). Split check: {T[0] / (T[0] + C[0]):.1%} / {C[0] / (T[0] + C[0]):.1%} against the planned 70 / 30, fine.

Incremental conversions = lift x control conversions = {lift_all:.3f} x {C[1]:,} = **{inc_naive:,.0f}**.
Media spend on the test cell: {eur(spend)} (the PSA impressions, {eur(psa_cost)}, are a one-off study cost and are left out).
Incremental CPA = {eur(cpa_naive)}; at {eur(MARGIN)} contribution per order, **POAS = {poas_naive:+.2f}**. The campaign loses money as it runs today.

## Segments (lift_by_segment.csv)

- Device: mobile lift {pc(lm)}, desktop {pc(ld)}. Desktop is barely moving.
- Age: 65+ shows the strongest lift of any group, {pc(l65, 0)}. 18-24 shows {pc(l1824[2])}; with these numbers that is within noise, so no change for 18-24.
- Exposure: users who saw 10 or more ads converted at {pc(f10[0], 2)}, against {pc(f12[0], 2)} for 1-2 ads. More exposure clearly drives purchase.

## Recommendations

1. Cut the total budget by 25% until POAS is positive.
2. Within what is left, stop desktop delivery and move it to mobile.
3. Add a 65+ ad set with its own budget.
4. Raise the weekly frequency cap from 6 to 10.
"""

files = {
    "resources/lift_study_readout.md": readout,
    "resources/lift_by_segment.csv": to_csv(["dimension", "level", "cell", "users", "impressions", "converters"], seg_rows),
}

prompt = """
Our paid social agency ran a conversion lift study on our always-on Meta prospecting in September. Their readout is resources/lift_study_readout.md and the segment numbers are in resources/lift_by_segment.csv. Contribution per order is EUR 41, as they say. I have to agree next quarter's Meta plan with them on Monday. Should we go with their four recommendations? Write your view in report.md.
"""

g_recall = f"""
The readout contains 4 planted problems. Ground truth (computed from lift_by_segment.csv):

1. Incremental conversions on the wrong base. Incremental = test converters - control rate x test users = {T[1]:,} - {pc(rc, 3)} x {T[0]:,} = about {inc_true:,.0f}, not lift x control conversions = {inc_naive:,.0f} (the control cell is only 30% of users). Incremental CPA is about {eur(cpa_true)} and POAS about {poas_true:+.2f}, not {poas_naive:+.2f}: the campaign makes money. Counts as found if report.md recomputes incremental conversions on the test cell (any figure within 10% of {inc_true:,.0f}) or gives a positive POAS / profit.
2. Device split is not a tested difference. Mobile lift {pc(lm)} vs desktop {pc(ld)}; the test of the difference (interaction) gives z = {z_dev:.2f}, p = {p_dev:.2f}. Counts as found if report.md says the device gap is not statistically established (or is within noise / needs an interaction test) so stopping desktop is not supported.
3. 65+ cell too small. 65+ has {c65[0]:,} control users and {c65[1]} control converters ({t65[1]} in test); the {pc(l65, 0)} lift is unreadable. Counts as found if report.md flags the tiny 65+ sample/converter count.
4. Frequency read as cause. Users with 10+ exposures convert at {pc(f10[0], 2)} in test but {pc(f10[1], 2)} in the PSA control too: lift at 10+ is {pc(f10[2])} (95% CI {pc(f10_ci[0], 0)} to {pc(f10_ci[1], 0)}) vs {pc(l_lo)} below 10 exposures (difference p = {p_f:.4f}), while 10+ users take {pc(f10_imp_share, 0)} of test impressions. Heavy-exposure users are likely buyers anyway. Counts as found if report.md compares 10+ test vs control (or says the high conversion rate is selection, not exposure) and says raising the cap is not supported.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 4, each with its substance (a number or the specific comparison). FAIL otherwise.
"""

g_decision = f"""
Correct main recommendation: keep the campaign (do not cut the budget for being unprofitable) and do not raise the frequency cap. With incremental conversions computed correctly (about {inc_true:,.0f}), incremental CPA is about {eur(cpa_true)} against {eur(MARGIN)} contribution per order, POAS about {poas_true:+.2f}. Extra impressions beyond 10 per user add no measurable lift (10+ band lift {pc(f10[2])}) and are about {pc(f10_imp_share, 0)} of impressions, so if anything the cap should stay or be tested lower. Device and 65+ moves are at most hypotheses to test.

Naive wrong answer: follow the agency: cut budget 25% because POAS is {poas_naive:+.2f}, stop desktop, add a 65+ ad set, raise the cap from 6 to 10.

PASS if report.md (a) rejects the 25% budget cut, saying the campaign is profitable/incremental POAS is positive (or that the readout's incremental count is too low), AND (b) does not endorse raising the frequency cap.
FAIL if it endorses the 25% cut or the cap increase, or accepts the readout's negative POAS.
"""

g_decoy = f"""
Two things look questionable but are correct and must not be presented as problems:
- D1. The split is 70% test / 30% control by design. Observed {T[0]:,} vs {C[0]:,} ({T[0] / (T[0] + C[0]):.2%} / {C[0] / (T[0] + C[0]):.2%}), chi-square {srm_chi:.2f} (p > 0.05): no sample ratio problem. The unequal cell sizes are not a flaw.
- D2. The 18-24 lift is {pc(l1824[2])} (p = {p1824:.2f}); the readout correctly calls it noise and makes no change for 18-24.

PASS if report.md does not call the 70/30 split a problem or an imbalance, and does not claim the ads hurt 18-24 or recommend excluding 18-24 on this evidence. Neutral mentions or agreeing they are fine PASS.
FAIL if it flags the unequal split as an imbalance/sample ratio issue, or says 18-24 should be cut/excluded because the lift is negative.
"""

if __name__ == "__main__":
    write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
    print(f"{NAME}: lift {lift_all:.3f} p {p_all:.4f}; inc {inc_true:.0f} vs naive {inc_naive:.0f}; POAS {poas_true:+.2f} vs {poas_naive:+.2f}; "
          f"dev {lm:.3f}/{ld:.3f} p {p_dev:.2f}; 65+ ctrl conv {c65[1]} lift {l65:.2f}; 18-24 {l1824[2]:.3f} p {p1824:.2f}; "
          f"10+ lift {f10[2]:.3f} vs <10 {l_lo:.3f} p {p_f:.4f} imp share {f10_imp_share:.2f}")
