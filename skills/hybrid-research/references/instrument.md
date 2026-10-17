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
