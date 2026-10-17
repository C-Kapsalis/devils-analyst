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
