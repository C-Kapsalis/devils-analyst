---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

The resources/ directory has our September 2026 paid-media spend for Lumen Streaming, spend_sep.csv (channel, spend), and our trial export, trials.csv (user_id, trial_start, channel, converted_at, monthly_price), pulled on 20 October 2026. converted_at is when the free trial turned into a paid subscription (blank = did not convert). Gross margin is 70%.

What's our CAC by channel for September, and which channel pays back fastest? Write report.md with CAC and payback by channel and where you'd shift budget.

Save report.md in the current working directory, not inside resources/.
