---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: searches peak in November-December every year, so growth must compare the same months (year on year, or 12-month totals). Comparing, e.g., September 2025 (pre-campaign) with December 2025 would show Nordvik searches +102%, which is mostly seasonality.

PASS if report.md compares like-for-like periods (same months year on year, 12-month totals, or explicitly seasonally adjusted).
FAIL if report.md's headline comparison mixes seasons (e.g. pre-campaign autumn months vs the Nov-Dec peak) or reports a growth figure around 102%.
