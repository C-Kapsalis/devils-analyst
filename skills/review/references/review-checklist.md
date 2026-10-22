# Review checklist

Each row: the claim that is often wrong, how to spot it from the report (and
the data, if given), the fix, and the usual severity. Ordered by how often
it changes the decision. Severity is a default: raise it when the claim sits
in the headline or drives the recommendation, lower it when it sits in a side
table nobody acts on.

Ids carry the prefix RV- (review) so they never clash with the audit ids,
where A is attribution, C is CRM, D is dashboards and E is email: RV-C3 is
the Search Console lag check below, audit C3 is a CLV check. Cite review
findings with the prefix.

## RV-A. Numbers and aggregation

| # | Claim that is often wrong | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-A1 | A ratio rolled up as the average of row ratios (CTR, CVR, CPC, CPA, ROAS, CTOR, open rate) | Recompute sum(numerator) / sum(denominator) from the table; it differs from the printed total | Print the ratio of sums at every grain | Must if headline, else Should |
| RV-A2 | Monthly users or reach built by adding daily or weekly values | Monthly figure equals the sum of the days or weeks; reach above impressions on a row; reach above the audience that exists | Take the period's distinct count from the source; never sum distinct counts | Must if used for CPM, frequency or CAC |
| RV-A3 | A snapshot summed over time (list size, subscribers, open pipeline, stock) | "Total subscribers" far above the latest list size; a balance column added across months | Use the end-of-period (or average) value | Must |
| RV-A4 | Totals that do not add | Rows do not sum to the total row; percentages do not sum to about 100% | Recompute; find the missing or duplicated row | Must if the total is quoted |
| RV-A5 | Spend joined to orders row by row before dividing (CAC, CPA) | CAC far above spend / customers computed from totals | Aggregate each fact separately, then divide | Must |
| RV-A6 | Unweighted average position or Quality Score | Simple mean of rows; tiny rows weigh like flagship rows | Impression-weighted mean | Should (Must if it picks the page to fix) |
| RV-A7 | Percent change on a tiny base | "+300%" from 3 to 12; a rate tile with no volume | Show the counts; say the base is too small to read | Should |

## RV-B. Definitions

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-B1 | "Conversions" that are not sales | No conversion-action label; CPA implausibly low; conversions far above orders | Scope CPA, CVR and ROAS to the action that means money | Must |
| RV-B2 | Platform revenue added across platforms | Channel revenue sums above the store or analytics total; "total ROAS" built from platform claims | One shared revenue number (store or analytics) against total spend; platform figures labelled as platform claims | Must |
| RV-B3 | Open rate as the email verdict | Open rate is the headline KPI or ranks campaigns | Judge on clicks and revenue; opens as a trend only, with the privacy caveat | Should |
| RV-B4 | Revenue ROAS where margins differ | Products or channels ranked on ROAS with different margins | Rank on profit after cost of goods, or ROAS against 1 / margin | Must if it moves budget |
| RV-B5 | A share with no denominator | "62% of revenue", "25% market share" with a filter on or a served market | Name the denominator; recompute on the unfiltered total | Should |
| RV-B6 | A trend that crosses a definition change | Step change on the day a key event, tracking setup, survey wording or analytics platform changed | Break the series at the change; compare like with like | Must if a win is claimed from the step |
| RV-B7 | Users read as people | "We reached 80,000 people" from analytics users | Say browsers or devices | Nice |
| RV-B8 | Industry figures quoted as the company's own | "$36 per $1 email ROI", "5% retention = 25-95% profit" as a forecast | Replace with the company's own attributed number, or label as an outside benchmark | Should |

## RV-C. Comparisons

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-C1 | A number with no comparator | No prior period, target, control or last year on the tile | Add the same-length prior period and same period last year | Should |
| RV-C2 | Unequal windows | 31 vs 30 days compared on totals; a campaign sent yesterday ranked against month-old ones on lifetime totals | Per-day values; same accrual age | Should (Must if it ranks campaigns) |
| RV-C3 | Search Console "crash" in the last 2-3 days | The drop sits only in the final days | Exclude the lag window; compare same weekdays | Must if it triggers action |
| RV-C4 | GSC clicks minus GA4 sessions as "lost traffic" | A reconciliation line between two systems | Read each against itself over time | Should |
| RV-C5 | A blended rate across groups that behave differently | One CTR or CVR for brand and generic, brand and non-brand organic, mobile and desktop, one giant send and many small ones | Split rows; judge each group | Must if the blend hides a loss |
| RV-C6 | Seasonality read as trend | Month-over-month across a peak; moving average window not equal to the cycle | Same period last year; window equal to the cycle | Should |
| RV-C7 | Top by clicks crowned | Campaigns, pages or sends ranked on clicks or sessions; revenue column contradicts | Rank by revenue or profit, and revenue per buyer | Must if it decides what to repeat |

## RV-D. Causal claims and tests

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-D1 | Attribution credit stated as cause | "Meta drove 40k", "SEO generated" with no holdout, lift study or model named | "Meta was credited with 40k under [model]"; propose a holdout if the decision depends on it | Should (Must if it moves budget) |
| RV-D2 | Exposed vs unexposed as ad effect | "Viewers converted 4.8% vs 1.9% for non-viewers" | Platforms aim at likely buyers; only a randomized control shows the effect | Must if it moves budget |
| RV-D3 | Before/after with no control | "Since the redesign, CVR is up 12%" | Name the rival (season, spend, mix, promo); difference in differences or a test | Should |
| RV-D4 | Significance claimed with no test, or against zero when the change has a cost | "Significant" with no n or p; a lift tested against 0 when the change costs money | Test against the break-even lift | Must if it decides a launch |
| RV-D5 | Test too short or uneven | Under 7 days or partial weeks; arms far from the planned split | Run whole weeks; check sample ratio before reading | Must if it decides a launch |
| RV-D6 | Segment winner from a pivot table | "Works on mobile, not desktop" with no interaction test and thin cells | Call it a hypothesis; test the interaction or rerun | Should |
| RV-D7 | Lift as raw points only | "+0.4 points" with no relative lift and no incremental count | Lift = (T - C) / C; incremental = T conversions - C rate x T users | Nice (Should if it sizes the payoff) |
| RV-D8 | Regression to the mean as a win | Worst units last month fixed and their rebound claimed | Compare with equally bad untouched units | Should |
| RV-D9 | Promo lift = promo-week revenue | No baseline, no dip after, no discount cost | Net incremental after pull-forward and discount | Must if "run it again" depends on it |
| RV-D10 | Last-click ROAS used to cut upper funnel | Display or video ROAS lowest, cut recommended | Treat last click as a floor; test before cutting | Should |
| RV-D11 | Survey or AI-panel finding as customer truth | Low or missing response rate; synthetic respondents with no human check | State the response rate; label as directional | Should |
| RV-D12 | GA4 data-driven attribution quoted on low volume | DDA column identical to last click; a key event with a few hundred conversions a month | Say the model in effect is last click | Must if it moves budget |

## RV-E. Actions

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-E1 | The recommendation does not follow from the corrected numbers | Redo the decision after fixing RV-A to RV-D | Rewrite it on the corrected numbers | Must |
| RV-E2 | An action with no way to verify | No number it should move, no date, no place to check | Add: the metric, the expected direction and size, when and where to check | Should |
| RV-E3 | Display or video judged on CTR or last click | Display "underperforms" at 0.3-0.5% CTR | Judge on reach, viewable impressions, cost per thousand and a holdout | Should |
| RV-E4 | Budget raised where the limit is rank, not budget | "Add budget" while impression share lost to rank dominates | Fix quality or bids first; budget goes where lost-to-budget is high and CPA beats target | Must if it moves budget |
| RV-E5 | Cheap CPC celebrated with no ceiling | No break-even line (margin per sale x CVR) | Compare CPC with the break-even CPC | Should (Must if it scales a losing line) |
| RV-E6 | Universal red/amber/green thresholds | Hard-coded "danger" values with no owner or reason | Owner sets thresholds with a written reason | Nice |
| RV-E7 | A subject-line or creative test recommended while the upstream step is broken | Delivery under 95%, complaints over 0.1%, or tracking broken | Fix the upstream step first | Must |

## RV-F. The "why" section

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| RV-F1 | "Why" written as prose, not computed | No driver bridge or mix vs rate table that sums to the change | Compute the bridge (`whats-changed`) | Should |
| RV-F2 | Parts that do not reconcile | Contributions do not sum to the total change | Recompute | Must if quoted |
| RV-F3 | Mix shift read as performance | A rate moved because the audience mix changed | Within-segment rates at a common mix | Should |
