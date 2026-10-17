---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: December 2026 revenue $249,957 is +37% on November ($181,802), but every December is the seasonal peak (seasonal index about 1.77 vs November 1.29). Underlying growth is about 1.0% a month: December 2026 vs December 2025 is +11.5%, and full-year 2026 vs 2025 is +12.8%.

PASS if report.md states underlying growth of roughly 0.7% to 1.3% a month or roughly 9% to 16% year on year, and attributes the +37% December jump to seasonality.
FAIL if it treats December's +37% as growth / momentum, or gives a growth rate above 25% a year.
