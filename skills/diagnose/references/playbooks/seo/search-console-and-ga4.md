---
title: Search Console and GA4: find your CRO windows
question: Where is organic traffic being wasted on-site
order: 11
---

Use this when the question is "where is organic traffic being wasted on-site?" The goal is a shortlist of pages that earn organic traffic and engagement but lose the sale, each routed to the right owner: snippet, content/UX, or CRO.

## The framework

1. **Assemble the joined view.** Pull impressions, clicks, and position per page from Search Console's Performance report; pull sessions, engagement rate, conversions, and revenue per landing page from GA4, filtered to the Organic Search channel. Join on landing page (a spreadsheet works; the URL sets will not match perfectly (that is fine)). Each row now reads as one funnel: impressions → clicks → sessions → engagement → conversions → revenue.
2. **Sort by organic sessions descending.** You want the pages that already earn traffic.
3. **Walk each high-traffic page left to right and name where it breaks:**
   - Huge impressions, tiny clicks → **snippet** break. Owner: SEO (title/meta).
   - Clicks fine, low engagement → **content/UX** break. Owner: content or design.
   - Engagement fine, conversions near zero → **CRO window**. Owner: CRO (offer, CTA, checkout path).
   - High conversion, low sessions → not a problem: a starved winner. Feed it traffic; do not "optimize" it.
4. **Keep only the CRO-window pages** for a CRO sprint; route the others to their owners.

## Metrics that matter, and their traps

- **Clicks vs sessions**: different measurement systems (results-page counting vs on-site tagging after consent and blockers); the columns will never foot as arithmetic. Read the funnel *shape* per page and each column against itself over time; never sum across systems.
- **Engagement rate**: GA4 counts a session engaged after meaningful time, a second page, or a conversion event. It is the gate between an SEO problem and a CRO problem: low engagement means the page broke the query's promise; healthy engagement with no conversion means the page held them and the offer failed.
- **Conversions and revenue**: the pinhole detector. A page with hundreds of thousands of impressions, tens of thousands of sessions, healthy engagement, and a handful of transactions is the definition of a CRO window (often something as concrete as price display or size guidance below the fold).
- **The healthy-shape reference**: keep one page on the list that converts well, as proof the site *can* turn organic traffic into sales when the page earns it. It calibrates every other read.

## Interview prep

**"How do you connect Search Console and GA4, given they do not share metrics?"**
Join per landing page: SC brings impressions/clicks/position, GA4 (filtered to organic) brings engagement and conversion, and read each row as one funnel shape. A strong candidate volunteers that the columns will not reconcile and refuses to add across systems.

**"What separates a CRO problem from an SEO problem on the same page?"**
Where the funnel breaks: impressions-to-clicks is snippet (SEO), clicks-to-engagement is content/UX, engagement-to-conversion is CRO. Naming the transition names the owner; a shortlist without owners is just a chart.

**"A page has 9,400 organic sessions, 47% engagement, and 14 transactions. Diagnose it."**
Giant funnel, pinhole bottom: traffic and attention are earned, the purchase path fails: a CRO window, not a ranking or content job. Ask what changed on the page and what sits below the fold before proposing anything upstream.
