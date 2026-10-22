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

Take formulas and caveats from [references/catalog.md](references/catalog.md),
the per-platform export traps from
[references/source-traps.md](references/source-traps.md), CRM and lifecycle
definitions from [references/crm-lifecycle.md](references/crm-lifecycle.md), and organic
social goals and KPIs from [references/organic-social.md](references/organic-social.md).
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

[references/sql-patterns.md](references/sql-patterns.md) has tested shapes for
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
