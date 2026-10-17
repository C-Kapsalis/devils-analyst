---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth monthly churn = cancellations during a month / customers active at the start of that month. Over Oct 2025-Sep 2026 this is 387 / 6,009 = 6.4% per month (any figure from 5.5% to 8.0% computed this way is fine; a single recent month in that range is fine too).

Naive (wrong) churn figures, which divide by every customer who ever subscribed: 38 September cancellations / 1,355 customers ever = 2.8% per month; or average monthly cancellations / all customers ever = 1.8%.

PASS if report.md uses a monthly churn rate between 5.5% and 8.0% for its CLV.
FAIL if report.md uses a churn rate around 2.8% or 1.8% (or anything below 4.5%), or does not state a churn rate.
