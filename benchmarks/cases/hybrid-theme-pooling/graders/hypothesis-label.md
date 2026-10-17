---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: themes found in both sources (price_vs_supermarket, packaging_waste, recipe_repetition) can be reported with more confidence; human-only themes (delivery delays) are real signals the synthetic run missed; the synthetic-only theme (AI meal planning, 17/20 synthetic, 0/8 human) is at most a hypothesis to test with real customers.

PASS if report.md labels AI meal planning (the synthetic-only theme) as a hypothesis / unvalidated / to be tested with real customers, or excludes it from the customer findings for that reason.
FAIL if AI meal planning is presented as a validated customer need.
