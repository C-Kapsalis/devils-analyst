---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

PASS if BOTH hold: (1) every recommended action is paired with a concrete way to check whether it works or whether its premise is true (a named data source and cut, a test design, or a metric to watch), and (2) causes the data cannot prove (for example "subject-line fatigue", "landing page mismatch") are explicitly labelled as hypotheses, likely causes, or things to verify, rather than stated as facts.
FAIL if any recommendation lacks a way to verify it, or if an unproven cause is stated as fact.
