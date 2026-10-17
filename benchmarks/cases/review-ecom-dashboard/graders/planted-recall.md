---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The dashboard (dashboard_sep2026.html) contains 6 planted problems. Answer key:

1. Truncated bar axis behind a false headline. The bar chart of the top 3 channels starts its y axis at 3,100, and its title says "Email revenue nearly double Paid Social". Email is $3,462 and Paid Social $3,275: Email is only 6% higher. Counts as found if report.md says the axis does not start at zero (or the bars exaggerate) AND that the real gap is small (about 6%, or quotes both values), so the headline and the "shift 15% of Paid Social into Email" action are not supported.
2. Average order value inflated by wholesale. The tile shows $217 (the mean of all 305 orders, including 5 wholesale invoices of $7,600 to $10,400). The median order is $58 (retail median $58, retail mean $65). Only 0.3% of web orders are $200 or more, so a $200 free-shipping threshold set "in line with our typical order" is wrong. Counts as found if report.md says the AOV is pulled up by the wholesale orders (or quotes a median or retail figure between $55 and $75) and challenges the $200 threshold.
3. Rate without volume. The TikTok landing page tile "9.8%, +3.1 pts" comes from 41 sessions and 4 orders (August: 30 sessions, 2 orders). Counts as found if report.md says the base is too small to read (cites the 41 sessions or 4 orders) or that the tile needs its volume, and that "scale it" is not supported.
4. Cumulative chart hiding a decline. "Revenue year to date: still climbing" is a running total; the weekly file shows each of the last four weeks fell (week 35 $6,831, then $6,384, $4,962, $4,751, $3,504). Counts as found if report.md says the weekly revenue has been falling for several weeks and the cumulative line hides it.
5. Filtered percent of total. "Google Ads share of revenue 60%" is computed with the filter Channel group = Paid; Google Ads is 31% of all web store revenue ($6,116 of $19,601). Counts as found if report.md says the share uses the paid-only denominator and gives a figure between 29% and 33% or says it must be relabelled as share of paid revenue.
6. Pie chart with 9 slices for revenue share. Counts as found if report.md recommends replacing the 9-slice pie with sorted bars (or similar).

List which ones were found in your reasoning.
PASS if report.md identifies at least 5 of the 6 problems, each with its substance (a vague mention such as "double-check the charts" does not count).
FAIL if it identifies fewer than 5.
