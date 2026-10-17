# Layouts by question

Each layout follows the shared skeleton (answer title, KPI row, what changed,
where, what to do, definitions). Below: what goes in each slot for the most
common marketing questions. Read sections in the order listed; the order is the
reading order a practitioner uses (hygiene before growth, fine-tuning last).

## Weekly marketing pulse (cross-channel, for a lead or an executive)

- **KPIs**: revenue (or qualified leads), new customers, blended CAC or cost per
  qualified lead, marketing spend, conversion rate. Week vs prior week and vs
  the 8-week average.
- **What changed**: bridge from last week's revenue to this week's by channel.
- **Where**: channel table (spend, sessions, conversions, revenue on one shared
  denominator, CAC), sorted by contribution to the change. Platform-reported
  ROAS in a separate, labelled column.
- **Watch list**: budget pacing per campaign (projected month-end vs budget),
  anything inside the noise band muted.
- **What to do**: at most three findings.

## Paid search (Google Ads, Microsoft Ads)

Order: showing up, earning the click, paying back.

- **KPIs**: spend, conversions (one pinned event), CPA, conversion value or
  ROAS (revenue and, when margin is known, profit), impression share on core terms.
- **Brand vs generic** split of every KPI, side by side; flag brand queries
  leaking into generic campaigns.
- **Impression share**: lost to rank vs lost to budget, per campaign. A
  converting campaign losing share to budget is the clearest "raise the cap".
- **Spend efficiency**: cost per sale by match type; zero-conversion search
  terms clustered by intent (the waste list).
- **Pacing**: month-to-date, trailing 7-day average, projected month-end per campaign.
- **Device and time**: last, and only when bids are manual.

## Performance Max and paid media (display, YouTube, Demand Gen)

- **KPIs**: spend, conversions on one purchase lens, conversion value, ROAS,
  CPM. Filter PMax by campaign type, not by name.
- **Clicks vs CPC by month** on one chart (two lines, shared x-axis, separate
  y-axes clearly labelled): clicks rising with CPC is bought growth.
- **Branded vs non-branded conversions** inside PMax (cannibalization).
- **Reach quality**: viewable rate, placement report, quartile completion for
  video, frequency.
- **Measured vs platform ROAS** per campaign: own-analytics value over cost next
  to the platform's figure.

## Paid social (Meta, TikTok, LinkedIn)

- **Split by job**: prospecting and retargeting in separate columns; never one
  blended ROAS.
- **KPIs per job**: spend, CPM, reach, frequency, link CTR, CPA, ROAS on one
  attribution window (state it).
- **Fatigue**: frequency and CTR on one weekly chart per top ad set.
- **Creative table**: ads ranked by spend, with CTR, CPA and frequency; mute
  ads below a minimum spend.

## SEO (Search Console with GA4)

Order: showing up, earning the click, paying back, pipeline.

- **KPIs**: organic clicks, impressions, CTR, impression-weighted position,
  organic conversions (from GA4). Brand vs non-brand split of clicks and conversions.
- **CTR vs position** scatter by query, with zones: 1-3 (defend, rewrite the
  snippet when CTR is soft), 4-20 (push rank), 50+ (leave alone).
- **Landing pages**: joined page funnel (impressions, clicks, sessions,
  engagement rate, conversions), sorted by opportunity not by clicks.
- **Pipeline**: new pages per month, newly ranking queries, sitemap pages with
  zero impressions.
- **AI answers**: LLM-referred sessions as a share of total, by month.

## Email (Klaviyo, Mailchimp, Brevo, HubSpot email)

Order: delivery, engagement, revenue, list health.

- **KPIs**: delivered rate, CTR, CTOR, revenue per recipient, net list growth.
  Opens only as a trend, labelled "inflated by privacy protection".
- **Send table**: one row per send with delivered, CTR, CTOR, orders, revenue,
  revenue per recipient. Sort by revenue per recipient, not by clicks.
- **Funnel**: sent, delivered, clicked, ordered as a stepped bar with the
  conversion between steps.
- **List health**: monthly new subscribers, unsubscribes, cleaned addresses,
  net growth; complaint rate against the 0.1% warning line.
- **Flows vs campaigns** split of revenue.

## Web and on-site funnel (GA4)

- **KPIs**: sessions, engagement rate, conversion rate (one named event),
  revenue, revenue per engaged session.
- **Channel table**: sessions, engagement rate (with the spread vs peers),
  conversions, revenue per engaged session; sorted by revenue, not sessions.
- **Funnel by channel**: session, engaged, key action, purchase; the step where
  each channel leaks.
- **Landing pages**: entrances, engagement rate, conversion rate.
- **Tagging health**: share of sessions and revenue in direct or `(not set)`.

## CRM and pipeline (HubSpot, Salesforce)

- **KPIs**: new leads, MQLs, SQLs, opportunities created, pipeline value,
  closed-won revenue, win rate.
- **Stage conversion**: lead to MQL, MQL to SQL, SQL to opportunity,
  opportunity to won, by source; cohort by creation month so recent leads are
  not counted as failures.
- **Velocity**: median days per stage; deals stuck beyond twice the median.
- **Source quality**: cost per SQL and revenue per lead by original source,
  joined to ad spend after aggregation.

## Customers, cohorts and LTV (Shopify, backend orders)

- **KPIs**: new customers, CAC, first-order AOV, repeat rate at day 90 (matched
  age), payback months.
- **Cohort triangle**: retention or cumulative revenue per customer by
  acquisition month and months since first order. Compare down columns.
- **New vs returning revenue** by month.
- **LTV** as floor (realized margin to date), estimate and ceiling, with the
  horizon stated; never one unlabelled number.
- **Acquisition quality by channel**: day-90 repeat and payback per acquisition
  channel.

## Campaign wrap-up (one campaign, all channels)

- **KPIs**: spend, reach, conversions, revenue on one shared denominator,
  cost per acquisition, vs the plan if one exists.
- **By channel and by creative** (utm_campaign, utm_content), with tagging
  coverage stated.
- **Before, during, after**: daily line of the outcome with the campaign window
  shaded; the baseline the lift is read against.
- **Lift**: only if there was a holdout; otherwise label results "attributed",
  not "caused".
