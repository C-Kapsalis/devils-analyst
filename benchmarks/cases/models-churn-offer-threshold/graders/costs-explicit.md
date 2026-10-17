---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: the two errors have different costs. Sending a credit to someone who would stay wastes $15; missing a churner loses about 0.4 x $180 = $72 of expected margin. A 0.5 cut-off only makes sense if both errors cost the same.

PASS if report.md states both error costs (about $15 and about $72, or per-customer equivalents) and says that using 0.5 (or the model's default) assumes equal costs / is not right here.
FAIL if it does not state both costs explicitly.
