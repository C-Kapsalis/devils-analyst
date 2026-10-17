---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The materials contain 4 planted problems. Answer key (computed from the files):

1. Audit sell-out includes shrinkage. Sell-out is opening + deliveries - closing, so stolen or damaged stock counts as sales. In epos_scan_check.csv, Copperleaf in Coastal 2026-H1 scanned only 79.8% of the audit-derived units (about 20% gap), vs 96.8% in 2025-H1 and over 95% for every other brand/region. Corrected for this, Coastal Copperleaf units changed by about -1% (not +19%). Counts as found if report.md uses the EPOS scan vs audit gap for Coastal Copperleaf (quotes a ratio or gap, or a corrected growth figure near -1%) to say Coastal's growth is overstated.
2. Midvale panel change. The method note says Midvale's 12 discounter stores left the panel in 2026; Copperleaf is weak in discounters, so the share rise (19.3% to 24.5%) is composition. Like-for-like supermarkets: 24.5% vs 24.5%, flat. Counts as found if report.md attributes the Midvale rise to the discounter stores leaving the panel (ideally with a like-for-like figure).
3. AI shopper panel is synthetic and miscalibrated. The validation sheet shows synthetic means 4.6, 4.3, 4.1 vs human pilot 3.9, 3.5, 3.4 (about +0.7 on a 5-point scale) and SDs around 0.3 vs 1.1. Counts as found if report.md says the 4.6/5 should not be used as shopper evidence because synthetic answers run higher and/or far less varied than the human pilot (quoting a number).
4. Coastal price cut. Copperleaf's Coastal shelf price fell from GBP 3.60 to GBP 3.10 (-14%) while other brands/regions rose ~3%. Volume was bought with price; scanned-based Coastal revenue fell about 15%. Counts as found if report.md notes the Coastal price drop for Copperleaf and that growth/revenue must be read with it.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 problems, each with its evidence (a number, a column, or a quote from the files).
FAIL if fewer than 3 are identified with evidence.
