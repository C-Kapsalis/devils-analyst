---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The pilot write-up and its data contain 5 planted problems. Ground truth (computed from the files):

1. Regression to the mean. The pilot regions were chosen for the weakest Q2-vs-Q1 growth (pilot Q2 growth -6.5%). The next five weakest regions (Aldmoor, Kestwick, Ivelford, Lowmarsh, Carrow Vale), which got no media, also bounced back: Q3 vs Q2 7.0%, against -9.3% for the remaining eight regions. Counts as found if report.md says regions selected for a bad quarter rebound on their own and compares with similar untreated regions (or otherwise names regression to the mean / selection on a bad quarter).
2. Benchmark includes the pilot. "Company total" (-0.2%) contains the five pilot regions; non-pilot regions grew -3.6%. Counts as found if report.md says the comparison group includes the treated regions.
3. Click & collect added mid-pilot. From week of 17 August, Bexwell, Glenhaven, Redfern include click & collect in lfl_sales (column click_collect_included, EUR 163,716 in Q3). Without it, pilot growth is 8.5% instead of 11.2%. Counts as found if report.md notices the click_collect_included amounts (or a definition change in those regions) and removes or flags them.
4. Return on revenue, not profit. The readout's 2.5x is revenue / cost. At the 34% contribution margin even its own EUR 675,213 of extra sales is worth EUR 229,572, a 0.83x return: it does not cover the EUR 275,000 cost. Counts as found if report.md converts to contribution/margin and says the pilot does not pay back (any contribution ROI below 1 or a loss figure).
5. Awareness survey design. The same panel was re-interviewed, the June wave asked directly about Brightwell Pet Supply (sensitising respondents), the two waves use different questions, and no control regions were surveyed. Counts as found if report.md flags at least one of: same panel primed by a brand-naming pre-wave, question wording changed between waves, or no control group for the survey.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 5, each with its substance (a number, column, region names or quoted survey detail). FAIL otherwise.
