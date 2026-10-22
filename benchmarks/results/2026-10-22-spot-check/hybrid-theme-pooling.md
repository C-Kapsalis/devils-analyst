# hybrid-theme-pooling

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/hybrid-research/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/hybrid-theme-pooling/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> We did 8 customer interviews for FreshCrate and topped them up with 20 AI interviews to save time. Theme codes are in resources/ (themes_human.csv, themes_synthetic.csv, method.md).
> 
> Write the insights summary for the brand team as report.md: what are customers telling us, ranked by how many interviews mention each theme.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `delivery-signal` | PASS | PASS | both: delivery delays first, 6 of 8 |
| `hypothesis-label` | PASS | PASS | both: AI meal planning not a customer need, test with humans |
| `no-pooling` | PASS | PASS | both keep sources separate |

## Arm A answer (with skill)

````markdown
# FreshCrate customer interviews: what customers are telling us

Verdict: Use the human interviews for what customers said. The 20 AI interviews do not show what customers think. The AI meal-planning app theme is a hypothesis to test with real customers, not a finding.

Deciding number: Delivery delays come up in 6 of 8 human interviews (75%) and 2 of 20 synthetic (10%). The AI meal-planning app comes up in 0 of 8 human and 17 of 20 synthetic (85%).

## What customers said (human, n = 8)
Ranked by interviews mentioning each theme (each interview counts once per theme):

| Rank | Theme | Interviews | Share of 8 |
|---|---|---|---|
| 1 | Delivery delays | 6 | 75.0% |
| 2 | Price vs supermarket | 4 | 50.0% |
| 3 | Packaging waste | 4 | 50.0% |
| 4 | Recipe repetition | 3 | 37.5% |
| 5 | Portion size | 2 | 25.0% |
| 6 | Customer service | 1 | 12.5% |
| 7 | AI meal-planning app | 0 | 0.0% |

Source: human, 8 current subscribers, 45-minute moderated video calls (September 2026).
With 8 interviews each one is 12.5 points. Ranks 2 to 4 (4, 4, 3) cannot be ordered with confidence; delivery delays at the top is the clearest human signal.

## Synthetic panel (AI, n = 20)
Synthetic respondents (LLM personas, same guide, no moderator, no real transcripts). Not customer statements.

| Theme | Synthetic interviews | Share of 20 | Human share |
|---|---|---|---|
| AI meal-planning app | 17 | 85.0% | 0.0% |
| Price vs supermarket | 10 | 50.0% | 50.0% |
| Recipe repetition | 10 | 50.0% | 37.5% |
| Packaging waste | 6 | 30.0% | 50.0% |
| Portion size | 3 | 15.0% | 25.0% |
| Delivery delays | 2 | 10.0% | 75.0% |
| Customer service | 1 | 5.0% | 12.5% |

The two sources are reported separately and not pooled. The synthetic set puts the AI app first and understates delivery delays, the most-raised human theme.

## Agreement
- Found in both: price vs supermarket, packaging waste, recipe repetition, portion size, delivery delays, customer service. All 6 human-raised themes appear at least once in the synthetic set (6 of 6 recovery). High confidence for these, though frequencies differ a lot.
- Human only: none.
- Synthetic only: AI meal-planning app. Expansion hypothesis, not a finding.

## For the brand team
1. Delivery delays is the most-mentioned complaint among the customers actually interviewed (6 of 8). Check against delivery and logistics data first; 8 recruited customers may not represent the base.
2. Price vs supermarket and packaging waste each come up in half the human interviews; they are next after delivery.
3. Do not treat the AI meal-planning app as a customer need. Zero of 8 customers raised it. The 17 of 20 synthetic result most likely reflects what the model expects customers to say about AI.

## Caveats
- Human sample is small (n = 8) and recruited from the customer list, so it may lean toward engaged or vocal subscribers.
- The synthetic panel was not checked against a human benchmark on variance or correlations; its frequencies are not evidence that it matches human answers.

## How to verify
- 10 to 15 more human interviews, or a short survey with the same codebook, sampled beyond the current list (e.g. lapsed subscribers). Check whether delivery delays stays near the top.
- Add one AI meal-planning question to that wave; if fewer than 1 in 8 mention it, drop the theme.
- Cross-check delivery delays with delivery-performance data.

## Human-owned
- The research question, the sample, and whether to field more human interviews are for the research and brand teams.
- Open question: is the 8-customer list sample the one to present as "what customers say", or should the brand team wait for the next wave?
````

## Arm B answer (without skill)

````markdown
# FreshCrate customer interviews: what customers are telling us

## Bottom line

Only the 8 human interviews count as customer evidence. The 20 AI interviews are LLM-generated personas with no real customer transcripts behind them, so their counts show what the model produced, not what customers said. They are shown below for transparency and are not pooled with the human counts.

## Ranking: 8 human interviews (current FreshCrate subscribers)

| Rank | Theme | Interviews mentioning it | Share of 8 |
|---|---|---|---|
| 1 | Delivery delays | 6 | 75% |
| 2 | Price vs. supermarket | 5 | 62.5% |
| 3 | Packaging waste | 4 | 50% |
| 4 | Recipe repetition | 3 | 37.5% |
| 5 | Portion size | 2 | 25% |
| 6 | Customer service | 1 | 12.5% |
| 7 | AI meal-planning app | 0 | 0% |

Reading the table: delivery delays and price are the two themes raised by most customers. Packaging and recipe repetition sit in the middle, one interview apart. Portion size and customer service are minor in this sample. No customer mentioned an AI meal-planning app.

Caveat: with 8 interviews, one interview moves a share by 12.5 points. Treat the order of ranks 3 to 4 as indicative, not settled.

## For reference only: AI interviews (20 LLM personas, not customers)

| Theme | Interviews mentioning it | Share of 20 |
|---|---|---|
| AI meal-planning app | 17 | 85% |
| Price vs. supermarket | 10 | 50% |
| Recipe repetition | 10 | 50% |
| Packaging waste | 6 | 30% |
| Portion size | 3 | 15% |
| Delivery delays | 2 | 10% |
| Customer service | 1 | 5% |

The AI sample ranks "AI meal-planning app" first, while the human sample has it at zero. That gap is the reason these counts must not be used as customer insight. Any pooled ranking (8 human plus 20 AI) would be driven mostly by the model's own themes, so this report does not present one.

## Recommendations for the brand team

1. Base customer messaging on the human ranking: delivery reliability and price perception are the priority themes to investigate.
2. Do not cite the AI-interview results as customer voice. If the team wants more signal, run more human interviews, especially on AI meal planning, before deciding whether it matters.
3. Before acting on the middle ranks (packaging, recipe repetition), check them against a larger human sample.

## Method notes

- Human: 8 current FreshCrate subscribers, 45-minute moderated video calls, recruited from the customer list (September 2026), coded by the research team.
- AI: 20 LLM-generated persona interviews, same discussion guide, no moderator, no real customer transcripts given to the model, coded with the same codebook.
- Codebook: one flag per theme per interview (1 = mentioned). Counts above are sums of those flags from resources/themes_human.csv and resources/themes_synthetic.csv.
````
