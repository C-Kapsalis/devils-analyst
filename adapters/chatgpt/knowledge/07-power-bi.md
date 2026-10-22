# Skill: power-bi-definitions

---
name: power-bi-definitions
description: >-
  Use the metric definitions already governed in a Power BI semantic model when building a
  Claude dashboard or analysis on the same warehouse (Snowflake, Databricks, BigQuery,
  Redshift, SQL Server, Fabric). Reads the model's measures (DAX, formats, descriptions),
  relationships and the warehouse tables behind each model table, translates the needed
  measures to SQL faithfully, and reconciles one number against Power BI. Use when the
  user has a Power BI model, PBIP, TMDL, .pbix or a list of DAX measures, says "use our
  Power BI definitions", or when a dashboard number must match what Power BI shows.
---

# power-bi-definitions

Most companies that point Claude at Snowflake or Databricks already have a Power
BI model on the same tables, and that model already says what CAC, ROAS and
"active customer" mean. A dashboard that re-invents those definitions disagrees
with the report everyone else reads. This skill makes the dashboard use the
model's definitions, so the two show the same number.

## 1. Get the model's definitions

Pick the first route that works:

| The user has | Do this |
|---|---|
| A PBIP folder on disk (Claude Code) | `python3 scripts/metric_contract.py <folder> --format markdown` (path relative to this skill's folder; in Claude Code use `${CLAUDE_SKILL_DIR}/scripts/metric_contract.py`) |
| A zip of the `*.SemanticModel` folder (claude.ai with code execution) | Unzip it in the sandbox, then run the same script on it |
| A `.pbix` only | Ask them to open it in Power BI Desktop and *File > Save as > Power BI Project* (PBIP) with the TMDL format, then zip the `.SemanticModel` folder |
| Pasted TMDL, or a list of measures and their DAX | Read it directly and build the same table by hand |

The script is read-only and uses only the Python standard library. Its output
has four parts: measures (name, format, description, DAX), tables and visible
columns, **warehouse sources** (connector, database.schema.table or native SQL
behind each table, plus columns renamed from the source), and relationships.

Suggest saving the result as `metric-dictionary.md` in a Claude Project, so every
later dashboard in that Project starts from it.

## 2. Show the definitions, and flag what is missing

Before building, show the measures the request needs, and flag:

- measures with no description (the meaning is a guess until someone writes it);
- ratios that are not `DIVIDE` of two base measures;
- entity counts taken from a dimension instead of the fact;
- two measures that look like the same business metric with different DAX.

## 3. Map model tables to warehouse tables

Use the *warehouse sources* section. Then check three things with the user, or
in the data:

- **Power Query steps after navigation** (filters, merges, renamed columns) are
  part of the definition. The script lists renamed columns; it cannot see row
  filters applied in Power Query. Ask, or compare row counts.
- **Import vs DirectQuery.** Import models show data as of the last refresh; the
  warehouse shows now. Expect differences for recent days.
- **Row-level security** in the model does not exist in a direct warehouse query.
  Say so if the model has roles.

## 4. Best: query the model itself

If the user has added a Power BI MCP server as a connector (Microsoft's Power BI
MCP server, which can run DAX queries against a semantic model), a Claude
Dashboard dataset can query the model directly, so the dashboard uses the
model's own measures, with each viewer's own permissions:

```
EVALUATE
SUMMARIZECOLUMNS (
    'Calendar'[Year-Month],
    Channels[channel_group],
    "Spend", [Total Ad Spend],
    "New customers", [New Customers #],
    "CAC", [CAC]
)
```

Reference measures by name; never re-implement them in the DAX query. The
connector usually needs the semantic model's ID (not its name) and a tenant
setting enabled by a Fabric admin; ask the user for both. Shape the answer into
rows with a loader, and return the DAX that ran as `meta` so readers can see it
in Sources. Only if no such connector exists, translate to warehouse SQL:

## 5. Otherwise, translate the measures to SQL, faithfully

Follow [references/dax-to-sql.md](references/dax-to-sql.md). The rules that
break most translations: `CALCULATE` filters *replace* a slicer on the same
column, ratios are computed from summed parts at the displayed grain, two fact
tables are aggregated separately before they are joined, and BLANK is not zero.

If a measure cannot be translated faithfully (calculation groups, complex
context transition, many-to-many with bidirectional filters), say so, and leave
it out or show it labelled "Power BI only". Never ship a near-miss under the
real name.

In the dashboard's definitions panel, show each metric's DAX next to the SQL
that implements it.

## 6. Reconcile one number

Ask for one number the user can see in their Power BI report (a KPI card, a
total), with its filters. Compute the same in SQL. If it differs, check in this
order: report or page filters, Power Query row filters, refresh timing, time
zone of the date column, RLS, and the translation itself. Report the match, or
the difference and its cause, at the top of the dashboard.

## 7. Build

Hand over to the `marketing-dashboard` skill with the translated metrics as the
definitions. Power BI stays the source of truth: if the user wants a metric the
model lacks, propose the DAX (name, format, description) so it can be added to
the model, rather than defining it only in the dashboard.

## 8. Audit the measures you reuse

Before you reuse a measure, run it past
[references/power-bi-audit.md](references/power-bi-audit.md): averaged rates,
summed snapshots, toggle defaults, stacked platform revenue, duplicate KPIs.
Compare each measure with the formula, source and grain the
`metric-definitions` skill gives for that metric (and with any house rule
that overrides it), not with the measure's name. A wrong measure reused
faithfully is still wrong: flag it, propose the corrected DAX, and let the
model owner decide.

## Power BI developers in Claude Code

If the user also maintains the model as PBIP in git, the companion command-line
tools (model linting, building sample models from a spec, keeping client copies
in sync, styling report charts) are described in
[references/power-bi-tools.md](references/power-bi-tools.md). They need a local
shell and `uv`; they do not run in claude.ai.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Read the model | "Which toggle or selector silently changes this measure?" | every disconnected table and its fallback value listed | pin it explicitly in the query |
| Map measures | "Is this measure really the catalog metric it is named after?" | DAX compared with the metric-definitions formula | classify as defensible or wrong |
| Audit the DAX | "Would this measure be right at every grain (averaged rates, summed snapshots, unfiltered report levels)?" | evaluate at two grains; compare with a DIVIDE of sums | propose corrected DAX |
| Translate to SQL | "Does the SQL reproduce one number the user can see in Power BI?" | reconcile one KPI | find the cause in the order given |
| Write to the model | "Has the user approved this change, on a write-capable connector?" | explicit approval | propose only |

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

## File: power-bi-definitions/references/dax-to-sql.md

# DAX to SQL, faithfully

A DAX measure is an aggregation evaluated in a *filter context*: the slicers,
rows and columns of the visual, flowing from dimensions to facts through the
model's relationships. A faithful SQL translation reproduces that context:
WHERE for the filters, GROUP BY for the visual's rows, joins along the model's
relationships, and nothing else.

## Building blocks

| DAX | SQL | Watch out |
|---|---|---|
| `SUM(T[c])` | `SUM(t.c)` | Empty set: DAX returns BLANK, SQL NULL. Same thing. |
| `AVERAGE(T[c])` | `AVG(t.c)` | Both skip blanks/NULLs. |
| `MIN` / `MAX` | `MIN` / `MAX` | |
| `COUNTROWS(T)` | `COUNT(*)` | Empty: DAX BLANK, SQL 0. Use `NULLIF(COUNT(*), 0)` to match. |
| `DISTINCTCOUNT(T[c])` | `COUNT(DISTINCT t.c)` | DAX counts BLANK as one value; SQL ignores NULL. Use `DISTINCTCOUNTNOBLANK` semantics only if the DAX says so, otherwise add 1 when NULLs exist, or say why it differs. |
| `DIVIDE(a, b)` | `a / NULLIF(b, 0)` (cast a to float) | DIVIDE returns BLANK on zero; plain `a / b` in DAX returns infinity. |
| `[Other Measure]` | the other measure's SQL, inlined | Translate the dependency first. |
| `VAR x = ... RETURN ...` | a CTE or an inline expression | Variables are evaluated once, in the outer context. |
| `IF(cond, a, b)` / `SWITCH(TRUE(), ...)` | `CASE WHEN ... END` | |
| `COALESCE(x, 0)`, `IF(ISBLANK(x), 0, x)` | `COALESCE(x, 0)` | Turns BLANK into 0: rows that were hidden now show. |
| `RELATED(D[c])` inside an iterator | a join to D along the active relationship | |
| `SUMX(T, T[a] * T[b])` | `SUM(t.a * t.b)` | Row-level first, then sum. Never `SUM(a) * SUM(b)`. |
| `SUMX(VALUES(D[k]), [M])` | aggregate M per k in a subquery, then `SUM` | The grain of the iteration matters. |

## CALCULATE: the filter that replaces

`CALCULATE([Revenue], Campaigns[type] = "Promotion")` does not intersect with
a slicer on `Campaigns[type]`; it **replaces** it. If the visual is grouped by
campaign type, this measure shows promotion revenue on every row.

| DAX | SQL |
|---|---|
| `CALCULATE([M], D[c] = "x")` | M computed with `D.c = 'x'` and with any filter or GROUP BY on `D.c` removed. Inside a grouped query: `SUM(CASE WHEN d.c = 'x' THEN f.v END)` only when the query does not group or filter by `D.c`; otherwise compute it in a separate CTE without that grouping and join it back. |
| `CALCULATE([M], KEEPFILTERS(D[c] = "x"))` | intersect: `SUM(CASE WHEN d.c = 'x' THEN f.v END)` in the grouped query |
| `CALCULATE([M], ALL(D))` / `REMOVEFILTERS(D)` | M with every filter and grouping on D removed: a separate CTE, cross-joined back (the "share of total" pattern) |
| `CALCULATE([M], ALLEXCEPT(D, D[c]))` | M grouped by `D.c` only, joined back on `D.c` |
| `CALCULATE([M], FILTER(T, cond))` | M with `cond` added to the existing filters (an intersection): FILTER iterates T as it is already filtered. This differs from the boolean shorthand `D[c] = "x"`, which replaces filters on that column |
| `CALCULATE([M], FILTER(ALL(T[c]), cond))` | the boolean shorthand written out: replaces the filter on `T.c` |
| `CALCULATE([M], USERELATIONSHIP(F[ship_date], Cal[Date]))` | join the calendar on `f.ship_date` instead of the active date column |

## Time intelligence

Time functions need a contiguous calendar. In SQL, compute each period with an
explicit date range; never use `LAG()` over rows, because a missing month
shifts every comparison by one.

| DAX | SQL date range for the current row's period [start, end] |
|---|---|
| `TOTALYTD([M], Cal[Date])` | from Jan 1 of end's year to end |
| `SAMEPERIODLASTYEAR(Cal[Date])` | [start - 1 year, end - 1 year] |
| `DATEADD(Cal[Date], -1, MONTH)` | [start - 1 month, end - 1 month], clipped to month ends |
| `PREVIOUSMONTH(Cal[Date])` | the whole calendar month before start |
| `DATESINPERIOD(Cal[Date], MAX(Cal[Date]), -28, DAY)` | [end - 27 days, end] |

A fiscal year that does not start in January changes every one of these: read
the calendar table's definition, or ask.

## Relationships and grain

- Filters flow from the one side (dimension) to the many side (fact). A filter
  on a fact column does not filter the dimension unless the relationship is
  bidirectional (`crossFilteringBehavior: bothDirections`).
- **Two facts are never joined row to row.** Aggregate each fact to the shared
  dimensions (date, channel, campaign) in its own CTE, then join the CTEs on
  those keys. Joining spend rows to order rows on channel and date multiplies
  spend by the number of orders: the most common way an AI dashboard inflates
  CAC denominators and ROAS.
- Inactive relationships carry no filter unless a measure activates them.
- A fact row whose key is missing from the dimension is grouped under BLANK in
  Power BI; an inner join drops it in SQL. Use a LEFT JOIN and label the NULL
  group "(blank)", or report how many rows were dropped.

## What does not translate

Say so instead of approximating:

- calculation groups and field parameters (a field parameter is a metric picker:
  build the picker in the dashboard instead);
- measures that depend on visual-level context (`ISINSCOPE`, `SELECTEDVALUE` of
  a column the dashboard does not have);
- many-to-many relationships with bidirectional filtering;
- RLS-dependent logic (`USERPRINCIPALNAME()`).

## Example

```
CAC = DIVIDE([Total Ad Spend], [New Customers #])
Total Ad Spend = SUM(AdSpend[spend])
New Customers # = CALCULATE(DISTINCTCOUNT(Orders[customer_id]), Orders[order_sequence] = 1)
```

Monthly CAC on Snowflake, with each fact aggregated on its own:

```sql
WITH spend AS (
  SELECT DATE_TRUNC('MONTH', s.date) AS month, SUM(s.spend_usd) AS spend
  FROM MARKETING.ADS.DAILY_SPEND s
  GROUP BY 1
),
new_customers AS (
  SELECT DATE_TRUNC('MONTH', o.order_date) AS month,
         COUNT(DISTINCT o.customer_id) AS new_customers
  FROM SHOP.PUBLIC.ORDERS o
  WHERE o.order_sequence = 1
  GROUP BY 1
)
SELECT COALESCE(s.month, n.month) AS month,
       s.spend / NULLIF(n.new_customers, 0) AS cac
FROM spend s
FULL OUTER JOIN new_customers n ON n.month = s.month
ORDER BY 1;
```

Not this, which multiplies spend by the number of orders on each day:

```sql
-- illustrative anti-pattern: do not run
SELECT DATE_TRUNC('MONTH', s.date), SUM(s.spend_usd) / COUNT(DISTINCT o.customer_id)
FROM DAILY_SPEND s JOIN ORDERS o ON o.order_date = s.date ...
```

---

## File: power-bi-definitions/references/power-bi-audit.md

# Power BI models (TMDL, PBIP, a list of DAX measures)

Read every measure the reports use, the disconnected tables (toggles and
selectors) and the relationships. Evaluate suspicious measures at two grains
(a day and a month, a campaign and the total); a correct ratio gives the same
answer as a DIVIDE of sums at each grain. The agreed formula, source and
grain for each metric come from the `metric-definitions` skill
([../../metric-definitions/SKILL.md](../../metric-definitions/SKILL.md)) or the
team's house rules: compare each measure with that, not with its name. The
same checks, with the same ids, are the Power BI area of the `audit` skill
([../../audit/references/power-bi.md](../../audit/references/power-bi.md)).

## Measure checks

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| P1 | Ratio measures | `AVERAGE(Fact[ctr])`, `AVERAGEX(..., [rate])` or an average of a precomputed rate column | A day with 20 impressions weighs like a day with 20,000; the total is true of nothing | `DIVIDE(SUM(Fact[clicks]), SUM(Fact[impressions]))` | 1 |
| P2 | Snapshot measures (list size, subscribers, open pipeline, stock, followers) | `SUM` over a daily or monthly snapshot column | A month shows 30 times the list | Closing value: `CALCULATE(SUM(...), LASTDATE('Date'[Date]))`, or `LASTNONBLANKVALUE` over dates, or an average if that is the definition | 1 |
| P3 | Distinct counts | `SUM(Fact[active_users])` from a daily table used for monthly users | Users who visit on many days counted many times | Distinct count from user-level data, or a source monthly figure; label otherwise | 1 |
| P4 | Toggles and selectors: disconnected tables read with `SELECTEDVALUE(Table[Col], <default>)` | The default (no selection) differs from the agreed definition (gross instead of net revenue; 28-day click instead of 7-day; all channels instead of paid) | Every card nobody filtered shows the wrong version; exports and subscriptions too | Default to the agreed value; or make the slicer single-select with a required default; state the default in the description | 1 |
| P5 | Platform revenue measures | Google and Meta claimed revenue added into one "Paid Revenue" and divided by spend | Stacked ROAS | ROAS on store or analytics revenue; platform claims as separate, labelled measures | 1 |
| P6 | Duplicate business metrics | Two CAC (or ROAS) measures with different filters or exclusions | Two numbers for one KPI across pages | One canonical measure; retire or rename the other | 2 |
| P7 | `CALCULATE` filters | A filter on a column the user also slices on, which silently replaces the slicer | Cards ignore the page filter | `KEEPFILTERS`, or document the override | 2 |
| P8 | BLANK vs zero | `+ 0` or `IF(ISBLANK(...), 0)` on every measure | Rows appear for every combination; averages fall | Keep BLANK unless zero is meant | 4 |
| P9 | Measure descriptions and formats | No description on measures the reports use | Meaning is a guess | Description with numerator, denominator, grain, filters | 4 |
| P10 | Template vs client copies | The template changed a definition; client copies still carry the old one | "The same KPI" differs by client | Detect drift per copy; fix with an allowlist for intended differences | 2 |

## Model and process checks

| # | Look at | Red flag | Fix | Tier |
|---|---|---|---|---|
| P11 | Text-model structure | Broken table references; duplicate lineage tags | Run a read-only lint; apply only mechanical fixes; re-check | 2 |
| P12 | Versioning | Model only as .pbix, no checks before deploy | PBIP/TMDL in git with a linter in CI | 4 |
| P13 | Openability | Validated on paper only | Open in Desktop and record the result | 4 |
| P14 | Auto-fix boundary | A business definition "fixed" by a tool | Mechanical fixes only; judgement items stay open for a human | 2 |

## How to prove each finding

- Averaged rate: compute the measure as written and as DIVIDE of sums on the
  sample data or on two made-up rows (20 impressions at 10% and 20,000 at 2%:
  average 6%, true 2.01%).
- Summed snapshot: compare the measure for a month with the last day's list
  size.
- Toggle default: write what a card shows with no slicer selection, and what
  the description or the business says it should show.

## Decoys

`DIVIDE(SUM(...), SUM(...))` ratios; `REMOVEFILTERS` in a share-of-total
measure that is labelled as such; a disconnected table whose default matches
the stated definition; `SUMX` over a fact table of additive amounts.

## Tools for models kept as PBIP

P10 is what `tmdl-drift-doctor` checks across client copies. P11 and P14 are
`tmdl-preflight`: a read-only lint, mechanical fixes only, then a re-check
from disk. Both are in [power-bi-tools.md](power-bi-tools.md) and need a
local shell. P13 stays a human step: the tools prove the files pass their
validators, not that Power BI Desktop opened them.

---

## File: power-bi-definitions/references/power-bi-tools.md

# Power BI developer tools (Claude Code only)

Four open-source command-line tools for models kept as PBIP/TMDL in git. They
run through one wrapper that fetches each tool's tagged GitHub release into a
throwaway environment (needs [uv](https://docs.astral.sh/uv/); nothing is
installed globally):

```
T="${CLAUDE_SKILL_DIR}/scripts/devils-analyst-tool"
$T tmdl-preflight --version        # prints "tmdl-preflight 1.2.0" when ready; exit 127 = install uv first
```

The wrapper pins tag `v1.2.0`. To pin another tag, set
`DEVILS_ANALYST_TOOLS_VERSION` (for example `DEVILS_ANALYST_TOOLS_VERSION=v1.1.0 $T ...`);
`DEVILS_ANALYST_USE_LOCAL=1` prefers tools already on PATH.

The wrapper is a bash script. On Windows without Git Bash or WSL, run a tool
through `uvx` directly in PowerShell, with the same arguments:

```powershell
uvx --from git+https://github.com/C-Kapsalis/tmdl-preflight@v1.2.0 tmdl-preflight --version
uvx --from git+https://github.com/C-Kapsalis/pbip-model-forge@v1.2.0 pbip-forge --version
uvx --from git+https://github.com/C-Kapsalis/tmdl-drift-doctor@v1.2.0 drift-doctor --version
uvx --from git+https://github.com/C-Kapsalis/pbi-plot-styler@v1.2.0 pbi-plot-styler --version
```

At `v1.2.0`, each tool's own listing gives: `tmdl-preflight rules --json`
119 rules, 25 of them auto-fixable; `pbip-forge --help` 8 commands and
`pbip-forge rules` 22 spec rules; `drift-doctor --help` 20 commands;
`pbi-plot-styler --help` 6 commands. Quote the counts the build you run
prints, not these.

Rules for all four: never hand-write TMDL a tool can generate or fix; never
claim a model opens in Power BI Desktop beyond what `tmdl-preflight check`
proves (opening it is the user's step); show the tool's counts and exit codes
instead of describing them.

## tmdl-preflight: will it open, and is it sound?

```
$T tmdl-preflight check <path> --format json   # 0 clean, 1 violations, 2 usage error
$T tmdl-preflight fix <path>                   # auto-fixes, then re-checks from disk
$T tmdl-preflight rules --json                 # the catalog: id, severity, fixable, options (119 rules at v1.2.0)
```

`fix` edits files: if the folder is not under git, ask first or copy it. CI:
`baseline <path>` then `check --baseline <path>/.tmdl-preflight-baseline.json`;
`--format github` or `--format sarif`; pre-commit hook id `tmdl-preflight` from
`https://github.com/c-kapsalis/tmdl-preflight`, rev `v1.2.0`.

## pbip-model-forge: a model from a spec

Turns a spec (a Python file with a module-level `SPEC` dict: tables, rows,
calendar, measures, relationships) into an openable PBIP with sample data and a
`handoff/SPEC.md` (data dictionary and Mermaid diagram) for data engineers.
[../assets/email_campaigns_forge_spec.py](../assets/email_campaigns_forge_spec.py)
is a complete, passing example for email campaigns; copy it into the user's
project before editing.

```
$T pbip-forge check spec.py --profile handoff          # need 0 P0, 0 P1 (22 rules; `rules` lists fixes)
$T pbip-forge build spec.py out/Model --check --profile handoff
$T tmdl-preflight check out/Model                      # need 0 errors
```

Spec rules: one hidden fact with its grain as the description; 2-4 dimensions
with one `int64` key each; foreign keys named like the key they reference; an
"Unknown" member (key -1) instead of null keys; a description on everything; a
measures table never named `Measures`; ratios as `DIVIDE` of base measures;
entity counts from the fact's foreign key. To change the model, edit the spec
and rebuild; never edit the generated TMDL.

## tmdl-drift-doctor: one template, many client models

```
$T drift-doctor capture                 # snapshot the template (after every template change)
$T drift-doctor detect --json           # 0 clean, 1 actionable drift, 3 parse error
$T drift-doctor remediate --dry-run     # unified diffs; then without --dry-run to apply
$T drift-doctor remediate --sync        # also deletions (retire.*): ask first
$T drift-doctor review --out REVIEW.md  # what needs a human
$T drift-doctor ratchet tighten|check   # CI: fail when drift rises
```

Configured by `fleet.yml`: `template`, `models` (short or long form with
`gating: advisory` and declared `overrides`), `state_dir`, and
`allowlist: {kinds: [...], expressions: [...]}`. Start the allowlist with
non-destructive kinds (`measure.missing`, `measure.expression_drift`,
`measure.property_drift`, `column.missing`, `relationship.missing`). Show
dry-run diffs and get a yes before applying.

## pbi-plot-styler: one style for every chart

For PBIR reports using the one-canvas pattern (field-parameter tables
`x-Plot Specific 1`, `x-Plot Specific 2`, `y-Plot Specific`; others via
`--table`):

```
$T pbi-plot-styler style X.Report --dry-run              # exit 1 = would change a visual
$T pbi-plot-styler style X.Report --palette "#1F6F4A" --palette "#2B6CB0"
$T pbi-plot-styler style X.Report --color "Email Measures.CTR %=#2B6CB0"
$T pbi-plot-styler check X.Report --json                 # bindings and bookmarks; --fix repairs BMK001/002
```

Ask for the brand's hex codes; never guess them. A renamed or removed measure
silently breaks the visuals and bookmarks bound to it: run `check` after model
changes.
