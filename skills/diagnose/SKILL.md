---
name: diagnose
description: >-
  Turn a marketing number that moved into a diagnosis a consultant would sign, covering
  the likely cause, the evidence for and against it, the next action and how to verify it.
  Uses the Cohortica funnel diagnostic (acquisition, activation, revenue, retention, each
  declining, flat or inefficient), the brand strategy diagnostic, and 59 practitioner
  playbooks across email, paid search, Performance Max, SEO, GA4, paid and organic social,
  customer analytics, attribution, GEO and product. Use after a dashboard or the whats-
  changed skill finds a real movement, or when the user asks why performance is down, what
  to do next, or for recommendations.
---

# diagnose

A dashboard says *what* moved. A diagnosis says *why it probably moved, what to
check to be sure, and what to do*. This skill turns the first into the second
without inventing causes the data cannot support.

## 1. Start from a measured movement

Only diagnose a change that survived the `whats-changed` noise screen, and know
its driver: "revenue down 12%, driven by conversion rate (-15%), concentrated
in paid social". Without a driver, you are guessing which journey broke.

## 2. Place it on the funnel

Map the driver to one journey and one state in
[references/funnel-diagnostic.md](references/funnel-diagnostic.md):

| The driver that moved | Journey |
|---|---|
| sessions, new users, reach, impressions, branded search | Acquisition |
| engagement, add-to-cart, checkout start, lead form completion, CVR | Activation |
| AOV, revenue per session, margin, ROAS, CAC | Revenue |
| repeat rate, time between orders, churn, unsubscribes, list erosion | Retention |

| Pattern over the comparison | State |
|---|---|
| clear fall | Declining |
| no movement while effort or spend rose | Flat |
| volume holds but cost per outcome rises, or quality falls | Inefficient |

Read only that journey's section of the file, not the whole file.

The diagnostic is written for e-commerce (stores, collections, orders). For B2B
or lead generation, read *order* as qualified lead or opportunity, *AOV* as
average deal size, and *repeat purchase* as expansion or renewal, and say you
made that mapping.

## 3. Test the signals against the data you have

Each state lists signals in four kinds: *observed*, *diagnostic*, *outcome*,
*context*. For each signal, mark it:

- **confirmed**: you checked it in the data (cite the number);
- **contradicted**: you checked it and it is not so (cite the number);
- **unchecked**: the data to check it is not connected. Say which source would
  check it ("needs Search Console branded queries").

**Market or us, before any cause on our side.** For any acquisition or
volume drop, first ask whether the market moved: competitors' estimates,
category or non-brand search volume, impressions at unchanged position and
click-through, the same weeks last year. If the comparison set fell by about
the same share and your share of it held, the leading hypothesis is lower
demand in the category (seasonal or market-wide), not a fault in your SEO,
ads or site. Say so first, and verify it with the same period last year or
a category demand source. Check tracking and site changes first only when
your series moved and the comparison set did not; when both moved together,
a measurement fault on your side cannot explain the competitors' drop, so it
is a secondary check, not the lead.

A diagnosis with only unchecked signals is a hypothesis list, and must be
labelled so. Pull the data for the cheapest unchecked signals before writing
the diagnosis, when a connector for them is available.

## 4. Go deeper with the playbook

[references/playbook-index.md](references/playbook-index.md) lists 59 playbooks
by discipline with the question each answers. Open the one that matches the
driver (for a paid search CPA rise, `paid-search/conversions-cpa-and-return.md`;
for an email click-to-order fall, `email-marketing/click-to-revenue.md`). Use its
*framework* and *metrics and their traps* sections; ignore its interview-prep
section. Cite the playbook by title when you use its reasoning.

For brand questions (positioning, architecture, equity, messaging, repositioning)
use [references/brand-diagnostic.md](references/brand-diagnostic.md) the same way.

## 5. Write the diagnosis

Write by the `marketing-dashboard` skill's `references/writing.md`: answer first, one point per paragraph, plain words.

Use this shape for each finding (at most three per report; rank by money at
stake):

```
**[Journey] is [state]: [the measured movement, one sentence with numbers].**
Likely cause: [cause] ([confirmed / partly confirmed / hypothesis]).
Evidence: [confirmed signals with numbers]; against: [contradicted signals].
Do next: [one or two actions from the state's action list, made specific to this data].
Verify in: [the source and the exact cut that would confirm or kill the cause].
```

Rules:

- **Never state a cause as fact unless a confirmed signal shows it.** "Likely",
  plus the evidence, is the honest default.
- **Specific beats generic.** "Shift 20% of Meta prospecting budget to the two
  ad sets with CPA under $40" beats "optimize budget allocation".
- **One action per finding should be doable this week.**
- Compare the account with its own history first. A benchmark from a playbook
  (for example "deliverability above 95%", "complaints past 0.1% is a
  warning") may be cited as a labelled heuristic with the playbook it came
  from, never as a target and never as the only evidence.

## 6. In a dashboard

Add a "What to do" panel under the KPIs: the findings in the shape above,
collapsed to the bold first line plus "Do next", and a link or toggle to the
evidence. Color the state (declining, flat, inefficient) with one muted tone
each; reserve red for findings with money at stake.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Start from a movement | "Did this movement survive the noise screen and have a driver?" | whats-changed output with a driver | go back and decompose first |
| Place it on the funnel | "Could the same pattern sit in another journey (a tracking change looks like an activation drop), or outside the business (the whole category moved)?" | check tagging and data changes for the period; compare with competitors, category demand and last year | rule out measurement before behaviour when only your series moved; lead with demand when the market moved with you |
| Name the cause | "What rival cause produces the same pattern?" | for each rival, the data that rules it out | keep the survivors, labelled hypotheses |
| Recommend | "What does it cost if this is wrong, and what would the CFO ask?" | downside sized; a test or metric that verifies | add a test, or shrink the action |
| Rank findings | "Is the top finding the one with the most money at stake?" | findings ordered by value at stake | reorder |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.
