# Paid search (Google Ads, Microsoft Ads)

Read the account in this order; do not tune devices or schedules while the
steps above them are broken: conversions, overview by campaign, brand vs
generic split, leakage, search-term waste, new queries, return on spend,
pacing, devices and timing.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| PS1 | Conversions segmented by conversion action | The Conversions column mixes micro actions (newsletter, account sign-up, add to cart) with purchases; CPA looks tiny, CVR spectacular | Smart Bidding and every CPA or ROAS read optimise toward email addresses, not sales | Make the purchase (or the action that means money) the only primary conversion; read CPA and ROAS on it | 1 |
| PS2 | Raw export with empty conversion columns | Profitability reads zero or blank | Analyst concludes "nothing converts" | Scope the export to a conversion action first | 1 |
| PS3 | Search terms by campaign type: brand campaign x brand query, generic campaign x brand query | Generic campaigns serving brand queries (generic looks brilliant); brand campaign paying for generic queries | Generic gets scaled on borrowed brand demand; brand budget leaks into low-intent traffic | Brand terms as negatives in generic campaigns; generic terms as negatives in brand | 2 |
| PS4 | Brand vs generic split of CTR, CPC, CPA | Account CTR or CPA healthy only because brand carries it; generic CPA above break-even | A blended average describes a business that does not exist; generic can lose money under brand's halo | Report brand and generic as separate lines, never blended | 2 |
| PS5 | Search terms sorted by cost with zero conversions | Informational or irrelevant clusters (how to, care, repair, jobs, free, second-hand, salary) with spend and no sales | Pure waste, every day | Negative the whole cluster; review the report monthly | 2 |
| PS6 | Search-terms coverage claims | The visible terms treated as all the terms ("waste is 8% of spend") | Since 2020 only terms with enough volume show; often 40-60% of click-driving queries are visible | Treat query level as a sample; make spend calls at campaign or ad group level | 4 |
| PS7 | Impression share, lost to budget, lost to rank, per campaign | A campaign beating its CPA target loses much impression share to budget, while uncapped campaigns above target run over budget | Profitable volume left unbought; money flowing to the worst unit economics | Raise the cap on the profitable campaign; pull back the over-target one | 3 |
| PS8 | Lost to rank on campaigns asking for budget | "Add budget" while lost to rank dominates | More budget buys nothing when rank is the limit | Fix Quality Score components or bids first | 3 |
| PS9 | Average CPC vs break-even CPC (margin per sale x CVR) per line | CPC above the ceiling on a line called "efficient" or "cheap" (40 margin x 5% CVR = 2.00 ceiling; a 2.40 click loses money) | Every click loses money on average | Cap bids at break-even or fix CVR; raise the ceiling only with repeat-purchase evidence | 3 |
| PS10 | Quality Score weighted by impressions or spend | Large share of spend on keywords with below-average landing page experience or QS 1-5 | QS 10 roughly halves CPC against average; QS 1 multiplies it several times | Fix the below-average component (page, relevance, expected CTR) before raising budget | 3 |
| PS11 | Account-level QS or impression share as a simple mean of rows | Small keywords weigh like flagship ones; "<10%" and ">90%" buckets treated as numbers | Wrong visibility number | Impression-weighted averages; treat buckets as clamped | 4 |
| PS12 | Match types: cost per sale, not CPC | Broad has the lowest CPC and the worst cost per sale, and budget is moving to it | Cheap clicks that never convert | Read cost per sale per match type; keep broad for discovery with negatives | 2 |
| PS13 | Ad groups: keywords per group | One group with dozens of mixed keywords and one generic ad | Lower CTR and higher CPC than tight groups | Split into themed groups of about 5-15 keywords with matching ad and page | 4 |
| PS14 | Month-to-date spend, trailing 7-day spend, projected month end per campaign | A profitable campaign hits its cap by midday every day; another runs far over plan | Google may spend up to 2x the daily budget on a day; only the month (daily x 30.4) is capped. Under-spend on a converter is the quiet failure | Project on the last 7 days per campaign; move money between campaigns | 3 |
| PS15 | Device and schedule modifiers on Target CPA or Target ROAS campaigns | Manual modifiers set and credited for results | Automated bidding prices device and time into each auction; the modifiers are not applied as set | Remove them or treat as no-ops; manage through targets | 4 |
| PS16 | Geo report | A map drawn from one pooled row or regions inferred from account names | Bids move on a number that does not exist per region | Adjust geo only where data resolves to real markets | 4 |
| PS17 | Brand campaign spend with no holdout | Brand ROAS cited as proof of value | Brand clicks may be ones the organic listing would win free; evidence goes both ways | Geo or time-split pause test; check organic brand position first | 5 |
| PS18 | Revenue ROAS on low-margin lines | Revenue ROAS above target on a line that loses money after cost of goods | Healthy revenue ROAS can be a loss | Profit on ad spend when margins are known | 3 |
| PS19 | Converting paid themes with no organic page | Paying every month for demand an evergreen page could win | Rented demand | Brief SEO pages from paid converting queries | 4 |
| PS20 | Markets and engines read only as a blended total | Strong home market masks a weak one | Losses subsidised and unseen | Read account by account and engine by engine | 3 |

## Decoys

Brand CTR of 30-50% and the lowest CPA; phrase or exact with the highest CPC
but a good cost per sale; a small lost-to-rank share on brand; impression
share reported as "<10%".
