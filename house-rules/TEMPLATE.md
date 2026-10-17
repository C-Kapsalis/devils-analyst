---
id: HR-000
area: paid-search
overrides: none
check: One sentence that says what to check.
where_to_look: The column, setting or report, with its exact name and where it lives.
red_flag: The threshold that makes it a finding, as a number or a condition you can test.
why_it_costs_money: What goes wrong in a decision, a budget or a report if nobody checks.
fix: What to do when the red flag shows, and how to verify the fix.
source: Where this comes from (an incident, a platform doc, a finance policy), with a link or a date.
owner: Who answers questions about this rule (a name or a role).
date: YYYY-MM-DD
---

<!--
One rule per file. Save it as house-rules/HR-<number>-<short-name>.md in your
own project, not in this plugin's folder.

Fields:

- id: unique within your rules, for example HR-014. Findings cite it.
- area: one of paid-search, pmax, meta, ga4-utm, search-console, email,
  crm-lifecycle, ecommerce-revenue, experiments, attribution, dashboards,
  power-bi, or a new area your team uses.
- overrides: the shipped check or definition this rule replaces, as
  <file>:<check id> (for example audit/ga4-utm:GA2, or
  metric-definitions/catalog:ROAS), or "none" for a new check.
- check, where_to_look, red_flag, why_it_costs_money, fix: the same columns
  as the shipped audit tables (Look at, Red flag, Why it costs money, Fix).
  Write the red flag so two analysts would agree whether it fired.
- source: an incident, a document, a decision. "We have always done it this
  way" is not a source.
- owner and date: who to ask, and when it was last confirmed true. A rule
  that names a column or setting that no longer exists gets flagged to its
  owner, not applied.

Optional body below the frontmatter: two or three sentences of context, the
query that tests the red flag, or the incident that taught the team.
-->
