# Chart checks

A chart is wrong when a reader looking at it for five seconds would believe
something the numbers do not support. Flag the chart, say what a reader
believes, and give the number that corrects it.

| # | Flaw | Spot it | What the reader wrongly believes | Fix | Default |
|---|---|---|---|---|---|
| 1 | Truncated bar axis | Bar axis starts above zero (e.g. at 80,000) | A 6% gap looks like a doubling | Bars start at zero; put the % gap in the label | Must if the text repeats the exaggeration, else Should |
| 2 | Dual axes that mislead | Two y-axes scaled so lines cross at a "turning point" | A relation or crossover that is an artefact of scaling | One axis, or indexed lines (start = 100); two axes only when the relation is the point, both labelled in series colours | Should |
| 3 | Pie with many slices | More than 5 slices, legend instead of labels | Nothing precise; slices cannot be compared | Sorted bars with share labels, or a treemap with at most 10 tiles | Nice |
| 4 | Rate without volume | KPI tile shows a rate and a change, no count ("CVR 9.8%, +3.1 pts" from 41 sessions) | A big win where the base is too small to read | Show the count behind every rate; grey out tiles under a minimum volume | Should (Must if it drives a budget move) |
| 5 | Cumulative line hiding a decline | Year-to-date or month-to-date line still climbing while each recent period fell | "Still growing" | Per-period bars next to the running total | Must if the headline says growth |
| 6 | Rainbow palette for ordered data | Retention or heat table coloured red, yellow, green, blue | False boundaries between values | Sequential single-hue scale | Nice |
| 7 | Diverging scale off-centre | Week-over-week change on a sequential scale, or a diverging scale whose neutral sits away from zero | Small declines look neutral or positive | Diverging scale centred on zero (or on plan) | Should |
| 8 | Smoothing that hides a step | Moving average with no window stated; a tracking break turned into a gentle slope | A gradual trend where there was a break | State the window; show the raw series around breaks | Should |
| 9 | Mean on skewed data | "Average order value" pulled up by a few very large orders | A typical order that does not exist | Median for skewed measures, say which | Must if it sets a price, threshold or target |
| 10 | Filtered percent of total | "Google Ads is 62% of revenue" with a Paid filter on | The channel's share of the business | Label the denominator; recompute on the full total | Should |
| 11 | Extrapolated trend line | Solid fit line running past the last data point | A forecast nobody made | Stop fits at the last observed point; forecasts dashed and labelled | Should |
| 12 | Bubble sized by radius | Bubble radius proportional to spend | Twice the spend looks four times bigger | Size by area, or use bars | Nice |
| 13 | Topic title | Title names a topic ("Email performance"), not the answer | Nothing; the reader must work out the point | Title states the answer with its number | Nice |
| 14 | Inconsistent colours | The same channel in different colours on different charts | Wrong series compared | One colour per channel everywhere | Nice |
| 15 | Map on pooled data | Every region shows the same rate, or regions inferred from account names | Regional differences that are not in the data | Sorted bars on regions with real data; drop the map | Should |

How to check from a description or HTML: read the axis minimum, the scale
type, the filter state, the n behind each rate, and whether lines extend past
the data. If a chart is only described in words and the description omits
the axis or filter, say so under "Not checked" instead of guessing.
