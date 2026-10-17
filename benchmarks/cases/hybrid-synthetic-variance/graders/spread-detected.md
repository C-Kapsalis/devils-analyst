---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: item means are close (mean absolute difference 0.31 points; 7/8 items on the same side of the scale midpoint), BUT the synthetic answers are far less spread out. Item SDs human vs synthetic: q1 1.10 vs 0.61, q2 1.15 vs 0.73, q3 1.11 vs 0.68, q4 1.15 vs 0.63, q5 1.21 vs 0.67, q6 1.12 vs 0.62, q7 1.17 vs 0.66, q8 1.14 vs 0.65. Variance ratio (synthetic / human) is 0.30-0.41 on every item (mean 0.33), far outside an acceptable ~0.7-1.3 band.

Naive answer: "means differ by only ~0.31 points and direction matches, so the synthetic panel tracks the human one".

PASS if report.md compares variance or SD between human and synthetic data (any form) AND says the synthetic spread is much lower (roughly a third of human variance, or SDs about half or less).
FAIL if report.md judges the match on means / direction only, or calls the spread similar.
