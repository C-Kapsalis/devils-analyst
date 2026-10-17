---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Meta tracking broke from the week of 2026-07-27. facebook / paid_social sessions fall to a few dozen a week while l.facebook.com and m.facebook.com referral sessions jump from about 650 to about 8,182 a week, with Meta spend unchanged: the ads lost their UTMs. Before the break Meta's GA4 ROAS was about 2.9; the memo's 0.90 is a tagging artefact. Counts as found if report.md links the paid_social collapse to the facebook referral jump (UTMs lost) or says Meta's GA4 return is understated because of tracking.
2. Mixed sources. Google's 6.6 is the Google Ads platform's own conversion value; GA4 last click gives Google 4.8. Meta is measured in GA4. Counts as found if report.md says the channels are compared on different sources/attribution.
3. Brand hides non-brand. On GA4, brand_exact returns about 17.2 and generic_shopping_search about 1.61, below the break-even ROAS of 2.5 at 40% margin. Counts as found if report.md splits Google into brand and generic and says generic is below break-even (or the weakest line).
4. Wrong profitability line. With 40% gross margin, break-even ROAS is 2.5, not 1.0. Counts as found if report.md states the 2.5 break-even (or that ROAS 1 loses money).
5. Microsoft Ads untagged. $8,652 spent from 10 August; no bing / cpc rows exist, while bing / organic sessions rose from about 874 to 2,453 a week. Counts as found if report.md says Microsoft Ads traffic is landing in bing / organic (untagged / auto-tagging off) rather than producing nothing.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
