"""Review an A/B test readout (Copperleaf Cookware, recommendation widget).

Planted problems (5): ship decision on p < 0.05 against zero while the platform
cost sets a break-even lift the data cannot show it beats (MUST); test ran
4 days, Monday to Thursday (MUST); "launch on mobile only" from a pivot with
no interaction test; lift given only in points and misread as a percent;
"lift consistent across the test" while it is concentrated in returning users
on days 1-2 (novelty).
Decoys (2): sample ratio check reported and correct; conversion rate per
user (orders / users), correct."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "review-ab-test-readout"
rng = random.Random(55120)
DATES = ["2026-09-14", "2026-09-15", "2026-09-16", "2026-09-17"]   # Monday to Thursday
MARGIN = 0.40
BASE = {("mobile", "new"): 0.0245, ("mobile", "returning"): 0.0360,
        ("desktop", "new"): 0.0330, ("desktop", "returning"): 0.0455}
SHARE = {("mobile", "new"): 0.36, ("mobile", "returning"): 0.26, ("desktop", "new"): 0.21, ("desktop", "returning"): 0.17}
DEV_MULT = {"mobile": 1.035, "desktop": 0.945}
RET_DAY = [1.30, 1.22, 1.03, 1.00]
NEW_MULT = 1.05
AOV = 88.0

def phi_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))

rows = []
for d, date in enumerate(DATES):
    day_total = int(rng.uniform(17600, 18400))
    for (dev, vt), sh in SHARE.items():
        for arm in ("control", "treatment"):
            users = int(round(day_total * sh / 2 * rng.uniform(0.985, 1.015)))
            rate = BASE[(dev, vt)]
            if arm == "treatment":
                rate *= DEV_MULT[dev] * (RET_DAY[d] if vt == "returning" else NEW_MULT)
            orders = int(round(users * rate * rng.uniform(0.97, 1.03)))
            revenue = round(orders * AOV * rng.uniform(0.96, 1.04), 2)
            rows.append([date, arm, dev, vt, users, orders, revenue])

def agg(f):
    sel = [r for r in rows if f(r)]
    return sum(r[4] for r in sel), sum(r[5] for r in sel), sum(r[6] for r in sel)

nc, oc, rc = agg(lambda r: r[1] == "control")
nt, ot, rt = agg(lambda r: r[1] == "treatment")
pc_, pt_ = oc / nc, ot / nt
diff = pt_ - pc_
rel = diff / pc_
pp = (oc + ot) / (nc + nt)
se_pool = math.sqrt(pp * (1 - pp) * (1 / nc + 1 / nt))
z0 = diff / se_pool
p0 = 2 * phi_sf(abs(z0))
se_un = math.sqrt(pc_ * (1 - pc_) / nc + pt_ * (1 - pt_) / nt)
ci_lo, ci_hi = diff - 1.96 * se_un, diff + 1.96 * se_un

# SRM (decoy)
exp_ = (nc + nt) / 2
chi_srm = (nc - exp_) ** 2 / exp_ + (nt - exp_) ** 2 / exp_
p_srm = math.erfc(math.sqrt(chi_srm / 2))

# business case
monthly_users = (nc + nt) / len(DATES) * 30.4
rev_per_user_c = rc / nc
monthly_rev = monthly_users * rev_per_user_c
BE_TARGET = rel - 0.008
cost = 1000 * round(BE_TARGET * monthly_rev * MARGIN / 1000)
be_rel = cost / MARGIN / monthly_rev
be_abs = be_rel * pc_
z_be = (diff - be_abs) / se_un
p_be = phi_sf(z_be)                         # one-sided, H0: lift <= break-even
ci_rel_lo, ci_rel_hi = ci_lo / pc_, ci_hi / pc_

# device pivot and interaction
def arm_rate(arm, f):
    n, o, _ = agg(lambda r: r[1] == arm and f(r))
    return n, o, o / n
dev = {}
for dv in ("mobile", "desktop"):
    n1, o1, r1 = arm_rate("control", lambda r: r[2] == dv)
    n2, o2, r2 = arm_rate("treatment", lambda r: r[2] == dv)
    se = math.sqrt(r1 * (1 - r1) / n1 + r2 * (1 - r2) / n2)
    dev[dv] = dict(rc=r1, rt=r2, d=r2 - r1, rel=(r2 - r1) / r1, se=se, oc=o1, ot=o2, nc=n1, nt=n2)
z_int = (dev["mobile"]["d"] - dev["desktop"]["d"]) / math.sqrt(dev["mobile"]["se"] ** 2 + dev["desktop"]["se"] ** 2)
p_int = 2 * phi_sf(abs(z_int))
z_desk = dev["desktop"]["d"] / dev["desktop"]["se"]

# novelty: lift by day and by visitor type
def lift(f):
    _, _, r1 = arm_rate("control", f)
    _, _, r2 = arm_rate("treatment", f)
    return r2 / r1 - 1
day_lift = [lift(lambda r, dt=dt: r[0] == dt) for dt in DATES]
ret_early = lift(lambda r: r[3] == "returning" and r[0] in DATES[:2])
ret_late = lift(lambda r: r[3] == "returning" and r[0] in DATES[2:])
new_lift = lift(lambda r: r[3] == "new")
early_lift = lift(lambda r: r[0] in DATES[:2])
late_lift = lift(lambda r: r[0] in DATES[2:])

# ---------- asserts ----------
assert p0 < 0.05, (z0, p0)
assert ci_lo > 0 and ci_rel_lo < be_rel < rel + 0.02, (ci_rel_lo, be_rel, rel)
assert p_be > 0.15, p_be
assert chi_srm < 3.84 and abs(nc / (nc + nt) - 0.5) < 0.005
assert dev["mobile"]["rel"] > 0.10 and dev["desktop"]["rel"] < 0.06, (dev["mobile"]["rel"], dev["desktop"]["rel"])
assert p_int > 0.05, (z_int, p_int)
assert ret_early > 0.20 and ret_late < 0.08 and early_lift > 2 * late_lift, (ret_early, ret_late, early_lift, late_lift)
assert rel > 0.06 and 100 * diff < 0.5   # points misread as percent: ~0.3 vs ~9%

pts = lambda x: f"{100 * x:.2f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"
usd = lambda x: f"${x:,.0f}"

artefact = f"""# A/B test readout: "Complete the set" recommendation widget

Copperleaf Cookware, product page test. Owner: ecommerce team.

## Setup

- Variant B adds the "Complete the set" recommendation widget (from our new personalisation platform) under the add-to-cart button on every product page. Control A is the current page.
- 50/50 split of all visitors, randomised per user.
- Primary metric: conversion rate = users who ordered / users exposed.
- Test window: {DATES[0]} to {DATES[-1]}.

## Sample ratio check

Control {nc:,} users, treatment {nt:,} users ({pc(nc / (nc + nt), 2)} / {pc(nt / (nc + nt), 2)}). Chi-square {chi_srm:.2f}, p = {p_srm:.2f}: no sample ratio mismatch.

## Results

| Variant | Users | Orders | Conversion rate | Revenue |
|---|---|---|---|---|
| A (control) | {nc:,} | {oc:,} | {pc(pc_, 2)} | {usd(rc)} |
| B (widget) | {nt:,} | {ot:,} | {pc(pt_, 2)} | {usd(rt)} |

**Conversion rate is up {pts(diff)} points for B. Two-proportion z-test: z = {z0:.2f}, p = {p0:.3f}. The result is statistically significant at 95%.** 95% confidence interval for the difference: +{pts(ci_lo)} to +{pts(ci_hi)} points.

In plain terms, the widget makes about {100 * diff:.1f}% more visitors buy.

The lift was consistent across the test, so we expect it to hold after launch.

## By device

| Device | A conversion | B conversion | Lift |
|---|---|---|---|
| Mobile | {pc(dev['mobile']['rc'], 2)} | {pc(dev['mobile']['rt'], 2)} | {pc(dev['mobile']['rel'])} |
| Desktop | {pc(dev['desktop']['rc'], 2)} | {pc(dev['desktop']['rt'], 2)} | {pc(dev['desktop']['rel'])} |

The widget clearly works on mobile and does little on desktop.

## Business case

The personalisation platform costs {usd(cost)} per month (licence and support). Our gross margin is {pc(MARGIN, 0)}. The test result is statistically significant, so the cost is justified.

## Recommendation

1. Ship the widget to 100% of mobile traffic on Monday and sign the 12-month platform contract.
2. Leave desktop on the current page for now.
"""

files = {
    "resources/ab_test_readout_complete_the_set.md": artefact,
    "resources/ab_test_daily.csv": to_csv(["date", "variant", "device", "visitor_type", "users_first_exposed", "orders", "revenue"], rows),
}

prompt = """
Our ecommerce team wrote up the product page test (resources/ab_test_readout_complete_the_set.md) and the raw daily numbers are in resources/ab_test_daily.csv. The head of ecommerce wants to sign the platform contract next week based on this. Is the readout right? Tell me what, if anything, needs fixing before it goes to her, and whether the recommendation stands. Write it up in report.md.
"""

g_recall = f"""
The readout contains 5 planted problems. Answer key:

1. Tested against zero, not against the break-even. The platform costs {usd(cost)} a month at a {pc(MARGIN, 0)} margin. Monthly revenue at control's rate is about {usd(monthly_rev)} (about {monthly_users:,.0f} users a month), so the widget must lift revenue by about {pc(be_rel)} just to pay for itself (break-even). The observed relative lift is {pc(rel)} with a 95% interval of roughly {pc(ci_rel_lo)} to {pc(ci_rel_hi)}; the lower end is below break-even, and a one-sided test against the break-even gives p = {p_be:.2f}. Significant against zero does not mean it pays. Counts as found if report.md says the decision must be tested against the cost or break-even lift (any break-even between {100 * be_rel - 1.5:.1f}% and {100 * be_rel + 1.5:.1f}% relative, a higher figure if computed on mobile revenue only, or an equivalent absolute or money figure) and that the data does not show the lift clears it.
2. Test too short. It ran 4 days, Monday {DATES[0]} to Thursday {DATES[-1]}, with no weekend. Counts as found if report.md says the test covers less than a full week (or no weekend) and should run whole weeks.
3. Segment winner from a pivot. "Ship to mobile only" rests on mobile lift {pc(dev['mobile']['rel'])} vs desktop {pc(dev['desktop']['rel'])}, with no interaction test; the difference between the two device lifts is not significant (z = {z_int:.2f}, p = {p_int:.2f}). Counts as found if report.md says the device difference is untested or not significant and the mobile-only rollout is a hypothesis.
4. Points misread as percent. The readout says the widget makes "about {100 * diff:.1f}% more visitors buy"; the {pts(diff)}-point gain is a relative lift of about {pc(rel)} ({ot:,} orders vs {pc(pc_, 2)} x {nt:,} = {pc_ * nt:,.0f} expected, about {ot - pc_ * nt:,.0f} incremental orders). Counts as found if report.md gives the relative lift (between {100 * rel - 1:.0f}% and {100 * rel + 1:.0f}%) or the incremental orders and says the "{100 * diff:.1f}%" wording is wrong.
5. Novelty, not a consistent lift. The lift by day falls from {pc(day_lift[0], 0)} and {pc(day_lift[1], 0)} on days 1-2 to {pc(day_lift[2], 0)} and {pc(day_lift[3], 0)} on days 3-4; returning users drive it early ({pc(ret_early, 0)} on days 1-2 vs {pc(ret_late, 0)} on days 3-4) while new users are steady at about {pc(new_lift, 0)}. Counts as found if report.md says the lift fades over the test or is concentrated in returning users early, so "consistent, will hold after launch" is not supported.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention such as "the test may need more data" does not count).
FAIL if it identifies fewer than 4.
"""

g_rank = f"""
Two of the problems are Must-fix because they decide whether to sign the contract:
- A. The ship decision tests the lift against zero (p = {p0:.3f}); against the break-even lift of about {pc(be_rel)} set by the {usd(cost)} monthly cost, the evidence is not there (lower end of the interval about {pc(ci_rel_lo)}, one-sided p = {p_be:.2f}).
- B. The test ran only 4 days (Monday to Thursday), less than a full week.
The lesser problems are: the mobile-only pivot, the points-as-percent wording, and the novelty pattern.

PASS if report.md flags both A and B and places each in its highest-severity group (Must fix, critical, or equivalent), or, if it uses no groups, lists both among its first three findings; other problems may share that group. The verdict must not endorse signing the contract or shipping on the current evidence.
FAIL if A or B is missing, is labelled lower severity (Should fix, Nice to have, minor) than any of the lesser problems, or if the verdict says the recommendation stands as written.
"""

g_decoy = f"""
The readout contains two elements that are correct and must not be flagged:
- D1. The sample ratio check: control {nc:,} vs treatment {nt:,} users ({pc(nc / (nc + nt), 2)} / {pc(nt / (nc + nt), 2)}), chi-square {chi_srm:.2f}, p = {p_srm:.2f}. There is no sample ratio mismatch.
- D2. Conversion rate is defined per user (users who ordered / users exposed), matching the randomisation unit; control {pc(pc_, 2)}, treatment {pc(pt_, 2)} are computed correctly from the daily file.

PASS if report.md does not present D1 or D2 as an error or something to fix. Mentioning either as correct or fine is a PASS.
FAIL if it says there is a sample ratio mismatch or the split is a problem, or says the conversion rate definition or the two conversion rates are wrong.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: cvr {pc_:.4f} -> {pt_:.4f} (rel {rel:.3f}, p0 {p0:.3f}); break-even {be_rel:.3f}, CI rel [{ci_rel_lo:.3f},{ci_rel_hi:.3f}], p_be {p_be:.2f}; "
      f"SRM chi {chi_srm:.2f}; mobile {dev['mobile']['rel']:.3f} desktop {dev['desktop']['rel']:.3f} p_int {p_int:.2f}; "
      f"days {[round(x, 3) for x in day_lift]}; cost {cost}")
