# review-clean-control

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/review/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/review-clean-control/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Here's our weekly paid search and email report (resources/weekly_report_wk41.md), plus the Google Ads, email, GA4 and Shopify exports it's based on. Can you check it before I send it to my boss? If there's anything wrong I'd rather know now. Write report.md with your verdict and anything I need to change.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `called-clean` | PASS | FAIL | A: "Verdict: Send it." with no findings; B: asks for three unsourced claims to be fixed before sending |
| `no-false-findings` | PASS | FAIL | A: lists the 5.9% gap, median vs mean and the hedged keyword line as fine; B: asks to drop the stated 5-10% range and source the hedged keyword line |
| `verified-numbers` | PASS | PASS | both confirm 26.23, 7.1% or 3.41% and more |

## Arm A answer (with skill)

````markdown
Verdict: Send it.

What this report says: Generic search cost per purchase fell to €26.23 from €30.87 the week before, on flat total spend (€4,472 vs €4,477), and is below the €35 target. It recommends keeping Google Ads budgets flat and the email schedule unchanged, and checking again on 2 November.
Who decides what: I assumed the obvious reader, your boss, decides whether to keep Google Ads budgets flat and the email schedule as they are.

No Must fix, Should fix or Nice to have findings. Every number I could recompute from the exports matches the report.

Checked and fine: Google Ads totals and rates recompute from the campaign export. Generic cost per purchase is €3,855.38 / 147 = €26.23 (prior week €3,920.49 / 127 = €30.87; same week 2025 €3,486.21 / 109 = €31.98), and the change is -15.0%. Brand CTR is 2,179 / 5,271 = 41.3%. Conversions are purchases only, and brand is split from generic. The Google ROAS figures are Google's own claims, and the report does not use them to set budget. Email: click rate 3.18% and 3.41%, click-to-open 9.9% and 10.7%, unsubscribe rate 0.23% in both weeks, and tagged revenue €3,965 and €4,208 all recompute from the send file. Shopify: 960 orders dated 5 to 11 October, mean €46.70 (sum €44,834.09), and median €40.30 (the 480th and 481st orders are €40.29 and €40.31). The two largest orders, €1,249 and €1,189, are the only ones above €140, and the report's note that they lift the mean is correct. GA4 google/cpc sessions are 7,061 against 7,504 Google Ads clicks, 5.9% fewer, which the report reads as a normal gap. GA4 newsletter sessions of 1,190 against 1,246 email clicks is expected and is not a finding. The report hedges the negative-keyword link as one week, not proof of cause, and its recommendations carry checks (generic cost per purchase under €35, click rate above 2%, unsubscribe rate under 0.4%).

Not checked: the €35 target and the 30 September negative-keyword date are not in the files. The GA4 file has no date range, so I assumed it covers the same week. Google revenue is not compared with Shopify revenue (€44,834), because the report makes no total ROAS claim.
````

## Arm B answer (without skill)

````markdown
# Review of weekly_report_wk41.md (Fernhill Garden Supply, 5 to 11 October 2026)

## Verdict

The figures I could recompute from the exports match the report. Before you send it, fix the three unsourced claims and the wording items below. The median and mean order values are not verified (see "Not checked").

## Checked and correct

**Google Ads (week_start 2026-10-05)**
- Brand: cost €616.52 (€617), clicks 2,179, CTR 41.3%, CPC €0.28, 270 purchases, cost per purchase €2.28, ROAS 26.08x.
- Generic (three campaigns summed): cost €3,855.38 (€3,855), clicks 5,325, CTR 5.3%, CPC €0.72, 147 purchases, cost per purchase €26.23, ROAS 2.14x.
- Total: cost €4,471.90 (€4,472), clicks 7,504, CTR 7.1%, CPC €0.60, 417 purchases, cost per purchase €10.72, ROAS 5.44x.
- Prior week generic cost per purchase €30.87 (€3,920.49 / 127). Prior week total spend €4,477. Change of -15.0%.
- Same week 2025 generic cost per purchase €31.98 (€3,486.21 / 109).

**GA4 comparison**
- google / cpc sessions 7,061 against 7,504 Ads clicks is 5.9% fewer, as the report says.

**Email (email_sends.csv has four sends; two fall in each week)**
- Prior week (29 Sep and 2 Oct): delivered 36,750; unique clicks 1,169; click rate 3.18%; click-to-open 9.9%; unsubscribe 0.23%; revenue €3,965.24.
- This week (6 and 9 Oct): delivered 36,550; unique clicks 1,246; click rate 3.41%; click-to-open 10.7%; unsubscribe 0.23%; revenue €4,207.81 (€4,208).
- GA4 newsletter sessions 1,190 against 1,246 clicks.

**Orders**
- shopify_orders_wk41.csv has 960 orders (FH-40211 to FH-41170).
- The two largest orders are €1,249.00 (FH-40228) and €1,189.00 (FH-40252), as stated.

## Needs a source or a change before it goes to your boss

1. **"Below our €35 target"** (Summary). No target appears in any export. Cite where the €35 comes from, or label it as an internal guideline.
2. **"Coincides with the negative keyword list added on 30 September"** (Google Ads section). The exports contain no change log. Either cite the date from your account history or remove the sentence.
3. **"A gap of 5-10% is typical"** (Google Ads section). This is a benchmark the data does not support. Either drop it or say it is your own rule of thumb. The 5.9% gap itself is correct.
4. **"Unsubscribe rates sit in the normal 0.1-0.4% band"** and the email "click rate above 2%" threshold are judgement calls, not data. Say where they come from, or present them as your targets.
5. **Email section (wording).** The table header says "2 sends" in both columns, which is right. Add the send dates (29 Sep, 2 Oct, 6 Oct, 9 Oct) so your boss can see which sends were counted.

## Not checked

- **Median order value €40.30 and mean €46.70.** I did not recompute these. Doing the median and mean across 960 rows by hand is not reliable enough to confirm the cents. Recompute them in a spreadsheet before sending.
- The outlier point holds in direction. Removing the two largest orders (€2,438 together) lowers the mean by about €2.54 ((€2,438 / 960) ≈ €2.54). The report's wording, "a few large orders", is fair, but there are also about fifteen orders above €100.

## Recommendation on the report

Keep the figures. Make the changes in items 1 to 5 and check the median and mean before sending.
````
