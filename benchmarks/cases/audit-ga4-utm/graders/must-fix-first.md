---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Three problems are Must-fix because they make later GA4 numbers wrong or unrecoverable:
- A. Data retention at 2 months (blocks the planned 12-month exploration; not retroactive).
- B. Data-driven attribution selected while purchase (262) and purchase_app_checkout (185) are each under about 400 a month, so the model in effect is last click.
- C. Scroll marked as a key event on 2026-08-12, inflating engagement rate from about 53% to about 72%.
The lesser problems are: the untagged display banners and site search being off. (The campaign-name spellings and the swapped source/medium may sit in either group.)

PASS if report.md flags all of A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND its closing "fix first" line (or explicit first priority) names A, B or C.
FAIL if any of A, B or C is missing, labelled lower severity (Should fix, Nice to have, minor), listed after one of the lesser problems, or if the first fix named is something other than A, B or C.
