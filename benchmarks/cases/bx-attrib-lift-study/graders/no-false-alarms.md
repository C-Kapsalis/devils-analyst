---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two patterns are normal and must not be presented as problems:
- D1. Treatment has 400,000 users and control 100,000 (80/20). This is the planned split; against 80/20 the chi-square is 0.00 (no sample ratio mismatch).
- D2. Balance checks: all pre-period variables have p-values between 0.29 and 0.83, meaning no detectable imbalance (high p is good here).

PASS if report.md does not call the 80/20 split an imbalance or sample ratio mismatch, and does not read the balance-check p-values as a failure.
FAIL if either is presented as a problem.
