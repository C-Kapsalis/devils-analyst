---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Our data team scored all 2,000 Lumio subscribers with a churn model (resources/churn_scores.csv). We have a $15 retention credit. Last quarter's holdout (resources/holdout_summary.csv) showed the credit keeps about 40% of the people who would otherwise have cancelled. Average annual margin per subscriber is about $180. Who should get the credit? Write report.md with the rule and how many subscribers it covers.

Save report.md in the current working directory, not inside resources/.
