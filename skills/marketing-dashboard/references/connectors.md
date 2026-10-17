# Sources: what to request, at what grain, and what each cannot tell you

Use whatever connector the user has (a native connector, an MCP server, a data
pipeline into a warehouse, or a CSV export). Field names below are the source's
own API names; connectors sometimes rename them, so match by meaning. Request
the grain you will display: anything marked *not additive* cannot be summed
afterwards.

## GA4 (Google Analytics 4)

- **Typical request**: date x session default channel group (or source /
  medium / campaign) x landing page, with `sessions`, `engagedSessions`,
  `keyEvents` (named conversions), `ecommercePurchases` or `transactions`,
  `purchaseRevenue` or `totalRevenue`.
- **Not additive**: `totalUsers`, `newUsers`, `activeUsers`. Request them at the
  exact grain shown (the month, the channel), never sum daily users.
- **Scopes do not mix**: session-scoped dimensions (`sessionDefaultChannelGroup`)
  and user-scoped ones (`firstUserDefaultChannelGroup`) answer different
  questions. Pick one per table and name it.
- **Cannot tell you**: cost (ROI needs the ad platforms), margin, offline
  revenue, anything before consent (sessions run below Search Console clicks).
- **Watch for**: `(not set)` and `(other)` rows (missing values, high
  cardinality), thresholding of small user counts when Google Signals is on,
  the attribution model in the property settings, data still processing for the
  last 24-48 hours.

## Search Console

- **Typical request**: date x query x page (plus country, device), with
  `clicks`, `impressions`, `ctr`, `position`. Keep a query-level table and a
  page-level table; use query x page only for cannibalization.
- **Not additive**: `position` (impression-weighted average; recompute as
  sum(position x impressions) / sum(impressions)). `ctr` (recompute from parts).
  Impressions in query x page rows double-count when two of your pages show.
- **Cannot tell you**: conversions or revenue (join to GA4 organic landing pages,
  and read shape, not sums: the systems never reconcile), anonymized rare
  queries (query tables sum to less than the property total).
- **Watch for**: 2-3 day lag (drop the last days or request final data only),
  16 months of history, row limits per request (page through results), property
  vs page aggregation giving different totals.

## Google Ads

- **Typical request**: date x campaign (x ad group), with cost (`cost_micros`
  divided by 1,000,000), `impressions`, `clicks`, `conversions`,
  `conversions_value`; campaign type (`advertising_channel_type`, for
  Performance Max); impression share, lost to rank, lost to budget for search
  campaigns; the search terms view for waste.
- **Conversions are by click date** by default: the last 7-30 days keep growing
  as late conversions arrive (conversion lag). Compare complete windows or say
  the recent CPA is provisional.
- **Pin the conversion action**: the default `conversions` column may include
  micro-conversions; filter to the purchase or qualified-lead action.
- **Cannot tell you**: margin, backend revenue, what other channels claim for
  the same sale.
- **Watch for**: impression share bucketed below 10% and above 90%, the
  search-terms report showing only a sample of terms, daily spend up to twice
  the daily budget.

## Meta Ads (and other paid social)

- **Typical request**: date x campaign x ad set (x ad), with `spend`,
  `impressions`, `reach`, `frequency`, `inline_link_clicks`, purchase actions
  and action values.
- **Not additive**: `reach` and `frequency` across days or ad sets.
- **Attribution window**: Meta reports conversions on its own window (commonly
  7-day click and 1-day view); state the window and keep it the same across
  periods. Meta's purchases will exceed GA4's.
- **Split by job**: prospecting vs retargeting (from campaign naming or
  audience settings) before any ROAS.

## HubSpot (and other CRMs)

- **Contacts**: lifecycle stage, the date each stage was entered (HubSpot keeps
  a timestamp property per stage), original source, create date.
- **Deals**: pipeline, stage, amount, create date, close date, closed-won flag,
  associated contacts or companies.
- **Count by entry date into each stage**, not by today's stage: a lead created
  last week has not had time to become an opportunity. Cohort by creation month.
- **Cannot tell you**: ad cost (join spend after aggregating, by source and
  month), anonymous web behaviour.
- **Watch for**: contacts skipping stages (count transitions, not current
  stage), deals without amounts, multiple pipelines with different stages.

## Email platforms (Klaviyo, Mailchimp, Brevo, HubSpot email)

- **Typical request**: one row per campaign send (and per flow message): sent
  (recipients), delivered, bounces, unique opens, unique clicks,
  unsubscribes, spam complaints, attributed orders and revenue, send date,
  audience or segment.
- **Opens are inflated** by privacy protection (machine opens) and image
  prefetching: trend only, never the primary KPI.
- **Attributed revenue** uses the platform's own window (check the account
  setting); it overlaps with paid and organic credit. Prefer revenue matched in
  analytics by campaign name when tagging is consistent.
- **Campaigns vs flows**: report separately; flows run continuously and
  out-earn campaigns per recipient.

## Shopify (and other order systems)

- **Orders**: created date, customer id, gross sales, discounts, returns or
  refunds, net sales, currency, cancelled and test flags, landing site or UTM
  fields when present.
- **Net revenue** = gross minus discounts minus refunds; exclude cancelled and
  test orders. State whether tax and shipping are in.
- **First order** = the customer's earliest order in all history. Needed for
  CAC, new vs returning, cohorts.
- This is the **shared denominator** for revenue across channels: platforms
  claim, the order system counts.

## A warehouse (Snowflake, Databricks, BigQuery, Redshift)

Data loaded by a pipeline (Fivetran, Airbyte, Stitch, a Google transfer) keeps
the source's grain and names, often in one schema per source. Find the
reporting tables (daily campaign stats, GA4 export, orders) before raw event
tables. If a Power BI model sits on the same tables, use its definitions
(`power-bi-definitions`).

## No connector

Ask for CSV exports with the columns above at the grain stated, one file per
source. Say which columns are required for the question and which are optional.
