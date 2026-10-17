---
name: brand-health
description: >-
  Use this skill when the question is about the brand rather than one campaign: "is our
  brand getting stronger or weaker", "is our brand healthy", brand awareness, consideration
  or preference from a tracker or survey, brand search or branded search volume, direct
  traffic as a brand signal, share of voice or share of search against competitors, social
  mentions and sentiment, "are promotions hurting the brand", baseline sales, how much of
  revenue comes from discounts, price premium or "can we raise prices", "should we cut
  brand ads and put it into performance", brand vs performance budget, a brand equity or
  brand score that stayed flat, NPS or preference up but repeat purchase down, "should we
  launch [product] under our brand", line or category extension, sub-brand or new brand,
  repositioning, rebrand, "milk or kill this brand", brand valuation, and whether content
  is on-brand (positioning, personality, archetype). It measures brand health from the
  data, separates short-term sales from long-term equity, checks per segment instead of on
  averages, and turns the result into a decision with a way to verify it.
---

# brand-health

Brand questions get answered with the wrong number more often than most:
a total that hides the segment that matters, a sales spike that hides a
falling baseline, a growing search volume that hides a shrinking share. This
skill measures brand health from data and turns it into a decision. Compute
every number in code. Volume next to every rate.

Related skills: the `diagnose` skill holds the qualitative brand-strategy
states (diagnose/references/brand-diagnostic.md); use it to name the state
after this skill has measured it. Use `metric-definitions` for formulas of
CLV, CAC, repeat rate and engagement rate, and `evidence-check` for
significance tests, holdouts and pull-forward.

## 0. The human owns the question and the decision

Before any analysis, confirm two things with the user. Do not assume them.

1. **The decision.** What will change depending on the answer (budget split,
   price, launch, discount calendar, rebrand)? If none, say the analysis is
   monitoring, not a decision.
2. **The frame.** Which competitors, which category terms, which customer
   segments, which period. A brand is healthy only relative to a frame.

If either is missing and cannot be read from the data, ask one short
question listing your default (for example "I will compare against the three
brands in the file and treat 2024 as the baseline year: right?").

## 1. Route the question

| The user asks | Go to | Depth in |
|---|---|---|
| Is the brand getting stronger or weaker? | §3 scorecard, then §5 | [health-metrics](references/health-metrics.md) |
| Are promotions or discounts hurting us? Promotions "work better than ever"? | §4 long view | [long-view](references/long-view.md) |
| Brand vs performance budget, cut brand ads? | §4, then `evidence-check` §4 | [long-view](references/long-view.md) |
| Brand score, NPS or preference flat or up, but sales or repeat down (or the reverse) | §5 per customer | [per-customer-equity](references/per-customer-equity.md) |
| Search, mentions, sentiment, share of voice moved | §3 rows 4 to 8 | [health-metrics](references/health-metrics.md) |
| Can we raise prices / is our premium safe? | §3 row 9, §4 | [long-view](references/long-view.md) |
| Is this content, claim or campaign on-brand? Is our positioning clear? | §6 | [positioning-content](references/positioning-content.md) |
| Extension, sub-brand, reposition, rebrand, milk/prune/sell, brand value | §7 | [architecture-moves](references/architecture-moves.md) |

## 2. What the data must contain

| Question | Minimum data | If missing |
|---|---|---|
| Health trend | the same metric at the same grain for at least two comparable periods, plus one competitor or category series | report levels only; say "no trend or benchmark, no verdict" |
| Promotions vs baseline | weekly (or daily) units or revenue with a promo flag or discount amount, 8+ quarters ideally, at least 4 | if no promo flag, infer promo weeks from discount_amount > 0 and say so |
| Survey / tracker | respondent-level rows with segment, wave, and the scores; n per wave | aggregate-only scores: report, but refuse a segment verdict |
| Share of voice / search | own and competitor mentions or brand-term volumes, same source and period | own-only volume cannot show share; say growth may be category-wide |
| Extension or reposition | intent or fit scores split by current customer vs not, and by segment | refuse a go/no-go from one average |
| Valuation | branded price, generic price, units, assumptions | refuse a single number; give a range |

Refuse or caveat: a causal claim from a tracker alone (attitudes do not
equal behaviour); a verdict on a survey change smaller than its sampling
error (test it as a proportion with `evidence-check` §1.2); a perceptual map
from fewer than about 100 respondents; direct traffic read as pure awareness
(it also counts bookmarks and app opens).

## 3. The brand health scorecard

Compute each row that the data allows, per period, own brand and benchmark.

| # | Metric | Formula | Healthy reading | Trap |
|---|---|---|---|---|
| 1 | Aided / unaided awareness | aware respondents / respondents, per wave | rising or stable vs competitors | awareness is potential, not equity |
| 2 | Funnel conversion | consideration / awareness, preference / consideration, repeat / trial | find the stage with the biggest drop: that is the bottleneck | comparing stage levels instead of stage ratios |
| 3 | Repeat rate without promotion | customers repeating at full price / customers | stable or rising | repeat driven by coupons is not loyalty |
| 4 | Share of search | own brand-term volume / (own + competitor brand-term volumes) | stable or rising | own volume up while share falls = category tide |
| 5 | Brand vs category demand | own brand-term volume / generic category-term volume | stable or rising | seasonal category swings |
| 6 | Share of voice | own mentions / all mentions (own + competitors), same tool | stable or rising | tagged mentions only; untagged and misspelled count too |
| 7 | Net sentiment | (positive - negative) / all mentions; plus negative mentions by topic tag | stable or rising; no topic driving negatives | volume growth read as "buzz" when it is complaints |
| 8 | Engagement quality | shares / reach and comments / reach, next to likes / reach | shares growing | likes are the cheapest signal; impressions are not reach |
| 9 | Price premium | own average paid price / category or private-label average price - 1 | stable or rising at stable volume | list price instead of paid price |
| 10 | Promo dependence | revenue in promo periods (or discounted orders) / total revenue | below 40% | above 40% the brand is training deal-seekers |
| 11 | Baseline sales | average non-promo-week sales per quarter | flat or rising | see §4 |
| 12 | Customer equity | sum of CLV across active customers (or active customers x CLV per segment) | rising | brand score up while this falls |

Read the scorecard as a whole: the verdict is the direction most rows agree
on, after §5 has checked that no segment reverses it.

## 4. Short term vs long term (the long view)

Run this whenever promotions, discounts or a brand-vs-performance budget
are in the question. Full method in [long-view](references/long-view.md).

1. Flag promo weeks (promo flag, or discount_amount > 0). Keep the 1 to 2
   weeks after each promotion separate (pull-forward, see `evidence-check`).
2. Per quarter: **baseline** = mean sales in non-promo weeks; **lift** =
   mean promo-week sales / that quarter's baseline; **promo share** = promo
   revenue / total revenue.
3. Trend each across quarters (slope, and first vs last quarter).
4. Read the pattern:

| Baseline | Lift | Reading | Action |
|---|---|---|---|
| falling | rising | customers trained to wait for deals; promotions look better because the base eroded | cut promo frequency and depth, protect baseline, expect a short dip first |
| falling | flat or falling | brand erosion or category decline | compare with category (§3 rows 4 to 6) before blaming promotions |
| flat or rising | stable | healthy | keep calendar; test one fewer promotion |
| rising | falling | equity building | do not add discounts |

5. Price sensitivity: estimate it on quarterly, not weekly, aggregates
   (weekly data overstate it several-fold because of stockpiling). Rising
   sensitivity over quarters means the premium is eroding.
6. Brand budget questions: a short attribution window misses most brand
   effects, and brand ads keep working after they stop. Do not cut brand
   spend on short-window ROAS; propose a geo or time holdout read on
   baseline sales and branded search over at least two quarters.
7. Remember the triangle: equity, share and short-term profit cannot all be
   maximised at once. Say which one the recommendation trades away.

## 5. Per customer, never only the average

A single brand score averaged over all respondents is true of nobody.

1. Split every survey or tracker metric by segment (customer vs
   non-customer, value tier, tenure, region) and by wave. Report n per cell
   and test each change for sampling error before calling it.
2. Weight by value, not headcount, before a verdict: weight each segment's
   score change by its share of CLV or revenue. A stable average with a
   falling high-CLV segment is a decline.
3. Check composition: if the respondent mix changed between waves, compare
   at a common mix (as in `evidence-check` §3).
4. Check behaviour against attitude: stated preference or NPS up while
   repeat rate or share of wallet falls means trust the behaviour.
5. Use rank or relative scores across brands, not absolute scale points
   (one person's 6 is another's 4).
6. Name which equity drives choice in this category (value, brand or
   relationship) before recommending a brand investment; see
   [per-customer-equity](references/per-customer-equity.md).

## 6. Positioning and content checks

Use [positioning-content](references/positioning-content.md) when the
question is "is this on-brand", "why are we known but not chosen", or a
claim review. In order:

1. **Frame:** does the customer place us in the intended category? (search
   queries, comparison sites, who we are compared with).
2. **Points of parity:** list the category must-haves; rate each 1 to 10
   (survey or reviews). Any below 7 is a disqualification risk: fix before
   promoting a difference.
3. **Points of difference:** relevant, distinctive ("only", not "best"),
   believable (one provable reason to believe), deliverable (feasible,
   profitable, hard to copy).
4. **Content:** score each piece against the brand's chosen personality
   dimension (sincerity, excitement, competence, sophistication, ruggedness)
   and archetype; flag pieces that express another one, claims without
   proof, and SEO targets that pull an off-brand audience.

## 7. Architecture and growth moves

Use [architecture-moves](references/architecture-moves.md). Decision rules:

| Move | Decide on | Rule |
|---|---|---|
| Extension | intent and fit split by current core customers vs others | same brand only if the extension's buyers resemble current customers; similar product but different customers fails; core-customer permission below 6/10 means sub-brand or new brand |
| Line vs category extension | cannibalization (share of extension sales taken from the core) vs incremental | line extensions: watch cannibalization; category extensions: watch permission and spillover risk |
| Reposition | trigger severity (blip, cyclical, structural, existential) | blips and cycles do not justify repositioning; move in steps inside the latitude of acceptance; identity brands use a sub-brand |
| Rebrand | evidence the experience has changed | a new name without new experience keeps the old associations |
| Decline | brand health x market health | strong/strong invest; strong brand, weak market milk; weak brand, strong market fix or sell; weak/weak prune; try reposition, extension and new markets before milking |
| Valuation | price-premium NPV with ranges | always show the sensitivity to discount rate, brand share of premium and growth |

## 8. Adversary for every move

Run the attack for each step you used. A step whose check fails is redone
or downgraded as the last column says.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Accept the question | Is this the decision the user is making, and the frame they mean? | §0 answers on record (decision, competitors, period, segments) | ask the one question; do not proceed on a guess |
| Compute a metric | Is the numerator and denominator from the same source, grain and period? | recompute one total two ways (sum of rows vs reported total) | fix the grain or join and recompute |
| Call a trend | Is the change larger than noise and not a season? | proportion test for survey changes; same period last year for search and sales | label "no detectable change" |
| Credit or blame the brand | Did the category or competitors move the same way? | share of search, share of voice, own vs category index (§3 rows 4 to 6) | reframe as category movement |
| Read an average | Does any segment, especially the high-value one, move the other way? | §5 split and CLV weighting | report the segment, change the verdict |
| Trust a survey | Does behaviour agree with the attitude? | repeat rate, share of wallet, baseline sales in the same period | trust behaviour; mark the attitude result as unconfirmed |
| Judge a promotion | Is the lift real growth or a falling base? | baseline and lift trend by quarter (§4) | rewrite the verdict around baseline |
| Read a mentions spike | Is the growth positive talk or complaints? | negative share and topic tags before vs after | report it as an issue, route to service or product |
| Name a cause | What else produces the same pattern? | list two rivals and the data that rules each out | label it a hypothesis and name the test |
| Approve an extension or reposition | Who exactly says yes: our customers or others? | intent split by current core vs non-customers; latitude check | recommend sub-brand, new brand, or a smaller step |
| Recommend | What does it cost if this is wrong, and what would the CFO ask? | downside in money or customers, and a verification test with a date | add a holdout or shrink the bet |
| Put a value on the brand | How much does the number move with the assumptions? | sensitivity table (discount rate, brand share of premium, growth) | give a range, not a point |

## 9. Score-and-probe gate before handover

1. Every adversary check in §8 for the steps used must pass (or be
   explicitly downgraded in the text). Do not score a draft that still
   has a failing check.
2. Score the draft 0 to 100 on four criteria: **clarity** (one verdict, plain
   words, numbers a reader can redo), **relevance** (answers the user's
   decision, in their frame), **depth** (benchmark, segments and long-term
   view covered where the data allows), **insightfulness** (says something
   the headline number did not).
3. If any score is below 80, write the probe question that would raise it
   (for example "which segment drives the flat score?"), answer it from the
   data, revise, and re-score. Maximum two loops; after that, ship and list
   what is still weak.
4. End by naming what the human must decide: the question and the
   decision stay theirs. State the trade-off they are choosing.

## 10. Output format

```
Verdict: [brand stronger / weaker / no detectable change / inconclusive]: [one line]
Deciding number: [e.g. "baseline sales -18% over 6 quarters while promo lift rose 1.3x -> 1.9x"]
What the headline number says and why it misleads: [one line]
Benchmark: [own vs category / competitors]   Segments: [the one that matters]
Action: [what to do] · Trade-off: [equity vs share vs short-term profit]
How to verify: [test, metric, date] · Your decision: [the choice left to the user]
```

Keep a short table of the computed checks under the verdict so the reader
can redo the arithmetic.
