---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: CAC = September spend / paid subscribers from trials started in September (all conversions count, including those whose converted_at falls in October, since the 14-day trials of late-September starters convert in October). 121 of the conversions are dated in October.
- google_search: spend $15,600, 109 paid from 240 trials (45.4%), CAC $143.12, avg price $19.76, payback 10.3 months
- meta: spend $19,800, 125 paid from 380 trials (32.9%), CAC $158.40, avg price $18.03, payback 12.6 months
- tiktok: spend $8,400, 36 paid from 340 trials (10.6%), CAC $233.33, avg price $18.32, payback 18.2 months

Wrong answers:
- Cost per trial instead of CAC: tiktok $24.71, meta $52.11, google_search $65.00 (makes TikTok look cheapest).
- Counting only conversions dated in September: google_search $255.74 (61 paid), meta $304.62 (65 paid), tiktok $365.22 (23 paid).

PASS if report.md's CAC for each of the three channels is within 5% of the ground truth (meta $158.40, google_search $143.12, tiktok $233.33).
FAIL if any channel's CAC is missing or outside 5%, or report.md reports cost per trial or the September-dated-only figures as CAC.
