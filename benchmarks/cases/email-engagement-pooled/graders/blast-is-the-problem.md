---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth breakdown:
- The weekly catch-all blast ("weekly_all_subscribers", 13 sends) is 93% of all delivered email. Its unique click rate is 0.98%, CTOR 6.8%, unsubscribe rate 0.34% of delivered.
- The five targeted segment campaigns (restock alerts, VIP early access, cart follow-up, new arrivals, loyalty reminders) have a pooled unique click rate of 4.99%, CTOR 12.6%, unsubscribe rate 0.11%.
- So the low pooled click rate is caused by one send: the catch-all blast. The targeted program is healthy (roughly 5x the blast's click rate).

PASS if report.md identifies the weekly all-subscribers blast as the drag on engagement (contrasted with the much stronger targeted segments) AND its main recommendation is to fix that send (e.g. segment it, suppress unengaged subscribers, cut its frequency or audience, or shift volume to the targeted programs).
FAIL if report.md concludes that email engagement is weak across the board, recommends a generic overhaul of all emails (subject lines, design, templates for everything) without singling out the blast, or does not distinguish the blast from the targeted campaigns.
