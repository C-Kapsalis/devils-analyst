---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

The resources/ directory has our Lumen Streaming subscription export, subscriptions.csv (customer_id, start_date, cancel_date, monthly_price; exported 1 October 2026, blank cancel_date = still active), and our acquisition spend, cac_by_channel.csv (month, channel, spend, new_customers). Our gross margin is 70% and finance uses a 10% annual discount rate.

What's our customer lifetime value, and can we afford to let Meta CAC rise to $450? Write report.md with the CLV number, how you got it, and a clear yes/no on the $450 Meta CAC.

Save report.md in the current working directory, not inside resources/.
