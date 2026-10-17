---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The GA4 exports contain 7 planted problems. Answer key:

1. Data retention at 2 months (data_retention_event_data = "2 months"). Explorations cannot look back further, so the planned 12-month funnel exploration comparing this autumn with last autumn is impossible; the maximum is 14 months and the change is not retroactive. Counts as found if report.md says retention must be raised to 14 months (or names the 2-month limit as blocking the year-over-year exploration).
2. Data-driven attribution on too little volume. reporting_attribution_model = Data-driven, but the purchase outcome is split into two key events, purchase (262) and purchase_app_checkout (185) in 30 days, each under the roughly 400-a-month level data-driven needs, while together they are 447. GA4 falls back to last click without notice, so the budget split read from the "data-driven" report is last click. Counts as found if report.md says the data-driven model is likely not active (falls back to last click) because purchase volume per key event is too low; noting the split into two events (consolidate into one) is the full answer, either point alone counts.
3. Scroll marked as a key event on 2026-08-12. Engagement rate steps from about 53% before that date to about 72% after it, because any session with a key event counts as engaged. The content team's claim that the lookbook pages raised engagement is not supported. Counts as found if report.md links the engagement jump to scroll becoming a key event (and recommends un-marking it or annotating the change).
4. Campaign key split over four spellings: autumn_sale, Autumn_Sale, autumn-sale, "autumn sale " (15,700 sessions, $32,590 revenue in total; the largest single spelling has only $17,008). Counts as found if report.md flags the inconsistent utm_campaign values and recommends one naming convention.
5. Source and medium swapped: rows with session_source = paid_social and session_medium = facebook (8,500 sessions, $10,145 revenue), which breaks default channel grouping (likely Unassigned). Counts as found if report.md flags the swapped utm_source / utm_medium.
6. Untagged display banners. Display spend of $9,558 over four weeks brought only 43 google / display sessions, while Direct sessions rose from about 4,192 to about 5,612 a week in the same weeks. Counts as found if report.md says the display traffic is probably landing in Direct because banner links are untagged (or that display cannot be judged until tagged).
7. Site search tracking off (enhanced_measurement_site_search = off) on a catalogue site; search terms are lost and cannot be backfilled. Counts as found if report.md recommends turning site search on.

List which ones were found in your reasoning.
PASS if report.md identifies at least 6 of the 7 problems, each with its substance (a vague mention such as "check your attribution settings" does not count).
FAIL if it identifies fewer than 6.
