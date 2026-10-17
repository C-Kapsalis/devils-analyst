# Insight patterns

"If you see X, it usually means Y; check Z." About seventy recurring readings from the playbooks, by discipline. Use them to propose a likely cause, then confirm it in the data before writing it as a finding. Paths in parentheses name the Cohortica playbook a definition comes from; the playbooks themselves ship in the `diagnose` skill (`references/playbooks/`). **[std]** marks a standard industry definition added where the playbooks are silent; **GAP** marks what neither covers.


## Web / on-site
- Huge sessions, engagement rate far below peers -> "attention that evaporates on arrival"; fix creative, targeting or landing page, not more traffic (web-analytics/ga4-fundamentals.md).
- Engagement rate collapsed MoM -> traffic-mix change, landing-page change, or tagging change, "in that order" (web-analytics/ga4-fundamentals.md).
- High sessions, low engagement -> "a landing-page or intent-match problem, not a traffic problem" (web-analytics/on-site-funnel.md).
- Long duration with pages/visit near 1.0 -> "people are stuck, not absorbed" (web-analytics/on-site-funnel.md).
- Total revenue up, revenue per user down -> "you bought growth" (web-analytics/on-site-funnel.md).
- Site CVR fell 2.4% -> 2.1% -> refuse the blend; check mix shift by channel and named action (web-analytics/on-site-funnel.md).
- Channel gains big credit under DDA vs last-click -> contributes along the path but rarely lands last; check volume threshold (web-analytics/on-site-funnel.md).
- Traffic up 30%, revenue flat -> walk hand-offs; locate the first transition that broke (web-analytics/marketing-funnel-overview.md).
- Plenty of impressions with low CTR -> "a message problem no extra budget fixes" (web-analytics/marketing-funnel-overview.md).
- Direct spiked after a campaign -> untagged links first, not brand lift (web-analytics/utm-tagging.md).
- Paid social engagement fine, conversion zero -> checkout or offer; bounces on every page -> buying the wrong audience, pull spend (web-analytics/on-site-funnel.md).

## SEO
- Soft CTR at strong position -> title/snippet problem; soft CTR at position 12 -> ranking problem (seo/insight-roadmap.md).
- Top-3 query with ~1% CTR -> cheapest win; rewrite title/meta, not links (seo/search-console-queries.md).
- Great CTR, no conversion -> landing page/intent match, not ranking (seo/insight-roadmap.md).
- Clicks fine, engagement low -> content/UX; engagement fine, conversion near zero -> CRO window; high conversion, low sessions -> starved winner, feed it (seo/search-console-and-ga4.md).
- Blog post with big impressions on commercial term -> drill queries; thin explainer can't close; point the right page at the intent (seo/landing-page-performance.md).
- Low CTR page -> drill to queries: own intent = snippet; other page's intent or sibling = cannibalization/mismatch (seo/search-console-landing-pages.md).
- One query, two of your URLs -> cannibalization; consolidate (seo/query-level-data.md).
- Organic sessions declining with no ranking losses -> zero-click compression; check impressions vs clicks and AI-referral stream (emerging/llm-traffic-and-organic-search.md).
- Steady clicks, no new pages/queries underneath -> "coasting toward decline" (seo/new-and-newly-ranking-pages.md).
- Clicks growing faster than impressions -> CTR improving, not just visibility (seo/seo-overview.md).
- New page with high impressions at pos 27 from browsing queries -> awareness churn; note it, do not fund (seo/new-and-newly-ranking-pages.md).
- Existing page newly ranking for new query -> deepen, not a rival page (seo/new-and-newly-ranking-pages.md).
- Query converts well in paid, organic absent/20+ -> content bet; 4-20 -> leverage zone; 1-3 -> "why still paying?" test the bid (seo/organic-paid-overlap.md).
- Organic traffic drop -> split country/device, then position drop vs CTR drop at stable position, then brand vs non-brand (seo/seo-overview.md).

## Paid search
- Healthy blended CTR, cheap CPC -> may be pure brand halo hiding a bleeding generic program (paid-search/brand-vs-generic.md).
- Generic campaign looks brilliant -> check forward leakage of brand queries (paid-search/brand-vs-generic.md).
- Spectacular CVR, CPA of pennies -> micro-conversions scoped; re-read on purchases (paid-search/conversions-cpa-and-return.md).
- Strong CTR, weak conversion -> landing page: message match, speed, checkout friction (paid-search/conversions-cpa-and-return.md).
- Low impression share -> split rank vs budget before acting (paid-search/impression-share-and-quality-score.md).
- Converting campaign with high IS lost to budget -> "the clearest raise-the-cap signal" (paid-search/budget-pacing.md).
- 34% spent on the 20th -> serious under-pace, likely capped winners (paid-search/budget-pacing.md).
- Uncapped generic over budget at poor CPA while brand campaign pinned at cap -> fix caps before keywords (paid-search/account-structure.md).
- Rising CPC on core terms -> crowding auctions; look for competitor terms where you have zero IS (competitive-research/competitive-and-keyword-research.md).
- Mobile cheap CPC -> compute value: 2x CPC at half CVR = ~1/4 desktop value (paid-search/device-and-timing.md).
- Bid modifier did nothing -> automated bidding (paid-search/device-and-timing.md).
- Account "up 20% on conversions" -> check scoping, brand leakage, concentration in one branch (paid-search/insight-roadmap.md).

## Paid media / social
- Clicks up with rising CPC -> bought growth; check conversions keep pace (paid-media/auditing-pmax.md).
- PMax 6x ROAS -> apply purchase lens, check branded overlap, clicks vs CPC (paid-media/performance-max.md).
- Lowest CPM and biggest budget -> interrogate viewability, MFA placements, downstream demand (paid-media/display-advertising.md).
- Rising cost of reach or falling engagement at flat spend -> creative fatigue; refresh cadence (paid-media/demand-gen.md).
- Quartile cliff after first 25% -> hook past skip button (paid-media/video-and-youtube.md).
- Retargeting 5-6x, prospecting <1x -> don't shift; retargeting harvests prospecting's demand (paid-social/paid-social-overview.md; paid-media/display-advertising.md).
- Frequency climbing + CTR falling -> creative burnout, rotate before raising budget (paid-social/paid-social-overview.md).
- Rising CPC with steady CTR -> auction competition (paid-social/paid-social-overview.md).
- Rising CPM at flat reach -> audience too narrow or creative fatiguing (paid-social/paid-social-overview.md).
- Meta conversions > GA4 -> likely view-through on Meta's window (hypothesis until the account's attribution setting is checked); set one window (paid-social/paid-social-overview.md).
- Display worst on last-click ROAS -> floor lowest for upper funnel; model or holdout before cutting (paid-media/true-roas.md).
- Platforms' ROAS sum exceeds finance revenue -> double-counting; one shared denominator (paid-media/true-roas.md).

## Email
- Healthy opens, flat revenue -> walk delivery, CTR, on-site conversion, net list growth (email-marketing/email-marketing-overview.md).
- Fine CTOR, low CTR -> sent too broadly; narrow audience, don't rewrite (email-marketing/engagement-and-the-click.md).
- Opens steady, clicks halved -> offer, CTA, subject over-promise, broadened segment (email-marketing/reading-the-send-funnel.md).
- Bounce rate rising at steady volume -> lapsed hygiene, before delivery falls (email-marketing/deliverability-and-inbox-placement.md).
- Complaints past 0.1% -> consent/frequency; cut volume (email-marketing/email-marketing-overview.md).
- Best-clicking send earned least -> low-intent volume; check revenue per purchaser and page match (email-marketing/click-to-revenue.md).
- Clicks but zero revenue -> instrumentation first (untagged links) (email-marketing/click-to-revenue.md).
- Sessions far below clicks on one send -> broken or untagged link (email-marketing/click-to-revenue.md).
- All campaign metrics stable for a year -> check net list growth sign (email-marketing/list-health-and-reputation.md).

## Customer analytics
- Blended repeat rate fell -> composition trap; re-read at matched age plus new vs returning mix (customer-analytics/reading-acquisition-quality.md).
- December cohort retains worse -> seasonality; compare to last December (customer-analytics/reading-acquisition-quality.md).
- Payback stretching 3 -> 6 months -> growth bought at quality's expense (customer-analytics/reading-acquisition-quality.md).
- 80% still active -> pulse not flow; check order gap and basket size (customer-analytics/cohort-analysis.md).
- Decline shapes: seasonal recurring quiet / stop after refund or ticket = experience problem / steady erosion with no incident = competitor / hard stop = goodbye (customer-analytics/cohort-analysis.md).
- LTV €340 on dashboard -> ask churn model, horizon, discounting; place between floor and ceiling (customer-analytics/clv-vs-cac.md).
- Two LTVs 3x apart -> likely different horizons/decisions (customer-analytics/clv-vs-cac.md).

## Attribution / GEO
- Viewers 20% vs non-viewers 9% -> proves targeting, not effect (attribution-experiments/controlled-experiments.md).
- Model contradicts holdouts -> miscalibrated (attribution-experiments/attribution-and-mmm.md).
- LLM traffic converts below organic baseline -> answer set an expectation the page doesn't meet; fix page (emerging/llm-traffic-and-organic-search.md).
- Page drops out of LLM cited set while organic holds -> competitor displaced you in answers (emerging/measuring-llm-traffic-in-ga4.md).
- Named in AI answers, no traffic lift -> zero-click by design; watch branded demand (emerging/geo-getting-cited-in-ai-answers.md).

## Pricing and promotions (from the author's notes)

- Falling baseline sales with rising promo lift -> customers learning to wait for deals, not better promotions; check baseline trend, full-price share, time to repeat.
- More than ~40% of revenue on promotion -> training deal-seekers; check repeat rate at full price by cohort.
- Promotion lifted units -> not yet a win; net out margin cost, pull-forward (post-promo dip) and repeat.
- Price up and revenue up, or price down and revenue down -> demand is inelastic; test whether price is below its profit optimum.
- Loss-leader item with negative margin -> judge its spillover (traffic, basket) before cutting it.

## Demand, share and loyalty (from the author's notes)

- Flat sales -> decompose into category demand x share first; flat can hide share loss in a growing category.
- Small brand repeats less than the leader -> expected (double jeopardy), not evidence of a weaker product.
- Loyalty-programme members repeat more -> mostly buyers who would have stayed anyway; growth comes from penetration.
- High aided awareness, low unaided -> a salience problem, not a reach problem.
- Raw "+65%" jump -> deseasonalize first; it may be "+5% real".
- Worst segment improves right after you intervene -> regression to the mean; check against a control or the segment's own history.

## Attribution and experiments (from the author's notes)

- Channel worthless on last-click, strong on first-click -> an introducer, not a closer; compare models, then run a holdout.
- Frequency vs lift is an inverted U -> check lift by frequency band before raising frequency caps.
- A/B split drifts from the intended ratio -> sample ratio mismatch; do not ship, check assignment and logging.
- Big early lift that fades -> novelty effect; split new vs returning users.
- Metric moved right after a tracking change -> instrumentation, not customers.
- Direct traffic spikes -> tagging first; a sustained high direct share can be brand strength.
- New/returning user ratio falling sharply -> acquisition is falling behind.
- Branded searches climb the week after AI-answer mentions -> the closest thing to a GEO scoreboard.
