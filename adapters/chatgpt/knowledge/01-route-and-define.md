# Skill: route-question

---
name: route-question
description: >-
  Use this skill first, before any other Devil's Analyst skill, whenever someone asks a marketing
  or analytics question that needs data: "how did paid search do", "why did revenue drop",
  "build me a dashboard", "what's our CAC". It inventories what data is actually reachable
  (connector tools, MCP servers, database connections, uploaded files), maps the question
  to analysis categories (paid search, paid social, organic social, video, email, web
  analytics, SEO, page speed, spend, competition, CRM, e-commerce, subscriptions), rewrites
  it into a precise request (metric, conversion action, account, scope, date window, grain,
  report level, attribution window), and says up front what can and cannot be answered
  with the data available. It reads the team's house rules (a house-rules/ folder) before
  anything else.
---

# route-question

Most wrong answers start before the first query: the question asked for
something the data cannot say, or the request to the platform asked for the
wrong thing. Route first, then analyse.

## 0. Read the house rules first

House rules are what this team knows about its own data that no shipped check
can know: which revenue is the revenue of record, which campaigns are brand,
which threshold their volume needs, which column lies. Read them before the
inventory, because they change what counts as a source and which defaults
apply.

1. **Find them.** Look for a `house-rules/` folder at the root of the project
   or workspace you are working in. Read every `.md` file in it except
   `README.md`, `TEMPLATE.md` and anything under `examples/` (those are
   fictional and never apply). In a chat without files, use rules the user
   pasted or uploaded, or that sit in the project's knowledge. If there are
   none, say nothing about them and go on.
2. **List them.** Keep one line per rule: id, area, the check, the red flag
   threshold and, if it has one, the shipped check it overrides
   (`overrides:`).
3. **Apply them by precedence**, highest first:
   1. what the user says in this conversation;
   2. the team's house rules;
   3. the team's governed definitions (a Power BI model, a metric dictionary);
   4. the shipped defaults (these skills, their checks and catalogs).

   A house rule replaces the default it names or contradicts: its definition,
   threshold or default wins. A house rule cannot make arithmetic true that is
   false: if one seems to require summing users or averaging rates, report the
   house rule's number, show the core-rule number next to it, and say why they
   differ.
4. **Cite them.** When a house rule changed a number, a default or a finding,
   name its id in the scope line or the finding ("per HR-003, revenue is
   finance net revenue"). A rule older than its review date, or one whose
   column or setting no longer exists, is flagged to its owner, not silently
   applied.

`metric-definitions` reads the same rules; pass the list on with the request.

## 1. Inventory what is reachable

List the sources you can actually read right now, with their scope:

| Source kind | How to tell | Note |
|---|---|---|
| Connector or MCP tools | tool names and descriptions (e.g. a GA4, Google Ads, Meta, Search Console, email-platform or CRM tool) | note each tool's account(s), dimensions, metrics and date range limits |
| Power BI semantic model | a Power BI or Fabric MCP connector (Microsoft's Power BI MCP servers, Fabric tools) that lists models or runs DAX; or a PBIP/TMDL folder | **takes precedence over everything below**: see section 1a |
| Database or warehouse | a SQL tool or connection; list schemas and tables | read table names and columns before writing SQL |
| Files | uploaded CSV/XLSX exports | read headers, row grain and date range |
| Nothing | none of the above | go to section 4 (onboarding) |

For every source, record: platform, account(s), date range present, freshness
(latest date with data), grain, and any column that changes meaning by option
(conversion action, attribution window, report level, search type, unique vs
total).

## 1a. When a Power BI model is connected

A semantic model is the team's statement of what each number means. It takes
precedence over raw sources, but it is not trusted blindly: models carry the
same traps as ad-hoc queries, only better hidden. Switch to the
`power-bi-definitions` skill, which carries the full Power BI workflow, and:

1. **Read the model**: measures (DAX, format, description), tables and their
   grain, relationships (direction, cardinality, active or not), and every
   disconnected toggle or selector table (conversion type, attribution window,
   unique vs total, lab vs field, report level, cost type) with the value the
   DAX falls back to when nothing is selected.
2. **Map the measures the question needs to Devil's Analyst's definitions**
   (`metric-definitions`): which catalog metric each one claims to be.
3. **Audit each mapped measure and the model around it** against the rules:
   - ratios built as `DIVIDE(SUM, SUM)`, not `AVERAGE`/`AVERAGEX` of a rate
     or of per-row averages (average view duration, engagement rate, CTR);
   - non-additive columns not summed across days, campaigns or levels
     (users, reach, frequency, impression share, snapshots such as followers
     or list size);
   - a fact table holding several report levels or overlapping columns
     (attribution windows, `conversions` vs `all_conversions`) is filtered to
     one before any sum;
   - toggle fallbacks match the measure's description and the business
     default;
   - entity counts come from the fact, not a dimension;
   - `CALCULATE` filters that silently replace a slicer, BLANK treated as
     zero, ambiguous or bidirectional relationships, a missing or inactive
     date relationship, many-to-many joins that duplicate rows.
4. **Classify** each measure: *correct*, *differs but defensible* (say how),
   or *wrong* (say what number it produces instead, and why).
5. **Use what is correct; fix what is not.** Query correct measures by name
   with DAX, pinning every toggle and required filter explicitly. For a wrong
   measure, show the model's number next to the corrected one, propose the
   corrected DAX (name, format, description), and add it to the model only
   with the user's approval and a write-capable connector.
6. **Tell the user what the connection unlocks**, once: live answers from the
   model's measures; the audit above for any part of the model; proposed or
   applied measure fixes; reconciling a dashboard number with a report; and in
   Claude Code with PBIP in git, model linting, building a model from a spec,
   syncing client models to a template, and styling report charts.

A question the model has no measure for is answered from raw sources only if
the user agrees, labelled as outside the model, with the DAX to add it.

## 2. Map the question to categories

| Category | Typical words | Needs |
|---|---|---|
| Paid search | search ads, Google Ads, Bing, keywords, CPC, impression share, quality score | search campaigns only; display, video, Performance Max and shopping belong to Spend |
| Paid social | Meta, Facebook ads, Instagram ads, TikTok, LinkedIn ads, reach, frequency | one attribution window |
| Spend (cross-platform) | total spend, budget, pacing, blended CPA, MER | one currency, one report level, media vs fees |
| Organic social | posts, followers, engagement rate, page | post vs page level; snapshots vs daily changes |
| Video | YouTube, views, watch time, retention, subscribers | Shorts vs long-form |
| Email campaigns | sends, opens, clicks, CTOR, unsubscribes | delivered as the denominator; unique vs total |
| Email lists | list size, growth, churn | a starting count plus daily changes |
| Web analytics | GA4, sessions, users, conversion rate, landing pages, channels | users are not additive; one key event |
| SEO | Search Console, rankings, organic clicks, queries, pages | query vs query x page; web search type |
| Page speed | Core Web Vitals, LCP, INP, Lighthouse | field vs lab; traffic weighting |
| Competition | competitors, auction insights, keyword volume, share of voice | overlap, not market share |
| CRM / pipeline | leads, MQL, SQL, opportunities, win rate | lifecycle definitions |
| E-commerce / backend | orders, revenue, customers, AOV, refunds | the revenue of record |
| Subscriptions | trials, subscribers, churn, retention, LTV, cohorts | observed cohorts only |

A question can touch several categories ("CAC" = Spend + backend; "is brand
search worth it" = Paid search + SEO + backend). Each category needs its own
source; a category with no source cannot be answered, only described.

## 3. Rewrite the question into a request

Before any query, write the request out and show it in one line:

> Answering: Google Ads, account "Store EU", **search campaigns**, purchases
> (conversion action "purchase", primary conversions), 1-30 Sep 2026 vs 1-31
> Aug 2026, by campaign, campaign-level rows. Data through 30 Sep.

Fill every slot. When the user did not say, pick the default below and state it:

| Slot | Default |
|---|---|
| Date window | the last complete month (exclude today; exclude the last 3 days for Search Console) |
| Comparison | the previous equal period |
| Account | ask if several exist and the question does not imply one; otherwise all, labelled as combined |
| Conversion action | the purchase or primary lead action; never "all actions" |
| Attribution window | the platform's account setting if known; otherwise 7-day click, stated |
| Report level | one level only (campaign for spend; account for reach) |
| Grain | the grain of the answer: monthly users are queried monthly, not summed from days |
| Search type | web |
| Currency | the business's reporting currency, converted with stated rates |

Per-connector tools, parameters, defaults, row limits and traps (ad platforms,
GA4, Search Console, CRMs, email, e-commerce, warehouses, Power BI and Fabric)
are in section "File: route-question/references/connectors.md" in 01-route-and-define.md.

When the connector lets you choose these, choose them in the request; do not
pull everything and fix it afterwards.

## 4. Model before you query

Write the question's data model before the first query, in the shape a
semantic model would take. It is short, and it decides what every query is
allowed to do.

```yaml
facts:
  - name: ads_campaign_day          # one source, one grain
    grain: one row per campaign per day
    source: Google Ads connector, account "Store EU"
    additive: [cost, clicks, impressions]
    non_additive: [search_impression_share]   # never summed; weight by eligible impressions
    selectors: {report_level: campaign, conversion_action: purchase, conversions_column: conversions}
  - name: shop_orders
    grain: one row per order
    source: Shopify export
    additive: [net_revenue]
    keys: [order_date, customer_id]
dimensions:
  - {name: date, grain: day, shared_by: [ads_campaign_day, shop_orders]}
  - {name: channel, shared_by: [ads_campaign_day, shop_orders], key_rule: lower-case, trimmed}
metrics:
  - {name: CPA, formula: sum(cost) / sum(purchases), facts: [ads_campaign_day]}
  - {name: MER, formula: sum(net_revenue) / sum(cost), across: date}   # two facts: aggregate each, then divide
```

The rules the model enforces:

- **One grain per fact.** If a source returns several grains or report
  levels (account, campaign and ad-group rows of the same spend), the
  selector picks one; the others are never in the same sum.
- **Every ambiguous option is a selector with a stated value**: conversion
  action, `conversions` vs `all_conversions`, attribution window, unique vs
  total, report level, search type, lab vs field, currency, media vs fees.
  An unset selector stops the query.
- **Facts meet only through shared dimensions, after aggregation.** A metric
  that needs two facts (CAC, MER, blended ROAS) aggregates each to the shared
  dimension (date, month, channel, campaign key) and then divides. No row to
  row joins.
- **A metric belongs to the facts it names.** If no fact in the model can
  supply a metric's parts, the metric is out of scope (section 5), not
  approximated from another source.
- **Non-additive columns stay at their grain**: users, reach, impression
  share, percentiles, snapshots.

When a database or warehouse is connected, the same model becomes SQL: one
CTE per fact at its grain, then joins on the shared dimensions. When the
source is a connector, the selectors become the request parameters. If the
team has a Power BI model, its tables, measures and toggles are the model:
use the `power-bi-definitions` skill instead of writing one.

## 5. Decide the route

| Outcome | When | What to do |
|---|---|---|
| Answer | every category the question needs has a source | proceed with `metric-definitions`, then the analysis skills |
| Answer partly | some categories have no source, or a metric's parts are in no fact of the model, or the window is not covered | answer what the data supports; list what is missing and what it would add ("CAC needs order data; spend alone gives cost per click") |
| Reframe | the question cannot be answered as asked, but a close one can ("which channel drives sales" without paths -> "which channel's last-click revenue rose") | propose the reframed question in one line and answer that, labelled |
| Onboard | no source at all, or none relevant | say what is connected, which categories it can answer, and which connection or export would answer the question |
| Decline the method | the question asks for something the data cannot support (a forecast from two months, causality from a correlation, LTV from one month of a cohort) | say why in one line and offer the nearest supported answer |

Check freshness: if the latest data is older than the window asked for, say
so and use the latest complete period instead.

## 6. Hand over

Pass the rewritten request (section 3), the model (section 4) and the house
rules that apply (section 0) to the next skill, and repeat its
scope line under the report or dashboard title, so every reader sees what the
numbers cover.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Read house rules | "Did a house rule change a default, a definition or a threshold you then used anyway?" | each default in the scope line checked against the rule list | apply the rule and cite its id |
| Inventory sources | "Is there a source you did not look for (a Power BI model, a warehouse table, a second account)?" | list every tool, connection and file once more, with account and date range | add it; if it is a Power BI model, go to 1a |
| Map to categories | "Does the question need a category with no source (orders for CAC, spend for ROAS)?" | each metric's parts traced to a category with a source | answer partly and say what is missing |
| Rewrite the request | "Which slot did you fill by default without saying so?" | every slot in the scope line has a value and a reason | state the default, or ask |
| Model before query | "Can two facts meet row to row anywhere, or a non-additive column be summed?" | each metric's facts aggregate to a shared dimension first | restructure the model before querying |
| Decide the route | "Is this answer stronger than the data allows?" | each claim maps to a fact in the model | downgrade to answer-partly or reframe |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.

---

## File: route-question/references/connectors.md

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

---

# Skill: metric-definitions

---
name: metric-definitions
description: >-
  Use this skill whenever you compute a marketing metric from data, before writing the
  query or code: CTR, CTOR, open rate, conversion rate, CPA, CAC, ROAS, LTV, repeat rate,
  average position, users, sessions, reach, frequency, watch time, list size, retention,
  churn, Core Web Vitals, keyword volume and spend, from GA4, Search Console,
  Google Ads, Meta, YouTube, Facebook pages, email platforms, HubSpot or other CRMs,
  Shopify, subscription billing, Lighthouse/CrUX or a warehouse. It holds the correct formula, the grain each metric is valid at and the trap
  that makes it lie (averaged rates, daily users summed into monthly users, unweighted
  position, two tables joined row to row, platform revenue double-counted), plus tested
  SQL patterns. Also use it when the user asks how a metric is defined or why two numbers
  disagree. The team's house rules (a house-rules/ folder) are read first and override
  these defaults.
---

# metric-definitions

Most broken dashboards do not look broken. The total is right and the rows are
wrong, or every number is right and the comparison is wrong. This skill is the
definition layer: decide what each number means, at what grain, from which
source, before any chart exists.

## 0. Read the house rules first

Before the dictionary, read the team's house rules: every `.md` file in a
`house-rules/` folder at the root of the project or workspace, except
`README.md`, `TEMPLATE.md` and `examples/` (fictional, never applied). In a
chat without files, use rules the user pasted, uploaded or keeps in the
project's knowledge. If `route-question` already listed them, use its list.

Precedence, highest first: what the user says in this conversation; the
team's house rules; the team's governed definitions (a Power BI model, a
metric dictionary); the shipped catalog and traps in this skill. A house rule
that defines a metric, a revenue of record, a conversion action, a filter or
a threshold replaces the catalog entry it names in `overrides:`, or the one it
contradicts. It cannot make an averaged rate or a summed distinct count
correct: if it seems to, report its number, show the core-rule number beside
it and say why they differ. In the dictionary, put the rule's id in the
Caveat column of every metric it changed.

## 1. Write the metric dictionary first

Before querying, write a short dictionary for the metrics the dashboard needs,
and show it with the dashboard (as a "Definitions" panel):

| Metric | Formula | Source | Grain | Filters | Format | Caveat |
|---|---|---|---|---|---|---|
| CTR % | unique clicks / delivered | Klaviyo campaign report | per send, summed | campaigns only, no flows | 0.0% | not clicks / opens; that is CTOR |
| CAC | paid acquisition spend / new customers | Google Ads + Meta spend; Shopify first orders | month | excludes brand search | $0 | platform spend, no agency fees |

Take formulas and caveats from section "File: metric-definitions/references/catalog.md" in 01-route-and-define.md,
the per-platform export traps from
section "File: metric-definitions/references/source-traps.md" in 01-route-and-define.md, CRM and lifecycle
definitions from section "File: metric-definitions/references/crm-lifecycle.md" in 01-route-and-define.md, and organic
social goals and KPIs from section "File: metric-definitions/references/organic-social.md" in 01-route-and-define.md.
If the team has a Power BI model, its definitions win over this catalog
(house rules still win over both): use the `power-bi-definitions` skill. If the user or a Claude Project already has a
metric dictionary, use it and say so.

Offer to save the dictionary as `metric-dictionary.md` in the user's Claude
Project, so the next dashboard uses the same definitions.

## 2. The rules

These come from Power BI modelling practice. They hold in any SQL, any
spreadsheet, any connector.

1. **One grain per table, stated.** "One row per campaign per day." Every
   aggregation starts from knowing it.
2. **Ratios are computed from summed parts at the grain shown.**
   `SUM(clicks) / SUM(impressions)`, never `AVG(ctr)`. An average of rates is a
   number true of nothing.
3. **Never join two facts row to row.** Aggregate each source to the shared keys
   (date, campaign, channel) first, then join. Joining spend rows to order rows
   multiplies spend.
4. **Count entities from the fact.** Customers who ordered =
   `COUNT(DISTINCT orders.customer_id)` in the filtered orders, not a count of
   the customers table.
5. **Know what does not add up.** Distinct counts (GA4 users, reach, unique
   customers) cannot be summed across days, channels or campaigns. Query them at
   the grain displayed, or show sessions instead.
6. **Weighted averages are weighted.** Search Console average position is
   impression-weighted: `SUM(position * impressions) / SUM(impressions)`.
7. **Pin one conversion event** before any CVR, CPA or ROAS. Sign-ups and
   purchases are never summed.
8. **Never stack platform-reported numbers.** Google Ads and Meta both claim the
   same sale. Sum platform revenue only with a warning, or use one shared
   denominator (backend or analytics revenue).
9. **Blank is not zero.** No data is "no data"; zero is a measurement. Divide
   with a zero guard (`NULLIF(x, 0)`) and show blanks as blanks.
10. **Complete periods only.** Exclude today, the Search Console lag, and the
    ad platforms' open conversion window; say what was excluded.
11. **Split before judging.** Brand vs generic, prospecting vs retargeting, new
    vs returning, device, country. A blended rate moves when the mix moves.
12. **Every metric has a description of what it measures.** If you cannot write
    one sentence, the metric is not ready to show.
13. **Overlapping columns are alternatives, never addends.** Pick one and say
    which: Meta attribution windows (`n_1d_click`, `n_7d_click`, `n_28d_click`,
    view windows: each contains the shorter ones), `conversions` vs
    `all_conversions`, total vs unique clicks and opens, `report_level` rows
    (account, campaign, ad group rows repeat the same spend), query rows vs
    query x page rows, web vs image vs video search types. If an export has a
    column like these, filter or choose before any SUM.
14. **Levels are not flows.** Followers, fans, list members, subscribers and
    active installs are snapshots: take the end value, or sum the daily change
    column from a starting count. A column that is already a daily net change
    is summed, never read as a level. Growth rate = net change / level at the
    start of the period; gross new sign-ups are not growth.
15. **One system per ratio.** Numerator and denominator come from the same
    source: GA4 purchases / GA4 sessions, ad-platform conversions / ad clicks.
    When joining systems on a campaign name, normalise the key (case, spaces,
    `-` vs `_`) and report the rows that did not match.
16. **Averages carry their weights.** Average view duration = minutes watched
    x 60 / views; engagement rate = total engagements / total reach; position =
    impression-weighted. Never the mean of a column of per-row averages or
    rates. Keep unlike formats apart (Shorts vs long-form video, image vs web
    search) before averaging, and compare retention across videos of different
    length by % viewed, not seconds.
17. **Cohorts are read only where observed.** A cohort grid exported with
    zeros for months not yet reached is censored, not churned: average month-N
    retention only over cohorts at least N months old, weighted by cohort size.
    Churn = cancellations in the month / customers active at its start (not all
    customers ever). Follow trials as a cohort into later months: CAC = spend /
    paying customers from that cohort, not per trial and not only conversions
    dated in the same month. LTV uses gross margin, churn and a discount rate;
    compare it with CAC before approving spend.
18. **Money is in one currency and one unit.** Convert with stated rates,
    divide `*_micros` by 1,000,000, and keep media spend apart from fees,
    payroll or other manual expense rows.
19. **Percentiles and thresholds do not average.** A site's p75 LCP is not the
    mean of page p75s. Use field (real-user) data over lab data, drop failed
    audits, take the latest date, and weight pass/fail by traffic (share of
    sessions on passing pages).
20. **Repeated attributes are counted once.** A value repeated on every row of
    an entity (keyword volume on every SERP result row, a monthly budget on
    every day) is taken once per entity and period, then summed.

## 3. Query with the safe patterns

section "File: metric-definitions/references/sql-patterns.md" in 01-route-and-define.md has tested shapes for
the cases that go wrong most: rates from parts, two sources joined after
aggregation, period over period with explicit date ranges, impression-weighted
position, the cohort triangle, new vs returning, budget pacing, and
platform-vs-backend reconciliation. Adapt them to the warehouse dialect.

When the data comes from a connector rather than SQL (an API returning rows),
apply the same rules in code: request the grain you will display, sum parts,
divide last.

## 4. Check before showing

- Recompute one total two ways (for example sum of channel rows vs the
  account total) and say whether they match.
- Funnels run downhill: delivered ≤ sent, clicks ≤ impressions, conversions ≤
  clicks (on the same scope). A step that runs uphill is a scope or definition
  error.
- Platform totals vs backend totals: show the gap when both are available.
- Volume next to every rate. A 12% CVR on 25 clicks is not a finding.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Write the dictionary | "Could two readers compute this metric differently from your definition?" | formula, grain, filters and source all filled | tighten the definition |
| Pick the grain | "Is any column in this sum non-additive or overlapping (users, reach, windows, report levels)?" | rules 5 and 13-20 checked against every column used | query at the right grain or pick one column |
| Join sources | "Did two facts meet before aggregation?" | recompute one total two ways (sum of rows vs source total) | aggregate each source first, then join |
| Compute rates | "Is any rate an average of rates or a ratio across two systems?" | numerator and denominator from the same system, summed | recompute from parts |
| Show the number | "What would make this number wrong that the reader cannot see?" | volume beside every rate; exclusions stated | add the caveat or the volume |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.

---

## File: metric-definitions/references/catalog.md

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

---

## File: metric-definitions/references/crm-lifecycle.md

# CRM, lifecycle and pipeline metrics

The playbooks do not cover CRM pipelines, so most definitions here are standard
practice **[std]**; lines from the author's notes are marked *(notes)*. Applies
to HubSpot, Salesforce and similar CRMs.

## Grain first

A CRM holds three different grains. Never mix them in one ratio without saying
so.

| Object | One row per | Typical questions |
|---|---|---|
| Contact (lead) | person | how many leads, MQLs, SQLs; conversion between stages; lead source |
| Company (account) | organisation | accounts engaged, accounts with pipeline (account-based marketing) |
| Deal (opportunity) | sales opportunity | pipeline value, win rate, deal size, cycle length |

A contact can have several deals; a deal can have several contacts. Counting
"leads that became customers" goes through the association, and double-counts
if a contact sits on two deals.

## Lifecycle stages are a ratchet

HubSpot lifecycle stages (subscriber, lead, MQL, SQL, opportunity, customer,
evangelist) normally only move forward, and contacts can skip stages. A
snapshot of the *current* stage undercounts everyone who passed through a stage
and moved on.

- **Count by the date the stage was entered** (HubSpot keeps one timestamp
  property per stage), not by today's stage.
- **Cohort by creation month**: a lead created last week has not had time to
  become an opportunity. Compare stage conversion at the same age, the way
  cohorts are compared in customer analytics.
- A contact that skipped MQL and went straight to SQL counts as reaching MQL
  for funnel conversion (it passed the threshold), or is reported separately;
  say which.

## Definitions

| Metric | Formula | Caveat |
|---|---|---|
| New leads | contacts created in the period (excluding imports, test and internal contacts) | Imports and list uploads inflate it; filter by creation source |
| MQLs | contacts that entered MQL in the period | The MQL rule is the company's own; state it |
| Stage conversion (N to N+1) | contacts in a creation cohort that reached stage N+1 / contacts in that cohort that reached stage N | Same cohort, same age; never this month's SQLs / this month's MQLs |
| Lead-to-customer rate | cohort contacts that became customers / cohort leads | Long cycles: report at 30 / 90 / 180 days |
| Pipeline created | sum of amount of deals created in the period | Deals without amount: count them and report the gap |
| Open pipeline | sum of amount of open deals at a date | A stock, not a flow: never sum across months |
| Win rate | closed-won / (closed-won + closed-lost), by close date | Excluding open deals; state whether by count or by value |
| Average deal size | closed-won amount / closed-won deals | |
| Sales cycle length | median days from deal creation to close (won) | Median, not mean: a few stalled deals skew the mean |
| Pipeline velocity | open opportunities x win rate x average deal size / sales cycle length (days) | Revenue per day the current pipeline should produce |
| Pipeline coverage | open pipeline due in the period / revenue target for the period | Coverage of 3x is a common heuristic, not a law |
| Cost per lead / MQL / SQL | marketing spend / leads (MQLs, SQLs) in the period | Join spend after aggregation, by source and month |
| Cost per opportunity, CAC (B2B) | spend / opportunities created; spend / new customers | Lag: this month's spend creates next quarter's customers. Use a lagged or cohort view, and say which |
| Revenue per lead by source | closed-won amount from a source cohort / leads in that cohort | The honest way to compare sources: volume x quality |

## Source attribution in the CRM

- **Original source** (first known touch) and **latest source** answer
  different questions: what introduced the lead vs what brought them back.
  Name the one you use.
- *(notes)* For long B2B cycles, a W-shaped model gives 30% to the first touch,
  30% to the lead-creation touch (form fill, demo request), 30% to the touch
  that created the opportunity or closed it, and 10% across the rest. Any model
  is credit, not cause.
- Join ad spend to CRM sources on a mapped source name (paid search, paid
  social, organic, email, referral, direct), aggregated per month, never row by
  row.

## Insight patterns

- **MQLs up, SQLs flat**: the MQL rule loosened, or a new source sends volume
  without fit. Check stage conversion by source.
- **Win rate down, pipeline up**: quality traded for volume. Check win rate by
  source and deal size band.
- **Cycle length stretching**: deals stalling at one stage. Find the stage with
  the largest rise in median days.
- **Cost per lead falling, cost per opportunity rising**: cheap leads that do
  not progress. Judge sources on cost per opportunity or revenue per lead.
- *(notes)* "Potential is a ceiling, forecast is a bet, quota is a goal." Set
  targets against potential, not against last year's result.
- *(notes)* Judge a team only on the stages it controls: marketing on lead
  volume and quality, sales on conversion after acceptance.

---

## File: metric-definitions/references/organic-social.md

# Organic social: goal first, then the KPI

Organic social is judged against the business goal it serves, not by whatever
number grew. Ask which goal the account is for, then read only that goal's
KPIs, in funnel order.

| Goal | KPIs | Read it as | Trap |
|---|---|---|---|
| Awareness | follower growth (net: follows - unfollows), reach, impressions, social traffic, share of voice | reach = unique people, impressions = screen appearances; impressions / reach = how often the same people saw it | big impressions on flat reach is the same fans again, not discovery; follower counts are snapshots, growth is the change |
| Engagement | engagement rate, shares, comments, brand mentions (tagged and untagged), sentiment, video completion | engagement rate = total engagements / total reach (or impressions; say which), pooled across posts | averaging per-post rates lets tiny posts win; likes are the cheapest signal, shares the strongest |
| Traffic | link clicks, sessions from social (UTM-tagged), conversions after the visit, sign-ups, trials | clicks are the platform's count; sessions are the analytics tool's; never divide one by the other | untagged links land in "direct"; without UTMs social's traffic is invisible |
| Leads and sales | revenue, lead conversion rate, non-revenue conversions, sign-ups | name the attribution model; organic social rarely gets last click | last-click revenue on organic posts undercounts them; do not cut a channel on it alone |

## Engagement is a ladder

From weakest to strongest signal: clicks, reactions and likes, comments,
shares and saves. A share puts the brand in front of someone else's audience;
a like costs nothing. When formats compete, compare them on shares and
comments per reach, not likes.

## Brand health, measured continuously

1. **Listening**: brand and product names, common misspellings and category
   keywords, tagged and untagged; sentiment as a trend, not a single score.
2. **Benchmarking**: share of voice = your mentions / all mentions in the
   category (you plus named competitors). A drop in your mentions with a flat
   share of voice is a category shift, not a brand problem.
3. **Inbound comments and messages as data**: tag them by topic (support,
   product feedback, feature requests, pricing) and report tag volumes over
   time; that shows what drives negative and positive sentiment.

## Distinctions to hold

- Reach is not impressions; organic reach is not paid reach (report them
  apart).
- Organic KPIs (reach, engagement rate, follower growth) are not paid KPIs
  (CTR, CPC); do not judge one with the other's.
- A creator is paid for the content asset (judge the asset's performance
  wherever it runs); an influencer is paid for distribution and persuasion
  (judge reach into a new audience, tracked links or codes, and incremental
  sales).
- Brand-specific shifts are not category-wide shifts: only share of voice
  against competitors tells them apart.

---

## File: metric-definitions/references/source-traps.md

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

---

## File: metric-definitions/references/sql-patterns.md

# Safe SQL patterns for marketing metrics

Written in portable SQL (tested on DuckDB). Dialect notes at the end. Table and
column names are placeholders: map them to the warehouse, keep the shape.

## 1. Rates from parts, at the grain shown

```sql
SELECT campaign,
       SUM(clicks)                                   AS clicks,
       SUM(impressions)                              AS impressions,
       SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0) AS ctr
FROM ad_daily
WHERE day BETWEEN DATE '2026-09-01' AND DATE '2026-09-30'
GROUP BY campaign;
```

Never `AVG(ctr)`. For a total row, recompute from the summed parts, not from the
campaign rows' rates.

## 2. Two sources: aggregate each, then join (CAC, ROAS on backend revenue)

```sql
WITH spend AS (
  SELECT DATE_TRUNC('month', day) AS month, SUM(cost) AS spend
  FROM ad_daily                      -- Google Ads + Meta, already unioned
  GROUP BY 1
),
customers AS (
  SELECT DATE_TRUNC('month', order_date) AS month,
         COUNT(DISTINCT customer_id)   AS new_customers,
         SUM(net_revenue)              AS first_order_revenue
  FROM orders
  WHERE is_first_order
  GROUP BY 1
)
SELECT COALESCE(s.month, c.month)                     AS month,
       s.spend,
       c.new_customers,
       s.spend / NULLIF(c.new_customers, 0)          AS cac
FROM spend s
FULL OUTER JOIN customers c ON c.month = s.month
ORDER BY 1;
```

The shared key (month, or month and channel) must exist in both CTEs at the same
grain. To split by channel, the orders side needs an acquisition-channel column
that uses the same channel names as the spend side; map them explicitly.

## 3. Period over period with explicit ranges

```sql
WITH periods AS (
  SELECT 'current'  AS period, DATE '2026-09-01' AS d0, DATE '2026-09-30' AS d1
  UNION ALL
  SELECT 'previous',           DATE '2026-08-02',       DATE '2026-08-31'  -- same 30 days, same weekdays
)
SELECT p.period, SUM(f.clicks) AS clicks, SUM(f.conversions) AS conversions,
       SUM(f.conversions) * 1.0 / NULLIF(SUM(f.clicks), 0) AS cvr
FROM periods p
JOIN ad_daily f ON f.day BETWEEN p.d0 AND p.d1
GROUP BY p.period;
```

Do not use `LAG()` over monthly rows: a missing month silently shifts the
comparison. Match weekdays for weekly businesses; say when months differ in
length.

## 4. Impression-weighted average position (Search Console)

```sql
SELECT page,
       SUM(clicks)                                          AS clicks,
       SUM(impressions)                                     AS impressions,
       SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0)      AS ctr,
       SUM(position * impressions) / NULLIF(SUM(impressions), 0) AS avg_position
FROM gsc_page_query_daily
GROUP BY page;
```

Query-page rows double-count impressions when two of your pages show for one
search: use the query-level (or page-level) table for totals, the query-page
table for cannibalization.

## 5. Non-additive counts (GA4 users, reach)

Request users from the source at the exact grain displayed (the month total,
the channel total). Never sum daily users into a monthly number:

```sql
-- wrong: SUM(daily_users) counts the same person once per day they visited
-- right: monthly users come from a monthly query to GA4, stored at that grain
SELECT month, channel, users      -- as returned by GA4 for (month, channel)
FROM ga4_monthly_channel;
```

If only daily data exists, show sessions, and label users "not available at this
grain".

## 6. Cohort triangle (retention by months since first order)

```sql
WITH first_orders AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders GROUP BY 1
),
activity AS (
  SELECT f.customer_id,
         DATE_TRUNC('month', f.first_date) AS cohort,
         DATE_DIFF('month', DATE_TRUNC('month', f.first_date), DATE_TRUNC('month', o.order_date)) AS age
  FROM orders o JOIN first_orders f USING (customer_id)
),
sizes AS (SELECT cohort, COUNT(DISTINCT customer_id) AS n FROM activity WHERE age = 0 GROUP BY 1)
SELECT a.cohort, a.age,
       COUNT(DISTINCT a.customer_id) * 1.0 / s.n AS retained_share
FROM activity a JOIN sizes s USING (cohort)
GROUP BY a.cohort, a.age, s.n
ORDER BY 1, 2;
```

Compare cohorts down a column (same age), never across. Young cohorts have
empty cells, not low values. Cumulative revenue per customer uses the same frame
with `SUM(net_revenue) / n` accumulated over age.

## 7. New vs returning revenue

```sql
SELECT DATE_TRUNC('month', o.order_date) AS month,
       SUM(CASE WHEN o.order_date = f.first_date THEN o.net_revenue END) AS new_revenue,
       SUM(CASE WHEN o.order_date > f.first_date THEN o.net_revenue END) AS returning_revenue
FROM orders o JOIN (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY 1) f
  USING (customer_id)
GROUP BY 1 ORDER BY 1;
```

First order = the customer's earliest order in all history, not in the filtered
period.

## 8. Budget pacing (per campaign, not account)

```sql
SELECT campaign,
       SUM(cost)                                                   AS mtd_spend,
       SUM(CASE WHEN day > CURRENT_DATE - 8 AND day < CURRENT_DATE THEN cost END) / 7.0 AS avg_daily_7d,
       SUM(cost) + SUM(CASE WHEN day > CURRENT_DATE - 8 AND day < CURRENT_DATE THEN cost END) / 7.0
                 * (DATE_DIFF('day', CURRENT_DATE, LAST_DAY(CURRENT_DATE)) + 1) AS projected_eom
FROM ad_daily
WHERE day >= DATE_TRUNC('month', CURRENT_DATE) AND day < CURRENT_DATE
GROUP BY campaign;
```

Projection = month-to-date spend + trailing 7-day average x days remaining
(including today). Compare with each campaign's monthly budget; the account
total hides a starved winner next to an overspending loser.

## 9. Platform vs backend reconciliation

```sql
WITH platform AS (
  SELECT DATE_TRUNC('week', day) AS week, SUM(conversion_value) AS platform_revenue
  FROM ad_daily GROUP BY 1
),
backend AS (
  SELECT DATE_TRUNC('week', order_date) AS week, SUM(net_revenue) AS backend_revenue
  FROM orders GROUP BY 1
)
SELECT COALESCE(p.week, b.week) AS week, p.platform_revenue, b.backend_revenue,
       p.platform_revenue / NULLIF(b.backend_revenue, 0) AS claimed_share
FROM platform p FULL OUTER JOIN backend b ON b.week = p.week
ORDER BY 1;
```

A claimed share above 1.0 means the platforms claim more revenue than the store
made: overlapping attribution. Show it; do not hide it in a blended ROAS.

## Dialect notes

| Need | DuckDB / Postgres | Snowflake | BigQuery | Databricks |
|---|---|---|---|---|
| Month start | `DATE_TRUNC('month', d)` | `DATE_TRUNC('MONTH', d)` | `DATE_TRUNC(d, MONTH)` | `date_trunc('MONTH', d)` |
| Monday week start | `DATE_TRUNC('week', d)` | `DATE_TRUNC('WEEK', d)` (WEEK_START=0/1) | `DATE_TRUNC(d, ISOWEEK)` | `date_trunc('WEEK', d)` |
| Months between | `DATE_DIFF('month', a, b)` (DuckDB); `(EXTRACT(YEAR FROM age(b,a))*12 + EXTRACT(MONTH FROM age(b,a)))` (Postgres) | `DATEDIFF('month', a, b)` | `DATE_DIFF(b, a, MONTH)` | `months_between(b, a)` (fractional: wrap in `floor`) |
| Safe divide (blank on zero) | `x / NULLIF(y, 0)` | `x / NULLIF(y, 0)` (not `DIV0NULL`, which returns 0) | `SAFE_DIVIDE(x, y)` | `try_divide(x, y)` |
| Last day of month | `LAST_DAY(d)` | `LAST_DAY(d)` | `LAST_DAY(d)` | `last_day(d)` |

---

## File: house-rules/README.md

# House rules

The shipped checks know what goes wrong in most marketing data. They cannot
know what goes wrong in yours: that your revenue of record is finance net
revenue, that campaigns starting `BR_` are brand, that your payment page
lives on another domain, that the "purchase" key event double-fired for a
month last spring. A senior analyst carries those in their head. House rules
write them down, so the agent reads them before it touches a number and a new
colleague does not have to learn them the expensive way.

## How the agent uses them

`route-question` and `metric-definitions` read house rules first, before the
inventory and before any metric is defined. They look for a `house-rules/`
folder at the root of the project or workspace the agent is working in and
read every `.md` file there except `README.md`, `TEMPLATE.md` and anything in
`examples/`. In a chat without files (Claude web, ChatGPT), paste the rules or
add them to the project's knowledge.

The folder in this plugin holds only this README, the template and two
fictional examples. Nothing in it is applied to your data.

## Precedence

Highest first:

1. What you say in the conversation.
2. Your house rules.
3. Your governed definitions: a Power BI model (`power-bi-definitions`), a
   metric dictionary.
4. The shipped defaults: the skills, their checks and catalogs.

A house rule replaces the shipped check or definition it names in
`overrides:`, and any default it contradicts. One thing it cannot do is make
arithmetic true that is false. If a rule seems to require averaging rates or
summing daily users, the agent reports the rule's number, shows the
core-rule number next to it and says why they differ. Findings and scope
lines cite the rule id that changed them, so you can always see where a
number came from.

## Writing one

Copy section "File: house-rules/TEMPLATE.md" in 01-route-and-define.md to `house-rules/HR-<number>-<short-name>.md`
in your own project, one rule per file. The fields are the same columns as the
shipped audit tables (what to check, where to look, the red flag, why it costs
money, the fix), plus a source, an owner and a date. Two examples:

- [HR-001](https://github.com/C-Kapsalis/devils-analyst/blob/main/house-rules/examples/HR-001-revenue-of-record.md) replaces a shipped default:
  ROAS is computed on finance net revenue, not store gross revenue.
- [HR-002](https://github.com/C-Kapsalis/devils-analyst/blob/main/house-rules/examples/HR-002-checkout-domain-referrals.md) adds a check the
  shipped GA4 checks cannot know: the team's payment domain showing up as a
  referral source.

Write the red flag so two analysts would agree whether it fired: a number, a
column, a condition. "Engagement looks off" is not a red flag; "engagement
rate steps down more than 5 points in a week with no change in users" is.

## Growing them

- **After an incident.** When a number was wrong and someone found out why,
  that is a rule. Write it the same week, with the incident as its source.
- **After a review.** When a reviewer corrects an analysis for a reason the
  checks did not cover, ask whether it is a one-off or a rule.
- **On a date.** Each rule carries the date it was last confirmed. Re-read
  the old ones each quarter: a renamed column or a retired setting makes a
  rule wrong without anyone noticing, and the agent flags such rules to their
  owner instead of applying them.
- **Upstream.** A rule that would hold for most teams (not just yours) belongs
  in the shipped checks. [CONTRIBUTING.md](https://github.com/C-Kapsalis/devils-analyst/blob/main/CONTRIBUTING.md) says how to
  propose it, with a benchmark case that plants the problem.

A planned, optional loop that proposes house-rule changes from your own past
analyses, one at a time and only with your approval, is described in
[docs/self-improving.md](https://github.com/C-Kapsalis/devils-analyst/blob/main/docs/self-improving.md). It is not built yet.

---

## File: house-rules/TEMPLATE.md

---
id: HR-000
area: paid-search
overrides: none
check: One sentence that says what to check.
where_to_look: The column, setting or report, with its exact name and where it lives.
red_flag: The threshold that makes it a finding, as a number or a condition you can test.
why_it_costs_money: What goes wrong in a decision, a budget or a report if nobody checks.
fix: What to do when the red flag shows, and how to verify the fix.
source: Where this comes from (an incident, a platform doc, a finance policy), with a link or a date.
owner: Who answers questions about this rule (a name or a role).
date: YYYY-MM-DD
---

<!--
One rule per file. Save it as house-rules/HR-<number>-<short-name>.md in your
own project, not in this plugin's folder.

Fields:

- id: unique within your rules, for example HR-014. Findings cite it.
- area: one of paid-search, pmax, meta, ga4-utm, search-console, email,
  crm-lifecycle, ecommerce-revenue, experiments, attribution, dashboards,
  power-bi, or a new area your team uses.
- overrides: the shipped check or definition this rule replaces, as
  <file>:<check id> (for example audit/ga4-utm:GA2, or
  metric-definitions/catalog:ROAS), or "none" for a new check.
- check, where_to_look, red_flag, why_it_costs_money, fix: the same columns
  as the shipped audit tables (Look at, Red flag, Why it costs money, Fix).
  Write the red flag so two analysts would agree whether it fired.
- source: an incident, a document, a decision. "We have always done it this
  way" is not a source.
- owner and date: who to ask, and when it was last confirmed true. A rule
  that names a column or setting that no longer exists gets flagged to its
  owner, not applied.

Optional body below the frontmatter: two or three sentences of context, the
query that tests the red flag, or the incident that taught the team.
-->
