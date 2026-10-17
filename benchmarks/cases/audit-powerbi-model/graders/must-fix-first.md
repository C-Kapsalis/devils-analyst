---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three problems are Must-fix because every page that uses them shows a wrong number by default:
- A. CTR as AVERAGE of the ctr column (3.77% vs true 1.60%).
- B. Email List Size summing a daily snapshot (556,869 vs 18,699).
- C. Revenue Basis toggle defaulting to Gross instead of the agreed Net (€91,066 vs €67,162).
The lesser problems are Paid ROAS on platform claims, the duplicate CAC (Exec), and Monthly Users summed.

PASS if report.md flags A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND its closing "fix first" line (or explicit first priority) names one of A, B or C.
FAIL if any of A, B, C is missing, labelled lower severity (Should fix, Nice to have), or listed after one of the lesser problems, or if the first fix named is something else.
Note: also placing Paid ROAS or CAC (Exec) in Must fix is acceptable, as long as A, B and C are there and not ranked below them.
