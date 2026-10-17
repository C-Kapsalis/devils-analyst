# The questions a report should answer, by discipline

Each question names the comparison or cut that answers it. A dashboard section exists to answer one of these; if a chart answers none, cut it. Paths in parentheses name the Cohortica playbook a definition comes from; the playbooks themselves ship in the `diagnose` skill (`references/playbooks/`). **[std]** marks a standard industry definition added where the playbooks are silent; **GAP** marks what neither covers.


## Web analytics / GA4
1. Which channels earn engaged, buying traffic, not just sessions? -> channel table sorted by sessions, then engagement rate spread vs peers, then revenue per engaged session (web-analytics/ga4-fundamentals.md).
2. Where does on-site value leak? -> chain session -> engaged -> key action -> revenue, cut by channel and by landing page (web-analytics/on-site-funnel.md).
3. Is growth real or bought? -> total revenue vs revenue per user trend (web-analytics/on-site-funnel.md).
4. Which funnel hand-off broke? -> band-to-band transition rates: impressions -> CTR -> engagement -> conversion -> AOV/repeat (web-analytics/marketing-funnel-overview.md).
5. Which channels does last-click under/over-fund? -> last-click vs data-driven credit deltas, with volume threshold check (web-analytics/on-site-funnel.md).
6. What did a campaign earn across every channel? -> group on utm_campaign; sessions/transactions/revenue by channel and by utm_content; disclose coverage (web-analytics/utm-tagging.md).

## SEO / Search Console
1. Are we showing up, and where? -> impressions and position by country and device, scoped to served markets (seo/insight-roadmap.md).
2. Is visibility earning the click? -> CTR vs position per query; buckets snippet rewrite / rank push / leave alone (seo/search-console-queries.md).
3. Is organic acquiring new customers or coasting on brand? -> brand vs non-brand split of clicks and CVR (seo/query-level-data.md; seo/seo-overview.md).
4. Which pages earn vs waste impressions? -> per page by country/device, three stories, drilled to queries (seo/landing-page-performance.md).
5. Does the organic click pay back? -> joined GSC+GA4 per landing page / page group: clicks -> engagement -> conversion (seo/search-console-and-ga4.md).
6. Is the pipeline flowing? -> new pages per month; newly ranking queries; zero-impression sitemap pages (seo/search-console-new-pages.md).
7. What content should we build next? -> paid converters with weak organic rank, grouped by theme (seo/organic-paid-overlap.md).

## Paid search
1. Which transition leaks: showing up, click, payback? -> IS, CTR/CPC vs ceiling, CVR/CPA/ROAS (paid-search/paid-search-overview.md).
2. Where exactly? -> drill service > account > campaign > ad group; cluster overlay by product line (paid-search/account-structure.md).
3. What does generic look like without brand? -> brand vs generic split; 2x2 leakage (paid-search/brand-vs-generic.md).
4. Where is spend wasted? -> cost per sale by match type; zero-conversion search terms clustered by intent (paid-search/match-types-and-wasted-spend.md).
5. Does the click pay back? -> scoped conversions, CPA per campaign vs break-even, revenue and profit ROAS (paid-search/conversions-cpa-and-return.md).
6. Which campaign deserves more budget now? -> pace under plan + strong conversion + high IS lost to budget (paid-search/budget-pacing.md).
7. Is brand spend incremental? -> geo holdout on total conversions (paid-search/brand-vs-generic.md).

## Paid media (PMax, display, video, Demand Gen)
1. Where does the budget go? -> allocation by channel/cluster (paid-media/insight-roadmap.md).
2. Is reach cheap and real? -> CPM, viewable rate, placement report, downstream demand (paid-media/display-advertising.md).
3. Is the creative holding attention? -> cost per view, quartile completion, frequency (paid-media/video-and-youtube.md).
4. Is PMax scaling or buying growth, and is it cannibalizing brand? -> clicks vs CPC by month; one purchase lens; branded vs non-branded conversions (paid-media/performance-max.md).
5. What is each channel's true return? -> measured ROAS on one denominator, then model/holdout (paid-media/true-roas.md).

## Paid social
1. What is each job doing? -> split prospecting vs retargeting (paid-social/paid-social-overview.md).
2. Is prospecting reach healthy? -> CPM, reach, frequency, CTR.
3. Is creative fatiguing? -> frequency vs CTR in the same window.
4. Is retargeting closing efficiently? -> ROAS/CPA on its own.
5. What did the account deliver overall? -> blended conversion count on one attribution window.

## Organic social
1. Is reach growing relative to follower base, and via shares? 2. Is engagement rate above platform median? 3. Which formats earn saves/shares? 4. Is video watched (duration) rather than viewed? 5. Is retargeting CPA on engaged audiences cheaper than cold? (organic-social/organic-social-overview.md).

## Email
1. Is mail reaching the inbox? -> delivery >95%, bounce trend at steady volume, complaints (email-marketing/deliverability-and-inbox-placement.md).
2. Which transition leaks? -> sent -> delivered -> opened -> clicked (email-marketing/reading-the-send-funnel.md).
3. Which send drags engagement? -> per-send CTR vs 2-5%; aggregate CTOR vs ~10% (email-marketing/engagement-and-the-click.md).
4. Is the list growing? -> monthly net list growth sign (email-marketing/list-health-and-reputation.md).
5. What did each send earn? -> sessions/transactions/revenue/revenue per purchaser per campaign key (email-marketing/click-to-revenue.md).

## Customer analytics
1. Did this month's marketing buy good customers? -> month-1 and month-3 repeat at matched age next to spend (customer-analytics/reading-acquisition-quality.md).
2. Is a blended drop real or composition? -> cohort columns + new vs returning mix.
3. How fast does a cohort pay back, and is it stretching? -> cohort payback trend.
4. Are "active" customers eroding? -> order gap and AOV by cohort (customer-analytics/cohort-analysis.md).
5. What is a customer worth? -> floor / estimate / ceiling, by decision horizon (customer-analytics/clv-vs-cac.md).

## Attribution / experiments
1. What did each channel contribute beyond last-click? -> MTA/MMM on the spend-and-outcome table.
2. Did the ad cause sales? -> randomized PSA holdout; lift and incremental conversions.
3. Where does it work? -> segment lift by day, device, frequency band, with significance (attribution-experiments/*).

## GEO / LLM
1. Is the share growing? -> LLM sessions / total by month. 2. Which pages are cited, and who entered/dropped? 3. Does it engage and convert vs organic baseline? 4. Is branded demand rising faster than non-branded? (emerging/*).

## Competitive research
1. Which demand is worth chasing? -> intent depth x volume x competition x current rank. 2. Where is the gap? -> impressions without clicks; terms competitors own. 3. Are we investing enough in visibility? -> share of voice vs share of market (competitive-research/competitive-and-keyword-research.md). Personas: does an audience matching the profile convert and repeat? (competitive-research/marketing-personas.md).
