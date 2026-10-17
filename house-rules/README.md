# House rules

The shipped checks know what goes wrong in most marketing data. They cannot
know what goes wrong in yours: that your revenue of record is finance net
revenue, that campaigns starting `BR_` are brand, that your payment page
lives on another domain, that the "purchase" key event double-fired for a
month last spring. A senior analyst carries those in their head. House rules
write them down, so the agent reads them before it touches a number and a new
colleague does not have to learn them the expensive way.

## How the agent uses them

`route-question` and `metric-definitions` read house rules first, before the
inventory and before any metric is defined. They look for a `house-rules/`
folder at the root of the project or workspace the agent is working in and
read every `.md` file there except `README.md`, `TEMPLATE.md` and anything in
`examples/`. In a chat without files (Claude web, ChatGPT), paste the rules or
add them to the project's knowledge.

The folder in this plugin holds only this README, the template and two
fictional examples. Nothing in it is applied to your data.

## Precedence

Highest first:

1. What you say in the conversation.
2. Your house rules.
3. Your governed definitions: a Power BI model (`power-bi-definitions`), a
   metric dictionary.
4. The shipped defaults: the skills, their checks and catalogs.

A house rule replaces the shipped check or definition it names in
`overrides:`, and any default it contradicts. One thing it cannot do is make
arithmetic true that is false. If a rule seems to require averaging rates or
summing daily users, the agent reports the rule's number, shows the
core-rule number next to it and says why they differ. Findings and scope
lines cite the rule id that changed them, so you can always see where a
number came from.

## Writing one

Copy [TEMPLATE.md](TEMPLATE.md) to `house-rules/HR-<number>-<short-name>.md`
in your own project, one rule per file. The fields are the same columns as the
shipped audit tables (what to check, where to look, the red flag, why it costs
money, the fix), plus a source, an owner and a date. Two examples:

- [HR-001](examples/HR-001-revenue-of-record.md) replaces a shipped default:
  ROAS is computed on finance net revenue, not store gross revenue.
- [HR-002](examples/HR-002-checkout-domain-referrals.md) adds a check the
  shipped GA4 checks cannot know: the team's payment domain showing up as a
  referral source.

Write the red flag so two analysts would agree whether it fired: a number, a
column, a condition. "Engagement looks off" is not a red flag; "engagement
rate steps down more than 5 points in a week with no change in users" is.

## Growing them

- **After an incident.** When a number was wrong and someone found out why,
  that is a rule. Write it the same week, with the incident as its source.
- **After a review.** When a reviewer corrects an analysis for a reason the
  checks did not cover, ask whether it is a one-off or a rule.
- **On a date.** Each rule carries the date it was last confirmed. Re-read
  the old ones each quarter: a renamed column or a retired setting makes a
  rule wrong without anyone noticing, and the agent flags such rules to their
  owner instead of applying them.
- **Upstream.** A rule that would hold for most teams (not just yours) belongs
  in the shipped checks. [CONTRIBUTING.md](../CONTRIBUTING.md) says how to
  propose it, with a benchmark case that plants the problem.

A planned, optional loop that proposes house-rule changes from your own past
analyses, one at a time and only with your approval, is described in
[docs/self-improving.md](../docs/self-improving.md). It is not built yet.
