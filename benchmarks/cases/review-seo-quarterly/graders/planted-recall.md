---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The report under review (organic_search_report_q3_2026.md) contains 5 planted problems. Answer key:

1. False "crash" from reporting lag. "Organic clicks fell 32% this week" compares 7-13 Oct (5,919) with 30 Sep-6 Oct (8,671), but the last three days (11, 12, 13 Oct: 266, 409, 499 clicks against about 1,100-1,350 on normal days) are not fully reported yet; Search Console lags 2-3 days. Comparing the complete days (7-10 Oct vs 30 Sep-3 Oct) gives 4,745 vs 4,840 (-2.0%), essentially flat. Counts as found if report.md says the drop is in the last 2-3 days / reporting lag (or that like-for-like days are flat) and the penalty audit is not justified.
2. Wrong page celebrated, starved winner rewritten. /journal/how-to-care-for-linen has the most sessions (10,366) but converts at 0.12% (12 transactions) against a site organic rate of 1.27%; /bedding/linen-duvet-covers converts at 3.63% on only 881 sessions and is put on the CRO rewrite list. The guide page needs links into product pages (it does not sell), and the duvet page needs more traffic, not a rewrite. Counts as found if report.md flags either half with numbers: the guide's very low conversion (so "double down on guides" is not supported by revenue) or the duvet page's high conversion (so it should get traffic, not a rewrite). Both halves is ideal; one with numbers counts.
3. Averaged cluster CTR. The linen cluster CTR 10.4% is the mean of the 11 query CTRs, inflated by tiny long-tail queries; total clicks / total impressions = 4.8%. Counts as found if report.md gives a cluster CTR within 0.3 points of 4.8% or says the figure is an average of query rates that must be recomputed from totals.
4. Demand double counted. "Linen duvet cover" demand of 17,343 adds query+page rows; when two of our pages show for one search, each logs an impression. Query-level impressions are 10,575. The overlap (6,768) is a sign the buying guide competes with the product page (cannibalisation). Counts as found if report.md gives demand of about 10,575 or says the page rows double count.
5. Snippet problem bucketed as "defend, build links". "linen bedding" ranks at position 2.3 with 49,081 impressions but only 1.1% CTR; a top-three result normally gets well above 10%. The fix is the title and meta description (snippet), not links. Counts as found if report.md flags the low CTR at a top-3 position and recommends a title/snippet rewrite instead of (or before) link building.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention does not count).
FAIL if it identifies fewer than 4.
