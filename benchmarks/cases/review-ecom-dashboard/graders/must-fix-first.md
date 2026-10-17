---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two of the problems are Must-fix because the founders will act on them:
- A. The bar chart's y axis starts at 3,100, so Email ($3,462) looks about twice Paid Social ($3,275) when the gap is 6%; the headline and the budget shift rest on it.
- B. Average order value $217 is the mean including 5 wholesale orders; the typical (median) order is about $58, so the $200 free-shipping threshold is set on a typical order that does not exist.
The lesser problems are: the TikTok tile with no volume, the cumulative year-to-date line, the paid-filtered Google share, and the 9-slice pie.

PASS if report.md flags both A and B and places each in its highest-severity group (Must fix, critical, or equivalent), or, if it uses no groups, lists both among its first three findings; other problems may share that group. The verdict must not say the dashboard can be sent as is.
FAIL if A or B is missing, is labelled lower severity (Should fix, Nice to have, minor) than any of the lesser problems, or if the verdict approves sending it unchanged.
