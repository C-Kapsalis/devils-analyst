---
name: whats-changed
description: >-
  Use this skill whenever a marketing number went up or down between two periods and you
  are about to explain why: it splits the change into drivers (sessions x conversion rate
  x order value), into mix versus rate for any percentage (did CTR fall, or did the
  audience shift?), and into contributions by channel, campaign or segment, and screens
  out noise. Triggers include "why did revenue drop", "what changed", month-over-month or
  week-over-week comparisons, and any report or dashboard that compares periods.
---

# whats-changed

The LLM narrates; the arithmetic decides. Before you write "revenue fell
because of paid social", the decomposition has to say so, with numbers that add
up to the change you are explaining.

## 1. Fix the comparison first

A wrong comparison makes every insight after it wrong.

- **Same length, same weekdays.** Week over week compares Monday-Sunday with
  Monday-Sunday. Month over month on daily data: compare equal day counts, or
  say the months differ in length.
- **Complete periods only.** Drop today. Drop the last 2-3 days of Search
  Console (it lags). Drop the conversion window still open for ad platforms
  (Google Ads keeps adding conversions for days after a click). Say what you
  dropped.
- **Seasonality.** If the business is seasonal or the period holds a promotion
  or holiday, add the same period last year as a second comparison and say which
  one the conclusion rests on.
- State the comparison in the dashboard subtitle: "Mar 1-31 vs Feb 1-28, 2025".

## 2. Pick the decomposition that matches the metric

| Metric shape | Example | Method |
|---|---|---|
| A sum | Revenue, sessions, spend, clicks | **Contribution**: change per channel / campaign / segment, as a share of the total change |
| A ratio | CTR, CVR, CPA, ROAS, open rate, CAC | **Mix vs rate** across the segments: did the rates inside segments move, or did the volume shift between segments? |
| A product of drivers | Revenue = sessions x CVR x AOV; email revenue = delivered x CTR x click-to-order x AOV | **Driver tree** (log decomposition): how much of the change each driver explains |

Most good answers use two: a driver tree for the headline number, then mix vs
rate or contribution on the driver that moved most. Formulas, edge cases and a
fully worked example are in [references/decomposition.md](references/decomposition.md).
Read it before computing; the formulas there are exact (the parts add up to the
change) and the naive alternatives are not.

## 3. Compute, then check it adds up

Compute in code (the analysis tool, a SQL query, or Python), never in your
head. Then check:

- contributions sum to the total change (to rounding);
- every rate you report has its volume beside it;
- each segment's change is tested against noise (section 4 of the reference).
  A change inside the noise band is reported as "no clear change", not as a
  finding.

## 4. Write the insight

Write by the `marketing-dashboard` skill's `references/writing.md`: answer first, one point per paragraph, plain words.

One finding per sentence. Number first, driver second, interpretation last, and
label interpretation as a hypothesis when the data cannot prove it.

> CTR rose 0.64 points to 4.6%, but 0.59 of those points are mix: the new VIP
> segment (18% CTR) entered the send. Within segments, only Active customers
> improved (+1.3 points, beyond noise). Newsletter CTR dipped 0.4 points, which
> is within noise at this volume.

Not: "CTR improved thanks to better content." Content was not measured.

**A written report shows the arithmetic, not only the story.** Before the
findings, include the decomposition as a small table whose rows add up to the
headline change, with the check stated:

| Driver of revenue change (Mar to Apr) | Amount |
|---|---|
| Sessions | +$4,120 |
| Conversion rate | -$7,860 |
| Order value | +$1,340 |
| New channel (affiliates) | +$5,600 |
| **Total change** | **+$3,200** (= $61,700 - $58,500) |

For a rate, add the mix-vs-rate split as its own line: "CVR -0.20 pts =
+0.15 pts mix + (-0.35) pts within channels". A report that lists
before-and-after figures per segment without these two pieces has not
explained the change; it has described it.

## 5. In a dashboard

In a Claude Dashboard the decomposition is a dataset or a calculation, not text:
the mix-vs-rate and driver-bridge SQL in the `marketing-dashboard` skill's
`references/claude-dashboards.md` runs live, so the explanation refreshes with
the data and every number in it can be clicked. Elsewhere:


- Put the decomposition next to the headline it explains: a waterfall (bridge)
  from last period's value to this period's, one bar per driver or segment.
- Rates: a two-bar "mix" vs "rate" split, then the segments sorted by their
  contribution.
- Mark changes inside the noise band in a muted color, and say so in the legend.
- Hand the largest real movement to the `diagnose` skill for the likely cause
  and the next action.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Fix the comparison | "Are the periods equal and complete, and is seasonality in play?" | same length and weekdays; no open conversion window; last year's period if seasonal | change the comparison or state the limit |
| Decompose | "Do the parts add up to the change, exactly?" | sum of contributions = total change (to rounding) | use the exact method in the reference |
| Mix vs rate | "Did the audience shift, so a blended rate moved with no behaviour change?" | mix share vs within-segment share computed | lead with whichever dominates |
| Screen noise | "Would this change appear by chance at this volume?" | noise band per segment | report "no clear change" |
| Write the insight | "Is the interpretation proven, or a story?" | each cause tied to a measured driver | label it a hypothesis and say how to test it |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.
