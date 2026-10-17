---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

This report is correct. Every figure recomputes from the exports: rates are totals divided by totals, conversions are purchases only, brand and generic are split, comparisons are to the prior week and the same week last year, causal statements are hedged, and each recommendation names the metric and the date to check.

PASS if report.md's verdict says the report can be sent (as is, or with optional wording or presentation changes), and it raises no finding that a number is wrong or that a conclusion does not follow from the data (no Must-fix / critical / blocking finding about the numbers or the conclusions).
FAIL if the verdict says not to send it, or says it must be fixed first, or report.md lists any Must-fix / critical problem.
