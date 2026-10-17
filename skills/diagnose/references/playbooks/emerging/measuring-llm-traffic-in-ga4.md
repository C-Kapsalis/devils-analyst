---
title: Measuring LLM traffic in GA4
question: How do you build a monthly read of the traffic AI answer engines send you
order: 3
---

Use this when the question is "are the AI answer engines sending us anyone, and what do we do about it?" The goal is a monthly read of the traffic ChatGPT, Perplexity, Gemini, and Claude send: how fast it is growing, which pages they cite, and whether it engages and buys. The volume is small; the slope and the cited-page set are the story.

## The framework

1. **Build the filter.** In a GA4 Exploration, isolate sessions whose traffic source matches the answer-engine referrers (chatgpt, perplexity, gemini, claude, and variants). Use contains-matching on the core names rather than an exact list: the engine set drifts as new tools appear, and an exact list silently goes stale. Check both the source and medium dimensions when you first build it: AI referrers do not always land in the field you expect.
2. **Set the rows and columns.** Landing page as the row; sessions, engaged sessions, engagement rate, conversions/transactions, and revenue as the metrics. Each row is one cited page's funnel.
3. **Read the slope.** Track LLM sessions as a share of total traffic, month over month. A move from 0.2% to 0.4% is a doubling a volume chart hides.
4. **Read the cited-page set.** The pages receiving this traffic are the pages the engines quote. New entrants mean a page just got recommended; dropouts mean a competitor's page displaced yours in the answers.
5. **Read the quality.** Answer-engine visitors arrive pre-convinced. Engagement and conversion at or above your organic-search baseline is the channel working as designed; below it means the answer set an expectation the page does not meet: fix the page, not the channel.

## Metrics that matter (and their traps)

- **Share of total sessions, over time**: the only honest size read for a small channel. Trap: the raw session count invites you to dismiss a stream that is doubling.
- **Engagement rate under the filter** is a quality gate: a tiny channel at 61% engagement is telling you something a big channel at 40% is not.
- **Conversion vs the organic baseline**: AI-referred sessions converting at a multiple of the organic rate (2x is not unusual on small volumes) is the finding that changes internal-linking priorities. Trap: small denominators; read the multiple over several months before acting on it.
- **Top cited page**: often an explainer, not the homepage or a product page. Its internal links to your commercial pages just became highly valuable links on the site.
- **The filter itself** is the biggest trap: maintenance, since a hardcoded referrer list drifts as new engines and domain variants appear. Re-verify it quarterly, and prefer contains-matching.

## Interview prep

**"How would you set up AI-referral tracking in GA4?"**
An Exploration filtered to sessions whose source contains the core engine names, landing page as the row, engagement and conversion as metrics. A strong candidate flags the maintenance problem unprompted (exact referrer lists go stale) and mentions checking which dimension the referrer actually lands in.

**"The channel is 0.2% of sessions but converts at twice the organic rate. What do you report?"**
The share trend and the per-session value, not the volume, and the cited-page set as an action list: strengthen internal links from the quoted explainers to the commercial pages. Also the small-denominator caveat: confirm the conversion multiple holds over several months.

**"How would you detect that a competitor displaced you in AI answers?"**
A page dropping out of the cited-page set: sessions from AI referrers to a page falling to zero while its organic performance holds. That is the closest thing to rank tracking this channel currently offers.
