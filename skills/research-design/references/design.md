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
