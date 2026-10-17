---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: in the human data items q1-q4 correlate strongly with each other (r 0.55-0.65) and q5-q8 likewise (r 0.48-0.58); in the synthetic data all inter-item correlations are near zero (-0.11 to +0.10). Mean absolute difference between human and synthetic correlation matrices: 0.38 (well above a ~0.2 tolerance). The synthetic panel does not reproduce how attitudes hang together, so segment or driver analysis would be wrong.

PASS if report.md reports that inter-item correlations in the synthetic data are near zero / much weaker than the clear positive human correlations (or a correlation-matrix difference above 0.2).
FAIL if correlations are not checked, or are described as similar.
