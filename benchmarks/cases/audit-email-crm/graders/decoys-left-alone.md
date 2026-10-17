---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three patterns in the exports are normal and must not be flagged:
- D1. Unsubscribe rates per send between 0.17% and 0.31%: inside the normal band (problem only above about 0.5%).
- D2. Click-to-open rates (unique clicks / unique opens) between 9.8% and 12.0%: inside the normal 8-15% band.
- D3. GA4 sessions 3-8% below ESP unique clicks on every send that joins by name: normal (some clicks never load the page).

PASS if report.md does not present D1, D2 or D3 as an error, a problem or something to fix. Mentioning them as normal or checked is a PASS. (Flagging the Autumn Collection name mismatch, where a send has no matching GA4 row at all, is a different problem and is fine.)
FAIL if it calls the unsubscribe rates too high, the CTOR weak, or the small click-to-session gap a tracking loss to fix.
