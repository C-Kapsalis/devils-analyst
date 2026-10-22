---
name: audit
description: >-
  Use this skill when someone wants a whole marketing setup or account checked, not
  one report: "audit our Google Ads account", "audit my GA4 setup", "audit our
  tracking", "health check our email program", "what's broken in our setup", "where
  are we wasting money", "we just took over this account, what should we fix first",
  "is our Meta / Performance Max set up right", "check our UTMs", "audit our Search
  Console", "audit our CRM or lifecycle program", "check our Power BI model", "review
  this TMDL / semantic model", or an account, settings or model export with "what's
  wrong with it". It maps the setup, runs the checks for each area present (paid
  search, Performance Max, Meta, GA4 and UTMs, Search Console, email, CRM, revenue,
  experiments, attribution, dashboards, Power BI), estimates the money at stake, ranks
  findings Must fix, Should fix, Nice to have and ends "Fix N first". One report or
  deck: use review. Whether a single channel pays: use channel-audit.
---

# audit

An account can look healthy on every dashboard while one upstream error
makes every number after it a fiction. An audit reads the setup in order,
fixes the measurement before judging performance, and tells the owner which
one thing to fix first. It does not list everything that could be better.

**The human owns the question and the decision.** The goal (sales, leads,
sign-ups), the margin and the targets come from the owner. Ask for any that
are missing in one short list, then proceed with a stated assumption
(for example "assuming purchase is the only goal and 40% gross margin").

## 1. Map first

Before any check, write the map (print it, five to eight lines):

| Map item | Find it in |
|---|---|
| Sources present | file names, columns, platform export formats |
| Period covered | date columns |
| Spend by channel | cost columns, summed per channel |
| Goals | conversion actions, key events, the owner's words |
| Margin, AOV, targets | the owner; if absent, ask and state the assumption |
| Revenue truth | the store, backend or finance total, if any file has it |
| What is missing | areas the owner asked about with no data |

Spend tells you where the money is. Audit the biggest spend and the
measurement every channel relies on (conversion setup, GA4, UTMs) first.

## 2. Pick the areas and load their checks

Run only the areas the data covers. Each reference lists the checks as Look
at / Red flag / Why it costs money / Fix.

| Area present | Reference |
|---|---|
| Google Ads or Microsoft Ads search | [paid-search.md](references/paid-search.md) |
| Performance Max, Demand Gen, display, video | [pmax.md](references/pmax.md) |
| Meta and other paid social | [meta.md](references/meta.md) |
| GA4 settings, key events, traffic, UTMs | [ga4-utm.md](references/ga4-utm.md) |
| Search Console and SEO | [search-console.md](references/search-console.md) |
| Email platform, deliverability, list | [email.md](references/email.md) |
| CRM lifecycle, retention, CLV | [crm-lifecycle.md](references/crm-lifecycle.md) |
| Store or backend revenue against platforms | [ecommerce-revenue.md](references/ecommerce-revenue.md) |
| A/B tests and lift studies | [experiments.md](references/experiments.md) |
| Attribution models and settings | [attribution.md](references/attribution.md) |
| Dashboards and reports in use | [dashboards.md](references/dashboards.md) |
| Power BI model (TMDL, PBIP, DAX list) | [power-bi.md](references/power-bi.md) |

Formulas and platform quirks: `metric-definitions`. Break-even maths per
campaign or creator: `channel-audit`. Whether a test or change caused a
result: `evidence-check`. Reading a Power BI model's measures for reuse:
`power-bi-definitions`. Use them; do not repeat them.

## 3. Run each check with a number

For every red flag you keep:

1. **Compute it from the export.** "Purchase is 31% of the 2,840
   conversions in the Conversions column", not "conversions may include
   micro actions".
2. **Name the concrete case.** Which campaign, query, send, event, measure.
3. **Estimate the money at stake** with the simplest honest formula:

| Finding type | Money at stake |
|---|---|
| Spend on something that does not pay | cost of the rows affected per month |
| Budget capped on a line that beats target | lost-to-budget share x current conversions x margin (an upper bound) |
| Measurement error | the spend or revenue whose reading it corrupts (say "all 42,000 of monthly paid spend is optimised on this number") |
| Reputation or deliverability risk | the revenue of the program at risk |
| Wrong definition in a model or dashboard | the decisions it feeds; size it by the spend or revenue it reports on |

If you cannot size it, say what it corrupts. Do not invent a figure.

4. **Check it is not a decoy.** Brand CTR of 30-50%, display CTR near 0.4%,
   GSC clicks above GA4 sessions, phrase match with the highest CPC,
   retargeting ROAS above prospecting, stable direct traffic around 10-25%:
   all normal. The review skill's decoy list
   ([../review/references/decoys.md](../review/references/decoys.md)) applies
   here too. Flag a pattern only when it costs money or corrupts a decision.

No number and no concrete case: no finding.

## 4. Rank: fix this first

Order findings by tier, then, within a tier, by dependency and then by
money at stake. Each check row in the area references carries its default
tier in the last column; use it, and raise or lower it only with a reason
from the data.

| Tier | What | Examples | Group |
|---|---|---|---|
| 1. Measurement integrity | anything that makes later numbers fiction, or stops the channel reaching anyone | the action the account optimises on is not the one that means money; a model or setting that silently does something other than what its label says; history that is being deleted or broken at a change date; one entity counted under several names, or one sale counted by several sources; a sender-reputation line crossed (authentication, delivery, complaints); a governed measure that averages a rate or sums a snapshot | Must fix |
| 2. Hygiene | leaks that waste money every day | brand and generic leakage; search-term waste; dormant contacts in main sends; retargeting buyers; cannibalising pages | Must fix if large, else Should fix |
| 3. Money left on the table | profitable lines starved | budget-capped campaign beating target; snippet rewrites at positions you hold; starved winner pages | Should fix |
| 4. Fine-tuning | adjustments on a setup that is already right | device, schedule, geo modifiers; creative refresh cadence | Nice to have |
| 5. Causal claims | credit sold as incremental | brand, retargeting, PMax brand share with no holdout | Should fix, written as "test this", never as a proven loss |

A tier-1 finding outranks a bigger tier-3 finding: fixing growth on a broken
measurement optimises toward the wrong number. Do not judge performance on a
metric that a tier-1 finding has broken; recompute it on the corrected
definition first, or say the read waits for the fix.

**Within a tier, upstream first.** When two findings share a tier, the one
every other number depends on goes first: whether mail is delivered at all
before any rate measured on delivered mail; whether the conversion is the
sale before any CPA or ROAS; whether tracking captures the visit before any
channel split. A finding that corrupts one decision (a forecast behind
one budget ask, a dashboard tile) comes after one that corrupts every later
reading, even when its money figure is larger. Money at stake breaks ties
after that.

**A leak that is already doing damage takes the damage's tier.** A hygiene
finding (tier 2) that has already pushed a rate the whole channel depends on
past a threshold in the area's checks, or far outside the account's own
normal range (a send's bounces or complaints several times the other
sends', a tag that stopped firing, a delivery rate that fell), is ranked as
tier 1: it is now the cause of a reputation or measurement failure, not
only a waste. Say which rate it moved, and by how much against the norm.

## 5. Write the audit

Plain English, short sentences. Define a term the first time. No emojis, no
em-dashes.

```
## Map
[five to eight lines: sources, period, spend by channel, goal, margin used, revenue truth, missing]

## Must fix
1. **[Short name]** ([where: campaign, event, send, measure])
   - **What it is:** [what the setup does now, with the number]
   - **Problem:** [why it is wrong, with the computation]
   - **Fix:** [the concrete change: setting, negative list, DAX, rule]
   - **If you skip it:** [money at stake per month, or the decision it corrupts]

## Should fix
...
## Nice to have
...

Checked and fine: [one line: the areas or settings that hold]
Not checked: [areas with no data, settings not in the export]
Fix [N] first.   <- or "Fix 1 and 2 first."
```

- Number findings across groups. At most 15; say how many smaller ones you
  left out.
- The last line names the first fix and why in a clause: "Fix 1 first:
  every CPA in the account is computed on newsletter sign-ups."
- A healthy area gets one line under "Checked and fine", not a finding.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check,
and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Map the setup | "What spend or source did I miss, and what is the real goal?" | spend summed per file equals the total; goal stated by the owner or assumed in writing | add it, or ask |
| Run a check | "Is this computed on the export, at the right grain and scope?" | one figure recomputed two ways (row sum and total row) | recompute |
| Keep a finding | "Is this normal for this channel (a decoy)?" | the decoy list and the channel's benchmark band | drop it |
| Size the money | "Would a CFO accept this figure, or is it inflated?" | the formula and its inputs shown; upper bounds labelled | shrink it, or say what it corrupts instead |
| Claim a cause | "Is this credit, or proven incremental?" | a holdout or test exists | write it as "test this" |
| Rank | "Does any performance finding sit on a number a tier-1 finding breaks, and within a tier, does anything listed first depend on something listed later?" | each tier 2-4 finding uses a corrected metric; within each tier, upstream findings come first | recompute, or reorder |
| Say "Fix N first" | "If the owner did only this, would the account be better off next month?" | the first fix unblocks or protects the most money | pick another |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision
belong to the person asking: when either is unclear, ask instead of assuming.
