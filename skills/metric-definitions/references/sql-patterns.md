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
