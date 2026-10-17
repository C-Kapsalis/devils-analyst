---
title: The on-site funnel in GA4
question: How do you read on-site behavior from session to revenue, and where does the money leak
order: 2
---

Every channel you run (SEO, search ads, social, email) ends in the same place: your site. GA4 owns that back half of the buyer's path, where a visit either engages, converts and spends, or leaks away the money you paid to earn it. Read it as a sequence of transitions, because traffic up 10% means nothing if the share of visits that convert fell by the same amount at the same time.

## The framework

Read on-site behavior as a chain, and cut every ratio two ways: by channel and by landing page, never blended:

1. **The session arrives**, tagged with the channel, campaign, source and medium that produced it.
2. **Does it engage?** GA4 counts a session as engaged if it lasts over ten seconds, fires two or more pageviews, or triggers a key action (the event-based successor to bounce rate). High sessions with low engagement is a landing-page or intent-match problem, not a traffic problem.
3. **Does engagement become a key action?** When conversion rate leaks, the fix lives in the path to the action (offer, form, checkout friction), not in more traffic.
4. **Was the action worth money?** Purchasers, transactions, revenue, and revenue per user.

On attribution: GA4 assigns conversion credit by model. Last-click overcredits closers (branded search, direct); first-click overcredits discovery; data-driven (the default) weighs each touch by measured contribution. Compare last-click against data-driven before touching a budget: the credit deltas are a sized fund-more/fund-less order. And credit is not cause: only an experiment (geo holdout, lift study) proves a channel drove conversions that would not have happened anyway.

## Metrics that matter, and their traps

- **Sessions**: volume that arrives with a falling engagement rate is the wrong kind of growth; never celebrate a session spike before checking engagement held.
- **Engagement rate**: healthy sites sit around 55-63%; below ~40% on a channel, the traffic and the landing page disagree. Trap: it can read high for structural reasons, since a one-page site clears the ten-second bar on almost every visit.
- **Average engagement time and pages per visit**: read together. Long duration with pages-per-visit near 1.0 usually means people are stuck, not absorbed.
- **Conversion rate**: ecommerce averages roughly 2-3% per session ([Statista](https://www.statista.com/statistics/439576/online-shopper-conversion-rate-worldwide/)). Trap: a site-wide blended rate describes no real visitor; direct converts far better than cold paid social. Cut by channel, and name the action you are counting.
- **Revenue per user**: the cleanest single health signal, folding engagement, conversion and order value into one number. Total revenue up while revenue per user falls means you bought growth: more traffic, thinner value per head.
- **Data-driven attribution**: needs roughly 400 conversions per conversion type over 28 days; below that GA4 silently falls back to last-click without telling you.

## Interview prep

**"Paid social sends thousands of sessions but conversion is near zero. Diagnose it."**
A strong candidate checks the session-to-engagement transition first: bounces inside ten seconds mean the ad and landing page disagree; engagement without conversion points at the checkout or offer. If the channel's visitors bounce on every page, the channel is buying the wrong audience: pull spend, do not rewrite pages.

**"Our site-wide conversion rate fell from 2.4% to 2.1%. Should we panic?"**
They refuse the blended number: a mix shift toward a low-converting channel moves it with no behavior change. They re-cut by channel and by named key action before concluding anything.

**"A channel gains 40% credit under data-driven versus last-click. What does that mean?"**
The channel contributes along the path but rarely lands last, so last-click habit was underfunding it. They also check the volume threshold, and note big reallocation bets still deserve an experiment.

**"Which single on-site number would you track weekly?"**
Revenue per user, with engagement rate by landing page as the diagnostic underneath: one says whether value per head is improving, the other names the page to fix.
