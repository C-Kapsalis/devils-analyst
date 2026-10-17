---
name: channel-audit
description: >-
  Use this skill when a marketer asks whether a digital channel or tactic pays and what
  to change in it: "should we raise our Google Ads bids or budget", "we're losing
  impression share", "what's the most we can pay per click", "is our Quality Score
  hurting us", "is display worth it, the CTR is terrible", "which audience or day did the
  ad work for", "should we cap frequency", "are our influencers worth it", "should we
  work with bigger creators", "TikTok or Instagram", "do discount codes help", "which
  keywords should we target for SEO", "why don't we rank", "our pages compete with each
  other", "are our backlinks good", "why aren't we in the local map pack", "how do we
  get cited by ChatGPT or AI Overviews", "which attribution model should we use",
  "data-driven and last click show the same", "where do people drop out of checkout",
  "is our bounce or cart abandonment bad". It works per campaign, creator tier, keyword
  or segment with break-even maths on margin, and labels what attribution can and cannot
  prove.
---

# channel-audit

Account averages hide the losers. A Google Ads account with CPA under margin
can carry campaigns that lose money on every click; an influencer program can
look strong because big creators bring the most orders while each of their
posts loses money; a keyword list ranked by volume is mostly terms you cannot
move. Judge each unit (campaign, creator tier, keyword, segment) on margin,
then recommend.

**The human owns the question and the decision.** Restate the decision in one
line. Ask for what the data lacks: gross margin or margin per conversion,
the primary conversion, the target audience. Never assume margin = revenue.

## 1. Route

| Question | Read first | Reference |
|---|---|---|
| Bids, budget, impression share, max CPC, Quality Score | Section 2 | [paid-search-economics.md](references/paid-search-economics.md) |
| Display or video value, ad lift test, which segment or frequency worked | Section 3 | [ad-lift-segments.md](references/ad-lift-segments.md) |
| Influencers: tiers, platforms, codes, rebooking | Section 4 | [influencer-roi.md](references/influencer-roi.md) |
| SEO keywords, cannibalization, on-page, backlinks, local, AI answers | Section 5 | [seo-search-visibility.md](references/seo-search-visibility.md) |
| Attribution model, channel credit, cutting a channel | Section 6 | [attribution-choice.md](references/attribution-choice.md) |
| Site engagement, checkout drop-off, bounce, conversion by site type | Section 7 | [site-funnel.md](references/site-funnel.md) |

Basic test validity (sample ratio, power, novelty, Simpson's paradox,
holdout maths) lives in the `evidence-check` skill; metric formulas and grain
in `metric-definitions`. Use them; do not repeat them here.

## 2. Paid search: does the next click pay

Per campaign (never only the account):

```
CVR = conversions / clicks          CPC = cost / clicks
Margin per conversion = AOV x gross margin (or the user's figure)
Break-even CPC = margin per conversion x CVR
Profit = conversions x margin per conversion - cost
```

| Pattern | Reading | Action |
|---|---|---|
| CPC < break-even, IS lost to budget high | Profitable and capped | Add budget here first |
| CPC > break-even, IS lost to budget high | Losing money and capped | Do not add budget; lower bids, fix CVR or landing page, or pause |
| IS lost to rank high, low Quality Score | Quality problem | Fix ad relevance, expected CTR, landing page; raising bids buys rank at a higher CPC |
| High impressions, low CTR | Ad not attractive | Copy, extensions, targeting |
| High CTR, low CVR | Click wasted | Landing page, offer, audience match |

- ROAS above 1 is not profit: compare ROAS with 1 / gross margin (at 40%
  margin, ROAS must exceed 2.5 to break even before other costs).
- Ad Rank = bid x Quality Score; actual CPC = Ad Rank of the advertiser below
  / your QS + 0.01. QS 10 cuts CPC about 50%, QS 1 raises it about 400%.
- Brand campaigns look best on every metric; their incrementality is unknown
  until tested (pause test in `evidence-check`).

## 3. Display, video and ad lift tests

- Judge display on viewable impressions, view-through conversions and lift,
  not CTR (about 0.46% display vs 3.17% search is normal).
- Lift = (CVR_treatment - CVR_control) / CVR_control, user-level CVR over an
  impression-based window. Incremental conversions = treatment conversions -
  CVR_control x treatment users. Incremental profit = margin x incremental
  conversions. POAS = (incremental profit - ad cost) / ad cost.
- Inference needs n x p >= 5 and n x (1 - p) >= 5 in each group; balance
  checks on pre-exposure variables should give p > 0.05.
- **Segments:** a pivot of lift by day, device, new vs returning or exposure
  band is descriptive. Before cutting or shifting spend on a segment
  difference, test it: logistic regression with treatment x segment
  interaction; only a significant interaction proves the effect differs.
  Compare segments on lift %, not raw point gaps. Frequency usually shows an
  inverted U: too few and too many exposures both lose.

## 4. Influencers: profit per post, by tier

```
Engagement rate = engagements / followers x 100
CPA = fee / attributed orders
Profit per post = orders x margin per order - fee
POAS = profit / fee
```

- Group by platform x follower tier (nano < 10K, micro 10K-100K, macro
  100K-1M, mega > 1M) x code / no code. Rank groups by POAS and profit per
  post, never by orders per post: big creators bring more orders and can
  still lose money per post.
- Fees differ sharply by platform for the same follower count; compare
  per-post cost before comparing outcomes.
- Discount codes tend to lift orders most for small creators; check the code
  effect inside each tier (an interaction, not one average).
- Follower count and engagement rate move in opposite directions; do not put
  both, or post cost, into one regression as drivers.
- Orders tracked by code or link are attributed, not incremental; audit
  audience quality (suspicious followers) before rebooking.

## 5. Search visibility (SEO, local, AI answers)

Keyword focus, per keyword, in this order:
1. Intent matches a funnel stage you need (awareness, consideration, action).
2. Current rank 4-20: the zone where effort moves traffic. Rank 1-3:
   maintain. Rank 50+ or unranked on high-difficulty terms: not this quarter
   (long-tail versions instead).
3. Competition you can beat (difficulty vs your authority; who holds the top
   results).
4. Volume, as the tie-breaker among interchangeable terms.
5. One keyword, one URL. Two of your URLs ranking for one keyword is
   cannibalization: consolidate onto the page that should own it.

Top three organic positions take about two thirds of clicks; rank gains
inside page one matter more than gains on page five. Backlinks, local and
AI-answer checks are in the reference.

## 6. Attribution: credit is not cause

- Rule-based models see only converting paths. Data-driven attribution (GA4
  default) uses converting and non-converting paths but needs about 400
  conversions per key event in 30 days (plus enough multi-touch paths);
  below that GA4 silently falls back to last click. **Identical last-click
  and DDA numbers usually mean the fallback, not agreement.**
- Custom models need more: Markov about 2,000, Shapley about 5,000, full ML
  about 10,000 conversions a month.
- First- and last-click columns must each sum to total conversions or value.
  Google models exclude direct visits unless the whole path is direct.
- Before cutting a channel on credit, run a holdout or geo test; attribution
  divides credit, only an experiment shows what the channel caused.

## 7. On-site funnel

- Engaged session: over 10 seconds, or 2+ page views, or a key event. GA4
  bounce rate = share of sessions not engaged.
- Purchase CVR = purchases / sessions. Define the conversion by site type
  (purchase, lead, pageviews for ad-funded media, subscription).
- Cart abandonment benchmark about 70% (60% is very good). Read step by step
  (product view, add to cart, checkout, shipping, payment, purchase); fix the
  biggest step drop first and name its likely cause (hidden costs, forced
  account, long forms, missing payment method, trust).

## 8. Adversary for every move

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Frame the decision | Which decision, which conversion, which margin? | Decision restated; primary conversion and margin confirmed or asked | Ask; do not assume revenue is profit |
| Compute campaign economics | Is the account average hiding losers? | Break-even CPC and profit per campaign; totals recomputed two ways | Re-cut by campaign |
| Recommend budget or bids | Is the constraint budget or rank, and is the click profitable? | IS lost to budget vs rank, QS, CPC vs break-even | Move money only to profitable, budget-capped campaigns |
| Read an ad test | Is this lift or targeting? Is the segment gap real? | Randomised control, n x p >= 5, balance p > 0.05, interaction test | Label segment findings as hypotheses |
| Rank creators | Are we ranking by volume instead of profit? | POAS and profit per post by platform x tier x code | Re-rank by profit |
| Pick keywords | Can we move these, and do they compete with each other? | Rank band 4-20, intent, difficulty, one URL per keyword | Drop or consolidate |
| Read attribution | Did DDA actually run, and is credit being read as cause? | Monthly conversions per key event vs 400; columns sum to total | Say the comparison is uninformative; propose a holdout |
| Name the cause | What else produces the same pattern? | Data ruling out each rival (mix, season, tracking change) | Call it a hypothesis |
| Recommend | What does it cost if wrong, and what would the CFO ask? | Money at risk; the test or metric that confirms within weeks | Shrink the change; add a test |

## 9. Score-and-probe gate before handover

1. Every row in section 8 passes, or the answer says which could not and why.
2. Score the draft 0-100 on **clarity**, **relevance** (answers the decision
   asked), **depth** (per-unit numbers behind each claim) and
   **insightfulness** (what the account-level view hid).
3. Below 80 on any: write the probe question that would raise it, answer it
   from the data, revise, re-score. At most 2 loops; then hand over and note
   what stayed below 80.

## 10. Output

```
Verdict: <one line per unit: scale | hold | fix | cut | test first>
Number: <break-even vs actual CPC, POAS, lift with p, rank band, conversions vs 400>
Action: <specific change, sized in money or volume>
Verify: <metric and date, or the experiment that confirms it>
Caveats: <attribution limits, data gaps, what the user decides>
```

Show the per-unit table the verdict rests on.
