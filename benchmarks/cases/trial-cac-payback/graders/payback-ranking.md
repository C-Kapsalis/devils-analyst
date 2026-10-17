---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth payback (months) = CAC / (average monthly price of that channel's paid subscribers x 70% margin):
- google_search: spend $15,600, 109 paid from 240 trials (45.4%), CAC $143.12, avg price $19.76, payback 10.3 months
- meta: spend $19,800, 125 paid from 380 trials (32.9%), CAC $158.40, avg price $18.03, payback 12.6 months
- tiktok: spend $8,400, 36 paid from 340 trials (10.6%), CAC $233.33, avg price $18.32, payback 18.2 months
Fastest payback: google_search; slowest: tiktok. (Using price without margin gives shorter paybacks, google_search 7.2 months, meta 8.8 months, tiktok 12.7 months; that ignores the 70% margin but keeps the same ranking.)

Naive answer: TikTok is the best channel because it has the lowest cost per trial ($24.71 vs meta $52.11, google_search $65.00), despite only 11% of its trials converting.

PASS if report.md identifies google_search as the fastest payback channel and TikTok as the slowest/worst, with payback figures within 15% of the ground truth (margin-based), or within 15% of the revenue-based paybacks (google_search 7.2 months, meta 8.8 months, tiktok 12.7 months) if the report clearly labels them as revenue-based.
FAIL if report.md calls TikTok the best or most efficient channel, or ranks channels by cost per trial.
