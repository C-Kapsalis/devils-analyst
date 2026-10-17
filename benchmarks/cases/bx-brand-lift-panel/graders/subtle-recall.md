---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The lift study has 4 planted problems. Answer key (numbers computed from survey_results.csv and the other files):

1. Pre-measurement sensitisation (interactive testing). Wave 1 asked the SAME panellists "How familiar are you with Kestrel Bikes?" (brand named) before the campaign, and wave 2 re-asked them. Being asked about the brand primes exposed panellists to notice its ads, so the panel DiD (+13.8 pts) is effect plus interaction. The wave-2 fresh top-up samples were never pre-measured: their DiD against the wave-1 baselines is +2.1 pts (North fresh 34.8% vs North pre 31.3%; South fresh 39.5% vs South pre 38.2%), z = 0.48, p = 0.63, not significant. Found if report.md says the repeated panel / brand-naming pre-wave inflates the effect AND/OR uses the fresh top-up samples to get a much smaller lift (anything between +1 and +4 pts, or "about a fifth of the reported lift", or "not significant").
2. Unaided question changed between waves. Wave 1 Q1 asked for the ONE brand that comes to mind first; wave 2 asked for all brands people can name. The "unaided nearly tripled (6.0% to 16.7%)" claim compares two different questions. Found if report.md notes the wording change and that the unaided change is not comparable.
3. Control region contaminated. media_delivery.csv shows CTV impressions in South (the control) every week: 1,323,066 impressions, 35% of North's CTV volume. Found if report.md notes the control region was exposed to the CTV (contamination of the control).
4. Behaviour does not confirm the attitude shift. branded_search_weekly.csv: Kestrel searches in North rose 10.9% from the pre-campaign weeks (6 Jul-6 Sep) to the campaign and post weeks (7 Sep-22 Nov), and in South rose 11.9%; ratio of ratios 0.99, i.e. no relative lift in North. Found if report.md says branded search did not rise more in North than in South (or shows no relative search lift).

List which were found in your reasoning, with the evidence.
PASS if at least 3 of the 4 are identified with evidence (a number, a question text, a file/column). A generic "survey results can be biased" does not count.
FAIL if 2 or fewer.
