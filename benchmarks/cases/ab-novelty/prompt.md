---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

We ran the new checkout page test for four weeks (1-28 September 2026): variant A is the current checkout, variant B is the new one, 50/50 split. The resources/ directory has the daily GA4 export, ab_daily.csv (date, variant, user_type, users, conversions).

Did B win, and should we roll it out? Write report.md with the result (the lift in conversion rate and whether it's real) and your recommendation.

Save report.md in the current working directory, not inside resources/.
