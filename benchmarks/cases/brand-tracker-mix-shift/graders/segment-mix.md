---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: total brand score 7.33 (2025) -> 7.29 (2026), flat. By segment: core 8.24 -> 7.07 (n 600 -> 360); occasional 7.01 -> 6.87 (n 360 -> 360); new_promo 5.54 -> 7.78 (n 240 -> 480). The core segment fell about 1.2 points (t about 12, clearly not noise). The respondent mix shifted from 50% core / 20% new_promo to 30% core / 40% new_promo, and new_promo respondents rate the brand higher this year, so the total stayed flat. Holding the 2025 mix fixed, the score falls 7.33 -> 7.15.

Naive answer: "score stable at 7.3, the brand is healthy".

PASS if report.md splits the score by segment, reports the core segment's decline (about 8.2 -> 7.1, within 0.2) AND explains the flat total as a change in respondent mix / growth of the new_promo segment.
FAIL if report.md concludes the brand is healthy or stable based on the total score, or does not report the core decline.
