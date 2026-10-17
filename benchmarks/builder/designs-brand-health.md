# brand-health: eval case designs

Format follows benchmarks/cases/*/ (prompt.md asking for report.md,
fixture data in resources/, LLM graders with PASS/FAIL, plus a
`skill-fired` tool_used grader matching `brand-health`). All numbers below
follow by construction from the generation recipe; regenerate and recompute
in benchmarks/builder before freezing.

---

## 1. promo-baseline-erosion

**Prompt.** "resources/ has our weekly sales for Hearth & Field Pantry
(weekly_sales.csv: week_start, units, gross_revenue, discount_amount,
promo_flag) for 2024 and 2025. Promo weeks now sell almost twice a normal
week, so our promotions keep getting better. Should we schedule more promo
weeks in 2026? Our unit cost is $18. Write report.md."

**Data.** 104 weekly rows, 8 quarters. Regular price $40, promo price $30
(25% off). Per quarter q = 1..8: baseline units/week `1000 - 220 (q-1)/7`
(1,000 -> 780); promo weeks per quarter 2,2,3,3,4,4,5,5; each promo week
sells `baseline x lift`, lift `1.30 + 0.60 (q-1)/7` (1.30 -> 1.90); the
week after each promo week sells 0.9 x baseline; other weeks sell baseline.
Add +-3% noise.

**Ground truth.** Baseline (non-promo, non-post weeks) -22% (1,000 -> 780).
Lift 1.30x -> 1.90x. Units per quarter flat (about 13,400 -> 13,260).
Revenue per quarter 510,000 -> 456,300 (-10.5%). Contribution after $18
unit cost 268,800 -> 217,620 (-19%). Promo revenue share 15.3% -> 48.7%
(above the 40% line).

**Naive answers.** (a) "Lift rose from 1.3x to 1.9x, promotions are more
effective, add promo weeks." (b) "Units are flat, promotions are holding
volume."

**Graders.**
- (weight 3) PASS if report.md shows the non-promo baseline falling across
  quarters (about -20% or more) and explains that the rising lift is at
  least partly an artefact of the falling baseline (customers waiting for
  deals). FAIL if it reads the rising lift as promotions becoming more
  effective without addressing baseline.
- (weight 2) PASS if it recommends not adding promo weeks (hold or cut
  frequency/depth, protect full-price sales) and cites falling revenue or
  contribution or the promo share rising above about 40%. FAIL if it
  recommends more promo weeks.
- (weight 1) PASS if it warns that cutting promotions may dip sales for a
  quarter or two before baseline recovers, or proposes a test (fewer promos
  in some regions/periods). FAIL otherwise.

---

## 2. brand-search-share

**Prompt.** "We started a YouTube brand campaign for Nordvik in October
2025. resources/ has monthly Google search volumes from Keyword Planner
for Oct 2024 to Sep 2026 (search_volumes.csv: month, keyword, keyword_type
[brand_own, brand_competitor, category], competitor_name, avg_monthly_searches)
and our monthly YouTube spend. Our brand searches are up about 30%. Did the
campaign build the brand, and should we double its budget? Write report.md."

**Data.** 24 months x (3 own brand terms, 3 terms per each of 3 competitors,
4 category terms), with shared seasonality (Nov-Dec peak). 12-month totals,
prior year (Oct 24-Sep 25) -> campaign year (Oct 25-Sep 26): own 120,000 ->
156,000 (+30%); competitor A 200,000 -> 310,000 (+55%); B 150,000 ->
222,000 (+48%); C 75,000 -> 90,000 (+20%); category terms 1,000,000 ->
1,400,000 (+40%). YouTube spend 0 in year 1, 15,000/month in year 2.

**Ground truth.** Share of search 22.0% -> 20.1% (own / all brand terms).
Brand vs category index 0.120 -> 0.111 (-7%). Own growth is below category
growth and below two of three competitors: the 30% is category tide; the
data do not show that the campaign built the brand share. Verdict:
inconclusive at best; no case for doubling; propose a geo holdout or
on/off test read on branded search share and baseline sales.

**Naive answer.** "Brand searches +30% since the campaign started, the
campaign worked, scale it."

**Graders.**
- (weight 3) PASS if report.md compares own brand search with competitors
  and/or category demand and reports that Nordvik's share of brand search
  (or brand/category ratio) fell or did not rise. FAIL if it credits the
  campaign with the 30% growth without a competitor or category benchmark.
- (weight 2) PASS if it does not recommend doubling the budget on this
  evidence and proposes a controlled test (geo split, holdout, on/off).
  FAIL if it recommends doubling based on the raw growth.
- (weight 1) PASS if it compares the same months year on year (or
  otherwise handles the Nov-Dec seasonality). FAIL if it compares, e.g.,
  Sep 2025 with Dec 2025.

---

## 3. flat-tracker-score

**Prompt.** "Our annual brand tracker is back (resources/tracker.csv: wave,
respondent_id, segment, brand_score 0-10, would_recommend 0-10) plus
resources/segments.csv with the average 3-year CLV per segment from our
CRM and resources/repeat_rates.csv. The brand score was 7.3 last year and
7.3 this year. The board wants to know if the brand is healthy and whether
we can keep next year's brand budget flat. Write report.md."

**Data.** Two waves, n = 1,200 each. Segments: core (CLV 900), occasional
(CLV 250), new_promo (CLV 60). Mix wave 1: 50/30/20%; wave 2: 30/30/40%.
Mean scores wave 1 -> 2: core 8.2 -> 7.0; occasional 7.0 -> 7.0; new_promo
5.5 -> 7.7; sd about 1.8. Repeat rates (CRM): core 62% -> 51%, occasional
34% -> 33%, new_promo 12% -> 14%.

**Ground truth.** Total 7.30 -> 7.28 (flat). Core segment -1.2 points
(significant at n 600 -> 360). At a fixed wave-1 mix the score falls 7.30
-> 7.14; CLV-weighted (weights share x CLV from wave 1) 7.97 -> 7.02
(-0.95). The flat total is a mix shift toward low-value promo-acquired
respondents; the customers who carry the value rate the brand lower and
repeat less. Brand is not healthy among core customers.

**Naive answer.** "Score stable at 7.3, the brand is healthy, keep the
budget flat."

**Graders.**
- (weight 3) PASS if report.md splits the score by segment and reports the
  core segment's decline (about 8.2 -> 7.0) and that the flat total comes
  from a change in respondent mix or the growth of a low-value segment.
  FAIL if it concludes the brand is healthy/stable from the total.
- (weight 2) PASS if it weights by value (CLV or revenue) or otherwise
  states the decline matters more because the core segment carries most of
  the value, and uses the repeat-rate drop as behavioural confirmation.
  FAIL if CLV and repeat data are ignored.
- (weight 1) PASS if the recommendation targets the core segment (cause
  research, retention, brand support) rather than simply "keep flat"; and
  leaves the budget decision to the board with the trade-off stated. FAIL
  otherwise.

---

## 4. mentions-spike-complaints

**Prompt.** "We ran our summer influencer push for Brightwell in Q3 2026.
resources/mentions.csv is our social listening export (date, brand,
mention_id, sentiment, topic_tag, tagged_account yes/no) for Q2 and Q3 for
us and two competitors. Mentions went up 60% and our share of voice is the
highest it has ever been. Write a report for the CMO on how the campaign
did for the brand. Save report.md."

**Data.** Brightwell Q2 4,000 mentions (positive 1,600, negative 600,
neutral 1,800; delivery-tagged 300 of which 200 negative). Q3 6,400
(positive 1,900, negative 2,300, neutral 2,200; delivery-tagged 2,500 of
which 1,800 negative, concentrated after a carrier change in mid-July).
Competitor 1: 5,000 -> 5,400; competitor 2: 3,000 -> 3,300, sentiment
stable. Influencer-tagged posts (topic_tag "campaign") 0 -> 600, mostly
positive.

**Ground truth.** Share of voice 33.3% -> 42.4%, but net sentiment +25.0%
-> -6.3%. Non-delivery mentions 3,700 -> 3,900 (+5%); delivery mentions
300 -> 2,500 (+733%) explain about 92% of the increase. Positive mentions
+300. The campaign's measurable effect is small and positive; the spike is
a delivery problem that needs routing to operations.

**Naive answer.** "Mentions +60%, SOV 42%, the campaign was a success."

**Graders.**
- (weight 3) PASS if report.md shows that most of the mention growth is
  negative and/or delivery-related, with net sentiment falling. FAIL if it
  presents the 60% growth or the SOV gain as campaign success without this.
- (weight 2) PASS if it separates the campaign's own contribution (tagged
  campaign posts or non-delivery mentions, about +5% / +300 positive) from
  the complaint spike. FAIL otherwise.
- (weight 1) PASS if it recommends acting on the delivery issue
  (operations, service, response plan) as a brand priority. FAIL otherwise.

---

## 5. extension-permission-average

**Prompt.** "We're deciding whether to launch Calder Energy, a canned
coffee energy drink for convenience stores, under our Calder specialty
coffee brand. resources/extension_survey.csv has the concept test
(respondent_id, customer_status [core, lapsed, non_customer], age_band,
energy_drink_buyer yes/no, purchase_intent 0-10, brand_fit 0-10,
think_less_of_calder yes/no). Average purchase intent is 6.3, above our
6.0 go threshold. Can we launch it as Calder Energy? Write report.md."

**Data.** n = 1,000: core 400 (intent mean 4.2, fit 3.9, think-less 22%),
lapsed 150 (5.8, 5.5, 9%), non-customers 450 (8.4, 6.8, 2%), of whom 80%
are energy-drink buyers aged 18 to 29, unlike the core (mostly 35+).

**Ground truth.** Overall intent 6.33 = (400x4.2 + 150x5.8 + 450x8.4) /
1000. Core-customer intent 4.2 and fit 3.9, below the 6/10 permission
line; 22% of core customers would think less of Calder. Demand comes from
a different customer group buying a similar-category product: same brand
name is the failing cell of the customer-similarity test. Recommend a
sub-brand or separate brand (possibly endorsed), not "Calder Energy";
verify with a test market measuring core repeat and brand scores.

**Naive answer.** "6.3 > 6.0, launch as Calder Energy."

**Graders.**
- (weight 3) PASS if report.md splits intent by customer status and
  reports core customers' intent (about 4.2) and/or fit below the go line,
  noting the average is carried by non-customers. FAIL if it approves the
  launch under the Calder name based on the 6.3 average.
- (weight 2) PASS if it recommends a sub-brand, endorsed brand or separate
  brand (or no launch) and names the risk to the core brand (22% think
  less of Calder, spillover). FAIL otherwise.
- (weight 1) PASS if it proposes a verification step (test market, staged
  launch) with a metric on core customers. FAIL otherwise.
