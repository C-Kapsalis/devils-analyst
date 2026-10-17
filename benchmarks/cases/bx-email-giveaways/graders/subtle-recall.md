---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Giveaway subscribers barely buy. Purchasers per delivered email: giveaway 0.034% vs site_popup 0.42% (data: 131 purchasers from giveaway subscribers vs 6,819 from pop-up). Per 1,000 subscribers per month that is about 2.7 purchasers for giveaway vs 33.4 for pop-up, while each costs a similar amount to acquire (about $1.23 vs $1.09 per subscriber), so a giveaway subscriber costs roughly 14x more per purchase. Counts as found if report.md shows giveaway subscribers purchase (or click) far less than other sources, with a number.
2. Click-rate fall is mix, not creative. Program click rate fell from 3.69% to 2.96%, but each source's click rate is flat (site_popup 3.26%-3.53%, checkout_optin 3.95%-4.25%, giveaway 0.60%-0.63% across months); the drop comes from the rising share of giveaway subscribers. Counts as found if report.md says the decline is driven by list mix rather than tired creative.
3. Double opt-in off on the giveaway form. The giveaway landing page has double opt-in off; giveaway sign-ups include typo domains (gmial.com, hotmial.com, gmail.con) and 2,898 giveaway addresses were cleaned (bounced/removed). Counts as found if report.md flags the missing double opt-in or the typo domains / high cleaning of giveaway sign-ups.
4. Gross vs net growth. The "76%" counts gross sign-ups; after unsubscribes and cleaning the list grew 47% (35,000 to 51,318). Counts as found if report.md gives the net growth (within a few points) or says the 76% ignores unsubscribes and cleaning.
5. Borrowed ROI. "$36 for every $1" is an industry benchmark, not this program's measured return. Counts as found if report.md flags it.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
