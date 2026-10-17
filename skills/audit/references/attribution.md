# Attribution and incrementality

Attribution assigns credit according to a model someone picked. It does not
show what the spend caused; that takes a holdout or a test.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| A1 | GA4 reporting model vs 30-day conversions per key event | Data-driven selected on low volume; DDA column equal to last click | Silent last click; budget follows the wrong model | Report the model in effect; pick an explicit rule-based model | 1 |
| A2 | Lookback windows across reports and platforms | 30-day view compared with 90-day view; Meta 7-day click + 1-day view against Google 30-day click | Settings, not performance, make the difference | State and align windows before comparing | 1 |
| A3 | Platform conversions summed across platforms | Totals above site or store totals | Double counting | One de-duplicated source | 1 |
| A4 | Model switch log | Model changed with no note to bidding owners | Smart Bidding uses attribution as its signal; ROAS and bids change at once | Annotate; brief owners | 2 |
| A5 | Model vs business cycle | Last click on a long B2B cycle; first click on a short promo shop | Assists under- or over-credited | Short and transactional: last click or time decay; long: position-based or linear; mature with volume: data-driven | 3 |
| A6 | Time-decay half-life | 7 days on a long consideration cycle | Early touches get nothing | Calibrate to the real cycle | 4 |
| A7 | Custom data-driven models on little data | Markov under about 2,000 conversions a month; Shapley under about 5,000 | Overfit | Rule-based model, stated | 3 |
| A8 | Exposed vs unexposed | Sold as ad effect | Platforms target likely buyers | Randomised holdout | 5 |
| A9 | Retargeting, brand search, PMax brand share | Credited at full value with no test | Much may be people who would have bought anyway | Holdout or pause test | 5 |
| A10 | Last-click ROAS on awareness lines | Used to cut display or video | Last click is a floor, lowest for upper funnel | Test before cutting | 5 |
| A11 | Spend-vs-sales charts | "They move together" | Budgets often follow past sales | Experiments or a time-series design | 5 |
| A12 | Direct across models | "Direct did not change, so it is robust" | Direct is identical by construction in GA4 models | Explain it | 4 |
| A13 | Rule-based model used for channel cuts | Built only on converting paths | Non-converting paths ignored | Data-driven with volume; experiments for causal questions | 4 |

MMM (adstock, saturation) is not covered by these notes beyond the principle
that last-click is a floor and models need tests to calibrate them. Do not
audit an MMM from this list.

## Decoys

Last-click and DDA columns that differ when DDA has volume; Direct identical
across models; Meta reporting more conversions than GA4 when windows differ.
