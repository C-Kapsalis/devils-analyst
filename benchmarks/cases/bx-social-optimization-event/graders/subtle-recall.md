---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key (computed from the files):

1. Wrong optimisation event. Advantage+ Audience optimises for ADD_TO_CART, so its cost per result (€4.00) is cost per add to cart. Per purchase it costs €57.07 vs €34.80 for the purchase-optimised interest ad sets combined. Found if report.md says the Advantage+ result is add-to-cart (not purchase) and compares on purchases.
2. Fragmented, learning-limited prospecting. Six interest ad sets each get roughly 13-16 purchases a week and are all "Learning limited" (well below the ~50 optimisation events per week Meta needs). Found if report.md recommends consolidating ad sets because of learning-limited delivery / too few conversions per ad set.
3. Audience overlap. "Interest - Clean Beauty" and "Interest - Natural Cosmetics" overlap 61%. Found if report.md flags this overlap (bidding against yourself / merge).
4. Click-to-landing leak. "Interest - Skincare Routine" has the best link CTR (2.45%) but only 46% of link clicks become landing page views (vs 87% elsewhere), and the highest cost per purchase of the interest ad sets (€38.05). Found if report.md flags the landing-page-view drop (page speed / landing page problem) rather than crowning the creative.
5. Retargeting saturating. Retargeting weekly CPM rose from €9.1 to €17.2 while weekly reach fell from 21,400 to 16,500. Found if report.md flags rising CPM with shrinking reach (small/saturated audience).

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 with the specific evidence.
FAIL if fewer than 3.
