---
title: GA4 fundamentals, ranking channels by quality
question: Which channels actually earn engaged, buying traffic, not just the most sessions
order: 3
---

The default GA4 channel report sorts by sessions, and sessions are the easiest number to buy and the least meaningful to rank on. A channel ranking your budget conversation can stand on reads three lenses in order (attention, then how real it is, then what it is worth) and names the channel that is big but hollow.

## The framework

Work GA4's channel groups (Google's universal classification: Direct, Organic Search, Paid Search, Paid Social, Cross-network, Email, and so on) through three lenses:

1. **Attention: sessions.** Sort descending and note the giants. This is the starting order, never the verdict.
2. **Quality: engaged sessions and engagement rate.** The signature to hunt is a channel with huge sessions and an engagement rate far below the others: attention that evaporates on arrival. GA4 counts a session as engaged if it lasts over ten seconds, fires two or more pageviews, or triggers a key action.
3. **Value: transactions and revenue, read per engaged session.** Revenue per engaged session is the honest value-for-attention comparison across channels; it prices the traffic that actually stuck around.

A worked example: paid social tops the board at 410,000 sessions but engages at 23%, while direct, organic search and paid search all sit near 55%. Email, at a tenth of the volume, engages at 49% and carries €7,100 of revenue. The read writes itself: paid social is buying attention that mostly bounces, and email punches far above its volume. Neither fact is visible on a sessions-only chart.

One boundary: this ranks channel quality, not ROI. GA4 carries traffic and revenue by channel, not ad cost; true ROI needs spend reconciled from the ad platforms. Until then, read quality here and cost in the spend tools. Never approximate ROI by dividing revenue by raw sessions across channels with wildly different engagement rates.

## Metrics that matter, and their traps

- **Sessions by channel**: the attention lens. The trap: ranking on it. Volume is the cheapest thing a channel can deliver, and paid channels can top it indefinitely while converting nothing.
- **Engagement rate by channel**: the reality check on the giants. The trap: reading one channel's rate in isolation; the signal is the spread: one channel far below its peers is hollow.
- **Engaged sessions**: the honest denominator for value math; it filters out the ten-second bounces you paid for.
- **Revenue per engaged session**: the value-for-attention ratio the channel comparison can actually stand on. The trap: substituting revenue per raw session, which punishes high-engagement channels and flatters bouncy ones.
- **Revenue by channel**: the trap is treating GA4's revenue split as ROI; without cost per channel it says what a channel earned, not whether it paid.

## Interview prep

**"Paid social sends 4x more sessions than any other channel. Should it get more budget?"**
A strong candidate asks for engagement rate before answering. If it engages at 23% against ~55% for the rest, most of that volume evaporates on arrival: the next spend goes to fixing creative, targeting or the landing page, not to more traffic.

**"How would you compare email against paid search when email has a tenth of the traffic?"**
Per engaged session, not in totals: engagement rate to establish the traffic is real, then revenue per engaged session for value. Small channels with dense quality routinely beat giants on that read.

**"Can you compute channel ROI from GA4 alone?"**
No: GA4 carries traffic and revenue but not cost. They would reconcile ad spend from each platform beside the GA4 data, and refuse the revenue-over-raw-sessions shortcut.

**"A channel's engagement rate collapsed month over month. What are your hypotheses?"**
A traffic-mix change (a new campaign buying cheaper clicks), a landing-page change breaking the intent match, or a tagging change reclassifying traffic, in that order, each checkable in a day.
