# Marketing metric catalog

Every metric with its formula, the grain it is valid at, and the trap that makes it lie. Paths in parentheses name the Cohortica playbook a definition comes from; the playbooks themselves ship in the `diagnose` skill (`references/playbooks/`). **[std]** marks a standard industry definition added where the playbooks are silent; **GAP** marks what neither covers.

## Rules that recur in every discipline
- **Read the transition, not the step.** The leak is "almost always in a transition between steps, not in any single step" (paid-search/paid-search-overview.md; same logic in web-analytics/marketing-funnel-overview.md, email-marketing/reading-the-send-funnel.md, seo/search-console-and-ga4.md).
- **Never trust the blend.** Split before judging: brand vs generic, country x device, prospecting vs retargeting, match type, channel, landing page, cohort age, per send.
- **Recompute ratios from totals** at the grain you read; never average row-level rates (seo/landing-page-performance.md). Weight account-level aggregates by the right denominator (paid-search/impression-share-and-quality-score.md).
- **Pin one conversion/value event** before computing any CVR, CPA or ROAS (paid-search/conversions-cpa-and-return.md, paid-media/auditing-pmax.md, seo/search-console-and-sem.md).
- **Credit is not cause.** Attribution reassigns credit; only a randomized experiment proves incrementality (attribution-experiments/*, paid-media/true-roas.md).
- **The business model picks the top metric.** Store: conversion, ROAS, LTV. Publisher: sessions, depth, CTR, click volume (web-analytics/marketing-funnel-overview.md, seo/query-level-data.md, seo/organic-paid-overlap.md).
- **Order of reads matters.** Hygiene before growth; fine-tuning (device, geo) last (paid-search/insight-roadmap.md, seo/insight-roadmap.md, paid-media/insight-roadmap.md).


## GA4 / web analytics

| Metric | Formula | Grain / additivity caveat | Trap the playbooks warn about | Source |
|---|---|---|---|---|
| Sessions | count of sessions [std] | Additive across channels/pages within GA4; never sum with GSC clicks | Ranking channels on it: "the easiest number to buy and the least meaningful to rank on"; a spike with falling engagement is the wrong kind of growth | web-analytics/ga4-fundamentals.md; web-analytics/on-site-funnel.md |
| Engaged sessions | sessions lasting >10s, or 2+ pageviews, or firing a key action | Additive; "the honest denominator for value math" | — | web-analytics/ga4-fundamentals.md |
| Engagement rate | engaged sessions / sessions | Ratio: recompute from totals per cut; cut by channel and landing page, never blended | Reading one channel in isolation (the signal is the spread vs peers); can read high structurally (one-page site clears 10s bar). Healthy ~55-63%; below ~40% on a channel = traffic and landing page disagree | web-analytics/ga4-fundamentals.md; web-analytics/on-site-funnel.md |
| Avg engagement time + pages per visit | engagement time / sessions [std]; pageviews / sessions [std] | Read together | Long duration with pages/visit near 1.0 usually means stuck, not absorbed | web-analytics/on-site-funnel.md |
| Conversion rate | conversions (one named key action) / sessions | Ratio; must name the action; cut by channel | Site-wide blended rate "describes no real visitor"; a mix shift toward a low-converting channel moves it with no behavior change. Ecom ~2-3% per session (also quoted 1.5-2.5%) | web-analytics/on-site-funnel.md; seo/organic-and-on-site-behaviour.md |
| Revenue per engaged session | revenue / engaged sessions | Ratio per channel | Substituting revenue per raw session "punishes high-engagement channels and flatters bouncy ones" | web-analytics/ga4-fundamentals.md |
| Revenue per user | revenue / users | Ratio; users are not additive across cuts [std] | Total revenue up while revenue per user falls = bought growth. Named "the cleanest single health signal" | web-analytics/on-site-funnel.md |
| Revenue by channel | sum of revenue by channel group | Additive within the attribution model in use | Treating GA4's revenue split as ROI: GA4 has no cost; ROI needs spend reconciled from ad platforms | web-analytics/ga4-fundamentals.md |
| Revenue per purchaser | revenue / transactions (as defined in the playbook) | Ratio | Separates fat-basket sends from cheap-item buyers | email-marketing/click-to-revenue.md |
| Sessions / transactions / revenue by utm_campaign | grouped on campaign key | Only as good as tagging consistency | Judging channels on sessions: the click ranking often inverts on revenue | web-analytics/utm-tagging.md |
| Tagging coverage | share of traffic and revenue reconciling to a named campaign | — | "A scheme is only as good as its least disciplined link"; where it drifts, revenue figures are a floor | web-analytics/utm-tagging.md |
| Direct / untagged bucket | sessions/revenue with no campaign | — | Tell of tagging drift; a direct spike after launch = untagged links first, not brand lift | web-analytics/utm-tagging.md |
| Data-driven attribution credit vs last-click | per-channel credit delta between models | Needs ~400 conversions per conversion type over 28 days | Below threshold GA4 silently falls back to last-click; credit deltas are a "sized fund-more/fund-less order" but credit is not cause | web-analytics/on-site-funnel.md |
| Funnel band metrics: CTR (awareness), engagement rate (consideration), CVR/AOV/ROAS/LTV (action) | per band | Judge hand-off rates between bands | Any band metric read alone; comparing retention across cohorts of different ages | web-analytics/marketing-funnel-overview.md |

## Search Console / SEO

| Metric | Formula | Grain / additivity caveat | Trap | Source |
|---|---|---|---|---|
| Impressions | count of times a result was shown | Query level = one per search (true demand). Query-page level = one per page shown, so summing double-counts when 2 of your pages appear | Ambient: "prove visibility, not interest"; high impressions on mismatched intent "a trap dressed as a win"; tiny-impression rows are "sampling dust" | seo/query-level-data.md; seo/seo-overview.md; seo/landing-page-performance.md; seo/search-console-queries.md |
| Clicks | count of clicks on results page | Never foot to GA4 sessions; never add across systems | Sorting by clicks first "optimizes pages that were already fine"; read last | seo/search-console-queries.md; seo/organic-and-on-site-behaviour.md |
| CTR | clicks / impressions, recomputed from totals at the grain read | Never average row CTRs ("a number true of nothing") | Must be read against position: soft CTR at strong position = title/snippet problem; soft CTR at pos 12 = ranking problem. Top-3 should pull ~10-40%; #1 ~27.6% (27-39%) | seo/landing-page-performance.md; seo/insight-roadmap.md; seo/seo-overview.md |
| Average position | impression-weighted average of topmost rank per search | Not additive; at query level it is the topmost rank you held, masking a weaker second page | Hides the distribution (an "8" may swing 3-15); noisy at low volume; lags 2-3 days; read trend arrow, not decimal | seo/seo-overview.md; seo/query-level-data.md; seo/new-and-newly-ranking-pages.md |
| Position zones | buckets: 1-3 defend / snippet-rewrite if CTR weak; 4-20 leverage zone (rank push); 10-20 "workable zone"; 50+ leave alone | — | Spreading effort evenly; deep-tail effort (pos 35) | seo/search-console-queries.md; seo/new-and-newly-ranking-pages.md |
| Brand vs non-brand clicks / CVR | split by query classification | Split before any rate | Blended 2.2% CVR can be brand 6% + non-brand 0.7%; "a site coasting on brand clicks looks healthy while acquiring nobody new" | seo/query-level-data.md; seo/seo-overview.md |
| Query clusters | sum of variants (spellings, plurals) of one intent | Aggregate at query level, not query-page | Top string can be under half its intent's demand; clustering can double apparent demand | seo/query-level-data.md |
| Cannibalization signal | one query with 2+ of your URLs logging impressions (query-page level) | Only visible at query-page grain | Fix is consolidating intent, not tweaking two titles | seo/query-level-data.md; seo/search-console-landing-pages.md |
| New queries / newly ranking pages | pages/queries with impressions now that had ~none prior period | Date comparison | High impressions from browsing queries = awareness churn | seo/search-console-new-pages.md; seo/new-and-newly-ranking-pages.md |
| New pages per month | count of genuinely new pages entering the report | Trend | Flat line toward zero = clicks propped up by old pages, "coasting toward decline" | seo/search-console-new-pages.md |
| Zero-impression sitemap pages | sitemap URLs minus URLs with impressions | GSC never volunteers this list | Silent failure; classic cause a leftover `noindex` | seo/search-console-landing-pages.md |
| Joined page funnel | impressions -> clicks (GSC) -> sessions -> engagement -> conversions -> revenue (GA4 Organic) per landing page | URL sets won't match perfectly; read shape, not arithmetic | Summing or reconciling across systems | seo/search-console-and-ga4.md |
| Theoretical CVR | paid search CVR on the same query | Estimate, not measurement | Ad clicks land on tuned pages with skewed audience; "ranks opportunities; it does not promise outcomes" | seo/query-level-data.md; seo/search-console-and-sem.md |
| Share of rented demand per theme | share of converting paid spend in a theme with weak organic | Group by theme | Briefing off a flat query list ("row 214") | seo/organic-paid-overlap.md |

## Google Ads / paid search

| Metric | Formula | Grain / additivity caveat | Trap | Source |
|---|---|---|---|---|
| Impression share | impressions / eligible impressions | Aggregate weighted by eligible impressions; platform buckets <10% and >90% | Aim >~80% on core terms ("high tens of a percent") | paid-search/impression-share-and-quality-score.md; paid-search/paid-search-overview.md |
| IS lost to rank / lost to budget | share of eligible impressions lost to ad rank / to daily cap; IS + lost-rank + lost-budget = 100% of eligible pool | Same weighting | Opposite fixes: rank -> quality or bids; budget -> raise cap on a converting campaign. Confusing them wastes money both ways | paid-search/impression-share-and-quality-score.md |
| Top / absolute top impression rate | share of impressions above organic / in first slot [std phrasing] | — | "Are we showing well?"; matters most on mobile | paid-search/impression-share-and-quality-score.md |
| Ad rank | bid x quality score | — | Great QS can outrank a bigger budget | paid-search/paid-search-overview.md |
| Quality score | 1-10 from expected CTR, ad relevance, landing-page experience | Read as component distributions, not account average | Top score ~halves CPC, bottom ~5x it; read which component drags | paid-search/impression-share-and-quality-score.md |
| CTR | clicks / impressions | Split brand vs generic, by match type | Blended CTR flattered by brand (~45% brand vs <2% generic); search median mid-single digits | paid-search/brand-vs-generic.md; paid-search/paid-search-overview.md |
| CPC | cost / clicks | Split by device, match type | "Meaningless on its own"; judge vs break-even ceiling; broad's cheap CPC = "waste at a discount" | paid-search/paid-search-overview.md; paid-search/match-types-and-wasted-spend.md |
| Break-even CPC | margin per conversion x conversion rate | Per campaign/product line | $40 margin x 5% = $2.00; a "cheap" $2.40 click loses. First-order: repeat purchase raises it (LTV) | paid-search/conversions-cpa-and-return.md |
| Conversions | count of the scoped value action | Never blend micro (sign-ups) with sales | Same month: ~89,000 sign-up "conversions" vs ~32,000 sales | paid-search/conversions-cpa-and-return.md |
| Conversion rate | conversions / clicks [std denominator for ads] | Judge vs vertical | Search median ~7%; high CTR + low CVR "most expensive failure mode" | paid-search/paid-search-overview.md |
| CPA | cost / conversions (scoped) | Per campaign, never blended | Meaningless without ceiling; blended CPA hides a line over its margin | paid-search/conversions-cpa-and-return.md |
| ROAS (revenue) | conversion value / spend | Per campaign | Last-click ROAS credits the paid click with the whole sale | paid-search/conversions-cpa-and-return.md |
| ROAS (profit) | (conversion value x margin) / spend | Per line | 4:1 revenue ROAS on 20% margin = $0.80 profit per $1 = loss | paid-search/conversions-cpa-and-return.md |
| Spend share brand/generic | spend by segment / total | — | Typically ~15% brand / ~85% generic; congratulating cheap brand volume | paid-search/brand-vs-generic.md |
| Leakage impressions | brand queries in generic campaigns (forward) / generic queries in brand campaigns (reverse) | 2x2 campaign type x query type | Forward leakage flatters generic so you "scale a mirage" | paid-search/brand-vs-generic.md |
| Cost per sale by match type | cost / sales per match type | Split before judging | Broad cheapest per click, worst per sale; phrase can have highest CPC | paid-search/match-types-and-wasted-spend.md |
| Zero-conversion spend by search term | sum cost where conversions = 0 | Search terms are a sample | "Single highest-return read of a paid-search week"; cluster, do not cut row by row | paid-search/match-types-and-wasted-spend.md |
| New-query CVR vs parent keyword | term CVR vs keyword CVR | — | Promote only if converts (not clicks), specific, enough volume/margin | paid-search/query-performance.md |
| Pace: MTD spend, trailing-7-day avg daily spend, projected EOM | projection = MTD spend + (trailing 7d avg x days remaining) | Per campaign/group, not account | Account pace hides a starving winner and a hot bleeder cancelling out; different methods in different spreadsheets | paid-search/budget-pacing.md |
| CVR and CPC by device / day / hour | split | Manual-bid levers only | Phone click at 2x CPC and 1/2 CVR worth ~1/4 desktop click; under automated bidding modifiers are advisory | paid-search/device-and-timing.md |
| Ad group size | keywords per ad group | 5-15 tight keywords | 50-keyword grab-bag sags CTR; splitting can ~triple CTR at under half CPC | paid-search/account-structure.md |

## Performance Max / Display / Video & YouTube / Demand Gen

| Metric | Formula | Grain / caveat | Trap | Source |
|---|---|---|---|---|
| Clicks vs CPC by month (PMax) | trend pair | Filter by `performance_max` enum, not campaign name | Clicks up with rising CPC = bought growth; "doubled clicks at a doubled CPC with flat purchases ... precedes a quiet ROAS collapse" | paid-media/auditing-pmax.md; paid-media/performance-max.md |
| PMax campaign CTR | clicks / impressions | Campaign-type level | Do not compare to search CTR; different inventory | paid-media/auditing-pmax.md |
| Conversions under one lens | conversions of one value event (purchase) | Columns blank until a lens is chosen | Blended total mixes sign-up with €200 order; sparsity is legitimate, not broken | paid-media/auditing-pmax.md |
| Conversion value per campaign | sum value | — | Weigh on revenue, not headline count | paid-media/auditing-pmax.md |
| Branded vs non-branded conversions (PMax) | split | — | PMax cannibalizes brand; Optmyzr: Search/PMax overlap in 91% of 503 accounts, Search won ~2x as often | paid-media/performance-max.md |
| CPM | cost / impressions x 1000 | By campaign and cluster | Unbeatably low CPM often = unseen or bot impressions | paid-media/display-advertising.md |
| Display CTR | clicks / impressions | — | ~0.46% at ~$0.63 CPC; misleading as a display verdict | paid-media/display-advertising.md |
| Viewable rate | viewable impressions / measured impressions [std]; viewable = >=50% pixels on screen for 1 continuous second (MRC) | — | Reading raw served impressions | paid-media/display-advertising.md |
| Invalid-traffic signature | very low CPM + huge impressions + nothing downstream | — | Seductive price keeps drawing budget into MFA inventory | paid-media/display-advertising.md |
| Frequency | impressions / reach [std] | — | Past a handful of exposures, irritates; rising frequency + flat retention/demand = fatigue | paid-media/display-advertising.md; paid-media/video-and-youtube.md |
| Retargeting return | value / spend on retargeting | — | Harvests demand prospecting created; hard ceiling; exclude converters | paid-media/display-advertising.md |
| Cost per view | cost / views; skippable view = 30s watched (or whole ad if shorter) or an engagement click | — | Cheap views the creative cannot hold are the most expensive line | paid-media/video-and-youtube.md |
| Quartile completion | % viewers reaching 25/50/75/100% | — | Cliff after first quarter = hook buried past skip button | paid-media/video-and-youtube.md |
| View-through conversions | conversions after view without click | No platform hands the incremental version cleanly | Dressing a click count up as awareness verdict | paid-media/insight-roadmap.md; paid-media/video-and-youtube.md |
| Brand lift | awareness/consideration exposed vs held-back group | Experiment | — | paid-media/video-and-youtube.md |
| Last-click revenue by campaign name (Demand Gen) | on-site revenue matched by campaign name | "Measured floor" | Treating the floor as the whole return | paid-media/demand-gen.md |
| Budget allocation by channel/cluster | spend share | Read first | Without it, cheap reach drifts unseen | paid-media/insight-roadmap.md |
| Measured (true) ROAS | on-site recorded value (own analytics) / cost, matched by campaign name | One shared denominator; drillable service > account > campaign type > campaign | It is a last-click floor, understating upper funnel | paid-media/true-roas.md |
| Platform-reported ROAS | platform value / spend on platform's own attribution and window | Not additive across platforms | Stacking double-counts the same sale | paid-media/true-roas.md |

## Paid social / Meta (and organic social)

| Metric | Formula | Grain / caveat | Trap | Source |
|---|---|---|---|---|
| CPM | cost / impressions x 1000 | Prospecting | Holding prospecting to a return target starves the top | paid-social/paid-social-overview.md |
| Frequency | impressions / reach [std] | Per week | Heuristic ~2-4 exposures/person/week; rising frequency + falling CTR = creative burnout | paid-social/paid-social-overview.md |
| CTR (link) | link clicks / impressions | Filter to real link clicks | Incidental taps inflate; Meta feed ~1.5%+ healthy heuristic; Facebook avg ~0.90% (WordStream 2022) | paid-social/paid-social-overview.md |
| CPC | cost / clicks | — | Rising CPC with steady CTR = auction competition, not a worse ad | paid-social/paid-social-overview.md |
| Conversion rate | conversions / clicks [std] | — | ~8-9% Facebook landing-page CVR benchmark; strong CTR + expensive CPA = downstream leak | paid-social/paid-social-overview.md |
| ROAS / CPA by job | per prospecting vs retargeting | Never one blended number | Meta can count view-through on its own window (a likely cause unless the export shows the setting), reports more than analytics confirms | paid-social/paid-social-overview.md |
| Blended conversion count | account total under one attribution window | Set one window before comparing | Prevents either job claiming the other's credit | paid-social/paid-social-overview.md |
| Organic reach vs follower base | reach / followers | — | Raw reach meaningless without base | organic-social/organic-social-overview.md |
| Organic engagement rate | (reactions + comments + shares) / followers | Per post vs platform median (FB ~0.06%, IG ~0.43%, TikTok ~2.63%) | Raw engagement counts; posting more into a dead rate | organic-social/organic-social-overview.md |
| Impressions / reach | displays / unique heads | — | Big impressions on small reach = same loyal fans, not discovery | organic-social/organic-social-overview.md |
| Saves and shares per post | counts | Intent-weighted | Optimizing likes | organic-social/organic-social-overview.md |
| Watch time / avg view duration | — | Video | Celebrating views nobody finishes | organic-social/organic-social-overview.md |

## Email

| Metric | Formula | Grain / caveat | Trap | Source |
|---|---|---|---|---|
| Deliverability rate | delivered / sent | Gate; hold >95% | Reading anything downstream before the gate holds | email-marketing/deliverability-and-inbox-placement.md |
| Bounce rate | bounces / sent [std denominator] | Keep <2%; watch trend at steady volume | Watching level not trend | email-marketing/deliverability-and-inbox-placement.md |
| Complaint rate | complaints / delivered [std] | 0.1% warning, 0.3% critical | Treating it as creative problem; it is consent or frequency | email-marketing/list-health-and-reputation.md |
| Open rate | opens / delivered [std] | Directional only; trend across campaigns | Fires on previews, image loads; privacy masking | email-marketing/email-marketing-overview.md |
| CTR | clicks / delivered | Read per send vs 2-5% band; reach-weighted | Pooling across sends of different sizes; one big blast swamps average | email-marketing/engagement-and-the-click.md |
| CTOR | clicks / opens | Read at program aggregate (~10% avg; 14-17% best industries) | Judging a single small send's CTOR; letting a healthy aggregate excuse skipping per-send drill | email-marketing/engagement-and-the-click.md |
| Unsubscribe rate | unsubscribes / delivered | <~0.5% per send | Low churn on stagnant list still standing still | email-marketing/list-health-and-reputation.md |
| Net list growth | (new − unsubscribes − cleaned) / starting list, monthly | Sign matters most; no universal benchmark | No per-campaign metric will flag it | email-marketing/list-health-and-reputation.md |
| Sessions from a send | GA4 sessions with that campaign key | Slightly below clicks is normal; large gap = broken/untagged link | — | email-marketing/click-to-revenue.md |
| Email-attributed revenue / transactions per send | on-site revenue matched by campaign name | Floor; depends on tagging | Ranking sends by clicks | email-marketing/click-to-revenue.md |
| Revenue per purchaser | revenue / transactions | Per send | High-click thin-basket = promise the page/offer didn't keep | email-marketing/click-to-revenue.md |
| Attribution coverage | share of email revenue reconciling to a named send | — | — | email-marketing/click-to-revenue.md |

## CRM / HubSpot lifecycle

**GAP.** No playbook covers CRM, HubSpot, lifecycle stages, MQL/SQL, pipeline, or deal velocity. Related content only: email lifecycle flows (welcome, nurture, win-back) "out-convert one-size-fits-all sends" (email-marketing/email-marketing-overview.md, list-health-and-reputation.md); personas proven by "conversion and repeat rate by audience" (competitive-research/marketing-personas.md). Any lifecycle metric definitions in a skill would need to be [std], not sourced here.

## E-commerce / customer analytics (cohorts, CLV, CAC)

| Metric | Formula | Grain / caveat | Trap | Source |
|---|---|---|---|---|
| Cohort matrix | rows = acquisition month; columns = months since first order; cells = retention or revenue | Compare down columns at matched age only | Comparing a 2-month cohort to a 1-year one; reading young cohorts' empty cells as decline | customer-analytics/reading-acquisition-quality.md |
| Retention rate by cohort age | active customers at age k / cohort size [std] | — | Watch the plateau height (12% vs 6%), not the month-one cliff | customer-analytics/reading-acquisition-quality.md |
| Repeat purchase rate | repeat buyers / cohort customers [std] | Cohort over cohort | Pooled version owned by composition trap: fast-growing store's blended rate falls while every cohort improves | customer-analytics/reading-acquisition-quality.md; cohort-analysis.md |
| New vs returning revenue mix | revenue by first vs repeat customers | — | Context that defuses composition trap | customer-analytics/reading-acquisition-quality.md |
| Revenue per customer by cohort age | cumulative revenue / cohort size | — | — | customer-analytics/reading-acquisition-quality.md |
| CAC | total acquisition spend / customers won, per group and period | Group-level only | Dragging it to the individual "manufactures precision that was never there" | customer-analytics/clv-vs-cac.md |
| Cohort payback period | month when cumulative margin (or revenue) per customer >= acquisition cost | Per cohort; trend | Payback stretching 3 -> 6 months = growth bought at quality's expense | customer-analytics/clv-vs-cac.md; reading-acquisition-quality.md |
| Realized margin to date (LTV floor) | margin generated so far | Assumption-free | Under-investing by ignoring future value | customer-analytics/clv-vs-cac.md |
| Projected LTV (estimate) / ceiling | spend per order x future orders − cost to serve, discounted; ceiling = never churns | Report floor, estimate, ceiling | One-steady-churn-forever undiscounted formula = "the ceiling wearing an estimate's clothes" | customer-analytics/clv-vs-cac.md |
| LTV:CAC | group worth / same group's spend, matched horizon | — | Meaningless if levels or horizons mismatch | customer-analytics/clv-vs-cac.md |
| Order frequency (gap between orders) | days between orders | Per customer/cohort | Stretching gap = churn in progress an active flag never shows | customer-analytics/cohort-analysis.md |
| AOV | revenue / orders [std] | — | Shrinking baskets on "active" customers = wallet moved | customer-analytics/cohort-analysis.md |
| "Active customer" flag | — | — | The easy wrong question; ask "how much of them do we still have?" | customer-analytics/cohort-analysis.md |
| First order value / full-price share | — | By cohort | Discount cohorts that only bought the discount | customer-analytics/reading-acquisition-quality.md |

## Attribution / experiments

| Metric | Formula | Caveat | Trap | Source |
|---|---|---|---|---|
| Last-click ROAS per campaign | recorded value / cost | Floor; model calibration point | Cutting upper-funnel lines it understates | attribution-experiments/attribution-and-mmm.md |
| Multi-touch credit | credit spread across recorded touches | Only sees recorded touches | Credit reassignment, not causal proof | attribution-experiments/attribution-and-mmm.md |
| MMM channel response | modeled sales response to spend over time | Needs history and spend variation | False precision | attribution-experiments/attribution-and-mmm.md |
| Lift | (treatment rate − control rate) / control rate | — | 9.0% vs 20.3% = +125%, not "up 11 points" | attribution-experiments/controlled-experiments.md |
| Incremental conversions | treatment conversions − (control rate x treatment size) | — | 400 treated, 81 conv, 9% baseline -> ~45 caused, not 81 | attribution-experiments/controlled-experiments.md |
| Incremental value | recorded value of incremental orders | — | Not profit without margin | attribution-experiments/controlled-experiments.md |
| Balance-check p-values | test per covariate | >0.05 = groups indistinguishable (good) | — | attribution-experiments/controlled-experiments.md |
| Segment lift | lift by day/device/frequency band | Confirm significance | Averages hide sign flips (+188% weekdays, ~0 weekends) | attribution-experiments/controlled-experiments.md |

## GEO / LLM traffic

| Metric | Formula | Caveat | Trap | Source |
|---|---|---|---|---|
| LLM session share | LLM-referred sessions / total sessions, monthly | The only honest size read | 0.2% -> 0.4% is a doubling a volume chart hides | emerging/measuring-llm-traffic-in-ga4.md |
| Engagement rate under LLM filter | engaged / sessions | Compare vs organic-search baseline | — | emerging/measuring-llm-traffic-in-ga4.md |
| Conversion vs organic baseline | LLM CVR / organic-search CVR | Small denominators; read over several months | Comparing to site average; below baseline = page fix, not channel | emerging/llm-traffic-and-organic-search.md |
| Cited-page set | landing pages receiving LLM traffic; entrants/dropouts | — | Expecting it to mirror SEO priorities | emerging/llm-traffic-and-organic-search.md |
| Branded query volume | branded searches, growth relative to non-branded | Proxy | Without the non-brand comparison, SEO gains masquerade as GEO wins | emerging/geo-getting-cited-in-ai-answers.md |
| Citation share | share of relevant AI answers naming you | Not cleanly measurable | Vendors claiming a clean count are overselling | emerging/geo-getting-cited-in-ai-answers.md |

## Profit, pricing and promotions

From the author's notes (pricing, promotions and marketing analytics courses).

| Metric | Formula | Caveat |
|---|---|---|
| Profit ROAS | (conversion value x margin) / spend | Break-even = 1.0. A 4:1 revenue ROAS at 20% margin is 0.8: a loss |
| Net ad ROI | (incremental profit - ad cost) / ad cost | Break-even = 0%. Some notes call this "POAS": always name which of the two you show and state its break-even |
| Contribution-margin ratio | (price - variable cost) / price | |
| Markup vs margin | markup = (P - C) / C; margin = (P - C) / P | Mixing them is a common reporting error |
| Break-even volume | fixed cost / contribution per unit | For a campaign: program cost / contribution per incremental unit |
| Pace to plan | projected month-end spend - monthly budget | Under-spend is a failure too: the quieter, more expensive one. Per campaign or cluster |
| Baseline sales | sales at regular price, outside promotions | Track its trend: falling baseline with rising promo lift = deal dependence |
| Promo lift | promo-period sales - baseline | Not a win until margin cost, pull-forward (sales stolen from later weeks) and repeat are netted |
| Promotion share of revenue | revenue sold on promotion / total revenue | Above about 40% the notes call it "training deal-seekers" (heuristic) |
| Own-price elasticity | %change in quantity / %change in price | Omitting promo signage from the model overstates it |

## Customer value

| Metric | Formula | Caveat |
|---|---|---|
| CLV, gross (for CLV:CAC) | margin per period x retention / (1 + discount rate - retention) | Constant retention forever: an estimate near the ceiling, not a floor. Use it gross of acquisition cost when comparing with CAC |
| CLV, net | present value of margins - acquisition cost | Already net of CAC: never divide it by CAC (counts CAC twice) |
| Minimum retention | (1 + discount rate) / (1 + target return) | Retention needed to justify the acquisition spend |
| Customer equity | sum of CLV across customers | A north-star candidate for brand-level reporting |
| CLV:CAC | gross CLV / CAC, same group, same horizon | About 3:1 is the common heuristic (subscription businesses); below 1:1 loses money |

Report customer value as floor (realized margin to date), estimate and
ceiling, and say which definition and horizon you used.

## Brand, share and demand

| Metric | Formula | Caveat |
|---|---|---|
| Brand demand | category demand x market share | "Sales are flat" is not a finding: flat can be share loss in a growing category |
| Market share decomposition | penetration share x share of requirements x heavy-usage index | Broad and shallow = a retention problem; narrow and loyal = a reach problem |
| Revenue share vs unit share | brand revenue / category revenue vs brand units / category units | Revenue share above unit share = a price premium |
| Share of voice | brand mentions or ad share / category total | SOV above share of market predicts share gain |
| Seasonal index | ratio to a centred moving average of one season's length | Deseasonalize before reading growth: "+65% raw" can be "+5% real" |
| Frequency, GRP | impressions / reach; GRP = reach% x average frequency | Summing channel reach double-counts people |

## Experiments

| Metric | Formula | Caveat |
|---|---|---|
| Lift | (treatment rate - control rate) / control rate | Report lift with its confidence interval; a large lift on a tiny base is not a large business impact |
| Sample size per arm | about 16 x variance / (minimum detectable effect)^2 | Run whole weeks to cover day-of-week effects |
| Statistical power | 1 - beta | (Some notes write "power = beta": that is wrong) |
| Sample ratio mismatch | observed split vs intended split (chi-square) | A 50/50 test that lands 52/48 on large samples is broken; do not ship |
