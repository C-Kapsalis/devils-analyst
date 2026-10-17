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
