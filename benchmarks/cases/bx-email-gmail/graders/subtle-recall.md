---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. The dip is Gmail inbox placement. By mailbox provider, Gmail open rate fell from 30.9% to 9.1% after 9 September, while Yahoo (26.8% to 27.0%) and Outlook (24.1% to 23.9%) are flat; Postmaster domain reputation dropped from High to Low and then Bad. "Delivered" (99.5%) only means accepted, not inboxed. Counts as found if report.md isolates the drop to Gmail (or to spam-folder placement / domain reputation).
2. Gmail spam rate hidden from the ESP. Postmaster user-reported spam rate is 0.33%-0.44% from 8 September, above Google's 0.3% limit, while the ESP shows complaints of 0.03%. Counts as found if report.md cites the Postmaster spam rate above 0.3% (or says the ESP complaint figure misses Gmail complaints).
3. Volume spike. The 8 September reactivation send went to 60,558 addresses against about 24,049 normally, with a 5.4% bounce rate, the day before Gmail reputation fell. Counts as found if report.md links the reactivation blast (volume or old addresses) to the reputation drop.
4. One-click unsubscribe off. Settings show the List-Unsubscribe header as mailto only and one-click (List-Unsubscribe-Post) off, required for bulk senders by Gmail and Yahoo. Counts as found if report.md flags it.
5. Hard bounces not suppressed. Hard bounce handling is "suppress after 3 hard bounces"; the bounce log shows 36 of 60 sampled addresses hard-bounced 2-4 times. Counts as found if report.md says to suppress on the first hard bounce.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
