---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two problems are Must-fix (measurement integrity, which every return figure depends on):
- A. Meta + Google claimed revenue (€201,945) added together although it exceeds Shopify's total (€139,839).
- B. PMax conversions mix newsletter sign-ups with purchases (785 of 1159) and 67% of PMax purchases are brand queries with no brand exclusion.
The lesser problems are: CTR on all clicks, prospecting creative fatigue, and the retargeting audience settings. (The attribution-window mismatch may be ranked anywhere.)

PASS if report.md flags A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND the closing "fix first" line (or explicit first priority) names A, B, or the attribution-window mismatch.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the first priority named is one of the lesser problems.
