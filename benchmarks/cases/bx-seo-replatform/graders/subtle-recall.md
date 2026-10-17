---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Collection pages are noindexed. All 14 /collections/ URLs return 200 with meta robots "noindex, follow"; they have zero post-migration impressions, and the old /category/ URLs (which earned 26,719 clicks in the 6 weeks before) redirect into them. Counts as found if report.md names the noindex on the collection pages.
2. Missing redirects. Six old product URLs (e.g. /product/arc-floor-lamp.html) return 404 and are not in the redirect map; they lost 1,862 clicks. Counts as found if report.md flags old product URLs returning 404 / missing from the redirect map.
3. Canonical to staging. Three new product pages (/products/cove-candle-cedar, /products/loom-wool-throw, /products/shore-round-mirror) have canonical tags pointing to https://staging-harrowbay.myshopfront.dev. Counts as found if report.md flags the staging canonical.
4. 302 instead of 301. Four old product URLs redirect with 302, so old and new URLs both still collect impressions and split clicks. Counts as found if report.md flags the 302 redirects (or old and new URLs both ranking).
5. Sitemap lists non-indexable URLs. All 14 collection URLs in sitemap_urls.csv are noindex (sitemap and indexability disagree). Counts as found if report.md notes the sitemap contains noindexed URLs (it may be folded into finding 1 if the sitemap conflict is stated).

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 with evidence (URL, status, tag or click number).
FAIL if fewer than 3.
