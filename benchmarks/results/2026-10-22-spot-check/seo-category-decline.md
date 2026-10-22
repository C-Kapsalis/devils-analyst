# seo-category-decline

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/diagnose/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/seo-category-decline/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> We're Brightwater Pools. Our organic search traffic dropped 25% this quarter (Q3 2026 vs Q2 2026). What went wrong and what should we fix? resources/gsc_weekly.csv is our weekly Search Console data and resources/competition.csv is the weekly estimated organic clicks for our main competitors from our SEO tool. Write report.md with what happened and what we should do.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `competitor-share` | PASS | PASS | both: competitors -23.8%, share 23.1% to 23.0% |
| `demand-not-seo` | FAIL | FAIL | neither names lower category demand as the main cause; A leads with a site-wide or measurement change and argues brand demand cannot fall 25%; B lists demand as one of four candidates behind a "market-wide visibility" change |
| `recommendation` | PASS | PASS | both: no SEO overhaul; verify, compare with last year, monitor share (A leads with technical checks, borderline) |

## Re-run of arm A after the skill fix

| Grader | A, first run | A, re-run | Why |
|---|---|---|---|
| `competitor-share` | PASS | PASS | competitors -23.8%, share 23.1% to 22.9% |
| `demand-not-seo` | FAIL | PASS | lower category demand is now the first-ranked hypothesis, backed by impressions down at flat position and CTR and by the competitors' equal fall; says the data shows no SEO fault |
| `recommendation` | PASS | PASS | no SEO change; last year's weeks, a demand source, a share trigger |

## Arm A answer (with skill)

````markdown
# Organic clicks fell 25% in one step in the week of 6 July, and competitors fell by the same amount

Brightwater Pools, Q3 2026 vs Q2 2026, Search Console clicks. Each quarter is 13 weeks, assigned by week-start date (Q2 = 6 Apr to 29 Jun, Q3 = 6 Jul to 28 Sep).

**Bottom line:** The data does not show that we lost ground to competitors or that our rankings slipped. Our clicks fell in the same week, and by a similar amount, as the three competitors. Verify whether a site change or a change in reporting caused it before spending on SEO fixes.

## What happened

- Total clicks: 447,254 (Q2) to 337,335 (Q3), down 109,919 or 24.6%.
- Brand clicks: 284,008 to 213,906, down 24.7%. Non-brand clicks: 163,246 to 123,429, down 24.4%.
- Brand accounts for 70,102 of the lost clicks (64%).
- Impressions fell by a similar amount: brand down 25.2%, non-brand down 24.8%.
- Click-through rate and position did not move. Brand CTR was 35.7% in Q2 and 36.0% in Q3. Non-brand CTR was 3.09% and 3.11%. Brand position was 1.30 in both quarters. Non-brand average position was 8.40 in Q2 and 8.42 in Q3.
- Competitor estimated organic clicks (Aqua Depot, PoolPro Supply, SplashMart): 1,486,293 to 1,132,615, down 23.8%. Individually: Aqua Depot down 24.4%, PoolPro Supply down 22.9%, SplashMart down 24.0%.
- Our share of the four-site total was 23.1% in Q2 and 23.0% in Q3. This compares our Search Console clicks with the SEO tool's estimates, so only the trend is meaningful, not the level.

## The step happened in one week

Our Q2 weekly brand clicks stayed between 21,203 and 22,827. In the week of 6 July they dropped to 17,856, and total weekly clicks fell from 35,325 (week of 29 June) to 28,052 (week of 6 July), a drop of 20.6%. Over the same two weeks, competitor estimates fell 17.1% (Aqua Depot), 15.3% (PoolPro Supply) and 11.9% (SplashMart). A drop this sudden and this shared points to a common cause, not a gradual loss of share.

## Finding 1: Acquisition is declining, and the market fell the same week

**Organic acquisition is declining: clicks fell 24.6% (447k to 337k) from the week of 6 July, with brand and non-brand falling together.**

Likely cause: a site-wide or measurement change that hit us and the competitors' visibility at the same time (hypothesis; not yet confirmed). We have no data that identifies the specific change.

Evidence for: the step is in one week for both query types, and competitors dropped in that same week.

Evidence against: our average position and CTR did not change, so there is no sign that we ranked lower for the queries we still show for. The competitor estimates also fell, so "competitors took our clicks" is contradicted: our share held at about 23%.

Also, a 25% fall in brand impressions in one week is hard to explain by real search demand for our name. Check the reporting before concluding anything about demand.

Do next:
1. In Search Console, check what changed on or around 6 July: site migrations, template or robots changes, noindex tags, sitemap and indexing (Pages report), and property settings. A simultaneous drop in impressions across all queries is what a site-wide visibility or indexing change looks like.
2. Ask the SEO tool vendor whether their estimation method changed on or around 6 July. If it did, the competitor drop is partly an artifact, and our drop may be too.
3. Pull the same 13 weeks from last year. If clicks fall every early July, this is seasonality. Then set Q4 targets against last year, not against Q2.

Verify in: Search Console (Pages report, Crawl stats and sitemaps for weeks of 29 June and 6 July); GA4 organic sessions for the same weeks (if sessions fell too, the loss is real and not a reporting change); the SEO tool's methodology notes.

## Finding 2: The decline continued through Q3, and competitors slid too

**Clicks are still sliding within Q3: brand and non-brand each fell about 11% from July (weekly average) to September.**

Brand fell from an average of 17,401 clicks a week in July to 15,439 in September (down 11.3%). Non-brand fell from 10,021 to 8,889 (down 11.3%).

Competitors fell by a similar amount over the same months: Aqua Depot down 13.8%, PoolPro Supply down 11.6%, SplashMart down 10.4%.

So the slide is also visible in the market, and there is no sign that our share is shrinking within the quarter. Re-check in four weeks; if our slide runs ahead of the competitors', investigate that gap separately.

## Finding 3: Non-brand is the lever, but this data cannot show it

Our non-brand average position is 8.4. That sits in the 4 to 20 range, where moving up a few places usually adds the most clicks. This is a rule of thumb, not something this data proves. The files have no query-level or page-level data, so we cannot say which queries or pages to work on. Get a query-level Search Console export before choosing any content work.

## What the data cannot tell us

- The folder name says "category decline", but the data has no category split. We cannot say which product categories fell.
- Search Console clicks are not sessions or revenue. The 25% is a click number. We have no conversion or revenue data, so we cannot size the money at stake. Multiply the lost clicks by our click-to-order rate to size it.
- Competitor figures are third-party estimates. Their method is unknown and may have changed.

## Recommendation

Do not fund an SEO fix yet. Run the three checks in Finding 1 first. If they find a site-side change on or around 6 July, reverse that change, since it will likely recover the clicks. If they find a market-wide or reporting change, reset Q4 targets against last year and against the competitors, and use the query-level export to choose non-brand content work.

Source files: scratchpad sc/seo-category-decline/A/resources/gsc_weekly.csv and competition.csv. Method: devils-analyst diagnose skill, with the Cohortica funnel diagnostic (Acquisition) and the SEO playbooks on overview, query-level data and organic-paid overlap.
````

## Arm B answer (without skill)

````markdown
# Organic search decline, Q3 2026 vs Q2 2026

## Summary

Brightwater's organic clicks fell 24.6% in Q3 2026 against Q2 2026 (447,254 to 337,335 clicks). The decline is not a Brightwater-specific ranking failure. Brand and non-brand traffic fell by almost the same amount, average position did not move, and the three tracked competitors fell by a similar amount in the same week. The data points to a shared, market-wide step change starting in the week dated 2026-07-06, not to a problem Brightwater caused. Before spending on fixes, confirm the cause is real and not a measurement change.

Note on the brief: the drop is 24.6%, not 25%.

## What happened

Quarters are 13 weekly rows each. Q2 is the weeks dated 2026-04-06 to 2026-06-29. Q3 is the weeks dated 2026-07-06 to 2026-09-28.

| Measure | Q2 2026 | Q3 2026 | Change |
|---|---|---|---|
| Total clicks (brand + non-brand) | 447,254 | 337,335 | -24.6% |
| Brand clicks | 284,008 | 213,906 | -24.7% |
| Non-brand clicks | 163,246 | 123,429 | -24.4% |
| Brand impressions | 794,423 | 594,161 | -25.2% |
| Non-brand impressions | 5,279,606 | 3,969,808 | -24.8% |
| Brand average position (mean of weeks) | 1.30 | 1.30 | flat |
| Non-brand average position (mean of weeks) | 8.40 | 8.42 | flat |
| Brand CTR (clicks / impressions) | 35.8% | 36.0% | flat |
| Non-brand CTR | 3.09% | 3.11% | flat |

Three things stand out:

1. **A single step, not a slide.** Weekly clicks ran at 33,000 to 35,500 in every week of Q2. The week dated 2026-07-06 dropped to 28,052 (from 35,325 the week before), and the level then held at 23,000 to 29,000 for the rest of Q3. There was no gradual erosion.
2. **Visibility fell, rankings and click-through did not.** Impressions dropped about 25% in both brand and non-brand, while position and CTR stayed flat. Fewer people (or fewer result slots) saw Brightwater's listings; the listings that did appear performed as before.
3. **Competitors dropped in the same week.** Combined estimated organic clicks for Aqua Depot, PoolPro Supply and SplashMart fell from 1,486,293 (Q2) to 1,132,615 (Q3), or -23.8%. By competitor: Aqua Depot -24.4%, PoolPro Supply -22.9%, SplashMart -24.0%. Each one's largest weekly drop is in the week dated 2026-07-06 (Aqua Depot 53,737 to 44,556; PoolPro 38,124 to 32,303; SplashMart 23,430 to 20,641).

Brightwater's share of the four-site total (Brightwater plus the three competitors) went from 23.1% in Q2 to 23.0% in Q3, about 0.2 points. That is essentially unchanged.

## What this means

- The loss is consistent with a market-wide change in search visibility that hit every site in the set in the same week, including Brightwater's brand queries. Brand demand is not normally something a company loses to its own ranking, so the cause is more likely outside the site.
- This data does not show a ranking loss, a click-through problem, or a loss of share to competitors. Investing in ranking work to "fix" this would be aimed at the wrong symptom.
- The data cannot show the cause. Candidate causes include a search-engine change around 2026-07-06, a change in how Search Console or the SEO tool measures impressions, a site-wide technical event (indexing, tracking or outage) on the same date, or a real drop in search demand for pool products.
- The competitor figures are estimates from the SEO tool, not measured data. A same-week drop across all four sites could partly be a change in the tool's model. This needs checking.
- The dataset covers only 26 weeks, so we cannot test whether a summer drop is normal seasonality for pool products. Last year's weekly data would settle that.

## What we should do

1. **Confirm the drop is real before acting (this week).**
   - Check the Search Console property for changes, verification issues or coverage drops around 2026-07-06.
   - Check that the site was up, indexed and tracked the same week (uptime, index coverage, analytics tags, any site release).
   - Ask the SEO tool vendor whether its competitor estimates changed methodology around that week.
2. **Establish the external cause.** Check the search-engine change log and industry reports for early July 2026, and pull prior-year weekly data to test seasonality.
3. **Do not start a ranking overhaul yet.** Average position is flat in both brand and non-brand queries. Revisit only if a later week shows position falling.
4. **If the drop is real and market-wide, protect what still works.** CTR held steady, so the remaining impressions convert as before. Focus on keeping the high-intent pages and listings that still earn impressions, and on demand sources that do not depend on search visibility (for example email, paid search and direct campaigns), because brand search volume itself fell.
5. **Set up monitoring.** Track weekly brand and non-brand impressions and Brightwater's share of the four-site total. Alert if the share falls below about 22.5% or if position moves more than about 0.5 places in either query type. Those thresholds are judgement calls, not derived from this data.

## Open questions for the team

- Did anything change on the site, in paid search, or in content around 2026-07-06?
- Does the SEO tool's competitor estimate use the same method before and after that week?
- Do we have prior-year Search Console data for the same weeks?

## Method

Totals are the sum of brand and non-brand clicks (and impressions) per week, summed by quarter. Position is the simple mean of the 13 weekly values, since the source does not give impression weighting. Competitor totals are sums of the weekly estimates per site. Shares are Brightwater clicks divided by Brightwater plus the three competitors. All figures were computed by hand from resources/gsc_weekly.csv and resources/competition.csv, without running code.
````

## Arm A re-run answer (after the skill fix)

````markdown
# Brightwater Pools: organic clicks fell 24.6% in Q3, in step with the category

Organic clicks fell from 447,254 in Q2 2026 to 337,335 in Q3 2026, a drop of 24.6% (the 25% you quoted, to one decimal). The three competitors in the data fell 23.8% together, and our share of the four sites' clicks held at 23.1% in Q2 and 22.9% in Q3. The whole step happened in one week, the week labelled 2026-07-06. The data does not show a fault in our SEO. It shows the category and the results page dropping together. The cause is not yet proven.

## What happened

**The drop came in one week and stayed.** Our clicks (brand plus non-brand) went from 35,325 in the week of 2026-06-29 to 28,052 in the week of 2026-07-06, down 20.6%. The three competitors' estimated clicks went from 115,291 to 97,500, down 15.4%. Both stayed near the new level through September. Nothing recovered.

**Impressions fell; position and click-through did not.**
- Brand: impressions 794,423 to 594,161 (down 25.2%). Average position 1.30 in both quarters. CTR 35.8% to 36.0%.
- Non-brand: impressions 5,279,606 to 3,969,808 (down 24.8%). Average position 8.40 to 8.42. CTR 3.09% to 3.11%.

Fewer searches are showing our listings, at the same position and the same click rate. That points at demand (fewer searches for these terms), not at our rankings or our snippets.

**Brand and non-brand fell by the same share.** Brand clicks fell 24.7% (284,008 to 213,906). Non-brand clicks fell 24.4% (163,246 to 123,429). Brand is 63% of our clicks in both quarters. Non-brand is the part that brings in new customers, and it fell as far as brand did.

## Is it us? The competitor check

| Site | Q2 clicks | Q3 clicks | Change |
|---|---|---|---|
| Brightwater (GSC) | 447,254 | 337,335 | -24.6% |
| Aqua Depot | 676,933 | 511,983 | -24.4% |
| PoolPro Supply | 489,259 | 377,386 | -22.9% |
| SplashMart | 320,101 | 243,246 | -24.0% |

Our share of the four sites' clicks was 23.1% in Q2 and 22.9% in Q3, a change of 0.2 points.

Our Search Console series and the competitor estimates stepped down in the same week. A tracking fault on our side cannot change the competitors' estimates, so a shared step points at the market or at Google's results page, not at our site.

Caveats: the competitor figures are a tool's estimates, not measured clicks. Search Console counts clicks on Google's results page, not sessions, so this report says nothing about orders or revenue. Quarters are the 13 weekly rows labelled by week start: Q2 is 2026-04-06 to 2026-06-29, Q3 is 2026-07-06 to 2026-09-28. Average positions are simple means of the weekly values. Click-through rates are clicks divided by impressions over each quarter.

## Hypotheses, ranked

1. **Lower search demand for the category, seasonal or market-wide.** Supported: all four sites fell about 24%, and our impressions fell at a steady position. Not confirmed: we have no same-period data from last year and no demand source yet.
2. **A change to Google's results page in late June or early July 2026.** Supported by a one-week step that hit every site. Not checked.
3. **Lost pages or ranking coverage on our side.** Against it: brand position held at 1.3 and non-brand position held at 8.4, and the fall is even across brand and non-brand. Not ruled out at page level.

## What we should do

1. **Do not change the SEO plan or move budget off SEO based on this quarter.** Our share held, so the evidence does not point at our work. Verify with steps 2 to 4.
2. **Check whether the step is seasonal or a Google change, this week.** Pull the same weeks of 2025 from Search Console. If the same step appears in the week of early July, it is seasonal. Check Google's Search Status Dashboard for updates dated late June to early July 2026. Verify: a step in the same week last year, or a dated Google update in that window.
3. **Check demand directly.** Pull Google Trends or Keyword Planner volumes for our brand name and our top 10 non-brand terms, for the same weeks. Verify: if those terms fell by about 24% in the same week, the loss is demand.
4. **Find where impressions fell, page by page.** Pull Search Console by page for the same two quarters. Verify: if most pages fell about 25%, it is demand. If a few pages fell by half or more, investigate those pages first.
5. **Set a share trigger.** Track our share of the four sites' clicks each week. Investigate our own pages if it falls below 21% for three weeks running, two points under the Q2 level of 23.1%. Verify: the weekly share line.
6. **Brand demand is a marketing question, not an SEO one.** Brand impressions fell 25%, so fewer people searched our name. Check whether paid brand spend, PR or offers changed this summer. Verify: spend and reach in the ad platforms for the same weeks.
````
