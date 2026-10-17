---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Brand rise hides a non-brand fall. Total clicks moved +3.4% April to September, but brand queries (containing "hollowmere") rose +42% while non-brand queries fell -24% (Q2 to Q3: non-brand 38,600 to 32,968). Counts as found if report.md splits brand and non-brand and states the non-brand decline (about 20-30% either monthly or about 15% quarterly).
2. Impressions growth from countries Hollowmere does not ship to. Property impressions +18% Q2 to Q3, but United States and Canada impressions changed -3.8%; the growth (185,496 extra impressions) is India, Philippines, UK and Australia at positions 21-37 with CTR under 1%. Counts as found if report.md says the visibility growth is in unserved markets (or that served-market impressions did not grow).
3. New-page pipeline run dry. Pages earning their first impressions per month: 13, 10, 7, 4, 3, 0 (April to September). Counts as found if report.md notes the count falling to zero / no new pages earning impressions, i.e. clicks are held up by old pages.
4. AI-assistant traffic is not zero. The filter used old referrer names; GA4 shows chatgpt.com, perplexity.ai, gemini.google.com and copilot.microsoft.com with 1,799 sessions, 74 purchases, conversion rate about 4.1% against Organic Search about 1.9%. Counts as found if report.md says the AI referral figure is wrong because of the filter (outdated domains) and gives the real sessions or conversion.
5. "Ranks #2" on tiny volume. /blog/trail-shoe-rotation has position 2.0 on 38 impressions and 3 clicks in Q3; average position on so few impressions is noise, not a rank. Counts as found if report.md questions the "#2" claim because of the low impressions.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence (a number or named row).
FAIL if fewer than 3.
