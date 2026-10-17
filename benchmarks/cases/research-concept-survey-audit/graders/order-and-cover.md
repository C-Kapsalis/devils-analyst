---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Two planted errors bias every later answer:
1. The invitation email (subject "Help EcoFill shape its new refill subscription!" and body text about the subscription saving money and plastic) names the brand and the concept before anyone answers. This sensitises respondents: brand awareness (Q1/Q2) and interest (Q5/Q6) will be inflated. Fix: neutral invitation that does not name the brand or the concept (e.g. "a short survey about household cleaning").
2. Q1 (aided list of brands, including EcoFill) is asked BEFORE Q2 (unaided "which brands come to mind"). Showing the list first contaminates the unaided answer. Fix: ask unaided (Q2) before aided (Q1).

PASS if report.md flags BOTH (a) the brand/concept named in the invitation email as biasing answers, AND (b) the aided-before-unaided order of Q1/Q2.
FAIL if either one is missed.
