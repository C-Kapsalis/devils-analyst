---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The draft deck (q3_social_review.md) has 5 planted problems. Answer key (numbers computed from the exports):

1. TikTok engagement rate on the wrong base for the benchmark. The deck's TikTok 6.9% is engagements / VIEWS (the export's engagement_rate column), compared with a follower-based median of 1.73%. Per follower (total engagements / summed followers across videos) TikTok is 2.11%, and 1.44% without the giveaway video. Found if report.md says the TikTok rate is per view (or reach) and not comparable to the follower-based benchmark, or recomputes it per follower (about 2.1% or 1.4%).
2. Instagram "engagements" are likes only. In instagram_posts_q3.csv the engagements column equals likes; comments, shares and saves are separate. With all four, Instagram ER per follower is 0.55% (deck: 0.31%), above the 0.36% median. Found if report.md notes the likes-only definition (or the definitions differ between platforms) and/or gives a corrected Instagram rate around 0.55%.
3. Giveaway inflating TikTok. The video "Win a year of tea! Follow + comment..." (2026-08-14) has 7,815 engagements (34% of all TikTok engagements in Q3, mostly comments: 4,870). The giveaway days brought about 5,000 extra follows (64% of Q3 TikTok follows), and unfollows rose after the 28 Aug draw (about 1,704 extra). Net TikTok growth without the giveaway is about 1,153 of the reported 4,449. Found if report.md identifies the giveaway video/period as inflating engagement and/or follower growth (any of these numbers, or a clear description with the date).
4. Share of voice fell. Own mentions +34% QoQ, but all four brands' mentions grew 58%; Fernhill's share of voice went from 22.2% to 18.8%. Found if report.md says competitors grew faster / share of voice fell (any SOV figures near these, or the competitor growth).
5. Reach summed across posts. "Instagram reached 464,696 people" is the sum of per-post reach (464,696); account_summary_q3.csv gives quarterly account reach of 99,909. Found if report.md says post reach cannot be summed into people reached and/or quotes the ~100K quarterly figure.

List which ones were found in your reasoning, each with its evidence.
PASS if at least 3 of the 5 are identified with evidence (a number, a column, a post, or a specific quote). A vague "check the benchmarks" does not count.
FAIL if 2 or fewer are identified.
