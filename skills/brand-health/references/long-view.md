# The long view: promotions, baseline and brand budget

Contents: [Why short-term data mislead](#why) · [Baseline method](#method) · [Price sensitivity](#sensitivity) · [Brand vs performance budget](#budget) · [The triangle](#triangle) · [Patterns](#patterns)

<a id="why"></a>
## 1. Why short-term data mislead

Real-time sales data make promotions look very profitable: the spike is
visible this week, while the cost (lower future baseline, lower price
premium, competitor retaliation) arrives later and is hard to attribute.
Advertising works the other way: little shows this week, most arrives over
the following months. Three forces push managers short: abundant
short-term data, hard-to-measure long-term effects, and brand-manager
tenures shorter than the effects.

The vicious cycle: frequent discounts -> customers learn to wait and
stockpile -> baseline falls -> lift over baseline rises -> promotions look
even better -> more discounts -> premium erodes -> deeper discounts needed.

Published benchmarks (Lodish and Mela) are useful as stated assumptions,
never as facts about this brand: the long-run effect of a promotion is
about 80% of its short-term effect (a 20% penalty); the long-run effect of
advertising can be about 60% larger than its short-term effect; roughly
half of TV campaigns show no lift at all, so test.

<a id="method"></a>
## 2. Baseline and lift, step by step

Input: weekly units or revenue, a promo flag or discount amount.

1. Mark promo weeks. If no flag exists, treat weeks with discount_amount > 0
   (or average discount above a stated threshold) as promo weeks and say so.
2. Mark the 1 to 2 weeks after each promotion as "post-promo"; exclude them
   from the baseline and report them (pull-forward dip, see
   `evidence-check` §4).
3. For each quarter q:
   - `baseline_q = mean(sales in non-promo, non-post weeks of q)`
   - `lift_q = mean(sales in promo weeks of q) / baseline_q`
   - `promo_share_q = promo-week revenue / total revenue in q`
4. Trend: first quarter vs last quarter, and the slope of a simple
   regression of baseline on quarter index. Remove seasonality by comparing
   the same quarter year on year when there are 8+ quarters.
5. Total sales can be flat while baseline falls and promo share rises: the
   brand is replacing full-price demand with discounted demand.
6. Contribution check: compare full-price margin on baseline units with the
   margin left on promo units after discount; a rising promo share at a
   lower margin lowers profit even at flat revenue.

What to say: "promotions look more effective (lift 1.3x -> 1.9x) because
the base they are measured against fell 20%". The recommendation is fewer
and shallower promotions plus brand support, with a warning that the first
quarters may dip before the baseline recovers (the Clorox pattern:
revenue and profit dipped for two quarters after cutting discounts, then
baseline rose and lift fell).

<a id="sensitivity"></a>
## 3. Price and promotion sensitivity

- Estimate on quarterly aggregates. Weekly data overstate price
  sensitivity several-fold (about 7x in the source study) because they
  capture stockpiling and miss competitor reactions.
- Track the trend across years, not one estimate: rising sensitivity means
  the brand is losing differentiation.
- Also track response to regular price (willingness to pay full price),
  not only response to deals.

<a id="budget"></a>
## 4. Brand vs performance budget

- Short attribution windows count the last click; brand advertising mostly
  raises baseline, branded search and direct demand over months. A brand
  campaign judged on 7-day ROAS will always lose to search.
- Do not cut brand spend on short-window ROAS. Propose a test: hold out
  regions or a period, and read baseline sales, branded search share and
  new-customer volume over at least two quarters (incrementality method in
  `evidence-check` §4).
- Distribution and assortment also have long-term effects (Lacoste: cheap
  channels lifted sales short term and cost the brand its standing for
  years). Count them in the trade-off.
- Someone above the brand manager must own the long-term metrics; say who
  should review them.

<a id="triangle"></a>
## 5. The brand management triangle

| Objective | Raised by | Hurt by |
|---|---|---|
| Brand equity | higher price, advertising, selective distribution | discounting, cheap channels |
| Market share | lower price, quality, ad and promo spend | price rises, spend cuts |
| Short-term profit | price rises, cost and spend cuts | spend increases, discounts |

Every recommendation trades one of these. Name the one being traded.

<a id="patterns"></a>
## 6. Patterns and readings

| Pattern | Reading |
|---|---|
| Lift rising, baseline falling | trained deal-seekers; the promotion "improvement" is an artefact |
| Promo share above 40% and rising | brand depends on discounts; premium at risk |
| Baseline falling, competitors' too | category decline; check before blaming promotions |
| Brand ad cut, sales flat for a quarter | expected; effects lag; read baseline and branded search for 2+ quarters |
| Price premium stable, volume down | demand problem, not pricing power; look at funnel |
| Price sensitivity up year on year | differentiation eroding; check share of voice and associations |
