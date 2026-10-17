# Connector query research for Devil's Analyst (as of 2026-10-17)

**Scope.** For each connector: who makes it and where it runs, the tool parameters that decide grain, attribution, uniqueness and limits, the mistakes it invites with the correct request, and what it cannot provide.

**How to read it.**
- Every claim cites the page it was read from.
- **(unverified)** marks claims from secondary sources, or ones I could not confirm.
- "Observed in session" means the connector appeared in this Claude Code session's tool list: the claude.ai HubSpot connector, and the marketing-plugin MCPs for HubSpot, Klaviyo, Amplitude, Supermetrics, Close and Salesforce, plus the data-plugin BigQuery MCP. That shows each exists as a Claude connector or plugin entry. I did not inspect those tool schemas beyond their names.

**Directory status.** I could not read the official Claude connectors directory or the ChatGPT app/plugin directory directly. Secondary sources say OpenAI renamed the ChatGPT App Directory to a "Plugin Directory" in July 2026 (unverified; https://www.moburst.com/blog/chatgpt-app-directory-explained-what-brands-need-to-know/). Where a connector says "Claude / ChatGPT", that comes from the vendor's own page.

---

## 1. Ad platforms

### Google Ads: `googleads/google-ads-mcp` (official, Google Ads API team)
- **Where it runs:** a generic MCP server that you host yourself (local, or deployed to Cloud Run). It is read-only, and there is no Google-hosted endpoint (hosting and Cloud Run from secondary coverage, unverified: https://adkit.so/resources/google-ads-mcp).
- **Prerequisites:** a developer token with at least Explorer access, OAuth or ADC with the `adwords` scope, and an optional `login_customer_id` for manager (MCC) access. Source: https://github.com/googleads/google-ads-mcp
- **Tools:**
  - `list_accessible_customers`
  - `get_resource_metadata`: shows the fields a resource can select.
  - `search(customer_id, fields[], resource, conditions[], orderings[], limit, login_customer_id)`
  - Source: https://raw.githubusercontent.com/googleads/google-ads-mcp/main/ads_mcp/tools/search.py
- **How `search` works:**
  - **No raw query:** it does not take a raw GAQL string. It builds `SELECT fields FROM resource WHERE conditions AND ... ORDER BY ... LIMIT` itself.
  - **Customer ID:** digits only.
  - **Field names:** fully qualified, such as `campaign.id`.
  - **Dates:** `YYYY-MM-DD`, and every date range needs both a start and an end.
  - **Paging:** it reads every `search_stream` batch, so there is no paging and every row is returned in one list. A broad query can flood the context window.
  - **Annotation:** `readOnlyHint=True`.
- **What decides grain:**
  - The `FROM` resource sets the base grain: "Every report is initially segmented by the resource specified in the FROM clause". Each segment you add multiplies the row count. Any `segments.date/week/month/quarter/year` in SELECT requires a finite date range in WHERE. Source: https://developers.google.com/google-ads/api/docs/reporting/segmentation
  - Selecting any `segments.keyword.*` field "restricts the results to only those rows directly associated with a Search Network keyword", which silently drops DSA, Shopping and PMax data (same page).
  - Performance Max has no ad groups: "querying resources such as `ad_group` or `ad_group_ad` won't return any data for your Performance Max campaigns". Use `campaign`, `asset_group`, `asset_group_asset` or `campaign_search_term_view`. Source: https://developers.google.com/google-ads/api/docs/performance-max/reporting
- **Mistakes and correct requests:**
  - **Conversions:**
    - `metrics.conversions` counts only actions with `include_in_conversions_metric=true`, the primary actions that bidding uses.
    - `metrics.all_conversions` "includes all conversions regardless of" that flag: secondary actions, store visits, calls and so on.
    - Report CPA and ROAS on `conversions`/`conversions_value`, unless the client has defined the KPI as a specific action.
    - Source: https://developers.google.com/google-ads/api/reference/rpc/v22/Metrics
  - **Specific action:**
    - Add `segments.conversion_action` (or `segments.conversion_action_name`) and filter on it.
    - This "changes the granularity of the query results to one row per conversion action per campaign", and "rows with zero conversions are excluded". Cost and clicks are not repeated per action, so pull spend in a **separate query without the conversion-action segment** and join them.
    - Source: https://developers.google.com/google-ads/api/docs/conversions/reporting
  - **Conversion date vs click date:**
    - `conversions` together with `segments.date` is dated by **interaction (click) date**, so recent days keep filling in.
    - `metrics.conversions_by_conversion_date` and `all_conversions_by_conversion_date` date by conversion time. Pick one and say which.
    - Recent data "isn't available instantly".
    - Sources: same conversions page; https://developers.google.com/google-ads/api/reference/rpc/v22/Metrics
  - **Money:**
    - `metrics.cost_micros` divided by 1,000,000 gives account currency ("one million is equivalent to one currency unit"). Source: https://developers.google.com/google-ads/api/reference/rpc/v24/SuggestSmartCampaignBudgetOptionsResponse.BudgetOption
    - The currency is the account's own (`customer.currency_code`), so do not sum across MCC children in different currencies. The currency field is my inference (unverified).
  - **Non-additive metrics:** don't sum or average `search_impression_share`, `ctr` or `average_cpc` across rows. Re-derive them from components; impression share can't be re-derived.
  - **Lookback:** granular date segments allow up to 37 months (segmentation page).
- **Cannot:** write changes, Keyword Planner volumes (no tool in the official server; unverified), GA4-side conversions unless imported, or any user-level data.

### Meta (Facebook/Instagram) Ads
**Official: Meta Ads AI Connectors MCP (Meta, open beta since 2026-04-29)**
- **Where it runs:** remote at `https://mcp.facebook.com/ads`. Add it in Claude as a custom connector. Meta says it is compatible with Claude and ChatGPT.
- **Tools:** 29 in total. The 7 insights tools are `ads_insights_advertiser_context`, `ads_insights_anomaly_signal`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_industry_benchmark`, `ads_insights_performance_trend`, `ads_get_opportunity_score` and `ads_get_help_article`.
- **Scopes:** read-only, read/write and financial tiers. There are no per-tool toggles.
- **Created objects start PAUSED.**
- **Parameters:** not published. I could not verify whether its tools expose `level`, `time_increment` or `action_attribution_windows` (unverified).
- **Sources:** https://mcp.directory/blog/meta-ads-cli-mcp, https://ppc.land/meta-opens-its-ad-system-to-claude-and-chatgpt-with-new-ai-connectors/
- **Companion CLI** (`meta ads insights get`), which shows Meta's intended defaults:
  - Default `--date-preset last_30d`.
  - Default `--time-increment all_days` (also `daily`, `weekly`, `monthly`).
  - Default fields `spend, impressions, clicks, ctr, cpc, reach`.
  - Default `--limit 50`.
  - Account level unless you filter by campaign, ad set or ad.
  - Source: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/insights

**Community: `pipeboard-co/meta-ads-mcp` (popular; hosted Pipeboard or self-run)**
- **Tool:** `get_insights(object_id, time_range="maximum", breakdown, level="ad", limit=25, after, action_attribution_windows, action_breakdowns, compact)`.
- **No `time_increment` parameter**, so you can't get daily rows from it.
- **Defaults are dangerous:** level is `ad` and the time range is `maximum`. Set `level` and `time_range` on every call.
- **Paging:** `limit` 25 with an `after` cursor. Page until `paging.next` is absent.
- **Attribution value:** the docstring says "The 'value' field always shows 7d_click". Read the per-window keys when you pass `action_attribution_windows`.
- **Source:** https://raw.githubusercontent.com/pipeboard-co/meta-ads-mcp/main/meta_ads_mcp/core/insights.py

**Underlying Insights API rules** (apply to every Meta connector, including Supermetrics, Windsor and the rest):
- `time_increment` defaults to `all_days` ("one result set for the whole period"). `1` gives daily, `monthly` gives months. `date_preset` defaults to `last_30d`. `level` is ad, adset, campaign or account. `action_breakdowns` defaults to `["action_type"]`.
  - `use_unified_attribution_setting=true` gives the "same behavior as in the Ads Manager".
  - `action_report_time` is impression, conversion, mixed or lifetime.
  - Totals go back 37 months.
  - Source: https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/
- **Attribution windows from 2026-01-12:** `7d_view` and `28d_view` "will no longer be returned".
  - Still available: 1d_click, 7d_click, 28d_click, 1d_ev (engaged view) and 1d_view.
  - Unique-count fields with any breakdown are limited to 13 months, and so are hourly breakdowns. `frequency_value` is limited to 6 months.
  - Source: https://developers.facebook.com/blog/post/2025/10/16/ads-insights-api-metric-availability-updates/
  - Windsor's MCP docs still show `{"attribution_window": "7d_view,1d_click"}` as their example, so don't copy it.

**Mistakes and correct requests (Meta):**
- **Reach and frequency are deduplicated people counts.** For period reach, request `level=<the grain you report>`, `time_increment=all_days` and the exact period. Never sum daily reach, or reach across ad sets or campaigns. Account-level reach needs `level=account`.
- **Conversions:**
  - Request `actions` and `action_values` with explicit `action_attribution_windows` (e.g. `["7d_click","1d_view"]`), or `use_unified_attribution_setting=true` to match Ads Manager.
  - Then pick **one** `action_type` (e.g. `offsite_conversion.fb_pixel_purchase` or `omni_purchase`). Don't add `purchase`, `omni_purchase` and `offsite_conversion.*` together: they are overlapping views of the same events. Pipeboard's `compact` exists to strip those duplicates.
- **ROAS:** compute `action_values[purchase] / spend` from one consistent action type and window, or read `purchase_roas` with the same window.
- **Breakdowns:** sum only additive metrics across breakdown rows. `impression_device` can't be used alone. `platform_position` requires `publisher_platform`.

**Cannot:** user-level data, view-through beyond 1 day, modelled conversions split from observed (unverified), or cross-channel dedup.

### Microsoft Ads, LinkedIn Ads, TikTok Ads, Amazon Ads
See section 1b below (from the sub-research).

---

## 2. Web and app analytics

### GA4: `googleanalytics/google-analytics-mcp` ("analytics-mcp", official, Google)
- **Where it runs:** a local generic MCP server (pipx or ADC). Read-only.
- **Tools:** `get_account_summaries`, `get_property_details`, `list_google_ads_links`, `run_report`, `run_funnel_report`, `get_custom_dimensions_and_metrics` and `run_realtime_report`. Source: https://github.com/googleanalytics/google-analytics-mcp
- **`run_report` parameters:** `property_id`, `date_ranges[]`, `dimensions[]`, `metrics[]`, `dimension_filter`, `metric_filter`, `order_bys`, `limit` (≤250,000), `offset`, `currency_code` (defaults to the property currency) and `return_property_quota`.
  - Field names are **snake_case** protobuf names, not the camelCase in the docs.
  - Source: https://raw.githubusercontent.com/googleanalytics/google-analytics-mcp/main/analytics_mcp/tools/reporting/core.py
- **API behaviour:**
  - Default limit is 10,000 rows, max 250,000 per request. Page with `offset`.
  - `keepEmptyRows=false` by default, so zero rows are dropped. Not exposed by the MCP (unverified).
  - Source: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
  - Response metadata:
    - `samplingMetadatas`: present only if the report was sampled.
    - `subjectToThresholding`: small-user rows are hidden.
    - `dataLossFromOtherRow`: values were rolled into "(other)".
    - `currencyCode` and `timeZone`.
    - Source: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/ResponseMetaData
- **Mistakes and correct requests:**
  - **User counts are not additive across days or dimensions.**
    - `totalUsers` ("distinct users who have logged at least one event"), `activeUsers` and `sessions` are HLL++ approximations, and "totals across dimensions may not add up". Source: https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations
    - For monthly users, request `dimensions=["year_month"]` with the month range, or no date dimension with an exact range. Never sum `date` rows.
    - For the period total, run a separate request without the breakdown dimension.
  - **Revenue:**
    - `purchaseRevenue` is purchases minus refunds.
    - `totalRevenue` is purchases, subscriptions and ads, minus refunds.
    - Name which one you use. Use `currency_code` explicitly when comparing to ads cost.
    - Source: https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
  - **Conversions:**
    - Use `keyEvents`, optionally with `dimensions=["event_name"]` and a filter on the specific key event. Unfiltered `keyEvents` sums every key event.
    - "Marking an event as key only affects reports from that point forward" (api-schema).
  - **Channel scope:** `sessionDefaultChannelGroup` (session-scoped, "based primarily on source and medium") vs `firstUserDefaultChannelGroup` (the channel that "first acquired the user"). Don't mix user-scoped and session-scoped dimensions in one report.
  - **More dimensions mean fewer events counted:** "only events with data for every requested dimension are included" (data-expectations page). So a high-cardinality breakdown can understate totals.
  - **Check metadata** for sampling, thresholding and "(other)" before quoting numbers. Thresholding (Google Signals) hides small segments.
  - **Recent data** may shift while it is still being processed.
- **Cannot:** user-level or row-level data (use the BigQuery export), exact unique counts (HLL), cost data for non-Google channels, or unsampled results guaranteed on standard properties (unverified).

### Amplitude, Mixpanel
See section 2b below.

---

## 3. Search

### Google Search Console: no official Google MCP found
- **Most cited community server:** `ahonn/mcp-server-gsc` (npx, service account).
  - **Tools:**
    - `list_sites`
    - `search_analytics(siteUrl, startDate, endDate, dimensions, type, aggregationType, rowLimit, pageFilter, queryFilter, countryFilter, deviceFilter, filterOperator, regexFilter)`
    - `enhanced_search_analytics`
    - `detect_quick_wins`
    - `index_inspect`
    - `list_sitemaps`
  - Its README mentions `dataState` (default `final`), but the schema doesn't list it, and **`startRow` is not exposed**. Source: https://glama.ai/mcp/servers/@ahonn/mcp-server-gsc
  - Other options are hosted vendor servers, such as Scalably (read-only, 5 tools). Many low-adoption forks exist (unverified).
- **Underlying API rules** (https://developers.google.com/webmaster-tools/v1/searchanalytics/query):
  - `type` defaults to `web`. `discover`, `googleNews`, `news`, `image` and `video` are separate.
  - `dataState` defaults to final. `all` adds fresh (preliminary) data. `hourly_all` goes with the HOUR dimension.
  - `aggregationType`: auto, byPage or byProperty.
  - `rowLimit` is 1–25,000 (default 1,000). `startRow` pages through results.
  - Results are sorted by clicks descending, and "does not guarantee to return all data rows but rather top ones".
- **Data limits:** at most "50K rows of data per day per search type". Grouping by page and/or query "can cause data loss", so omit those dimensions for accurate totals. To paginate, step `startRow` by 25,000 until zero rows come back. Source: https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data
- **Property vs page aggregation:** the chart aggregates by property, where two results from one site count as one impression. Query, country, device and date tables are by property. Page and search-appearance tables are by page. "The chart totals can sometimes differ from the table totals." Chart position is the site's top result. Fresh data "might change in the next few hours". Source: https://support.google.com/webmasters/answer/7576553
- **Mistakes and correct requests:**
  - **Site totals** (clicks, impressions, CTR, position): request with **no** query or page dimension (optionally `date`), and set `type=web` explicitly. Never sum query rows to get site clicks, because anonymized and long-tail queries are dropped.
  - **Position:** impression-weighted, so never take a plain average of row positions. Weight by impressions, or take it from the aggregate request.
  - **Page vs query analyses:** don't compare a page-dimension total with a query-dimension total. They use different aggregation and truncation.
  - **Over 25k rows:** loop `startRow`. With ahonn's server you can't, so narrow with filters or date slices and state the truncation.
  - **Freshness:** for "last N days", either keep `final` (and mention the roughly 2–3 day lag; lag is unverified) or set `all` and label recent days preliminary.
  - **Site URL format:** `sc-domain:example.com` vs `https://www.example.com/` gives different property scopes.
- **Cannot:** query-level data for anonymized queries, more than 50k rows per day per type, conversions or revenue, or exact match to GA4 sessions.

---

## 4. Aggregators (multi-source)

### Supermetrics MCP ("SuperMCP", official, Supermetrics)
- **Where it runs:** remote at `mcp.supermetrics.com`, with OAuth. Also a Claude marketing-plugin connector (observed in session), a Microsoft Power Platform connector, and generic MCP. Needs a subscription with API access. Sources: https://docs.supermetrics.com/docs/supermetrics-mcp-server, https://learn.microsoft.com/en-us/connectors/supermcp
- **Tools:**
  - `data_source_discovery`
  - `accounts_discovery(ds_id)`
  - `field_discovery(ds_id, field_type)`
  - `data_query(ds_id, ds_accounts[], fields[], date_range_type, start_date, end_date, timezone, filters, settings, compare_type, compare_show, ...)`: returns a `schedule_id`.
  - `get_async_query_results(schedule_id)`
  - `get_today`
  - Throttle: 100 calls per 60 s per connection.
  - Source: https://learn.microsoft.com/en-us/connectors/supermcp
- **Traps:**
  - **Timezone:** `timezone` defaults to **UTC** (an ad account in another timezone will be shifted), so pass the account timezone.
  - **Relative ranges:** `date_range_type` is `custom` or `last_X_Y`, plus `_inc` to include today. Always call `get_today` first.
  - **Grain:** comes from the dimensions in `fields`. Including a date dimension gives daily rows, so the reach and users rules above apply.
  - **Source-specific options** (attribution window, conversion action) go in `settings`, which is undocumented per source (unverified). Inspect `field_discovery` for per-window or per-action fields instead.
  - **Async:** you must poll. Don't treat an empty first poll as zero.
  - **Meta history:** queries over 13 months error for unique fields after Meta's Jan 2026 change. Source: https://docs.supermetrics.com/docs/facebook-ads-new-historical-limitations-attribution-window-and-metric-removals-january-12-2026

### Windsor.ai MCP (official, Windsor)
- **Where it runs:** remote at `https://mcp.windsor.ai/` (Streamable HTTP), with OAuth or an API key.
- **Tools:**
  - `get_connectors`, `get_options`, `get_fields`
  - `get_data(connector, fields[], accounts[], date_from, date_to, date_preset, date_filters, options, filters, force_refresh)`
  - `create_custom_field`, `list_actions`/`execute_action` (writes)
  - Exports
  - Sources: https://mcp.windsor.ai/llms.txt, https://mcp.windsor.ai/llms-full.txt
- **Traps:**
  - **No date given:** "the last 3 days are used".
  - **Metric vs dimension:** NUMERIC and PERCENT fields are aggregated as metrics, so **percent fields get aggregated**. Request components and recompute ratios.
  - **Meta attribution:** goes in `options` (its doc example `7d_view,1d_click` is no longer valid at Meta). Discover valid values with `get_options`.
  - **Warehouse connectors** need `date_filters` to choose the date column, e.g. `{"orders":"created_at"}`.
  - **Pending:** a slow pull returns `pending`. Repeat the identical call.
  - **Size:** results that are too large error rather than truncate.
  - **Dates:** `date_preset` values like `this_monthT`, where `T` means including today.

### Funnel MCP (official, Funnel)
- **Where it runs:** remote, per-account URL (global `https://mcp.ai.funnel.io/mcp`), OAuth, read-only tools. Works in Claude, ChatGPT and Cursor. Access is through the account team.
- **Tool names and parameters:** not published on the pages I read (unverified).
- **Sources:** https://funnel.io/funnel-mcp, https://help.funnel.io/en/articles/15502539-connect-funnel-mcp-from-funnel-ai
- **Trap:** Funnel harmonizes fields across sources, so check which source field a "conversions" field maps to.

### Coupler.io MCP (official, Railsware)
- **Where it runs:** remote at `https://mcp.coupler.io/mcp`, OAuth. Works in Claude, ChatGPT, Gemini, Perplexity and Cursor. Source: https://mcpservers.org/remote-mcp-servers/coupler-io
- **Tools:** list data flows, get flow metadata or table schema, and run **read-only SQL over a data flow's output**. Needs Professional (or Starter) plan or higher. Source: https://blog.coupler.io/coupler-mcp-server/
- **Trap:** you query whatever grain and attribution the data flow was configured with, and as fresh as its last refresh. Inspect the flow config before computing reach, users or conversions.

### Improvado MCP (official, Improvado)
- **Where it runs:** endpoint `https://report.improvado.io/experimental/agent/api/mcp-customer/v1/invoke`, OAuth. Vendor-reported: 84 tools, 500+ sources, harmonized metrics ("Cost" in Google Ads equals "spend" in Meta), read and write. Source: https://improvado.io/docs-section-topic/improvado-mcp (vendor claims, unverified)
- **Trap:** harmonized "conversions" may mix definitions across platforms.

### Adzviser
- I found no published MCP server spec. The site lists ChatGPT and Claude as "destinations" and 40+ sources (unverified). Source: https://adzviser.com

### Others seen (unverified)
Porter Metrics, GoMarble, Adspirer, Pipeboard, Ryze AI and Markifact offer hosted ads MCPs, several with write tools. Sources: https://portermetrics.com/?p=184985, https://adkit.so/resources/google-ads-mcp

**General aggregator rule.** An aggregator re-exposes the source API's semantics behind its own field names. The same rules apply: the grain comes from the date and dimension fields; the attribution window and conversion action must be explicit; non-additive fields (reach, users, frequency, ratios, impression share, position) must be fetched at the reporting grain, never summed; and the default timezone and date range must be overridden.

---

## 1b. Ad platforms (other)

### Microsoft Advertising (Bing Ads)
- **MCP availability:** Microsoft has no official MCP. The best-known community server is `mharnett/mcp-bing-ads`, a local stdio server.
  - Its tools are `bing_ads_get_campaign_performance(start_date, end_date)`, `bing_ads_keyword_performance(start_date, end_date, [campaign_ids])` and `bing_ads_search_term_report`.
  - Write tools are hidden unless `BING_ADS_MCP_WRITE=true`.
  - The server fixes aggregation, columns, conversion columns and time zone, and you cannot change them.
  - Sources: https://github.com/mharnett/mcp-bing-ads, https://cdn.jsdelivr.net/npm/mcp-bing-ads@1.1.0/README.md
- **SOAP retirement:** SOAP goes REST-only for new features on 2026-10-01 and is fully deprecated on 2027-01-31 (unverified).
- **What sets the grain:** The report type sets the level (Account, Campaign, AdGroup and so on). Every attribute column you add splits rows, for example DeviceType. Source: https://learn.microsoft.com/en-us/advertising/guides/reports
- **Aggregation values:** Summary, Hourly, Daily, Weekly (Sun–Sat), WeeklyStartingMonday, Monthly, Yearly, DayOfWeek and HourOfDay.
  - Weekly, monthly and yearly ranges are widened to full periods.
  - DayOfWeek and HourOfDay roll up across the whole range, so they are not time series.
  - Source: https://learn.microsoft.com/en-us/advertising/reporting-service/reportaggregation
- **Conversions vs AllConversions:** `Conversions` and `Revenue` exclude goals with ExcludeFromBidding=true. `AllConversions` and `AllRevenue` include every goal. Source: https://learn.microsoft.com/en-us/advertising/reporting-service/campaignperformancereportcolumn
- **Impression share columns:**
  - They cannot be combined with Hourly or HourOfDay.
  - They refresh 14–18 hours after the UTC day ends.
  - They are mutually exclusive with some attributes, such as DeviceOS and Goal.
- **Time zone:** `ReportTimeZone` only decides how predefined ranges such as "Yesterday" resolve. Its default is PacificTimeUSCanadaTijuana. Source: https://learn.microsoft.com/en-us/advertising/guides/reports
- **Incomplete data:** The default `ReturnOnlyCompleteData=false` returns partial data silently and only sets the header "Potential Incomplete Data: true". Setting it to `true` fails while data is incomplete, and it cannot be used for ranges that include today. Source: https://learn.microsoft.com/en-us/advertising/reporting-service/reportrequest
- **Zero-impression rows:** A row can have clicks or conversions but zero impressions, because the impression happened before the period.
- **Correct request:**
  - Report: CampaignPerformanceReport with Aggregation=Daily.
  - Dates: an explicit custom range, with a ReportTimeZone that matches the account.
  - Complete data: ReturnOnlyCompleteData=true for closed days.
  - Conversions: choose Conversions or AllConversions explicitly.
- **Cannot:** Impression share at hourly grain. The community MCP cannot change columns or aggregation.

### LinkedIn Ads
- **MCP availability:** LinkedIn has no official MCP (vendor blog, unverified: https://theadspend.com/blog/linkedin-ads-mcp).
  - Community and vendor servers: Charlton Media LICampaignsMCP (https://glama.ai/mcp/servers/charltonmediagroup/LICampaignsMCP), Radiate B2B mcp-linkedinads (https://glama.ai/mcp/servers/radiateb2b/mcp-linkedinads) and CData read-only (https://mcp.so/servers/linkedin-ads-mcp-server-by-cdata).
  - Their parameters are undocumented, so inspect each with tools/list.
- **API finders:** `q=analytics` takes one `pivot`. `q=statistics` takes up to three `pivots`.
- **Fields:** Leaving out `fields` returns only impressions and clicks. You can request at most 20 metrics.
- **No pagination:** Responses are capped at 15,000 elements, so wide DAILY×CREATIVE pulls truncate. Split them by date or entity. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting
- **timeGranularity:** ALL, DAILY, MONTHLY or YEARLY.
- **Metrics are approximate:** Daily rows do not sum to the period total, and campaigns do not sum to the account. Query the full period at the level you report (same URL).
- **`approximateMemberReach`:**
  - It is unique, so never sum it.
  - It is incompatible with MEMBER_ pivots.
  - It only returns for ranges of 92 days or less.
  - Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting-schema
- **Conversions:** `externalWebsiteConversions` counts post-click plus post-view, and may include estimates. The `...PostClickConversions` and `...PostViewConversions` fields give the split. All conversion rules are summed unless you add `pivot=CONVERSION` (same URL).
- **Demographic (MEMBER_) pivots:**
  - Only the top 100 values per creative per day are returned.
  - Values with fewer than 3 events are dropped.
  - Data lags 12–24 hours.
- **Correct request:**
  - Main pull: `q=analytics&pivot=CAMPAIGN&timeGranularity=ALL&dateRange=...&fields=impressions,clicks,costInLocalCurrency,externalWebsitePostClickConversions,externalWebsiteConversions,approximateMemberReach,pivotValues,dateRange`
  - Conversions by rule: a separate `pivot=CONVERSION` call.
- **Cannot:** Exact sums, reach over more than 92 days, or demographic long tails.

### TikTok Ads
- **Official MCP:** TikTok hosts one, announced 2026-05-13.
  - Flat version (about 400 tools): `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat`
  - Layered version (about 40 tools): `.../tt-ads-mcp-layer`
  - Sign-in is browser OAuth that lasts 30 days.
  - Source: https://mcpplaygroundonline.com/mcp-servers/tiktok.md (third-party). Tool parameters are unverified, because the official docs at https://business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3 did not render.
- **Community server:** `@getmcpads/tiktok-ads-mcp-server`. TikTok returns HTTP 200 on errors, so check the app-level `code`. Source: https://mcpservers.org/servers/getmcpads-com/tiktok-ads-mcp-server
- **Underlying API (`report/integrated/get`):**
  - `report_type` (BASIC, AUDIENCE and others) and `data_level` (AUCTION_AD, AUCTION_ADGROUP, AUCTION_CAMPAIGN or AUCTION_ADVERTISER).
  - `dimensions` (for example `stat_time_day`), `metrics`, `start_date`/`end_date` and `query_lifetime`.
  - `page`/`page_size`, where `page_size` **defaults to 10**.
  - `enable_total_metrics`.
  - Dates are inclusive and use the advertiser time zone.
  - Sources: https://raw.githubusercontent.com/tiktok/tiktok-business-api-sdk/main/python_sdk/docs/ReportingApi.md, https://archive.linux.duke.edu/cran/web/packages/rtiktokads/refman/rtiktokads.html
- **Reach and frequency:** Never sum them across days.
- **Attribution:** "The TikTok API does not support Custom Attributions", so windows come from the UI settings.
- **Delays and limits:** Spend can lag up to 48 hours. A synchronous request covers at most 365 days. Source: https://docs.supermetrics.com/docs/good-to-know-about-tiktok-ads
- **Correct request:**
  - Additive metrics: BASIC with AUCTION_CAMPAIGN and `dimensions=["campaign_id","stat_time_day"]`.
  - Reach and frequency: a separate `dimensions=["campaign_id"]` request over the full range.
  - Always paginate.

### Amazon Ads
- **Official MCP:** Amazon's own Amazon Ads MCP Server has been in open beta since 2026-02-02.
  - Only Amazon Ads API partners with active credentials can use it.
  - It works with Claude, ChatGPT and Gemini.
  - It covers reporting, campaign create/update/delete, settings and billing.
  - Source: https://advertising.amazon.com/en-us/library/news/amazon-ads-mcp-server-open-beta/
  - Tool names and parameters are unverified, because the docs at https://advertising.amazon.com/API/docs/en-us/mcp/mcp-overview are JavaScript-only.
- **Reporting is asynchronous:** create the report, poll, then download (https://adbrew.io/blog/amazon-ads-mcp).
- **Attribution windows:** Sales metrics come per window: `sales1d`, `sales7d`, `sales14d` and `sales30d`. Same-SKU and other-SKU sales are separate fields (third-party: https://docs.adriel.com/data-sources/a-f/amazon-ads/data-reference.md).
  - The convention that SP defaults to 7d and SB/SD to 14d is unverified.
  - Mistake: summing SP 7d with SB 14d. Pin one window per ad product and state it.
- **Retention:** About 60–95 days depending on ad type (third-party, unverified). Older data must come from a warehouse.

---

## 2b. Product analytics

### Amplitude (official MCP)
- **Endpoint:** `https://mcp.amplitude.com/mcp`, with EU at `https://mcp.eu.amplitude.com/mcp`.
  - It works in Claude and in ChatGPT (about 25 tools there), and was observed in session.
  - Source: https://amplitude.com/docs/amplitude-ai/amplitude-mcp
- **Tools:**
  - `query_amplitude_data`: segmentation, funnels and retention, or running an existing chart by ID.
  - `get_amplitude_charts`, `query_experiment`, `use_amplitude_cohorts`, `get_amp_taxonomy` and `get_amplitude_context`.
  - Parameters are not in the docs. Use `describe_tool` with `?discovery=progressive`.
- **Known limits:** Large charts can be truncated and complex queries can time out. Dashboard charts may run with default settings rather than the saved filters.
- **Underlying semantics:** These come from the Dashboard REST API and are likely mirrored by the MCP (unverified).
  - `m` defaults to **uniques**; the alternatives are totals, pct_dau, average, sums and formula.
  - Interval values: 1 is daily, 7 weekly, 30 monthly.
  - Group-by `limit` defaults to 100, with a maximum of 1,000.
  - The project time zone is used, and there is no timezone parameter.
  - `seriesCollapsed` holds the deduplicated uniques for the whole range.
  - Source: https://amplitude.com/docs/apis/analytics/dashboard-rest
- **Mistakes:**
  - Summing daily uniques. Read the collapsed value, or query at the target interval.
  - Leaving uniques on when you want totals.
  - Missing group values beyond the limit.

### Mixpanel (official MCP)
- **Endpoint:** `https://mcp.mixpanel.com/mcp`, with EU and IN variants.
  - It is in the Claude connector directory and the ChatGPT app listing.
  - An org admin must enable it.
  - Sources: https://docs.mixpanel.com/docs/features/mcp, https://docs.mixpanel.com/docs/mcp.md
- **Tools:**
  - `Run-Query` covers insights, funnels, flows and retention.
  - Call `Get-Query-Schema` first to get the parameters.
  - Also `Get-Report`, `Get-Events`, `List-Properties`, and cohort and metric tools.
- **Limits:**
  - `Run-Query` cannot filter or break down by cohort.
  - It does not support SCD profile-history properties.
  - 600 requests per hour per user.
- **Legacy Segmentation semantics:**
  - `type` defaults to `general`, which counts **events**. Use `unique` for users.
  - `unit` defaults to day.
  - Breakdown `limit` defaults to 60 values, which silently truncates.
  - Source: https://docs.mixpanel.com/reference/segmentation-query.md
- **Mistake:** Summing daily uniques. Query at the target unit instead.
- **Time zone:** Raw export uses UTC for projects created after January 2023 (unverified).

---

## 5. Email / marketing automation

### Klaviyo (official MCP)
- **Endpoints:** Remote at `https://mcp.klaviyo.com/mcp` (OAuth; needs the Owner, Admin or Manager role). Local via `uvx klaviyo-mcp-server@latest` with `PRIVATE_API_KEY`. Observed in session.
- **Server settings:** Remote query parameters `read-only`, `core-tools-only` (on by default in ChatGPT), `toolsets`, `paginate-lists`/`list-page-size` (default 20) and `beta`.
  - **The listed Claude connector and ChatGPT app do not accept these parameters**, so read-only mode needs a custom connector.
  - Source: https://developers.klaviyo.com/en/docs/connect_to_the_klaviyo_mcp_server
- **Tools:**
  - Reporting: `get_campaign_report`, `get_flow_report`, `query_form_values/series` and `query_segment_values/series`.
  - Events: `get_metrics` and `query_metric_aggregates`.
  - Many tools write, for example `send_campaign`, `update_flow` and `delete_*`.
  - Source: https://developers.klaviyo.com/en/docs/klaviyo_mcp_server_available_tools
- **Reporting API underneath:**
  - Required: `statistics`, `timeframe` (a preset key or custom start/end; at most 1 year; account timezone) and `conversion_metric_id`.
  - `group_by`, `send_channel` (email, sms, push or whatsapp) and `interval` for series (hourly, daily, weekly or monthly; default weekly).
  - Rates come back as 0–1 fractions.
  - Rate limits: 1 per second burst, 2 per minute steady, 225 per day.
  - Sources: https://developers.klaviyo.com/en/reference/query_campaign_values, https://developers.klaviyo.com/en/docs/reporting_api_overview
- **Definitions:**
  - `opens` counts all opens; `opens_unique` counts unique opens.
  - `open_rate` = unique opens ÷ **delivered**.
  - `click_rate` = unique clicks ÷ delivered.
  - `click_to_open_rate` = unique clicks ÷ unique opens.
  - `conversions` counts events; `conversion_uniques` counts people.
  - A custom `end` rounds up to the hour.
  - `last_12_months` excludes the current month, while `last_365_days` includes it.
- **`query_metric_aggregates`:**
  - Takes `metric_id` and `measurements` (count, unique or sum_value), with `interval` hour, day, week or month.
  - Requires a `datetime` filter (greater-or-equal plus less-than).
  - Grouping uses `by` (for example `$flow`, `$message` or `Campaign Name`), with page_size 500.
  - **`timezone` defaults to UTC**, whereas reports use the account time zone.
  - Source: https://developers.klaviyo.com/en/reference/query_metric_aggregates
- **Mistakes and correct requests:**
  1. Guessing `conversion_metric_id`. Look up the "Placed Order" ID with `get_metrics` first.
  2. Using `opens` as the open-rate numerator.
  3. Using metric aggregates to match campaign UI numbers. Aggregates are dated by event time, while the UI uses send date, so use the Reporting tools.
  4. Leaving aggregates in UTC.
  5. Treating Placed Order `sum_value` (total store revenue) as email-attributed revenue.
- **Account settings that change results:**
  - The attribution window defaults to 5 days for email opens and clicks.
  - Apple MPP opens can be excluded from attribution but **not from reporting**.
  - Bot clicks are excluded by default on new accounts.
  - Changes apply retroactively.
  - Source: https://help.klaviyo.com/hc/en-us/articles/11118357030555
- **Cannot:** Set the attribution window per query.

### Mailchimp (Intuit)
- **Official Claude connector:** Reportedly at `ai-inc.mailchimp.com/claude/mcp/v2`, with 12 tools for **creating and editing campaigns only**. It has **no reporting, audience or list tools** (unverified: https://agentman.ai/agentskills/connections/mcp-server/intuit-mailchimp).
- **Official Mandrill MCP:** At `mandrillapp.com/mcp`, transactional only. "Mailchimp hasn't shipped an MCP server for the Marketing API" (https://growthmethod.com/mailchimp-mcp-server/).
- **Community servers:** For example `damientilman/mailchimp-mcp-server`, Zapier and Pipedream (unverified).
- **API fields** (https://mailchimp.com/developer/marketing/api/reports/get-campaign-report/):
  - Opens: `opens_total` and `unique_opens`. `open_rate` = unique opens ÷ deliveries.
  - MPP-excluded opens: `proxy_excluded_opens`, `proxy_excluded_unique_opens` and `proxy_excluded_open_rate`.
  - Clicks: `unique_clicks` and `unique_subscriber_clicks`.
  - Revenue: `ecommerce.total_revenue`.
  - List averages: `list_stats` gives list-wide averages on a **0–100** scale.
- **Mistakes:**
  - Using `opens_total` for open rate. Prefer `proxy_excluded_open_rate`.
  - Mixing the 0–100 list_stats scale with campaign rates.
  - Measuring list growth from current member counts. Use list activity (`subs`, `unsubs`, `other_adds`, `other_removes`), which covers **180 days only** and defaults to `count=10` (https://mailchimp.com/developer/marketing/api/list-activity/list-recent-activity/).

### Brevo (official MCP)
- **Endpoint:** `https://mcp.brevo.com/v1/brevo/mcp` with an MCP-enabled API key as a Bearer token. Single-module endpoints are also available, for example `/v1/brevo_campaign_analytics/mcp`.
- **Limits:** There is no read-only mode and no transactional stats module.
- **Source:** https://developers.brevo.com/docs/mcp-protocol
- **Fields** (https://developers.brevo.com/reference/get-email-campaign):
  - `statistics` parameter: globalStats, linksStats, statsByDomain, statsByDevice or statsByBrowser.
  - Delivery: `sent`, `delivered`.
  - Opens: `viewed` (all opens), `uniqueViews`, `trackableViews` (recipients without privacy protection), `estimatedViews` and `appleMppOpens`.
  - Clicks: `clickers` (all clicks) and `uniqueClicks`.
- **Mistakes:**
  - Treating `viewed` or `clickers` as unique counts.
  - Using `sent` as the denominator instead of `delivered`.
  - Not adjusting for MPP. Use `trackableViews` as the base, or subtract `appleMppOpens`.

### ActiveCampaign (official MCP)
- **Availability:** Remote server, listed at `claude.com/connectors/activecampaign`. It covers contacts, automations and "campaign performance". Source: https://www.activecampaign.com/apps/claude-integration
- **Tool names:** Unverified, because the help center returned 403.
- **API fields** (https://developers.activecampaign.com/reference/list-all-campaigns):
  - Fields: `send_amt`, `opens`, `uniqueopens`, `linkclicks`, `uniquelinkclicks`, `subscriberclicks`, `unsubscribes`, `hardbounces` and `softbounces`.
  - They come back **as strings**, cumulative per campaign.
  - There is no delivered field, no rates and no date-range stats.
- **Mistakes:**
  - Using `opens` instead of `uniqueopens`.
  - Using `send_amt` as delivered. Delivered ≈ send_amt − hard bounces − soft bounces (derived, unverified).
  - Not casting the string values before doing arithmetic.
  - Treating cumulative totals as period values.

### Customer.io (official MCP)
- **Endpoints:** `https://mcp.customer.io/mcp` (US) and `https://mcp-eu.customer.io/mcp` (EU).
- **Scopes:** read (default), read:sensitive, write, write:live and configure.
- **Tools:** Generic API tools only: `cio_prime`, `cio_schema`, `cio_read_api`, `cio_write_api`, `cio_delete_api`, `cio_skills_*` and `cio_auth_status`. Source: https://docs.customer.io/ai/mcp-server
- **Metrics endpoint:** `GET /v1/campaigns/{id}/metrics`. Send `version=2` with `res` (hourly, daily, weekly or monthly), `start`/`end` as Unix timestamps, `tz` (default UTC) and `type` (email, push and others).
  - v1 is deprecated: it always uses Eastern time and has a 45-day cap.
  - Metrics: `opened` vs `human_opened`/`prefetch_opened`, `clicked` vs `human_clicked`/`machine_clicked`, plus `delivered` and `converted`.
  - Rate limit: 10 requests per second.
  - Source: https://docs.customer.io/integrations/api/app/tag/automations/campaignMetrics/
- **Mistakes:**
  - Omitting `version=2`.
  - Using `opened` or `clicked` including machine events.
  - Leaving out `type=email`, which mixes channels.
- **Cannot:** Revenue attribution. Whether the counts are unique is undocumented.

---

## 6. E-commerce / payments

### Shopify
- **Official servers:**
  - **Dev MCP** (`npx -y @shopify/dev-mcp@latest`) reads docs and schemas only, not store data. Source: https://shopify.dev/docs/apps/build/devmcp
  - **Storefront MCP** at `https://{shop}/api/mcp`, plus UCP for catalog and cart, and **Customer Accounts MCP**. Both are shopper-facing, not analytics. Source: https://shopify.dev/docs/apps/build/storefront-mcp
  - **Official merchant connectors** for Claude, ChatGPT, Gemini, Perplexity and Copilot. You authorize from the Shopify admin, **one store at a time**. Their analytics coverage is undocumented. Source: https://help.shopify.com/en/manual/apps/connecting-ai-tools
  - Tool names such as `graphql_query` and a ShopifyQL tool are unverified.
- **ShopifyQL:** Admin GraphQL `shopifyqlQuery`, for example `FROM sales SHOW net_sales TIMESERIES day SINCE -30d UNTIL today`. Source: https://shopify.dev/docs/api/shopifyql
- **Sales schema** (https://shopify.dev/docs/api/shopifyql/latest/schemas/sales_revenue/sales):
  - `gross_sales`: before discounts and returns; excludes taxes, shipping, duties and fees.
  - `net_sales` = gross − discounts − `sales_reversals`. Reversals cover refunds, returns, cancellations and edits; `returns` is deprecated as of 2026-10.
  - `total_sales` = net + fees + duties + shipping + taxes.
  - Rows are events, so later refunds add rows dated when they happen (inferred, unverified).
  - Amounts are in store currency.
  - `is_canceled_order` and `is_sales_reversal` are available as filters.
- **Orders API** (https://shopify.dev/docs/api/admin-graphql/latest/objects/Order):
  - `test` flag: exclude test orders.
  - `cancelledAt` and `displayFinancialStatus`.
  - `createdAt` vs `processedAt`. The query sorts by PROCESSED_AT.
  - `totalPriceSet` is before returns and `currentTotalPriceSet` is after. Both include tax and shipping. Both are MoneyBags with shopMoney and presentmentMoney.
  - `totalRefundedSet`.
  - **Only the last 60 days** of orders are available without `read_all_orders`.
- **Pagination:** At most 250 per page, using `first`/`after` and `pageInfo`. Use bulk operations for big pulls. Source: https://shopify.dev/docs/api/usage/pagination-graphql
- **Correct request:**
  - With ShopifyQL: `FROM sales SHOW gross_sales, discounts, sales_reversals, net_sales, total_sales`, grouped by the period.
  - With orders only: exclude `test:true`, decide how to treat cancelled orders, use shopMoney, paginate fully, and never call summed `totalPriceSet` "net sales".

### Stripe (official MCP)
- **Endpoint:** `https://mcp.stripe.com`, using OAuth or an **agent API key**. Full-access and untagged restricted keys are rejected from December 2026.
- **Availability:** Claude directory connector and ChatGPT plugin.
- **Mode:** Check `livemode`, because test and live mode can both be connected. Source: https://docs.stripe.com/mcp
- **Tools:**
  - `stripe_api_search`, `stripe_api_details`, `stripe_api_read` (any GET) and `stripe_api_write`.
  - `get_stripe_account_info` and `search_stripe_documentation`.
  - `stripe_analytics` (preview): metrics and subscriptions. Natural-language SQL requires Sigma.
- **Pagination:** `limit` is 1–100 (default **10**). Use `starting_after` while `has_more` is true. Source: https://docs.stripe.com/api/pagination
- **Traps:**
  - **Minor units:** 1000 means 10.00 USD. Zero-decimal currencies such as JPY are not divided. Source: https://docs.stripe.com/currencies
  - **Subscriptions list excludes canceled by default.** Pass `status=all` for churn. Source: https://docs.stripe.com/api/subscriptions/list
  - **Use balance transactions for revenue.** Group by `reporting_category`. Refunds are their own rows, and disputes appear as `adjustment`. Source: https://docs.stripe.com/reports/balance-transaction-types
  - **Avoid double-counting.** Counting PaymentIntents and Charges together double-counts (unverified). Invoices are not cash.
- **MRR:** **Not an API field.** It is the sum of monthly-normalized active subscriptions, as in Stripe's Billing analytics. If you compute it yourself, state the rules for trials, discounts and past_due. Source: https://support.stripe.com/questions/calculating-monthly-recurring-revenue-(mrr)-in-billing

---

## 7. Warehouses

### BigQuery
- **Google remote MCP:** `https://bigquery.googleapis.com/mcp`, with OAuth and IAM. Source: https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp
  - **Tools:** `list_dataset_ids`, `list_table_ids`, `get_dataset_info`, `get_table_info`, `execute_sql` and `execute_sql_readonly`.
  - **Result limits:** Results are capped at **3,000 rows**, and queries time out at 3 minutes. Aggregate in SQL.
  - **No cost tool:** No dry-run or cost tool is documented.
- **Other options:**
  - MCP Toolbox for Databases (`googleapis/genai-toolbox`, renamed mcp-toolbox, `--prebuilt=bigquery`). Its tool names are unverified. Source: https://github.com/googleapis/genai-toolbox
  - A BigQuery plugin MCP was observed in session.
- **GA4 export traps** (https://support.google.com/analytics/answer/7029846, https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables):
  - **Intraday tables:** `events_*` also matches `events_intraday_*`, which **double-counts**. Filter `_TABLE_SUFFIX BETWEEN '20261001' AND '20261015'` with constants, which also prunes bytes scanned.
  - **Late events:** Events can arrive up to 3 days late.
  - **Time zones:** `event_date` is in the property time zone. `event_timestamp` is UTC microseconds.
  - **Users:** Count users with `COUNT(DISTINCT user_pseudo_id)`. These counts are exact, whereas the UI uses HLL++, so expect small gaps (https://support.google.com/analytics/answer/9191807).

### Snowflake
- **Snowflake-Labs/mcp is deprecated.** Source: https://github.com/Snowflake-Labs/mcp
- **Managed MCP server:** `CREATE MCP SERVER ... FROM SPECIFICATION`, with the endpoint `https://<account>/api/v2/databases/{db}/schemas/{schema}/mcp-servers/{name}`.
  - **Tool types:**
    - `CORTEX_ANALYST_MESSAGE` (semantic views)
    - `CORTEX_SEARCH_SERVICE_QUERY`
    - `CORTEX_AGENT_RUN`
    - `SYSTEM_EXECUTE_SQL` (read-only by default)
    - `GENERIC` (UDFs and stored procedures)
  - **Limits:** SQL responses are **truncated at 250 KB**. A server can have at most 50 tools.
  - Source: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp
- **Prefer Cortex Analyst over a semantic view when one exists.** It encodes the metric definitions.

### Databricks
- **Managed MCPs:** DBSQL, Genie, UC functions and vector search. Paths are `https://<host>/ai-gateway/mcp-services/<name>`, or the legacy `/api/2.0/mcp/sql`. Source: https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp
- **DBSQL `execute_sql`:**
  - **Reads and writes by default.** Set `disallow_writes: true` in policy.
  - Runs async, so poll for results.
  - Large results are truncated. Aggregate in SQL.
  - Source: https://docs.databricks.com/aws/en/agents/mcp-tools/databricks-sql
- **Genie spaces:** Genie is recommended for natural-language analytics, because it carries curated definitions.

### Postgres
- **Reference server:** `modelcontextprotocol/servers` postgres was **archived on 2025-05-29**. It has a single `query(sql)` tool in a READ ONLY transaction, which can be escaped with `COMMIT; DROP ...`. Use a SELECT-only database role.
  - Sources: https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres, https://securitylabs.datadoghq.com/articles/mcp-vulnerability-case-study-SQL-injection-in-the-postgresql-mcp-server/
- **crystaldba/postgres-mcp:** `--access-mode=restricted` gives read-only access with a time limit.
  - Tools: `list_schemas`, `list_objects`, `get_object_details`, `execute_sql`, `explain_query` and `analyze_*`.
  - Source: https://github.com/crystaldba/postgres-mcp

### ELT schema traps (any warehouse)
- **Fivetran:**
  - Soft-deleted rows keep `_fivetran_deleted = TRUE`. Filter with `WHERE NOT COALESCE(_fivetran_deleted, FALSE)`.
  - History-mode tables are SCD2. Filter `_fivetran_active = TRUE`, or you count every version.
  - Source: https://fivetran.com/docs/core-concepts/sync-modes/history-mode
- **Airbyte:**
  - Metadata columns are `_airbyte_raw_id`, `_airbyte_extracted_at` and `_airbyte_meta`. Source: https://docs.airbyte.com/understanding-airbyte/airbyte-metadata-fields
  - Append mode keeps duplicates per primary key, so dedup on the latest `_airbyte_extracted_at` (unverified).
- **Ads tables from ELT** keep the API's semantics. Fivetran Google Ads stats rows are per day × segment, so summing reach or unique columns across days is still wrong.

---

## 8. Power BI / Microsoft Fabric

Microsoft offers two MCP servers for this:
- **Authoring** builds and edits models.
- **Fabric IQ** reads them. Microsoft says not to use Authoring to answer business questions.
- The older "Consumption" endpoint is still documented.
- Source: https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview

**DAX rules for every Power BI connector:**
- **Reference model measures.** Use `EVALUATE SUMMARIZECOLUMNS(<group cols>, <filters e.g. TREATAS(...)>, "Name", [Existing Measure])`. Don't rebuild a measure with `SUM()`, which loses the author's filters and time intelligence.
- **Missing rows are not zeros.** SUMMARIZECOLUMNS drops rows where every expression is BLANK, so an absent row means "no value". Wrap a measure in `IGNORE()` to keep blank rows. Source: https://learn.microsoft.com/en-us/dax/summarizecolumns-function-dax
- **Set toggle and selector tables explicitly.** A measure that reads a disconnected parameter table through `SELECTEDVALUE` returns its fallback (BLANK by default) when there is no single selection. A query has no slicers, so pass `TREATAS({"<option>"}, Param[Col])`. Then confirm the report's choice with GetReportMetadata, which returns slicers and filters.
  - Sources: https://learn.microsoft.com/en-us/dax/selectedvalue-function-dax, https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started
- **Respect the executeQueries limits.** Each call runs one query and returns one result table.
  - At most **100,000 rows or 1,000,000 values**, and 15 MB. Truncation still returns HTTP 200 with an error.
  - 120 queries per minute per user.
  - `includeNulls` defaults to false.
  - DAX only; no INFO functions or DMVs.
  - Aggregate in DAX instead of pulling raw rows.
  - Source: https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries
- **RLS:** Results depend on the signed-in user. Service principals bypass RLS and aren't supported on models that have RLS.

### Fabric IQ MCP (Microsoft, GA; recommended for reading)
- **Endpoint:** `https://fabriciq.svc.cloud.microsoft/v1/mcp/fabriciq`. With private links, use `api.fabric.microsoft.com/v1/mcp/fabriciq`.
- **Tools:** `DiscoverArtifacts` (by name), `ResolveFabricItem` (from a browser URL), `GetReportMetadata`, `GetSemanticModelSchema`, `ValueSearch` and `ExecuteQuery`.
- **Read-only.** There is no natural-language answer tool, so the agent writes the DAX.
- **No IDs needed.** A name or URL is enough, and Build or workspace roles are not required.
- **Auth:** Delegated Entra OAuth only (`Item.Read.All`, `Item.Execute.All`, `Dataset.Read.All`). Service principals are not supported.
- **Clients:** Documented for GitHub Copilot CLI. Other clients may need a single-tenant app registration.
- **Capacity and region:** Fabric or Premium capacity is not required. The tenant's home region must support Fabric.
- **ExecuteQuery limits:** One model per call. The default is **250 rows** unless you set `maxRows`. Large results come back as an embedded CSV that may be truncated.
- **Contract header:** Pin `X-Variants: Fabric.Routing.FabricIQ.V1`.
- **Freshness and security:** Data is as of the last refresh. RLS and OLS apply.
- **Cannot:** Dashboards, paginated reports, cross-model queries or writes.
- Source: https://learn.microsoft.com/en-us/fabric/iq/connectors/fabric-iq-mcp

### Power BI Consumption MCP (Microsoft, preview, older)
- **Endpoint:** `https://api.fabric.microsoft.com/v1/mcp/powerbi`
- **Tools:**
  - Execute Query: takes the **model GUID** (not a name) and DAX.
  - Get Semantic Model Schema: includes "prep for AI" metadata.
  - Get Report Metadata.
  - Generate Query: needs a Copilot license and uses capacity.
- **Prerequisites:** The tenant setting "Users can use the Power BI Model Context Protocol server endpoint (preview)" must be on, and you need Build permission. Source: https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started
- **Claude Desktop and ChatGPT:** You must self-register an Entra app.
  - Claude redirect URI: `https://claude.ai/api/mcp/auth_callback`.
  - Scopes: `Dataset.Read.All`, `Workspace.Read.All`, `MLModel.Execute.All`.
  - Source: https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-external-clients

### Power BI Authoring (Modeling) MCP (Microsoft; local GA, hosted preview)
- **Hosted:** `https://api.fabric.microsoft.com/v1/mcp/powerbi/authoring`. It is stateful and needs the `mcp-Session-Id` header.
- **Local:** `npx @microsoft/powerbi-modeling-mcp`, the VS Code extension, or an exe.
  - Connects to Power BI Desktop, PBIP/TMDL files, or Fabric over XMLA (Read Write).
  - **Not supported on macOS.**
- **Tools:** 21 tools, including `measure_operations`, `relationship_operations`, `table_operations`, `dax_query_operations`, `security_role_operations` and `calculation_group_operations`.
- **Read vs write:** `--readwrite` is the default and `--readonly` is available.
- **DAX limit:** Queries are capped at 100k rows.
- **Invites:** Creating new measures when existing ones would do. Use `--readonly` when you are only pulling metrics.
- **Sources:** https://learn.microsoft.com/en-us/power-bi/developer/mcp/power-bi-authoring-mcp, https://github.com/microsoft/powerbi-modeling-mcp

### microsoft/fabric-toolbox
- **Semantic Model MCP Server** (v0.3.0, Python and .NET, XMLA):
  - Lists workspaces and datasets, gets TMSL, runs DAX, updates TMSL (writes), runs lakehouse SQL and Best Practice Analyzer.
  - Requires Premium or Fabric capacity.
  - Aimed at VS Code Copilot.
  - Source: https://github.com/microsoft/fabric-toolbox/tree/main/tools/SemanticModelMCPServer
- **DAX Performance Tuner:**
  - Tools: `connect_to_dataset`, `prepare_query_for_optimization`, `execute_dax_query` and `get_session_status`.
  - Windows-only. Built for tuning, not metric retrieval.
  - Source: https://github.com/microsoft/fabric-toolbox/tree/main/tools/DAXPerformanceTunerMCPServer

### Fabric MCP (`microsoft/mcp`): Core remote and local
- **Core endpoint:** `https://api.fabric.microsoft.com/v1/mcp/core`. Covers workspaces, items, capacities and definitions.
- **Local server:** Covers OneLake, catalog search and pipelines.
- **Neither runs DAX.** Use them only to find IDs. Core can delete workspaces, so gate it.
- **Sources:** https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/what-is-fabric-mcp-server, https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/core-remote/tools-core-mcp-server

### sulaiman013/powerbi-mcp (community, MIT, about 124 stars)
- **Tools:** 82, including `execute_dax`, `desktop_execute_dax`, `create_measure`/`delete_measure`, `validate_dax`, `scan_measure_dependencies`, `rls_test_harness` and PBIP/PBIR editing.
- **Connections:** Power BI Desktop via ADOMD, the Service via XMLA and REST with a service principal, or offline PBIP.
- **Read-only switch:** `POWERBI_MCP_READONLY=true`.
- **Platform:** Live connections are Windows-only. The cloud paths have "not yet validated against a production tenant".
- **RLS:** The service principal bypasses RLS unless a role is set.
- **Source:** https://github.com/sulaiman013/powerbi-mcp

**No Power BI connector provides:** values exactly as a report renders them (visual filters, bookmarks and slicer state are not applied), data newer than the last refresh, or joins across models.

---

## 9. CRMs

### HubSpot: remote MCP (official), developer MCP, ChatGPT connector
- **Remote MCP (`mcp.hubspot.com`):** HubSpot's own server, using OAuth with per-user scopes. It is also the claude.ai HubSpot connector seen in this session.
  - **Read tools:** `discover_hubspot_schema`, `search_crm_objects`, `get_crm_objects`, `query_crm_data`, `search_properties`, `get_properties`, `search_owners`, `get_campaign_attribution_reports`, `read_campaign_data`, `get_marketing_email_analytics`, `get_content_analytics_report`, among others.
  - **Write tools:** `manage_crm_objects`, `manage_custom_properties`, `manage_campaign_objects` and others, with a confirmation step.
  - **Tool availability** depends on the subscription and the user's permissions.
  - Source: https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server.md
- **Query limits:**
  - **`search_crm_objects`:** up to 5 filter groups with up to 6 filters each, and at most 200 results per page.
  - **`get_crm_objects`:** at most 100 IDs.
  - **`query_crm_data`:** "does not support joins, column aliases, subqueries, association traversal, or currency conversion".
- **Underlying Search API:**
  - A query stops at **10,000 total results**, and paging past that returns a 400 error.
  - Pages default to 10 rows, with a maximum of 200.
  - One sort rule only, and 5 requests per second.
  - Archived records are excluded, and new changes can take a short time to appear.
  - Source: https://developers.hubspot.com/docs/api-reference/search/guide
- **Data the connectors cannot see:** With Sensitive Data turned on, activity and conversation data is blocked.
- **ChatGPT connector:**
  - Reads, creates and updates records. It never deletes, and bulk writes are capped at 10.
  - It "can't copy entire CRM databases".
  - It connects to one portal at a time.
  - Source: https://knowledge.hubspot.com/integrations/connect-your-hubspot-account-to-chatgpt
- **Developer MCP (`hs mcp setup`):** for building apps, not for analytics. Source: https://developers.hubspot.com/mcp
- **Mistakes and correct requests:**
  - **Counts and row limits:** One unpaged call returns 10 rows, and any search caps at 10k. Read `total` for counts. Page with `after`, and slice by date to stay under 10k.
  - **Stage entry:**
    - Use `hs_v2_date_entered_{stage_id}` and `hs_v2_date_exited_{stage_id}`. They are keyed by the stage's internal ID within each pipeline.
    - The legacy `hs_date_entered_*` stopped working on 2024-11-20 (secondary source: https://community.hubspot.com/t/upcoming-sunset-of-legacy-stage-calculated-properties-for-contacts-and-deals/114378).
    - Stage-calculated properties need Professional or Enterprise. Source: https://knowledge.hubspot.com/properties/stage-calculated-properties
  - **Cohort dates:**
    - `createdate` can be edited by users.
    - `closedate` is the *expected* close date while a deal is open. It is set to today when the deal closes.
    - Count bookings with `closedate` in range **and** `hs_is_closed_won = true`, plus a `pipeline` filter. Don't match the "Closed Won" label, because stage IDs differ per pipeline.
    - Source: https://knowledge.hubspot.com/properties/hubspots-default-deal-properties
  - **Currency:** `amount` is in the deal's own currency. In multi-currency portals, use the amount in company currency (internal name `amount_in_home_currency`, unverified).
  - **Lifecycle stage:**
    - Lifecycle stage moves forward only by default.
    - The legacy "Became a … date" values are cleared when a record moves backward.
    - Use the date-entered properties for funnel timing.
    - Source: https://knowledge.hubspot.com/records/use-lifecycle-stages
  - **Original source:** A deal's "Original Traffic Source" comes from the earliest associated contact, falling back to the company. Otherwise, traverse associations yourself, because `query_crm_data` cannot.
- **Cannot:** joins or FX conversion in `query_crm_data`, more than 10k rows per search, archived records, or Sensitive Data properties.

### Salesforce: hosted MCP servers (official) and DX MCP
- **Hosted read server:** `https://api.salesforce.com/platform/mcp/v1/platform/sobject-reads`.
  - Read-only, and runs as the signed-in user, so field-level security and sharing apply.
  - The guide says to always include `WHERE` and `LIMIT`.
  - Tool names are unverified (developer.salesforce.com returned 403). Search-result source: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/sobject-reads.html
  - Secondary source: GA in April 2026 for Enterprise Edition and above, with a quota of 100k requests per 24 hours (https://truto.one/blog/best-mcp-servers-and-tools-for-salesforce-ai-agent-integrations-2026/).
  - A Salesforce marketing-plugin MCP was observed in this session.
- **DX MCP (`salesforcecli/mcp`):** provides `run_soql_query`. It is a developer tool, and the package reaches end of life on **2026-11-02**. Source: https://github.com/salesforcecli/mcp
- **Mistakes and correct requests:**
  - **Win/close:** Filter `IsWon` and `IsClosed`, not StageName strings.
  - **Stage entry:**
    - Use `OpportunityHistory`.
    - Opportunities that were never changed have no rows there, so use `OpportunityFieldHistory` as well. It only covers tracked fields.
    - Search-result source: https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_opportunityhistory.htm
  - **Currency:**
    - Use `convertCurrency(Amount)` in `SELECT` only. With advanced currency management, it uses dated rates.
    - It is not allowed in `WHERE`, `ORDER BY` or aggregates.
    - Filter with ISO-prefixed literals such as `USD5000`.
    - Search-result source: https://developer.salesforce.com/docs/atlas.en-us.224.0.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_querying_currency_fields.htm
  - **Attribution:**
    - `Opportunity.CampaignId` is the single primary campaign.
    - Multi-touch credit is in `CampaignInfluence`, filtered by model. Deactivating a model deletes its records.
    - Search-result source: https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_campaigninfluencemodel.htm
  - **Aggregation:** Use `COUNT()` and `GROUP BY` in SOQL rather than pulling rows.

### Pipedrive: native MCP (official, launched 2026-06-30)
- **Availability:** Works with ChatGPT and Claude, uses OAuth, is on all plans, and both reads and writes.
  - Each action is logged.
  - Plan-based token limits apply.
  - Tool names and the endpoint are not published.
  - Sources: https://www.pipedrive.com/en/newsroom/pipedrive-launches-native-mcp-server-bringing-crm-workflows-directly-into-ai-assistants, https://www.pipedrive.com/en/features/mcp-server
- **Community servers:** for example a read-only server with 22 tools (https://osher.com.au/blog/pipedrive-mcp-server-released/) and an MIT-licensed one with 155 tools (https://devcommunity.pipedrive.com/t/open-source-pipedrive-mcp-server-155-tools-v2-first-mit/20392).
- **Underlying API:**
  - `GET /api/v2/deals` takes `status`, `pipeline_id`, `stage_id`, `filter_id`, `updated_since`, `cursor` and `limit` (default 100, maximum 500).
  - `won_time` and `lost_time` record when the status changed. `first_won_time` is returned only through `include_fields`.
  - `/v1/deals/{id}/flow` returns the change log.
  - Source: https://developers.pipedrive.com/docs/api/v1/Deals
- **Mistakes and correct requests:**
  - **Won date:** `expected_close_date` and `update_time` are not the win date. Use `status=won` and bucket by `won_time`.
  - **Stage history:** `stage_change_time` holds only the latest change (unverified). Use the deal flow for stage history.
  - **Currency:** Sum `value` per `currency`.

### Close: official MCP
- **Endpoint:** `https://mcp.close.com/mcp`.
  - Uses OAuth, or an API key plus the `Close-Scope` header.
  - Scopes are `mcp.read`, `mcp.write_safe` and `mcp.write_destructive`.
  - Works with Claude, Claude Code and ChatGPT, and was seen in this session.
  - Source: https://developer.close.com/mcp.md
- **Tools:**
  - `find_opportunities`: filters on status, owner, lead and close-date range.
  - `aggregation`: call `get_fields` first.
  - `search` and `paginate_search`.
  - `fetch_opportunity`.
  - `find_pipelines_and_opportunity_statuses`.
  - Source: https://developer.close.com/mcp/tools.md
- **Underlying API:**
  - Filters `status_type` (active/won/lost), `date_won__gte/lte` and `date_created__*`.
  - `value` is in **cents**.
  - `value_period` is one_time, monthly or annual, and `annualized_value` is monthly × 12.
  - Responses carry totals over all matching results, such as `total_value_annualized`.
  - `_limit` defaults to 100, with `_skip` for paging.
  - Sources: https://developer.close.com/api/resources/opportunities/list.md, https://developer.close.com/api/resources/reporting/get-opportunity-statuses.md
- **Mistakes and correct requests:**
  - **Wins:** Filter `status_type=won`, not custom status labels, and bucket by `date_won`.
  - **Units:** Divide `value` by 100.
  - **Mixed periods:** Don't add monthly and one-time values together. Use annualized or per-period values.
  - **Totals:** Read the API totals, not the sum of one page.
- **Cannot:** stage-history timestamps on the opportunity itself. Use the opportunity-status report instead.

---

## 10. Cross-connector request checklist

Run through this list before calling any connector tool.

1. **Grain = reporting grain.**
   - Set the level or resource explicitly, because defaults can be ad level (Pipeboard) or account level (Meta CLI).
   - Every dimension you add (date, device, conversion action, keyword) splits or drops rows.
2. **Non-additive metrics are fetched, never summed.**
   - This covers reach, frequency, unique users and opens, impression share, average position, CTR, CPC, ROAS, and LinkedIn's approximate metrics.
   - Request them once at the exact period and level you report:
     - Meta: `time_increment=all_days`
     - GA4: `year_month` or no date dimension
     - LinkedIn: `timeGranularity=ALL`
     - Amplitude: `seriesCollapsed`
     - GSC: no query or page dimension
   - Recompute ratios from their additive parts.
3. **Pin conversions.**
   - Name the action:
     - Google Ads: `segments.conversion_action`
     - Meta: one `action_type`
     - LinkedIn: `pivot=CONVERSION`
     - Klaviyo: `conversion_metric_id`
     - GA4: the key event name
   - Choose primary or all (Google `conversions` vs `all_conversions`; Microsoft `Conversions` vs `AllConversions`).
   - Pull spend in a separate query when the conversion segment would split or drop cost rows.
4. **Pin attribution.**
   - Set the window explicitly. Meta: `action_attribution_windows` or `use_unified_attribution_setting=true`; 7d_view and 28d_view are gone since 2026-01-12.
   - Use one Amazon window per ad product.
   - Know when the platform takes it from the UI only (TikTok, Klaviyo account settings).
   - State the conversion date semantics (click date vs conversion date).
5. **Date semantics and time zone.**
   - Pass explicit start and end dates, never defaults:
     - Windsor: last 3 days
     - Meta: last_30d
     - Pipeboard: maximum
   - Set the time zone: Supermetrics, Klaviyo aggregates and Customer.io default to UTC, and Microsoft Ads to Pacific.
   - Exclude incomplete recent days or label them:
     - GSC: `dataState`
     - Microsoft: ReturnOnlyCompleteData
     - Also allow for spend and conversion lag.
6. **Unique vs total.**
   - Defaults differ: Amplitude counts uniques, Mixpanel counts general events, Klaviyo `opens` vs `opens_unique`, Mailchimp `opens_total` vs `unique_opens`.
   - Rate denominators are delivered, not sent.
   - Prefer MPP- and machine-excluded opens.
7. **Money.**
   - Convert units:
     - Google `cost_micros` ÷ 1e6
     - Stripe minor units ÷ 100 (except zero-decimal currencies)
     - Close cents ÷ 100
   - Use one currency: GA4 `currency_code`, HubSpot company-currency amount, Salesforce `convertCurrency`, Shopify shopMoney.
   - Use the named revenue definition: Shopify gross, net or total sales; GA4 purchaseRevenue vs totalRevenue; Stripe balance transactions.
8. **Exclusions.**
   - Shopify test and cancelled orders.
   - Stripe test mode (`livemode`) and canceled subscriptions (`status=all`).
   - Fivetran `_fivetran_deleted` and history rows.
   - GA4 BigQuery `events_intraday_*`.
   - HubSpot pipeline filter.
9. **Completeness.** Paginate to the end, or report the truncation. Limits per connector:

   | Connector | Limit |
   |---|---|
   | GSC | 25k per request, step `startRow`; 50k rows per day |
   | GA4 | 10k default, 250k maximum |
   | Pipeboard | 25 rows per page |
   | TikTok | 10 rows per page |
   | Stripe | 10 default, 100 maximum |
   | Shopify | 250 per page; 60-day orders window |
   | HubSpot | 10k cap per search |
   | LinkedIn | 15k elements |
   | BigQuery MCP | 3k rows |
   | Snowflake | 250 KB |
   | Power BI executeQueries | 100k rows |
   | Fabric IQ | 250 rows default |
   | Mixpanel | top 60 segments |
   | Amplitude | top 100 groups |

   - Async tools (Supermetrics, Windsor, Amazon, Databricks) must be polled until done. An empty first response is not zero.
10. **Check response metadata before quoting numbers.**
    - GA4: `samplingMetadatas`, `subjectToThresholding`, `dataLossFromOtherRow`.
    - Microsoft: the "Potential Incomplete Data" header.
    - TikTok: app-level `code` on HTTP 200.
    - Power BI: an error on HTTP 200 truncation.
11. **Use the semantic layer when one exists.** Reference existing measures (Power BI `[Measure]`, Snowflake semantic views and Cortex Analyst, Databricks Genie) instead of re-implementing them. Set disconnected selector tables explicitly.
12. **Least privilege.** Prefer read-only modes:
    - Klaviyo `read-only` (only on a custom connector)
    - Databricks `disallow_writes`
    - Power BI `--readonly`
    - Close `mcp.read`
    - Postgres SELECT-only role
    - Many listed connectors also expose write or delete tools.
