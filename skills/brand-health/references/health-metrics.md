# Brand health metrics: what to track, where it comes from, how it lies

Contents: [Buckets](#buckets) · [Survey metrics](#survey) · [Behavioural metrics](#behaviour) · [Search and traffic](#search) · [Social](#social) · [Price and money](#money) · [Tracking design](#tracking) · [Small-brand kit](#small)

<a id="buckets"></a>
## 1. The five buckets

A brand dashboard needs at least one metric from each bucket. A dashboard
that tracks only sales misses the early warnings.

| Bucket | Question it answers | Typical metrics |
|---|---|---|
| Awareness / salience | do people think of us at all? | aided and unaided awareness, recognition, entry into the consideration set, branded search |
| Attitudes / associations | what comes to mind, and is it ours? | association strength, perceived quality, uniqueness ("only brand that..."), sentiment |
| Behaviour | do they buy, repeat, recommend? | trial, repeat at full price, share of wallet, switching, advocacy |
| Relationship quality | is trust holding? | satisfaction, complaint volume and topics, NPS |
| Financial | does the brand earn money a generic would not? | price premium, promo dependence, CLV, customer equity, brand value trend |

Awareness signals potential; loyalty (repeat, share of wallet) signals
realised equity. A dashboard heavy on awareness and light on behaviour
over-reports health.

<a id="survey"></a>
## 2. Survey and tracker metrics

- **Awareness levels:** unaided recall (top of mind), aided recall,
  recognition. Report each as a share of respondents per wave with n.
- **Funnel ratios (Keller pyramid read as a funnel):** salience, meaning,
  response, resonance. Compute stage-to-stage ratios: consideration /
  awareness, preference / consideration, trial / preference, repeat / trial,
  advocacy / repeat. The bottleneck is the lowest ratio relative to a
  competitor's ratio at the same stage, not the lowest level.
- **Perceived quality and associations:** rate own and competitor brands
  on the same attributes; read relative position (rank or gap to the leader)
  rather than absolute scores, because scale use differs between people.
- **Significance:** a wave-to-wave change in a share (awareness 34% to 37%)
  is a two-proportion comparison; run the test in `evidence-check` §1.2 and
  call it "no detectable change" when it fails.
- **Attitude-behaviour gap:** people do not always act on their stated
  attitudes, even when they believe they would. Always pair a tracker with
  one behavioural series from the same period.
- **Survey fatigue:** long attribute batteries produce random answers;
  prefer 6 to 10 attributes.

<a id="behaviour"></a>
## 3. Behavioural metrics

- **Repeat purchase rate at full price:** customers with a second
  non-discounted order / customers with a first order, by cohort. Compute the
  cohort correctly (only cohorts old enough; see `metric-definitions` rule 17).
- **Share of wallet / share of customer:** own category spend / customer's
  total category spend (needs panel or survey data). Customer-centred brands
  manage this instead of share of market.
- **Promo dependence:** revenue from promo periods or discounted orders /
  total revenue. Above 40% means customers are being trained to buy only on
  deal.
- **Customer equity:** sum of CLV over active customers, across all the
  firm's brands. It can fall while brand scores rise (the base is shrinking
  or shifting to low-value customers).
- **CLV to CAC:** is acquisition sustainable; formulas in `metric-definitions`.

<a id="search"></a>
## 4. Search and traffic as brand signals

| Signal | Formula | What it tells you | Trap |
|---|---|---|---|
| Branded search volume | monthly searches for brand terms (Search Console impressions on brand queries, Keyword Planner, Trends) | people looking for you, not the category | volume grows with the whole category and with seasons |
| Share of search | own brand-term volume / sum of brand-term volumes for own + named competitors | your share of brand-seeking demand; the share-of-voice formula applied to search | competitor list must be the same every period |
| Brand vs category index | own brand-term volume / generic category-term volume | are you gaining or losing within your category's demand? | category terms must be fixed in advance |
| Direct traffic | GA4 direct sessions | partly brand recall | also includes bookmarks, app opens and untagged links; a new app or broken UTMs inflate it |

Read search in this order: own volume, then share of search, then index vs
category. If own volume rose but share fell, competitors rose faster: the
category grew, the brand did not. Compare the same months year on year
before reading a trend.

<a id="social"></a>
## 5. Social signals

- **Reach vs impressions:** reach = unique viewers; impressions = times
  shown. Never present impressions as audience size.
- **Engagement ladder:** clicks and likes are cheap; comments show
  interaction; shares put the brand in front of someone else's audience and
  are the strongest resonance signal. Engagement rate = engagements / reach,
  computed from summed parts.
- **Share of voice:** own mentions / all mentions (own + competitors) in
  the same listening tool and period. Include untagged and misspelled
  mentions; tagged-only counts miss most conversation.
- **Sentiment:** classify positive, negative, neutral; net sentiment =
  (positive - negative) / all. Track it over time and against competitors.
- **Topic tags:** tag mentions and inbound messages by topic (support issue,
  product feedback, pricing, delivery, feature request). Report tag volumes
  and trends: they show what drives negative vs positive sentiment.
- **Brand-specific or category-wide?** Only a competitor benchmark can tell.
  A rise in mentions that competitors share is a category event.

<a id="money"></a>
## 6. Price and money

- **Price premium:** own average paid price / generic or category average
  paid price - 1. Use paid (transaction) prices, not list prices.
- **Price sensitivity:** % volume change / % price change at regular price,
  estimated on quarterly data (see long-view.md). A rising trend means the
  premium is weakening.
- **Price test:** raise price 5 to 10% in a test cell or period and measure
  the volume lost; it is the cheapest direct read of brand strength.
- **MROI:** gross profit delivered by the product / marketing spent on it.
- **Brand value:** see architecture-moves.md §6; always a range.

<a id="tracking"></a>
## 7. Tracking-study design

| Design question | Why |
|---|---|
| What is the baseline period? | without it, change is vague |
| How often is it measured? | too sparse misses movement; too frequent is noise |
| Which segments are kept separate? | averages hide drift |
| Which touchpoints are included? | meaning forms across encounters, not ads alone |
| What action will each metric trigger? | a metric that triggers nothing is dead weight |

Keep raw data for years: brand trajectories need long series.

<a id="small"></a>
## 8. Small-brand kit (no paid tracker)

| Track | Free source | Tells you |
|---|---|---|
| Repeat rate without promotion | Shopify / POS / email purchase history | do customers come back without a deal? |
| % of revenue from promotions | own sales data | above 40% = training deal-seekers |
| Sentiment and user content | listening tools, reviews | is the story resonating, or only the price? |
| Direct traffic and branded search | GA4, Search Console | are people seeking you or the category? |
| Price elasticity | occasional 5 to 10% price tests | how much volume a price rise costs |
| CAC vs CLV | basic finance data | is growth sustainable? |
