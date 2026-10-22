# research-concept-survey-audit

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/research-design/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/research-concept-survey-audit/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Before we send this to 5,000 customers, can you check our survey for the new EcoFill refill subscription? The draft is in resources/draft_survey.md. We'll use the yes share from Q6 to forecast subscribers. Write report.md with what to change.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `coverage` | PASS | PASS | both find 7 of 7 with fixes |
| `forecast-misuse` | PASS | PASS | both: yes share overstates; graded scale and calibration |
| `order-and-cover` | PASS | PASS | both flag the invitation and the Q1-before-Q2 order |

## Arm A answer (with skill)

````markdown
# EcoFill refill subscription survey: review of draft v3

## Verdict

Do not send to 5,000 customers yet. As drafted, the survey measures how many respondents say "Yes" to GBP 12 a month, not how many customers will subscribe. The Q6 yes share cannot support the year-one forecast without the fixes below.

## Deciding number

Forecast = Q6 "Yes" share x 180,000. Every 1 percentage point of yes share is 1,800 subscribers.

Three biases push the yes share up, and they do not cancel:

1. **Stated intent overstates purchase.** Raw yes/no answers fed into a volume forecast are inflated.
2. **Respondents are self-selected.** Interested customers are more likely to reply, and there is no non-response follow-up in the plan.
3. **The wording primes interest.** The invitation and Q5 both name the benefit (saves money, less plastic) before Q6 asks about buying.

Sampling error is also unplanned. The plan sets no target number of completes. Illustration only (no response count exists yet): for a worst-case margin of +/-3 points at 95% (p = 0.5), you need about 1,068 completes, which is a 21% response rate from 5,000 invitations. That margin is about +/-5,400 subscribers before any bias. At +/-2 points you need about 2,401 completes (48%). Sampling error shrinks with the square root of n, but bias does not shrink at all.

**Naive read:** "Yes share x 180,000 = year-one subscribers." It is wrong on bias, on error, and because the figure assumes everyone who says yes subscribes in year one with no churn or ramp.

## Findings and fixes

| # | Where | Problem | Fix | How to verify |
|---|---|---|---|---|
| 1 | Q6, analysis plan | Yes/No used as a purchase forecast. Stated intent overstates buying. | Ask a 0 to 10 purchase-probability scale and average it, or deflate using calibration from past launches. Ask the team for past launch intent vs actual. | Check the deflation factor against one past launch before using it. |
| 2 | Analysis plan | Forecast treats every "yes" as a year-one subscriber. No churn, no ramp, no launch reach. | Label the figure an upper bound until calibrated. Apply year-one retention and a ramp. | Compare with an in-market pilot or a limited-release offer. |
| 3 | Field plan | No non-response plan. The reason to reply (interest) relates to the answer. | Draw a random follow-up sample of non-respondents. If anonymous, re-contact about a third of the sample with "did you submit?". Report the uncorrected and corrected figures side by side. | Follow-up interest close to respondent interest means small bias. A large gap means the respondent figure is overstated. |
| 4 | Frame | 5,000 invited, described as "bought in last 12 months". The forecast base is 180,000 "active customers". 5,000 is 2.8% of 180,000. | Confirm whether 5,000 is a random sample of 180,000 (then weight and state the method) or the whole frame (then 180,000 is the wrong base). | Reconcile the CRM counts with the team. |
| 5 | Invitation | Names the benefit ("saves you money", "keeps plastic out of landfill") and names EcoFill in the subject and body. This primes interest. | Use a neutral cover note. Do not name the brand in the cover note if Q1 measures awareness. | Re-read against the questionnaire audit (B and C checks). |
| 6 | Q1 and Q2 order | Unaided (Q2, "which brands come to mind?") comes after the aided list in Q1. Unaided must come first. | Move Q2 before Q1. | The order in the final instrument. |
| 7 | Q1 awareness | No fictitious brand planted, so false recognition cannot be measured. "Select all" makes non-response undetectable. The brand is already named in the cover note. | Plant a fictitious brand. Ask yes/no per brand with a "don't know" option. State the awareness measure in the report. | Fictitious-brand "yes" rate is the false-recognition baseline. |
| 8 | Q3 | Categories overlap at 2 and at 4 ("0-2" / "2-4" / "4 or more"). A respondent can fit two answers. | Use mutually exclusive bands, e.g. 0-1, 2-3, 4-5, 6 or more. | Check that every answer maps to one band. |
| 9 | Q4 | Double-barrelled: "price and scent" in one answer. | Split into two questions. | Check each item has one dimension. |
| 10 | Q5 | Leading: "Given how much plastic waste refills save" names the gain before asking interest. The scale has only positive labels (Extremely / Very / Interested) and no lower end. The planned top-box "interest" cannot be interpreted without a negative end. | Remove the priming clause. Use a labelled 5 to 7 point scale with a negative end. Report the distribution, and the median for an ordinal scale. | Read the item cold, with no benefit stated, and check it has both ends. |
| 11 | Q6 | Single price, no status quo, no "don't know". The respondent has no baseline for GBP 12 (C4). | State what they pay now for comparable refills. Add a "would not buy refills" option or a "don't know". If the threshold is unknown, test more than one price. | Check the price cue against current prices. |
| 12 | Behaviour block | Purchase frequency for cleaning products is asked in Q3, but CRM purchase history already holds it. Usage data beats stated usage. | Join CRM purchase history to the survey on customer ID (aggregate each source to the customer before joining). Keep Q3 only if the CRM cannot supply it. | Compare CRM frequency with Q3 answers on a sample. |
| 13 | Incentive | GBP 100 draw may attract people who want the entry, not the product. | Keep the draw, but treat the yes share as coming from a mix of product interest and draw interest. Check whether yes answers differ by draw-entry status. | Compare yes share for entrants vs a random check. |

## Decision threshold and questions for you

Section 0 of the method: the forecast is not tied to a decision yet. Before fielding, please answer:

1. **What subscriber number makes the launch worth it (the break-even K)?** Without it, the survey cannot say whether the forecast clears the bar.
2. **Is the 180,000 the same frame as the 5,000 invited?** If not, which customers are in the 180,000?
3. **Do you have past launch data** (intent scores vs actual subscribers) to calibrate the deflation?
4. **What response rate and follow-up budget** will you commit to? A +/-3 point margin needs about 1,068 completes.
5. **Will the survey be the only evidence?** A small in-market test (limited-release offer) can check the intent-to-purchase conversion directly.

## What is not flagged

The one-week field period and the Q7 open text are fine as drafted.

## Score

Clarity 85, relevance 90, depth 85, insight 85. Revised once for the Q1/Q2 order and the cover-note brand question.
````

## Arm B answer (without skill)

````markdown
# EcoFill refill subscription survey: review of DRAFT v3

**Bottom line:** do not send this draft to 5,000 customers yet. The Q6 "Yes" share is the forecast input, and the draft would inflate it through question order, a binary yes/no with no "not sure" option, a leading premise in Q5, and a sample that answers only if it chooses to. Fix the items below first.

## Must fix before sending

1. **Q1 and Q2 are in the wrong order.** Q1 shows the brand list (EcoFill first) before Q2 asks which brands come to mind. Respondents will name brands they just saw, so Q2 no longer measures unaided awareness. Move Q2 above Q1 and keep Q1 as the aided question. Add a "None of these" option to Q1, since the list has no way to opt out.

2. **Q3 answer bands overlap.** "0-2" and "2-4" both include 2; "2-4" and "4 or more" both include 4. Use non-overlapping bands: 0-1, 2-3, 4 or more times a month.

3. **Q4 is double-barreled.** It asks about price and scent in one question. Split it into two questions: satisfaction with price, and satisfaction with scent.

4. **Q5 is leading and one-sided.** The premise "Given how much plastic waste refills save" tells people the answer. The scale has only positive options (Extremely / Very / Interested) and no neutral or negative option, so the "top-box" in the analysis plan cannot separate interest from indifference. Suggested wording: "How interested are you in buying refills through a subscription?" with a balanced five-point scale: Extremely interested / Very interested / Somewhat interested / Not very interested / Not at all interested.

5. **Q6 is a single binary question on one price, with no product description.** Stated intent from a yes/no question overstates purchase. Changes to make:
   - Describe what the subscription includes: delivery frequency, what the GBP 12 covers, how to cancel.
   - Use a five-point purchase-intent scale (Definitely would / Probably would / Might or might not / Probably would not / Definitely would not), and add "Not sure".
   - If the price is not yet fixed, test two or three prices across split samples. One price point cannot show a demand curve.
   - Do not use the raw Yes share as a forecast. Calibrate it against a known conversion from past EcoFill launches, if one exists.

6. **The forecast formula is not a forecast.** "Q6 Yes share x 180,000" has these gaps:
   - The denominator is unclear. It should be the Yes share among respondents who answered Q6, not among the 5,000 invited.
   - The sample frame ("bought in the last 12 months") does not match the base ("active customers"). Align them or state the difference.
   - There is no adjustment for self-selection, for the gap between stated and actual purchase, or for year-one churn.
   - The draft gives no response rate, which the forecast needs.
   - Report a range with scenarios, not one number.

   Sensitivity, using only the draft's own base of 180,000:
   - Each 1 point of Yes share = 1,800 subscribers, before any adjustment.
   - Sampling error only, assuming a random sample. At 1,000 completed responses, a 50% share has about ±3.1 points, which is ±5,580 subscribers (180,000 x 0.031).
   - At 250 completed responses, the same share has about ±6.2 points, which is ±11,160 subscribers (180,000 x 0.062).
   - Self-selected responders make the true error larger than these figures.

7. **The invitation frames the survey as a launch announcement, and claims need checking.** The text says "We're getting ready to launch a refill subscription that saves you money and keeps plastic out of landfill". Two risks:
   - Respondents may read it as a sales message and answer differently.
   - Research must not be used to sell (MRS Code of Conduct). The savings and landfill claims need substantiation (CMA Green Claims guidance).

   Suggested change: state that it is a research survey, and remove the savings and landfill claims unless they are substantiated. Ask compliance to confirm the consent basis for contacting these customers, and the terms of the GBP 100 draw.

## Check before launch

- Confirm the survey length (about 6 minutes) with a timed test run.
- Confirm whether the 5,000 is a census of the CRM list or a random draw.
- Confirm whether a conversion benchmark from past EcoFill launches exists.
- Confirm whether the GBP 12 price is fixed.
- Get the expected response rate, and set the target number of completes before fielding.

## Keep as is

- Q7 (open text, last question).
- The personalised greeting, if the CRM field is verified.
````
