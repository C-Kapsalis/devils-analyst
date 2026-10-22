# Spot check, 2026-10-22

A first look at the two groups the breadth run did not cover: 13 of the 62
focused trap cases and 4 of the 12 audits and reviews. It is a small,
hand-graded sample. Read it as a smoke test of the skills, not as a
measurement of how much they help.

## Method

- **Cases.** 13 focused cases, at least one per skill that has a focused
  case (two for `metric-definitions`), and 4 audit or review cases (two
  audits, one flawed review, the clean control). Chosen by me before any
  run, to spread across skills; not chosen by difficulty.

  | Case | Skill read by arm A |
  |---|---|
  | `ab-srm` | evidence-check |
  | `email-mix` | whats-changed |
  | `ga4-users` | metric-definitions |
  | `cohort-retention-censoring` | metric-definitions |
  | `pricing-discount-break-even` | pricing-promotions |
  | `channel-seo-keyword-focus` | channel-audit |
  | `product-npv-share-of-sam` | product-decisions |
  | `models-price-elastic-underpriced` | marketing-models |
  | `hybrid-theme-pooling` | hybrid-research |
  | `research-concept-survey-audit` | research-design |
  | `dashboard-email` | marketing-dashboard |
  | `seo-category-decline` | diagnose |
  | `brand-search-share` | brand-health |
  | `audit-ga4-utm` | audit |
  | `audit-email-crm` | audit |
  | `review-ab-test-readout` | review |
  | `review-clean-control` | review |

- **Fixtures.** Each case's `scaffold.sh` wrote the exports into a fresh
  folder per arm, so both arms saw byte-identical data.
- **Arms.** Two Claude Haiku subagents per case (the `haiku` model of
  Claude Code's Agent tool), one run each:
  - **A, with the skill:** read `hooks/core.md`, then the skill's
    `SKILL.md`, then the references that `SKILL.md` names for the job, then
    answered the case prompt.
  - **B, without:** the same prompt and data, told to read nothing else.
  - Both: Read and Grep only (Glob where the host offered it), no Bash and no
    code, arithmetic by hand. Neither arm could read `benchmarks/`.
- **Output.** The host would not let a subagent write files, so each arm
  handed back its report as text and I saved it as written. I removed only
  the arm's one-line note that the write had been refused. The answers are
  in the case pages below, verbatim.
- **Judge.** I graded every answer against the case's `graders/*.md` as
  written, PASS or FAIL, with a one-line reason per grader. The
  `skill-fired` grader does not apply (no plugin was loaded), so 48 graders
  were scored per arm.
- **Skill fixes and re-runs.** For every grader the skill arm failed, I
  looked for the gap in the skill text, fixed the general rule (never the
  case's specifics), and re-ran that case's arm A once on the fixed skill.
  The table shows both the first run and the re-run; the totals below are
  the first runs only. The tool restriction and the hand-back instruction
  were tightened after the first batch of arms (they had also been offered
  Write, which the host refused); the data, prompts and skills they read
  were the same.

## Results (first runs, before any skill change)

| Case | Graders | A passed | B passed |
|---|--:|--:|--:|
| `ab-srm` | 2 | 2 | 2 |
| `email-mix` | 5 | 4 | 3 |
| `ga4-users` | 1 | 1 | 1 |
| `cohort-retention-censoring` | 2 | 2 | 2 |
| `pricing-discount-break-even` | 3 | 3 | 3 |
| `channel-seo-keyword-focus` | 2 | 2 | 2 |
| `product-npv-share-of-sam` | 2 | 2 | 2 |
| `models-price-elastic-underpriced` | 2 | 2 | 2 |
| `hybrid-theme-pooling` | 3 | 3 | 3 |
| `research-concept-survey-audit` | 3 | 3 | 3 |
| `dashboard-email` | 5 | 5 | 2 |
| `seo-category-decline` | 3 | 2 | 2 |
| `brand-search-share` | 3 | 3 | 3 |
| `audit-ga4-utm` | 3 | 3 | 1 |
| `audit-email-crm` | 3 | 2 | 2 |
| `review-ab-test-readout` | 3 | 2 | 1 |
| `review-clean-control` | 3 | 3 | 1 |
| **Focused (13 cases)** | 36 | 34 | 30 |
| **Audits and reviews (4 cases)** | 12 | 10 | 5 |
| **All (17 cases)** | 48 | 44 | 35 |
| Cases where every grader passed | 17 | 13 | 10 |

Where the arms differed:

- **Only A passed:** `email-mix` decomposition and verifiable actions,
  `dashboard-email` bridge, hypotheses and mix-vs-rate, `audit-ga4-utm`
  must-fix-first and decoys, `review-ab-test-readout` must-fix-first,
  `review-clean-control` called-clean and no-false-findings.
- **Only B passed:** `email-mix` no-open-rate-headline.
- **Both failed:** `seo-category-decline` demand-not-seo,
  `audit-email-crm` must-fix-first, `review-ab-test-readout`
  decoys-left-alone.

On the clean control, B asked for three changes before the report could be
sent; A said "Send it." On the easy single-trap cases (sample ratio, summed
users, censored cohorts, discount break-even, sunk cost, synthetic pooling)
both arms passed: the model already knows those traps when the prompt sits
next to them.

## What the failures changed in the skills

| Failing grader (arm A) | Gap found in the skill | Change | Re-run of arm A |
|---|---|---|---|
| `email-mix` / no-open-rate-headline | `whats-changed` listed open rate as a ratio to decompose with no caveat, and its worked example was an email VIP segment much like this case | New rule: opens are a weak driver, caveat them beside the number and never verify an action on them. Worked example moved to paid search | PASS (5 of 5) |
| `seo-category-decline` / demand-not-seo | `diagnose` told the model to "rule out measurement before behaviour" and had no step for "did the whole market move?" | New step: market or us first; when competitors, category and impressions at flat position all moved together, lead with lower demand and verify with last year | PASS (3 of 3) |
| `review-ab-test-readout` / decoys-left-alone | `review` said "no number, no finding" but did not say where a doubt the data cannot settle goes | New rule: such a doubt is a question under "Not checked", with no group, fix or effect on the verdict | PASS (3 of 3) |
| `audit-email-crm` / must-fix-first | `audit` ranked within a tier by money alone, so a one-decision finding outranked a sender-reputation finding; and a hygiene leak stayed tier 2 even after it had pushed a send's bounces far past the account's norm | First fix: within a tier, upstream first (delivery before rates on delivered mail, the conversion before CPA), then money. Second fix: a leak that is already doing damage takes the damage's tier | First re-run FAIL (complaints moved up, the dormant send still sat after CLV); after the second fix, second re-run PASS (3 of 3) |

The audit skill's tier-1 example list had named this benchmark's planted
problems almost one for one ("retention at 2 months", "UTM keys split"). It
now describes the classes instead, and points to the tier column of each
area's check table as the source.

## Limits

- **Small.** 17 cases out of 74 in these two groups, one run per arm. One
  run moves a case from pass to fail. The 44 against 35 gap is nine graders,
  and five of them sit in two cases (`dashboard-email` and the clean
  control).
- **Author as judge.** I wrote the skills, the cases and the graders, and I
  graded the answers, knowing which arm was which. Some calls were close
  and are marked "borderline" in the case pages; a different judge could
  flip them. No second grader has checked these grades.
- **Haiku as a subagent, not the plugin.** Arm A read the skill files it
  was pointed to; it did not choose a skill through the plugin's hook and
  `Skill` tool, so this does not test routing. Arm B was told not to read
  the skills; it had no plugin to ignore.
- **No code.** Neither arm could run code, so both did arithmetic by hand.
  The skills tell the model to compute in code; in a real session it can.
- **Re-runs prove little.** Each fixed case was re-run once on the skill
  arm only (`audit-email-crm` twice, because the first fix was not
  enough). A pass after a fix shows the rule can be followed, not that it
  raises the pass rate. The four re-run cases have now been seen by the
  person who wrote the fix.

## Case pages

One page per case, with the prompt, the grades and both answers:
[ab-srm](ab-srm.md), [email-mix](email-mix.md), [ga4-users](ga4-users.md),
[cohort-retention-censoring](cohort-retention-censoring.md),
[pricing-discount-break-even](pricing-discount-break-even.md),
[channel-seo-keyword-focus](channel-seo-keyword-focus.md),
[product-npv-share-of-sam](product-npv-share-of-sam.md),
[models-price-elastic-underpriced](models-price-elastic-underpriced.md),
[hybrid-theme-pooling](hybrid-theme-pooling.md),
[research-concept-survey-audit](research-concept-survey-audit.md),
[dashboard-email](dashboard-email.md),
[seo-category-decline](seo-category-decline.md),
[brand-search-share](brand-search-share.md),
[audit-ga4-utm](audit-ga4-utm.md), [audit-email-crm](audit-email-crm.md),
[review-ab-test-readout](review-ab-test-readout.md),
[review-clean-control](review-clean-control.md).
