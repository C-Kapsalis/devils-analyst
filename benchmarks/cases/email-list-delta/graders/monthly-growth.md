---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth monthly growth for the newsletter list (growth = net change in the month / members at the start of the month):
- 2026-04: start 48,210, new subscribers 2,070, unsubscribes 853, cleaned 339, net change +878, growth 1.82%, end 49,088
- 2026-05: start 49,088, new subscribers 2,250, unsubscribes 1,111, cleaned 508, net change +631, growth 1.29%, end 49,719
- 2026-06: start 49,719, new subscribers 2,391, unsubscribes 1,223, cleaned 658, net change +510, growth 1.03%, end 50,229
- 2026-07: start 50,229, new subscribers 2,434, unsubscribes 1,492, cleaned 807, net change +135, growth 0.27%, end 50,364
- 2026-08: start 50,364, new subscribers 2,597, unsubscribes 1,657, cleaned 988, net change -48, growth -0.10%, end 50,316
- 2026-09: start 50,316, new subscribers 2,710, unsubscribes 1,743, cleaned 1,088, net change -121, growth -0.24%, end 50,195

Growth decelerated from 1.82% in April to -0.24% in September: the list SHRANK by 121 members in September, even though new subscribers (2,710) were at their highest. Unsubscribes and cleaned (bounced/invalid) addresses grew faster than sign-ups.

Wrong answers produced by common mistakes:
- Treating new subscribers as growth: September 2,710 new subscribers = 5.39% of the list, "growing strongly".
- Month-over-month % change of the net-change numbers themselves, or growth computed on the summed members column.

PASS if report.md states that net growth in September 2026 was negative or about zero (a monthly growth rate within 0.3 percentage points of -0.24%, or a net change within 15% of -121) AND makes clear that gross sign-ups are being offset by unsubscribes/cleaned addresses.
FAIL if report.md says the list is growing healthily in the latest month, presents new subscribers (or new subscribers / list size, about 5.39%) as the growth rate, or gives no latest-month growth figure.
