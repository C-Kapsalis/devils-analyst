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
