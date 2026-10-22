# Skill: marketing-dashboard

---
name: marketing-dashboard
description: >-
  Use this skill before analysing or reporting on ANY marketing data, even when the task
  looks simple: CSV or spreadsheet exports, or connector data, from email platforms
  (Klaviyo, Mailchimp, Brevo, HubSpot email), ad platforms (Google Ads, Meta, LinkedIn,
  TikTok), GA4, Search Console, HubSpot or another CRM, Shopify or a warehouse. Triggers
  include performance reports, dashboards, "how did X do this month", campaign or channel
  reviews, client reports, CAC, ROAS, CTR, conversion, SEO or pipeline questions, and any
  use of Claude Dashboards on marketing data. It sets which questions to answer, which
  definitions and comparisons are correct, how to explain what changed, and how to end
  with what to do.
---

# marketing-dashboard

A good marketing dashboard answers a question someone will act on. It leads
with the answer, shows the evidence in the order you would read it, and ends
with what to do. Everything else is decoration.

Work through the steps in order. Steps 1-3 happen before the first query.

## 1. Pin the question, the reader and the period

Ask only what you cannot infer, in one message:

- **Question**: "how did paid search do last month", "why are leads down",
  "weekly marketing pulse". Map it to one or more sections of
  section "File: marketing-dashboard/references/questions.md" in 06-dashboards.md; each section lists the
  questions a good analyst answers for that discipline and the cut that answers
  each.
- **Reader**: an executive (5 numbers, what changed, what to do), a channel
  owner (the drill-down that names the broken branch), a client (the same, plus
  plain language and no internal jargon).
- **Period and comparison**: default to the last complete week or month against
  the period before it, and the same period last year when the business is
  seasonal. State it in the subtitle.
- **Business model**: it picks the top metric. A store leads with revenue,
  conversion, ROAS and repeat; lead generation with qualified leads, cost per
  qualified lead and pipeline; a publisher with sessions, engagement and reach.

## 2. Inventory the data

List which sources are connected and what each can answer.
section "File: marketing-dashboard/references/connectors.md" in 06-dashboards.md gives, per source, the
tables to request, their grain, and what each cannot tell you (GA4 has no cost,
ad platforms have no margin, Search Console has no conversions). If a source the
question needs is missing, say which, and either proceed with what exists
(labelled) or ask for an export.

## 3. Define before you query

Use the `metric-definitions` skill: write the metric dictionary for the metrics
this dashboard needs. If the team has a Power BI model on the same data, use the
`power-bi-definitions` skill so the dashboard matches the report everyone else
reads.

## 4. Pull and compute

- Request each source at the grain you will display (non-additive counts such as
  users and reach cannot be re-aggregated later).
- Aggregate each source separately, join on shared keys after aggregation.
- Drop incomplete days (today, the Search Console lag, the ad platforms' open
  conversion window) and say so.
- Recompute one total two ways and confirm it matches.

## 5. Find what matters

- Use the `whats-changed` skill on the headline metrics: driver tree for the
  top metric, mix vs rate for the rates, contribution by channel or campaign.
  Only movements beyond noise become findings.
- Use the `diagnose` skill on the largest real movements: likely cause with
  evidence, the next action, how to verify.
- Cap it at three findings, ranked by money at stake. If nothing moved beyond
  noise, say that plainly: "a steady month" is a finding.

## 6. If it is a Claude Dashboard

When the output is a Claude Dashboard (asked for by name, chosen from the
Output menu, or built from the Dashboards template), read
section "File: marketing-dashboard/references/claude-dashboards.md" in 06-dashboards.md before writing
any dataset. It maps every Devil's Analyst rule onto the dashboard's datasets,
descriptions and calculations, and gives tested SQL that makes the "what
changed" analysis a live, clickable part of the dashboard instead of a pasted
paragraph. For any other output (a chat answer, a document, an HTML page),
continue below.

## 7. Lay it out

Pick the layout for the question from section "File: marketing-dashboard/references/layouts.md" in 06-dashboards.md
and follow the design rules in section "File: marketing-dashboard/references/design.md" in 06-dashboards.md.
Write every title, finding and note by section "File: marketing-dashboard/references/writing.md" in 06-dashboards.md.
The skeleton every layout shares:

1. **Title that states the answer**, not the topic: "Paid search held revenue
   while CPA rose 18%", not "Paid search performance".
2. **KPI row**: at most five tiles, each with value, change vs comparison,
   a sparkline, and the volume behind any rate.
3. **What changed**: the decomposition (a bridge chart for the headline).
4. **Where**: the drill-down that names the branch (campaign, channel, landing
   page, segment), sorted by contribution to the change.
5. **What to do**: the findings in the `diagnose` shape.
6. **Definitions and data notes**: the metric dictionary, sources, freshness,
   what was excluded and why.

## 8. Check before handing over

- [ ] Every number traces to a dictionary definition and a source.
- [ ] No rate shown without its volume; no average of rates.
- [ ] Comparison periods are complete and equal (or the difference is stated).
- [ ] Platform-reported revenue is labelled, and not summed across platforms
      without a warning.
- [ ] Each finding has a number, a driver, a cause labelled confirmed or
      hypothesis, an action, and a way to verify.
- [ ] Platform mechanics the export does not show (view-through counting,
      attribution windows, modelled conversions) are offered as likely causes,
      not stated as facts about this account.
- [ ] The title states the answer.
- [ ] Nothing on the page that answers none of the reader's questions.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Pin the question | "Who decides what after reading this?" | one-sentence reader and decision | ask the user |
| Inventory and define | "Is every metric on the page in the dictionary, at the right grain?" | metric-definitions checks passed | fix the definition first |
| Headline | "Does the title state the answer, and is it the finding with the most money at stake?" | title has a number and a direction | rewrite the title |
| KPI tiles | "Is any tile coloured good or bad because of mix or noise?" | tile colour vs mix and noise results | grey it and label it |
| Charts | "Does any chart mislead (truncated bar axis, dual axis, rate without volume, cumulative hiding a decline)?" | design.md rules per chart | change the chart |
| Actions | "Can the reader verify each action, and is each cause labelled?" | action + check + label per finding | add them |

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

## File: marketing-dashboard/references/claude-dashboards.md

# Building it as a Claude Dashboard

When the output is a Claude Dashboard, the Dashboard type's own instructions
govern the mechanics (datasets, the page, marking every number, the `dash`
API). This file says how to apply Devil's Analyst inside those mechanics. Where the two
seem to conflict, the type's rules about what is allowed on the page win, and
the Devil's Analyst rule moves into the SQL or a calculation.

A dashboard reader can click any number and see its query, its rows and its
freshness in Sources. That makes the definition the visible part of the
product: put it where readers look.

## 1. Pick the source in this order

1. **A governed definition.** If the team has a semantic layer the connector
   can query (a Power BI semantic model through a Power BI MCP connector, a
   warehouse semantic view, a BI tool's semantic query), query the metric
   through it. The number then matches what people see everywhere else. See
   the `power-bi-definitions` skill.
2. **The warehouse**, with SQL you write from the metric dictionary
   (`metric-definitions`). Say in the dataset description that the SQL is
   yours and give the definition.
3. **An app connector** (an ad platform, a CRM, an email platform) through
   one of its tools, shaped into rows with a loader.
4. **A file the user gave** (an export). Say once that anyone who can open
   the dashboard can read it, and name the connector that could serve the
   same numbers live.

## 2. One dataset per source, at the grain you show

- Do the aggregation and every ratio in SQL: `SUM(clicks) * 1.0 /
  NULLIF(SUM(delivered), 0)`, never an average of row rates, never a ratio
  computed in the page from rounded figures.
- One dataset per fact source (ad spend, orders, sessions), each aggregated
  to the keys the page needs (date, channel, campaign).
- **Two sources on different connectors** (Google Ads spend and Shopify
  customers for CAC) meet only in a `dash.calc` over their *aggregated* rows,
  joined on the shared key. Never row to row.
- Non-additive counts (GA4 users, reach) come from the source at the grain the
  card shows. A card that shows monthly users needs a monthly query.
- Map channel names once, in SQL, to one shared list (Paid search, Paid
  social, Email, Organic search, Direct, Referral, Other) so every dataset
  joins and colours the same way.

## 3. Put the definition in the description

The dataset description is what a reader sees when they click a number. Write
the metric dictionary line there, then the data it reads:

> "Click rate = unique clicks / delivered, summed over sends before dividing;
> click-to-order = platform-attributed orders / unique clicks. Reads
> marketing.email_sends."

For a `dash.calc`, the description says the method in one line ("Exact split of
the click-rate change into mix and rate per segment, with a noise screen"), and
the function's parameters are named after the datasets they read.

## 4. Compare complete periods, in the query

Compute the previous and current period in one query with explicit date
ranges (see `metric-definitions` sql-patterns, section 3), so each row says
which period it is. If the dashboard has a date filter, derive both ranges
from it in SQL. Exclude incomplete days (today, Search Console's lag, open
conversion windows) and say so in the card note.

## 5. Make the "why" live

The page may not hold numbers of its own, so the explanation must come from
data too. That is the strength: the decomposition re-runs on every refresh and
every number in the explanation can be clicked and checked.

**Mix vs rate as SQL** (example: email click rate by segment, two periods;
adapt the columns):

```sql
WITH tagged AS (
  SELECT segment, delivered, unique_clicks,
         CASE WHEN send_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31' THEN 'previous'
              WHEN send_date BETWEEN DATE '2026-09-01' AND DATE '2026-09-30' THEN 'current' END AS period
  FROM email_sends
),
seg AS (
  SELECT segment,
         SUM(CASE WHEN period = 'previous' THEN delivered     ELSE 0 END) * 1.0 AS d0,
         SUM(CASE WHEN period = 'previous' THEN unique_clicks ELSE 0 END) * 1.0 AS c0,
         SUM(CASE WHEN period = 'current'  THEN delivered     ELSE 0 END) * 1.0 AS d1,
         SUM(CASE WHEN period = 'current'  THEN unique_clicks ELSE 0 END) * 1.0 AS c1
  FROM tagged WHERE period IS NOT NULL
  GROUP BY segment
),
tot AS (SELECT SUM(d0) AS D0, SUM(c0) AS C0, SUM(d1) AS D1, SUM(c1) AS C1 FROM seg),
r AS (
  SELECT s.segment, s.d0, s.d1,
         s.d0 / t.D0 AS w0, s.d1 / t.D1 AS w1,
         COALESCE(s.c0 / NULLIF(s.d0, 0), s.c1 / NULLIF(s.d1, 0)) AS r0,   -- new segment: all mix
         COALESCE(s.c1 / NULLIF(s.d1, 0), s.c0 / NULLIF(s.d0, 0)) AS r1,   -- dropped segment: all mix
         (t.C0 / t.D0 + t.C1 / t.D1) / 2 AS r_bar
  FROM seg s CROSS JOIN tot t
)
SELECT segment,
       CASE WHEN d0 > 0 THEN r0 END                       AS ctr_prev,
       CASE WHEN d1 > 0 THEN r1 END                       AS ctr_curr,
       (r1 - r0) * (w0 + w1) / 2 * 100                    AS rate_pts,
       (w1 - w0) * ((r0 + r1) / 2 - r_bar) * 100          AS mix_pts,
       CASE WHEN d0 = 0 THEN 'new this period'
            WHEN d1 = 0 THEN 'not sent this period'
            WHEN ABS(r1 - r0) > 2 * SQRT(r0 * (1 - r0) / d0 + r1 * (1 - r1) / d1)
                 THEN CASE WHEN r1 > r0 THEN 'clear rise' ELSE 'clear fall' END
            ELSE 'within noise' END                       AS verdict
FROM r
ORDER BY ABS((r1 - r0) * (w0 + w1) / 2 + (w1 - w0) * ((r0 + r1) / 2 - r_bar)) DESC
```

**Driver bridge as SQL** (revenue = delivered x click rate x click-to-order x
order value; log split, contributions add up to the change exactly):

```sql
WITH p AS (
  SELECT SUM(CASE WHEN send_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31' THEN delivered END) * 1.0 AS d0,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31' THEN unique_clicks END) * 1.0 AS c0,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31' THEN orders END) * 1.0 AS o0,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31' THEN revenue END) * 1.0 AS v0,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-09-01' AND DATE '2026-09-30' THEN delivered END) * 1.0 AS d1,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-09-01' AND DATE '2026-09-30' THEN unique_clicks END) * 1.0 AS c1,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-09-01' AND DATE '2026-09-30' THEN orders END) * 1.0 AS o1,
         SUM(CASE WHEN send_date BETWEEN DATE '2026-09-01' AND DATE '2026-09-30' THEN revenue END) * 1.0 AS v1
  FROM email_sends
),
f AS (SELECT *, (v1 - v0) / LN(v1 / v0) AS lm FROM p)   -- logarithmic mean; needs v1 <> v0, all values > 0
SELECT 1 AS step, 'Before'         AS driver, v0 AS value, NULL AS contribution FROM f
UNION ALL SELECT 2, 'Delivered',      NULL, lm * LN(d1 / d0)                    FROM f
UNION ALL SELECT 3, 'Click rate',     NULL, lm * LN((c1 / d1) / (c0 / d0))      FROM f
UNION ALL SELECT 4, 'Click to order', NULL, lm * LN((o1 / c1) / (o0 / c0))      FROM f
UNION ALL SELECT 5, 'Order value',    NULL, lm * LN((v1 / o1) / (v0 / o0))      FROM f
UNION ALL SELECT 6, 'Now',            v1,   NULL                                FROM f
ORDER BY step
```

Both queries are tested: on the Devil's Analyst email sample they reproduce the
reference results to the cent. Replace the literal date ranges with the
dashboard's period parameters when it has a date filter. For a file or a
cross-connector source, write the same arithmetic as a `dash.calc` over the
aggregated rows.

**Words chosen by the numbers.** Write the finding sentences in the page with
every number marked to a dataset or calculation, and let the script choose the
words from the values (rose or fell; "mostly audience mix" when mix outweighs
rate; hide a finding whose condition no longer holds). A sentence then never
contradicts the numbers beside it after a refresh. Label causes the data cannot
prove as hypotheses in plain words; they are fixed text, so keep them general
enough to stay true ("the landing page or the offer").

## 6. Lay it out with the type's shapes

| Devil's Analyst layout | Dashboard shape to start from |
|---|---|
| Weekly pulse, channel scorecard | Scorecard |
| Monthly or campaign review | Review |
| "Why did X move" | Visual analysis |
| Funnel (web, email, CRM stages) | Funnel |
| Campaign, query or send tables | Table |

On top of the shape keep the Devil's Analyst skeleton: a header sentence that states
the answer (its numbers marked), KPI tiles with the change from the previous
period coloured by whether it is good for the business, the decomposition
next to the headline it explains, the drill-down that names the branch, a
"What to do" card, and a collapsed "Definitions and data notes" card.

## 7. Same look in every dashboard

Tabular Editor's review of Claude Dashboards notes that "every design choice
is made again in every dashboard". Avoid it for marketing work:

- **Fixed channel colours** across every dashboard: Paid search
  `dash.colors[0]`, Paid social `[1]`, Email `[2]`, Organic search `[3]`,
  Direct `[4]`, Referral `[5]`, Display and video `[6]`, Other
  `--cds-chart-muted`. Write the mapping into the definitions card.
- The same tile order for the same business model (store: revenue, new
  customers, CAC or cost per order, conversion rate, ROAS on one shared
  denominator; lead generation: qualified leads, cost per qualified lead,
  pipeline, win rate).
- The same names for the same metrics, from the metric dictionary.

## 8. Hand over

After the type's own hand-over lines, add the Devil's Analyst ones: which definitions
the dashboard uses and where they came from (a semantic model, the metric
dictionary, your own SQL), what was excluded and why, the reconciliation check
and its result, and the one finding most worth acting on.

---

## File: marketing-dashboard/references/connectors.md

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

---

## File: marketing-dashboard/references/design.md

# Design rules for marketing dashboards

The reader looks before reading. The layout, the order and the one highlighted
number carry the argument; prose explains it.

## Words

- **The title states the answer**, with its number: "Email revenue rose 12% on
  the VIP send; newsletter clicks are flat." The subtitle states period,
  comparison and sources.
- Section titles are questions or answers ("Where did CPA rise?"), not labels
  ("Campaign table").
- Every finding sentence: number, driver, interpretation (labelled hypothesis
  if unproven), in that order.
- Plain words. No "leverage", "synergy", "deep dive", "robust". Write "people
  who clicked", not "engaged users", unless the metric dictionary defines it.

## KPI tiles

- Value, change vs comparison (absolute and percent; for rates, in points:
  "+0.6 pts"), a sparkline of the last 8-13 periods, and the volume behind any
  rate ("4.6% of 20,650 delivered").
- Colour the change by whether it is good for the business, not by sign: a CPA
  that fell is good. Changes inside the noise band are grey.
- A blended rate whose change is mostly audience mix (the mix share of the
  change outweighs the within-segment share, or has the opposite sign) is not
  good news: colour it grey and say so on the tile ("+0.36 pts, all mix;
  like-for-like -0.43 pts").
- Lay the tiles out in one row at desktop width (a grid of as many columns as
  tiles); never leave one tile alone on a second row.
- At most five tiles. If everything is a KPI, nothing is.

## Charts

| To show | Use | Not |
|---|---|---|
| A metric over time | line (bars for few periods) | area stacks with many series |
| What moved a total from A to B | bridge (waterfall), one bar per driver or segment | two bars side by side |
| Items ranked | horizontal bars, sorted by value | pie, unsorted bars |
| Parts of a whole over time | stacked bars with at most 5 parts plus "Other" | stacked lines |
| A funnel | stepped bars with the step conversion printed between steps | a funnel shape whose widths are not to scale |
| Two rates per item (CTR vs position) | scatter with labelled zones | two bar charts |
| Cohorts | triangle heatmap, one sequential colour | line per cohort beyond 6 cohorts |
| How a metric is spread (order values, days to convert, time on page) | histogram, or a box plot per group when comparing groups | a single average bar |
| Whether two measures move together (spend vs conversions per campaign) | scatter, one dot per item, with the item count in the subtitle | two lines on two axes |
| Many periods by many items (week by channel, hour by weekday) | highlight table (heatmap) with values printed | a line per item beyond 6 items |
| Share of a total in one period | sorted horizontal bars with a share label, or a treemap with at most 10 tiles plus "Other" | pie or donut |
| A running total (month to date, year to date) | cumulative line next to the per-period bars or line | the cumulative line alone |
| Where (country, region, city) | a map only when location or distance is the question; otherwise sorted bars | a filled map for a ranking |
| An average by group | dot or bar for the mean with its interval, and n per group | bars with no n |

- Start bar axes at zero. Lines may zoom, with the axis labelled.
- One filled area for a single total is fine; stacked areas follow the stacked-bars cap (5 parts plus "Other"). Treemaps only with labels printed and at most 10 tiles.
- Two y-axes only when the two series share the x-axis and the point is their
  relation (clicks vs CPC); label both axes in the series' colours.
- Annotate events on time charts: launches, promotions, tracking changes,
  budget changes. An unexplained step is the first question a reader asks.

## Colour

- One colour per channel or metric, the same everywhere on the page (Paid
  search is always the same blue). Write the mapping into the definitions panel.
- Grey for context, one accent for the thing the title is about.
- Red only for findings with money at stake. Never red and green as the only
  difference: add a sign or an icon.
- Check both light and dark themes when the surface supports them.

## Tables

- Sorted by what the reader decides on (contribution to change, revenue), not
  alphabetically.
- Right-align numbers, same decimals per column, units in the header.
- A total row recomputed from parts (rates from summed numerators and
  denominators).
- Mute rows below a minimum volume, or fold them into "Other".

## Interaction (when the surface supports it)

- A period picker and at most two filters (channel, country or segment) that
  apply to the whole page.
- A metric picker beats ten near-identical charts: one chart, the reader picks
  the metric.
- Clicking a number shows its definition and its query.

## Definitions and data notes panel

Always present, collapsed by default:

- the metric dictionary (name, formula, source, grain, caveat);
- sources and the time each was last refreshed;
- what was excluded (incomplete days, conversion lag, untagged traffic) and how
  much it was;
- the reconciliation check and its result.

## Principles from the author's notes

- **Climb the value pyramid**: number, insight, diagnosis, decision, outcome.
  "Most analytics tools stop at the first two rungs." A dashboard that stops
  at the number leaves the reader to guess the cause.
- **Report to the decision.** "Lead with the answer." If a section cannot
  change what someone would do, cut it.
- **"A monthly report is an autopsy. A pace read is a diagnosis with time left
  to treat it."** Put the forward-looking read (pacing, leading indicators)
  next to the backward-looking totals.
- **Nothing means anything in isolation**: against the prior period, the plan,
  the category or a competitor, always with the denominator named.
- **Twyman's law**: a figure that looks surprising is usually wrong. Check the
  tracking and the definition before you headline it.
- **Layout follows a Z**: top-left the highest-level summary, top-right
  secondary KPIs and context, bottom rows the detail.
- **Colour**: orange and blue before red and green; at most 7-10 distinct
  colours; one saturated colour for the highlight against grey.
- **No pie charts.**
- **Name the attribution model** in the subtitle of any chart that splits
  conversions or revenue by channel.
- **Leading before lagging**: list growth, branded search and pipeline lead;
  revenue lags. Show at least one leading indicator per dashboard.

## Encoding

- Size encodes magnitude badly. Use bubble or tile size only for a secondary
  measure, scale by area not radius, and print the value on the largest marks.
- Shapes tell categories apart up to about 10. Beyond that, group into "Other".
- Put detail in the tooltip, not on the mark. Print data labels only for the
  key values the title talks about.

## Colour scales

- **Sequential** (one hue, light to dark) when every value has the same sign:
  spend, sessions, retention.
- **Diverging** (two hues meeting at a neutral midpoint) when values cross a
  meaningful midpoint: change vs prior period, variance to plan. The neutral
  colour sits exactly at zero (or at plan), and the scale is symmetric.
- Never a rainbow or categorical palette for ordered data.
- A colour means the same thing in every chart on the page: if orange is
  "this period" in one chart, it is not "Paid social" in the next.

## Reference lines and annotations

- Add a reference line wherever a reader would ask "is that good": the
  average, the target, the benchmark or the warning threshold. Label the line
  with its value and what it is.
- Highlight anomalies and outliers on the chart (a marked point or a short
  note), not only in the prose.

## Smoothing, totals and denominators

- A moving average hides seasonality and smears steps. State the window in the
  axis or legend ("7-day average"), and never use a smoothed series to argue
  there is no weekly or seasonal pattern.
- Running totals hide declines: a cumulative line keeps rising while each
  period falls. Show the per-period values next to it.
- A "percent of total" computed on a filtered view uses the filtered total.
  Label the denominator ("share of Paid channels", not "share").
- Use the median, not the mean, for skewed measures (order value, days to
  close, time on page) or when outliers are present, and say which one the
  tile shows.

## Statistics on charts

- A trend or regression line stops at the last observed point. Anything beyond
  it is a forecast: dashed, shaded, labelled "forecast", with its method.
- A scatter's correlation coefficient is a sample figure. Do not write "strongly
  related" unless it is tested (state n and the p-value), and never "drives".
- When a fitted model is shown, the fit is printed in business terms
  ("spend explains about 60% of the week-to-week change in leads"), and a model
  that fails its significance test is not shown as a finding.

## Data notes

- Report rows dropped or unmatched by joins (orphan records, untagged
  campaigns). An inner join hides dirty data silently; the definitions panel
  says how much was lost.
- One name per field everywhere on the page: the tile, the chart, the table and
  the dictionary use the same label.

## Layout and reading time

- The page title (or subtitle) carries the date range and any active filter, so
  a screenshot still says what it shows.
- Filters sit together in one place, in the same position on every page.
- Leave white space between sections; no background images, borders or
  gridlines that carry no information. Remove an axis when the marks are
  labelled.
- The main story reads in under 7 minutes. If it does not, cut sections.
- When phone readers matter, check the phone layout on its own; it is not the
  desktop layout shrunk.
- Animated transitions (where the surface has them) keep each mark on its own
  data point from state to state, so the eye follows the point instead of
  re-reading labels. Never animate for decoration.

---

## File: marketing-dashboard/references/layouts.md

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

---

## File: marketing-dashboard/references/questions.md

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

---

## File: marketing-dashboard/references/writing.md

# Writing the report

A marketing report is read once, quickly, by someone deciding something. Write
so that the first screen is enough to act on and every later line supports it.

## 1. Know who decides what

Before drafting, finish this sentence for yourself: "After reading this,
[who] will [do what] by [when]." It settles what goes in and how much detail
the reader needs. The people running the campaigns want the arithmetic; their
director wants the decision, the number behind it and the risk.

## 2. Structure: answer, proof, decision

- **Open with the answer.** The title and first sentence carry the conclusion
  and its number: "Generic search loses money: CPA $67 against a $36
  break-even", not "Paid search overview".
- **Group, then order.** Collect related points (the finding, the numbers
  behind it, what argues against it, an example) into one section, and order
  sections by how much they change the decision.
- **Close on the decision.** The last lines say what to do, what it should
  change, and how the reader will know. Do not end on a caveat list.
- **Make findings look alike.** Each one has the same parts in the same order
  (number, driver, likely cause, action, check), and headings follow one
  pattern ("Cut", "Keep", "Test").

## 3. Paragraphs

One point per paragraph, two or three sentences long. Start a new paragraph
when the point changes, so a reader skimming the page lands on whole ideas.

## 4. Sentences

- **One direction per sentence.** Good news and bad news go in separate
  sentences.
- **Say who did what.** "Returning visitors bought less" beats "a decline in
  conversion was observed in the returning segment".
- **Cut filler.** "In order to", "it is worth noting that", "with regard to",
  "is designed to drive an increase in" (increases).
- **Name things again instead of pointing back.** Write "the VIP send", not
  "the former" or "as mentioned above".
- **One action per sentence.** "Pause brand search and test generic bids"
  hides two decisions with different owners; split it.
- **Mix short and long sentences**, and read each paragraph aloud once before
  handing it over.

## 5. Words

- **Plain words.** enable -> allow, facilitate -> make possible or help,
  provision -> provide, actualize -> reach, generate -> make, enact -> do,
  implement -> carry out, visualize -> see, consequently -> as a result,
  developed -> made, utilize or leverage -> use, commence -> start,
  approximately -> about (unless the precision matters).
- **Concrete over abstract.** "Had an impact" says nothing; name the number,
  the direction, the size and who it affected.
- **Reserve "significant"** for a statistical test. Otherwise say "large" or
  "clear" and give the number.
- **No jargon the reader would not use.** Spell out an acronym the first time
  if the audience might not know it (MER, iROAS, CTOR).
- **Emphasis is scarce.** Bold the one number or decision per section the
  reader must not miss. No italics, capitals or quotation marks for emphasis.
- **Numbers.** Metrics stay as digits with unit and period ("CPA $17.37,
  September"). Round to what the decision needs: "$84.5k", not "$84,522.90",
  unless the reader will reconcile it.

## 6. Edit in four passes

1. **Shorter:** delete repetition, filler and anything the reader would not
   miss.
2. **Clearer:** the conclusion is in the first sentence; each sentence follows
   from the one before.
3. **Smoother:** vary sentence length; check that headings and findings share
   one pattern.
4. **Sharper, lightly:** a strong verb or a concrete picture where it helps a
   number land ("one weekly blast drags every average down"), never at the
   cost of accuracy and never exaggerated.
