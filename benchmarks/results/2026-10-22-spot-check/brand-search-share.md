# brand-search-share

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/brand-health/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/brand-search-share/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> We started a YouTube brand campaign for Nordvik (outdoor jackets) in October 2025. resources/ has monthly Google search volumes from Keyword Planner for October 2024 to September 2026 (search_volumes.csv: month, keyword, keyword_type, competitor_name, avg_monthly_searches) and our monthly YouTube spend (youtube_spend.csv).
> 
> Our brand searches are up about 30%. Did the campaign build the brand, and should we double its budget? Write report.md with your numbers and recommendation.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `budget-decision` | PASS | PASS | both: do not double; geo holdout |
| `seasonality` | PASS | PASS | both compare 12-month windows |
| `share-of-search` | PASS | PASS | both: share 22.2% to 19.9%, category +40.1% |

## Arm A answer (with skill)

````markdown
# Nordvik YouTube brand campaign: did it build the brand, and should we double it?

Verdict: brand weaker relative to its market. The campaign is not shown to have built the brand, and doubling the budget is not supported by these data.

Deciding number: own brand share of search fell from 22.2% to 19.9% (-2.3 points). Own brand volume rose 28.8%, but the category rose 40.1% and competitors rose 48.3%.

What the headline says and why it misleads: "brand searches up about 30%" is right (+28.8%), but the category grew faster (+40.1%). Own brand grew more than Vallo (+22.0%) only, and less than Fjellmark (+58.8%) and Arcton (+47.3%).

Benchmark: own brand vs category (4 generic terms) and 3 named competitors (Fjellmark, Arcton, Vallo).   Segments: none in the data; the keyword split is the only cut available.

Action: do not double the budget yet. Hold spend and run a geo holdout for at least two quarters.   Trade-off: brand share (equity) vs short-term spend. Doubling adds about 179.6k a year on an effect not yet shown.

How to verify: a regional holdout (YouTube brand spend paused or reduced in matched regions) for two quarters, reading own brand-term volume, share of search and baseline sales against the holdout, with the pass threshold set before the test starts. Your decision: whether to hold, test, or double now, knowing the test costs two quarters of answer time.

## Assumptions to confirm
- Decision: whether to double YouTube brand spend.
- Own brand terms: nordvik, nordvik jacket, nordvik outlet.
- Competitors: Fjellmark (3 terms), Arcton (3 terms), Vallo (3 terms), held fixed for both periods.
- Category: rain jacket, waterproof jacket, hiking jacket, insulated jacket.
- Launch: Oct 2025. Pre period: Oct 2024 to Sep 2025 (12 months). Post period: Oct 2025 to Sep 2026 (12 months). Comparing 12-month windows covers seasonality.

## Computed checks (redo by summing the rows in search_volumes.csv)

| # | Check | Pre (Oct 2024 to Sep 2025) | Post (Oct 2025 to Sep 2026) | Change |
|---|---|---|---|---|
| 1 | Own brand volume | 120,680 | 155,400 | +28.8% |
| 2 | Competitor brand volume (9 terms) | 422,390 | 626,210 | +48.3% |
| 3 | Category volume (4 terms) | 995,920 | 1,394,850 | +40.1% |
| 4 | Share of search = own / (own + competitor) | 22.2% | 19.9% | -2.3 pts (-10.5% relative) |
| 5 | Brand vs category index = own / category | 12.1% | 11.1% | -1.0 pt (-8.1% relative) |

Per competitor, pre to post: Fjellmark 198,050 to 314,530 (+58.8%); Arcton 150,380 to 221,460 (+47.3%); Vallo 73,960 to 90,220 (+22.0%).

Monthly brand-to-category index: the pre-campaign range was 0.1158 (Mar 2025) to 0.1261 (Apr 2025). The launch month (Oct 2025) was 0.1172, inside that range. All 11 months from Nov 2025 to Sep 2026 were below 0.1158, with the low at 0.1054 (Jun 2026). The index fell after launch.

Year-on-year own brand growth was positive in every month, from +22.2% (Jun 2026) to +32.0% (Oct 2025). The steady rate looks like a trend, not a launch step. The file starts in Oct 2024, so there is no earlier year to test whether the trend began before the campaign.

YouTube spend and reach (Oct 2025 to Sep 2026):
- Spend 179,607.32 in total (currency as in the file), average 14,967.28 a month, range 14,622.49 (Mar 2026) to 15,168.77 (Jul 2026), within about 2% of each other.
- Impressions 19,707,328; views 4,833,456 (view rate 24.5%).
- Cost per 1,000 impressions 9.11; cost per view 0.037.

## Adversary pass
1. Category tide: category demand grew 40.1%, faster than the brand. The brand's 28.8% is below market, so no credit can go to the campaign from the headline alone.
2. Competitor response: competitor terms grew 48.3%. The file has no competitor spend, so it cannot show whether they reacted to our campaign or to the market.
3. Lagged effect: brand advertising can work over months (long-view method). That is a hypothesis, not a finding. The share number fell in the first year, which weakens a large early effect.
4. Spend variation: spend barely moved (about 2% range). The data cannot show how brand search responds to spend, so doubling would be an extrapolation outside the observed range.

## What the data cannot show
- No sales, margin or baseline-sales data, so no profit verdict and no check on whether search growth turned into sales.
- No geography, so no regional holdout can be read from these files.
- No history before Oct 2024, so no pre-trend test.
- No competitor spend or share-of-voice data.
- Keyword Planner volumes are estimates.

## Recommendation
1. Do not double the budget on this evidence.
2. Hold spend at the current level during the test. Cutting is also a decision, not a neutral default.
3. Run a regional holdout for at least two quarters. Pause or cut YouTube brand spend in matched regions and compare own brand-term volume, share of search and baseline sales with the regions that keep spending. Pull regional brand-term volumes from Google Ads or Search Console, since this file is not split by geography.
4. Set the pass threshold before the test starts. Pick the lift in share of search that would justify the spend and check it against the noise in the regional data.
5. Ask the team for sales data by region and a competitor spend estimate, so that the next read covers profit and the competitor response.

## Score
- Clarity: one verdict, with numbers that can be redone from the CSV.
- Relevance: answers the double-or-not decision in the stated frame.
- Depth: benchmark, monthly index, competitor split and spend are covered. Segments are not available.
- Insight: the headline 30% is real, but the brand lagged the category.
````

## Arm B answer (without skill)

````markdown
# Nordvik YouTube brand campaign: did it build the brand?

## Answer

No, not on this evidence. Brand searches rose about 29% over the campaign year, but the category and the named competitors rose faster over the same months. Nordvik lost share of search. Do not double the budget yet.

## Numbers

Brand = the three `brand_own` keywords (nordvik, nordvik jacket, nordvik outlet). Campaign started October 2025.

| Measure | Pre-campaign (Oct 2024 to Sep 2025) | Campaign year (Oct 2025 to Sep 2026) | Change |
|---|---|---|---|
| Brand searches (12-month total) | 120,680 (avg 10,057/mo) | 155,400 (avg 12,950/mo) | +28.8% |
| Category searches (rain, waterproof, hiking, insulated jacket) | 995,920 | 1,394,850 | +40.1% |
| Competitor searches (Fjellmark, Arcton, Vallo) | 422,390 | 626,210 | +48.3% |
| Brand share of category | 12.1% | 11.1% | down 1.0 pt |
| Brand share of brand plus competitors | 22.2% | 19.9% | down 2.3 pts |

- Brand year-on-year, by month: +32.0% (Oct) to +22.2% (Jun), average about +29%.
- Category year-on-year, by month: +31.7% (Mar) to +46.1% (Sep).
- Brand grew more slowly than the category in all 12 campaign months. Brand share of category was below the prior year's share in every month from October 2025 onward.
- If brand had kept pace with the category (+40.1%), it would have reached about 169,000 searches. It reached 155,400, about 13,600 short.

Spend and reach (YouTube, campaign "Nordvik Brand - Built for Weather", Oct 2025 to Sep 2026):

- Total cost: 179,607.32 (currency as in the file; average 14,967 per month).
- Monthly cost stayed within 14,622 to 15,169 (about plus or minus 2%).
- Impressions: 19,707,328. Views: 4,833,456 (24.5% of impressions).
- Cost per view: about 0.037. Cost per 1,000 impressions: about 9.11.

## Why the 30% does not show the campaign worked

1. The market grew faster. Category searches rose about 40% and competitor searches about 48% over the same months, with no Nordvik campaign on those keywords. A brand that rises 29% in a market that rises 40% has lost ground.
2. Brand share fell. The campaign did not take share from competitors or grow Nordvik's part of the category.
3. Spend was flat. Monthly cost varied by about 2% for all 12 months, so the data cannot show how brand searches respond to more or less spend. Doubling the budget would be an extrapolation the data does not support.
4. No clean control. The file has no data before October 2024, so the pre-campaign trend cannot be measured year over year. The category and competitor series are the nearest controls, and both grew faster.

## Recommendation

1. Do not double the budget now.
2. Hold the current budget and test it. Options: a geo holdout (pause in a few regions for 8 to 12 weeks), or a planned step-down and step-up of spend, with brand share of category tracked as the primary measure.
3. Ask the team for a brand-lift survey or a branded-search baseline from before October 2025, so the pre-period trend is measured directly.
4. Before any budget decision, check whether Nordvik's own brand terms are being cannibalised or the category is driving the search growth.

## Caveats

- Search volumes are Keyword Planner monthly estimates for three brand terms, so small changes are noise.
- Brand, category and competitor totals are simple sums of the keywords listed in the file. They are not weighted.
- Spend and impressions do not show what the campaign reached in the target audience, only what it delivered.
- The file has no currency and no sales data. Nothing here measures revenue or purchases.
- These are descriptive comparisons, not a causal test.
````
