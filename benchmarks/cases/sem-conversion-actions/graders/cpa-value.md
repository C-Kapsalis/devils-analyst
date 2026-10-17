---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

A "sale"/acquisition here is the purchase conversion action only. Ground truth for September 2026 (whole account):
- Cost: 40,568.34
- Purchases (conversion_action = purchase, conversions column): 2,335.8
- CPA = cost / purchases = 17.37
Wrong CPAs from counting the wrong conversions:
- Using the campaign `conversions` column (purchases + newsletter signups, 4,329.4): CPA 9.37
- Using `all_conversions` (adds add_to_cart and view-through, 9,013.9): CPA 4.50

PASS if report.md states the September account CPA as 17.37 within 3% (cost per purchase).
FAIL if the headline CPA is near 9.37 or 4.50, or if no September CPA is given.
