---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: baseline before the sale (2-29 Mar 2026) averaged 506 orders/day. During the Spring Sale (30 Mar-05 Apr) orders averaged 903/day (+2,778 orders vs baseline), but for the 21 days after the sale (06 Apr-26 Apr) orders fell to 380/day (-2,656 vs baseline) before recovering to ~500/day. Net incremental orders over the sale plus the following 3 weeks: +122 (using pre+recovery days as baseline: +69). Most of the sale's extra orders were pulled forward from the following weeks.

Naive answer: "orders up 78% during the sale week (+2,778 orders)", treated as the sale's incremental impact, ignoring the post-sale dip.

PASS if report.md identifies the post-sale drop in orders as pull-forward / cannibalisation (or equivalent) AND reports that net incremental orders across the sale plus the post-sale period are small (any figure between -281 and +472 orders, or a clear statement that the dip offset roughly all/most of the sale-week gain).
FAIL if report.md reports the sale-week lift (~78% / ~2,778 orders) as the incremental effect without netting out the post-sale dip, or does not notice the dip.
