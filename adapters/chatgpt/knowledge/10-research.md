# Skill: research-design

---
name: research-design
description: >-
  Use this skill when a marketer plans, reads or relies on research about customers or
  a market: "should we run a survey or focus groups", "write or review our
  questionnaire", "is this question biased", "how many people do we need to survey",
  "how many responses for a ±3% margin", "can I trust these survey results", "only 10%
  answered our survey", "our survey went to our followers / newsletter list", "what
  share of customers would buy", "would people pay for this", "how aware are people of
  our brand", "measure awareness before and after the campaign", "is this above our
  break-even", "is the difference between these groups real", "which brand has the
  most loyal buyers", "what features matter most", "conjoint", "what is our market
  share". Chooses the design, the instrument, the sample and the inference, and says
  what the data can and cannot support. Whether a test or change worked: use
  evidence-check. Fitting models: use marketing-models.
---

# research-design

Every number a study produces is the truth plus four errors:

```
measured = true value + sampling bias + random sampling error
                      + measurement bias + random measurement error
```

A bigger sample shrinks only the two random terms. Bias (who answered, who
could be reached, how the question was worded) does not shrink with n; only
design removes it. This skill finds which term dominates and fixes or flags
it before any number is used for a decision.

## 0. What the human owns

Problem definition and the choice of design stay with the user; the skill
proposes, the user disposes. Ask, do not assume:

| Ask | Why |
|---|---|
| What decision will this study change, and what is the status quo? | A study that cannot change the decision is not worth running; H0 = status quo |
| What threshold matters (break-even, target)? | Tests are run against K, not against zero |
| Who is the population, and is there a list of it? | Sets the sampling method and whether bias can be measured |
| How precise must the answer be (± what, at what confidence)? | Sets n |

## 1. Classify the request

| The user wants | Go to | Reference |
|---|---|---|
| To know what to ask, or why something happens, questions still vague | Exploratory design | [design.md](references/design.md) |
| How big, how many, who, what share: a snapshot | Descriptive, cross-sectional | [design.md](references/design.md) |
| Change over time, who switches to whom | Descriptive, longitudinal; fixed panel for switching | [design.md](references/design.md) |
| Proof that X causes Y | Causal design: plan here, judge results in evidence-check | [design.md](references/design.md) |
| A questionnaire written or reviewed | Construction, error audit, coding | [questionnaire.md](references/questionnaire.md) |
| A sample planned, sized or allocated | Sampling method and size | [sampling.md](references/sampling.md) |
| Survey results turned into a population number | CI, bias correction, test vs break-even | [sampling.md](references/sampling.md) |
| Awareness, attitude, feature importance, intent, share, loyalty | Measures and their traps | [measures.md](references/measures.md) |

## 2. Check the data or plan

| Check | Threshold or rule | If it fails |
|---|---|---|
| Who is in the sample, and why | Name the factor that put each person in it; is it related to the quantity measured? | Related: biased. Say so, correct (section 3) or refuse to generalise |
| Response rate | Low, and the reason to respond could relate to the answer | Treat respondents and non-respondents as two strata; need a follow-up sample of non-respondents |
| Selection likelihood | Some types more likely to be sampled (frequent visitors, heavy users, engaged followers) | Re-weight by n_i/f_i |
| Normal approximation | Means n ≥ 30; proportions n·p ≥ 5 and n(1 − p) ≥ 5; n/N < 0.05 | Use t (df = n − 1) for small means; caveat |
| Scale level | Purely ordinal (ranks, few ordered categories): median, not mean | Report medians or distributions |
| Awareness figure | States which measure (unaided first-named, unaided any, aided) | Number is not interpretable; ask |
| Intent figure | Stated intent overstates buying | Deflate before forecasting |
| Share figure | States units or revenue, served or total market | Ask; both can be right and differ a lot |
| Before/after on the same people with aided recall, attitude to a named brand or knowledge | The first measurement sensitises the treated group | Plan after-only with a control group; judge results in evidence-check |

## 3. Run it: exact formulas

| Need | Formula |
|---|---|
| CI, mean | x̄ ± z_{α/2} s/√n (n < 30: t_{α/2, n−1}) |
| CI, proportion | p ± z_{α/2} √(p(1 − p)/n) |
| CI, total | N × estimate ± N × margin |
| n, mean, absolute error E | n ≥ (z_{α/2} σ/E)²; no σ: σ ≈ (plausible high − plausible low)/6 |
| n, mean, relative error r | n ≥ (z_{α/2}/r)² (σ/μ)², CV borrowed from a proportional proxy |
| n, proportion | n ≥ z²_{α/2} π(1 − π)/E²; no prior π: 0.5 |
| n for a total N·π within ± NE | E = NE/N, then the proportion formula |
| Precision scaling | n ∝ 1/E²: halving E needs 4x the sample. Round n up |
| Stratified estimate | x̄_s = Σ (N_h/N) x̄_h; SE = √(Σ (N_h/N)² s_h²/n_h) (proportions: p_h(1 − p_h)) |
| Allocation | proportional n_h = (N_h/N) n; optimal n_h ∝ N_h σ_h/√c_h |
| Non-response weights | N_1/N = response rate (respondents); N_2/N = 1 − rate (non-respondents, from the follow-up) |
| Non-coverage weights | N_1/N = (n_1/f_1)/(n_1/f_1 + n_2/f_2), f = 1 for the less likely group, f = x for the group x times more likely |
| Test vs break-even | H0: Par ≤ K. Reject if est > K + z_α SE; p = P(Z ≥ (est − K)/SE) |
| SE by test | mean s/√n; proportion √(K(1 − K)/n) (uses K, not p); two independent groups √(s_1²/n_1 + s_2²/n_2); paired s_d/√n |
| z values | one-sided 95% 1.645, 99% 2.33; two-sided 95% 1.96, 99% 2.575; 90%: 1.28 / 1.645 |
| Conjoint importance | range_i / Σ ranges, range = max − min part-worth of attribute i |
| Brand switching | X and Y do not compete iff xy = 0 and yx = 0; loyalty = diagonal / row total |

## 4. Decision rules

| Situation | Rule |
|---|---|
| Exploratory output (focus groups, open answers, selected cases) | Ideas and hypotheses, never percentages to generalise |
| What drives success | Compare extreme successes with extreme failures attribute by attribute, never winners alone |
| Focus groups | 8 to 12 people, 1.5 to 2 h, a moderator; at least 2 groups; stop when the next adds nothing |
| Secondary data | Internal first, then external, then paid syndicated; primary research only for what is left |
| Correlation in descriptive data | Association, not cause; one snapshot cannot show change or switching |
| Biased sample | More interviews do not fix bias; re-weight or redesign |
| Break-even decisions | Act only if the estimate clears K + z_α SE; otherwise keep the status quo |
| Two groups differ? | Independent groups: no weights in the SE. Same people twice or matched: paired test |
| Not significant | No evidence, not proof of no difference; give the CI |
| Attitude tool | Low involvement: one simple rating; high and emotional: Likert (check one dominant factor); high and rational: semantic differential or conjoint |
| Conjoint | Overall ratings only; one model per respondent; interpolate between studied levels, never extrapolate |
| Feature importance | Stated importance underrates must-haves; prefer derived (conjoint or regression) |

## 5. Write the answer

```
Verdict: [what the study can support, in one line]
Deciding number: [estimate ± margin, n, and the bias check]
Naive read and why it is wrong: [one line]
Action: [use / correct / redesign / collect more] · How to verify: [follow-up sample, re-weighting, pilot, test]
What the user must decide: [question, threshold or design choice left to them]
```

## 6. Adversary for every move

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Define the question | "What decision changes if the answer comes back high vs low?" | User names the decision and status quo | Ask; do not design yet |
| Pick the design | "Is the question precise enough for a descriptive study?" | Population and variables known in advance | Start exploratory |
| Pick the design | "Does the user need change over time or switching?" | Repeated measurement of the same units planned | Use a panel; a snapshot cannot show it |
| Pick the design | "Is this a causal claim?" | Wording: caused, worked, effect of | Plan a controlled design; judge results in evidence-check |
| Write questions | "Could a respondent misread, not apply, or feel pushed?" | Audit A1 to A6, B, C1 to C5 (questionnaire.md) | Rewrite the item |
| Order questions | "Does an early question tell them what we study?" | Funnel: general first, brand later, sensitive last; unaided before aided | Reorder; remove the brand from the cover note |
| Code answers | "Is a blank a 'none' or a non-answer?" | Question structure lets you tell them apart | Code blank, not 0, and say non-response is undetectable |
| Choose the sample | "What made each person likely to be in it, and does that relate to the answer?" | Convenience-bias test | Re-weight, redesign, or limit the claim to that group |
| Size the sample | "Did I scale n linearly with precision?" | n ∝ 1/E²; per-subgroup reads need n per subgroup | Recompute |
| Estimate | "Who did not answer, and would they answer differently?" | Response rate; follow-up of non-respondents | Stratified correction; or flag as an upper bound |
| Estimate | "Did the procedure favour some types?" | Selection factors f by group | Non-coverage weights |
| Test vs threshold | "Is H0 the status quo, and is K the real break-even?" | H0: Par ≤ K with K from the decision | Rewrite H0; convert totals to per-unit K = total/N |
| Report a measure | "Which measure is this number?" | Awareness type, unit vs revenue share, served vs total | Name it or ask |
| Use intent | "Will they actually buy?" | Intent is stated, not revealed | Deflate; recommend a market test |
| Recommend | "What does it cost if this is wrong, and what would the CFO ask?" | Downside in money; a cheap way to verify (pilot, follow-up, test) | Add the check or shrink the bet |

## 7. Score-and-probe gate before handover

1. Confirm every adversary check passed or its fix was applied. Any open
   failure: fix first; do not score.
2. Score the draft 0 to 100 on the moderation rubric from the user's
   hybrid-research notes:
   - **Clarity**: verdict, number and action readable in one pass.
   - **Relevance**: answers the user's decision.
   - **Depth**: shows the estimate, its margin, and the bias check.
   - **Insightfulness**: names the error term that dominates and what the naive read misses.
3. Any score below 80: write the probe that would raise it (for example "how
   would the estimate move if non-respondents were half as interested?"),
   answer it from the data, revise, re-score. At most 2 loops, then hand over
   and say what is still weak.

---

## File: research-design/references/design.md

# Choosing a research design

## The two questions every study answers

1. What information would improve this decision?
2. How do we get it at the lowest cost?

If the answer could not change the decision, do not run the study.

## Design families

| Situation | Design | Output |
|---|---|---|
| Research questions not yet precise; must not miss anything | Exploratory | Ideas, hypotheses, the right questions |
| Population and variables known; want distributions, sizes, shares | Descriptive, cross-sectional (one snapshot) | Estimates with margins |
| Need trends, seasonality, who moves where | Descriptive, longitudinal | Change over time; a fixed panel adds switching |
| Need to establish and size cause and effect | Causal (experiment) | Effect estimate |

Variants of longitudinal work: trend study (fresh sample each wave: change in
the population), cohort study (same group re-sampled), panel (same
individuals: the only design that shows individual switching). Panels drift
over time through dropout and conditioning (being measured changes
behaviour).

A snapshot shows association, never change or switching: two brands can hold
steady shares while many buyers cross between them.

## Exploratory tools

| Tool | Use for | Rules |
|---|---|---|
| Open-ended survey | Usage, intentions, value systems, and recent changes in them | Answers coded after collection; articulate respondents are over-represented |
| Analysis of selected cases | What separates success from failure on a measured outcome | Take both extremes, compare attribute by attribute; the differing attributes are candidate drivers. Studying winners alone ("best practices") cannot separate drivers from shared habits |
| Focus groups | New ideas, concept screening, shifting preferences | 8 to 12 people, 1.5 to 2 h, a moderator with a topic outline (no leading questions); at least two groups; stop when another adds nothing; never treat output as statistics |

## Data sources, in order

1. Internal secondary data (sales, prices, promotions, CRM): free, fast.
2. External secondary: libraries, trade press, government (population and
   strata sizes N, N_h).
3. Syndicated services, judged by unit (store, household, individual) and
   method (asking vs observing). Store audits miss demographics and loyalty;
   household panels give loyalty and switching. Self-recorded diaries add
   random errors and change behaviour (people become price-aware); passive
   scanning avoids both. Audit sales (start stock + deliveries − end stock)
   count shrinkage as sales: biased upward.
4. Primary research for what remains.

## Causal designs (planning only)

Judging whether a test or change actually worked belongs to evidence-check.
These rules choose a design before fielding.

Cause needs: the two move together, the cause comes first, and nothing else
explains the change. Correlation alone fails the third (budgets often follow
past sales).

| Control over who is measured | Control over who is treated (randomise or match) | Class |
|---|---|---|
| Yes | Yes | True experiment |
| Yes | No (self-selection, or no control group exists) | Quasi-experiment |
| No | No | Pre-experiment: hypotheses only |

Threats and their design remedies:

| Threat | Remedy |
|---|---|
| History and maturation (U) | Control group; difference in differences |
| Groups not comparable (selection) | Randomise or match |
| Dropout tied to a demanding treatment | Before-after design (shows who started) |
| Units picked for extreme scores (regression to the mean) | Representative sample; select on long-run behaviour |
| Measurement method changes between waves | Same instrument throughout |
| People react to being measured | Anonymity; otherwise acknowledge |
| First measurement directly affects the second (carryover) | Removed by a control group if equal in both |
| First measurement sensitises the treated group (interactive testing) | Only removing the pre-measurement fixes it |

Interactive testing is common in marketing: aided recall ("have you heard of
brand Z?"), attitude toward a named brand, or knowledge questions asked
before a campaign. A before-after design with a control group then reports
effect + interaction, which can be far larger than the effect. Use after-only
with a randomised control group, unless the treatment is demanding (dropout
would make the groups differ).

Designs without randomisation: global events with no control group use
separate samples before and after (effect + U; keep the interval short);
a chain-wide promotion uses a non-equivalent control (a non-competing
product or other stores); periodic history can be removed with moving
averages over a long series.

---

## File: research-design/references/measures.md

# Customer measures and their traps

## Scale levels

| Level | Meaning | Allowed |
|---|---|---|
| Nominal | categories only | counts, mode, cross-tabs, chi-square; dummies in regression; Y in logit |
| Ordinal | order, gaps not comparable (ranks, ordered ranges) | + median, percentiles |
| Interval | equal units, no true zero | + mean, SD, correlation, regression |
| Ratio | equal units and a true zero | + ratios and % changes |

Rating scales with many points approximate interval well enough for means;
few ordered categories do not. Reliability = free of random error; validity =
free of random error and bias. A reliable measure can be consistently wrong.

## Awareness

| Measure | Question | Note |
|---|---|---|
| Top-of-mind | First brand named, no brand mentioned | Strictest |
| Unaided recall | Any brand named, no prompt | |
| Aided (recognition) | "Have you heard of X?" | Easiest; crowds near the ceiling, so it cannot separate strong brands |

- Record per respondent as 0/1; report the share of the sample, always with
  the measure named. "40% awareness" alone means nothing.
- Ask unaided first, then aided. Never let an earlier question or the cover
  note name the brand.
- A large aided-minus-unaided gap = known but not salient.
- Plant a fictitious brand in aided lists; its "yes" rate measures false
  recognition.
- Aided recall asked before a campaign sensitises respondents: see design.md.

## Attitude and feature importance

| Involvement | Tool |
|---|---|
| Low: product seen as a whole | One simple rating per object |
| High, emotional | Likert summated scale; valid if factor analysis of the items shows one dominant factor |
| High, rational | Semantic differential with importance weights, or conjoint |

Rating-scale choice by how finely respondents can distinguish: unfamiliar
respondents → itemized (about 5 categories); very familiar → graphic; able to
compare absolute sizes → constant sum (avoids the compression a low
reference causes in fractionation); rank order only if they use the same
criterion for every comparison.

Importance weights:
- Stated ("how important is...") underrates must-have attributes that people
  take for granted.
- Derived by regression of overall rating on attribute ratings pools everyone
  into one set of weights and assumes linear effects.
- Conjoint fixes both.

## Conjoint

1. Attributes that drive choice and that you control; 2 to 4 levels each,
   always including the extremes of the feasible range.
2. Hypothetical profiles from an orthogonal design (each level appears
   equally often and independently, e.g. a Latin square for 3 attributes of
   equal levels); add all-best and all-worst anchors, drop them before
   fitting.
3. Ask only an overall rating per profile.
4. Fit one dummy-coded regression per respondent (needs clearly more ratings
   than parameters). Part-worth = 0 at each attribute's lowest level.
5. Outputs: ideal profile (best level of each); importance_i = range_i/Σ
   ranges; share simulation (each respondent picks the highest-utility
   option, share = fraction choosing it, needs a sample representative of the
   market); benefit segments (cluster on part-worths).
6. Interpolate part-worths linearly between studied levels; never evaluate a
   level outside the studied range.

## Purchase intention

- Use it when there is no purchase history: new concepts, durables, rare
  purchases. Otherwise use actual usage data.
- Stated intent overstates purchase, and the errors do not cancel in
  aggregate. Never feed top-two-box or raw "yes" into a volume forecast:
  deflate with factors calibrated on past launches, or use a 0 to 10
  probability scale and average the probabilities; validate per category.
- Interest questions also carry politeness bias (questionnaire.md, B).

## Share, switching, loyalty

- Market share: state units or revenue (revenue share above unit share = a
  price premium) and served or total market (same numerator, different
  denominator).
- Share = penetration share × share of requirements × usage index: low
  penetration is a reach problem, low share of requirements a loyalty
  problem.
- Brand-switching matrix (needs the same buyers on two occasions, i.e. a
  panel): rows = first purchase, columns = next. X and Y do not compete only
  if both xy and yx are 0. Loyalty = diagonal / row total.
- Repeat rate rises with brand size; compare a brand's loyalty with what a
  brand of its size usually shows before crediting the brand team.
- Behavioural loyalty (repeat, share of wallet) and attitudinal loyalty
  (stated preference, recommend scores) often disagree; name which you report.

## Media habits

Reach = unique people exposed at least once; frequency = impressions/reach;
GRP = reach % × frequency. Channel reaches cannot be summed (people overlap).
See metric-definitions for the metric formulas.

---

## File: research-design/references/questionnaire.md

# Questionnaire: construction, error audit, coding

## Construction

1. Name the main block of information (usually current or future usage) and
   the decision it feeds. Ask other blocks only where they relate to it.
2. Blocks available: state of being (demographics, ownership of related
   products), state of mind (awareness, value system = attribute weights,
   knowledge/beliefs = ratings, attitude), behaviour (usage where a purchase
   history exists; intentions for durables, rare purchases and new concepts;
   media habits).
3. Outline each block, then pick each question's form.
4. Sequence as a funnel: easy, general, interesting first; more specific
   next; sensitive last. Early questions must not reveal what is studied.
   Unaided awareness before any brand list.
5. Cover note: short, no brand named, thank the respondent.

### Question forms

| Form | Use when | Coding consequence |
|---|---|---|
| Open-ended | Answer space unknown (exploratory) | Post-coded; articulate people over-represented |
| Multiple choice, pick one | Answer space known (descriptive) | One variable; categories must be mutually exclusive, collectively exhaustive and appropriate |
| Dichotomous | Yes/no | One 0/1 variable |
| Check all that apply | Several yes/no items | One 0/1 variable per option; non-response undetectable |
| Multiple choice + "Other (specify)" | Main answers known, tail unknown | Scheme finished after collection |

Appropriate categories: pick a very low but possible and a very high but
possible value as the end categories, split the range between into equal
steps (5 to 7 categories total).

## Error audit (run on every draft)

| Code | Check | Fix |
|---|---|---|
| A1 | Does it apply to everyone? | "Does not apply" option; "Don't know" on every rating; screening question with a skip |
| A2 | Unfamiliar words or units | Plain words; define terms |
| A3 | Categories overlap, leave gaps, or all answers land in one | Fix ranges; add "other", "both", "neither"; use the end-value recipe |
| A4 | Vague terms ("regularly"), unlabeled scale ends, object with several dimensions | Define frequency over a stated period; label ends; one dimension per question |
| A5 | Respondent must estimate or calculate | Ask the components; compute yourself |
| A6 | Double-barrelled (two things, one answer) | Split |
| B | A socially preferred answer exists (interest in a new concept, donations, ethical premiums) | Observe instead; anonymity; a counter-biasing sentence before the question |
| C1 | Long option list: first and last picked more (worse by phone) | Randomise order |
| C2 | Categories create the answer (unfamiliar people pick the middle; "Other" rarely written in) | Open-ended with "don't know" |
| C3 | Two-sided issue, one side shown | Show both sides |
| C4 | Status quo unclear ("saves 70%" vs "30% die") | State the baseline |
| C5 | Gain named, cost hidden | Name the sacrifice |

Framing errors (C) are strongest when respondents know little about the
topic: the wording supplies the opinion they lack. Expect stated interest in
a new concept to be both polite (B) and framed (C).

## Coding

For each question: how many variables, which values, which non-response
code.

| Question type | Variables | Non-response |
|---|---|---|
| Pick one | 1 nominal, codes 1..k | Blank |
| Pick one + Other | 1 nominal; frequent "other" answers get codes, the rest "all other" | Blank |
| Number | 1, entered as given | Blank |
| Rating with DK | 1 per item | Blank if skipped or DK (never a number) |
| Check all / open list | 1 binary per option or mentioned item, rare ones lumped | Undetectable: an empty row may be "none" |
| Screener (yes/no) + list | Screener 1/0 + one binary per item | Screener "no": 0s. Screener "yes", list empty: list blank. Both empty: all blank. Screener skipped, list filled: screener = 1 |
| Top-3 ranked reasons | 1 per reason, coded 3/2/1/0 | All blank only if no reason given; one or two given is not non-response |

Blank means unknown; 0 means known not to apply. Use 0 only where the
question structure distinguishes the two. In a regression, a nominal variable
with k categories enters as k − 1 dummies; keep all columns in the data.

---

## File: research-design/references/sampling.md

# Sampling, sample size and inference

## Choosing the method

| You have | Method |
|---|---|
| No idea of the variance | Sequential: small pilot, estimate σ, add units until precise enough |
| A list, distinct subgroups that behave differently, a list per subgroup | Stratified (proportional; optimal if σ_h and costs known) |
| A list sortable by a continuous proxy, no cycles along it | Systematic: k = N/n, random start R, take R, R + k, ... |
| A list, nothing else | Simple random sampling |
| No list; a trait linked to the answer with known population % | Quota |
| No list; a sub-population judged typical (test-market city) | Judgement |
| No list; a rare group whose members know each other | Snowball |
| No list, nothing else | Convenience, after the bias test |

**Convenience-bias test.** Name the exact factor that made each person likely
to be included. If it relates to what you measure, the estimate is biased
(newsletter subscribers on "interest in our new line"; social followers on
"brand awareness"). If not, it can be fine.

Systematic sampling on a list where the quantity cycles with period k
captures one phase of the cycle: worse than random.

## Sample size

| Case | Formula |
|---|---|
| Mean, absolute error E | n ≥ (z_{α/2} σ/E)² |
| σ unknown, plausible range known | σ ≈ (high − low)/6 |
| Mean, relative error r (E = rμ) | n ≥ (z_{α/2}/r)² (σ/μ)²; borrow σ/μ from a proportional proxy |
| Proportion | n ≥ z²_{α/2} π(1 − π)/E²; π = 0.5 if no prior (safe, may overspend) |
| A total N·π or N·μ within ± NE | E = NE/N, then the formulas above |
| Back out n from a reported margin m | n = z²_{α/2} p(1 − p)/m² |

- Always round up.
- n ∝ 1/E². Halving the margin multiplies n by 4; tightening ±6 to ±3 is not
  "double the sample".
- Each subgroup that needs its own read at margin E needs its own n.
- Stratifying on groups that really differ lowers the σ that matters, so it
  needs fewer interviews for the same precision; groups that do not differ
  add cost for nothing.

Illustration: a prior read of 30% and a target of ±2.5 points at 95%:
n ≥ 3.8416 × 0.21/0.000625 = 1,290.8 → 1,291. For ±5 points: 323.

## Stratified estimates

x̄_s = Σ (N_h/N) x̄_h; SE = √(Σ (N_h/N)² s_h²/n_h); n_h ≥ 30 for means,
n_h p_h ≥ 5 and n_h(1 − p_h) ≥ 5 for proportions.
Stratification removes the between-group part of SRS variance.
Allocation: proportional n_h = (N_h/N) n; optimal n_h/n =
(N_h σ_h/√c_h)/Σ(N_j σ_j/√c_j).

## Correcting non-response

Non-respondents often differ from respondents on the very thing asked
(interested people reply). Respondents-only estimates are biased, and more
replies of the same kind do not help.

1. Treat respondents and non-respondents as two strata.
2. Get a random follow-up sample of non-respondents to answer (named list:
   contact a random subset; anonymous survey: re-contact about a third of the
   whole sample with a "did you submit?" screener).
3. Weights: N_1/N = response rate, N_2/N = 1 − response rate.
4. Stratified estimate, SE, CI; report next to the uncorrected figure.

Illustration: 2,000 invited, 300 replied (15%), 58% interested; follow-up of
120 non-respondents, 15% interested. Corrected: 0.15 × 0.58 + 0.85 × 0.15 =
0.215. SE = √(0.0225 × 0.58 × 0.42/300 + 0.7225 × 0.15 × 0.85/120) = 0.028;
95% CI 21.5% ± 5.5. The respondents-only 58% overstates by 2.7x. Pooling the
two waves unweighted (192/420 = 46%) is also wrong.

No follow-up exists: say the respondents' figure is likely overstated when the
reason to reply relates to the answer (interest, satisfaction), and recommend
a follow-up sample before the number drives a decision.

## Correcting non-coverage

When the procedure favours some types (intercepts at a venue favour frequent
visitors; followers and openers favour engaged customers):

1. Split the sample into the groups (clustering can reveal them).
2. f = 1 for the less likely group, f = x for the group x times more likely
   (from secondary data or the visit-frequency ratio).
3. N_1/N = (n_1/f_1)/(n_1/f_1 + n_2/f_2); then the stratified estimate.

## Confidence intervals

x̄ ± z_{α/2} s/√n (n < 30: t); p ± z_{α/2} √(p(1 − p)/n); totals: multiply
estimate and margin by N. Conditions: n/N < 0.05, n ≥ 30, n·p and n(1 − p)
≥ 5. The width shrinks with √n, not n.

## Testing against a business threshold

1. H0 is the status quo, written as Par ≤ K; Ha: Par > K (the claim that
   would justify acting). Reorder differences so the claim is "> K".
2. K from the break-even; totals become per-unit (K = total/N).
3. Reject if est > K + z_α SE (one-sided z_α: 1.645 at 95%, 2.33 at 99%).
   Proportion test SE uses K: √(K(1 − K)/n). p-value = P(Z ≥ (est − K)/SE).
4. Then give a two-sided CI for the size.

| Comparison | SE |
|---|---|
| One mean | s/√n (t with df n − 1 if n < 30) |
| One proportion | √(K(1 − K)/n) |
| Two independent groups | √(s_1²/n_1 + s_2²/n_2); small samples t with df n_1 + n_2 − 2 |
| Same units twice / matched | s_d/√n on the differences |

Pitfalls: z_{α/2} in a one-sided test; p instead of K in the proportion test
SE; paired data tested as independent; stratified weights used to compare two
groups (weights belong to estimating one population).

---

# Skill: hybrid-research

---
name: hybrid-research
description: >-
  Use this skill when a marketer wants to run research with an AI in the loop: "can we
  use AI respondents / synthetic personas / a synthetic panel instead of a survey",
  "simulate how customers would answer", "test our concepts with ChatGPT personas",
  "draft a survey or questionnaire", "write an interview or discussion guide", "pilot
  our survey before we field it", "how many respondents do we need", "does our
  synthetic data match the real survey", "is this AI panel good enough", "run AI
  interviews", "summarise these interview transcripts into themes", or any use of
  LLM-generated answers as evidence for a launch, price, positioning or budget
  decision. It decides when synthetic respondents are acceptable, reviews the
  instrument, builds personas and prompts, runs the backward pilot, scores recovery
  against a human benchmark, and keeps the question and the decision with the human.
  Synthetic data informs; it never replaces real evidence for high-stakes decisions.
---

# hybrid-research

An LLM can draft the survey, play the respondents, probe itself and code the
themes in an afternoon. It cannot tell you the right question, and its answers
look right on the mean while being wrong on the spread and on how answers hang
together. This skill runs the hybrid: the LLM proposes, the checks attack, the
human disposes.

## 1. Classify the request

| The user wants to... | Go to | Data you need |
|---|---|---|
| decide whether synthetic respondents are OK for a question | 2 | research brief, the decision it feeds |
| draft or review a survey or discussion guide | 3 | brief, target population, any draft |
| build personas and prompts, generate synthetic answers | 4, 5 | final instrument, sample spec or human sample demographics |
| pilot an instrument before fielding ("backward" research) | 6 | instrument, synthetic panel |
| judge whether a synthetic panel matches reality | 7 | human data on the same items (respondent x item) |
| run or judge AI interviews, extract themes | 5, 8 | guide, transcripts |
| write up findings | 9 | all of the above |

If no research brief exists (business objective, research question, target
population, intended use), stop and ask for it. That stage is human-owned.

## 2. Decision tree: are synthetic respondents acceptable?

Walk it top to bottom. The first "stop" wins.

| # | Question | If yes | If no |
|---|---|---|---|
| 1 | Is the research question and design (exploratory, descriptive, causal) set by a human? | next | stop: ask for the brief |
| 2 | Is the topic new to the world (a product, behaviour or trend the model cannot have seen)? | stop: human respondents only; LLM for drafting and analysis | next |
| 3 | Culturally sensitive topic, or a population the model is likely to stereotype (non-Western, in-group language)? | human respondents for those segments; synthetic for the rest at most | next |
| 4 | Vulnerable groups, children, health, politics? | human judgement on what may be asked; no synthetic stand-ins | next |
| 5 | Would personal data (PII) have to go into prompts? | stop: anonymise or do not send | next |
| 6 | Is the decision high-stakes (launch, pricing, large budget)? | synthetic only to preview and refine the instrument; field to humans for the evidence | synthetic may suffice, after it passes section 7 on a historical benchmark |
| 7 | Hard-to-reach population (B2B buyers, specialists) with a tiny human sample? | synthetic as a prior and supplement; report agreement and divergence with the humans | as above |

Configuration by available context (quant):

| You have | Use | Expect |
|---|---|---|
| nothing beyond personas | zero-shot (LLM1) | direction right, extremes too strong, low variance, correlations near 0 |
| prior answers of the same respondent | few-shot with response history (LLM2) | variance and correlations improve; mean bias unchanged |
| relevant past qual research or reports | few-shot + RAG (LLM3), K = 3-5 chunks | best correlation recovery; mean bias unchanged |

Response history is non-negotiable for any survey run. Qual: start with
Hybrid 3 (human guide and sample, LLM respondent and moderator); see
[references/qual-interviews.md](references/qual-interviews.md).

## 3. Co-design the instrument

The LLM drafts screeners, concept descriptions, Likert items, behaviour bins,
demographics and skip logic. The human refines and signs off. Before sign-off
run every item through this table:

| Item check | Fails when | Fix |
|---|---|---|
| Double-barrelled | two attributes joined ("fast and easy", "visually or for the brand") | split into two items |
| Leading or loaded | wording presumes the answer ("our new improved", "how much did you enjoy") | neutral wording, balanced scale |
| Scale | binary yes/no on an attitude; unbalanced or unanchored scale | 5- or 7-point Likert, labelled ends |
| Rank order | "rank these 5" | rate each item separately |
| Open text for a structured variable | "gender: ____" | fixed options |
| Expected spread | 90%+ will answer the same way | rewrite or drop |
| Construct | item does not measure what the brief needs (face validity) | rewrite or add the missing item |
| Flow (A/B surveys) | anything between stimulus and outcome items; outcome items differ by arm | warm-up, stimulus, outcomes, characteristics, demographics; identical outcomes |

Item rules, the A/B flow and outcome items: [references/instrument.md](references/instrument.md).

## 4. Build the persona matrix

Quant personas are a vector of discrete variables, not a story. Qual personas
add biography, quirks and conflicting attitudes.

| Layer | Contents |
|---|---|
| Core demographics | age, gender, ethnicity, location, urbanicity, education, income, employment, marital status, household size |
| Category qualifiers | ownership, usage frequency, purchase role, brand awareness (must satisfy the screener) |
| Attitudinal priors | category attitudes, price sensitivity, lifestyle (add when demographics are too thin, which is usual) |

Matrix checks:

1. **Coverage.** Every segment named in the brief and every segment the
   decision targets has rows (e.g. lapsed customers for a win-back study,
   non-buyers for an acquisition study). Ask the LLM which niche or
   under-represented segments are missing; the human decides which to add.
2. **Distribution.** Replication: match the human sample's demographic
   distribution 1:1 and show the comparison table. New sample: match the
   stated quotas.
3. **Uniqueness.** No two personas identical on all variables; qual personas
   must not read as variations of one person.
4. **Sensitivity.** Swap one demographic (gender, income, ethnicity) on a few
   personas and re-ask. If answers do not move where they should, or move as a
   caricature, the model is stereotyping: report it.

## 5. Prompt, generate, validate, retry

Prompt = context + system role (persona) + user role (question and format).
Never skip the context. Templates: [references/quant-synthetic.md](references/quant-synthetic.md).

Generation loop per persona, per question:

1. System role: persona (+ prior Q/A pairs of this respondent; + retrieved
   context if RAG).
2. User role: verbatim question, rigid format ("Answer with a single number
   only... Use this format to answer: 3"), the options.
3. Validate: format (parses to an allowed value), completeness (no refusal or
   hedge), plausibility (in range for persona and question), in character.
4. On failure resend the same question, up to 3 attempts; then log it as
   missing, never fill it in.
5. Settings: temperature 1.0 for surveys (lower clusters at the mode), fixed
   seed, logged prompts. In a chat with no temperature control, ask for
   heterogeneity ("avoid converging toward the average").
6. Random assignment to arms is done in code, not by the LLM.

Report: retry rate and unresolved failures per question.

## 6. Backward research: simulate before you field

Analyse the synthetic panel as if it were real, then use it to fix the
instrument, not to answer the business question.

| Synthetic result | Read it as | Action |
|---|---|---|
| an item with (near) zero variance | wording problem or too obvious, or variance compression | rewrite or drop; confirm on humans |
| a needed dimension has no item | gap | add the item |
| one concept dominates by a wide margin | the human survey may only confirm it | human decides whether to field; never "launch on synthetic" |
| item SD for power | a floor, because synthetic variance runs low | n per arm = 16 x sigma^2 / delta^2 with sigma^2 = synthetic variance / variance ratio from past studies (section 7); if none, show n as a minimum and give the range |

## 7. Recovery against a human benchmark

Compute on the same items, the same scale, and a demographically matched
sample. Formulas and code: [references/recovery-metrics.md](references/recovery-metrics.md).

| Metric | Formula | Pass |
|---|---|---|
| Mean bias (MAE) | mean over items of abs(mean_human - mean_LLM) | < 0.5 on a 5-point scale |
| Variance ratio | var_LLM / var_human, per item | 0.7 to 1.3 on every key item |
| Correlation MAE | mean over item pairs of abs(r_human - r_LLM) | < 0.2 |
| Distribution | chi-square on binned answer counts, per item | p > .05 |
| Winner | top concept, synthetic vs human | same |
| Rank order | Spearman rho of item or concept rankings | >= .80 |

Read the metrics in this order: variance ratio and correlation MAE first,
mean second. A matching mean with a variance ratio below 0.7 is a failed
panel: segment cuts, drivers, correlations and sample sizes from it are
wrong. Typical zero-shot pattern: direction right, about 0.5-0.7 points too
extreme on 5 points, variance low, correlations near zero. Context fixes
structure (variance, correlation), not level (mean). Correct a mean only with
a bias measured on past studies in the same category.

No human benchmark: say the panel is unvalidated, run a historical replication
(old survey, its demographics) before trusting it, and log every study in a
validation repository.

## 8. Qual: self-moderation and themes

- Score each answer 0-100 on clarity, relevance, depth, insightfulness;
  average below 80 triggers a natural follow-up probe aimed at the weakest
  dimension; at most 2 probes per question. If under 20% of turns trigger a
  probe, the threshold is too low.
- Pass full Q/A history every turn; re-run turns that refuse, go off-topic or
  break character.
- Themes: recovery of human-baseline themes >= 80%; themes found in both
  sources are high confidence, human-only themes carry lived experience,
  LLM-only themes are expansion hypotheses to test, not findings.
- Similarity of LLM to human answers: embedding cosine >= .5 is high.

Detail: [references/qual-interviews.md](references/qual-interviews.md).

## 9. Report

```
Verdict: [synthetic OK for X / preview only / not acceptable]: [one line]
Deciding number: [e.g. "variance ratio 0.31 on 7 of 8 items; correlation MAE 0.46"]
Source label: every number tagged human, synthetic, or both
Naive read and why it is wrong: [one line]
Action: [fix instrument / add segment / field N humans per arm / proceed]
How to verify: [human wave, historical replication, A/B test]
Human-owned: [the question, the design, the decision; open questions for the user]
```

Never write "customers say" or "the market wants" about synthetic answers.
Write "synthetic respondents (n=, model, configuration) answered". Do not
present a p-value from a synthetic panel as evidence: the analyst chose n, so
more personas always make it "significant". Do not pool synthetic and human
counts into one ranking; report each source, then the overlap.
Commercial synthetic panels get the same checks (sections 4, 5, 7).

## Adversary pass

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Accept the brief | "Who set this question, and what decision rides on it?" | brief has objective, question, population, use | ask the human; do not draft |
| Choose synthetic | "Is this new to the world, sensitive, PII, or high-stakes?" | walk section 2 | humans for the evidence; synthetic as preview only |
| Sign off the instrument | "Could one answer mean two things, or does the wording push it?" | every item through the section 3 table | split, neutralise, rescale |
| Build the matrix | "Who that the decision targets is not in here?" | coverage vs brief and decision; distribution table | add the segment, regenerate |
| Generate | "Would these answers parse, and did any get filled in silently?" | validation log, retry and missing counts | fix the format prompt, re-run |
| Pilot backward | "Is this zero variance the item or the model?" | compare with a human pilot or past variance ratio | rewrite item; treat SD as a floor |
| Claim a match | "Does the spread and the correlation match, not only the mean?" | variance ratio and correlation MAE computed | panel fails; add history, priors, RAG |
| Merge themes | "Which themes did a human ever say?" | source tag per theme | LLM-only themes become hypotheses |
| Recommend | "What does it cost if the synthetic read is wrong, and what would the CFO ask?" | downside stated; a human wave or test named with its n | shrink the bet or field first |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on clarity (unambiguous), relevance (answers the question asked,
for this reader), depth (explains why with numbers) and insightfulness (says
something new and what to do). If any is below 80, write the probe question
that would raise it, answer it from the data, revise, and score again (two
loops at most). The question, the research design and the decision belong to
the person asking: when either is unclear, ask instead of assuming.

---

## File: hybrid-research/references/instrument.md

# Instrument design and review

Load when drafting or reviewing a survey or discussion guide.

## 1. Division of labour

| LLM drafts | Human does |
|---|---|
| screeners, concept descriptions at several lengths, Likert items (flags redundancy), behaviour bins, demographics, skip logic | checks each item measures its construct; removes redundant and double-barrelled items; checks scales are balanced and anchored; adds business-specific items; tests flow, timing and fatigue; adds platform instructions (randomisation, piping, quotas); signs off |
| discussion guide: warm-up, core sections per research question, probes, wrap-up | adds business terms; cuts off-topic items; reorders for natural flow; matches respondent vocabulary; adds conditional branches; signs off |

Prompt for a draft with: the brief, the respondent profile, hypotheses, length
and mode. Break it into stages (outline, sections, refinement) rather than one
"do everything" prompt. Ask the LLM how to refine your prompt when the draft
is generic.

## 2. Item rules (they bite harder on synthetic respondents, which read literally)

| Rule | Why | For synthetic data |
|---|---|---|
| 5- or 7-point Likert, not yes/no, for attitudes | binary gives one bit | the model already compresses variance; binary makes it worse |
| No rank-order items | hard to answer and analyse | the model ranks each position independently, not as a constrained set |
| Fixed options for structured variables | parsing | essential for machine-parsable output |
| Items must spread | 90% same answer gives no power | pre-test with ~20 synthetic answers; one-bin items get rewritten or dropped |
| No double-barrelled items | a respondent who agrees with one half cannot answer | the model silently answers one half; you cannot know which |
| Balanced, anchored scales | an unbalanced scale pushes answers | |
| Force response (human surveys) | missing data costs power | synthetic always answers; validate instead |

Leading or loaded wording (an item that presumes or praises: "our improved",
"how much did you enjoy") is screened together with scale balance: the
question must not tell the respondent which answer is expected. (See
SOURCES.md: this rule is standard survey practice requested for this skill,
not stated in the notes beyond scale balance.)

Spotting a double-barrelled item: it contains "and" or "or" joining two
attributes, or two adjectives that can diverge (attention-grabbing and
striking; visually or brand-wise). Test: can a person honestly agree with one
part and disagree with the other? If yes, split.

## 3. A/B concept survey flow

1. Introduction
2. Warm-up questions (easy customer characteristics; also pre-treatment
   balance variables)
3. Random assignment, one version per respondent (done in code)
4. Outcome items, immediately after the stimulus, identical for both arms
5. Other customer characteristics (category interest, past purchase,
   loyalty, psychographics)
6. Demographics

Balance check after assignment: t-test per numeric characteristic,
chi-square per categorical one; p >= .05 on each means no evidence of
imbalance.

## 4. Outcome item families

Pick the family that maps to the real-world metric; word your own items.

| Real metric | Item family (7-point) |
|---|---|
| conversion | likelihood to add to cart, buy, visit the store, buy as a gift |
| usability | ease of use, information presented effectively, easy to understand, visual appeal |
| engagement | likelihood to click the named CTA, browse more, comment or like |
| affect | overall liking, eye-catching image, product looks [attribute] (one attribute per item) |

Customer characteristic batteries (tech-savvy, fashion-conscious, impulse,
health, green, inclusive, socially conscious, category spend, social media
use) double as balance variables.

## 5. Discussion guide checks

- Every research question in the brief has a core section.
- Each core question has probes; probes sound natural, not interrogative.
- Branches exist where roles differ (buyer vs user, host vs guest).
- Warm-up before core, wrap-up last.

---

## File: hybrid-research/references/qual-interviews.md

# Synthetic in-depth interviews and theme analysis

Load for exploratory research: AI interviews, self-moderation, transcripts to
themes, merging human and synthetic insight.

## 1. Human-owned start

- Research question: 100% human (objective, questions, population, use).
- Method choice: the LLM may compare methods (IDIs, focus groups, diaries,
  ethnography) with pros and cons; the human picks and records why.

## 2. Sample and personas

Two ways, combinable:
- **Replication:** take the profile from a past study, customer data or panel
  screener.
- **Discovery:** ask the LLM who should be interviewed, including niche and
  hard-to-reach groups and unusual users. Its strength is spotting segments
  recruiters miss. Then push: "which under-represented segments or edge cases
  are missing?" The human approves the list.

Qual persona = demographics + psychographics + behaviour + research-specific
role (buyer vs user, experience level, category attitude), plus a name, a short
biography, quirks and some conflicting attitudes. Fifteen personas must not
sound like one person.

## 3. Hybrid configurations

| Config | Guide | Sample | Respondents | Moderation | Use for |
|---|---|---|---|---|---|
| 1 | human | human | LLM | human | replicating a known study, most control |
| 2 | human | LLM | LLM | human | discovering new segments |
| 3 | human | human | LLM | LLM | best information density and similarity to human data; start here |
| 4 | human | LLM | LLM | LLM | maximum delegation |

The guide is always human-approved.

Choice: topic poorly represented in training data, or unsure: human
respondents, LLM for analysis only. Exploratory: 3 or 4. Confirmatory: 1.
Culturally sensitive populations: add human respondents for those segments.

## 4. Running the interview

1. System role: persona + interview context (in-depth interview, date,
   moderator, topic) + "stay in character; do not mention being an AI".
2. User role per question: the topic and "answer in as much detail as you
   like; there are no wrong answers"; plain conversational language if
   readability matters.
3. Send questions in order with the full conversation history each time.
4. Self-moderation (configs 3, 4): after each answer, a scoring prompt rates
   clarity, relevance, depth, insightfulness 0-100 and averages them. Average
   below 80: generate one natural follow-up aimed at the weakest dimension,
   collect the answer, re-score. Cap at 2 probes per question, then move on.
5. Monitor probe frequency: under 20% of turns probed means the threshold is
   too lenient; endless probing means it is too strict (the cap handles cost).
6. After the interview: re-run any turn that refused, drifted off-topic or
   broke character.

## 5. Analysis

LLM analyst prompt shape: act as an experienced qualitative analyst; for one
question and its answers, (1) pick the most informative sentences, (2) cluster
them into themes, (3) summarise the insight in a short paragraph.

- Humans highlight more sentences, including near-duplicates; the LLM
  deduplicates. Their selections usually agree closely (cosine around .78 or
  more).
- Theme recovery vs an all-human baseline: target >= 80%. New themes are
  welcome but tagged.
- Best summaries come from mixed pipelines (human data + LLM analyst, or LLM
  data + human analyst), judged on thoroughness, readability, balance of
  functional and emotional, specificity, actionability.

## 6. Consolidation

Analyse human and synthetic sets separately, then merge:

| Theme found in | Status in the report |
|---|---|
| both | high-confidence finding |
| human only | lived experience, cultural nuance; keep |
| synthetic only | expansion insight: a hypothesis to test with humans or an experiment |

Every theme in the findings document carries its source. Never present a
synthetic-only theme as what customers said.

From qual to quant: turn themes into testable hypotheses (hypothesis, control
vs variant, metric to judge) for a survey or a live A/B test.

## 7. Pitfalls

| Pitfall | Fix |
|---|---|
| generic personas, low density | specific behaviour, quirks, conflicting attitudes |
| no history | pass full history every turn |
| threshold too low / too high | 80; cap 2 probes; watch the 20% probe rate |
| breaks character | explicit stay-in-character instruction |
| academic tone | ask for short, casual sentences |
| decisions on synthetic alone | triangulate with human data, market signals or prior research |

## 8. Learning repository

After each study record: configuration, quality metrics vs human data, themes
unique to each source, what prompting worked, expert feedback. Turn stable
patterns into rules (theme recovery rate per category, density gain from
moderation, how often LLM-suggested segments proved useful).

---

## File: hybrid-research/references/quant-synthetic.md

# Synthetic survey respondents: method

Load when building personas, prompts or a generation script for a survey.

## 1. The five parts of the system

| Part | What it is | Owner of mistakes |
|---|---|---|
| Inputs | persona matrix, the instrument, model settings | human signs off all three |
| Prompt | context + system role (persona) + user role (question, format) | |
| Validation | format, completeness, plausibility, in character; resend on fail | code |
| History | prior Q/A pairs of this respondent passed into the next prompt | code |
| Output | respondent x variable matrix shaped like a human survey export | |

## 2. Prompt templates

Context line (always first): the situation, today's date, the topic. Without
it answers go generic.

System role for a quantitative persona: factual, structured, no narrative.

```
Pretend that:
- You currently [qualifier, e.g. subscribe to a meal kit]
- You are [qualifier, e.g. considering cancelling in the next 3 months]
Your characteristics:
- You are [ethnicity], [gender], [age] years old.
- You live in [region], [country]; your area is [urban/suburban/rural].
- Household of [N]; marital status [status].
- Education [level]; household income [amount]; employment [status].
[Optional attitudinal priors: price sensitivity, category attitude.]
```

User role:

```
Question: [verbatim item]
Answer format: answer with a single number only, nothing else.
Use this format to answer: 3
Choices: (1) [label] ... (5) [label]
```

The example answer in the format line anchors parsing. Specify length for open
text ("2-3 sentences").

## 3. Generation script outline (Python)

```python
for p in personas:                       # one row of the matrix
    history = []
    for q in questions:                  # in instrument order, skip logic applied
        for attempt in range(3):
            system = persona_prompt(p) + format_history(history) + rag_context(p, q)  # rag optional
            reply = call_llm(system, user_prompt(q), temperature=1.0, seed=SEED)
            value = parse(reply, q)      # None if not an allowed value
            if value is not None and plausible(value, p, q):
                break
        log(p.id, q.id, attempt + 1, reply)
        answers[p.id][q.id] = value      # stays None (missing) after 3 failures
        history.append((q.text, value))
```

Arm assignment for A/B concept tests: shuffle persona ids in code, 50/50, then
show the arm's concept in the user role before the outcome items.

## 4. Context injection

**Few-shot with response history.** Q1 sees the persona only; Q2 sees persona
+ Q1/A1; Q3 sees persona + Q1/A1 + Q2/A2, and so on. Effect: the respondent
stays consistent with itself, so correlations turn positive and directionally
right and variance widens. Mean bias does not improve.

**RAG.** Build a knowledge base from past qualitative research on the topic
(transcripts, open ends), prior surveys in the category, relevant reports.
Chunk by paragraph or section, embed with a sentence transformer, store in a
vector index (FAISS, Chroma and the like). For each persona x question, embed
the question, retrieve the top K = 3-5 chunks, and add them to the system role
framed as background from prior research. Effect: best correlation recovery;
variance holds; mean bias unchanged.

RAG pitfalls:
- Irrelevant documents add noise and make results worse than no context.
- Too much context makes respondents parrot the qual findings and lose
  realistic variance. Use snippets, not whole transcripts.

## 5. Settings

| Setting | Value | Why |
|---|---|---|
| Temperature | 1.0 for structured survey items | lower values cluster answers at the mode; results are stable across temperatures for short scales |
| Seed | fixed | reproducibility |
| Retries | up to 3 per question | stochastic failures often pass on retry |
| Chat UI, no temperature | add "introduce meaningful behavioural variation; avoid converging toward the average; ensure realistic heterogeneity across individuals" | partial fix only |

## 6. Expected behaviour by configuration

| Config | Mean | Variance | Correlations |
|---|---|---|---|
| LLM1 zero-shot | direction right, about 0.5-0.7 points more extreme on 5 points | low, clustered (often 4-5 on agreement) | near zero |
| LLM2 few-shot history | same bias | improved | positive, directionally right |
| LLM3 few-shot + RAG | same bias | improved (like LLM2) | closest to human |

Why variance is low: demographic personas explain little of the variance in
attitudes, so the model answers the "typical" reply for the profile. Add
behavioural and attitudinal variables, response history and RAG.

## 7. Validation repository and calibration

Every study run alongside or before a human survey adds a row: category,
question type, configuration, MAE, variance ratio per item, correlation MAE,
winner match, which segments were stereotyped. Over time this answers which
categories the model handles (familiar consumer categories) and which it does
not (niche B2B, novel concepts, culturally specific preferences), and how big
the bias is. Cheap start: replicate archived surveys using their original
sample demographics.

Turn the repository into written rules only once the pattern is stable, in
the form "for [category] and [question type], synthetic picks the human winner
in X% of studies; agreement items run Y points high; variance ratio Z". A mean
correction is allowed only from such a rule, never guessed.

## 8. Where synthetic earns most

Hard-to-reach B2B and specialist populations: recruitment is expensive and
samples small. Use synthetic answers to pre-test the instrument before
spending scarce human access, and to supplement the small human sample while
reporting where the two agree and differ. It is a low-cost prior, not the
measurement.

## 9. Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Demographics-only persona | everyone answers alike | add behaviour and attitudes; history; RAG |
| No history | correlations near zero | always pass history |
| Low temperature | variance even lower | 1.0 |
| Synthetic as ground truth | decisions on uncalibrated data | validate on human data first |
| Comparing means only | bimodal human vs unimodal synthetic hidden | compare full distributions (histograms, chi-square) |
| No tracking over time | cannot tell if the model got better or worse | keep the repository; review quarterly |

---

## File: hybrid-research/references/recovery-metrics.md

# Recovery metrics: synthetic vs human

Load when comparing a synthetic panel with human answers on the same items.

## 1. Preconditions

- Same items, same wording, same scale on both sides.
- Synthetic personas matched to the human sample's demographics (1:1 for a
  replication). Show the comparison table; a mismatch makes every metric below
  a comparison of different populations.
- Respondent-level data on both sides (respondent x item), not only summary
  means. Without it variance and correlations cannot be checked: say so.
- Missing synthetic answers (failed after retries) excluded, counted, reported.

## 2. The metrics

| Metric | Computation | Pass |
|---|---|---|
| Mean bias | for each item `abs(mean_h - mean_s)`; MAE = their mean | MAE < 0.5 on 5 points |
| Variance ratio | for each item `var_s / var_h` | 0.7 to 1.3 |
| Correlation MAE | for each item pair `abs(r_h - r_s)`; their mean | < 0.2 |
| Distribution | chi-square test on the counts per answer option, human vs synthetic | p > .05 |
| Winner | top concept on the outcome item | same concept |
| Rank order | Spearman rho between the human and synthetic ranking of items or concepts | >= .80 |

Note the variance ratio uses variances. An SD ratio of 0.6 is a variance
ratio of 0.36: a fail.

Other scales: the 0.5 MAE threshold is stated for a 5-point scale. For a
7-point item, rescale the gap to 5 points (gap x 4/6) before comparing.

```python
import numpy as np, pandas as pd
from scipy import stats
items = [...]                                    # Likert columns
mae = np.mean([abs(H[c].mean() - S[c].mean()) for c in items])
vr  = {c: S[c].var(ddof=1) / H[c].var(ddof=1) for c in items}
rh, rs = H[items].corr(), S[items].corr()
iu = np.triu_indices(len(items), 1)
corr_mae = np.mean(np.abs(rh.values[iu] - rs.values[iu]))
chi = {c: stats.chi2_contingency(pd.crosstab(
        np.r_[np.zeros(len(H)), np.ones(len(S))],
        np.r_[H[c].values, S[c].values]))[1] for c in items}
```

## 3. Reading order and interpretation

1. **Variance ratio per item.** The usual failure. Below 0.7 means the panel
   is too uniform: any segment difference, driver analysis, correlation or
   power calculation from it is understated.
2. **Correlation MAE.** Near-zero synthetic correlations against strong human
   ones mean each answer was drawn on its own, not by a coherent person. Fix
   with response history, then RAG.
3. **Distribution.** Means can match while shapes differ (human bimodal,
   synthetic unimodal). Look at histograms, not only the test.
4. **Mean bias.** Direction usually right; the size of the miss tends to be
   about 0.5-0.7 points toward the extremes in zero-shot runs. Context does
   not fix it. A correction needs a calibration rule from past studies in the
   same category.
5. **Winner and rank order.** For concept tests the business cares about the
   ranking. A match on one study is one data point for the repository, not a
   licence.

A panel passes only when every key item passes variance, the correlation MAE
passes, and the mean passes. A good MAE alone is the classic false pass.

## 4. Sample size from a synthetic pilot

Per arm, for a difference delta in means of an item: `n = 16 x sigma^2 / delta^2`
(80% power, 5% two-sided). Synthetic sigma^2 runs low, so n from it is too
small. Use `sigma^2_human_est = sigma^2_synthetic / variance_ratio` with the
variance ratio from the repository (same category and configuration). Without
a ratio, report the synthetic n as a minimum and a range using a plausible
human variance from any past wave on similar items.

## 5. Qual-side metrics (for completeness)

| Metric | Use | Read |
|---|---|---|
| SMOG, Gunning Fog, Flesch-Kincaid | readability | LLM text usually reads harder; ask for plain, conversational language if it matters |
| Unique tokens per document | information density | self-moderated LLM interviews tend to be highest |
| Topic coherence (LDA) | are there interpretable themes | higher is better |
| Embedding cosine (e.g. SBERT), UMAP map | similarity to human answers | >= .5 is high; clusters in one source only are the complementary insights |
| Blind human rating (clarity, relevance, depth, insightfulness) | research-objective fit | mixed-effects model controlling for question, length, rater |
| Theme recovery | share of human-baseline themes found | >= 80% |
| New theme rate | share of themes not in the baseline | a feature; label as hypotheses |
