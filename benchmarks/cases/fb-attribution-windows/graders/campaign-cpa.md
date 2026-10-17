---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth cost per purchase by campaign on 7-day click (spend / n_7d_click):
- Prospecting - Broad: spend 14,000.12, 7d-click purchases 374, cost per purchase 37.43 (wrong, all windows summed: 11.07)
- Prospecting - Lookalike 2%: spend 10,722.33, 7d-click purchases 314, cost per purchase 34.15 (wrong, all windows summed: 10.27)
- Retargeting - Site Visitors 30d: spend 7,555.67, 7d-click purchases 306, cost per purchase 24.69 (wrong, all windows summed: 7.39)
- Video - Brand Awareness: spend 9,124.14, 7d-click purchases 100, cost per purchase 91.24 (wrong, all windows summed: 4.95)
- Advantage+ Shopping: spend 17,846.19, 7d-click purchases 557, cost per purchase 32.04 (wrong, all windows summed: 10.09)
On 7-day click the cheapest campaign is "Retargeting - Site Visitors 30d" (24.69) and the most expensive is "Video - Brand Awareness" (91.24).
The trap: "Video - Brand Awareness" gets most of its credit from view-through windows, so summing windows makes it look like the cheapest campaign (4.95).

PASS if report.md's per-campaign cost per purchase figures match the 7-day-click values above within 5% (or, if the report uses the labelled 7d-click + 1d-view setting, are consistent with that), AND it does NOT recommend "Video - Brand Awareness" as the most cost-efficient campaign for extra budget.
FAIL if it ranks "Video - Brand Awareness" as the cheapest/most efficient campaign, or recommends it for extra budget on cost-per-purchase grounds, or the per-campaign costs come from summed windows.
