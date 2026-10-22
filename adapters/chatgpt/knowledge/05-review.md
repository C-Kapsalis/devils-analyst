# Skill: review

---
name: review
description: >-
  Use this skill when someone hands over a marketing report, deck, dashboard, analysis
  or agency write-up that someone else made and wants it checked: "review this
  report", "review this dashboard", "review this deck", "can you check this before I
  send it to my boss", "is this right", "check my numbers", "sanity check this", "does
  this hold up", "what's wrong with this analysis", "would you sign off on this", "the
  agency sent us this, is it fair". Works on markdown, HTML, a pasted deck, a
  screenshot description or a spreadsheet, with or without the data behind it. It
  recomputes every number it can, checks definitions, charts, comparisons, causal
  claims and recommendations, leaves correct things alone, and returns a verdict plus
  findings ranked Must fix, Should fix, Nice to have. Auditing a whole account or
  setup: use audit. Building a new report: use marketing-dashboard. Email copy itself
  is out of scope.
---

# review

The chart can be right and the conclusion wrong. A review finds the places
where a reader would decide something different if the report were correct,
proves each one with a number, and leaves everything else alone. A review
that flags correct things, or pads the list, teaches the reader to ignore it.

**The human owns the question and the decision.** Before reviewing, write one
line: "After reading this, [who] will [decide what]." If the report does not
say who reads it or what they will decide, assume the obvious reader (the
boss, the client) and say so in one line. Do not stop to ask unless the
decision is truly unclear.

## 1. Build the claim ledger

Read the whole artefact once. List every claim that a decision could rest on,
in a scratch table (do not print it):

| # | Claim as written | Type | Can I check it? |
|---|---|---|---|
| 1 | "Blended ROAS 5.2x" | number | yes: spend and revenue in the CSVs |
| 2 | "The new creative drove the lift" | cause | partly: is there a control? |
| 3 | "Cut display" | action | yes: what it is judged on |

Types: **number** (a value or a total), **definition** (what a metric
means), **comparison** (up, down, best, worst), **chart** (what a visual
implies), **cause** (drove, caused, because), **action** (cut, scale, keep).
Headline and summary claims first: they carry the decision.

If data files come with the report, map each file to the claims it can test
(columns, grain, date range, which platform). If no data comes with it, check
internal consistency only (totals that should sum, rates that should match
their parts, text that contradicts a table) and say so under "Not checked".

## 2. Run the checks, in this order

Stop on each claim at the first check that fails. Details and detection rules
for every item: [references/review-checklist.md](references/review-checklist.md).

| Order | Check | Fails when | Typical recomputation |
|---|---|---|---|
| 1 | **Arithmetic** | a total does not sum, a rate does not match its parts | sum the column; divide the summed parts |
| 2 | **Aggregation** | a ratio is an average of row ratios; distinct counts (users, reach) are summed across days or weeks; a snapshot (list size, subscribers) is summed over time | sum(numerator) / sum(denominator); take the period value, not the sum |
| 3 | **Definition** | "conversions" mix micro actions with purchases; open rate used as engagement; platform revenue used as sales | scope to the action that means money; use the store or analytics total |
| 4 | **Double counting** | channel claims sum above the store total; query-page impressions summed as demand | compare the sum with the single source of truth |
| 5 | **Comparison** | no comparator; unequal periods or ages; last 2-3 days of a lagging source read as a drop; a filtered "% of total" | same-length prior period, same window last year, same accrual age |
| 6 | **Blend** | one rate across groups that behave differently (brand and generic, mobile and desktop, one giant send and small ones) | split rows; compare within each group |
| 7 | **Chart** | the visual implies something the numbers do not | see [references/chart-checks.md](references/chart-checks.md) |
| 8 | **Cause** | drove, caused, thanks to, because, with no control, holdout or test | name the rival explanation the data cannot rule out |
| 9 | **Significance** | "significant" with no test or n; a costed change tested against zero instead of its break-even; a segment winner from a pivot table | compute it, or call it a hypothesis |
| 10 | **Action** | the recommendation does not follow from the corrected numbers, or has no number to watch and no way to verify | redo the decision on the corrected numbers |

Metric formulas and platform quirks live in the `metric-definitions` skill
(catalog and source traps); causal tests (holdouts, SRM, power, novelty,
Simpson's paradox, pull-forward) in `evidence-check`; period-over-period
decomposition in `whats-changed`. Use them for the recomputation. Do not
repeat their content in the review.

## 3. Prove it or drop it

A finding needs a concrete case: "this cell says X; the data gives Y; here is
the arithmetic". Before keeping any finding:

1. **Recompute it.** Show the numbers that disagree, from the report or the
   data, in one line ("CTR printed 6.1% is the mean of row CTRs; 4,210 clicks
   / 118,400 impressions = 3.6%").
2. **Check the decoy list.** Many things look wrong and are fine:
   [references/decoys.md](references/decoys.md). Examples: Search Console clicks
   above GA4 sessions, display CTR near 0.4%, brand campaigns with 30-50% CTR,
   sessions slightly under email clicks on every row, rounding gaps under 1%,
   a median that differs from the mean when the report says which it uses.
3. **Check the report did not already handle it.** A caveat, a footnote, or a
   split table elsewhere in the report can answer the point. Read it before
   flagging.
4. **Ask "would the reader decide differently?"** If no, it is Nice to have
   at most. If it is only taste (fonts, wording you would phrase differently),
   drop it.

No number, no finding. No "consider", no "might want to", no vague worry.

## 4. Rank

| Group | Put here when | Examples |
|---|---|---|
| **Must fix** | a headline or decision number is wrong; a definition error changes the answer; the recommendation points money the wrong way; a chart reverses the reading | stacked platform revenue as ROAS; CPA on newsletter sign-ups; "organic crashed" from the lag days; ship decision tested against zero instead of break-even |
| **Should fix** | the direction holds but the number is off; a causal claim with no test; a missing comparison; an action with no way to verify; a chart that exaggerates without reversing | averaged CTR in a side table; "the new creative drove it"; no prior period; display judged on CTR |
| **Nice to have** | labels, a missing denominator the reader can infer, chart type choices | 9-slice pie; unlabelled moving-average window |

Within a group, order by the money or the decision at stake: the finding that
moves the most budget or revenue goes first. Number findings across all
groups so the reader can say "fix 1 and 3".

## 5. Write the review

Plain English, short sentences, the reader may not be an analyst. Define a
term the first time (CTOR, ROAS). No emojis, no em-dashes.

```
Verdict: [Send it. | Fix 1 and 2 before sending. | Do not send: the main conclusion is wrong.]

What this report says: [two sentences: its main claim and its recommendation]
Who decides what: [one line, from the ledger]

## Must fix
1. **[Short name of the problem]** ([where: slide 3, tile "ROAS", table 2 row "Meta"])
   - **What it says:** [the claim, quoted or paraphrased, with its number]
   - **What is wrong:** [the recomputation or the rule, with the right number]
   - **Fix:** [the corrected number or wording, ready to paste]
   - **If you skip it:** [the decision or money at stake, in one sentence]

## Should fix
...
## Nice to have
...

Checked and fine: [one line: the main numbers or claims you verified and that hold]
Not checked: [one line: what you could not test and why]
```

- Skip empty groups. Keep at most 10 findings; if you left smaller ones out,
  say how many.
- "If you skip it" names the consequence in money or in the decision: "the
  team scales a campaign that loses 0.40 on every click", not "accuracy
  suffers".
- The fix is concrete: the corrected figure, the replacement sentence, or the
  chart change. Not "clarify".
- When the report is correct: `Verdict: Send it.`, then "What this report
  says", then "Checked and fine" listing what you verified. Add a Nice to have
  only if it is real. Do not invent problems to look thorough.

A worked example of one finding, and of a clean verdict:
[references/finding-examples.md](references/finding-examples.md).

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check,
and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Build the ledger | "Did I skip the claims in the summary, the chart titles or the footnotes?" | every headline, chart title and recommendation has a ledger row | add the rows, re-run section 2 on them |
| Recompute a number | "Am I computing at the same grain, period and filter as the report?" | match one number the report got right before calling another wrong | align the scope, recompute |
| Flag a definition | "Is the report's definition a stated, defensible choice?" | the report's own notes and the metric-definitions catalog | drop it, or downgrade to Nice to have |
| Flag a cause | "What else produces the same pattern?" | name the rival (season, spend change, mix, selection) and whether the data rules it out | if the data rules it out, drop the finding |
| Keep a finding | "Is this a decoy?" | the decoy list and the report's own caveats | drop it |
| Rank | "Which finding would change the decision most if fixed?" | money or decision at stake per finding | reorder |
| Give the verdict | "Would I send this report to the boss with my fixes applied?" | the Must fix list is empty or the verdict says what to fix first | rewrite the verdict |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision
belong to the person asking: when either is unclear, ask instead of assuming.

---

## File: review/references/chart-checks.md

# Chart checks

A chart is wrong when a reader looking at it for five seconds would believe
something the numbers do not support. Flag the chart, say what a reader
believes, and give the number that corrects it.

| # | Flaw | Spot it | What the reader wrongly believes | Fix | Default |
|---|---|---|---|---|---|
| 1 | Truncated bar axis | Bar axis starts above zero (e.g. at 80,000) | A 6% gap looks like a doubling | Bars start at zero; put the % gap in the label | Must if the text repeats the exaggeration, else Should |
| 2 | Dual axes that mislead | Two y-axes scaled so lines cross at a "turning point" | A relation or crossover that is an artefact of scaling | One axis, or indexed lines (start = 100); two axes only when the relation is the point, both labelled in series colours | Should |
| 3 | Pie with many slices | More than 5 slices, legend instead of labels | Nothing precise; slices cannot be compared | Sorted bars with share labels, or a treemap with at most 10 tiles | Nice |
| 4 | Rate without volume | KPI tile shows a rate and a change, no count ("CVR 9.8%, +3.1 pts" from 41 sessions) | A big win where the base is too small to read | Show the count behind every rate; grey out tiles under a minimum volume | Should (Must if it drives a budget move) |
| 5 | Cumulative line hiding a decline | Year-to-date or month-to-date line still climbing while each recent period fell | "Still growing" | Per-period bars next to the running total | Must if the headline says growth |
| 6 | Rainbow palette for ordered data | Retention or heat table coloured red, yellow, green, blue | False boundaries between values | Sequential single-hue scale | Nice |
| 7 | Diverging scale off-centre | Week-over-week change on a sequential scale, or a diverging scale whose neutral sits away from zero | Small declines look neutral or positive | Diverging scale centred on zero (or on plan) | Should |
| 8 | Smoothing that hides a step | Moving average with no window stated; a tracking break turned into a gentle slope | A gradual trend where there was a break | State the window; show the raw series around breaks | Should |
| 9 | Mean on skewed data | "Average order value" pulled up by a few very large orders | A typical order that does not exist | Median for skewed measures, say which | Must if it sets a price, threshold or target |
| 10 | Filtered percent of total | "Google Ads is 62% of revenue" with a Paid filter on | The channel's share of the business | Label the denominator; recompute on the full total | Should |
| 11 | Extrapolated trend line | Solid fit line running past the last data point | A forecast nobody made | Stop fits at the last observed point; forecasts dashed and labelled | Should |
| 12 | Bubble sized by radius | Bubble radius proportional to spend | Twice the spend looks four times bigger | Size by area, or use bars | Nice |
| 13 | Topic title | Title names a topic ("Email performance"), not the answer | Nothing; the reader must work out the point | Title states the answer with its number | Nice |
| 14 | Inconsistent colours | The same channel in different colours on different charts | Wrong series compared | One colour per channel everywhere | Nice |
| 15 | Map on pooled data | Every region shows the same rate, or regions inferred from account names | Regional differences that are not in the data | Sorted bars on regions with real data; drop the map | Should |

How to check from a description or HTML: read the axis minimum, the scale
type, the filter state, the n behind each rate, and whether lines extend past
the data. If a chart is only described in words and the description omits
the axis or filter, say so under "Not checked" instead of guessing.

---

## File: review/references/decoys.md

# Decoys: things that look wrong and are fine

Flagging a correct item costs the review its credibility. Before keeping a
finding, check it is not one of these. If the report states the item
correctly, list it under "Checked and fine" instead.

| Looks wrong | Why it is fine | Flag only if |
|---|---|---|
| Search Console clicks higher than GA4 organic sessions | Different systems: Google counts the click, analytics counts a consented, tagged session | the report subtracts one from the other as "lost traffic" |
| Ad platform clicks a few percent above analytics sessions | Same reason: blockers, consent, bounces before the tag fires | the gap is over about 25% or changed suddenly |
| Sessions slightly under email clicks on every row | Normal; some clicks never load the page or are scanner clicks | a send has clicks and zero sessions (broken tagging) |
| Display CTR around 0.3-0.6% | Normal for display; it is a reach channel | display is judged or cut on CTR |
| Brand search CTR of 30-50% and the lowest CPA | Normal for brand terms | brand is blended into the account CTR or CPA, or called fully incremental |
| Phrase or exact match with the highest CPC | Precise matches cost more per click | cost per sale is also worst |
| Retargeting ROAS far above prospecting | Expected: it closes demand others created | budget is moved from prospecting on that basis |
| Direct traffic around 10-25% and stable | Bookmarks, typed URLs, apps | a sudden spike lines up with untagged campaigns |
| Direct credit identical under every attribution model | GA4 models give direct credit only when the whole path is direct | the report calls it "robust" as evidence |
| A median order value well below the mean | Expected with a few large orders; the median is the right typical value | the report quotes the mean as typical and acts on it |
| Rounding differences under 1% | Rounding | the rounded figure flips a ranking or a threshold |
| Open rate shown as a trend with a privacy caveat | Correct use of opens | opens rank campaigns or are the verdict |
| A rate computed as sum / sum that differs from the average of the row rates | The report did it right; the row average is the wrong one | never |
| A smaller period total than last period when the period is shorter | Check per-day values | per-day values also fall and the report denies it |
| Unsubscribe rate 0.1-0.4% per send | Normal band | above about 0.5% on a send |
| Complaint rate under 0.1% on every send | Normal | one send is above 0.1%, hidden in an average |
| A CTOR of 8-15% | Normal band | the report ranks sends on it with tiny opens |
| Sample split of 49.9 / 50.1 in a 50/50 test | Within chance; check with chi-square | the chi-square statistic is above 10.8 (p < 0.001) |
| Position quoted as an impression-weighted average | Correct | the average is unweighted |
| Last-click and data-driven columns that differ | Expected when DDA is active and has volume | they are identical while DDA is claimed |
| A forecast drawn dashed and labelled beyond the data | Correct | the line is solid or unlabelled |

Rule of thumb: a decoy is a pattern that has a normal, known cause. Flag it
only when the report draws a wrong conclusion from it, and then the finding is
about the conclusion, not the pattern.

---

## File: review/references/finding-examples.md

# Finding examples

Synthetic examples. They show the shape and the level of proof each finding
needs.

## One Must fix finding

```
1. **Total ROAS counts the same sales twice** (summary, "Blended ROAS 5.4x")
   - **What it says:** Paid media returned 5.4x: Google 61,200 plus Meta
     48,900 in revenue on 20,400 of spend.
   - **What is wrong:** Google and Meta each report sales they touched, on
     their own windows, so the same order is often claimed by both. Their sum
     (110,100) is above the store's total revenue for the month (84,300),
     which includes organic and email. Against the store total, all revenue
     on paid spend is at most 84,300 / 20,400 = 4.1x, and the paid share is
     lower still.
   - **Fix:** Replace the line with "Store revenue 84,300 on 20,400 paid
     spend (4.1x, all channels). Platform claims: Google 61,200, Meta 48,900;
     they overlap." Judge each channel against the store or analytics total,
     not its own claim.
   - **If you skip it:** The plan to raise paid budget by 30% rests on a
     return that does not exist; at 4.1x or lower the extra spend may not pay
     back at the 35% margin.
```

What makes it a good finding: the claim is quoted with its number, the
recomputation uses figures the reader can find, the fix is ready to paste,
and the cost is a decision, not "accuracy".

## A finding that should be dropped

"The report uses a pie chart for device split." There are three slices, all
labelled with percentages, and nobody decides anything from it. Not a
finding.

"Search Console shows 12,400 clicks but GA4 shows 10,900 organic sessions,
so 1,500 visits are missing." The report itself says the two will not match.
Decoy; list it under "Checked and fine" if at all.

## A clean verdict

```
Verdict: Send it.

What this report says: Paid search CPA on purchases fell from 41.20 to 38.90
in September while spend held at 18,000; the report credits lower generic
CPCs and recommends keeping budgets flat.
Who decides what: the marketing lead decides whether to keep budgets flat.

Checked and fine: totals and every CPA and CTR recompute from the export
(ratio of sums); conversions are scoped to purchases; brand and generic are
split; September is compared with August per day and with September last
year; the CPC claim matches the auction data; the recommendation names the
number to watch (generic CPA under 45) and when (mid-October).
Not checked: revenue against the store total (no store export provided).
```

No padding: a clean report gets a short review.

---

## File: review/references/review-checklist.md

# Review checklist

Each row: the claim that is often wrong, how to spot it from the report (and
the data, if given), the fix, and the usual severity. Ordered by how often
it changes the decision. Severity is a default: raise it when the claim sits
in the headline or drives the recommendation, lower it when it sits in a side
table nobody acts on.

## A. Numbers and aggregation

| # | Claim that is often wrong | Spot it | Fix | Default |
|---|---|---|---|---|
| A1 | A ratio rolled up as the average of row ratios (CTR, CVR, CPC, CPA, ROAS, CTOR, open rate) | Recompute sum(numerator) / sum(denominator) from the table; it differs from the printed total | Print the ratio of sums at every grain | Must if headline, else Should |
| A2 | Monthly users or reach built by adding daily or weekly values | Monthly figure equals the sum of the days or weeks; reach above impressions on a row; reach above the audience that exists | Take the period's distinct count from the source; never sum distinct counts | Must if used for CPM, frequency or CAC |
| A3 | A snapshot summed over time (list size, subscribers, open pipeline, stock) | "Total subscribers" far above the latest list size; a balance column added across months | Use the end-of-period (or average) value | Must |
| A4 | Totals that do not add | Rows do not sum to the total row; percentages do not sum to about 100% | Recompute; find the missing or duplicated row | Must if the total is quoted |
| A5 | Spend joined to orders row by row before dividing (CAC, CPA) | CAC far above spend / customers computed from totals | Aggregate each fact separately, then divide | Must |
| A6 | Unweighted average position or Quality Score | Simple mean of rows; tiny rows weigh like flagship rows | Impression-weighted mean | Should (Must if it picks the page to fix) |
| A7 | Percent change on a tiny base | "+300%" from 3 to 12; a rate tile with no volume | Show the counts; say the base is too small to read | Should |

## B. Definitions

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| B1 | "Conversions" that are not sales | No conversion-action label; CPA implausibly low; conversions far above orders | Scope CPA, CVR and ROAS to the action that means money | Must |
| B2 | Platform revenue added across platforms | Channel revenue sums above the store or analytics total; "total ROAS" built from platform claims | One shared revenue number (store or analytics) against total spend; platform figures labelled as platform claims | Must |
| B3 | Open rate as the email verdict | Open rate is the headline KPI or ranks campaigns | Judge on clicks and revenue; opens as a trend only, with the privacy caveat | Should |
| B4 | Revenue ROAS where margins differ | Products or channels ranked on ROAS with different margins | Rank on profit after cost of goods, or ROAS against 1 / margin | Must if it moves budget |
| B5 | A share with no denominator | "62% of revenue", "25% market share" with a filter on or a served market | Name the denominator; recompute on the unfiltered total | Should |
| B6 | A trend that crosses a definition change | Step change on the day a key event, tracking setup, survey wording or analytics platform changed | Break the series at the change; compare like with like | Must if a win is claimed from the step |
| B7 | Users read as people | "We reached 80,000 people" from analytics users | Say browsers or devices | Nice |
| B8 | Industry figures quoted as the company's own | "$36 per $1 email ROI", "5% retention = 25-95% profit" as a forecast | Replace with the company's own attributed number, or label as an outside benchmark | Should |

## C. Comparisons

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| C1 | A number with no comparator | No prior period, target, control or last year on the tile | Add the same-length prior period and same period last year | Should |
| C2 | Unequal windows | 31 vs 30 days compared on totals; a campaign sent yesterday ranked against month-old ones on lifetime totals | Per-day values; same accrual age | Should (Must if it ranks campaigns) |
| C3 | Search Console "crash" in the last 2-3 days | The drop sits only in the final days | Exclude the lag window; compare same weekdays | Must if it triggers action |
| C4 | GSC clicks minus GA4 sessions as "lost traffic" | A reconciliation line between two systems | Read each against itself over time | Should |
| C5 | A blended rate across groups that behave differently | One CTR or CVR for brand and generic, brand and non-brand organic, mobile and desktop, one giant send and many small ones | Split rows; judge each group | Must if the blend hides a loss |
| C6 | Seasonality read as trend | Month-over-month across a peak; moving average window not equal to the cycle | Same period last year; window equal to the cycle | Should |
| C7 | Top by clicks crowned | Campaigns, pages or sends ranked on clicks or sessions; revenue column contradicts | Rank by revenue or profit, and revenue per buyer | Must if it decides what to repeat |

## D. Causal claims and tests

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| D1 | Attribution credit stated as cause | "Meta drove 40k", "SEO generated" with no holdout, lift study or model named | "Meta was credited with 40k under [model]"; propose a holdout if the decision depends on it | Should (Must if it moves budget) |
| D2 | Exposed vs unexposed as ad effect | "Viewers converted 4.8% vs 1.9% for non-viewers" | Platforms aim at likely buyers; only a randomized control shows the effect | Must if it moves budget |
| D3 | Before/after with no control | "Since the redesign, CVR is up 12%" | Name the rival (season, spend, mix, promo); difference in differences or a test | Should |
| D4 | Significance claimed with no test, or against zero when the change has a cost | "Significant" with no n or p; a lift tested against 0 when the change costs money | Test against the break-even lift | Must if it decides a launch |
| D5 | Test too short or uneven | Under 7 days or partial weeks; arms far from the planned split | Run whole weeks; check sample ratio before reading | Must if it decides a launch |
| D6 | Segment winner from a pivot table | "Works on mobile, not desktop" with no interaction test and thin cells | Call it a hypothesis; test the interaction or rerun | Should |
| D7 | Lift as raw points only | "+0.4 points" with no relative lift and no incremental count | Lift = (T - C) / C; incremental = T conversions - C rate x T users | Nice (Should if it sizes the payoff) |
| D8 | Regression to the mean as a win | Worst units last month fixed and their rebound claimed | Compare with equally bad untouched units | Should |
| D9 | Promo lift = promo-week revenue | No baseline, no dip after, no discount cost | Net incremental after pull-forward and discount | Must if "run it again" depends on it |
| D10 | Last-click ROAS used to cut upper funnel | Display or video ROAS lowest, cut recommended | Treat last click as a floor; test before cutting | Should |
| D11 | Survey or AI-panel finding as customer truth | Low or missing response rate; synthetic respondents with no human check | State the response rate; label as directional | Should |
| D12 | GA4 data-driven attribution quoted on low volume | DDA column identical to last click; a key event with a few hundred conversions a month | Say the model in effect is last click | Must if it moves budget |

## E. Actions

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| E1 | The recommendation does not follow from the corrected numbers | Redo the decision after fixing A-D | Rewrite it on the corrected numbers | Must |
| E2 | An action with no way to verify | No number it should move, no date, no place to check | Add: the metric, the expected direction and size, when and where to check | Should |
| E3 | Display or video judged on CTR or last click | Display "underperforms" at 0.3-0.5% CTR | Judge on reach, viewable impressions, cost per thousand and a holdout | Should |
| E4 | Budget raised where the limit is rank, not budget | "Add budget" while impression share lost to rank dominates | Fix quality or bids first; budget goes where lost-to-budget is high and CPA beats target | Must if it moves budget |
| E5 | Cheap CPC celebrated with no ceiling | No break-even line (margin per sale x CVR) | Compare CPC with the break-even CPC | Should (Must if it scales a losing line) |
| E6 | Universal red/amber/green thresholds | Hard-coded "danger" values with no owner or reason | Owner sets thresholds with a written reason | Nice |
| E7 | A subject-line or creative test recommended while the upstream step is broken | Delivery under 95%, complaints over 0.1%, or tracking broken | Fix the upstream step first | Must |

## F. The "why" section

| # | Claim | Spot it | Fix | Default |
|---|---|---|---|---|
| F1 | "Why" written as prose, not computed | No driver bridge or mix vs rate table that sums to the change | Compute the bridge (`whats-changed`) | Should |
| F2 | Parts that do not reconcile | Contributions do not sum to the total change | Recompute | Must if quoted |
| F3 | Mix shift read as performance | A rate moved because the audience mix changed | Within-segment rates at a common mix | Should |
