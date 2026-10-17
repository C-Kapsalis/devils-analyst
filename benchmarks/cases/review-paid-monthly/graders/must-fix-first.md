---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two of the problems are Must-fix because they change the decision in the report:
- A. Blended ROAS 5.36x built from Google + Meta self-reported revenue (€87,621) that exceeds total Shopify revenue (€68,195).
- B. Google CPA €6.62 counts newsletter and account sign-ups; the purchase CPA is €17.51 and generic purchase CPA €41.76 is above the €30 target, so "scale generic +30%" is wrong.
The lesser problems are: the averaged CTR, the carousel causal claim, and display judged on CTR.

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the report can be sent as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves sending the report unchanged.
