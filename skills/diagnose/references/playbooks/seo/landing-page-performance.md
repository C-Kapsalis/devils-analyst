---
title: Landing-page performance: earning the impressions
question: Which pages earn the impressions they get, and which waste them
order: 4
---

Ahrefs studied a billion pages and found 90.6% of them get no organic search traffic from Google at all ([Ahrefs](https://ahrefs.com/blog/search-traffic-study/)). The pages that do earn traffic carry the whole estate, so knowing exactly which ones, and why the rest do not, is the entire job. A page-level average will not tell you: it is two averages stacked on top of each other, one blending queries, the other blending countries and devices, and both of them lie.

## The framework

1. **Take the page, drop to country, then device, then read the four numbers together**: impressions, clicks, CTR, position. The same position earns a different share of clicks per device and market, so a page can look healthy on desktop at home and be near-invisible on mobile abroad, with the average sitting comfortably between.
2. **Scope to your business.** Geography is where your audience lives and which markets you serve; device is where they are active. Filter out countries you do not ship to, or the read is noise.
3. **Name which of the three stories the page tells**, then apply that story's fix, and refuse the other fixes:
   - **Earning its impressions**: CTR in line with position, on the queries it was built for. Feed it (depth, internal links); do not audit it.
   - **Strong position, weak click**: good rank, CTR well below what the position should pull. Rewrite title and snippet; do not build links. The expensive part, the rank, is already paid for.
   - **Ranking for what it cannot serve**: impressions on a valuable query the page does not answer (a fabric explainer collecting buying-term impressions). Build or point the right page at the intent; a title tweak fixes nothing.
4. **Drill any suspect page to its queries** to confirm the story: an informational query served fine at position three can coexist with 40k+ impressions on transactional terms the same page has no way to satisfy.

## Metrics that matter, and their traps

- **Impressions per page**: visibility earned. Trap: high impressions on a mismatched intent look like success at property level and are a trap dressed as a win.
- **CTR against position**: the #1 organic result pulls about 27.6% CTR ([Backlinko](https://backlinko.com/google-ctr-stats)); a page at position two or three converting a fraction of that is leaving clicks on the table no link-building recovers. Google's own guidance: the title link and meta description are what earn the click at a rank you already hold.
- **Average position**: impression-weighted, hides the distribution; lags two to three days and samples the long tail. Read as a trend and pair with CTR before acting.
- **CTR as a ratio**: recompute from totals (clicks over impressions) at whatever grain you read; averaging each row's rate gives a number true of nothing.
- **Cannibalization signal**: two of your pages surfacing for the same valuable query split the signal, a common cause of pages stalling below the position they could reach.

## Interview prep

**"A page holds position 2.8 and converts under 1% of impressions into clicks. What do you do?"**
Rewrite the title and meta description: nothing about the ranking is broken; searchers see the result and scroll past. A strong candidate says explicitly what the fix is *not*: link-building. One snippet rewrite here beats a quarter of links on a worse-ranked page.

**"A blog post shows big impressions on a high-value commercial term. Good news?"**
Only after drilling to the queries. If a thin explainer is collecting impressions on buying terms it cannot close, the demand belongs on a product or category page: the fix is pointing the right page at the intent, not polishing the wrong one.

**"Why split a page's numbers by country and device?"**
Because CTR at a given position is not a constant: it shifts by device and market, so a strong home market subsidizes a weak overseas one and the page total hides both. Then scope the split to markets and devices that carry the business case.

**"How would you triage a thousand-page site?"**
Group pages into meaningful sets (sections, templates, product lines) and read at that grain first: a category that looks fine in total can hide one line gaining impressions while its CTR falls. Then apply the three-stories triage per page inside the offending set.
