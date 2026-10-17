---
title: Query-level data: why aggregates mislead
question: What does the aggregate organic number hide, and at what level does the truth live
order: 3
---

"Organic converted at 2.2%" survives every meeting precisely because no one can interrogate it. The channel total is an average over things that should never be averaged: brand and non-brand demand, ten different intents, pages competing with each other. Read at the query level, the same month's data starts answering back.

## The framework

1. **Know why your two dashboards disagree.** Search Console counts clicks on Google's results page; GA4 counts sessions your own tag recorded, after consent banners and blockers took their cut. Clicks are not sessions; neither tool is lying. Each holds exactly the half the other is missing: Search Console knows queries but not conversions, GA4 knows conversions but not queries. Do not spend a week reconciling them.
2. **Read the three levels apart.** Property level describes, never explains. Query level counts one impression per search: a true read of demand. Query-page level counts one impression per page shown, so when two of your pages rank for the same search, summing the rows double-counts the demand. Read the query level for demand, the query-page level for which page answers it, and treat the double listing itself as a finding: keyword cannibalization, two pages splitting clicks and link equity.
3. **Cut brand from non-brand before reading any rate.** A blended 2.2% conversion rate can decompose into brand at 6% and non-brand at 0.7%: brand demand lending its warmth to hide a weak growth engine. Non-brand is the only part of organic that acquires new customers.
4. **Gather variants into clusters.** Search Console reports literal strings, so one intent arrives shattered into dozens of spellings, plurals, and misspellings. A top query can be under half of its own intent's demand; read the cluster and the demand roughly doubles without the market changing at all.
5. **Use the paid query as your organic crystal ball.** An organic conversion rate per query exists nowhere in your stack, but if you bid on the same queries, paid search has measured conversion per query at full price. Use that as the query's theoretical CVR to rank organic opportunities by conversion quality instead of raw volume.

## Metrics that matter, and their traps

- **Query-level impressions**: real demand, counted once per search. Trap: query-page rows double-count whenever two of your pages appear together.
- **Blended organic conversion rate**: against the ~2-3% ecommerce session average it can look healthy while the non-brand engine is broken. Split first, judge second.
- **Query-level position**: the topmost rank you held per search, so one strong page quietly masks how weakly a second page shows for the same term.
- **Theoretical CVR (paid CVR on the same query)**: an estimate for prioritization, never a measurement: ad clicks land on tuned pages and skewed audiences. High paid CVR with weak organic rank is where next quarter's content belongs; low paid CVR at any rank is informational demand: awareness, never the conversion priority. Cross-industry, search clicks convert around 7% ([WordStream](https://www.wordstream.com/blog/ws/2022/05/19/search-advertising-benchmarks)), but the per-query spread is the point.
- **Ranking metric choice**: a store ranks queries by conversion; an ad-supported publisher ranks by CTR and click volume, because the visit is what it sells. Business-model choice, not a default.

## Interview prep

**"Search Console shows 134k clicks and GA4 shows 127k organic sessions. Which is right?"**
Both: they measure different events in different places, on different sides of the click, with different losses. A strong candidate refuses the reconciliation project and reads each column against itself over time.

**"How would you find keyword cannibalization?"**
At the query-page level, the only level that sees it: one query, two of your URLs each logging impressions. The fix is consolidating intent onto one page, not tweaking two titles.

**"Why might a keyword-by-keyword read understate demand?"**
One intent fragments into dozens of string variants, each too small to matter when sorted by clicks. Cluster the variants and the demand often doubles; the reading changed, not the market.

**"How do you prioritize organic content bets without per-query conversion data?"**
Borrow the paid side: rank queries by their paid conversion rate as a theoretical CVR, then filter to weak organic rank. State the caveat unprompted: it ranks opportunities, it does not promise outcomes.
