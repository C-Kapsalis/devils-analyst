---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: Q3 ("How much did you enjoy our new, faster bank sync?") is leading/loaded: it presumes the respondent enjoyed it and asserts the bank sync is "faster". In the synthetic pilot 38 of 40 answered 5 (SD 0.22), a symptom of the wording, not proof of delight. Fix: neutral wording, e.g. "How would you rate the speed of bank sync?" or "How satisfied are you with bank sync?", without praising the change.

PASS if report.md flags Q3 as leading / loaded / presumptive (it assumes enjoyment and/or calls the sync faster) AND proposes neutral wording.
FAIL if Q3 is not flagged, or is only dropped/flagged for low variance without naming the wording problem.
