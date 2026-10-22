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
