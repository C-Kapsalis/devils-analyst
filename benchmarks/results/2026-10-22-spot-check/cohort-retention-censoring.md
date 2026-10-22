# cohort-retention-censoring

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/metric-definitions/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/cohort-retention-censoring/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> The resources/ directory has our subscriber cohort export from the Lumen Streaming billing system, cohorts.csv (cohort_month, cohort_size, month_offset, active_subscribers). It was exported on 1 October 2026.
> 
> What's our average month-3 and month-6 retention across cohorts, and is retention getting better or worse? Write report.md with the numbers and what you conclude.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `observed-only` | PASS | PASS | both 52.5%/52.0% and 34.9%/34.8%, zeros treated as unreached |
| `trend` | PASS | PASS | both: improving, same-offset comparison |

## Arm A answer (with skill)

````markdown
# Cohort retention, Lumen Streaming (export 1 October 2026)

## Answer

- **Month-3 retention:** 52.5% pooled across the six cohorts old enough to observe it (Jan to Jun 2026): 5,077 active of 9,663 subscribers. The simple mean of the six cohort rates is 52.0%. Cohorts run from 48.1% (Jan) to 56.5% (Jun).
- **Month-6 retention:** 34.9% pooled across the three cohorts old enough (Jan to Mar 2026): 1,416 active of 4,053. The simple mean is 34.8%. Cohorts run from 33.0% (Jan) to 36.8% (Mar).
- **Trend: getting better.** Month-3 rises in every cohort: Jan 48.1%, Feb 48.9%, Mar 50.8%, Apr 52.4%, May 55.3%, Jun 56.5%. Month-6 also rises across the three cohorts that have reached it: 33.0%, 34.7%, 36.8%.

## Method

- **Censoring.** In cohorts.csv, zeros after a cohort's last observed month are not churn. They are months not yet reached at the 1 October export. Observed offsets are 0 to 8 for Jan, 0 to 7 for Feb, 0 to 6 for Mar, 0 to 5 for Apr, 0 to 4 for May, 0 to 3 for Jun, 0 to 2 for Jul, 0 to 1 for Aug and 0 only for Sep. Every observed count is positive, so no observed cell is a true zero.
- **Eligibility.** Month-3 uses the six cohorts with offset 3 observed (Jan to Jun). Jul, Aug and Sep are excluded. Month-6 uses Jan, Feb and Mar only. Apr, which reaches offset 5 at most, is excluded.
- **Weighting.** The headline is pooled: total active at the offset divided by total cohort size, so larger cohorts count for more. The simple mean is shown beside it as a check.

## Why a naive read misleads

Treating the zeros as churn gives month-3 of 29.6% (5,077 of 17,139 across all nine cohorts) and month-6 of 8.3% (1,416 of 17,139). Both figures are wrong: they count unreached months as lost subscribers. A reader who saw these would think retention had collapsed, when every observed cohort is improving.

## What this does not show

- **Why retention is improving is not in this file.** There is no channel, plan, price or promotion column, so no cause can be tested. Possible explanations include product changes, a shift in acquisition mix or a change in promotions. Each is a hypothesis until a split by those dimensions is run.
- **Cohort sizes grew about 1.7 times from Jan (1,223) to Jun (2,082).** If recent cohorts came from discounted or trial-led acquisition, that could mix in lower-quality subscribers. It is a check to run, not a finding.
- **Month-6 rests on three cohorts.** Treat it as directional until Apr and May reach offset 6.
- **Offsets are calendar months.** If "month" in the billing system is a billing cycle rather than a calendar month, the offsets need re-checking against the billing calendar.

## Next steps

1. Split month-3 retention by acquisition channel, plan and any promotion code, if those exist in the billing export.
2. Re-run month-6 when the Apr and May cohorts reach offset 6, in early 2027.
3. Report retention as the pooled, eligible-cohort figure above, with the cohort counts and sizes shown beside it.
````

## Arm B answer (without skill)

````markdown
# Subscriber retention: month 3 and month 6, and the trend

Source: `resources/cohorts.csv` (Lumen Streaming billing export, 1 October 2026). Retention at offset k = `active_subscribers` at `month_offset` k divided by `cohort_size`.

## Censoring: the zeros are not churn

The export only covers months that have ended. The last full month before the export is September 2026. A cohort's offset k is observed only if cohort month + k is September 2026 or earlier. Every zero in the file falls after that point. For example, the 2026-02 cohort has offset 8 at 0, and February + 8 is October, which has not happened yet. The same holds for every trailing zero in the file.

So each cohort's observed window ends where its nonzero values end. I counted only observed offsets. Treating those zeros as churn would show month-3 retention of 34.7% and month-6 of 11.6%, which is wrong.

## Month-3 retention

Six cohorts (January to June 2026) have an observed month 3.

| Cohort | Size | Active at month 3 | Retention |
|---|---|---|---|
| 2026-01 | 1,223 | 588 | 48.1% |
| 2026-02 | 1,377 | 673 | 48.9% |
| 2026-03 | 1,453 | 738 | 50.8% |
| 2026-04 | 1,662 | 871 | 52.4% |
| 2026-05 | 1,866 | 1,031 | 55.3% |
| 2026-06 | 2,082 | 1,176 | 56.5% |

- Simple average across the six cohorts: **52.0%**.
- Pooled (total active over total size, 5,077 / 9,663): **52.5%**.

## Month-6 retention

Three cohorts (January to March 2026) have an observed month 6.

| Cohort | Size | Active at month 6 | Retention |
|---|---|---|---|
| 2026-01 | 1,223 | 404 | 33.0% |
| 2026-02 | 1,377 | 478 | 34.7% |
| 2026-03 | 1,453 | 534 | 36.8% |

- Simple average across the three cohorts: **34.8%**.
- Pooled (1,416 / 4,053): **34.9%**.

## Is retention getting better or worse?

Better. Month-3 retention rises with every newer cohort, from 48.1% to 56.5%. Month-6 retention rises across the three cohorts that have reached it, from 33.0% to 36.8%. Month 1 tells the same story: 62.6%, 62.3%, 64.2%, 65.5%, 65.9%, 67.1%, 70.2% (July), 70.9% (August) across the eight cohorts with an observed month 1.

## Caveats

- Only six month-3 points and three month-6 points. The trend is consistent, but the sample is small, and I have not tested it for statistical significance.
- Each cohort is observed in a different calendar period, so product, pricing or seasonal changes are mixed into the cohort trend and cannot be separated from it with this file.
- I assumed `month_offset` counts months after the cohort's first month, with offset 0 as the start.
- Cohort sizes grow every month (1,223 in January to 2,718 in September), so the most recent cohorts carry the largest weight in any pooled figure.
````
