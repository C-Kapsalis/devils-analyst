---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: two Harbor Outdoor pages compete for the same queries (keyword cannibalization) on 16 of the 20 hiking-boot queries:
- https://www.harboroutdoor.com/collections/hiking-boots (impression-weighted web position 6.7, 2,279 web clicks)
- https://www.harboroutdoor.com/blog/best-hiking-boots-2026 (impression-weighted web position 8.9, 579 web clicks)

PASS if report.md identifies that the collection page and the blog post both rank for the same hiking-boot queries (cannibalization / competing pages / split signals) and recommends consolidating or differentiating them (e.g. canonical, internal linking, merging, re-targeting the blog to informational queries).
FAIL if report.md does not mention that two of our pages compete for the same queries.
