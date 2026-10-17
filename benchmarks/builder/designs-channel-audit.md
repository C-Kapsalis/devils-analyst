# channel-audit: eval case designs

Format follows benchmarks/cases/*/ (prompt.md with frontmatter,
scaffold writing resources/*.csv, llm graders with PASS/FAIL, plus a
`tool_used` grader). Every case: `max_turns: 40`, `timeout_seconds: 900`,
`allowed_tools: [Read, Glob, Grep, Skill, Write]`, report.md in the working
directory. Generators and fixtures are in `eval-data/`.

Skill-fired grader for all cases:
`input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(channel-audit|evidence-check|diagnose|metric-definitions)"'`

Existing repo evals already cover attribution-model flips on paths,
retargeting holdouts, brand-search pauses and Simpson's paradox; these cases
target different traps.

---

## 1. search-breakeven-cpc

**Prompt.** "We're Northpeak Outdoor. Google Ads says we're losing a lot of
impression share. resources/google_ads_campaigns_sep.csv has September by
campaign and resources/business.csv has our order economics. Should we raise
budgets and bids next month, and where? report.md with numbers please."

**Data.** `google_ads_campaigns_sep.csv` (one row per campaign): `campaign,
clicks, cost, conversions, conv_value, search_impr_share,
search_lost_is_budget, search_lost_is_rank, avg_quality_score`.
`business.csv`: `aov 125, gross_margin 0.40`. Generator: `eval-data/c1.py`.

| Campaign | Clicks | Cost | Conv | IS | Lost budget | Lost rank | QS |
|---|---|---|---|---|---|---|---|
| Brand | 4,200 | 1,680 | 504 | 0.92 | 0.00 | 0.05 | 9 |
| Generic - Running Shoes | 18,000 | 37,800 | 900 | 0.48 | 0.35 | 0.17 | 7 |
| Generic - Trail Gear | 14,000 | 44,800 | 560 | 0.52 | 0.30 | 0.18 | 6 |
| Competitor Terms | 6,000 | 16,800 | 150 | 0.12 | 0.06 | 0.82 | 3 |

**Ground truth.** Margin per order $50. Break-even CPC = 50 x CVR.
- Brand: CPC $0.40 vs BE $6.00, profit +$23.5K, no budget constraint
  (incrementality untested).
- Running Shoes: CPC $2.10 vs BE $2.50, profit +$7.2K, 35% lost to budget:
  the only campaign where more budget is profitable.
- Trail Gear: CPC $3.20 vs BE $2.00, profit -$16.8K (ROAS 1.56 looks fine
  but is below the 2.5 break-even ROAS): losing 30% to budget, yet more
  budget loses more; cut bids or fix CVR.
- Competitor: CPC $2.80 vs BE $1.25, profit -$9.3K, 82% lost to rank with QS
  3: raising bids buys rank at a loss; fix quality or pause.
- Account: CPA $47.8 < $50 margin, ROAS 2.61, profit only +$4.6K, almost all
  from Brand.

**Naive answers.** "Account CPA is under margin and ROAS is 2.6, so raise
budgets and bids across the board"; or "Trail Gear ROAS 1.56 > 1, scale it".

**Graders.**
- `per-campaign.md` (weight 3): PASS if report.md judges each campaign
  against a margin-based break-even (break-even CPC, profit or POAS) and
  identifies Trail Gear and Competitor Terms as unprofitable (CPC above about
  $2.00 and $1.25 break-even, or negative profit about -$16.8K and -$9.3K).
  FAIL if it recommends raising budget or bids for Trail Gear or Competitor
  Terms, or judges profitability on ROAS > 1.
- `where.md` (weight 2): PASS if the budget increase is directed to Generic -
  Running Shoes (profitable and budget-limited) and the Competitor campaign's
  rank loss is tied to low Quality Score rather than fixed by higher bids.
  FAIL if increases are spread across all campaigns.

---

## 2. influencer-tier-profit

**Prompt.** "We paid 240 creators last quarter (resources/creator_posts.csv).
Big creators clearly drive the most orders. Our margin per order is $22.
Should we move next quarter's influencer budget toward bigger creators?
Answer in report.md."

**Data.** `creator_posts.csv`, 240 rows: `creator_id, platform (TikTok /
Instagram), followers, promo_code (0/1), fee_usd, orders`. Instagram fees
about 4x TikTok per 1,000 followers. Generator: `eval-data/c2.py` (seed 21).

**Ground truth (profit per post = 22 x orders - fee).**

| Tier | Orders/post | Fee/post | Profit/post | POAS |
|---|---|---|---|---|
| Nano (< 10K) | 9.6 | $74 | +$138 | 1.86 |
| Micro (10-100K) | 22.8 | $368 | +$134 | 0.36 |
| Macro (100K+) | 47.0 | $1,860 | -$826 | -0.44 |

Best cells: nano TikTok with code (POAS 4.14), micro TikTok with code (profit
$417 per post, POAS 2.38). Instagram macro loses about $2,100-2,300 per post;
Instagram micro without code loses $131. Program overall -$113 per post.
Bigger creators bring about 5x the orders of nano creators and lose money.

**Naive answer.** "Macro creators average 47 orders per post vs 10 for nano;
shift budget to bigger creators."

**Graders.**
- `profit.md` (weight 3): PASS if report.md computes profit or POAS per post
  by follower tier (and/or platform) and shows macro creators lose money
  (negative profit per post, about -$800 average) while nano and micro are
  profitable. FAIL if it recommends shifting budget to bigger creators, or
  ranks creators by orders without fees and margin.
- `where.md` (weight 2): PASS if the recommendation concentrates on TikTok
  nano/micro creators (with codes) and cuts or renegotiates Instagram macro
  posts. FAIL otherwise.

---

## 3. seo-keyword-focus

**Prompt.** "resources/keyword_rankings.csv is our Semrush export for
northpeak.com (domain authority 34). We have one content person this quarter.
Which keywords should our SEO work focus on? Pick up to 8 and say what to do
for each in report.md."

**Data.** `eval-data/c3_keywords.csv`, 20 rows: `keyword, monthly_volume,
current_rank, ranking_url, intent, keyword_difficulty`. "waterproof trail
running shoes" appears twice (category page rank 14, blog post rank 19).

**Ground truth.** Ranked by volume, 8 of the top 10 are wrong targets: rank 50+
on difficulty 62-91 (running shoes, trail running shoes, marathon training
plan, running socks), already top 3 (brand terms, how to start trail
running), or rank 41. The focus set is the rank 4-20 terms: trail running vest
(9), best trail running shoes for beginners (7), waterproof trail running
shoes (14 / 19, cannibalized), trail running shoes wide toe box (11), trail
running shoes sale (6), zero drop trail shoes (5), trail running gaiters (13),
how to clean running shoes (17), trail shoe size guide (4). The waterproof
term needs one owning page (the category page, matching transactional intent)
with the blog re-targeted.

**Naive answer.** Top 8 by volume: running shoes, trail running shoes,
marathon training plan, brand terms, running socks, carbon plate.

**Graders.**
- `bands.md` (weight 3): PASS if at least 6 of the chosen keywords currently
  rank 4-20 and none of running shoes, trail running shoes, marathon training
  plan, running socks, northpeak running, northpeak shoes is chosen as a
  focus keyword. FAIL otherwise.
- `cannibal.md` (weight 2): PASS if report.md notes that two URLs compete for
  "waterproof trail running shoes" and recommends one page own it. FAIL if not
  mentioned.

---

## 4. dda-fallback

**Prompt.** "Our CFO wants to cut paid social, which is a quarter of our
spend. I compared attribution models in GA4 for our lead form and paid social
gets about 3% of leads under both last click and data-driven, so the models
agree. resources/ has the comparison export, monthly leads and spend. Is
cutting paid social the right call? report.md."

**Data.** `ga4_model_comparison.csv`: `channel, key_event (generate_lead),
last_click_key_events, data_driven_key_events` with identical numbers
(Organic Search 214, Direct 188, Paid Search 141, Email 66, Referral 40,
Paid Social 21; total 670 for Jul-Sep). `key_events_by_month.csv`: Jul 231,
Aug 204, Sep 235. `spend_by_channel.csv`: paid search 45%, paid social 25%,
email tools 10%, other 20%.

**Ground truth.** About 223 leads a month, below the roughly 400 per key event
that GA4 data-driven attribution needs, so DDA has almost certainly fallen
back to last click; identical columns are the symptom, not confirmation.
Attribution (any model) is credit, not cause; paid social may start journeys
other channels close. Recommendation: do not cut on this evidence; run a
holdout or geo test (or a staged reduction measured as a test) before
cutting.

**Naive answer.** "Both models agree paid social drives 3% of leads for 25% of
spend; cut it."

**Graders.**
- `fallback.md` (weight 3): PASS if report.md says monthly lead volume (about
  200-235) is below the data-driven threshold (about 400 per month) so GA4
  likely used last click for both columns, making the agreement
  uninformative. FAIL if it treats the matching numbers as two independent
  models agreeing.
- `test.md` (weight 2): PASS if report.md recommends an incrementality test
  (holdout, geo or lift test, or a measured staged reduction) before cutting.
  FAIL if it recommends cutting paid social outright on attribution data.
