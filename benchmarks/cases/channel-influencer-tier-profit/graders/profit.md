---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Profit per post = $22 x orders - fee. POAS = profit / fee.
By follower tier:
- nano (< 10K followers) (n=68): 9.6 orders/post, fee $74/post, profit $138/post, POAS 1.86
- micro (10K-100K) (n=110): 22.8 orders/post, fee $368/post, profit $134/post, POAS 0.36
- macro (100K+) (n=62): 47.0 orders/post, fee $1,860/post, profit $-826/post, POAS -0.44
- Whole program: profit $-113 per post.
Macro creators bring about 5x the orders of nano creators but their fees are far larger, so they LOSE money on average; nano and micro posts are profitable.
Naive wrong answer: "macro creators average 47 orders per post vs 10 for nano, so shift budget to bigger creators."

PASS if report.md computes profit (or POAS / cost per order vs the $22 margin) per post by follower tier (and/or platform) and shows macro creators lose money (around $-826 per post, within 25%) while nano and micro are profitable.
FAIL if it recommends shifting budget toward bigger creators, or ranks creators by orders without accounting for fees and margin.
