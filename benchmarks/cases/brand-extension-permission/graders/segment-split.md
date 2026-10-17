---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: overall purchase intent 6.33 (n=1,000). By customer status: core customers (n=400) intent 4.2, brand fit 3.9; lapsed (n=150) intent 5.9, fit 5.5; non-customers (n=450) intent 8.3, fit 6.8. Existing customers (core + lapsed) average 4.7, below the 6.0 line. The 6.3 average is carried by non-customers (81% aged 18-29, mostly energy-drink buyers) vs core customers who are mostly 35+ (10% aged 18-29).

Naive answer: "6.3 > 6.0, launch as Calder Energy".

PASS if report.md splits intent (or fit) by customer status, reports core-customer intent (about 4.2, within 0.3) and/or fit (about 3.9) below the go line, and notes the average is carried by non-customers.
FAIL if report.md approves launching under the Calder name based on the 6.3 average, or does not split by customer status.
