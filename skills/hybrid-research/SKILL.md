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
