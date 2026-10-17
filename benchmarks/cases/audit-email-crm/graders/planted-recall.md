---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 7 planted problems. Answer key:

1. Authentication. DKIM status is "fail" (published key does not match the signing key) and DMARC is "missing". SPF passes. Bulk senders need all three passing. Counts as found if report.md says DKIM is failing and/or DMARC is missing and must be fixed.
2. Dormant contacts in the main send. "Newsletter - September" went to segment all_subscribers (sent 43,420, including about 9,400 contacts outside the engaged_12m segment); its bounce rate is 3.37% while every other send is between 0.45% and 0.58%. Counts as found if report.md links the September newsletter's high bounce rate (about 3.4%) to mailing the dormant / non-engaged list in the main send and says to separate or suppress them.
3. Complaint spike hidden by the average. "Flash Sale 48h" (2026-08-21) had 53 complaints on 33,793 delivered = 0.157%, above the 0.1% warning line, while the ESP's August average shows 0.072%. Counts as found if report.md names that send (or an August send) above 0.1% complaints.
4. Shrinking list. Net list growth was -0.39% in August and -0.60% in September (new subscribers minus unsubscribed minus cleaned), after positive months; campaign rates look steady because they only measure who is left. Counts as found if report.md says net list growth turned negative.
5. CLV on revenue. The CLV sheet uses revenue x orders x tenure = 327.60, ignoring the 38% gross margin and the 10% discount rate; CLV:CAC 4.00. On discounted margin, CLV is about 103.19 and CLV:CAC about 1.26. Counts as found if report.md says CLV must use margin (and ideally discounting) and that the ratio is far lower than 4.0 (any margin-based figure between 1.0 and 1.6 is fine).
6. Win-back flow has no exit rule (exit_rule "none") and sent 18,640 emails in 30 days. Counts as found if report.md says the win-back flow needs an exit or suppression rule.
7. Tagging mismatch. The ESP send "Autumn Collection" uses utm_campaign sep_autumn_collection, but GA4 records sep-autumn-collection (hyphens), so the campaign does not join by name. Counts as found if report.md points out the name mismatch.

List which ones were found in your reasoning.
PASS if report.md identifies at least 6 of the 7 problems, each with its substance (a vague mention such as "check deliverability" does not count).
FAIL if it identifies fewer than 6.
