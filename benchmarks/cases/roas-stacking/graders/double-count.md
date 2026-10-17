---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: total paid cost 31,100. Google Ads plus Meta claim 123,600 of conversion value (platform ROAS 3.97), but Shopify recorded only 84,600 of net sales for the whole store, so the platforms claim about 1.46x the revenue that exists: their attributions overlap. ROAS on Shopify revenue is at most 84,600 / 31,100 = 2.72 (and that credits paid media with all store revenue).

PASS if report.md points out that the platforms' combined claimed revenue exceeds Shopify's actual sales (double counting / overlapping attribution) and does not present 3.97 as the true total ROAS.
FAIL if it reports summed platform ROAS (about 3.97) as the answer without flagging the overlap.
