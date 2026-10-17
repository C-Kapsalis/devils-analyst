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
