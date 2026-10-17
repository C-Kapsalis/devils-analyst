---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Roadmap ranked by volume, not by what converts. The descaling cluster (informational) converts at about 0.56% in paid search, the grinder buying cluster ("burr grinder sale", "buy burr grinder", "espresso grinder sale", "flat burr grinder price") at about 8.5%. Counts as found if report.md uses the paid conversion rates (or another conversion signal) to say the descaling hub is low value per impression and the grinder buying terms are worth more.
2. Descaling demand double counted. The roadmap's 51,936 impressions sum the query+page rows, where two own pages (/guides/descaling-your-espresso-machine and /blog/descale-tips-for-home-baristas) show for the same searches. Query-level demand is 31,323; the 20,613 gap is overlap, i.e. the two pages cannibalise each other. Counts as found if report.md gives roughly 31,323 (within 5%) as the real demand or says the 51,936 double counts, or flags the two descaling pages competing.
3. Build vs deepen. Roadmap item 3 builds a new "best burr grinder for espresso" page, but /guides/grinder-buying-guide already ranks about 9.2 for that query. Counts as found if report.md says to improve the existing guide rather than build a competing page (or warns the new page would cannibalise it).
4. Wrong page ranking for buying queries. The grinder buying queries are answered by /blog/what-is-a-burr-grinder (an explainer) at positions about 11-16, average 13.5, CTR 0.84%; /shop/grinders does not appear in the query+page export at all. Counts as found if report.md notes that the explainer, not the category or product page, is the page ranking for these buying terms and that the category page should be pointed at them.
5. Paid converter with no organic footing. "milk frothing jug" and "milk jug for latte art" bring 181 paid conversions in Q3 and no jug query appears in Search Console. Counts as found if report.md flags this as a content or category-page gap.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with its evidence (a number, query or page).
FAIL if fewer than 3.
