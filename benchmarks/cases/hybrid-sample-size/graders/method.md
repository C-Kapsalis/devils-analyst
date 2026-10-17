---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

PASS if report.md shows the sample-size formula or a standard power calculation (e.g. n = 2(z_alpha/2 + z_beta)^2 sigma^2 / delta^2, or the 16 sigma^2 / delta^2 rule) with the inputs used.
FAIL if a number is given without any formula or power-calculation inputs.
