---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The deck recommends moving the Instagram content budget (EUR 18,000/quarter) to TikTok.

Correct call: do NOT move the Instagram budget to TikTok on this evidence (keep Instagram funded; at most run TikTok as a test or a smaller reallocation). Reasons from the data: like-for-like (all engagement types, per follower) Instagram is 0.55% vs its 0.36% median, while TikTok is 1.44% per follower without the giveaway, below its 1.73% median; and Instagram drove 8,483 GA4 sessions and 185 purchases (EUR 6,122) in Q3 vs TikTok's 2,096 sessions and 19 purchases (EUR 567).

Naive wrong answer: endorse the move because "TikTok 6.9% is 4.0x its benchmark and Instagram is below its median", or because TikTok followers grew +15.9%.

PASS if report.md's main recommendation is not to move the Instagram budget to TikTok (keep or protect Instagram; test TikTok separately or with a small share), for reasons tied to the corrected comparison and/or the sessions/purchases.
FAIL if report.md endorses moving the Instagram budget to TikTok (fully or mostly), or gives no clear recommendation on it.
