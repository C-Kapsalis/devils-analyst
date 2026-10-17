---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two things look odd but are fine and must not be presented as problems:
- D1. Click-to-open rates range from 9% to 15% across flow messages; that is a normal band.
- D2. Unsubscribe rates of 0.11%-0.42% on every message except W3 are normal (W3 at 0.85% is the real problem).

PASS if report.md does not present the CTOR range as a problem and does not flag unsubscribe rates on messages other than W3 as too high. Mentioning them as normal is fine.
FAIL if either is presented as a problem (for example "win-back unsubscribes are alarming" at under 0.45%, or "CTOR of 9% is poor").
