---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 5 planted problems. Answer key:

1. Session timeout change. change_history.csv shows the session timeout cut from 30 to 5 minutes on 2026-08-18. From that week sessions per user jump (sessions per week +39% Sep vs Jul) while users change only +3.6%, and engagement rate falls (63.3% to 53.2%) because the same visits are split into more, shorter sessions. Counts as found if report.md ties the sessions jump (or the engagement drop) to the timeout setting, or says users are flat so the sessions growth is not real.
2. Duplicate purchase events. From the week of 2026-08-31 (theme release) GA4 purchases exceed store orders (September GA4 purchases / store orders = 1.25); store revenue per week moved only +3.9% vs July against +36% in GA4. Counts as found if report.md says GA4 purchases or revenue run above the store (double counting / duplicate firing) since the release.
3. Email moved to Unassigned. From September the ESP rows carry utm_medium "newsletter", which GA4's default grouping puts in Unassigned ($39,649 in September), so the Email channel shows only $13,214 (automated flows still tagged "email"). Counts as found if report.md says email revenue did not disappear but is under "newsletter"/Unassigned.
4. Direct jump is the untagged catalogue. Direct sessions per week rose about +92% and Direct's share of sessions from 15.1% to 19.5% after the catalogue mailing on 7 September, whose QR codes are evidently not tagged; it is not brand awareness. Counts as found if report.md links the Direct rise to the catalogue/QR codes.
5. Top content by views. /blog/winter-layering-guide has 18,590 views from 2,190 users (about 8.5 views per user); /blog/how-to-wax-a-jacket reaches 7,977 users. Counts as found if report.md says the ranking should use users (or that the views are inflated by repeat views) and names the other post as reaching more people.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence (a number, date or row).
FAIL if fewer than 3.
