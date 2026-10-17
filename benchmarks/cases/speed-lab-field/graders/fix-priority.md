---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth fix priority (pages failing field mobile LCP on 2026-10-01, ordered by sessions):
  1. /: field mobile LCP p75 3,424 ms, 182,400 sessions (39.6% of traffic)
  2. /collections/coffee-beans: field mobile LCP p75 3,979 ms, 96,300 sessions (20.9% of traffic)
  3. /products/house-blend: field mobile LCP p75 3,207 ms, 61,800 sessions (13.4% of traffic)
  4. /collections/subscriptions: field mobile LCP p75 2,902 ms, 44,700 sessions (9.7% of traffic)
  5. /products/espresso-roast: field mobile LCP p75 2,712 ms, 28,900 sessions (6.3% of traffic)
All other pages pass field mobile LCP.

PASS if report.md's prioritised fix list starts with "/", "/collections/coffee-beans" and "/products/house-blend" (these three in its top three, in any order), and does not put passing low-traffic pages ahead of them.
FAIL if the top of the list is driven by lab scores or by the slowest low-traffic pages, or if any of those three pages is missing from the top three.
