---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Cost per lead ranks sources backwards. On mature cohorts (created January-May), cost per opportunity is paid_search $1,183, linkedin_ads $1,452, events $1,435, content_syndication $3,013; closed-won revenue per lead is paid_search $1,517 vs content_syndication $25. Content syndication has the lowest cost per lead ($35) but the highest cost per opportunity. Counts as found if report.md compares sources on cost per opportunity, revenue per lead or return on spend and shows content syndication is weak / paid search strong.
2. MQL-to-SQL from the wrong count. The 10% uses contacts currently at SQL vs currently at MQL; contacts who moved on to opportunity or customer drop out. By stage-entry counts for January-May cohorts it is about 24%. Counts as found if report.md says the snapshot understates conversion and recomputes it (roughly 24%, or from reached_* columns).
3. Webinars judged too early. Webinar leads exist only from August; deals take months to close, so 0 customers is expected. Their opportunity rate so far (12.7%) is comparable to paid search leads of the same age (14.0%). Counts as found if report.md says webinars are too young to judge on customers.
4. List import counted as event leads. In May, events include a create_method = import of 1,400 contacts (badge scans) that barely convert, against about 90 event form leads a month. Counts as found if report.md flags the import inflating event lead counts.
5. Pipeline understated for LinkedIn. 43% of LinkedIn Ads opportunities have no amount, so the review's $1,728,000 LinkedIn pipeline understates it (about $3,042,000 if those opportunities carried a typical amount). Counts as found if report.md flags the missing amounts.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
