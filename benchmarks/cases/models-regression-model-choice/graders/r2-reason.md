---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: R2 can never go down when variables are added to an OLS model, even pure noise variables; that is why the agency's 11-driver model has a slightly higher R2. Adjusted R2 (or an F-test / information criterion) penalises the extra variables.

PASS if report.md says (in any wording) that R2 always rises or cannot fall when more variables are added, so a higher R2 with more drivers is not evidence of a better model.
FAIL otherwise.
