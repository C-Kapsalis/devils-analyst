# Dashboards and reports in use

For a single report or deck, use the `review` skill. This list is what an
audit of the reporting setup looks for (the dashboards a team relies on
every week). The chart checks in
[../../review/references/chart-checks.md](../../review/references/chart-checks.md)
apply to each page.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| D1 | Ratio measures | Averages of row ratios (CTR, CVR, CPA, ROAS, CTOR) | Every rate on the page is wrong at every total | Ratio of sums at each grain | 1 |
| D2 | Distinct counts and snapshots | Users, reach or list size summed across days or months | Inflated audiences; wrong CPM, frequency and CAC | Period distinct counts; end-of-period snapshots | 1 |
| D3 | Joins | Spend joined to orders row by row; inner joins that drop orphan keys (for example Tableau's "assume referential integrity") | Totals silently too high or too low | Aggregate facts separately; outer joins to surface dirty keys | 1 |
| D4 | Grain | Session-level and user-level facts mixed in one view | Aggregation errors | Document grain per table | 2 |
| D5 | One canonical definition per metric | The same KPI defined differently on two pages or two copies | Teams argue over numbers, not decisions | One definition with owner, numerator, denominator, grain, filters, exclusions | 2 |
| D6 | Comparisons | Tiles with no prior period, target or last year | No way to judge a number | Add the comparator | 3 |
| D7 | Thresholds | Hard-coded red/amber/green values with no owner | Colour drives action with no reason | Owner sets thresholds with a written reason | 4 |
| D8 | "Why" sections | Prose with no driver bridge or mix vs rate split | Causes asserted, not computed | Bridge that sums to the change | 3 |
| D9 | Definitions panel | No definitions or data notes on the page | Readers misread metrics | Definitions on click | 4 |
| D10 | Freshness | No refresh time; "real-time" claimed for on-demand refresh | Decisions on stale data | Show last refresh | 4 |
| D11 | Top N per group | Global Top N shown as per-group | Wrong lists | Filter order fixed (context filter first) | 3 |
| D12 | Classification thresholds in churn or lead-score views | Default 0.5 cut-off | Assumes equal error costs | P >= c / (1 + c) with c = cost of a miss / cost of a false alarm | 3 |
| D13 | Lifecycle counts | Leads counted by today's stage | Monthly funnel wrong | Count by stage-entry date | 1 |
| D14 | Recomputed metrics | A dashboard recomputes CAC in SQL while the governed model defines it differently | Two CACs | Query the governed measure; label translations as untested until reconciled | 2 |

## Decoys

A median labelled as such; a dashed, labelled forecast; filters that apply to
the whole page and say so.
