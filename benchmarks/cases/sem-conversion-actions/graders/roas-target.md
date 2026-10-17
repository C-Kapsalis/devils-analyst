---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth for September 2026 (whole account): ROAS = purchase conversions_value / cost = 128,998.94 / 40,568.34 = 3.18x, which is BELOW the 4x target.
Wrong ROAS figures that make the account look on target:
- conversions_value / cost (includes newsletter_signup lead values of 20 each): 4.16x
- all_conversions_value / cost (adds add_to_cart values): 10.61x
For reference, July was 3.83x and August 3.48x on purchases (declining).

PASS if report.md gives September ROAS of 3.18x (within 3%) and clearly says the account is NOT hitting the 4x target.
FAIL if it reports 4.16x or 10.61x (or anything at or above 4x) as the ROAS, or says the target is met.
