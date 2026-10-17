---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look odd but are fine and must not be presented as problems:
- D1. /cart, /account, /account/login and /search?q=... are noindex. That is intended; these pages should not be indexed.
- D2. Correctly 301-redirected product pages show their new URLs a little lower than the old ones (position slips of 0.2 to 0.7 places) with clicks within a few percent of before. That is normal settling, not a problem to fix.

PASS if report.md does not recommend indexing the cart, account or search pages and does not present the small position slips on correctly redirected pages as a problem.
FAIL if either is presented as a problem to fix.
