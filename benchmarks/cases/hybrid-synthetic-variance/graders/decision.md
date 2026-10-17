---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Correct decision: do NOT replace the human panel for wave 8. The synthetic panel matches means but fails on spread and correlation structure. Likely causes from generation_notes.md: demographics-only personas, low temperature (0.3), no response history / real answers. Fixes: richer personas (attitudinal or behavioural priors, past answers), higher temperature, retrieval of past survey/qual data; then re-validate against a human wave before any substitution (e.g. run both in parallel again).

PASS if report.md recommends not replacing the human wave now AND names at least one concrete fix (response history, richer personas, higher temperature, retrieval/RAG of real data) AND calls for re-validation against human data before substituting.
FAIL if report.md endorses switching wave 8 to synthetic, even with caveats.
