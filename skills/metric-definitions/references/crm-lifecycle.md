# CRM, lifecycle and pipeline metrics

The playbooks do not cover CRM pipelines, so most definitions here are standard
practice **[std]**; lines from the author's notes are marked *(notes)*. Applies
to HubSpot, Salesforce and similar CRMs.

## Grain first

A CRM holds three different grains. Never mix them in one ratio without saying
so.

| Object | One row per | Typical questions |
|---|---|---|
| Contact (lead) | person | how many leads, MQLs, SQLs; conversion between stages; lead source |
| Company (account) | organisation | accounts engaged, accounts with pipeline (account-based marketing) |
| Deal (opportunity) | sales opportunity | pipeline value, win rate, deal size, cycle length |

A contact can have several deals; a deal can have several contacts. Counting
"leads that became customers" goes through the association, and double-counts
if a contact sits on two deals.

## Lifecycle stages are a ratchet

HubSpot lifecycle stages (subscriber, lead, MQL, SQL, opportunity, customer,
evangelist) normally only move forward, and contacts can skip stages. A
snapshot of the *current* stage undercounts everyone who passed through a stage
and moved on.

- **Count by the date the stage was entered** (HubSpot keeps one timestamp
  property per stage), not by today's stage.
- **Cohort by creation month**: a lead created last week has not had time to
  become an opportunity. Compare stage conversion at the same age, the way
  cohorts are compared in customer analytics.
- A contact that skipped MQL and went straight to SQL counts as reaching MQL
  for funnel conversion (it passed the threshold), or is reported separately;
  say which.

## Definitions

| Metric | Formula | Caveat |
|---|---|---|
| New leads | contacts created in the period (excluding imports, test and internal contacts) | Imports and list uploads inflate it; filter by creation source |
| MQLs | contacts that entered MQL in the period | The MQL rule is the company's own; state it |
| Stage conversion (N to N+1) | contacts in a creation cohort that reached stage N+1 / contacts in that cohort that reached stage N | Same cohort, same age; never this month's SQLs / this month's MQLs |
| Lead-to-customer rate | cohort contacts that became customers / cohort leads | Long cycles: report at 30 / 90 / 180 days |
| Pipeline created | sum of amount of deals created in the period | Deals without amount: count them and report the gap |
| Open pipeline | sum of amount of open deals at a date | A stock, not a flow: never sum across months |
| Win rate | closed-won / (closed-won + closed-lost), by close date | Excluding open deals; state whether by count or by value |
| Average deal size | closed-won amount / closed-won deals | |
| Sales cycle length | median days from deal creation to close (won) | Median, not mean: a few stalled deals skew the mean |
| Pipeline velocity | open opportunities x win rate x average deal size / sales cycle length (days) | Revenue per day the current pipeline should produce |
| Pipeline coverage | open pipeline due in the period / revenue target for the period | Coverage of 3x is a common heuristic, not a law |
| Cost per lead / MQL / SQL | marketing spend / leads (MQLs, SQLs) in the period | Join spend after aggregation, by source and month |
| Cost per opportunity, CAC (B2B) | spend / opportunities created; spend / new customers | Lag: this month's spend creates next quarter's customers. Use a lagged or cohort view, and say which |
| Revenue per lead by source | closed-won amount from a source cohort / leads in that cohort | The honest way to compare sources: volume x quality |

## Source attribution in the CRM

- **Original source** (first known touch) and **latest source** answer
  different questions: what introduced the lead vs what brought them back.
  Name the one you use.
- *(notes)* For long B2B cycles, a W-shaped model gives 30% to the first touch,
  30% to the lead-creation touch (form fill, demo request), 30% to the touch
  that created the opportunity or closed it, and 10% across the rest. Any model
  is credit, not cause.
- Join ad spend to CRM sources on a mapped source name (paid search, paid
  social, organic, email, referral, direct), aggregated per month, never row by
  row.

## Insight patterns

- **MQLs up, SQLs flat**: the MQL rule loosened, or a new source sends volume
  without fit. Check stage conversion by source.
- **Win rate down, pipeline up**: quality traded for volume. Check win rate by
  source and deal size band.
- **Cycle length stretching**: deals stalling at one stage. Find the stage with
  the largest rise in median days.
- **Cost per lead falling, cost per opportunity rising**: cheap leads that do
  not progress. Judge sources on cost per opportunity or revenue per lead.
- *(notes)* "Potential is a ceiling, forecast is a bet, quota is a goal." Set
  targets against potential, not against last year's result.
- *(notes)* Judge a team only on the stages it controls: marketing on lead
  volume and quality, sales on conversion after acceptance.
