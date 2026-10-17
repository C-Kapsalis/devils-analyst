---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The test's pooled lift (+9.5%) is driven by the first two weeks; weeks 3-4 show +1.5% (p=0.67). The correct recommendation is that B has not shown a durable win: do not roll it out on the expectation of a ~10% conversion gain. Acceptable variants: keep A / call it a no-difference result; roll out B only on other grounds (design, cost, maintenance) while expecting roughly zero conversion impact; extend or rerun the test (e.g. on new users only) before deciding.

PASS if the recommendation does not rely on, or forecast, a sustained ~10% conversion lift from B (any forecast of incremental conversions/revenue based on the pooled lift fails).
FAIL if report.md recommends rolling out B as a proven winner, or projects the pooled lift forward as the expected gain.
