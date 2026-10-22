# email-mix

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/whats-changed/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/email-mix/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Our email exports for August and September 2026 are in the resources/ directory (email_sends.csv, one row per campaign send to one segment). Write a short performance report to report.md: how did email do in September compared with August, why, and what should we do next?
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `conversion-decline` | PASS | PASS | A: click-to-order 11.9% to 10.0%; B: orders fell while clicks held or rose |
| `decomposition-quantified` | PASS | FAIL | A: four-driver bridge summing to +3,228 and mix +0.79 / rate -0.43 pts; B: before/after by segment only, no attributed shares |
| `mix-explained` | PASS | PASS | both: VIP drives the blended gain, Newsletter and Active fell |
| `no-open-rate-headline` | FAIL | PASS | A: makes "opens back to 38%" the success check for an action and reads the open drop as an inbox problem, no privacy caveat; B: open rate in tables and one cause line, not a success metric (borderline) |
| `verifiable-actions` | PASS | FAIL | A: every action has a Verify line, causes labelled hypotheses; B: "Keep the VIP program" and "track like-for-like" have no check |

## Re-run of arm A after the skill fix

| Grader | A, first run | A, re-run | Why |
|---|---|---|---|
| `conversion-decline` | PASS | PASS | click-to-order 11.94% to 10.00% |
| `decomposition-quantified` | PASS | PASS | four-driver bridge to +3,228 plus mix vs rate for CTR and click-to-order |
| `mix-explained` | PASS | PASS | VIP drives the gain; Newsletter and Active fell |
| `no-open-rate-headline` | FAIL | PASS | open rate mentioned once, with "do not use it as evidence: privacy features inflate opens"; actions verified on orders and click-to-order |
| `verifiable-actions` | PASS | PASS | every next step has a check; causes labelled hypotheses |

## Arm A answer (with skill)

````markdown
# Email performance, September vs August 2026

**September revenue rose $3,228 (+11.2%) to $32,128, but the whole gain comes from one new send: VIP Early Access added $10,400. The two existing lists lost $7,172 (-24.8%) and orders fell 2.2%, from 740 to 724.**

Comparison: August (four sends each to Newsletter subscribers and Active customers, 2026-08-04 to 08-25) against September (four sends each to Newsletter and Active, plus four VIP Early Access sends, 2026-09-01 to 09-22). Both months have four weeks and the same weekday. The export states no conversion window.

## Check the data before acting

Every weekly row is identical to the other weeks of the same segment and month. Newsletter and Active in both months, and VIP in September, each repeat one set of numbers four times. Real weekly sends almost never match to the unit, so the export may be a template or monthly averages copied into weekly rows. Everything below assumes the rows are real. If they are not, the arithmetic holds but the conclusions do not. Pull true per-send figures from the email platform first. Pass: the four weeks of each segment differ.

## Why revenue rose

Revenue = delivered x click rate x click-to-order x average order value. The four factors multiply to the change exactly.

| Driver of revenue change (Aug to Sep) | Amount |
|---|---|
| Delivered (156,360 to 167,416, +7.1%) | +$2,083 |
| Click rate (3.96% to 4.32%, +9.1%) | +$2,664 |
| Click-to-order (11.9% to 10.0%, -16.3%) | -$5,414 |
| Average order value ($39.05 to $44.38, +13.6%) | +$3,895 |
| **Total change** | **+$3,228** (= $32,128 - $28,900) |

Click rate rose, but click-to-order fell by more, so fewer clicks became orders. The gain comes from order value and from the VIP send.

Revenue by segment: VIP Early Access +$10,400 (new), Newsletter -$4,960, Active customers -$2,212. VIP alone exceeds the total gain. Orders by segment: VIP +200, Newsletter -148, Active -68, so total orders fell by 16.

## Click rate: mix or behaviour

Click rate rose 0.36 points (3.96% to 4.32%). Mix vs rate:

- Mix +0.79 points, almost all from the VIP send (+0.77), whose 19.0% click rate lifts the blend.
- Rate -0.43 points, from Newsletter (-0.45), with Active flat (+0.02).

Noise screen: the Newsletter click rate fell 0.60 points against a noise band of about 0.14 points, a clear change. Active rose 0.10 points against a band of about 0.33, within normal variation.

## What is driving the decline (hypotheses)

- **Newsletter opens fell from 40.0% to 33.3%.** Click-to-open held at 9.0% in both months, so content converts the people who open. The drop sits at the inbox: subject line, send time or deliverability. Hypothesis; the export has no subject-line or inbox-placement data.
- **Active customers: click-to-order fell from 14.1% to 10.1%, while order value rose from $41 to $44.** Fewer purchases at higher order value suggests the offer or landing page changed for this list. Hypothesis, to check against the send content.
- **VIP may take orders from the other lists.** Orders from the two existing lists fell by 216 while VIP added 200. If the same people sit on the Active and VIP lists, part of VIP's revenue is the same orders counted twice or moved from another send. The export does not say whether the lists overlap or which attribution window applies.

## What to do next

1. **Confirm the data.** Decide nothing on monthly totals until weekly figures are checked. Verify: the four weeks differ and the totals match the platform.
2. **Keep VIP Early Access, but test it.** Hold back a random 10 to 20% of eligible VIP buyers for four sends and compare total orders per week across all three lists. Verify: total orders per week rise above August's 185. September averaged 181.
3. **Fix Newsletter opens.** Test two subject lines and one send time on the next four sends, and check inbox placement. Verify: opens back to 38% or more, with click-to-open still near 9%.
4. **Check the Active offer and landing page.** Compare the page each Active click lands on in August and September. Verify: click-to-order back near 14%, or a reason found for the change.
5. **Report weekly, not monthly.** Track orders, revenue and click-to-order by list each week against these baselines.

Limits: no prior-year months, so seasonality is untested. No attribution window or list-overlap field. The weekly rows look copied.
````

## Arm B answer (without skill)

````markdown
# Email performance: September vs August 2026

Source: resources/email_sends.csv (20 rows: 8 August sends, 12 September sends). Rates use delivered as the base, except CTOR (clicks / opens). Revenue is in the export's unit; currency not stated.

## Headline
September revenue rose 11.2% (28,900 to 32,128), but orders fell 2.2% (740 to 724). The rise comes from a new segment (VIP repeat buyers), not the existing lists. On the two segments sent in both months (Newsletter subscribers, Active customers), revenue fell 24.8% (28,900 to 21,728) and orders fell 29.2% (740 to 524), while delivered rose 1.5% (156,360 to 158,704).

## Totals
| Metric | August (8 sends) | September (12 sends) |
|---|---|---|
| Delivered | 156,360 | 167,416 |
| Unique open rate | 40.0% | 36.5% |
| Click rate | 4.0% | 4.3% |
| CTOR | 9.9% | 11.9% |
| Unsubscribe rate | 0.15% | 0.15% |
| Orders per 1,000 delivered | 4.7 | 4.3 |
| Revenue | 28,900 | 32,128 |
| Revenue per delivered | 0.185 | 0.192 |
| Revenue per order | 39.05 | 44.38 |

Like-for-like (Newsletter + Active customers only):
| Metric | August | September |
|---|---|---|
| Open rate | 40.0% | 35.0% |
| Click rate | 4.0% | 3.5% |
| Orders per 1,000 delivered | 4.7 | 3.3 |
| Revenue | 28,900 | 21,728 (-24.8%) |
| Revenue per delivered | 0.185 | 0.137 |

## By segment
- Newsletter subscribers (4 sends each month): open rate 40.0% to 33.3%; click rate 3.6% to 3.0%; orders 480 to 332 (-31%); revenue 18,240 to 13,280 (-27%). List grew 31,000 to 31,500 per send.
- Active customers (4 sends each): open rate 40.0% to 40.8%; click rate 5.2% to 5.3%; orders 260 to 192 (-26%); revenue 10,660 to 8,448 (-21%). Revenue per order 41.0 to 44.0.
- VIP repeat buyers (new in September, 4 sends): open rate 63.4%; click rate 19.0%; orders 200; revenue 10,400 (32% of September revenue); revenue per order 52.00; unsubscribe rate 0.14%.

## Why
The export has no subject lines, offers, send times or content, so cause cannot be confirmed. What it shows:
1. The September gain is the VIP segment. Without VIP, September revenue is down about a quarter.
2. Newsletter engagement dropped on the same-size list: open rate down about 7 points, click rate down about 0.6 points. Points to content, subject line, timing or fatigue; the data does not say which.
3. Active customers held engagement but ordered less: orders and revenue fell while opens and clicks stayed flat or rose.

## Data checks before acting
- Every week repeats identical numbers: all four August sends per segment match, and all four September sends per segment match. Either the export copied one week into the others or it holds monthly totals. Week-by-week trends cannot be read from this file. Confirm with whoever built it.
- Possible overlap: if VIP repeat buyers are also in Active customers, September orders and revenue are double-counted. Check segment definitions before quoting the 11.2% gain.

## Next steps
1. Fix the export (or confirm the weekly figures) and re-run by week.
2. Check the September newsletter changes (subject, send time, content, offer) against August; A/B test the August version against the current one for the next two sends.
3. Keep the VIP early-access program (best rates and revenue per order), after confirming overlap with Active customers.
4. Review the active-customer offer and landing page: engagement held, so the gap is likely in the offer or conversion path.
5. Track like-for-like segments so new segments do not hide drops in existing ones.
````

## Arm A re-run answer (after the skill fix)

````markdown
# September email revenue rose 11%, but only because of the new VIP sends

September email revenue was $32,128 against $28,900 in August, up $3,228 (+11.2%). Orders fell from 740 to 724. The whole gain comes from VIP Early Access, a segment that was not sent in August: it added $10,400 and 200 orders. The Newsletter and Active customer sends lost $7,172 (-25%) on about 1.5% more delivered volume. Those two segments are where the decline is real.

Both months are four sends per segment, with the same weekly dates (Aug 4 to 25, Sep 1 to 22).

## The arithmetic

Revenue = delivered x CTR x click-to-order x average order value (AOV). Four-week totals, summed over sends. The log decomposition is exact.

| Driver of revenue change (Aug to Sep) | Aug | Sep | Change | Contribution |
|---|---|---|---|---|
| Delivered | 156,360 | 167,416 | +7.1% | +$2,083 |
| CTR (clicks / delivered) | 3.96% | 4.32% | +9.1% | +$2,664 |
| Click-to-order (orders / clicks) | 11.94% | 10.00% | -16.3% | -$5,414 |
| AOV | $39.05 | $44.38 | +13.6% | +$3,894 |
| **Total** | **$28,900** | **$32,128** | **+11.2%** | **+$3,228** (drivers sum to $3,227; $1 rounding) |

By segment:

| Segment | Aug revenue | Sep revenue | Change |
|---|---|---|---|
| Newsletter subscribers | $18,240 | $13,280 | -$4,960 |
| Active customers | $10,660 | $8,448 | -$2,212 |
| VIP repeat buyers (new in Sep) | $0 | $10,400 | +$10,400 |
| **Total** | **$28,900** | **$32,128** | **+$3,228** |

Mix vs rate:

- CTR +0.36 points = +0.79 points of mix + (-0.43) points within segments. The mix is almost all VIP (+0.77 points), because VIP clicks at 19.0%.
- Click-to-order -1.94 points = -2.34 points within segments + 0.40 points of mix.

Noise screen (2 x standard error band):

- Newsletter CTR 3.60% to 3.00% (-0.60 points, band 0.14): clear decline.
- Active CTR 5.20% to 5.30% (+0.10, band 0.33): no clear change.
- Newsletter click-to-order 11.0% to 9.0% (-2.0 points, band 1.3): clear decline.
- Active click-to-order 14.1% to 10.1% (-4.0 points, band 2.1): clear decline.

## What is happening

- Newsletter and Active customers clicked about as often, but fewer of those clicks turned into orders. Click-to-order fell in both segments. The data cannot show why. Hypotheses to test: a weaker offer, a landing page change, or a different product mix.
- AOV rose in every segment (Newsletter $38 to $40, Active $41 to $44). That kept the base segments from falling further.
- Unsubscribes held at about 0.15% of delivered in both months.
- Open rate fell from 40.0% to 36.5%. Do not use it as evidence: privacy features inflate opens. Judge the sends on orders and revenue.

## Why the VIP gain may overstate the result (hypothesis)

The base segments lost 216 orders and VIP added 200, so the net change is -16 orders. The VIP sends went out on the same days as the newsletter and Active sends. If VIP buyers were already on the Active list and would have bought in the regular send anyway, VIP moved orders rather than adding them. The export cannot show list overlap.

## Check the data before using these dollars

Every column repeats the same figure in all four weeks of each month, to the unit. That is unlikely for real sends. If each row is really a monthly total, the dollar totals are four times too large. The percentages do not change, but the noise bands are about half as wide as they should be. Confirm the rows against the email platform's send log. The Sep 22 sends may also still be collecting orders if the export was taken before the attribution window closed.

## Next steps

1. Confirm the export. Owner: data team. Check: each weekly row matches the send log, and the Sep 22 orders are final.
2. Test whether VIP adds orders. Split the VIP list for the next send, with a random holdout. Compare total orders per delivered across the two groups, not opens. Check: if the holdout buys about as much as the VIP group, VIP is moving orders from the regular sends.
3. Find the click-to-order drop in Newsletter and Active. Compare offer, price and landing page between an August and a September send. Check: click-to-order is back above 11% on the next Newsletter send.
4. Keep VIP only if total orders per delivered across the sends rise. Judge on orders and revenue.
````
