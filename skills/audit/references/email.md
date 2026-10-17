# Email program and deliverability

Read top-down and stop at the first broken transition: sent to delivered,
delivered to opened, opened to clicked, clicked to revenue. Never optimise a
subject line on a program that is failing to deliver.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| E1 | Delivered / sent per send | Below 95% | Every later rate measures a smaller audience; a reputation problem wearing a good open rate | Stop creative tests; fix authentication, list and complaints | 1 |
| E2 | SPF, DKIM, DMARC: present and passing | Any missing, failing, or set but never verified | Required for bulk senders at Google and Yahoo since February 2024; mail filtered or rejected | Set all three; confirm each passes | 1 |
| E3 | Complaints / delivered per send | Any send above 0.1% (0.3% is critical), even if the monthly average is under | The one rate that can take the program off the air | Cut frequency to that segment; tighten consent | 1 |
| E4 | Bounce rate trend at steady volume | Rising send after send while volume is flat, even under 2% | Hygiene lapsed; delivery falls next | Verify and suppress dead addresses | 2 |
| E5 | Hard bounces | Any address hard-bounced twice | Repeated sends to dead addresses hurt reputation | Suppress on the first hard bounce | 2 |
| E6 | Dormant contacts (no open or click in about 12 months) in main sends | Mixed into the main newsletter; win-back stats blended into averages | Spam traps and complaints poison placement for the engaged list | Separate win-back send; delete after one or two silent campaigns | 2 |
| E7 | Open rate as the verdict | Campaigns ranked or judged on opens | Opens fire on previews and privacy features; directional only | Judge on clicks and revenue | 4 |
| E8 | Pooled click rate | Program click rate dominated by the largest send | Overhauling a program when one send is the problem | Click rate per send against a 2-5% band | 3 |
| E9 | Wrong lever | Subject-line tests when CTOR is the leak; body rewrites when CTOR is fine and click rate is low | Effort on the wrong step | Opens lag = subject, sender, timing; CTOR lags = body, offer, CTA; low clicks with fine CTOR = narrow the audience | 3 |
| E10 | Net list growth: (new - unsubscribed - cleaned) / list at start, monthly | Flat or negative while campaign rates are steady | Rates measure survivors; the audience is shrinking | Track the sign monthly | 2 |
| E11 | Unsubscribe rate per send | Above about 0.5% on a send | Relevance or frequency problem | Segment; lower frequency | 3 |
| E12 | Sends ranked by clicks | The top-click send has the lowest revenue and revenue per buyer | The wrong format gets repeated | Rank by revenue and revenue per purchaser | 3 |
| E13 | UTM coverage: ESP campaign names vs analytics campaign names | Sends with clicks and zero sessions; revenue under a near-identical name | Email revenue goes uncredited; budget moves away | Exact name match; tag every link | 2 |
| E14 | Lifecycle vs blast mix | One email for day-one subscribers and lapsed customers; no welcome, nurture or win-back flows | Flows out-convert blasts; blasts drive attrition | Build the flows | 3 |
| E15 | Win-back flow exit rule | Lapsed contacts mailed indefinitely | Spam-trap risk with no return | Rejoin on open or click; delete after one or two silent sends | 2 |
| E16 | Campaign ages | A campaign sent a day ago ranked against month-old ones on lifetime totals | Wrong winner | Compare at the same accrual window | 4 |
| E17 | Compliance | Missing or broken unsubscribe link or postal address | Legal and deliverability risk | Fix before the next send | 1 |
| E18 | ROI claims | Industry "36 per 1" used as the program's own return | Budget set on someone else's number | Own attributed revenue per send | 4 |

## Decoys

Unsubscribe 0.1-0.4% per send; CTOR 8-15%; sessions slightly under clicks on
every row; open rate trending down with a privacy caveat; complaint rate under
0.1% on every send.
