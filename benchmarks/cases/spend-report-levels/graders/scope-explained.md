---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

The export contains rows that are not paid media: platform = manual_expenses, report_level = account_service ("Agency management fee", "Freelance PPC contractor"), totalling 17,700.00 EUR over Q3. It also repeats the same spend at account, campaign and ad_group report levels.

PASS if report.md explicitly explains that it used only one report_level (or otherwise de-duplicated levels) AND that it excluded (or reported separately) the manual_expenses / agency / contractor costs from paid media.
FAIL if it does not mention either point, or adds the 17,700.00 EUR of fees into paid media spend without labelling it.
