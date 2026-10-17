---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Organic clicks fell from 57,116 to 28,752 in the 6 weeks after the move (a loss of 28,364). Of that, about 25,392 (90%) is the noindexed collection pages; the 404s cost about 1,862, the staging canonicals about 1,116, and correctly redirected product pages are essentially flat.

The correct top priority: remove the noindex from the collection template (and resubmit those URLs) first, because it is most of the loss.

Naive answers: "wait, migrations take 3-6 months to settle" (the platform partner's line), a generic link-building or content push, or leading with the 404s or a general redirect audit while missing the noindex.

PASS if report.md's first priority is removing the noindex from the /collections/ pages (stated as the main cause of the drop or the largest loss).
FAIL if it recommends waiting for the migration to settle as the main action, if the noindex is missing, or if the first priority is something else (404s, canonicals, links, content).
