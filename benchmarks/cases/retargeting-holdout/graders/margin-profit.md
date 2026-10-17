---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: at AOV 76 and gross margin 42%, the retargeting campaign's incremental gross profit in September is -13,439 (negative): incremental revenue 15,428 x 0.42 = 6,480 against 19,919 spend. Break-even iROAS is 2.38.

PASS if report.md uses the margin to show the campaign is unprofitable on an incremental basis (negative incremental profit of roughly -13,439, within 20%, or iROAS 0.77 below the 2.38 break-even).
FAIL if it ignores margin entirely, or claims the campaign is profitable.
