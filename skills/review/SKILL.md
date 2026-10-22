---
name: review
description: >-
  Use this skill when someone hands over a marketing report, deck, dashboard, analysis
  or agency write-up that someone else made and wants it checked: "review this
  report", "review this dashboard", "review this deck", "can you check this before I
  send it to my boss", "is this right", "check my numbers", "sanity check this", "does
  this hold up", "what's wrong with this analysis", "would you sign off on this", "the
  agency sent us this, is it fair". Works on markdown, HTML, a pasted deck, a
  screenshot description or a spreadsheet, with or without the data behind it. It
  recomputes every number it can, checks definitions, charts, comparisons, causal
  claims and recommendations, leaves correct things alone, and returns a verdict plus
  findings ranked Must fix, Should fix, Nice to have. Auditing a whole account or
  setup: use audit. Building a new report: use marketing-dashboard. Email copy itself
  is out of scope.
---

# review

The chart can be right and the conclusion wrong. A review finds the places
where a reader would decide something different if the report were correct,
proves each one with a number, and leaves everything else alone. A review
that flags correct things, or pads the list, teaches the reader to ignore it.

**The human owns the question and the decision.** Before reviewing, write one
line: "After reading this, [who] will [decide what]." If the report does not
say who reads it or what they will decide, assume the obvious reader (the
boss, the client) and say so in one line. Do not stop to ask unless the
decision is truly unclear.

## 1. Build the claim ledger

Read the whole artefact once. List every claim that a decision could rest on,
in a scratch table (do not print it):

| # | Claim as written | Type | Can I check it? |
|---|---|---|---|
| 1 | "Blended ROAS 5.2x" | number | yes: spend and revenue in the CSVs |
| 2 | "The new creative drove the lift" | cause | partly: is there a control? |
| 3 | "Cut display" | action | yes: what it is judged on |

Types: **number** (a value or a total), **definition** (what a metric
means), **comparison** (up, down, best, worst), **chart** (what a visual
implies), **cause** (drove, caused, because), **action** (cut, scale, keep).
Headline and summary claims first: they carry the decision.

If data files come with the report, map each file to the claims it can test
(columns, grain, date range, which platform). If no data comes with it, check
internal consistency only (totals that should sum, rates that should match
their parts, text that contradicts a table) and say so under "Not checked".

## 2. Run the checks, in this order

Stop on each claim at the first check that fails. Details and detection rules
for every item: [references/review-checklist.md](references/review-checklist.md).

| Order | Check | Fails when | Typical recomputation |
|---|---|---|---|
| 1 | **Arithmetic** | a total does not sum, a rate does not match its parts | sum the column; divide the summed parts |
| 2 | **Aggregation** | a ratio is an average of row ratios; distinct counts (users, reach) are summed across days or weeks; a snapshot (list size, subscribers) is summed over time | sum(numerator) / sum(denominator); take the period value, not the sum |
| 3 | **Definition** | "conversions" mix micro actions with purchases; open rate used as engagement; platform revenue used as sales | scope to the action that means money; use the store or analytics total |
| 4 | **Double counting** | channel claims sum above the store total; query-page impressions summed as demand | compare the sum with the single source of truth |
| 5 | **Comparison** | no comparator; unequal periods or ages; last 2-3 days of a lagging source read as a drop; a filtered "% of total" | same-length prior period, same window last year, same accrual age |
| 6 | **Blend** | one rate across groups that behave differently (brand and generic, mobile and desktop, one giant send and small ones) | split rows; compare within each group |
| 7 | **Chart** | the visual implies something the numbers do not | see [references/chart-checks.md](references/chart-checks.md) |
| 8 | **Cause** | drove, caused, thanks to, because, with no control, holdout or test | name the rival explanation the data cannot rule out |
| 9 | **Significance** | "significant" with no test or n; a costed change tested against zero instead of its break-even; a segment winner from a pivot table | compute it, or call it a hypothesis |
| 10 | **Action** | the recommendation does not follow from the corrected numbers, or has no number to watch and no way to verify | redo the decision on the corrected numbers |

Metric formulas and platform quirks live in the `metric-definitions` skill
(catalog and source traps); causal tests (holdouts, SRM, power, novelty,
Simpson's paradox, pull-forward) in `evidence-check`; period-over-period
decomposition in `whats-changed`. Use them for the recomputation. Do not
repeat their content in the review.

## 3. Prove it or drop it

A finding needs a concrete case: "this cell says X; the data gives Y; here is
the arithmetic". Before keeping any finding:

1. **Recompute it.** Show the numbers that disagree, from the report or the
   data, in one line ("CTR printed 6.1% is the mean of row CTRs; 4,210 clicks
   / 118,400 impressions = 3.6%").
2. **Check the decoy list.** Many things look wrong and are fine:
   [references/decoys.md](references/decoys.md). Examples: Search Console clicks
   above GA4 sessions, display CTR near 0.4%, brand campaigns with 30-50% CTR,
   sessions slightly under email clicks on every row, rounding gaps under 1%,
   a median that differs from the mean when the report says which it uses.
3. **Check the report did not already handle it.** A caveat, a footnote, or a
   split table elsewhere in the report can answer the point. Read it before
   flagging.
4. **Ask "would the reader decide differently?"** If no, it is Nice to have
   at most. If it is only taste (fonts, wording you would phrase differently),
   drop it.

No number, no finding. No "consider", no "might want to", no vague worry.

## 4. Rank

| Group | Put here when | Examples |
|---|---|---|
| **Must fix** | a headline or decision number is wrong; a definition error changes the answer; the recommendation points money the wrong way; a chart reverses the reading | stacked platform revenue as ROAS; CPA on newsletter sign-ups; "organic crashed" from the lag days; ship decision tested against zero instead of break-even |
| **Should fix** | the direction holds but the number is off; a causal claim with no test; a missing comparison; an action with no way to verify; a chart that exaggerates without reversing | averaged CTR in a side table; "the new creative drove it"; no prior period; display judged on CTR |
| **Nice to have** | labels, a missing denominator the reader can infer, chart type choices | 9-slice pie; unlabelled moving-average window |

Within a group, order by the money or the decision at stake: the finding that
moves the most budget or revenue goes first. Number findings across all
groups so the reader can say "fix 1 and 3".

## 5. Write the review

Plain English, short sentences, the reader may not be an analyst. Define a
term the first time (CTOR, ROAS). No emojis, no em-dashes.

```
Verdict: [Send it. | Fix 1 and 2 before sending. | Do not send: the main conclusion is wrong.]

What this report says: [two sentences: its main claim and its recommendation]
Who decides what: [one line, from the ledger]

## Must fix
1. **[Short name of the problem]** ([where: slide 3, tile "ROAS", table 2 row "Meta"])
   - **What it says:** [the claim, quoted or paraphrased, with its number]
   - **What is wrong:** [the recomputation or the rule, with the right number]
   - **Fix:** [the corrected number or wording, ready to paste]
   - **If you skip it:** [the decision or money at stake, in one sentence]

## Should fix
...
## Nice to have
...

Checked and fine: [one line: the main numbers or claims you verified and that hold]
Not checked: [one line: what you could not test and why]
```

- Skip empty groups. Keep at most 10 findings; if you left smaller ones out,
  say how many.
- "If you skip it" names the consequence in money or in the decision: "the
  team scales a campaign that loses 0.40 on every click", not "accuracy
  suffers".
- The fix is concrete: the corrected figure, the replacement sentence, or the
  chart change. Not "clarify".
- When the report is correct: `Verdict: Send it.`, then "What this report
  says", then "Checked and fine" listing what you verified. Add a Nice to have
  only if it is real. Do not invent problems to look thorough.

A worked example of one finding, and of a clean verdict:
[references/finding-examples.md](references/finding-examples.md).

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check,
and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Build the ledger | "Did I skip the claims in the summary, the chart titles or the footnotes?" | every headline, chart title and recommendation has a ledger row | add the rows, re-run section 2 on them |
| Recompute a number | "Am I computing at the same grain, period and filter as the report?" | match one number the report got right before calling another wrong | align the scope, recompute |
| Flag a definition | "Is the report's definition a stated, defensible choice?" | the report's own notes and the metric-definitions catalog | drop it, or downgrade to Nice to have |
| Flag a cause | "What else produces the same pattern?" | name the rival (season, spend change, mix, selection) and whether the data rules it out | if the data rules it out, drop the finding |
| Keep a finding | "Is this a decoy?" | the decoy list and the report's own caveats | drop it |
| Rank | "Which finding would change the decision most if fixed?" | money or decision at stake per finding | reorder |
| Give the verdict | "Would I send this report to the boss with my fixes applied?" | the Must fix list is empty or the verdict says what to fix first | rewrite the verdict |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision
belong to the person asking: when either is unclear, ask instead of assuming.
