---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: before the announcement (5 Jan - 18 Feb) sales averaged 397 boxes/day. After the 19 Feb email, customers stocked up at the old price (19-28 Feb averaged 621/day, about 2,234 extra boxes). In early March sales dipped while customers used that stock (about 1,523 boxes below the settled level over 1-21 Mar), then settled at 382/day from 29 Mar onward.

Naive answer: comparing the 14 days before 1 March (554/day, inflated by stock-up) with the 14 days after (285/day, depressed by the dip): -49% units, implied elasticity about 4.9. Also naive: February vs March monthly averages (473 vs 334/day).

PASS if report.md identifies the late-February spike as stock-up / forward buying ahead of the increase (triggered by the announcement) and the early-March dip as its after-effect, AND measures the price effect against a pre-announcement baseline (before 19 Feb) and a settled post period (late March/April).
FAIL if report.md measures the effect by comparing the weeks/days or months immediately either side of 1 March, or does not recognise the stock-up.
