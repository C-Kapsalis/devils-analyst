# Concept test: method and interpretation

A concept test asks target customers to react to a product idea before it is
built. Its outputs are a choice between concepts, a list of fixes, and a unit
forecast. It replaces team judgment with customer data, so the data has to be
from the right people, shown the same way, and read without inflating intent.

## Design checks (ask about these before trusting the numbers)

| Element | What good looks like | Why it matters |
|---|---|---|
| Purpose | Written questions: like/dislike, fit to needs, which concept, how to improve, how many units, continue or pivot | Defines which measures are needed |
| Population | Mirrors the target market; screener questions end the survey for non-targets; each served segment sampled | Biased sample, biased forecast |
| Sample size | No formula; 10 for qualitative depth, 50+ for quantitative, up to ~1,000. Larger when late in development, when investment is high, or when few people are expected to value it | Below 50 a few heavy users can swing results |
| Format | Face-to-face for demos and many alternatives; structured online forms when questions are focused; email only to people with an existing relationship | Mode changes response |
| Stimulus | Same level of detail and same tone for every concept; positioning-style concepts predict behaviour better than bare core-idea statements; working prototypes risky (mistaken for the final product) | Words + visual raised intent ~20 points on average over words only; persuasive copy scores higher than factual |
| Price | Usually omit; ask open-ended price expectation instead. Include only if price is unusually high or low, performance needs a high price, or the category has no price reference | Early prices are guesses and steer preference |
| Competition | Show alternatives (and competitor products if possible), ask for choice | Enables share estimates; single concepts in a vacuum inflate intent |
| Scale | 5-point PI in fixed order: definitely, probably, might or might not, probably not, definitely not | The evidence-backed order |

## Four kinds of data to collect

1. Purchase measures: intent, expected frequency, units per purchase.
2. Overall diagnostics: uniqueness, believability, importance of the problem,
   interest, value for money (only if price was shown).
3. Attribute diagnostics: rating of each attribute and its importance.
   **Quadrant analysis**: plot importance against rating; the quadrant of high
   importance and poor rating is where improvement effort goes.
4. Profiling: current behaviour, category perception, switching barriers,
   role in the purchase decision.

## Cleaning sequence

1. Export numeric values (codes) and keep the label export as the codebook.
2. Remove header metadata rows; keep one header row.
3. Delete respondents failing any screener; delete mostly blank rows.
4. Range check every PI column; ranks must be unique and complete per person;
   remove implausible price expectations or fix obvious typos.
5. Report n before and after each step.

## Analysis

Summary table per concept: mean PI (2 decimals), sample SD, top-box %,
top-two-box %, % ranked first.

Significance:

| Design | Test | Statistic |
|---|---|---|
| Every respondent rated every concept | Paired t-test | `t = mean(d)/(sd(d)/sqrt(n))`, df = n - 1 |
| Each respondent saw one concept | Two-sample t-test | difference in means over pooled or Welch SE |

Run top vs second and top vs third. Report n, means, SDs, t, df, two-tailed p,
the alpha set beforehand, and one plain sentence. Course practice used alpha
0.10; say which you use.

Why pairing matters: respondents differ a lot in how generous they are with
any concept. The paired test removes that person-level spread, so a modest
but consistent preference shows up; the two-sample test leaves it in the
noise.

If metrics disagree (mean favours A, ranked-first favours B), state the
trade-off and choose with qualitative comments and feasibility in view.

## Interpreting the level, not just the ranking

- Benchmarks: own historical tests first, then research-firm databases, then
  published norms. Published: 80-90% favourable (definitely + probably)
  encourages development (experience across 100+ brands); average
  "definitely" about 19% across categories, varying widely by category.
- A concept that wins the set but sits far below the norm needs rework, not
  a go.

## Forecast

`Q = N x A x P`, `P = C_def x F_def + C_prob x F_prob`.

- N from secondary data (potential buyers in the period).
- A = awareness x availability; hard to estimate; tie to the promotion and
  distribution plans.
- Constants: C_def typically 0.4 (0.1-0.5), C_prob 0.2 (0-0.25); category
  specific. P is a probability, not a price.
- Example shape (not from any case): 15% definitely and 25% probably gives
  P = 0.06 + 0.05 = 0.11.

What inflates PI: no real money at stake, wish to please the researcher,
polished stimulus better than the product will be, captive audience, no
competitors shown. What moves real sales away from the forecast: promotion
levels, word of mouth (raises A after launch), product or price differing from
what was tested, competitor response.

Intent predicts trial much better than repeat (in a classic six-product
study, repeat-given-trial barely differed across intent levels). For
nondurables collect purchase frequency and treat volume beyond trial as
unknown until repeat is observed.

Reflect: were key benefits communicated? Is the forecast consistent with
sales of similar products? Run sensitivity on N, A and P.

## When skipping formal testing is defensible

Fast-moving software with a short market window, or testing costs above the
value of the information. Truly novel products are hard for respondents to
judge. Most firms still should test when development cost is high.
