---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Q3 2026 orders (sum of orders_q3.csv): 6,909.
Ground truth cost per order = paid media EUR / orders = 84,522.90 / 6,909 = 12.23 EUR.
Wrong values: 37.43 (every row summed), 14.80 (agency/contractor fees counted as media), 11.62 (Meta left in GBP).

PASS if report.md states a media cost per order within 2% of 12.23 EUR. A separate fully-loaded figure including the manual expenses (14.80) is fine as long as it is labelled as including fees and the media-only figure is also given.
FAIL if the only cost per order given is 37.43, 14.80 unlabelled, or another value more than 2% from 12.23.
