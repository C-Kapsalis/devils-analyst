# Skill: audit

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
| Google Ads or Microsoft Ads search | paid-search.md (section "File: audit/references/paid-search.md" in 04-audit.md) |
| Performance Max, Demand Gen, display, video | pmax.md (section "File: audit/references/pmax.md" in 04-audit.md) |
| Meta and other paid social | meta.md (section "File: audit/references/meta.md" in 04-audit.md) |
| GA4 settings, key events, traffic, UTMs | ga4-utm.md (section "File: audit/references/ga4-utm.md" in 04-audit.md) |
| Search Console and SEO | search-console.md (section "File: audit/references/search-console.md" in 04-audit.md) |
| Email platform, deliverability, list | email.md (section "File: audit/references/email.md" in 04-audit.md) |
| CRM lifecycle, retention, CLV | crm-lifecycle.md (section "File: audit/references/crm-lifecycle.md" in 04-audit.md) |
| Store or backend revenue against platforms | ecommerce-revenue.md (section "File: audit/references/ecommerce-revenue.md" in 04-audit.md) |
| A/B tests and lift studies | experiments.md (section "File: audit/references/experiments.md" in 04-audit.md) |
| Attribution models and settings | attribution.md (section "File: audit/references/attribution.md" in 04-audit.md) |
| Dashboards and reports in use | dashboards.md (section "File: audit/references/dashboards.md" in 04-audit.md) |
| Power BI model (TMDL, PBIP, DAX list) | power-bi.md (section "File: audit/references/power-bi.md" in 04-audit.md) |

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
   (section "File: review/references/decoys.md" in 05-review.md) applies
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

---

## File: audit/references/attribution.md

# Attribution and incrementality

Attribution assigns credit according to a model someone picked. It does not
show what the spend caused; that takes a holdout or a test.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| A1 | GA4 reporting model vs 30-day conversions per key event | Data-driven selected on low volume; DDA column equal to last click | Silent last click; budget follows the wrong model | Report the model in effect; pick an explicit rule-based model | 1 |
| A2 | Lookback windows across reports and platforms | 30-day view compared with 90-day view; Meta 7-day click + 1-day view against Google 30-day click | Settings, not performance, make the difference | State and align windows before comparing | 1 |
| A3 | Platform conversions summed across platforms | Totals above site or store totals | Double counting | One de-duplicated source | 1 |
| A4 | Model switch log | Model changed with no note to bidding owners | Smart Bidding uses attribution as its signal; ROAS and bids change at once | Annotate; brief owners | 2 |
| A5 | Model vs business cycle | Last click on a long B2B cycle; first click on a short promo shop | Assists under- or over-credited | Short and transactional: last click or time decay; long: position-based or linear; mature with volume: data-driven | 3 |
| A6 | Time-decay half-life | 7 days on a long consideration cycle | Early touches get nothing | Calibrate to the real cycle | 4 |
| A7 | Custom data-driven models on little data | Markov under about 2,000 conversions a month; Shapley under about 5,000 | Overfit | Rule-based model, stated | 3 |
| A8 | Exposed vs unexposed | Sold as ad effect | Platforms target likely buyers | Randomised holdout | 5 |
| A9 | Retargeting, brand search, PMax brand share | Credited at full value with no test | Much may be people who would have bought anyway | Holdout or pause test | 5 |
| A10 | Last-click ROAS on awareness lines | Used to cut display or video | Last click is a floor, lowest for upper funnel | Test before cutting | 5 |
| A11 | Spend-vs-sales charts | "They move together" | Budgets often follow past sales | Experiments or a time-series design | 5 |
| A12 | Direct across models | "Direct did not change, so it is robust" | Direct is identical by construction in GA4 models | Explain it | 4 |
| A13 | Rule-based model used for channel cuts | Built only on converting paths | Non-converting paths ignored | Data-driven with volume; experiments for causal questions | 4 |

MMM (adstock, saturation) is not covered by these notes beyond the principle
that last-click is a floor and models need tests to calibrate them. Do not
audit an MMM from this list.

## Decoys

Last-click and DDA columns that differ when DDA has volume; Direct identical
across models; Meta reporting more conversions than GA4 when windows differ.

---

## File: audit/references/crm-lifecycle.md

# CRM lifecycle, retention and CLV

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| C1 | CLV formula | Built on revenue; no margin, no servicing cost, no discount rate | Overstates value and the acquisition ceiling; overspends on CAC | Margin net of service cost x survival per period, discounted, summed; subtract acquisition cost for net CLV | 1 |
| C2 | Churn applied twice | Survival factor R^t and a discount rate rho = (1 + i - R) / R in the same term | Understates CLV and the allowable CAC | Use V_t R^t / (1 + i)^t, or V_t / (1 + rho)^t, not both | 1 |
| C3 | CLV:CAC with a CLV already net of CAC | Ratio computed on net CLV | Acquisition cost counted twice | State the definition; compare gross NPV of future margin with CAC | 1 |
| C4 | Retention input precision | CLV quoted to the cent while retention is rough | At a 10% discount rate the multiple r / (1 + d - r) is 2.67 at r 0.80 and 4.50 at 0.90 | Report CLV as a range over plausible retention | 3 |
| C5 | CLV:CAC by channel | Below 1:1 (losing money per customer) or far above 3:1 (under-investing) | Wrong channels scaled or starved | Reject channels where CAC exceeds CLV minus a buffer | 3 |
| C6 | Churn in a buy-when-you-like business | A simple observed churn rate | Churn is inferred from purchase gaps there | Probabilistic models (purchase count and value) | 4 |
| C7 | Cohort CLV after an acquisition change | Projecting new cohorts from old ones after the channel mix changed | Contaminated forecast | Re-estimate on recent cohorts | 4 |
| C8 | "Active customer" definition | Changed between periods or undocumented | Retention moves with the definition | One documented definition | 1 |
| C9 | Segment ranking | By ticket size or sales; low-survival segments kept on full contact cost | Later-year NPV can turn negative | Rank by discounted profit after service and acquisition cost | 3 |
| C10 | Repeat rate credited to a loyalty program or CRM team | No size benchmark, no control | Bigger brands show higher repeat almost mechanically | Compare with what a brand of that size should show | 5 |
| C11 | Inflow vs outflow | Acquisition spend rising while the net base is flat | The bucket leaks | Fix the leak before turning up the tap | 3 |
| C12 | NPS as the only loyalty measure | No retention or share of wallet | Stated, not revealed, loyalty | Pair with repeat rate and share of wallet | 4 |
| C13 | Lifecycle stages counted by today's stage | Leads counted by current lifecycle stage, not by the date each stage was entered | Funnel conversion by month is wrong | Count by stage-entry date; compare leads created in the same month | 1 |
| C14 | Win-back with no exit | Lapsed contacts mailed forever | Deliverability risk | Exit and delete rule | 2 |
| C15 | Promo judged on one period | Intro offer killed or kept without later retention | Wrong call on customers the promo creates | Judge on cohort CLV | 4 |
| C16 | Folklore figures | "5% retention = 25-95% profit" as the forecast | Plan built on someone else's arithmetic | Use the company's own retention and margin | 4 |
| C17 | CAC ceiling | Set equal to the point estimate of CLV | No buffer for model error | Subtract a safety margin | 3 |

## Decoys

A CLV:CAC around 3:1 for subscription businesses; repeat rate rising with
market share; switching to rivals in proportion to their size.

---

## File: audit/references/dashboards.md

# Dashboards and reports in use

For a single report or deck, use the `review` skill. This list is what an
audit of the reporting setup looks for (the dashboards a team relies on
every week). The chart checks of the `review` skill
(section "File: review/references/chart-checks.md" in 05-review.md,
or `references/chart-checks.md` in the installed review skill) apply to each
page.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| D1 | Ratio measures | Averages of row ratios (CTR, CVR, CPA, ROAS, CTOR) | Every rate on the page is wrong at every total | Ratio of sums at each grain | 1 |
| D2 | Distinct counts and snapshots | Users, reach or list size summed across days or months | Inflated audiences; wrong CPM, frequency and CAC | Period distinct counts; end-of-period snapshots | 1 |
| D3 | Joins | Spend joined to orders row by row; inner joins that drop orphan keys (for example Tableau's "assume referential integrity") | Totals silently too high or too low | Aggregate facts separately; outer joins to surface dirty keys | 1 |
| D4 | Grain | Session-level and user-level facts mixed in one view | Aggregation errors | Document grain per table | 2 |
| D5 | One canonical definition per metric | The same KPI defined differently on two pages or two copies | Teams argue over numbers, not decisions | One definition with owner, numerator, denominator, grain, filters, exclusions | 2 |
| D6 | Comparisons | Tiles with no prior period, target or last year | No way to judge a number | Add the comparator | 3 |
| D7 | Thresholds | Hard-coded red/amber/green values with no owner | Colour drives action with no reason | Owner sets thresholds with a written reason | 4 |
| D8 | "Why" sections | Prose with no driver bridge or mix vs rate split | Causes asserted, not computed | Bridge that sums to the change | 3 |
| D9 | Definitions panel | No definitions or data notes on the page | Readers misread metrics | Definitions on click | 4 |
| D10 | Freshness | No refresh time; "real-time" claimed for on-demand refresh | Decisions on stale data | Show last refresh | 4 |
| D11 | Top N per group | Global Top N shown as per-group | Wrong lists | Filter order fixed (context filter first) | 3 |
| D12 | Classification thresholds in churn or lead-score views | Default 0.5 cut-off | Assumes equal error costs | P >= c / (1 + c) with c = cost of a miss / cost of a false alarm | 3 |
| D13 | Lifecycle counts | Leads counted by today's stage | Monthly funnel wrong | Count by stage-entry date | 1 |
| D14 | Recomputed metrics | A dashboard recomputes CAC in SQL while the governed model defines it differently | Two CACs | Query the governed measure; label translations as untested until reconciled | 2 |

## Decoys

A median labelled as such; a dashed, labelled forecast; filters that apply to
the whole page and say so.

---

## File: audit/references/ecommerce-revenue.md

# E-commerce and backend revenue against platforms

Three views of revenue, in order of authority: the order system (store,
backend, finance) net of refunds and cancellations; web analytics (the
attribution layer, losing some purchases to blockers and consent); each ad
platform's claim on its own window, overlapping with the others. Align
refunds, tax and shipping, currency, order date vs click date and test orders
before comparing.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| R1 | Sum of revenue claimed by each platform vs the store total | Claims sum above the store total, or above the analytics total for paid channels | The same sale is claimed twice; blended ROAS is fiction | One shared denominator; platform numbers labelled as claims | 1 |
| R2 | Single-touch attribution columns | A last-click column that does not sum to total conversion value | Credit invented or lost | Each single-touch column sums to the total | 1 |
| R3 | Budget ranked on ROAS where margins differ | Low-margin lines with high revenue ROAS ranked first | A healthy revenue ROAS can lose money | Rank on profit on ad spend; break-even ROAS = 1 / gross margin | 3 |
| R4 | Promotion revenue | Promo credited with total sales in the window | Pull-forward, stockpiling and the dip after are ignored | Incremental units x margin - discount cost - pull-forward | 5 |
| R5 | Average order value | Mean pulled up by a few wholesale or B2B orders | Thresholds and targets set on a typical order that does not exist | Median, or split retail from wholesale | 3 |
| R6 | Free-shipping threshold | Far from the typical basket, or none | Many new orders too small to be profitable | Just above the typical basket; test | 4 |
| R7 | Test orders, refunds, cancellations | Included in revenue | Overstated revenue and ROAS | Exclude or net them | 1 |
| R8 | Currency and tax | Platforms in one currency or gross of tax, store in another | Apparent gaps that are units | Align before comparing | 1 |
| R9 | Market share claims | Share with no denominator (units vs revenue, served vs total market) | Board decks overstate position | Label both | 4 |
| R10 | Customer records across store, web and app | Separate records per channel | Cross-channel customers invisible | Unify IDs | 4 |

## Decoys

Analytics revenue a few percent under the store total (blockers, consent);
platform conversions above analytics when windows differ, as long as nobody
adds them up.

---

## File: audit/references/email.md

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

---

## File: audit/references/experiments.md

# Experiments and lift studies

The full tests (sample ratio chi-square, two-proportion z, power, novelty,
interaction) are in `evidence-check`. This list is what an audit of a testing
program looks for.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| X1 | Users per arm vs the planned split | Chi-square on assignment counts above 10.8 (p < 0.001) | Assignment or logging broken; results unreadable | Find the cause before reading outcomes | 1 |
| X2 | Null hypothesis vs the cost of the change | Lift tested against zero when the change has a cost | A lift can beat zero and still not pay | Convert the cost to a break-even lift; test against it | 1 |
| X3 | Duration | Under 7 days or partial weeks | Day-of-week effects | Whole weeks, usually 1-2 | 1 |
| X4 | Pre-registered minimum detectable effect and sample size | None; stopped when it "looked significant" | Noise wins shipped | Size before launch | 2 |
| X5 | Rows vs randomisation units | More rows than unique users, analysed per row | Inflated n fakes significance | Dedupe to the user | 1 |
| X6 | Balance checks | On variables measured after exposure | Treatment can move them | Balance on pre-period variables | 3 |
| X7 | Changes between A and B | Copy, layout and price changed together | Cannot attribute the result | One change, or a factorial design | 3 |
| X8 | Primary metric vs objective | "More orders" goal measured by product clicks | Optimising a proxy | A metric measurable, attributable, sensitive and timely in both arms | 2 |
| X9 | Segment winners | Rollout to a segment from a pivot table with no interaction test | Launching on noise | Interaction test; call it suggestive | 3 |
| X10 | Novelty | Lift concentrated in returning users early | Fades after launch | Split by new vs returning and by week | 3 |
| X11 | Lift study reporting | Raw point gap; no relative lift; no incremental count; cost on treatment impressions only | Misstated payoff | Lift = (T - C) / C; incremental = T conversions - C rate x T users; cost on control plus treatment impressions | 3 |
| X12 | Exposed vs unexposed comparisons | Sold as ad effect | Selection, not effect | Randomised holdout | 5 |
| X13 | Interventions on last month's worst units | Rebound claimed | Regression to the mean | Untreated equally extreme control | 5 |
| X14 | Surprising big lifts | Shipped with no rerun | A figure that looks too interesting is usually wrong | Replicate | 3 |
| X15 | A/A tests on new tooling | Never run | Unknown bias | Run periodically | 4 |
| X16 | Brand-lift pre-waves | Pre-wave names the brand | Sensitises only the exposed group | After-only design with a randomised control | 3 |

## Decoys

A 49.9 / 50.1 split; a non-significant result reported as "no evidence at
this confidence" (correct wording); tests of 14 days.

---

## File: audit/references/ga4-utm.md

# GA4 setup and UTMs

## GA4

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| GA1 | Admin > Data settings > Data retention | 2 months (the default) | Explorations, funnels and paths cannot look back further; year-over-year in explorations is impossible; the setting is not retroactive | Set 14 months now | 1 |
| GA2 | Reporting attribution model and 30-day count per key event | Data-driven selected while a key event has a few hundred conversions a month (the notes cite about 400 per 30 days) | GA4 falls back to last click without telling anyone; budget and bidding signals are last click | Report the model in effect; for low volume, pick an explicit rule-based model; check current Google guidance on the threshold | 1 |
| GA3 | Key events list | One business outcome split over several key events (purchase, purchase_app, checkout_complete), each under the threshold | Fragmentation alone pushes every type into silent last click, and totals double count | One key event with a parameter for the variant | 1 |
| GA4 | Key events vs business model | Shop without purchase as a key event; lead-gen without phone calls | Every CPA is about a proxy | Map key events to the business: purchase; form plus call; subscription | 1 |
| GA5 | Micro actions marked as key events (scroll, file_download, video plays, newsletter) and the engagement rate trend around the date | Engagement rate steps up on the day a low-effort event became a key event | An engaged session is over 10 seconds, 2+ pages, or a key event, so engagement rises with no change in behaviour | Keep micro actions as plain events; annotate the change date | 1 |
| GA6 | Enhanced measurement toggles | Off, or site search off on a catalogue site | Search terms and outbound clicks are lost for good | Enable | 3 |
| GA7 | E-commerce funnel events | A step missing (view_item, add_to_cart, begin_checkout, add_shipping_info, add_payment_info, purchase) or firing at implausible ratios | The funnel cannot locate the drop-off | Implement all steps; validate in a funnel exploration | 2 |
| GA8 | Cart abandonment far outside about 60-80% | Near 0% or above 95% | Usually an event-firing problem, not a business result | Audit add_to_cart and purchase firing before acting | 1 |
| GA9 | Direct share and its trend vs the campaign calendar | Direct spikes on send or launch dates while banners, bio links or QR codes are live | Untagged campaign traffic lands in Direct and its revenue is credited to nobody | Tag every off-site link | 2 |
| GA10 | Unassigned channel | Non-trivial Unassigned sessions or revenue | Credit you paid for but cannot route | Use channel-type words in utm_medium so default grouping can classify them | 2 |
| GA11 | Exploration sampling | Segment claims from sampled explorations | Detail is unreliable | Shorter ranges or unsampled sources | 4 |
| GA12 | A trend crossing the old analytics cutover | Bounce rate step at the migration month | Different bounce definitions | Break the series | 4 |

## UTMs and campaign naming

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| U1 | Distinct utm_campaign values, normalised (lowercase, trim, unify - and spaces to _) | More than one raw spelling per key (spring_sale, Spring_Sale, spring-sale, "spring sale ") | One campaign split over rows; revenue under-credited and reconciled by hand | One house style; a link builder; no improvisation | 1 |
| U2 | utm_medium values | Platform names in medium (facebook, google, mailchimp) or channel types in source | Breaks channel grouping and feeds Unassigned | Controlled vocabulary: medium = channel type, source = platform | 1 |
| U3 | utm_content on multi-creative campaigns | Blank | Cannot tell which creative earned revenue | Require utm_content | 3 |
| U4 | Ad platform campaign names vs the shared key | Paid campaigns named off-scheme | Paid becomes a silo in cross-channel reads | Align names to the shared key | 3 |
| U5 | Display spend vs display sessions | Spend with near-zero display sessions and a Direct lift in the same weeks | Banners untagged; display looks worthless and gets cut | Tag every banner click URL | 2 |
| U6 | Organic social links, partner links, QR codes | Plain URLs | Clicks land in Direct; print shows as an unexplained spike | Tag them; hand partners pre-tagged links | 3 |
| U7 | Campaigns with clicks but no revenue, and revenue in (not set) or unnamed buckets | Both lists non-empty | The fingerprint of tagging drift | Track "share of revenue reconciled to a named campaign" | 2 |
| U8 | AI assistant referrals | Filter on the source field when the referrer lands in medium (or the reverse); stale referrer list | AI traffic reported as zero | Contains-match on both fields; recheck quarterly | 4 |

## Decoys

Stable Direct of 10-25%; (not set) under about 1%; GA4 sessions a few percent
under ad clicks; engagement rate changes with no key-event change on that date.

---

## File: audit/references/meta.md

# Meta and other paid social

Split the account by job before reading any number: prospecting (cold reach
that creates demand) and retargeting (closing people who already engaged).
They do opposite work and cannot share a scorecard.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| M1 | Attribution setting per campaign or ad set (for example `7d_click_1d_view`, `1d_click`) | Campaigns on different windows compared side by side; view-through included on some only | Different windows answer different questions; the view-through campaign looks better by construction | Set one window for comparisons; report the window on every number | 1 |
| M2 | Meta purchase value vs the store or analytics total | Meta's claimed revenue plus other platforms' claims above the store total | Meta counts view-through on its own window; the same sale is claimed twice | Judge against one shared revenue number; label platform figures as claims | 1 |
| M3 | Conversion event used for optimisation | Campaign optimising for add to cart, landing page view or a lead form while the goal is purchase | The algorithm finds cheap clickers, not buyers | Optimise for the event that means money when volume allows | 1 |
| M4 | CTR definition | CTR on all clicks (likes, profile taps, see more) instead of link clicks | Incidental taps inflate CTR; creative looks better than it is | Use link clicks / impressions; link CTR around 0.8-2.5% is the normal band | 1 |
| M5 | Prospecting frequency and CTR over the same weeks | Weekly frequency well above about 2-4 while link CTR falls | Creative fatigue; more budget makes it worse | Rotate creative before raising budget | 3 |
| M6 | Prospecting CPM trend at flat reach | CPM rising while reach is flat | Audience too narrow or creative fatiguing | Broaden the audience or refresh creative | 3 |
| M7 | Prospecting judged on ROAS | Prospecting cut or held to a return target because retargeting returns more | Retargeting's return is largely demand prospecting created; cutting prospecting dries up the warm pool later | Judge prospecting on CPM, reach, frequency and link CTR; retargeting on CPA and ROAS | 3 |
| M8 | Retargeting audience settings | No purchaser exclusion; very long membership; no frequency cap | Paying to reach recent buyers | Exclude purchasers for a sensible window; cap frequency | 2 |
| M9 | Reach summed across ad sets or weeks | Account reach equals the sum of ad set reach; reach above impressions | Reach is people, not additive; CPM per person and frequency are wrong | Take reach at the level and period reported by the platform | 1 |
| M10 | Retargeting ROAS used to justify scaling | No holdout | Much of it is people who would have bought anyway | Holdout before scaling | 5 |
| M11 | Strong CTR, expensive CPA | Diagnosis focuses on the ad | The ad did its job; the leak is after the click | Landing page, offer, audience-message fit | 3 |

## Decoys

CPM of 2-12; link CTR of 0.8-2.5%; retargeting ROAS several times
prospecting; Meta conversions above GA4's for the same campaign when the
windows differ (expected, not a bug, as long as nobody adds them up).

---

## File: audit/references/paid-search.md

# Paid search (Google Ads, Microsoft Ads)

Read the account in this order; do not tune devices or schedules while the
steps above them are broken: conversions, overview by campaign, brand vs
generic split, leakage, search-term waste, new queries, return on spend,
pacing, devices and timing.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| PS1 | Conversions segmented by conversion action | The Conversions column mixes micro actions (newsletter, account sign-up, add to cart) with purchases; CPA looks tiny, CVR spectacular | Smart Bidding and every CPA or ROAS read optimise toward email addresses, not sales | Make the purchase (or the action that means money) the only primary conversion; read CPA and ROAS on it | 1 |
| PS2 | Raw export with empty conversion columns | Profitability reads zero or blank | Analyst concludes "nothing converts" | Scope the export to a conversion action first | 1 |
| PS3 | Search terms by campaign type: brand campaign x brand query, generic campaign x brand query | Generic campaigns serving brand queries (generic looks brilliant); brand campaign paying for generic queries | Generic gets scaled on borrowed brand demand; brand budget leaks into low-intent traffic | Brand terms as negatives in generic campaigns; generic terms as negatives in brand | 2 |
| PS4 | Brand vs generic split of CTR, CPC, CPA | Account CTR or CPA healthy only because brand carries it; generic CPA above break-even | A blended average describes a business that does not exist; generic can lose money under brand's halo | Report brand and generic as separate lines, never blended | 2 |
| PS5 | Search terms sorted by cost with zero conversions | Informational or irrelevant clusters (how to, care, repair, jobs, free, second-hand, salary) with spend and no sales | Pure waste, every day | Negative the whole cluster; review the report monthly | 2 |
| PS6 | Search-terms coverage claims | The visible terms treated as all the terms ("waste is 8% of spend") | Since 2020 only terms with enough volume show; often 40-60% of click-driving queries are visible | Treat query level as a sample; make spend calls at campaign or ad group level | 4 |
| PS7 | Impression share, lost to budget, lost to rank, per campaign | A campaign beating its CPA target loses much impression share to budget, while uncapped campaigns above target run over budget | Profitable volume left unbought; money flowing to the worst unit economics | Raise the cap on the profitable campaign; pull back the over-target one | 3 |
| PS8 | Lost to rank on campaigns asking for budget | "Add budget" while lost to rank dominates | More budget buys nothing when rank is the limit | Fix Quality Score components or bids first | 3 |
| PS9 | Average CPC vs break-even CPC (margin per sale x CVR) per line | CPC above the ceiling on a line called "efficient" or "cheap" (40 margin x 5% CVR = 2.00 ceiling; a 2.40 click loses money) | Every click loses money on average | Cap bids at break-even or fix CVR; raise the ceiling only with repeat-purchase evidence | 3 |
| PS10 | Quality Score weighted by impressions or spend | Large share of spend on keywords with below-average landing page experience or QS 1-5 | QS 10 roughly halves CPC against average; QS 1 multiplies it several times | Fix the below-average component (page, relevance, expected CTR) before raising budget | 3 |
| PS11 | Account-level QS or impression share as a simple mean of rows | Small keywords weigh like flagship ones; "<10%" and ">90%" buckets treated as numbers | Wrong visibility number | Impression-weighted averages; treat buckets as clamped | 4 |
| PS12 | Match types: cost per sale, not CPC | Broad has the lowest CPC and the worst cost per sale, and budget is moving to it | Cheap clicks that never convert | Read cost per sale per match type; keep broad for discovery with negatives | 2 |
| PS13 | Ad groups: keywords per group | One group with dozens of mixed keywords and one generic ad | Lower CTR and higher CPC than tight groups | Split into themed groups of about 5-15 keywords with matching ad and page | 4 |
| PS14 | Month-to-date spend, trailing 7-day spend, projected month end per campaign | A profitable campaign hits its cap by midday every day; another runs far over plan | Google may spend up to 2x the daily budget on a day; only the month (daily x 30.4) is capped. Under-spend on a converter is the quiet failure | Project on the last 7 days per campaign; move money between campaigns | 3 |
| PS15 | Device and schedule modifiers on Target CPA or Target ROAS campaigns | Manual modifiers set and credited for results | Automated bidding prices device and time into each auction; the modifiers are not applied as set | Remove them or treat as no-ops; manage through targets | 4 |
| PS16 | Geo report | A map drawn from one pooled row or regions inferred from account names | Bids move on a number that does not exist per region | Adjust geo only where data resolves to real markets | 4 |
| PS17 | Brand campaign spend with no holdout | Brand ROAS cited as proof of value | Brand clicks may be ones the organic listing would win free; evidence goes both ways | Geo or time-split pause test; check organic brand position first | 5 |
| PS18 | Revenue ROAS on low-margin lines | Revenue ROAS above target on a line that loses money after cost of goods | Healthy revenue ROAS can be a loss | Profit on ad spend when margins are known | 3 |
| PS19 | Converting paid themes with no organic page | Paying every month for demand an evergreen page could win | Rented demand | Brief SEO pages from paid converting queries | 4 |
| PS20 | Markets and engines read only as a blended total | Strong home market masks a weak one | Losses subsidised and unseen | Read account by account and engine by engine | 3 |

## Decoys

Brand CTR of 30-50% and the lowest CPA; phrase or exact with the highest CPC
but a good cost per sale; a small lost-to-rank share on brand; impression
share reported as "<10%".

---

## File: audit/references/pmax.md

# Performance Max, Demand Gen, display and video

Read black-box formats after the readable ones (Search, Shopping). A black box
read first hides leaks the clear formats would show.

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| PM1 | PMax conversions by conversion action | Blended total mixing sign-ups and orders | Close to meaningless; one asset group may drive nearly all purchases while another drives none | Read through the purchase action only | 1 |
| PM2 | Brand vs non-brand share of PMax conversions; brand exclusions | Much of PMax's credit sits on brand searches you already rank first for organically; no brand exclusion | The scorecard is inflated by demand you already had | Add brand exclusions; compare brand and non-brand; read incremental, not self-reported | 2 |
| PM3 | Clicks vs CPC month over month | Clicks grow only because CPC climbs | Bought growth; fine only if conversions keep pace | Track volume against unit price | 3 |
| PM4 | PMax and Demand Gen both on the product feed | Both running with no owner for discovery | They compete for the same inventory | Decide which owns discovery | 4 |
| PM5 | PMax search-term insights | Converting non-brand terms not reused | Missed Search campaigns and SEO pages | Mine them into Search or SEO | 4 |
| DV1 | Display KPI | Display judged on CTR (about 0.46% is normal) or last click | Cuts a line doing its reach job | Judge on CPM, reach, viewable impressions, view-through and a holdout | 5 |
| DV2 | Placements: CPM, viewable rate, downstream sessions | Very low CPM, huge impressions, zero sessions, no viewability column | Signature of invalid traffic or made-for-advertising sites | Pull the placement report; exclude domains; viewable = at least 50% of pixels for 1 second (video 2 seconds) | 2 |
| DV3 | Retargeting settings | No purchaser exclusion; membership of a year or more; no frequency cap | Paying to resell to buyers; burnout | Exclude converters; shorten windows; cap frequency | 2 |
| DV4 | Retargeting share of the display story | Retargeting cited as the growth driver | It recaptures, it does not discover | Separate prospecting and retargeting; holdout before scaling | 5 |
| DV5 | Brand safety | No placement, content or topic exclusions; made-for-kids not excluded on YouTube | Spend in places that hurt the brand | Exclusion lists; prune placements | 3 |
| DV6 | Video quartile completion and CPV | Cheapest CPV line with the curve collapsing after 25% | Paid for a skip, not attention | Brand and hook in the first 5 seconds | 4 |
| DV7 | Frequency vs on-site demand over time | Frequency rising while demand flattens | Creative wear-out | Refresh or cap | 4 |
| DV8 | Demand Gen judged on last-click sales | Paused for an empty last-click column | A demand creator graded on a capturer's numbers | Reach and CPM, last-click as a floor, then a test | 5 |
| DV9 | "This image or audience won" in Demand Gen | Asset or seed-audience credit claimed | That breakdown is not cleanly in the data | Mark as unanswered | 5 |

## Decoys

Display CTR of 0.3-0.6%; blank conversion columns on small asset groups
(sparsity); retargeting ROAS above prospecting.

---

## File: audit/references/power-bi.md

# Power BI models (TMDL, PBIP, a list of DAX measures)

Read every measure the reports use, the disconnected tables (toggles and
selectors) and the relationships. Evaluate suspicious measures at two grains
(a day and a month, a campaign and the total); a correct ratio gives the same
answer as a DIVIDE of sums at each grain. Reading measures to reuse them in a
Claude dashboard is the `power-bi-definitions` skill.

## Measure checks

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| P1 | Ratio measures | `AVERAGE(Fact[ctr])`, `AVERAGEX(..., [rate])` or an average of a precomputed rate column | A day with 20 impressions weighs like a day with 20,000; the total is true of nothing | `DIVIDE(SUM(Fact[clicks]), SUM(Fact[impressions]))` | 1 |
| P2 | Snapshot measures (list size, subscribers, open pipeline, stock, followers) | `SUM` over a daily or monthly snapshot column | A month shows 30 times the list | Closing value: `CALCULATE(SUM(...), LASTDATE('Date'[Date]))`, or `LASTNONBLANKVALUE` over dates, or an average if that is the definition | 1 |
| P3 | Distinct counts | `SUM(Fact[active_users])` from a daily table used for monthly users | Users who visit on many days counted many times | Distinct count from user-level data, or a source monthly figure; label otherwise | 1 |
| P4 | Toggles and selectors: disconnected tables read with `SELECTEDVALUE(Table[Col], <default>)` | The default (no selection) differs from the agreed definition (gross instead of net revenue; 28-day click instead of 7-day; all channels instead of paid) | Every card nobody filtered shows the wrong version; exports and subscriptions too | Default to the agreed value; or make the slicer single-select with a required default; state the default in the description | 1 |
| P5 | Platform revenue measures | Google and Meta claimed revenue added into one "Paid Revenue" and divided by spend | Stacked ROAS | ROAS on store or analytics revenue; platform claims as separate, labelled measures | 1 |
| P6 | Duplicate business metrics | Two CAC (or ROAS) measures with different filters or exclusions | Two numbers for one KPI across pages | One canonical measure; retire or rename the other | 2 |
| P7 | `CALCULATE` filters | A filter on a column the user also slices on, which silently replaces the slicer | Cards ignore the page filter | `KEEPFILTERS`, or document the override | 2 |
| P8 | BLANK vs zero | `+ 0` or `IF(ISBLANK(...), 0)` on every measure | Rows appear for every combination; averages fall | Keep BLANK unless zero is meant | 4 |
| P9 | Measure descriptions and formats | No description on measures the reports use | Meaning is a guess | Description with numerator, denominator, grain, filters | 4 |
| P10 | Template vs client copies | The template changed a definition; client copies still carry the old one | "The same KPI" differs by client | Detect drift per copy; fix with an allowlist for intended differences | 2 |

## Model and process checks

| # | Look at | Red flag | Fix | Tier |
|---|---|---|---|---|
| P11 | Text-model structure | Broken table references; duplicate lineage tags | Run a read-only lint; apply only mechanical fixes; re-check | 2 |
| P12 | Versioning | Model only as .pbix, no checks before deploy | PBIP/TMDL in git with a linter in CI | 4 |
| P13 | Openability | Validated on paper only | Open in Desktop and record the result | 4 |
| P14 | Auto-fix boundary | A business definition "fixed" by a tool | Mechanical fixes only; judgement items stay open for a human | 2 |

## How to prove each finding

- Averaged rate: compute the measure as written and as DIVIDE of sums on the
  sample data or on two made-up rows (20 impressions at 10% and 20,000 at 2%:
  average 6%, true 2.01%).
- Summed snapshot: compare the measure for a month with the last day's list
  size.
- Toggle default: write what a card shows with no slicer selection, and what
  the description or the business says it should show.

## Decoys

`DIVIDE(SUM(...), SUM(...))` ratios; `REMOVEFILTERS` in a share-of-total
measure that is labelled as such; a disconnected table whose default matches
the stated definition; `SUMX` over a fact table of additive amounts.

---

## File: audit/references/search-console.md

# Search Console and SEO

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| S1 | Brand vs non-brand split of clicks and conversions | One organic rate with no split | Non-brand is the part that acquires; brand warmth hides a weak growth engine | Brand / non-brand as the first cut on every organic rate | 1 |
| S2 | Query-level vs query+page impressions | Demand sized from summed query-page rows | One impression per page shown, so the sum double counts; the gap is a cannibalisation list | Demand at query level; page assignment at query-page level | 1 |
| S3 | Ratios rolled up | Cluster or property CTR as a mean of row CTRs | A number true of nothing | Sum clicks / sum impressions at every grain | 1 |
| S4 | Country x device | A healthy property CTR hides a large segment at very low CTR and deep position | The blended number funds no fix | Scope to served markets and buyer devices | 3 |
| S5 | Position 1-3 with low CTR | Top-three position with CTR far under about 10% on high impressions | Clicks left at a rank you already hold | Rewrite title and meta to the intent; not a link problem | 3 |
| S6 | Effort by position band | Work on positions 1-3 (defend only) or 50+ | Effort that moves nothing | Rank-push list: high impressions at positions about 4-20 | 4 |
| S7 | Sitemap URLs vs pages with impressions | Sitemap URLs with no impressions | Not indexed, blocked or off-target | Check noindex, robots, canonical | 2 |
| S8 | New landing pages earning first impressions per month | Trending to zero while clicks hold flat | Coasting on old pages toward decline | Restart the content pipeline | 3 |
| S9 | Top-click pages joined to sessions and conversions | The biggest organic page converts far under the site; a high-CVR page with few sessions sits on a CRO list | Ranking work wasted; the page that works gets changed instead of fed | Fix intent on the first; send links and ranking effort to the second | 3 |
| S10 | Informational page ranking for transactional queries | Explainer collecting buying queries at page two | Buying demand stuck on a page that cannot close it | Point the product page at the buying terms | 3 |
| S11 | Content plan order | Ranked by volume for a shop | Low-converting topics first | Rank by paid CVR on the same queries (an estimate) for a store | 4 |
| S12 | Brand paid spend on queries ranking first organically | High brand spend, no test | Possibly paying for free clicks; evidence goes both ways | Pause test, not a blind cut | 5 |
| S13 | Report filters | Organic or CVR columns blank because of a filter or no conversion selected | Reads as "no organic" | Fix the filter | 1 |
| S14 | Last 2-3 days | Dip in the final days read as a drop | Search Console lags 2-3 days | Exclude the lag window | 1 |
| S15 | Clicks vs sessions reconciliation | Gap treated as lost traffic | Different systems; time wasted | Read each column against itself | 4 |
| S16 | Backlinks | High spam score; no new links in 3 months; links from 1-2 domains | Ranking risk | Disavow high-risk; earn editorial links | 4 |
| S17 | Local listings (if physical locations) | Generic category; NAP mismatches; no recent reviews | Lost map visibility | Exact NAP everywhere; review velocity | 4 |
| S18 | "AI citation share" metrics | Presented as measured | Not cleanly measurable today | Use proxies: branded query growth, AI-referral sessions | 5 |

## Decoys

GSC clicks above GA4 organic sessions; position quoted as an
impression-weighted average; low-impression rows with noisy positions that
nobody acts on.
