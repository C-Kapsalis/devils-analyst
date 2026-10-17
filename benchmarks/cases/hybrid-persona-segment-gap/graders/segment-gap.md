---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: every one of the 200 personas in personas.csv has subscription_status = "active" (200/200; tenure 3-30 months, all currently receiving boxes). The brief targets subscribers who CANCELLED in the last 6 months. No persona represents the target population, so a synthetic survey with this file answers a different question (what active subscribers think), and its offer ranking is not valid for the win-back decision.

Naive answer: simulates answers from the 200 personas and recommends an offer, e.g. "40% off wins with 61% likely to resubscribe".

PASS if report.md notes that all personas are active subscribers while the brief targets cancelled/lapsed subscribers AND treats this as invalidating the synthetic run (does not present an offer ranking from these personas as the answer).
FAIL if report.md does not mention the mismatch, OR mentions it but still recommends an offer based on simulated answers from these personas.
