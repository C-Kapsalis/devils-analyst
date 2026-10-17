---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The 10 rewritten ad groups were selected because they had the worst CPA in the week of 2026-08-17, a single week with only 2–6 conversions per ad group, so that week was mostly bad luck.
Ground truth:
- Rewritten ad groups: CPA 79.94 in week 2026-08-17 -> 34.25 after the change (2026-08-24 to 2026-09-14 (4 weeks)): 57% "improvement". This is the naive answer.
- Their CPA in the 6 weeks BEFORE week 2026-08-17 was 34.90, i.e. after the rewrite they are simply back to their normal level (-2% vs that earlier baseline).
- Placebo with the same selection rule: the 10 worst-CPA untouched ad groups in the week of 2026-08-10 (not rewritten) went from CPA 81.35 to 34.86 over the following 4 weeks, a 57% improvement with no change at all. Difference-in-differences vs the rewritten group: +0 percentage points, i.e. about zero.
- The next 10 worst in week 2026-08-17 (ranks 11–20, not rewritten, slightly less extreme): CPA 52.47 -> 29.10, 45% improvement with no change. (A residual gap of ~13 points vs this group is expected because they were less extreme in the selection week, not evidence of an effect.)

PASS if report.md concludes the rewrite had little or no measurable effect (or that the improvement cannot be attributed to the rewrite) because comparable untouched ad groups improved about as much and/or the rewritten ad groups were just returning to their earlier CPA (regression to the mean / selection on a bad week).
FAIL if it credits the rewrite with a ~57% (or any substantial) CPA improvement, e.g. "the rewrite cut CPA by 57%".
