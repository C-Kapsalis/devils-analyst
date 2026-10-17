---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth for queries containing "hiking boot" (20 queries), Google web search, July-September 2026, from the query-level export gsc_query.csv (search_type = web):
- Impressions (search demand we appear for): 83,216
- Clicks: 2,858
- Organic CTR: 3.43%

Wrong numbers produced by common mistakes:
- Summing query x page rows (double counts searches where two of our pages appear): web-only 118,417 impressions; all search types 378,148 impressions.
- Including image and video search: query-level all types 273,393 impressions with CTR 1.33%; from summed query x page rows CTR 0.96%.
- Web CTR from summed query x page rows: 2.41%.

PASS if report.md reports web-search impressions for hiking-boot queries within 3% of 83,216 AND an organic CTR within 0.3 percentage points of 3.43%. Also reporting an all-search-types impression total of about 273,393 is fine as long as it is not the headline CTR basis.
FAIL if the headline impressions/demand figure is a summed query x page total (118,417 or 378,148), or the headline CTR is an all-search-types figure (about 1.33% or 0.96%), or either number is missing.
