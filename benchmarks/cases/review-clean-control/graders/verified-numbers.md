---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

PASS if report.md shows it checked the report against the data: it states at least two specific figures it recomputed or confirmed from the exports (for example generic cost per purchase €26.23, total CTR 7.1%, email click rate 3.41%, median order value €40.30), and those figures agree with the report (within rounding).
FAIL if it confirms no specific figure from the data, or the figures it gives disagree with these values.
