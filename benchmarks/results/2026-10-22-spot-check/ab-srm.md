# ab-srm

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/evidence-check/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/ab-srm/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Here are the results of our homepage hero test for Harbor Outdoor. The test setup is in resources/experiment_config.json and the results export is resources/ab_results.csv (variant, users, conversions, revenue).
> 
> Which version should we go with? Write report.md with the result and your recommendation.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `srm-detected` | PASS | PASS | both flag 52,000 vs 47,000 against 50/50, chi-square about 252, result unreliable |
| `recommendation` | PASS | PASS | both: do not ship B, investigate the split first |

## Arm A answer (with skill)

````markdown
# Homepage hero test (Harbor Outdoor): which version to ship

Recommendation: do not ship B on this result. Keep A (product grid) live and fix the test first.

Verdict: inconclusive. The split is broken (sample ratio mismatch), so the result cannot be trusted whatever its p-value.

## Naive read and why it is wrong
Naive read: B converts 8.0% better (3.24% vs 3.00%), p = 0.03, so ship B.
The test was planned 50/50, but the export shows 52,000 users in A and 47,000 in B. With 99,000 total, the planned split is 49,500 per arm. That mismatch is too large to be chance, so assignment or logging is broken.

## Checks
Experiment hp_hero_2026_09, 2026-09-07 to 2026-09-27 (21 days), unit = user, primary metric = purchase conversion rate.

1. Sample ratio: expected 49,500 per arm. A: (52,000 - 49,500)^2 / 49,500 = 126.26; B: (47,000 - 49,500)^2 / 49,500 = 126.26. Chi-square = 252.53 (1 df), far above 10.8 (p < 0.001). FAILS. Split is 52.5% / 47.5%.
2. Significance (reference only, invalid until check 1 passes): A rate 1,560 / 52,000 = 3.000%; B rate 1,523 / 47,000 = 3.240%; lift +0.240 pp (+8.0% relative); pooled p = 3,083 / 99,000 = 3.114%; se = 0.1106 pp; z = 2.17; two-sided p = 0.030. 95% CI for the difference: +0.02 pp to +0.46 pp (+0.8% to +15.3% relative).
3. Power: MDE at 80% power, 5% two-sided, about 2.8 x sqrt(2 x 0.031 x 0.969 / 50,000) = 0.31 pp absolute (about 10% relative). The observed 0.24 pp is below the MDE, so a significant result at this size would tend to overstate the effect (winner's curse).
4. Novelty (weekly, new vs returning): not in the export.
5. Segments (device etc.): not in the export.

Secondary metric, revenue per user (untested, no variance in export): A 110,702.64 / 52,000 = 2.13; B 109,753.10 / 47,000 = 2.34 (+9.7%). Total revenue is lower in B (109,753 vs 110,703) because B has fewer users. Per-user is the fair comparison but sits on the same broken split with no interval.

## What to do
1. Investigate the split before anything else: assignment/bucketing logic, bot and internal-traffic filters that may hit one arm, redirects or caching sending one variant elsewhere, variant logging coverage. Check mobile and desktop separately to locate the mismatch.
2. Keep A live. Nothing here shows B is better.
3. Re-run after the fix, sized for the smallest lift worth acting on. To detect +0.24 pp at 80% power (5% two-sided) needs about 84,000 users per arm (about 170,000 total), roughly 36 days at the test's traffic of about 4,700 users per day.
4. Pre-register the primary metric, MDE, planned split and decision rule; check the sample ratio daily during the run.

Data used: resources/experiment_config.json (planned 50/50, metrics, dates); resources/ab_results.csv (A: 52,000 / 1,560 / 110,702.64; B: 47,000 / 1,523 / 109,753.10). Arithmetic done by hand; figures rounded.
````

## Arm B answer (without skill)

````markdown
# Homepage hero test (hp_hero_2026_09): Harbor Outdoor

## Recommendation

Do not ship either version yet. Variant B (lifestyle photo) looks better on the numbers, but the traffic split is far from the 50/50 the test was configured for. That points to a broken assignment or logging problem, and until it is explained the result cannot be trusted. Investigate the split first. If the cause is found and fixed, and the conversion lift holds in a clean rerun or re-analysis, ship B.

## Test setup

- Experiment: Homepage hero, lifestyle photo (B) vs product grid (A)
- Run: 2026-09-07 to 2026-09-27 (21 days), all desktop and mobile visitors landing on `/`
- Unit: user; configured allocation 50/50
- Primary metric: purchase conversion rate. Secondary: revenue per user

## Results

| Variant | Users | Conversions | Conversion rate | Revenue | Revenue per user | Revenue per conversion |
|---|---|---|---|---|---|---|
| A (product grid) | 52,000 | 1,560 | 3.00% | 110,702.64 | 2.13 | 70.96 |
| B (lifestyle photo) | 47,000 | 1,523 | 3.24% | 109,753.10 | 2.34 | 72.06 |

- Conversion rate: B is +0.24 percentage points, about +8.0% relative to A.
- 95% confidence interval for the difference: roughly +0.02 to +0.46 points (+0.8% to +15.2% relative).
- Two-proportion z-test: z is about 2.17, two-sided p is about 0.03. This would pass the usual 0.05 threshold if the data were sound.
- Revenue per user: B is about +9.7% relative to A (2.34 vs 2.13).
- Revenue per conversion: B is about 1.5% higher, so the revenue gain comes mostly from more conversions, not larger baskets.

## Sample ratio mismatch

Users split 52,000 : 47,000 (52.5% A, 47.5% B). With 99,000 users and a 50/50 allocation, each variant should have about 49,500. The chi-square statistic is about 252 on 1 degree of freedom, so p is far below 0.001. A split this skewed almost never happens by chance with correct randomisation. Likely causes include a bug in assignment, redirects or bot filtering that drop users differently by variant, or a tracking difference between the two pages. An SRM this large means the conversion comparison may be biased, so the p-value above should not be relied on.

## Next steps

1. Find the cause of the 52/47 split: compare assignment logs with analytics counts per variant, check whether bots or redirects are filtered differently, and confirm both pages fire the same events.
2. Fix the cause, then rerun the test (or re-analyze from clean logs) with the 50/50 split confirmed.
3. If the rerun still shows B ahead on conversion with the split fixed, ship B and track revenue per user as the secondary check.

Note: the arithmetic was done by hand, so the p-value and confidence interval are approximate.
````
