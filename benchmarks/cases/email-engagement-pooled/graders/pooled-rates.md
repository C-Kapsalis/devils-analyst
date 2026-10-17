---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth for Harbor Outdoor email engagement, July-September 2026 (all campaigns pooled: sum of unique_clicks / sum of delivered, and sum of unique_clicks / sum of unique_opens):
- Pooled unique click rate (CTR) on delivered: 1.28%
- Pooled click-to-open rate (CTOR, unique clicks / unique opens): 7.8%
- Pooled unique open rate on delivered: 16.3%

Wrong numbers produced by common mistakes:
- Simple average of the per-campaign click rates: 3.97% (overstates; ignores that the weekly blast is >90% of volume)
- Average of per-campaign CTOR: 11.1%
- Total (non-unique) clicks / delivered: 1.83%; total clicks / sent: 1.80%
- Unique clicks / sent: 1.263% (small difference, acceptable only if labelled as per-sent)
- Total clicks / total opens as CTOR: 7.2%

PASS if report.md states an overall click rate within 0.10 percentage points of 1.28% (unique clicks / sent at 1.263% is also acceptable) AND either reports CTOR within 1.0 percentage point of 7.8% or does not report an overall CTOR at all.
FAIL if the headline overall click rate is the averaged per-campaign rate (around 3.97%) or a total-clicks rate (around 1.83%), or if no overall click rate is given.
