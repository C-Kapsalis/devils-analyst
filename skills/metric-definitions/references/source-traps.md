# Source-data traps by platform

What each platform's export does that makes a correct-looking number wrong. Check these before computing. Paths in parentheses name the Cohortica playbook a definition comes from; the playbooks themselves ship in the `diagnose` skill (`references/playbooks/`). **[std]** marks a standard industry definition added where the playbooks are silent; **GAP** marks what neither covers.


## GA4
- Engagement definition: engaged = >10s, 2+ pageviews, or key action; one-page sites score high structurally (web-analytics/on-site-funnel.md).
- No cost data: cannot compute ROI from GA4 alone (web-analytics/ga4-fundamentals.md).
- Data-driven attribution silently falls back to last-click below ~400 conversions per type per 28 days (web-analytics/on-site-funnel.md).
- Sessions are counted after consent banners and blockers take their cut, so they run below GSC clicks (seo/query-level-data.md; seo/search-console-and-ga4.md). Consent mode itself is not discussed further.
- Untagged links land in "direct"; tagging drift makes revenue nameless (web-analytics/utm-tagging.md; email-marketing/click-to-revenue.md).
- AI referrers do not always land in the expected field: check both source and medium; use contains-matching, re-verify quarterly (emerging/measuring-llm-traffic-in-ga4.md).
- Blended conversion rate moves with channel mix (web-analytics/on-site-funnel.md).
- GAP: sampling, thresholding, `(not set)`, users-not-additive are not covered by the playbooks. [std] GA4 user counts are distinct counts and do not sum across dimensions/date ranges; Explorations can sample; Google Signals/data thresholds can withhold rows; `(not set)` indicates missing dimension values.

## Search Console
- Lags two to three days; samples the long tail; reports queries, not people (seo/seo-overview.md; seo/landing-page-performance.md).
- Query-page rows double-count demand when two of your pages appear (seo/query-level-data.md).
- Average position is impression-weighted and the topmost rank per search; hides distribution and a weaker second page (seo/query-level-data.md).
- Literal strings fragment one intent into variants (seo/query-level-data.md).
- Clicks never reconcile with GA4 sessions: different systems, different sides of the click; read shape, never sum (seo/organic-and-on-site-behaviour.md).
- Never volunteers zero-impression pages; bring the sitemap (seo/search-console-landing-pages.md).
- No conversion column; borrow paid CVR as theoretical CVR (seo/query-level-data.md).
- Position at low volume swings with location/device/personalization (seo/new-and-newly-ranking-pages.md).
- [std] GSC also omits anonymized (rare) queries from query tables, so query totals sum to less than property totals. Not stated in the playbooks beyond "samples the long tail."

## Google Ads / Microsoft Ads
- Search-terms report: since 2020 only terms searched by significant numbers; visibility of click-driving queries fell from ~75-85% to ~40-60%. A strong sample, not a census; use campaign/ad-group levels for spend decisions (paid-search/account-structure.md; paid-search/query-performance.md).
- Impression share is bucketed at <10% and >90% (paid-search/impression-share-and-quality-score.md).
- Daily spend can hit 2x average daily budget; only monthly cap = daily budget x 30.4 (paid-search/budget-pacing.md).
- Conversion scoping: default columns may blend micro-conversions with sales (paid-search/conversions-cpa-and-return.md).
- Device/schedule modifiers are advisory under automated bidding (paid-search/device-and-timing.md).
- Geo data can pool to one organization-level row ("one number wearing a map") (paid-search/device-and-timing.md).
- Google vs Microsoft comparisons need consistently defined metrics, not exports with mismatched conversion scoping (paid-search/account-structure.md).
- Last-click ROAS credits the paid click with the whole sale (paid-search/conversions-cpa-and-return.md).
- GAP: conversion lag (late-arriving conversions in recent days) is not discussed. [std] Recent-day CPA/ROAS in Ads is understated until conversions mature.

## Performance Max
- Asset groups report as one `performance_max` pseudo ad group; no keywords; limited search-terms report; blended across seven inventory types (paid-media/auditing-pmax.md; paid-media/performance-max.md).
- Filter on the type enum, not names (paid-media/auditing-pmax.md).
- Blank conversion columns can be legitimate sparsity (paid-media/auditing-pmax.md).
- Absorbs branded/high-intent credit (paid-media/performance-max.md).

## Display / Video / Demand Gen
- Served impressions are not viewable impressions; bots/MFA inventory (paid-media/display-advertising.md).
- View-through and incremental effect are not handed over cleanly (paid-media/video-and-youtube.md).
- Demand Gen asset/audience attribution "often not cleanly in the data": treat as unanswered (paid-media/demand-gen.md).
- No search-terms report in Demand Gen (paid-media/demand-gen.md).

## Meta / paid social
- Meta can count view-through conversions on its own attribution window (the default includes 1-day view); reports more than analytics confirms; unless the export shows the window, name this as a likely cause, not a fact; set one window (paid-social/paid-social-overview.md).
- Incidental taps inflate CTR; filter to link clicks (paid-social/paid-social-overview.md).

## Cross-platform revenue
- Platform ROAS figures cannot be stacked; the same sale is claimed twice (paid-media/true-roas.md).
- Use one shared denominator (own analytics' recorded value), joined by campaign name; inconsistent naming silently breaks the join (paid-media/true-roas.md; attribution-experiments/attribution-and-mmm.md).
- Platform self-reported conversions "poison" MMM input (attribution-experiments/attribution-and-mmm.md).
- Finance-side backend revenue vs platform: "finance says total revenue does not support either" (paid-media/true-roas.md). Backend/order-system reconciliation beyond that is a GAP.

## Email platform
- Opens fire on previews and image loads; privacy features mask opens; directional only (email-marketing/reading-the-send-funnel.md; email-marketing-overview.md). [std] Apple Mail Privacy Protection pre-fetches images, inflating opens ("machine opens").
- The click is the last thing the platform sees; revenue lives in web analytics (email-marketing/click-to-revenue.md).
- Per-send rates only measure who is left on the list (composition trap) (email-marketing/list-health-and-reputation.md).
- Blended dormant/win-back segments hide true bounce/complaint rates (email-marketing/deliverability-and-inbox-placement.md).

## Organic social
- Last-click revenue on posts is "the trap itself" (organic-social/organic-social-overview.md).

## LLM / AI
- Zero-click exposure produces no session at all; referral traffic undercounts the channel (emerging/geo-getting-cited-in-ai-answers.md).
- Referrer lists go stale (emerging/measuring-llm-traffic-in-ga4.md).

## Customer data
- Silence is ambiguous in non-subscription businesses; LTV is "a guess about silence" (customer-analytics/clv-vs-cac.md).
- Never average measured and modeled lifetimes into one number (customer-analytics/cohort-analysis.md).
- December cohorts are gift-driven; compare to last December (customer-analytics/reading-acquisition-quality.md).

## Additions and corrections

From the author's notes, checked against current platform behaviour. **[std]**
marks standard facts added to fill gaps or correct outdated notes.

### GA4

- **Recent data is provisional.** Only the Realtime report is near-live;
  standard reports keep processing for roughly 24-48 hours **[std]**. Treat the
  last one or two days as provisional.
- **Sessions in GA4** end after 30 minutes of inactivity by default; unlike
  Universal Analytics, they do **not** restart at midnight or when the campaign
  changes **[std]**. Do not apply UA session rules or UA bounce-rate
  benchmarks to GA4.
- **Bounce rate in GA4** = 1 - engagement rate (non-engaged sessions /
  sessions).
- **Thresholding** withholds rows with small user counts when Google Signals or
  demographics are enabled **[std]**.
- **`(not set)`** usually means a missing value: a lost session start, an
  unpopulated dimension, or a dimension and metric of different scopes **[std]**.
- **Data retention** (2 or 14 months) limits Explorations and user-level data,
  not standard aggregated reports **[std]**.
- **Users** are identified by device or cookie ID, user ID and Google Signals,
  not by IP address **[std]**.
- **Data-driven attribution eligibility** has changed over time (the notes cite
  400+ conversions per type in 30 days plus about 10,000 multi-touch paths; the
  playbooks cite about 400 per 28 days). Check current Google documentation
  before stating a threshold.
- **Name the attribution model** (data-driven, last click) in every chart that
  splits conversions or revenue by channel. Same data, different model,
  opposite budget advice.

### Direct traffic

A sustained high share of direct traffic can reflect brand recognition
(bookmarks, typed URLs, apps). A **sudden spike** in direct is a tagging
problem until proven otherwise: untagged email, social and display links land
there.

### Email

- **Machine opens**: Apple Mail Privacy Protection and similar features
  pre-load images, so opens fire without a person **[std]**.
- **Bot clicks**: corporate security scanners pre-click links, inflating CTR on
  B2B lists, often within seconds of delivery **[std]**. Watch for clicks on
  every link of a message at the same second.

### Ad platforms

- **Video viewability** (MRC): at least 50% of pixels in view for at least 2
  continuous seconds; display: 1 second.
- **Conversion lag**: recent days' conversions keep arriving; Google Ads
  reports conversions on the click (interaction) date by default **[std]**.

### Revenue truth

Three views of revenue, in order of authority **[std]**:

1. **The order system** (Shopify, the backend, finance): what was sold, net of
   refunds and cancellations.
2. **Web analytics** (GA4): the attribution layer, losing purchases to ad
   blockers, consent and broken tags.
3. **Ad platforms**: each platform's claim, on its own attribution window,
   overlapping with the others.

Before comparing them, align: refunds and cancellations, tax and shipping,
currency, order date vs click date, and test orders.

### Benchmarks

Benchmarks differ by source and year (organic social engagement medians fell
across platforms between reports). Quote a benchmark only with its source and
year, as a heuristic, never as a target.
