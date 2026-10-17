---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Required n for a +/-2 point margin at 95% confidence = 1.96^2 x p(1-p) / 0.02^2.
- With p = 0.38: 2,263 completes PER read. The board wants separate UK and Germany reads, so about 2,263 per country, 4,526 in total.
- Also acceptable: worst case p = 0.5 -> 2,401 per country (4,802 total), or each country's own awareness (UK 40% -> 2,305; DE 36% -> 2,201).
Naive wrong answers: scaling linearly, 400 x 4.8/2 = 951; or 2,263 in total split across the two countries (about 1,131 each).

PASS if report.md's per-country requirement is between 2,141 and 2,451 (total about 4,282 to 4,902).
FAIL if the total is under 2,500, or the per-country figure is about 951 or about 1,131.
