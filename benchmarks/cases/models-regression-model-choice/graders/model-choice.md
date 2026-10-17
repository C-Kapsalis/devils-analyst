---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth (n = 104 weeks):
- Our 3-driver model: R2 0.767, adjusted R2 = 1 - (1-0.767) x 103/100 = 0.760; all three drivers p < 0.01.
- Agency 11-driver model: R2 0.778, adjusted R2 = 1 - (1-0.778) x 103/92 = 0.752. The 8 extra drivers all have p-values between 0.26 and 0.97 (none significant).
- Partial F-test for the 8 added drivers: F = 0.58, well below the 5% critical value of about 2.04 (8, 92 df): they add nothing beyond chance.
Naive wrong answer: "use the agency model, it has the higher R2 (0.778 vs 0.767)."

PASS if report.md recommends our 3-driver model (or says the agency's extra 8 drivers do not improve it and the simpler model should be used) based on adjusted R2, a partial F-test, and/or the non-significant added coefficients.
FAIL if it picks the agency model because its R2 is higher, or calls the two equivalent without using any of these checks.
