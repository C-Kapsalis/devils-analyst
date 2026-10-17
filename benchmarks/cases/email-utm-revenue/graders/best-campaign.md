---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (GA4 email revenue joined to ESP campaigns after normalising the utm_campaign spelling: lower-case, trim spaces, treat hyphens and underscores as the same), ranked by revenue:
- vip_reserve_preview: revenue $10,815, unique clicks 512, sent 4,150, revenue per send $2.606
- new_roast_launch: revenue $5,571, unique clicks 2,380, sent 61,200, revenue per send $0.091
- cart_reminder_series: revenue $4,849, unique clicks 1,120, sent 14,900, revenue per send $0.325
- subscription_winback: revenue $3,783, unique clicks 905, sent 24,800, revenue per send $0.153
- summer_clearance_blast: revenue $3,147, unique clicks 7,340, sent 186,400, revenue per send $0.017
- brew_guide_august: revenue $845, unique clicks 1,885, sent 92,600, revenue per send $0.009
- brew_guide_september: revenue $777, unique clicks 1,940, sent 93,300, revenue per send $0.008
- brew_guide_july: revenue $757, unique clicks 2,010, sent 91,800, revenue per send $0.008

The best campaign is vip_reserve_preview: $10,815 revenue from only 512 unique clicks, about 3.4x the revenue of summer_clearance_blast ($3,147), which has the most clicks (7,340).

Wrong answers produced by common mistakes:
- Ranking by clicks picks summer_clearance_blast.
- Joining on the exact campaign string drops the drifted rows (e.g. "VIP_Reserve_Preview", "vip-reserve-preview", "vip_reserve_preview " with a trailing space). Exact-join revenue:
- new_roast_launch: $2,943
- cart_reminder_series: $2,351
- subscription_winback: $2,251
- summer_clearance_blast: $2,240
- vip_reserve_preview: $1,633
- brew_guide_september: $679
- brew_guide_august: $630
- brew_guide_july: $589
  which puts new_roast_launch first and shows vip_reserve_preview at only $1,633.

PASS if report.md names vip_reserve_preview as the best-performing campaign (on revenue, revenue per click, or revenue per send) AND recommends doing more of that kind of targeted/VIP send.
FAIL if report.md names summer_clearance_blast (or any campaign other than vip_reserve_preview) as the best, or ranks campaigns by clicks/sessions as the measure of performance.
