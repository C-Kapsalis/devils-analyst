---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Two of the problems are Must-fix because each drives a Q4 budget ask:
- A. Slide 2: Paid Social +25% justified by "data-driven attribution" while GA4 is effectively on last click (purchase key event 224 in 30 days; Data-driven rows identical to Last click).
- B. Slide 3: YouTube +40% justified by viewers 4.46% vs non-viewers 1.53%, an exposed vs unexposed comparison that cannot show causation.
The lesser problems are: the 13-month exploration vs 2-month retention, the engagement jump from scroll becoming a key event, and the served-market share.

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the deck can be presented as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves the deck unchanged.
