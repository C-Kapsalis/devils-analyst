---
name: marketing-dashboard
description: >-
  Use this skill before analysing or reporting on ANY marketing data, even when the task
  looks simple: CSV or spreadsheet exports, or connector data, from email platforms
  (Klaviyo, Mailchimp, Brevo, HubSpot email), ad platforms (Google Ads, Meta, LinkedIn,
  TikTok), GA4, Search Console, HubSpot or another CRM, Shopify or a warehouse. Triggers
  include performance reports, dashboards, "how did X do this month", campaign or channel
  reviews, client reports, CAC, ROAS, CTR, conversion, SEO or pipeline questions, and any
  use of Claude Dashboards on marketing data. It sets which questions to answer, which
  definitions and comparisons are correct, how to explain what changed, and how to end
  with what to do.
---

# marketing-dashboard

A good marketing dashboard answers a question someone will act on. It leads
with the answer, shows the evidence in the order you would read it, and ends
with what to do. Everything else is decoration.

Work through the steps in order. Steps 1-3 happen before the first query.

## 1. Pin the question, the reader and the period

Ask only what you cannot infer, in one message:

- **Question**: "how did paid search do last month", "why are leads down",
  "weekly marketing pulse". Map it to one or more sections of
  [references/questions.md](references/questions.md); each section lists the
  questions a good analyst answers for that discipline and the cut that answers
  each.
- **Reader**: an executive (5 numbers, what changed, what to do), a channel
  owner (the drill-down that names the broken branch), a client (the same, plus
  plain language and no internal jargon).
- **Period and comparison**: default to the last complete week or month against
  the period before it, and the same period last year when the business is
  seasonal. State it in the subtitle.
- **Business model**: it picks the top metric. A store leads with revenue,
  conversion, ROAS and repeat; lead generation with qualified leads, cost per
  qualified lead and pipeline; a publisher with sessions, engagement and reach.

## 2. Inventory the data

List which sources are connected and what each can answer.
[references/connectors.md](references/connectors.md) gives, per source, the
tables to request, their grain, and what each cannot tell you (GA4 has no cost,
ad platforms have no margin, Search Console has no conversions). If a source the
question needs is missing, say which, and either proceed with what exists
(labelled) or ask for an export.

## 3. Define before you query

Use the `metric-definitions` skill: write the metric dictionary for the metrics
this dashboard needs. If the team has a Power BI model on the same data, use the
`power-bi-definitions` skill so the dashboard matches the report everyone else
reads.

## 4. Pull and compute

- Request each source at the grain you will display (non-additive counts such as
  users and reach cannot be re-aggregated later).
- Aggregate each source separately, join on shared keys after aggregation.
- Drop incomplete days (today, the Search Console lag, the ad platforms' open
  conversion window) and say so.
- Recompute one total two ways and confirm it matches.

## 5. Find what matters

- Use the `whats-changed` skill on the headline metrics: driver tree for the
  top metric, mix vs rate for the rates, contribution by channel or campaign.
  Only movements beyond noise become findings.
- Use the `diagnose` skill on the largest real movements: likely cause with
  evidence, the next action, how to verify.
- Cap it at three findings, ranked by money at stake. If nothing moved beyond
  noise, say that plainly: "a steady month" is a finding.

## 6. If it is a Claude Dashboard

When the output is a Claude Dashboard (asked for by name, chosen from the
Output menu, or built from the Dashboards template), read
[references/claude-dashboards.md](references/claude-dashboards.md) before writing
any dataset. It maps every Devil's Analyst rule onto the dashboard's datasets,
descriptions and calculations, and gives tested SQL that makes the "what
changed" analysis a live, clickable part of the dashboard instead of a pasted
paragraph. For any other output (a chat answer, a document, an HTML page),
continue below.

## 7. Lay it out

Pick the layout for the question from [references/layouts.md](references/layouts.md)
and follow the design rules in [references/design.md](references/design.md).
Write every title, finding and note by [references/writing.md](references/writing.md).
The skeleton every layout shares:

1. **Title that states the answer**, not the topic: "Paid search held revenue
   while CPA rose 18%", not "Paid search performance".
2. **KPI row**: at most five tiles, each with value, change vs comparison,
   a sparkline, and the volume behind any rate.
3. **What changed**: the decomposition (a bridge chart for the headline).
4. **Where**: the drill-down that names the branch (campaign, channel, landing
   page, segment), sorted by contribution to the change.
5. **What to do**: the findings in the `diagnose` shape.
6. **Definitions and data notes**: the metric dictionary, sources, freshness,
   what was excluded and why.

## 8. Check before handing over

- [ ] Every number traces to a dictionary definition and a source.
- [ ] No rate shown without its volume; no average of rates.
- [ ] Comparison periods are complete and equal (or the difference is stated).
- [ ] Platform-reported revenue is labelled, and not summed across platforms
      without a warning.
- [ ] Each finding has a number, a driver, a cause labelled confirmed or
      hypothesis, an action, and a way to verify.
- [ ] Platform mechanics the export does not show (view-through counting,
      attribution windows, modelled conversions) are offered as likely causes,
      not stated as facts about this account.
- [ ] The title states the answer.
- [ ] Nothing on the page that answers none of the reader's questions.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Pin the question | "Who decides what after reading this?" | one-sentence reader and decision | ask the user |
| Inventory and define | "Is every metric on the page in the dictionary, at the right grain?" | metric-definitions checks passed | fix the definition first |
| Headline | "Does the title state the answer, and is it the finding with the most money at stake?" | title has a number and a direction | rewrite the title |
| KPI tiles | "Is any tile coloured good or bad because of mix or noise?" | tile colour vs mix and noise results | grey it and label it |
| Charts | "Does any chart mislead (truncated bar axis, dual axis, rate without volume, cumulative hiding a decline)?" | design.md rules per chart | change the chart |
| Actions | "Can the reader verify each action, and is each cause labelled?" | action + check + label per finding | add them |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.
