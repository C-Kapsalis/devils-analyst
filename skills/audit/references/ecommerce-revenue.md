# E-commerce and backend revenue against platforms

Three views of revenue, in order of authority: the order system (store,
backend, finance) net of refunds and cancellations; web analytics (the
attribution layer, losing some purchases to blockers and consent); each ad
platform's claim on its own window, overlapping with the others. Align
refunds, tax and shipping, currency, order date vs click date and test orders
before comparing.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| R1 | Sum of revenue claimed by each platform vs the store total | Claims sum above the store total, or above the analytics total for paid channels | The same sale is claimed twice; blended ROAS is fiction | One shared denominator; platform numbers labelled as claims | 1 |
| R2 | Single-touch attribution columns | A last-click column that does not sum to total conversion value | Credit invented or lost | Each single-touch column sums to the total | 1 |
| R3 | Budget ranked on ROAS where margins differ | Low-margin lines with high revenue ROAS ranked first | A healthy revenue ROAS can lose money | Rank on profit on ad spend; break-even ROAS = 1 / gross margin | 3 |
| R4 | Promotion revenue | Promo credited with total sales in the window | Pull-forward, stockpiling and the dip after are ignored | Incremental units x margin - discount cost - pull-forward | 5 |
| R5 | Average order value | Mean pulled up by a few wholesale or B2B orders | Thresholds and targets set on a typical order that does not exist | Median, or split retail from wholesale | 3 |
| R6 | Free-shipping threshold | Far from the typical basket, or none | Many new orders too small to be profitable | Just above the typical basket; test | 4 |
| R7 | Test orders, refunds, cancellations | Included in revenue | Overstated revenue and ROAS | Exclude or net them | 1 |
| R8 | Currency and tax | Platforms in one currency or gross of tax, store in another | Apparent gaps that are units | Align before comparing | 1 |
| R9 | Market share claims | Share with no denominator (units vs revenue, served vs total market) | Board decks overstate position | Label both | 4 |
| R10 | Customer records across store, web and app | Separate records per channel | Cross-channel customers invisible | Unify IDs | 4 |

## Decoys

Analytics revenue a few percent under the store total (blockers, consent);
platform conversions above analytics when windows differ, as long as nobody
adds them up.
