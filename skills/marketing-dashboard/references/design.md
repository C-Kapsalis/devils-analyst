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
