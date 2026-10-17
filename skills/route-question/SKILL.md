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
are in [references/connectors.md](references/connectors.md).

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
