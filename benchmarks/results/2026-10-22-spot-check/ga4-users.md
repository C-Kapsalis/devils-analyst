# ga4-users

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/metric-definitions/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/ga4-users/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> resources/ga4_daily_by_channel.csv is a GA4 export for September 2026. Write report.md with a table of how many users each channel brought us in September, and one line on which channel matters most.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `users-not-summed` | PASS | PASS | A labels sums an upper bound, not uniques; B labels the column "sum of daily users" and notes uniques are lower |

## Arm A answer (with skill)

````markdown
# September 2026: users and sessions by channel

Answer: Organic Search brought the most users in September: 27,010 summed daily users (51.9%) and 33,012 sessions (52.3%). It is the channel that matters most.

Source: resources/ga4_daily_by_channel.csv, 2026-09-01 to 2026-09-30, 3 channels, 90 rows (no gaps).

| Channel | Users (sum of daily rows) | Share of users | Sessions | Share of sessions |
|---|---:|---:|---:|---:|
| Organic Search | 27,010 | 51.9% | 33,012 | 52.3% |
| Paid Search | 17,568 | 33.7% | 21,079 | 33.4% |
| Email | 7,502 | 14.4% | 9,005 | 14.3% |
| Total | 52,080 | 100.0% | 63,096 | 100.0% |

Caveat on the user column: GA4 users are distinct counts and do not add across days. Each channel figure sums 30 daily distinct counts, so it is an upper bound on September unique users for that channel. The 52,080 total is not September's unique visitor count. Sessions are additive and exact. For true monthly uniques, run one GA4 query over 2026-09-01 to 2026-09-30 grouped by channel only.

Checks: 90 rows = 30 days x 3 channels; sessions exceed users on every row; shares sum to 100.0%.

Method notes: followed hooks/core.md and metric-definitions SKILL.md, read references/catalog.md and references/source-traps.md. A house-rules/ folder exists in devils-analyst but I could not list or read its files with the tools available (Read, Glob, Grep, Write; Glob is unavailable here), so house rules were not applied. Did not read benchmarks/.
````

## Arm B answer (without skill)

````markdown
# September 2026: users by channel

Source: resources/ga4_daily_by_channel.csv (GA4 daily export, 1-30 September 2026, 3 channels).

| Channel | Users (sum of daily users) | Share of total |
|---|---:|---:|
| Organic Search | 27,010 | 51.9% |
| Paid Search | 17,568 | 33.7% |
| Email | 7,502 | 14.4% |
| Total | 52,080 | 100.0% |

Organic Search matters most: it brought the most users in September (27,010, about half of the total).

Note: these are sums of daily users. A user active on several days is counted once per day, so the monthly unique-user count per channel is lower than these figures.
````
