"""Regional OOH + radio pilot read as a before/after (Brightwell Pet Supply, Q3 2026).

Planted subtle problems (5):
P1 (decision) Regression to the mean: the 5 pilot regions were picked for the
   worst Q2-vs-Q1 growth; the next 5 worst, untreated, rebound almost as much.
P2 Benchmark contaminated: "company total" includes the pilot regions.
P3 Definition change: from 17 Aug three pilot regions' POS counts click &
   collect in store sales (click_collect_included column).
P4 ROI on revenue, not contribution: even the readout's own lift loses money
   at the 34% contribution margin.
P5 Awareness survey: same panel re-interviewed, pre-wave named the brand
   (pre-test sensitisation), no control regions surveyed.
Decoys (2): stores_total rises in one pilot region but lfl_sales uses the
   constant like-for-like base; "Pet Week" national promo spike hits every
   region equally."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-test-geo-pilot"
SEED = 31
rng = random.Random(SEED)

REGIONS = ["Aldmoor", "Bexwell", "Carrow Vale", "Dunmere", "Eastholt", "Fernby", "Glenhaven", "Harrowgate Downs",
           "Ivelford", "Kestwick", "Lowmarsh", "Mardale", "Northcote", "Oakhurst", "Pellridge", "Quarry Bay",
           "Redfern", "Stonebridge"]
TRUE_EFFECT = 0.015
MARGIN = 0.34
COST_PER_REGION = 55000
START = dt.date(2026, 1, 5)
WEEKS = 39
PET_WEEK = dt.date(2026, 8, 31)
CC_START = dt.date(2026, 8, 17)
season = [1 + 0.06 * math.sin(2 * math.pi * (w - 8) / 52) for w in range(WEEKS)]

level = {r: rng.uniform(70000, 160000) for r in REGIONS}
shock = {(r, q): rng.gauss(0, 0.07) for r in REGIONS for q in range(3)}


def q_of(w):
    return w // 13


# selection on Q2 vs Q1 expected growth
q_mean = {}
for r in REGIONS:
    for q in range(3):
        q_mean[(r, q)] = sum(level[r] * season[w] * (1 + shock[(r, q)]) for w in range(13 * q, 13 * q + 13))
growth_q2 = {r: q_mean[(r, 1)] / q_mean[(r, 0)] - 1 for r in REGIONS}
ranked = sorted(REGIONS, key=lambda r: growth_q2[r])
# shocks are known before data, but selection in the readout uses observed data; recompute after generating rows
rows = []
data = {}
for r in REGIONS:
    for w in range(WEEKS):
        day = START + dt.timedelta(days=7 * w)
        v = level[r] * season[w] * (1 + shock[(r, q_of(w))]) * rng.gauss(1, 0.025)
        if day == PET_WEEK:
            v *= 1.24
        data[(r, w)] = v

# observed selection: 5 worst Q2 vs Q1
def qsum(r, q, key="store"):
    return sum(base[(r, w)][key] for w in range(13 * q, 13 * q + 13))

base = {(r, w): {"store": data[(r, w)], "cc": 0.0} for r in REGIONS for w in range(WEEKS)}
obs_g2 = {r: qsum(r, 1) / qsum(r, 0) - 1 for r in REGIONS}
ranked = sorted(REGIONS, key=lambda r: obs_g2[r])
PILOT = ranked[:5]
NEXT5 = ranked[5:10]
CC_REGIONS = PILOT[:3]
NEW_STORE = PILOT[3]

# treatment effect and click & collect inclusion
for r in PILOT:
    for w in range(26, WEEKS):
        base[(r, w)]["store"] *= 1 + TRUE_EFFECT
for r in CC_REGIONS:
    for w in range(WEEKS):
        if START + dt.timedelta(days=7 * w) >= CC_START:
            base[(r, w)]["cc"] = base[(r, w)]["store"] * rng.uniform(0.075, 0.09)

for r in REGIONS:
    for w in range(WEEKS):
        day = START + dt.timedelta(days=7 * w)
        b = base[(r, w)]
        lfl_stores = 6 + (REGIONS.index(r) % 5)
        total_stores = lfl_stores + (1 if (r == NEW_STORE and day >= dt.date(2026, 7, 20)) else 0)
        rows.append([day.isoformat(), r, total_stores, lfl_stores, round(b["store"] + b["cc"], 2), round(b["cc"], 2)])
rows.sort(key=lambda x: (x[0], x[1]))

# ---------- ground truth ----------
def reported(r, q):
    return sum(round(base[(r, w)]["store"] + base[(r, w)]["cc"], 2) for w in range(13 * q, 13 * q + 13))

def clean(r, q):
    return sum(round(base[(r, w)]["store"] + base[(r, w)]["cc"], 2) - round(base[(r, w)]["cc"], 2) for w in range(13 * q, 13 * q + 13))

pil_q2 = sum(reported(r, 1) for r in PILOT); pil_q3 = sum(reported(r, 2) for r in PILOT)
co_q2 = sum(reported(r, 1) for r in REGIONS); co_q3 = sum(reported(r, 2) for r in REGIONS)
naive_pil_g = pil_q3 / pil_q2 - 1
naive_co_g = co_q3 / co_q2 - 1
naive_lift = naive_pil_g - naive_co_g                     # readout: points difference
naive_inc_rev = naive_lift * pil_q2
naive_rev_roi = naive_inc_rev / (COST_PER_REGION * 5)
naive_contrib_roi = naive_inc_rev * MARGIN / (COST_PER_REGION * 5)

pil_clean_g = sum(clean(r, 2) for r in PILOT) / sum(clean(r, 1) for r in PILOT) - 1
nonpilot = [r for r in REGIONS if r not in PILOT]
rest_g = sum(reported(r, 2) for r in nonpilot) / sum(reported(r, 1) for r in nonpilot) - 1
next5_g = sum(reported(r, 2) for r in NEXT5) / sum(reported(r, 1) for r in NEXT5) - 1
top8 = ranked[10:]
top8_g = sum(reported(r, 2) for r in top8) / sum(reported(r, 1) for r in top8) - 1
cc_q3 = sum(round(base[(r, w)]["cc"], 2) for r in PILOT for w in range(26, 39))
did_next5 = (1 + pil_clean_g) / (1 + next5_g) - 1
inc_rev_true = did_next5 * sum(clean(r, 1) for r in PILOT)
contrib_true = inc_rev_true * MARGIN - COST_PER_REGION * 5
be_lift = COST_PER_REGION * 5 / MARGIN / sum(clean(r, 1) for r in PILOT)
pil_q2_g = sum(qsum(r, 1) for r in PILOT) / sum(qsum(r, 0) for r in PILOT) - 1
next5_q2_g = sum(qsum(r, 1) for r in NEXT5) / sum(qsum(r, 0) for r in NEXT5) - 1
annual_rollout = COST_PER_REGION * len(REGIONS) * 4

# Pet week ratio check
pw = (PET_WEEK - START).days // 7
pw_ratio = {g: sum(reported_w for reported_w in [base[(r, pw)]["store"] for r in grp]) / sum((base[(r, pw - 1)]["store"] + base[(r, pw + 1)]["store"]) / 2 for r in grp)
            for g, grp in (("pilot", PILOT), ("rest", nonpilot))}

assert naive_lift > 0.08, naive_lift
assert naive_rev_roi > 1.5 and naive_contrib_roi < 1.0, (naive_rev_roi, naive_contrib_roi)
assert next5_g > 0.05, next5_g
assert abs(did_next5) < 0.04 and did_next5 < be_lift / 2, (did_next5, be_lift)
assert contrib_true < 0
assert abs(pw_ratio["pilot"] - pw_ratio["rest"]) < 0.06

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"EUR {x:,.0f}"

readout = f"""# Local media pilot: results and rollout proposal

Brightwell Pet Supply, field marketing. Draft for the commercial board, October 2026.

## What we did

From 6 July to 4 October 2026 (Q3) we ran outdoor posters near stores plus local radio in five regions: {", ".join(PILOT)}. We chose them because they had the weakest growth of all 18 regions in Q2 (Q2 vs Q1 like-for-like sales), so they had the most to gain. Cost: {eur(COST_PER_REGION)} per region for the quarter, {eur(COST_PER_REGION * 5)} in total.

## Sales

| | Q2 like-for-like sales | Q3 like-for-like sales | Growth |
|---|---|---|---|
| Pilot regions | {eur(pil_q2)} | {eur(pil_q3)} | {pc(naive_pil_g)} |
| Company total | {eur(co_q2)} | {eur(co_q3)} | {pc(naive_co_g)} |

The pilot regions grew **{100 * naive_lift:.1f} points faster** than the company. On the pilot regions' Q2 base that is about **{eur(naive_inc_rev)} of extra sales**, a return of **{naive_rev_roi:.1f}x** on the {eur(COST_PER_REGION * 5)} spend.

The national Pet Week promotion (week of 31 August) lifted sales everywhere that week; it is in both rows above.

## Brand awareness

Aided awareness in the pilot regions rose from 31% to 44% (survey_waves.csv).

## Proposal

Roll the local media programme out to all 18 regions from Q1 2027: {eur(annual_rollout)} a year.
"""

survey_rows = [
    ["1", "2026-06-15 to 2026-06-26", "pilot regions", "online panel, recruited June 2026", "Have you heard of Brightwell Pet Supply?", 640, 198],
    ["2", "2026-09-21 to 2026-10-02", "pilot regions", "same panel members re-contacted", "Which pet supply shops have you heard of? (list shown, includes Brightwell Pet Supply)", 588, 259],
]

files = {
    "resources/local_media_pilot_readout.md": readout,
    "resources/weekly_region_sales.csv": to_csv(
        ["week_start", "region", "stores_total", "stores_lfl", "lfl_sales", "click_collect_included"], rows),
    "resources/survey_waves.csv": to_csv(
        ["wave", "fieldwork", "regions", "sample_source", "question", "respondents", "aware"], survey_rows),
    "resources/finance_assumptions.md": (
        "# Finance assumptions 2026\n\n"
        f"- Contribution margin on like-for-like store sales: {int(MARGIN * 100)}% (after product cost, store variable costs and payment fees).\n"
        "- lfl_sales: sales of stores open in both years (stores_lfl); new stores are excluded until they have traded 12 months.\n"
        "- Media costs are booked in the quarter they run.\n"
    ),
}

prompt = """
Field marketing ran a local outdoor + radio pilot last quarter and wants to roll it out nationally next year. Their write-up is resources/local_media_pilot_readout.md, with the weekly sales by region, the awareness survey and finance's assumptions also in resources/. I sit on the commercial board that signs this off. Did the pilot work, and should we fund the national rollout? Write it up in report.md.
"""

g_recall = f"""
The pilot write-up and its data contain 5 planted problems. Ground truth (computed from the files):

1. Regression to the mean. The pilot regions were chosen for the weakest Q2-vs-Q1 growth (pilot Q2 growth {pc(pil_q2_g)}). The next five weakest regions ({", ".join(NEXT5)}), which got no media, also bounced back: Q3 vs Q2 {pc(next5_g)}, against {pc(top8_g)} for the remaining eight regions. Counts as found if report.md says regions selected for a bad quarter rebound on their own and compares with similar untreated regions (or otherwise names regression to the mean / selection on a bad quarter).
2. Benchmark includes the pilot. "Company total" ({pc(naive_co_g)}) contains the five pilot regions; non-pilot regions grew {pc(rest_g)}. Counts as found if report.md says the comparison group includes the treated regions.
3. Click & collect added mid-pilot. From week of 17 August, {", ".join(CC_REGIONS)} include click & collect in lfl_sales (column click_collect_included, {eur(cc_q3)} in Q3). Without it, pilot growth is {pc(pil_clean_g)} instead of {pc(naive_pil_g)}. Counts as found if report.md notices the click_collect_included amounts (or a definition change in those regions) and removes or flags them.
4. Return on revenue, not profit. The readout's {naive_rev_roi:.1f}x is revenue / cost. At the 34% contribution margin even its own {eur(naive_inc_rev)} of extra sales is worth {eur(naive_inc_rev * MARGIN)}, a {naive_contrib_roi:.2f}x return: it does not cover the {eur(COST_PER_REGION * 5)} cost. Counts as found if report.md converts to contribution/margin and says the pilot does not pay back (any contribution ROI below 1 or a loss figure).
5. Awareness survey design. The same panel was re-interviewed, the June wave asked directly about Brightwell Pet Supply (sensitising respondents), the two waves use different questions, and no control regions were surveyed. Counts as found if report.md flags at least one of: same panel primed by a brand-naming pre-wave, question wording changed between waves, or no control group for the survey.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 5, each with its substance (a number, column, region names or quoted survey detail). FAIL otherwise.
"""

g_decision = f"""
Correct main recommendation: do NOT fund the national rollout ({eur(annual_rollout)} a year) on this evidence. Compared with the five similarly weak untreated regions and with click & collect removed, the pilot effect is about {pc(did_next5)} (pilot clean growth {pc(pil_clean_g)} vs {pc(next5_g)}), worth roughly {eur(inc_rev_true)} of sales and {eur(contrib_true)} of contribution after the {eur(COST_PER_REGION * 5)} cost; break-even needs about {pc(be_lift)} extra sales. Even the readout's own lift loses money at margin ({naive_contrib_roi:.2f}x). Acceptable variants: rerun as a proper test with randomly assigned (or matched) regions and a holdout before any rollout; stop or pause the programme. A small, controlled re-test counts as PASS.

Naive wrong answer: "The pilot regions grew {100 * naive_lift:.1f} points faster than the company, {naive_rev_roi:.1f}x return: roll out to all 18 regions."

PASS if report.md's main recommendation is not to approve the national rollout now (decline, or re-test with a proper control first) and the reasoning includes at least one of: the regression-to-the-mean/untreated-comparison point, the contribution-margin point, or the click & collect inflation.
FAIL if it recommends approving the national rollout (even phased across all regions, or "with tracking") or says the pilot clearly worked.
"""

g_decoy = f"""
Two things look odd but are correct and must not be presented as problems:
- D1. In {NEW_STORE}, stores_total goes up by one from the week of 20 July, but stores_lfl stays constant and lfl_sales covers like-for-like stores only (finance_assumptions.md: new stores excluded for 12 months). The new store does not inflate the pilot's sales.
- D2. The Pet Week national promotion (week of 31 August) spikes sales in every region by about the same share (pilot regions x{pw_ratio['pilot']:.2f}, other regions x{pw_ratio['rest']:.2f} vs the surrounding weeks), so it does not bias the pilot-vs-other comparison.

PASS if report.md does not claim the new store inflates the pilot's sales or that the Pet Week spike biases the pilot result. Neutral mentions or saying they are fine PASS.
FAIL if it says lfl_sales is inflated by the new store in {NEW_STORE}, or that Pet Week must be removed because it distorts the pilot vs comparison result.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: pilot {PILOT}; naive lift {naive_lift:.3f} revROI {naive_rev_roi:.2f} contribROI {naive_contrib_roi:.2f}; next5 {next5_g:.3f}; "
      f"clean pilot {pil_clean_g:.3f}; DiD {did_next5:.3f}; BE {be_lift:.3f}; contrib {contrib_true:,.0f}")
