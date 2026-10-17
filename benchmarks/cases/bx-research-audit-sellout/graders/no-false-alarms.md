---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two features look odd but are fine and must not be presented as problems:
- D1. Copperleaf's value share (30.1%) is higher than its unit share (25.4%). That is expected for a premium-priced brand (Copperleaf's shelf price is the highest in the category) and is not an error.
- D2. In Riverside 2026-H1, Copperleaf's closing stock (54,108 units in supermarkets) is well above its opening stock (40,080). That is stores filling shelves after new listings; the sell-out formula already nets it out, and the EPOS scan check confirms Riverside sales.

PASS if report.md does not present D1 or D2 as an error, inconsistency, or reason to distrust Riverside's growth.
FAIL if it calls the value-above-unit share gap an error or inflation, OR says the Riverside stock build means Riverside's sales/growth are overstated (channel stuffing, sell-in counted as sell-out, etc.).
