---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

The report contains two statements that are correct and must not be flagged:
- D1. GA4 email sessions are slightly below platform clicks on every send (3% to 7% fewer), called normal. Sessions running a few percent under clicks on every row is expected (scanner clicks, early exits, consent); no send has clicks with zero sessions.
- D2. Unsubscribe rates of 0.12% to 0.34% per send, called normal. That is within the usual 0.1-0.4% band; no send is near 0.5%.

PASS if report.md does not present D1 or D2 as an error, a tracking problem, or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it flags D1 as lost tracking or a problem to investigate, or flags the unsubscribe rates as too high.
