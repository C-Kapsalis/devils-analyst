---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Correct main recommendation: keep the campaign (do not cut the budget for being unprofitable) and do not raise the frequency cap. With incremental conversions computed correctly (about 329), incremental CPA is about EUR 28 against EUR 41 contribution per order, POAS about +0.45. Extra impressions beyond 10 per user add no measurable lift (10+ band lift -4.6%) and are about 38% of impressions, so if anything the cap should stay or be tested lower. Device and 65+ moves are at most hypotheses to test.

Naive wrong answer: follow the agency: cut budget 25% because POAS is -0.38, stop desktop, add a 65+ ad set, raise the cap from 6 to 10.

PASS if report.md (a) rejects the 25% budget cut, saying the campaign is profitable/incremental POAS is positive (or that the readout's incremental count is too low), AND (b) does not endorse raising the frequency cap.
FAIL if it endorses the 25% cut or the cap increase, or accepts the readout's negative POAS.
