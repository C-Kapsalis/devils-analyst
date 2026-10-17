---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three problems are Must-fix (deliverability and reputation, which every other email number depends on):
- A. DKIM failing and DMARC missing.
- B. Dormant contacts mailed inside the September newsletter (bounce 3.4%).
- C. Flash Sale 48h complaint rate 0.157%, above 0.1%, hidden in an August average of 0.072%.
The lesser problems are: negative net list growth, the revenue-based CLV, the win-back exit rule and the utm_campaign name mismatch.

PASS if report.md flags A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND the closing "fix first" line (or explicit first priority) names one of A, B or C.
FAIL if A, B or C is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the first priority named is something other than A, B or C.
