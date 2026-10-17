---
title: Deliverability and inbox placement
question: Why are my emails not reaching the inbox, and what do I fix first
order: 3
---

Deliverability is the gate every other email number sits behind: the share of what you sent that actually arrived. Get it wrong and every downstream rate measures a smaller, quieter audience than you think, because opens and clicks can only count the people the email reached. A brilliant campaign delivered to 88% of the list is not a brilliant campaign; it is a reputation problem wearing a good open rate.

## The framework

Hold delivery above 95%. When it slips, three causes drag it down, and you work them in this order:

1. **Authentication gaps: binary, fix once.** SPF (which servers may send for your domain), DKIM (a cryptographic signature per message), and DMARC (the policy when the first two fail). Google and Yahoo [made all three mandatory for bulk senders](https://support.google.com/a/answer/14229414) in February 2024; a domain missing any of them is filtered or rejected outright. Set the records, confirm each actually passes.
2. **A dirty list: ongoing hygiene.** Dead addresses announce themselves through bounces. Hard bounces go onto a suppression list the moment they bounce; use a list-verification service to flag invalid addresses proactively instead of learning from the bounce.
3. **Complaints: a relevance problem.** A complaint-tripped filter is the fastest way to lose the inbox. The fix is fewer, better-targeted sends, never more volume through a cracking reputation.

Then quarantine risk: pull long-dormant subscribers (no open or click in ~12 months) into their own segment, run a dedicated win-back campaign, and delete the non-responders. Dormant addresses turn into spam traps; their risk never belongs inside the main send.

## Metrics that matter, and their traps

- **Deliverability rate** (delivered / sent): hold above 95%. The trap: reading anything downstream before this gate holds; a leak here shrinks the base every other rate is computed on.
- **Bounce rate**: keep under 2%. The trap is watching the level instead of the trend: a bounce rate rising while send volume holds steady is the early warning that hygiene has lapsed, long before delivery itself falls through the floor.
- **Complaint rate**: 0.1% is a warning shot; 0.3% is critical and gets your domain throttled or blocked. Complaints almost always mean a consent or frequency problem, not a creative one.
- **Authentication pass status**: not a rate, a checklist; SPF, DKIM, DMARC each verified as passing. The trap is assuming a published record validates.
- **Win-back send performance**: read the dormant segment on its own. Blended into the main campaign, a risky segment hides its true bounce and complaint rates inside a healthy average.

## Interview prep

**"Deliverability dropped from 97% to 90%. Walk me through your triage."**
Strong candidates go in cause order: verify SPF/DKIM/DMARC pass (binary, cheapest fix), then check the bounce trend at steady volume (hygiene), then complaint rate against 0.1%/0.3% (reputation). They explicitly refuse to discuss subject lines until the gate holds.

**"Marketing wants to re-mail the whole lapsed list to hit a revenue target. What do you say?"**
They flag the reputation risk: dormant addresses carry high bounce and complaint rates and some are spam traps. The compromise is a quarantined win-back segment with a dedicated offer, then deleting non-responders, containing the risk away from the engaged list.

**"Is cleaning 3,000 dead addresses off the list losing audience?"**
No. Those addresses were never reachable revenue, and mailing them is exactly what convinces providers the list is stale. Cleaning protects the deliverability of the audience that is still listening.

**"What changed for bulk senders in February 2024?"**
Google and Yahoo made SPF, DKIM and DMARC mandatory and enforce explicit complaint thresholds. Authentication moved from best practice to a hard requirement; unauthenticated bulk mail is now rejected, not just disadvantaged.
