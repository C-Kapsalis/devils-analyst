---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Total email revenue across the eight ESP campaigns, after merging spelling variants, is $30,543. An exact-string join only finds $13,316 (44%).
PASS if report.md either states total email campaign revenue within 5% of $30,543, or explicitly notes that GA4 campaign names have inconsistent spelling/case/hyphenation that had to be merged (or flags this as a tracking issue to fix).
FAIL if it reports total email revenue near $13,316 or otherwise shows no awareness that rows with variant campaign spellings were dropped.
