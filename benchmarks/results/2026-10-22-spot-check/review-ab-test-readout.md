# review-ab-test-readout

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/review/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/review-ab-test-readout/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Our ecommerce team wrote up the product page test (resources/ab_test_readout_complete_the_set.md) and the raw daily numbers are in resources/ab_test_daily.csv. The head of ecommerce wants to sign the platform contract next week based on this. Is the readout right? Tell me what, if anything, needs fixing before it goes to her, and whether the recommendation stands. Write it up in report.md.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `decoys-left-alone` | FAIL | FAIL | both raise the per-user conversion definition (orders vs buyers) as a finding to fix, though the data cannot show a problem |
| `must-fix-first` | PASS | FAIL | A: break-even and 4-day test are the two Must fix items; B: no groups, the business case is 4th and the short test 6th |
| `planted-recall` | PASS | PASS | A: 4 of 5 (misses the 0.4% wording); B: 5 of 5 |

## Re-run of arm A after the skill fix

| Grader | A, first run | A, re-run | Why |
|---|---|---|---|
| `decoys-left-alone` | FAIL | PASS | the orders-vs-buyers doubt now sits under Not checked as a question for the owner; SRM and rates listed as checked and fine |
| `must-fix-first` | PASS | PASS | break-even and the 4-day test are Must fix 1 and 2 |
| `planted-recall` | PASS | PASS | 5 of 5 (now also the 0.4% wording) |

## Arm A answer (with skill)

````markdown
# Review: "Complete the set" product page A/B readout

Verdict: Do not send as written. The widget probably lifts conversion, but the readout's own numbers do not support signing the 12-month contract, and its "consistent across the test" claim is contradicted by the daily data.

What this report says: The "Complete the set" widget raises conversion from 3.25% to 3.61% (p = 0.008), so ship it to 100% of mobile traffic on Monday and sign the 12-month platform contract at $65,000 a month.
Who decides what: The head of ecommerce decides whether to sign the 12-month platform contract (about $780,000 in total).

## Must fix

1. **The business case does not cover the cost.** (Business case section)
   - **What it says:** "The test result is statistically significant, so the cost is justified."
   - **What is wrong:** Significance says the lift is probably real. It does not say the lift pays for the platform. Scaling the 4-day test to a 30-day month (x 7.5, assuming the same traffic and the same effect):
     - All traffic: incremental revenue = 114,847.94 - 104,159.21 = 10,688.73 over 4 days, about 80,165 a month. Gross profit at 40% is about 32,066 a month, against a 65,000 cost. Short by about 33,000 a month.
     - Mobile only (the recommendation): incremental revenue = 66,664.22 - 58,135.93 = 8,528.29 over 4 days, about 63,962 a month. Gross profit is about 25,585 a month. Short by about 39,400 a month.
     - Break-even: 65,000 / 0.40 = 162,500 of incremental revenue a month. The test implies a 10.3% revenue lift on all traffic (20.8% needed) and 14.7% on mobile (37.3% needed).
   - **Fix:** Replace the sentence with: "At the test's effect, gross profit from all traffic is about 32,000 a month against a 65,000 cost. Break-even needs a revenue lift of about 21%; the 4-day test measured about 10%. We will not sign until a longer test shows the lift is large enough." Assumes revenue is gross and the 40% margin applies to it; the ecommerce team should confirm both.
   - **If you skip it:** About 780,000 is committed over 12 months for a widget that, on the readout's own numbers, returns about half its cost even on all traffic.

2. **The test is 4 days and the lift is fading.** (Results section; "consistent across the test")
   - **What it says:** "The lift was consistent across the test, so we expect it to hold after launch."
   - **What is wrong:** Daily conversion lift, in percentage points (B minus A), recomputed from the CSV:

     | Day | All | Mobile | Desktop |
     |---|---|---|---|
     | 14 Sep | +0.65 | +0.66 | +0.64 |
     | 15 Sep | +0.53 | +0.57 | +0.47 |
     | 16 Sep | +0.16 | +0.29 | -0.04 |
     | 17 Sep | +0.09 | +0.28 | -0.23 |

     The first two days average +0.59 points and the last two +0.13. The difference is 0.47 points, z about 1.7, p about 0.09. That is not proof of decay, but it is the opposite of "consistent" and fits a novelty effect. A 4-day test is shorter than one full week, and each day has only about 9,000 users per arm, so single-day lifts carry roughly ±0.26 points of noise. The trend is a warning, not a verdict.
   - **Fix:** Replace the sentence with: "The lift was larger in the first two days (+0.59 points) than in the last two (+0.13). The test ran 4 days, which is less than a week, so we cannot yet separate novelty from a real effect." Then run at least four whole weeks with a decision rule set in advance: ship only if the lift's 95% interval stays above the break-even conversion lift of about 0.7 points (20.8% of 3.25%, holding order value constant).
   - **If you skip it:** A launch is sized on the first two days of a fading effect, and the contract locks in that size for 12 months.

## Should fix

3. **"Works on mobile, does little on desktop" is a post-hoc split, and the gap is not shown.** (By device section)
   - **What it says:** "The widget clearly works on mobile and does little on desktop."
   - **What is wrong:** Mobile lifts 0.45 points (2.90% to 3.35%, +15.5%, p about 0.006). Desktop lifts 0.21 points (3.81% to 4.03%, +5.6%, p about 0.36). The gap between the two lifts is 0.24 points, z about 0.8, p about 0.4. Both are positive, and the difference is within chance. The readout also does not say the split was planned. The same CSV splits visitors by type: returning visitors lift 0.61 points (3.92% to 4.52%, p about 0.008), new visitors 0.16 points (2.75% to 2.91%, p about 0.31), and that gap is not significant (p about 0.12).
   - **Fix:** Replace the sentence with: "Mobile conversion rose 0.45 points and desktop 0.21 points. The difference between them is not significant, and the split was not planned. Treat 'mobile works best' as a hypothesis to test in a planned mobile-versus-desktop test before restricting the rollout."
   - **If you skip it:** The mobile-only rollout is built on a cut that may be chance, and it drops any desktop effect the data does not rule out.

4. **The primary metric and the table count different things.** (Setup and Results sections)
   - **What it says:** The primary metric is "users who ordered / users exposed", but the table divides orders by users (1,177 and 1,308 orders).
   - **What is wrong:** If a user can place more than one order in the test, the rate counts orders, not buyers, and the z-test (which treats each user as one trial) is then overstated. The CSV has no user-level data, so this cannot be confirmed from the files.
   - **Fix:** Ask the ecommerce team to confirm whether "orders" is a count of buyers per arm. If it is not, recompute the rate and the z-test on distinct buyers per arm and replace the figures.
   - **If you skip it:** The headline p-value may be too small, and the contract rests on it.

## Nice to have

None.

Checked and fine: Totals recompute from the daily rows: users 36,236 (A) and 36,265 (B), orders 1,177 and 1,308, revenue $104,159.21 and $114,847.94. Sample ratio: each arm's expected count is 36,250.5, deviation 14.5 each, chi-square 0.012, p about 0.91, so no sample ratio mismatch. Conversion rates 3.25% and 3.61%; two-proportion z = 2.66, p = 0.008; 95% interval +0.09 to +0.62 points, all recomputed and correct. Device conversions and relative lifts match the CSV (mobile 2.90% to 3.35%, +15.5%; desktop 3.81% to 4.03%, +5.6%). Revenue per user rises from $2.87 to $3.17 (+10.2%), consistent with the conversion lift. The test window is 14 to 17 September, as stated.

Not checked: Whether "orders" counts buyers or purchases (no user-level data). Whether revenue is gross or net of discounts and returns, and whether the 40% margin applies to it. Whether the $65,000 monthly fee changes with traffic or with a mobile-only rollout. Any weekly pattern beyond four days.
````

## Arm B answer (without skill)

````markdown
# Review of the "Complete the set" A/B readout

## Bottom line

The arithmetic ties out, but the readout's conclusions do not. The overall lift is real but small, it faded over the four test days, and the business case fails on the readout's own numbers. The recommendation does not stand. Do not sign the 12-month platform contract next week on this readout.

## What checks out

I rebuilt the totals from the 32 rows of `ab_test_daily.csv`:

- Users: control 36,236, treatment 36,265. Both match.
- Orders: control 1,177, treatment 1,308. Both match.
- Revenue: control $104,159.21, treatment $114,847.94. Both match.
- Sample ratio check: chi-square 0.01, p about 0.91. Correct.
- Conversion: A 3.25%, B 3.61%. Difference +0.36 points.
- Two-proportion z-test: z about 2.65, p about 0.008. Correct.
- 95% CI on the difference: +0.09 to +0.62 points. Correct.
- Device conversions: mobile 2.90% vs 3.35% (lift 15.5%), desktop 3.81% vs 4.03% (lift 5.6%). Correct.

## What needs fixing

1. **Wrong framing of the effect.** "About 0.4% more visitors buy" is wrong. The absolute lift is 0.36 percentage points, which is about an 11% relative lift (3.25% to 3.61%). Report both, and state which one you mean.

2. **"Consistent across the test" is false.** The daily lift in points, from the CSV:

   | Day | Control conv. | Treatment conv. | Lift (pts) |
   |---|---|---|---|
   | 2026-09-14 | 3.25% | 3.90% | +0.65 |
   | 2026-09-15 | 3.21% | 3.74% | +0.53 |
   | 2026-09-16 | 3.25% | 3.42% | +0.16 |
   | 2026-09-17 | 3.28% | 3.36% | +0.09 |

   The effect shrinks every day and is near zero by the last two days. This pattern is consistent with a novelty effect. It does not support "we expect it to hold after launch".

3. **The device claim is overstated.** The readout says the widget "clearly works on mobile and does little on desktop". The device split was not the pre-specified primary analysis. The mobile subgroup alone gives z of about 2.7 (p about 0.006). The desktop subgroup gives z of about 0.9 (p about 0.36). The difference between the two lifts is not significant (z of about 0.8). The data do not show that mobile and desktop respond differently. The mobile-only rollout rests on a post-hoc split that the data does not establish.

4. **The business case is a non sequitur.** "Statistically significant, so the cost is justified" does not follow. Significance says nothing about whether the gain covers the cost. Working from the test's own numbers at the stated 40% margin:
   - Site-wide incremental revenue is $10,688.73 over 4 days, about $2,672 per day. At 30.4 days per month that is about $81,000 revenue per month, or about $32,500 gross profit per month.
   - Mobile-only incremental revenue is $8,528.29 over 4 days, about $25,900 gross profit per month.
   - The platform costs $65,000 per month, or $780,000 over 12 months.
   - Break-even needs about $162,500 incremental revenue per month. The observed run rate is about half of that, and the most recent days run lower still.

   The mobile-only plan also does not reduce cost, unless the licence price is per device or per traffic. Confirm that.

5. **Metric definition needs checking.** The primary metric is defined as "users who ordered / users exposed". The CSV holds order counts, not distinct buyers. If a user can place several orders, the rate is not the defined metric. Confirm the source query.

6. **The test is short.** It covers four weekdays, Monday to Thursday, with no weekend. Two full weeks, including a weekend, would be the minimum for a decision of this size.

7. **Unreported split.** The lift is concentrated in returning visitors (3.92% vs 4.52%, +0.61 points) against new visitors (2.75% vs 2.91%, +0.16 points). This is not in the readout. Treat it as a hypothesis to test, not a finding.

## Does the recommendation stand?

No. Both parts fail:

- "Ship to 100% of mobile on Monday" rests on a post-hoc device split. The split is not significant as a difference, and the mobile effect is fading.
- "Sign the 12-month contract" rests on a significance test, not on the economics. On the test's own numbers the widget covers roughly 40% to 50% of its licence cost, and the trend is falling.

## Suggested next steps

- Extend the test to at least two full weeks, including a weekend. Pre-register the mobile hypothesis, or run a holdout.
- Confirm the metric definition and whether the licence is per device or per traffic.
- Redo the business case with break-even, the decaying daily lift, and the contract's real pricing. Negotiate a shorter term or a pilot if the case still does not close.
- Rewrite the readout: correct the 0.4% wording, drop "consistent across the test", and soften the device claim until it is tested.
````

## Arm A re-run answer (after the skill fix)

````markdown
Verdict: Do not sign the 12-month contract on this readout. The main conclusion (ship the widget and sign) is not supported by its own numbers.

What this report says: The "Complete the set" widget raises conversion from 3.25% to 3.61% (+0.36 points, significant), so ship it to all mobile traffic on Monday and sign the 12-month platform contract at $65,000 a month. Desktop stays on the current page.
Who decides what: the head of ecommerce decides whether to sign the platform contract next week.

## Must fix
1. **The platform does not pay back on the readout's own figures** (Business case section)
   - **What it says:** "The test result is statistically significant, so the cost is justified." Platform cost is $65,000 a month; gross margin 40%.
   - **What is wrong:** Significance tests whether the lift is zero. The question is whether the extra gross profit covers the cost. From the daily file, treatment revenue minus control revenue is $10,688.73 over the 4 test days (about $2,672 a day). Scaled to 30 days that is about $80,165 revenue, or $32,066 gross profit a month, against $65,000 cost: short by about $32,934 a month. Mobile only (the recommendation): $8,528.29 over 4 days, about $63,962 revenue and $25,585 gross profit a month, short by about $39,415 a month. Break-even for the whole site needs about $162,500 extra revenue a month, a 20.8% revenue lift on the control's roughly $781,000 a month; the observed revenue lift is 10.3%. Mobile break-even is about 37% against an observed 14.7%.
   - **Fix:** Replace the business case with: "Measured revenue lift is 10.3% across all devices (about $80k a month on a 4-day scale-up). At 40% margin that is about $32k gross profit a month against a $65k platform cost. The widget needs a 20.8% lift to break even. Do not sign a 12-month contract ($780k) until a longer test shows that." Also do not claim the cost is justified by significance.
   - **If you skip it:** $780,000 of committed spend on a platform the readout's own revenue data shows loses about $33k a month.

2. **The test is too short, and the lift is not consistent** (Test window and "consistent across the test")
   - **What it says:** "The lift was consistent across the test, so we expect it to hold after launch." Test window 14 to 17 Sep.
   - **What is wrong:** The test covers 4 days, not whole weeks. Daily conversion (control / widget) and lift: 14 Sep 3.25% / 3.90% (+0.65 pts); 15 Sep 3.21% / 3.74% (+0.53); 16 Sep 3.25% / 3.42% (+0.16); 17 Sep 3.28% / 3.36% (+0.09). The lift falls every day and is near zero on the last two. The readout's "consistent" claim is contradicted by its own file. A decline like this can be a novelty effect (a hypothesis, not proven). Daily samples are about 9,000 users per arm, so single days are noisy, but the readout cannot say the lift holds. The last two days alone give about +$1,658 revenue over 2 days; if that rate held, it is about $24.9k revenue a month, or $9.9k gross profit.
   - **Fix:** Replace "consistent" with: "Lift was +0.65 pts on day 1 and +0.09 pts on day 4; the effect is falling and the test ran 4 days. Re-run for at least 2 full weeks, with the lift and the break-even reported per week." Do not treat the 4-day average as the steady-state effect.
   - **If you skip it:** The 12-month contract is priced on an effect that may already be fading.

3. **The headline effect size is misstated** (Summary paragraph "In plain terms")
   - **What it says:** "The widget makes about 0.4% more visitors buy."
   - **What is wrong:** The gap is 0.36 percentage points (3.25% to 3.61%). Relative to control that is +11.1% more buyers (3.61 / 3.25 = 1.11). "0.4%" reads as a 0.4% relative gain, understating the effect about 27 times while mixing percentage points with percent.
   - **Fix:** "Conversion rises 0.36 percentage points, from 3.25% to 3.61%: about 11% more buyers than the current page."
   - **If you skip it:** The reader sizes the payoff from the wrong number and cannot judge the contract against it.

## Should fix
4. **The mobile-only recommendation rests on an untested device split** (By device section and recommendation item 1)
   - **What it says:** "The widget clearly works on mobile and does little on desktop." Mobile lift 15.5%, desktop 5.6%.
   - **What is wrong:** The device figures recompute (mobile 2.90% to 3.35%, desktop 3.81% to 4.03%). But the split was not pre-planned and the difference between devices is not tested. Mobile lift +0.45 pts, z = 2.74. Desktop lift +0.21 pts, z = 0.91, p about 0.36, not significant. The interaction (mobile lift minus desktop lift, +0.24 pts) has z = 0.83, p about 0.41. The data cannot show that desktop does little, so "leave desktop on the current page" is not supported either.
   - **Fix:** "Mobile lift was 15.5% and desktop 5.6%, but the device difference is not statistically significant (interaction p about 0.41). Treat the mobile result as a hypothesis. Confirm it in a pre-planned device test before shipping to mobile only, or keep a desktop holdout."
   - **If you skip it:** The company ships a mobile-only change on a split that may be noise, and the mobile-only economics above are still negative.

## Nice to have
None.

Checked and fine: Users (36,236 control, 36,265 widget), orders (1,177 and 1,308) and revenue ($104,159.21 and $114,847.94; readout shows $114,848) all recompute exactly from the daily CSV as sums over 32 rows. Conversion rates 3.25% and 3.61% and the +0.36 pt lift recompute. The z-test (z = 2.66, p about 0.008) and the 95% CI (+0.09 to +0.62 pts) recompute. Sample ratio 49.98% / 50.02% with chi-square about 0.01 (p about 0.91) holds. Device conversion rates and lifts (2.90 / 3.35 / 15.5%; 3.81 / 4.03 / 5.6%) recompute as ratios of summed parts. Daily totals sum to the overall totals. The statistical significance statement is correct as stated.

Not checked: (a) Whether "orders" counts purchases or distinct buyers: the readout defines conversion as users who ordered / users exposed; if one user can place two orders, the conversion figure is off. Owner to answer. (b) The platform contract terms: whether the $65,000 is fixed across devices, whether it can be cancelled, and any setup fee. (c) Store or analytics revenue reconciliation (no store export was provided). (d) The 30-day scale-up assumes the 4-day test is typical of a month; given the falling lift, this overstates the steady-state gain, so the business case is generous, not harsh.
````
