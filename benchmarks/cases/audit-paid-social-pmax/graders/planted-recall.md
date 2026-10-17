---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 6 planted problems. Answer key:

1. Stacked platform revenue. The headline "combined Meta + Google revenue" adds Meta's self-reported purchase value (€87,363, mostly on a 7-day click + 1-day view window) and Google's conversion value (€114,582) = €201,945, which is above Shopify's total sales for all channels (€139,839). Counts as found if report.md says the platform revenues overlap or exceed the Shopify total and cannot be added.
2. PMax conversions are blended and brand-heavy. PMax "conversions" (1159) include 785 newsletter sign-ups; only 374 are purchases. Of the purchases, 250 (67%) came from brand queries, and brand_exclusions is "none". PMax CPA is €8 on all conversions but €26 on purchases. Counts as found if report.md says PMax must be read on purchases only (sign-ups mixed in) OR says most PMax purchases are brand queries with no brand exclusion; full credit needs either point with its number.
3. Attribution settings differ. "Prospecting - Lookalike 2%" runs on 1d_click while the others use 7d_click_1d_view, so ROAS per ad set is not comparable; the agency plans to pause it for the lowest ROAS (3.05x). On the shared purchases_1d_click column it has the most purchases per spend of the prospecting ad sets (25.54 per €1,000 vs 14.60 for the next best). Counts as found if report.md says the attribution windows differ so the ROAS comparison or the pause decision is invalid.
4. CTR on all clicks. The quoted Meta CTR 3.57% uses clicks_all (likes, profile taps); link CTR is 28,565 / 2,235,110 = 1.28%. Counts as found if report.md says CTR should use link clicks, with a figure near 1.28% (within 0.15 points) or the reason.
5. Creative fatigue. Prospecting weekly frequency rose from 1.9 to 5.9 while link CTR fell from 1.62% to 0.84%. Counts as found if report.md names rising frequency with falling link CTR (fatigue) and asks for creative rotation or a cap.
6. Retargeting audience. "Site Visitors 540d" keeps people 540 days, does not exclude purchasers and has no frequency cap. Counts as found if report.md flags at least the missing purchaser exclusion or the 540-day membership.

List which ones were found in your reasoning.
PASS if report.md identifies at least 5 of the 6 problems, each with its substance (a vague mention such as "review your Meta setup" does not count).
FAIL if it identifies fewer than 5.
