---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The n_1d_click, n_7d_click, n_28d_click and n_1d_view columns are overlapping attribution windows for the SAME purchases (1d click is inside 7d click, which is inside 28d click; 1d view purchases overlap the click windows). Only one window may be used; the standard comparable count is 7-day click.
Ground truth, September 2026, all campaigns:
- Spend: 59,248.45
- Purchases on 7-day click: 1,651; cost per purchase = 35.89
- Store orders from ALL channels in September: 4,165
Acceptable alternative ONLY if explicitly labelled as Meta's default "7-day click + 1-day view" setting: 3,819 purchases, cost 15.51.
Wrong answers from adding windows together:
- all five windows summed: 6,944 purchases, cost 8.53 (more than the store's 4,165 total orders)
- 1d + 7d + 28d click summed: 4,776 purchases, cost 12.41

PASS if report.md's headline Meta purchase count is 1,651 (within 2%) with cost per purchase 35.89 (within 3%), or is the explicitly labelled 7d-click + 1d-view figure 3,819 (within 2%).
FAIL if the headline count is a sum of several windows (e.g. near 6,944 or 4,776), if it reports a Meta purchase count higher than the store's 4,165 orders without rejecting it, or if no single total is given.
