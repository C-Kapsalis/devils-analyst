---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. Made-for-advertising / invalid-traffic placements. Five Open Audience websites (dailyquizhub.net, top10-listicles.co, viralnewsfeed.site, recipes-daily-best.com, celebgossiphub.info) have CPMs around €0.26-0.33, carry 58% of Open Audience impressions, a viewable rate of 15%, and zero GA4 sessions. Found if report.md flags these placements (as low-quality / MFA / invalid / to exclude) with evidence.
2. Accidental app clicks. The two mobile-app game placements have CTR 5.1% (vs about 0.4% elsewhere) but only 0.08 sessions per click. Found if report.md flags the app placements as accidental/low-quality clicks.
3. Cheap CPM is not cheap results. Open Audience CPM €0.96 vs Custom Intent €4.23, but the low CPM comes from the MFA and app inventory; cost per engaged session is €3.13 for Open Audience vs €1.69 for Custom Intent (€2.54 Affinity). Found if report.md compares cost per session or engaged session (or a quality-adjusted cost) and shows Open Audience is not the efficient option.
4. Remarketing settings. "All visitors 30d" has no frequency cap and does not exclude purchasers; September frequency averaged 15.1 impressions per user per week. Found if report.md flags the missing cap/high frequency or the missing purchaser exclusion.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
