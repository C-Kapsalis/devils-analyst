"""Brand lift readout for an autumn video campaign (Kestrel Bikes), agency asks
for a Q1 renewal.

Planted subtle problems (4):
  P1 Interactive testing: the same panel was asked aided familiarity with the
     named brand before the campaign; the pre-measure sensitises the exposed
     panel, so panel DiD (+14 pts) overstates the effect. The fresh wave-2
     top-up samples (never pre-measured) give a DiD of about +2.5 pts, not
     significant. (decision-changing)
  P2 Unaided question wording changed between waves (first brand that comes
     to mind -> all brands you can name): the "unaided nearly tripled" claim is
     an instrument change.
  P3 Control contamination: CTV (national buy) delivered impressions in the
     control region too.
  P4 Behaviour does not confirm: branded search in North vs South moved in
     parallel through the campaign (ratio-of-ratios ~1.0).
Decision: do not renew at EUR 420k on this evidence; re-measure with an
after-only / fresh-sample design (or a smaller, properly designed geo test).
Decoys: different baseline awareness levels between regions (DiD handles
levels); panel attrition of ~8% balanced across regions."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-brand-lift-panel"
rng = random.Random(55817)
BUDGET_RENEW = 420000
ADULTS_NORTH = 4_200_000

# (region, wave, sample_type): (n, aided p, unaided p, consider p)
PLAN = {
    ("North", 1, "panel"): (600, 0.310, 0.060, 0.120),
    ("South", 1, "panel"): (600, 0.380, 0.070, 0.150),
    ("North", 2, "panel"): (552, 0.520, 0.170, 0.205),
    ("South", 2, "panel"): (551, 0.450, 0.150, 0.180),
    ("North", 2, "fresh_topup"): (400, 0.350, 0.130, 0.140),
    ("South", 2, "fresh_topup"): (400, 0.395, 0.135, 0.160),
}
cells = {}
rows = []
for (reg, w, st), (n, a, u, c) in PLAN.items():
    aa = round(n * (a + rng.uniform(-0.004, 0.004)))
    uu = round(n * (u + rng.uniform(-0.003, 0.003)))
    cc = round(n * (c + rng.uniform(-0.003, 0.003)))
    cells[(reg, w, st)] = (n, aa, uu, cc)
    rows.append([reg, w, "2026-08-25" if w == 1 else "2026-10-27", st, n, aa, uu, cc])

def p(reg, w, st, i=1):
    n = cells[(reg, w, st)][0]
    return cells[(reg, w, st)][i] / n, n

nN1, NN1 = p("North", 1, "panel"); sS1, NS1 = p("South", 1, "panel")
nN2, NN2 = p("North", 2, "panel"); sS2, NS2 = p("South", 2, "panel")
fN, FN = p("North", 2, "fresh_topup"); fS, FS = p("South", 2, "fresh_topup")
did_panel = (nN2 - nN1) - (sS2 - sS1)
did_fresh = (fN - nN1) - (fS - sS1)
se_fresh = math.sqrt(sum(q * (1 - q) / m for q, m in [(fN, FN), (nN1, NN1), (fS, FS), (sS1, NS1)]))
z_fresh = did_fresh / se_fresh
p_fresh = math.erfc(abs(z_fresh) / math.sqrt(2))
se_panel = math.sqrt(sum(q * (1 - q) / m for q, m in [(nN2, NN2), (nN1, NN1), (sS2, NS2), (sS1, NS1)]))
interaction = did_panel - did_fresh
uN1, _ = p("North", 1, "panel", 2); uN2, _ = p("North", 2, "panel", 2)
uFN, _ = p("North", 2, "fresh_topup", 2); uFS, _ = p("South", 2, "fresh_topup", 2)
attr_N = 1 - NN2 / NN1; attr_S = 1 - NS2 / NS1

# media delivery
weeks = [dt.date(2026, 9, 7) + dt.timedelta(weeks=i) for i in range(6)]
media = []
for wk in weeks:
    yt = int(rng.uniform(1.9e6, 2.3e6)); ctv_n = int(rng.uniform(0.55e6, 0.7e6))
    ctv_s = int(ctv_n * rng.uniform(0.32, 0.40))
    media.append([wk.isoformat(), "North", "youtube", yt, round(yt * 0.0105, 2)])
    media.append([wk.isoformat(), "North", "ctv", ctv_n, round(ctv_n * 0.031, 2)])
    media.append([wk.isoformat(), "South", "youtube", 0, 0.0])
    media.append([wk.isoformat(), "South", "ctv", ctv_s, round(ctv_s * 0.031, 2)])
ctv_south = sum(r[3] for r in media if r[1] == "South")
imp_north = sum(r[3] for r in media if r[1] == "North")
ctv_north = sum(r[3] for r in media if r[1] == "North" and r[2] == "ctv")
spend_total = sum(r[4] for r in media)
contam_share = ctv_south / imp_north
cost_per_aware_agency = spend_total / (did_panel * ADULTS_NORTH)
cost_per_aware_fresh = spend_total / (did_fresh * ADULTS_NORTH)

# branded search (weekly, 20 weeks)
sw = [dt.date(2026, 7, 6) + dt.timedelta(weeks=i) for i in range(20)]
srch = []
for i, wk in enumerate(sw):
    season = 1.0 + 0.012 * i
    n_b = int(4200 * season * rng.uniform(0.95, 1.05)); s_b = int(5100 * season * rng.uniform(0.95, 1.05))
    n_c = int(61000 * season * rng.uniform(0.96, 1.04)); s_c = int(70000 * season * rng.uniform(0.96, 1.04))
    srch.append([wk.isoformat(), "North", n_b, n_c]); srch.append([wk.isoformat(), "South", s_b, s_c])
def mean_s(reg, a, b, col=2):
    v = [r[col] for r in srch if r[1] == reg and a <= dt.date.fromisoformat(r[0]) < b]
    return sum(v) / len(v)
PRE_A, PRE_B, POST_A, POST_B = dt.date(2026, 7, 6), dt.date(2026, 9, 7), dt.date(2026, 9, 7), dt.date(2026, 11, 23)
nb_ratio = mean_s("North", POST_A, POST_B) / mean_s("North", PRE_A, PRE_B)
sb_ratio = mean_s("South", POST_A, POST_B) / mean_s("South", PRE_A, PRE_B)
search_rr = nb_ratio / sb_ratio

# asserts
assert 0.12 < did_panel < 0.16, did_panel
assert 0.0 < did_fresh < 0.045 and p_fresh > 0.3, (did_fresh, p_fresh)
p_panel = math.erfc(abs(did_panel / se_panel) / math.sqrt(2))
assert p_panel < 0.002, p_panel
assert uN2 / uN1 > 2.5
assert abs(attr_N - attr_S) < 0.01 and 0.06 < attr_N < 0.10
assert ctv_south / ctv_north > 0.3 and contam_share > 0.05
assert abs(search_rr - 1) < 0.04, search_rr
assert abs(nN1 - sS1) > 0.05

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
pts = lambda x: f"{100 * x:+.1f} pts"
k = lambda x: f"{x:,.0f}"

readout = f"""# Kestrel Bikes — Autumn video campaign: brand lift results

Prepared by Brightline Media for Kestrel Bikes marketing. Fieldwork: Pollwise online panel.

## Design
- Test region: North (YouTube + connected TV, 7 Sep to 18 Oct 2026). Control region: South (no Kestrel campaign).
- Panel of adults 18-64 recruited in August in both regions. Wave 1 (pre) fielded 25 Aug-1 Sep; wave 2 (post) fielded 27 Oct-3 Nov to the same panellists.
- Wave 2 also includes a fresh top-up sample of 400 adults per region recruited from the same panel provider (to protect base sizes). Headline results use the matched panel, as agreed in the brief.
- Effect = change in North minus change in South (difference in differences).
- Questionnaire: see questionnaire.md. Results by cell: survey_results.csv. Delivery: media_delivery.csv.

## Results (matched panel)

| Metric | North pre | North post | South pre | South post | Lift (DiD) |
|---|---|---|---|---|---|
| Aided awareness | {pc(nN1)} | {pc(nN2)} | {pc(sS1)} | {pc(sS2)} | **{pts(did_panel)}** |
| Consideration | {pc(p('North',1,'panel',3)[0])} | {pc(p('North',2,'panel',3)[0])} | {pc(p('South',1,'panel',3)[0])} | {pc(p('South',2,'panel',3)[0])} | {pts((p('North',2,'panel',3)[0]-p('North',1,'panel',3)[0])-(p('South',2,'panel',3)[0]-p('South',1,'panel',3)[0]))} |

- Aided awareness lift of {pts(did_panel)} is significant (p = {p_panel:.4f}).
- **Unaided awareness in North nearly tripled**, from {pc(uN1)} to {pc(uN2)}.
- North started from a lower awareness base than South ({pc(nN1)} vs {pc(sS1)}); the DiD design accounts for this.
- Panel retention was {pc(1 - attr_N, 0)} in North and {pc(1 - attr_S, 0)} in South.

## Efficiency
Media spend EUR {k(spend_total)}. {pts(did_panel)} on {ADULTS_NORTH / 1e6:.1f}M adults in North = {k(did_panel * ADULTS_NORTH)} newly aware adults, EUR {cost_per_aware_agency:.2f} per newly aware adult (category norm EUR 1.50-2.50).

## Recommendation
Renew for Q1 2027 at EUR {k(BUDGET_RENEW)}, same regions and mix, and extend to South in Q2.
"""

questionnaire = """# Kestrel Bikes brand tracker — questionnaire (as fielded)

Screener (both waves): adults 18-64, resident in North or South region, cycled at least once in the past 12 months.

## Wave 1 (25 Aug - 1 Sep 2026)
Q1 (unaided). When you think of bicycle brands, which ONE brand comes to mind first? [open text, one answer]
Q2 (aided). How familiar are you with Kestrel Bikes? [Never heard of it / Heard of it only / Know a little / Know it well]  -> aided_aware = any answer except "Never heard of it"
Q3. Kestrel Bikes is known for: [show 6 statements, agree/disagree]
Q4 (consideration). Next time you buy a bike, which of these brands would you consider? [list of 8 brands incl. Kestrel Bikes, multi-select]

## Wave 2 (27 Oct - 3 Nov 2026)
Q1 (unaided). Which bicycle brands can you think of? Name as many as you like. [open text, multiple answers]
Q2 (aided). How familiar are you with Kestrel Bikes? [Never heard of it / Heard of it only / Know a little / Know it well]  -> aided_aware = any answer except "Never heard of it"
Q3. Kestrel Bikes is known for: [show 6 statements, agree/disagree]
Q4 (consideration). Next time you buy a bike, which of these brands would you consider? [list of 8 brands incl. Kestrel Bikes, multi-select]
Q5 (wave 2 only). In the past 8 weeks, do you recall seeing any video advertising for bicycle brands? Which brands?

Coding: unaided_aware = Kestrel mentioned in Q1. consider = Kestrel ticked in Q4.
"""

files = {
    "resources/lift_study_readout.md": readout,
    "resources/questionnaire.md": questionnaire,
    "resources/survey_results.csv": to_csv(["region", "wave", "field_start", "sample_type", "respondents", "aided_aware", "unaided_aware", "consider"], rows),
    "resources/media_delivery.csv": to_csv(["week_start", "region", "channel", "impressions", "spend_eur"], media),
    "resources/branded_search_weekly.csv": to_csv(["week_start", "region", "searches_kestrel", "searches_category_bikes"], srch),
}

prompt = f"""
Our agency sent the brand lift results for the autumn YouTube/CTV campaign (resources/lift_study_readout.md, with the questionnaire, survey cells, delivery and our branded search data in resources/). They want us to renew for Q1 at EUR {k(BUDGET_RENEW)}. What do you make of the results, and should we renew? Put your answer in report.md.
"""

g_recall = f"""
The lift study has 4 planted problems. Answer key (numbers computed from survey_results.csv and the other files):

1. Pre-measurement sensitisation (interactive testing). Wave 1 asked the SAME panellists "How familiar are you with Kestrel Bikes?" (brand named) before the campaign, and wave 2 re-asked them. Being asked about the brand primes exposed panellists to notice its ads, so the panel DiD ({pts(did_panel)}) is effect plus interaction. The wave-2 fresh top-up samples were never pre-measured: their DiD against the wave-1 baselines is {pts(did_fresh)} (North fresh {pc(fN)} vs North pre {pc(nN1)}; South fresh {pc(fS)} vs South pre {pc(sS1)}), z = {z_fresh:.2f}, p = {p_fresh:.2f}, not significant. Found if report.md says the repeated panel / brand-naming pre-wave inflates the effect AND/OR uses the fresh top-up samples to get a much smaller lift (anything between +1 and +4 pts, or "about a fifth of the reported lift", or "not significant").
2. Unaided question changed between waves. Wave 1 Q1 asked for the ONE brand that comes to mind first; wave 2 asked for all brands people can name. The "unaided nearly tripled ({pc(uN1)} to {pc(uN2)})" claim compares two different questions. Found if report.md notes the wording change and that the unaided change is not comparable.
3. Control region contaminated. media_delivery.csv shows CTV impressions in South (the control) every week: {k(ctv_south)} impressions, {pc(ctv_south / ctv_north, 0)} of North's CTV volume. Found if report.md notes the control region was exposed to the CTV (contamination of the control).
4. Behaviour does not confirm the attitude shift. branded_search_weekly.csv: Kestrel searches in North rose {pc(nb_ratio - 1)} from the pre-campaign weeks (6 Jul-6 Sep) to the campaign and post weeks (7 Sep-22 Nov), and in South rose {pc(sb_ratio - 1)}; ratio of ratios {search_rr:.2f}, i.e. no relative lift in North. Found if report.md says branded search did not rise more in North than in South (or shows no relative search lift).

List which were found in your reasoning, with the evidence.
PASS if at least 3 of the 4 are identified with evidence (a number, a question text, a file/column). A generic "survey results can be biased" does not count.
FAIL if 2 or fewer.
"""

g_decision = f"""
The agency recommends renewing at EUR {k(BUDGET_RENEW)} because aided awareness rose {pts(did_panel)} (EUR {cost_per_aware_agency:.2f} per newly aware adult).

Correct call: do NOT renew at EUR {k(BUDGET_RENEW)} on this evidence. The clean comparison (fresh, never pre-measured samples) shows {pts(did_fresh)} (p = {p_fresh:.2f}), which would put the cost at about EUR {cost_per_aware_fresh:.2f} per newly aware adult if real; branded search shows no relative lift. Acceptable recommendations: pause or decline the renewal until a clean re-measurement (after-only design with fresh samples or randomised/geo holdout, no brand-naming pre-wave, uncontaminated control); OR renew only a reduced, explicitly test-designed flight with that measurement plan. Both count as PASS as long as the full EUR {k(BUDGET_RENEW)} renewal is not endorsed on the current numbers.

Naive wrong answer: renew (or renew and expand) because the lift is {pts(did_panel)}, significant, and cheap per aware adult.

PASS if report.md's main recommendation is one of the acceptable ones above.
FAIL if report.md recommends renewing at the full budget (with or without caveats as a footnote), or expanding to South, based on the {pts(did_panel)} result; or gives no recommendation.
"""

g_decoy = f"""
Two features look suspicious but are fine:
- D1. North's starting awareness ({pc(nN1)}) is lower than South's ({pc(sS1)}). Difference in differences compares changes, so different starting levels are not a problem by themselves.
- D2. Panel attrition between waves: {pc(attr_N, 1)} in North and {pc(attr_S, 1)} in South (552 and 551 of 600). Attrition is small and nearly identical in both regions.

PASS if report.md does not present D1 or D2 as a flaw that invalidates or biases the result. Mentioning them as fine is a PASS. (Criticising the panel for being re-interviewed, i.e. pre-measurement sensitisation, is a different issue and is NOT a false alarm.)
FAIL if report.md says the regions are not comparable because their baseline awareness levels differ, or that panel attrition/dropout biases the result.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: panel DiD {did_panel:.3f} (z {did_panel / se_panel:.1f}) vs fresh DiD {did_fresh:.3f} (p {p_fresh:.2f}); unaided {uN1:.3f}->{uN2:.3f}; "
      f"contam {ctv_south / ctv_north:.2f}; search rr {search_rr:.3f}; cost/aware {cost_per_aware_agency:.2f} vs {cost_per_aware_fresh:.2f}")
