---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three patterns in the exports are normal and must not be flagged:
- D1. Retargeting ROAS (9.07x) several times prospecting ROAS (3.48x). Expected: retargeting closes demand that prospecting created.
- D2. CPMs between €6.60 and €11.90, and weekly prospecting CPM flat around €8: normal for Meta.
- D3. Link CTR around 1.3% at account level: inside the normal 0.8-2.5% band.

PASS if report.md does not present D1, D2 or D3 as an error or something to fix. Mentioning them as normal is a PASS. Suggesting a holdout test before scaling retargeting is acceptable.
FAIL if it treats the retargeting-vs-prospecting ROAS gap as a problem in itself or recommends moving prospecting budget to retargeting because of it, calls the CPMs too high, or calls the link CTR weak.
