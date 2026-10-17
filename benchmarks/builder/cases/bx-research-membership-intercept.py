"""Delivery membership business case (Larchmont Grocers) built on an in-store
intercept survey.

Planted subtle problems (4):
P1 store-entrance intercepts over-sample frequent shoppers (chance of being
   interviewed ~ visits); intent rises with visits. Weight by 1/visits:
   definitely+probably falls from ~31% to ~21%.
P2 the business case's "41% interested (definitely/probably)" actually counts
   "might or might not" too; definitely+probably in the file is ~31%.
P3 the base is all 182,000 loyalty cardholders; only ~96,400 shopped in the
   last 12 months.
P4 the survey showed GBP 4.99/month; the business case prices at GBP 6.99.
   Demand at 6.99 was never measured (and break-even at 4.99 is ~53k members).
Decision: do not commit the fleet; run a paid pilot / pre-sale at the intended
price. Corrected member estimate ~5-6k vs break-even ~25.7k (at 6.99).
Naive: launch (37k members > 25.7k break-even).
Decoys: margin of error +/-3.9% at n=640 is right; unequal interviews per
store follow footfall quotas.
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-research-membership-intercept"
rng = random.Random(52031)

N_RESP = 640
CARDS, ACTIVE = 182_000, 96_400
FIXED = 1_200_000
VC = 3.10
P_CASE, P_SHOWN = 6.99, 4.99

# population of active shoppers by visit frequency (visits in last 4 weeks)
VIS = [1, 2, 4, 8, 12, 16]
POP = [0.30, 0.25, 0.20, 0.13, 0.08, 0.04]
P_DEF = [0.03, 0.04, 0.07, 0.12, 0.17, 0.22]
P_PROB = [0.10, 0.12, 0.15, 0.20, 0.24, 0.26]
P_MIGHT = [0.10, 0.10, 0.10, 0.10, 0.10, 0.10]
LEVELS = ["definitely would join", "probably would join", "might or might not", "probably would not", "definitely would not"]

STORES = {"Larchmont Central": 21000, "Quayside": 15500, "Elm Park": 12800, "Northgate": 11200,
          "Ashby Road": 9400, "Millbrook": 8300, "Fenwick": 6900, "Coleridge Sq": 4900}

# intercept sample: chance of being interviewed proportional to visits
w = [p * v for p, v in zip(POP, VIS)]
alloc = [round(N_RESP * x / sum(w)) for x in w]
alloc[3] += N_RESP - sum(alloc)

resp = []
for k, n in enumerate(alloc):
    nd, npb, nm = round(n * P_DEF[k]), round(n * P_PROB[k]), round(n * P_MIGHT[k])
    rest = n - nd - npb - nm
    npn = round(rest * 0.45)
    ans = [LEVELS[0]] * nd + [LEVELS[1]] * npb + [LEVELS[2]] * nm + [LEVELS[3]] * npn + [LEVELS[4]] * (rest - npn)
    rng.shuffle(ans)
    for a in ans:
        v = VIS[k] if VIS[k] <= 2 else VIS[k] + rng.choice([-1, 0, 0, 1])
        resp.append([v, a])
rng.shuffle(resp)

tot_ff = sum(STORES.values())
quota = {s: round(N_RESP * f / tot_ff) for s, f in STORES.items()}
quota["Larchmont Central"] += N_RESP - sum(quota.values())
store_list = [s for s, q in quota.items() for _ in range(q)]

AGES = ["18-34", "35-54", "55+"]
rows = []
for i, ((v, a), s) in enumerate(zip(resp, store_list)):
    day = f"2026-09-{rng.randint(7, 19):02d}"
    rows.append([f"LG{i + 1:04d}", s, day, v, rng.choices(AGES, [0.28, 0.40, 0.32])[0],
                 rng.choices([1, 2, 3, 4, 5], [0.24, 0.34, 0.17, 0.17, 0.08])[0], "4.99", a])
rows.sort(key=lambda r: (r[2], r[1]))
for i, r in enumerate(rows):
    r[0] = f"LG{i + 1:04d}"

# ---------- ground truth ----------
def share(levels, weighted):
    num = den = 0.0
    for r in rows:
        wt = 1 / r[3] if weighted else 1.0
        den += wt
        num += wt * (r[7] in levels)
    return num / den


top2_u = share(LEVELS[:2], False)
top3_u = share(LEVELS[:3], False)
def_u, prob_u = share(LEVELS[:1], False), share(LEVELS[1:2], False)
def_w, prob_w = share(LEVELS[:1], True), share(LEVELS[1:2], True)
top2_w = def_w + prob_w
mean_vis_sample = sum(r[3] for r in rows) / len(rows)
mean_vis_pop = len(rows) / sum(1 / r[3] for r in rows)
share_heavy = sum(r[3] >= 7 for r in rows) / len(rows)

case_members = CARDS * round(top3_u, 2) * 0.5
be_case = FIXED / ((P_CASE - VC) * 12)
be_shown = FIXED / ((P_SHOWN - VC) * 12)
p_cal = 0.4 * def_w + 0.2 * prob_w
truth_members = ACTIVE * p_cal
truth_hi = ACTIVE * top2_w * 0.5                   # generous: weighted top-two-box, case's 50% haircut, active base
only_base = ACTIVE * round(top3_u, 2) * 0.5
only_weight = CARDS * top2_w * 0.5
moe = 1.96 * math.sqrt(0.25 / N_RESP)

assert round(top3_u, 2) == 0.41, top3_u
assert 0.28 < top2_u < 0.34 and 0.19 < top2_w < 0.24, (top2_u, top2_w)
assert case_members > be_case * 1.3, (case_members, be_case)
assert truth_members < be_case / 3 and truth_hi < be_case, (truth_members, truth_hi, be_case)
assert only_base < be_case and only_weight < be_case
assert abs(moe - 0.039) < 0.001

files = {}
files["resources/intercept_survey.csv"] = to_csv(
    ["respondent_id", "store", "interview_date", "visits_last_4_weeks", "age_band", "household_size", "monthly_price_shown_gbp", "membership_intent"], rows)
files["resources/loyalty_card_base.csv"] = to_csv(
    ["card_status", "definition", "cardholders"],
    [["active", "at least one purchase in the last 12 months", ACTIVE], ["lapsed", "no purchase in the last 12 months", CARDS - ACTIVE]])
files["resources/fieldwork_note.md"] = f"""# Larchmont Plus survey: fieldwork note

- Method: face-to-face interviews at store entrances, 7-19 September 2026, 8 stores, 10:00-19:00.
- Interviews per store set in proportion to each store's average weekly footfall:

| Store | Weekly footfall | Interviews |
|---|---|---|
""" + "\n".join(f"| {s} | {f:,} | {quota[s]} |" for s, f in STORES.items()) + f"""

- Completed interviews: {N_RESP}. Margin of error for a proportion: +/-{100 * moe:.1f} points at 95% confidence.
- Concept card shown: "Larchmont Plus: unlimited next-day home delivery on orders over GBP 25, GBP 4.99 a month, cancel any time."
- Question: "If Larchmont Plus were available, how likely would you be to join?" (5-point scale)
"""
files["resources/business_case.md"] = f"""# Larchmont Plus: business case (draft for exec committee)

## Demand
- Survey: 41% of shoppers interested (definitely/probably would join).
- Customer base: {CARDS:,} loyalty cardholders.
- Conservative haircut: assume only half of interested shoppers join.
- Members: {CARDS:,} x 41% x 50% = **{case_members:,.0f}**

## Economics (annual)
- Price: GBP {P_CASE}/month.
- Delivery and picking cost per member: GBP {VC:.2f}/month.
- Fixed cost (12 vans on 3-year lease, drivers, routing software): GBP {FIXED:,}/year.
- Break-even members: {FIXED:,} / ((GBP {P_CASE} - GBP {VC:.2f}) x 12) = **{be_case:,.0f}**

## Recommendation
Members exceed break-even by {case_members / be_case - 1:.0%}. Sign the van lease and launch in January.
"""

prompt = """
We're deciding whether to launch Larchmont Plus, a paid home-delivery membership for our grocery stores. The draft business case for the exec committee is resources/business_case.md; it's based on the in-store survey we ran in September (resources/intercept_survey.csv, with the fieldwork note) and our loyalty card counts. The committee meets next week to sign off the van lease. Does the case hold up, and what should we recommend? Write it up in report.md with the member number you'd plan on.
"""

g_recall = f"""
The materials contain 4 planted problems. Answer key (computed from the files):

1. Intercept sample over-represents frequent shoppers. Interviews were at store entrances, so a shopper's chance of being interviewed rises with how often they visit. Respondents average {mean_vis_sample:.1f} visits in the last 4 weeks ({100 * share_heavy:.0f}% visited 7+ times); weighting each respondent by 1/visits gives a shopper-level average of about {mean_vis_pop:.1f}. Intent rises with visits, so weighting by 1/visits cuts definitely+probably from {100 * top2_u:.1f}% to about {100 * top2_w:.1f}%. Counts as found if report.md says the in-store sample is skewed toward frequent/heavy shoppers (citing visits_last_4_weeks or a weighted figure) and that this inflates interest.
2. The 41% includes "might or might not". The business case says 41% "definitely/probably", but in the file definitely+probably is {100 * top2_u:.1f}% ({100 * def_u:.1f}% definitely, {100 * prob_u:.1f}% probably); 41% ({100 * top3_u:.1f}%) is only reached by adding "might or might not". Counts as found if report.md states definitely+probably is about {100 * top2_u:.0f}% (28-34%) or says the 41% includes the "might" answers.
3. Wrong customer base. The case multiplies by {CARDS:,} loyalty cardholders, but loyalty_card_base.csv shows only {ACTIVE:,} are active (purchased in the last 12 months); the survey only reaches current shoppers. Counts as found if report.md replaces or challenges the {CARDS:,} base with {ACTIVE:,} active cardholders (or says lapsed cards should be excluded).
4. Price mismatch. Respondents were shown GBP {P_SHOWN}/month; the business case prices at GBP {P_CASE}. Interest at GBP {P_CASE} was never measured (and at GBP {P_SHOWN}, break-even would be about {be_shown:,.0f} members). Counts as found if report.md notes the survey price (4.99) differs from the business-case price (6.99).

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 problems, each with its evidence (a number, a column, or a quote from the files).
FAIL if fewer than 3 are identified with evidence.
"""

g_decision = f"""
The committee must decide whether to sign the van lease (GBP {FIXED:,}/year fixed) and launch.

Ground truth. Break-even at GBP {P_CASE} is {be_case:,.0f} members. Corrected demand: {ACTIVE:,} active shoppers x calibrated join probability. With frequency weighting, definitely = {100 * def_w:.1f}%, probably = {100 * prob_w:.1f}%; using typical intent calibration (0.4 x definitely + 0.2 x probably) about {truth_members:,.0f} members. Even a generous version (weighted definitely+probably {100 * top2_w:.1f}% x the case's own 50% haircut x active base) gives about {truth_hi:,.0f}, still below break-even. Fixing only the base ({only_base:,.0f}) or only the frequency weighting ({only_weight:,.0f}) already falls below break-even. And demand at GBP {P_CASE} was never tested.

Correct main recommendation: the case does not hold; do not sign the lease / launch as planned. Instead test real demand cheaply first (paid pilot in a few stores, pre-sale or paid waitlist at the intended price, or a short-term/flexible delivery arrangement) with a member threshold to proceed. A planned member figure well below break-even (anything under about {be_case * 0.75:,.0f}) is consistent with the ground truth.

Naive wrong recommendation: launch, because {case_members:,.0f} members exceed the {be_case:,.0f} break-even.

PASS if report.md's main recommendation is not to commit to the lease/launch now (no-go, or pilot/test first) AND its planned member number (if given) is below {be_case * 0.75:,.0f}.
FAIL if report.md recommends launching / signing the lease, or plans on a member number at or above break-even ({be_case:,.0f}), e.g. {case_members:,.0f}.
"""

g_decoys = f"""
Two things look questionable but are fine and must not be presented as problems:
- D1. The fieldwork note's margin of error, +/-{100 * moe:.1f} points at 95% for n = {N_RESP}, is computed correctly (1.96 x sqrt(0.25/{N_RESP})). The sample size is adequate for that precision. (Saying the margin of error does not cover bias from who was interviewed is correct and is NOT a false alarm.)
- D2. Interviews per store are unequal ({min(quota.values())} to {max(quota.values())}) because they were set in proportion to each store's weekly footfall. That is a sound quota design, not a sampling flaw.

PASS if report.md does not call the margin of error miscalculated, does not say n = {N_RESP} is too small to use, and does not present the unequal interviews per store as a flaw.
FAIL if it does any of those.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoys)])
print(f"{NAME}: top2 {top2_u:.3f} top3 {top3_u:.3f} weighted top2 {top2_w:.3f}; case {case_members:,.0f} vs BE {be_case:,.0f} (at 4.99 {be_shown:,.0f}); "
      f"truth {truth_members:,.0f} (generous {truth_hi:,.0f}); visits sample {mean_vis_sample:.1f} vs pop {mean_vis_pop:.1f}")
