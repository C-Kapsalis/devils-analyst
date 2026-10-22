# audit-email-crm

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/audit/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/audit-email-crm/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> I just took over email and CRM at Brightwater Candle Co from a freelancer. Everything I was handed is in resources/: the handover notes, our ESP exports for Q3, the domain check, our automated flows, list growth, GA4 email data and the CLV sheet from the board deck. Can you audit the whole program and tell me what to fix first before we add more sends in Q4? Put it in report.md.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `planted-recall` | PASS | PASS | both 7 of 7 |
| `must-fix-first` | FAIL | FAIL | A: all three in Must fix and "Fix 1 and 2 first", but the complaint spike (4th) sits after the CLV finding (3rd), a lesser problem; B: the complaint spike is not in its fix-first list |
| `decoys-left-alone` | PASS | PASS | A: unsubscribes, CTOR and the GA4 gap under Checked and fine; B: none flagged |

## Re-run of arm A after the skill fix

| Grader | A, first run | A, re-run | A, second re-run | Why |
|---|---|---|---|---|
| `planted-recall` | PASS | PASS | PASS | 7 of 7 in every run |
| `must-fix-first` | FAIL | FAIL | PASS | first re-run: the complaint spike moved up to 2nd, but the dormant send (4th) still sat after the CLV finding (3rd); second re-run: authentication, the dormant send and the complaint spike are Must fix 1 to 3, ahead of the win-back, tagging and CLV findings; "Fix 1 first" |
| `decoys-left-alone` | PASS | PASS | PASS | unsubscribes, CTOR and the GA4 gap under Checked and fine in every run |

## Arm A answer (with skill)

````markdown
# Email and CRM audit: Brightwater Candle Co

Scope: Q3 2026 sends (Jul to Sep), list history (Apr to Sep 2026), domain check, automated flows, GA4 email data and the CLV sheet. The export does not state a currency, so money figures are in the export's own units.

## Map
- **Sources:** ESP monthly summary and per-send export (9 sends, Jul to Sep 2026), domain authentication (SPF, DKIM, DMARC), 4 automated flows (sends in last 30 days), monthly list growth (Apr to Sep 2026), GA4 email sessions and revenue (9 campaigns), CLV sheet, handover notes.
- **Period:** sends Jul to Sep 2026; list Apr to Sep 2026.
- **Spend by channel:** none in the export. The CAC of 82 cites paid spend that is not given.
- **Goal:** repeat purchases (handover notes).
- **Inputs used:** AOV 42, 2.6 orders per customer per year, tenure 3 years (an estimate in the sheet), gross margin 38%, discount rate 10%. Assumed: the sheet's inputs are right and email revenue is GA4 purchase_revenue.
- **Revenue truth:** none. No store or finance total is in the export, so GA4 is the only revenue figure.
- **Missing:** paid spend and new-customer count behind the CAC; store revenue; GA4 key event, retention and attribution settings; revenue by automated flow; suppression list.

## Must fix
1. **DKIM fails and DMARC is missing** (brightwatercandle.com, every send)
   - **What it is:** SPF passes. DKIM for s1._domainkey fails because the published key does not match the ESP's signing key. No DMARC record exists.
   - **Problem:** Bulk senders need SPF and DKIM passing and a DMARC record (Google and Yahoo requirement since February 2024). Q3 delivered 311,554 of 314,430 sent (99.1%), so mail still arrives, but this is the failure that gets mail filtered later.
   - **Fix:** Publish the ESP's DKIM key at s1._domainkey (or rotate the ESP key to the published one). Confirm DKIM passes in the ESP. Add a DMARC record starting at p=none with a reporting address, and move to quarantine once reports are clean.
   - **If you skip it:** Q3 GA4 email revenue of 20,929.80 averages about 6,977 per month, and the whole list's inbox placement is exposed.

2. **Dormant contacts are mailed with no exit** (Win-back flow; September all-subscribers newsletter)
   - **What it is:** The Win-back flow sent 18,640 emails in the last 30 days, 81% of the 23,070 automated sends, with exit rule "none". That equals 43% of the 43,330 list if each contact gets one. The September newsletter went to all 43,420 subscribers, against about 33,700 for each engaged send.
   - **Problem:** The September newsletter bounced 1,463 of 43,420 (3.37%). Each engaged send bounced 0.45% to 0.58%. The roughly 9,400 extra addresses produced about 1,290 bounces, roughly 14% (estimate, assuming the engaged bounce rate of 0.52% applies to the first 34,000). Net list growth turned negative: August -0.39% (790 new, 700 unsubscribed, 260 cleaned) and September -0.60% (760, 740, 280). The list fell 430 over August and September. Gross adds are down 22% since April (980 to 760) and unsubscribes are up 42% (520 to 740).
   - **Counterpoint:** The September newsletter was the best Q3 send on outcomes: 59 transactions against an engaged-send average of 46, and 2,961.62 revenue against 2,246 average. The case against it is list damage, not revenue. Test a repeat against a holdout before deciding.
   - **Fix:** Give the Win-back flow an exit rule (rejoin on open or click; delete after two silent sends). Suppress addresses after a hard bounce. Keep the main newsletter to engaged_12m. Run one re-engagement send to the dormant group, then delete the silent ones.
   - **If you skip it:** 18,640 sends a month keep going to contacts who do not respond, and the list keeps shrinking. The flow's revenue is not in the export, so its money cannot be sized. The risk is the deliverability of the whole list (see 1).

3. **CLV and CAC ratio behind the Q4 budget are overstated** (CLV sheet, board deck)
   - **What it is:** CLV 327.60 = AOV 42 x 2.6 orders x 3 years. Divided by blended CAC 82 gives 4.0, the figure the sheet uses to justify +20% acquisition budget.
   - **Problem:** The CLV is revenue, not margin, and it is not discounted. Arithmetic is correct, but the inputs are the wrong measure. At 38% margin, 42 x 2.6 x 0.38 = 41.50 per year, so 124.49 over 3 years (ratio 1.52:1). Discounted at 10% per year, 103.19 (ratio 1.26:1). Tenure is an estimate: at 2 years the discounted ratio is 0.88:1, at 4 years 1.60:1. The sheet has no buffer on the CAC ceiling.
   - **Fix:** Rebuild CLV as discounted margin per customer (AOV x orders x margin, discounted at 10%) over a tenure range, not one point. Recompute CLV:CAC on that figure and keep a buffer. Hold the +20% acquisition budget until the ratio is re-run and clears your threshold.
   - **If you skip it:** The Q4 budget is set on a ratio about three times the measure it should use (4.0 against 1.26). The budget itself is not in the export. It is 20% of current paid acquisition spend, which you need to supply to total it.

4. **Flash Sale 48h complaint spike** (aug_flash_sale)
   - **What it is:** 53 spam complaints on 33,793 delivered, or 0.157%. The other engaged sends ran 0.027% to 0.036%.
   - **Problem:** 0.157% is above the 0.1% line and below the 0.3% critical line. The August monthly average (0.072%) hides it. This send also had the lowest revenue per delivered recipient in Q3 (0.058 against 0.067 for the engaged average).
   - **Fix:** Review the urgency format for the engaged list. Suppress recipients who complained. Judge each promotional send on complaints per delivered and revenue per delivered, not the monthly average. Check the rate on each promo before sending the next one.
   - **If you skip it:** The Q4 plan adds two promotional sends a month. At this rate, each one puts the complaint line at risk.

5. **Autumn Collection drops out of the revenue join** (sep_autumn_collection vs sep-autumn-collection)
   - **What it is:** The GA4 campaign name uses hyphens and the ESP uses underscores. Eight of nine campaigns match exactly.
   - **Problem:** An exact-name join drops 1,256 sessions, 51 transactions and 2,644.33 revenue. That is 12.6% of Q3 GA4 email revenue (20,929.80) and 34% of September's (7,784.92).
   - **Fix:** Rename the link to sep_autumn_collection, or normalise names before joining (lowercase, hyphens to underscores). Use one link builder for all campaign tags.
   - **If you skip it:** 12.6% of email revenue goes uncredited in any report that joins on name, so budget decisions read it as zero.

## Should fix
6. **Net list growth is shrinking** (list_growth_monthly)
   - **What it is:** Net growth ((new - unsubscribed - cleaned) / list at start) was +0.63% in April, then +0.11% in July, -0.39% in August and -0.60% in September.
   - **Problem:** Campaign rates measure survivors. Rates can look steady while the audience shrinks.
   - **Fix:** Add this line to the monthly report and review it before each send plan.

## Nice to have
None found in the export.

## Checked and fine
Q3 delivered/sent 99.1% (above 95%); SPF passes; the monthly ESP summary ties to the per-send export for sent, delivered and complaints in all three months; unsubscribes per send 0.17% to 0.31% (under 0.5%); click-to-open 9.8% to 12.0% (inside the 8% to 15% band); complaints under 0.1% on 8 of 9 sends, and the September newsletter at 0.079%; GA4 sessions run 92.6% to 95.9% of ESP clicks, which is normal; the welcome, abandoned-cart and post-purchase flows have sensible exit rules.

## Not checked
- Store or finance revenue: none in the export, so GA4 is not reconciled to sales.
- Paid spend and new-customer count behind CAC 82.
- GA4 data retention, key events and attribution model (GA1 to GA3).
- Revenue by automated flow.
- Suppression list and the hard versus soft bounce split.
- House-rules folder: not searched, because no search tool was available in this session.

Fix 1 and 2 first: email authentication protects delivery on every send, and the dormant contacts drive the bounces and list shrinkage that every later rate sits on. Hold the +20% budget and the two extra promo sends until finding 3 is re-run and finding 4 is fixed.
````

## Arm B answer (without skill)

````markdown
# Brightwater Candle Co: email and CRM audit, Q3 2026

## Fix first, in this order

1. **Email authentication.** DKIM fails (the published s1 key does not match the ESP's signing key) and there is no DMARC record. SPF passes. Fix DKIM so the ESP signs with a key that is published, publish a DMARC record at `p=none` with reporting, and tighten the policy once reports are clean. Do this before any Q4 send is added.
2. **Stop whole-list sends.** The September newsletter went to all 43,420 subscribers. It bounced at 3.37% (1,463 of 43,420), against about 0.52% for the engaged sends. Build a re-engagement step and a sunset rule for people with no engagement in 12 months.
3. **Win-back flow has no exit.** It sent 18,640 emails in the last 30 days, 81% of all automated sends (18,640 of 23,070). Its exit rule is "none". Add exits for purchase, unsubscribe, bounce and a send cap.
4. **Hold the two extra Q4 promotional sends.** The list shrank in August and September, and unsubscribes and cleans are rising. If you must test, add one extra send a month to the engaged segment only, with stop rules set in advance.
5. **Re-run the CLV:CAC case before the +20% acquisition budget.** The 4:1 figure uses revenue, not margin (details below).
6. **Fix tracking and attribution.** Clean up UTM names and account for list-level unsubscribes.

## Findings

### 1. Deliverability and authentication
- Domain check: SPF pass (`~all`), DKIM **fail**, DMARC **missing**. Google and Yahoo require DMARC for bulk senders, so the missing record is a compliance gap as well as a risk. This check only reads DNS; it does not measure inbox placement.
- Monthly ESP summary (campaign sends only):

| Month | Bounce % (of sent) | Complaint % (of delivered) | Unsub % (of delivered) |
|---|---|---|---|
| Jul | 0.48 | 0.031 | 0.20 |
| Aug | 0.53 | 0.072 | 0.28 |
| Sep | **1.66** | 0.048 | 0.22 |

- September bounces: 1,850 of 111,360 sent. The newsletter alone accounts for 1,463 of them.

### 2. Campaign-level results (rates on delivered, computed by hand)

| Campaign | Segment | Bounce % | Open % | Click % | Complaint % | Unsub % |
|---|---|---|---|---|---|---|
| Jul Newsletter | engaged_12m | 0.45 | 34.5 | 3.5 | 0.030 | 0.18 |
| Jul Summer Sale | engaged_12m | 0.48 | 33.3 | 4.0 | 0.036 | 0.20 |
| Jul New Scents | engaged_12m | 0.52 | 34.0 | 3.8 | 0.027 | 0.23 |
| Aug Newsletter | engaged_12m | 0.50 | 36.8 | 3.6 | 0.030 | 0.31 |
| Aug Flash Sale 48h | engaged_12m | 0.55 | 31.2 | 3.6 | **0.157** | 0.28 |
| Aug Back to Home | engaged_12m | 0.53 | 35.4 | 3.5 | 0.030 | 0.26 |
| Sep Newsletter | **all_subscribers** | **3.37** | **26.4** | 3.2 | 0.079 | 0.22 |
| Sep Autumn Collection | engaged_12m | 0.58 | 34.0 | 3.9 | 0.033 | 0.17 |
| Sep Candle Care | engaged_12m | 0.56 | 31.8 | 3.4 | 0.027 | 0.26 |

- The eight engaged sends average 33.9% open and 3.65% click on delivered.
- **Flash Sale complaints:** 53 on 33,793 delivered (0.157%), about five times the other sends. Review the 48-hour urgency format and its frequency before repeating it.
- **September newsletter reach:** the engaged segment averaged 33,876 sends, so roughly 9,500 recipients (about 22% of the 43,420 sent) were outside it. This is an estimate from the average engaged send size. If about 170 of the 1,463 bounces are typical for the engaged group, the remaining ~1,290 bounces are roughly 13% of those ~9,500. The estimate is rough, but the order of magnitude holds.
- Opens are unique opens, which Apple Mail Privacy Protection inflates. Judge decisions on clicks and revenue.

### 3. Revenue (GA4, last-click by session campaign)
- Total across the nine sends: 10,522 sessions, 427 transactions (4.06%), 20,929.80 revenue.
- September newsletter: 4.66% session-to-transaction, 2,961.62 revenue. That is the best conversion of the nine.
- Per 1,000 sent, the September newsletter earned about 68, against about 66 for the eight engaged sends. The extra reach did not add revenue per send in this data. The cost is list health, not lost revenue.
- **UTM mismatch:** the ESP tags the autumn send `sep_autumn_collection`; GA4 records `sep-autumn-collection`. Any join on the campaign name drops it. Standardise the naming before Q4.

### 4. List health (list_growth_monthly)
- Net change Apr to Sep: +130 (43,200 to 43,330).
- New subscribers fell from 980 (Apr) to 760 (Sep), down 22%.
- Unsubscribes rose from 520 to 740, up 42%. Cleaned rose from 190 to 280, up 47%.
- Net by month: Apr +270, May +170, Jun +70, Jul +50, Aug **-170**, Sep **-260**. Q3 net: -380.

### 5. Automated flows
- Welcome series: 2,140 sends in 30 days, exits after email 3 or first purchase. Consistent with about 760 new subscribers a month.
- Abandoned cart: 1,310 sends, exits on purchase or after email 2.
- Post-purchase review: 980 sends, exits after email 1.
- Win-back: 18,640 sends, entry "no purchase in 180 days", exit "none". This is the volume and risk driver (see priority 3).

### 6. CLV and CAC (clv_sheet)
- The sheet's CLV is 42 x 2.6 x 3 = 327.6. That is revenue, not margin.
- Margin adjustment: at 38% gross margin, CLV is 327.6 x 0.38 = **124.5** undiscounted. Divided by CAC of 82, that is **1.5:1**, not 4:1.
- With the 10% discount rate also applied (annual margin of 41.5, discounted over three years), CLV is about **103** and the ratio about **1.26:1**.
- The three-year tenure is labelled an estimate. The CAC is paid spend over new customers, so it does not reflect email. The +20% acquisition budget should not rest on the 4:1 figure as it stands.
- The 3:1 benchmark is a common rule of thumb, not a law. On a margin basis this business is below it.

### 7. Unexplained unsubscribes
- Campaign-level unsubscribes: 205 (Jul), 284 (Aug), 236 (Sep).
- List-level unsubscribes: 640 (Jul), 700 (Aug), 740 (Sep).
- Roughly 430 to 500 unsubscribes a month come from somewhere outside the three-campaign export, most likely flows or other sends. Pull flow-level unsubscribe data before changing send volume.

## Q4 recommendation
- Do not add two sends a month yet. That is a 67% increase (3 to 5 a month) on a list that shrank by 380 in Q3, with unsubscribes and cleans rising.
- Fix priorities 1 to 3 first. Then pilot one extra send a month to the engaged segment, with stop rules: complaints above 0.1% or bounces above 1% pause the programme.
- Re-state the CLV:CAC case on margin before any budget decision.

## Gaps in the data
- No ad spend, so CAC cannot be checked.
- No inbox-placement or Postmaster data.
- No flow-level sends for unsubscribes, bounces or complaints.
- GA4 attribution is last-click by session campaign. Revenue totals are indicative.
- The handover notes do not say which system is the source of truth for list size.

## Method
All arithmetic was done by hand from the CSVs in resources/. Rates use delivered as the denominator unless the column says otherwise. Totals reconcile: the monthly ESP sums match the campaign rows, and the list file reconciles start, new, unsubscribed, cleaned and end size for every month.
````

## Arm A re-run answer (after the skill fix)

````markdown
# Brightwater Candle Co: email and CRM audit, Q3 2026

Fix 1 first: DKIM fails and DMARC is missing on roughly 100,000 sends a month, so every later delivery and revenue number, and the Q4 sends, depend on authenticated mail. Hold the two extra promotional sends and the +20% acquisition budget until items 1 to 3 are done. The budget case rests on a CLV:CAC of 4.0:1, which falls to 1.3:1 once the CLV sheet's own margin and discount inputs are applied.

## Map
- Sources: ESP monthly summary and per-send log (9 sends, Jul to Sep 2026), domain authentication (SPF, DKIM, DMARC), 4 automated flows (last 30 days), list growth (Apr to Sep 2026), GA4 email campaigns (Jul to Sep), CLV sheet, handover notes.
- Period: sends 1 Jul to 30 Sep 2026; list Apr to Sep 2026.
- Spend by channel: not in the files. No email send cost. Blended CAC is 82 (paid spend / new customers, last 12 months).
- Goal: repeat purchases (handover notes). Assumed: purchase is the goal.
- Margin, AOV, targets: gross margin 38% and discount rate 10% (finance, CLV sheet); store AOV 42. No target given.
- Revenue truth: none. GA4 credits 20,929.80 of purchase revenue to email in Q3. No store total to reconcile it to.
- Missing: store revenue, email send cost, discount cost behind the sales, GA4 key events and retention setting.

## Must fix

1. **DKIM fails and DMARC is missing** (domain authentication, all sends)
   - **What it is:** SPF passes. DKIM for s1._domainkey fails because the published key does not match the signing key in the ESP. There is no DMARC record.
   - **Problem:** Monthly volume is 101,890 to 111,360 sent. Bulk senders at Google and Yahoo need authenticated mail and a DMARC policy. With no DMARC there is no policy and no reporting, and one of the two signatures is broken.
   - **Fix:** Publish the DKIM public key that matches the ESP's current signing key at s1._domainkey and confirm a pass in the ESP. Publish _dmarc with p=none and a reporting address. Read reports for two to four weeks, then tighten the policy.
   - **If you skip it:** GA4 credits 20,929.80 of Q3 purchase revenue to email, about 6,980 a month, and all of it depends on delivery. The Q4 volume goes through the same authentication.
   - **Verify:** A test send shows DKIM and DMARC pass in the headers. DMARC aggregate reports arrive.

2. **Flash sale complaints above 0.1% on one send** (aug_flash_sale, engaged_12m)
   - **What it is:** 53 complaints on 33,793 delivered, which is 0.157%. The other engaged sends have 9 to 12 complaints, or 0.027% to 0.036%.
   - **Problem:** The rule is any send above 0.1%, even when the monthly average is below it. August's average of 0.072% hides this send. The send also has the lowest revenue per 1,000 delivered in the set: 57.64, against 67.18 for the quarter.
   - **Fix:** Stop repeating 48-hour flash sends to engaged_12m until the offer and frequency are reviewed. Cap frequency for that segment. Check that the complaint path is not the only exit for unhappy readers.
   - **If you skip it:** A send above 0.1% is the rate that can take the program off the air. The discount cost is not in the data, so the sale itself is not sized.
   - **Verify:** Complaints per delivered on the next flash-type send are under 0.1%.

3. **CLV is built on revenue, not margin, and undiscounted** (CLV sheet, board deck)
   - **What it is:** CLV = 42 x 2.6 x 3 = 327.6. CLV:CAC = 327.6 / 82 = 4.0, shown as 4. The sheet lists gross margin 38% and discount rate 10%, but the formula uses neither.
   - **Problem:** Margin per order is 42 x 0.38 = 15.96, or 41.50 a year. Discounted at 10% over the 3-year tenure, that is 103.19, a ratio of 1.26:1 on CAC 82. Undiscounted margin gives 124.49, or 1.52:1. The 3-year tenure is an unsourced estimate. At 2 years the margin ratio is 0.88:1, and at 4 years it is 1.60:1. All three are below the 3:1 the board deck implies.
   - **Fix:** Use margin per order x orders per year x survival, discounted at 10%, summed. Compare the gross margin NPV with CAC. Report CLV as a range over tenure. Recompute CLV:CAC by channel before any budget change.
   - **If you skip it:** The +20% acquisition budget rests on the 4.0:1 ratio. On the corrected basis each new customer leaves about 21 after CAC (103.19 minus 82), not about 246 (327.6 minus 82).
   - **Verify:** A recomputed table using the sheet's own margin and discount inputs, with a tenure range, signed off by finance.

4. **Dormant contacts in the September newsletter** (sep_newsletter, all_subscribers)
   - **What it is:** Sent to all_subscribers (43,420 sent), not engaged_12m (about 33,950 in the other September sends). That leaves roughly 9,500 contacts, about 22% of the send, who were not in the engaged segment. The handover note says this was done "to wake people up".
   - **Problem:** Bounce was 3.37% (1,463 of 43,420), against 0.52% across the engaged sends. That is about 1,240 bounces more than the engaged rate predicts; if they sit in the dormant slice, that is about 13% bounce there. Complaints were 33 (0.079%), against about 0.03%, so about 20 more than expected. Opens were 11,074, the same as the engaged sends (10,544 to 12,419), so opens per delivered fell to 26.4% from 31% to 37%. Monthly bounce rose 0.48%, 0.53%, 1.66% while volume rose 9%. The open drop is the dormant mix, not a privacy effect. The send still earned the most revenue of the nine (2,961.62), so the cost is placement, not sales.
   - **Fix:** Send to engaged_12m only. Move dormant contacts to a separate win-back send with an exit rule (item 5). Delete after one or two silent campaigns.
   - **If you skip it:** Repeating the wide send in Q4 adds bounces and complaints to the whole list's placement, which item 1 already puts at risk.
   - **Verify:** The next wide-audience sends bounce under 0.6% and complain under 0.05%.

5. **Win-back flow has no exit rule** (automated_flows: Win-back)
   - **What it is:** Entry is no purchase in 180 days. Exit is "none". It sent 18,640 emails in the last 30 days, 8.7 times the Welcome series (2,140).
   - **Problem:** Lapsed contacts are mailed with no end point. The file counts sends, not unique contacts, so the size of the group is not known.
   - **Fix:** Exit when a contact opens or clicks (rejoin the main list). Delete after one or two silent sends.
   - **If you skip it:** Spam-trap and complaint risk on a flow that is the largest sender. Its revenue is not in the data, so it is not sized.
   - **Verify:** Unique recipients and the share who stay silent after two sends.

6. **The list is shrinking** (list_growth_monthly)
   - **What it is:** Net change (new minus unsubscribed minus cleaned) went from +270 in April (+0.63%) to +50 in July, then -170 in August and -260 in September (-0.60%). Q3 net is -380. New subscribers fell from 980 to 760 (-22%). Unsubscribes rose from 520 to 740 (+42%). Cleaned rose from 190 to 280 (+47%).
   - **Problem:** The campaign rates look steady because they are measured on survivors. The base is leaking, and the September blast added to the leak.
   - **Fix:** Track the net change monthly. Stop the leak (item 4, and the list's unsubscribes) before raising acquisition spend.
   - **If you skip it:** The Q4 acquisition budget fills a base that lost 380 net in Q3.
   - **Verify:** Net change is zero or positive for two consecutive months.

## Should fix

7. **One campaign with two names** (sep_autumn_collection in the ESP, sep-autumn-collection in GA4)
   - **What it is:** Eight of the nine campaigns match exactly. The autumn send is spelled with hyphens in GA4.
   - **Problem:** 2,644.33 of Q3 email revenue (12.6% of the 20,929.80 total) sits under a name that does not join to the ESP on an exact match.
   - **Fix:** One house style for utm_campaign, enforced by a link builder. Rename the GA4 row or the ESP name to match.
   - **If you skip it:** Reports that join ESP to GA4 on the campaign name leave 12.6% of email revenue unattributed.
   - **Verify:** An exact join on utm_campaign matches 9 of 9.

## Nice to have

8. **Source field holds a channel type** (utm_source = newsletter; utm_medium = email is correct)
   - Default channel grouping still classifies these as Email, so no money is at stake. Set source to the platform name at the next tagging change.

## Checked and fine
- Delivered per send 98.3% to 99.5% by month, above 95%. Monthly bounce under 2%.
- Click rate per send 3.2% to 4.0%, inside the 2% to 5% band. Click-to-open 9.8% to 12.0%. Unsubscribes per delivered 0.17% to 0.31%.
- Complaints under 0.1% on every send except the flash sale (item 2).
- GA4 sessions run 92% to 96% of ESP clicks on every row (normal).
- ESP monthly totals reconcile to the per-send log. List arithmetic reconciles every month.
- Welcome, abandoned cart and post-purchase flows have exit rules.

## Not checked
- Store or backend revenue (no file), so GA4 email revenue is not reconciled to orders.
- GA4 key events, attribution model, data retention and cart abandonment (no data).
- Email send cost and the cost of discounts (no data).
- The list file's unsubscribes (640 to 740 a month) do not match the campaign file's unsubscribes (205 to 284 a month). The gap may be flow or preference-centre unsubscribes. Confirm which feed the list number before relying on item 6.
- The 3-year tenure (an estimate with no source) and the definition of an "active customer" (C8).

Fix 1 first: DKIM fails and DMARC is missing on roughly 100,000 sends a month, so every later delivery and revenue number, and the Q4 plan, depend on authenticated mail.
````

## Arm A second re-run answer (after the second skill fix)

````markdown
# Email and CRM audit: Brightwater Candle Co (Q3 2026)

Short answer: fix the sending domain first (DKIM fails and DMARC is missing). Then stop mailing the dormant list in main sends, stop the open-ended win-back flow, and fix one campaign name that hides its revenue. Do not add the two Q4 promotional sends, or the 20% acquisition increase, until those are verified. The 4:1 CLV behind the increase is about 1.5:1 once margin is counted.

## Map
- Sources: ESP send-level export (9 sends, 3 Jul to 26 Sep 2026), ESP monthly summary (Jul to Sep), domain authentication check, automated flows (last 30 days), list growth (Apr to Sep 2026), GA4 email campaign rows (9, Q3), CLV sheet.
- Spend by channel: none in the export. The only spend-derived figure is blended CAC of 82 (CLV sheet, "paid spend / new customers"); the paid spend itself is not in the files.
- Goal: repeat purchases (handover notes). No targets were given, so none are used.
- Margin and AOV: gross margin 38% (finance), AOV 42 and 2.6 orders per customer per year (store, last 12 months), discount rate 10% (finance). Assumed: these are current.
- Revenue truth: none. GA4 purchase revenue for the nine sends totals 20,929.80 on 427 transactions; no store or order total was provided to reconcile it.
- Missing: paid spend, store orders, flow performance, GA4 settings, unsubscribe link and postal address.

## Must fix
1. **Sending domain authentication** (domain_authentication.csv)
   - **What it is:** SPF passes. DKIM fails: the key published at s1._domainkey.brightwatercandle.com does not match the ESP's signing key. DMARC is missing (no _dmarc record).
   - **Problem:** DKIM cannot pass while the published key differs from the signing key. With no DMARC record, receivers have no policy for the domain. The reference treats SPF, DKIM and DMARC as all required for bulk senders.
   - **Fix:** Copy the DKIM public key from the ESP and publish it at s1._domainkey, replacing the stale record. Publish a DMARC TXT record at _dmarc.brightwatercandle.com starting with "v=DMARC1; p=none; rua=mailto:[reporting address]", then move to quarantine once the reports are clean.
   - **Verify:** the domain check shows DKIM pass and DMARC present, and a test send's headers show dkim=pass and dmarc=pass.
   - **If you skip it:** up to about 6,977 a month of blast revenue is exposed (Q3 GA4 average, 20,929.80 over three months). Flow revenue is not in the export, and the Q4 volume lands on top of this.

2. **The all-subscriber September newsletter** (esp_sends_q3_2026.csv, 2 Sep)
   - **What it is:** sent to all_subscribers (43,420 sent). Bounces: 1,463 (3.37%), against 0.45% to 0.58% on the other eight sends, about six times the norm. Complaints: 33 (0.079% of delivered), about three times the 0.027% to 0.036% typical. The monthly bounce rate went from 0.48% (Jul) and 0.53% (Aug) to 1.66% (Sep).
   - **Problem:** the other sends went to engaged_12m, which was 33,600 to 34,000 recipients each. The September send therefore reached about 9,400 to 9,800 contacts (about 22%) with no open or click in 12 months. A send whose bounces run several times the others' has already damaged delivery, so it ranks as tier 1 under the audit rules.
   - **Fix:** keep dormant contacts out of main sends. Move them to a separate win-back send with an exit rule, and suppress addresses on the first hard bounce (the export does not split hard from soft).
   - **Verify:** the next main newsletter bounces under about 0.6% and complaints under 0.1%.
   - **If you skip it:** every later send in the list is exposed to the same bounce and complaint trend. Money at risk: the program's blast revenue, about 6,977 a month.

3. **Flash Sale 48h complaints** (esp_sends_q3_2026.csv, 21 Aug)
   - **What it is:** 53 complaints on 33,793 delivered, 0.157%. The other eight sends run 0.027% to 0.079%, and seven of them 0.027% to 0.036%.
   - **Problem:** this is above the 0.1% line in the email checks and about five times the typical count. The August monthly complaint rate (0.072%) looks fine only because the average hides this send. The flash send also had the lowest GA4 revenue of the nine sends (1,947.86 on 43 orders).
   - **Fix:** do not repeat the 48-hour format to the same segment. Review the list and the consent source for that send, and cut the frequency for the segment that complained.
   - **Verify:** the next promotional send to the same segment stays under 0.1% complaints.
   - **If you skip it:** the two Q4 promotional sends a month are this format. Money at risk: the program's blast revenue, about 6,977 a month.

4. **Win-back flow with no exit** (automated_flows.csv)
   - **What it is:** entry is no purchase in 180 days, exit is "none". It sent 18,640 messages in the last 30 days, about 43% of the list's end-of-September size (43,330).
   - **Problem:** lapsed contacts are mailed indefinitely. The reference's leak rule applies: this is the spam-trap and complaint pattern, and it feeds the bounce and complaint rates above. Flow-level rates are not in the export, so the cost cannot be sized in money.
   - **Fix:** exit the flow on any open or click, and delete contacts after one or two silent sends.
   - **Verify:** win-back sends per contact fall, and the flow's complaint and bounce rates are reported separately.
   - **If you skip it:** the list's reputation, which every send depends on. Money: not sized (flow revenue not in the export).

5. **Autumn Collection revenue is invisible under the ESP's name** (esp_sends_q3_2026.csv and ga4_email_campaigns_q3_2026.csv)
   - **What it is:** the ESP campaign is sep_autumn_collection. GA4 records the same campaign as sep-autumn-collection (hyphens). The exact-name match returns no revenue for the send.
   - **Problem:** 2,644.33 of GA4 revenue (51 orders, 12.6% of the quarter's 20,929.80) sits under a near-identical name. Any ranking by campaign that joins on the name will show this send at zero.
   - **Fix:** use one spelling everywhere (underscores), in the link builder, the ESP and GA4.
   - **Verify:** an exact-name join of the nine ESP sends to GA4 returns revenue on all nine.
   - **If you skip it:** every per-campaign ranking in the program is wrong for this send, and the budget that follows it.

6. **CLV is revenue, not margin, and the Q4 budget rests on it** (clv_sheet.csv)
   - **What it is:** CLV = AOV 42 x 2.6 orders x 3 years = 327.6 (checked, the arithmetic holds). The sheet uses revenue, no margin, no churn and no discounting. The 4:1 ratio is 327.6 / 82 = 3.99.
   - **Problem:** the finance sheet's own gross margin (38%) and discount rate (10%) are not applied. At margin, one customer-year is 42 x 2.6 x 0.38 = 41.50, and three years undiscounted is 124.49, so CLV:CAC is 124.49 / 82 = 1.52:1. Discounted at 10% over three years it is 103.20, so 1.26:1. Both are upper bounds, because the three-year tenure assumes no customer leaves (the sheet itself calls tenure an estimate). The +20% acquisition budget is justified by the 4:1 figure.
   - **Fix:** rebuild CLV as margin per year x survival x discount, from store cohorts, and compare it with CAC less a safety buffer. Hold the 20% increase until it is recomputed.
   - **Verify:** the rebuilt CLV:CAC, with stated survival and discount inputs, is reviewed before the budget decision.
   - **If you skip it:** the 20% uplift is scaled on a number about 2.6 times the margin-based one. Money: the uplift applies to paid spend, which is not in the export, so it cannot be sized here.

## Should fix
7. **Net list growth is negative** (list_growth_monthly.csv)
   - **What it is:** net growth (new minus unsubscribed minus cleaned) was +50 in July, -170 in August and -260 in September (-0.60% of start-of-month size). From April to September, new subscribers fell 22% (980 to 760), unsubscribes rose 42% (520 to 740) and cleaned addresses rose 47% (190 to 280). The list reconciles: start + new - unsub - cleaned = end, for all six months.
   - **Problem:** campaign rates measure survivors, so steady rates hide a shrinking audience. The export does not say where the unsubscribes came from. The three sends account for 236 of September's 740 unsubscribes (about 504 unexplained), and the same gap is 435 in July and 416 in August. Flows and other sources are the likely places, but this is not proven.
   - **Fix:** track net growth monthly. Find out where unsubscribes are coming from (flow footers, preference centre, manual), and what changed in sign-up volume.
   - **Verify:** net growth at zero or above for two consecutive months, with the unsubscribe source split reported.
   - **If you skip it:** the base every send relies on keeps shrinking. Money: not sized in the export.

8. **Test the September revenue before repeating it** (tier 5, causal claim)
   - **What it is:** the all-subscriber September send had the highest GA4 revenue of the quarter (2,961.62 on 59 orders). Its session conversion was 4.66%, against 3.98% for the other eight sends (368 orders on 9,257 sessions).
   - **Problem:** the gap is within chance (two-proportion z about 1.15, against 1.96 for significance). It is one send with no holdout, and the revenue may come from buyers who are already engaged. It is not evidence that wide sends pay.
   - **Fix:** test this, do not repeat it as a proven win. Run a dormant-only win-back against a 10% holdout.
   - **Verify:** the holdout comparison shows whether the send adds orders beyond the holdout.

## Nice to have
9. **GA4 source field** (ga4_email_campaigns_q3_2026.csv): all nine rows use source "newsletter", a channel type rather than the platform name. The medium is "email", so channel grouping works. Change the source to the ESP's name when the links are next rebuilt (this is the same fix as finding 5).

Checked and fine:
- Delivered as a share of sent: 96.6% to 99.6% on every send, above the 95% line.
- Unsubscribes per send: 0.17% to 0.31%, inside the 0.1% to 0.4% band.
- Click-to-open (CTOR): 9.8% to 12.0%, inside the 8% to 15% band.
- GA4 sessions are 92.6% to 95.9% of ESP unique clicks on every send: normal, not a tracking fault.
- The monthly summary reconciles to the send rows for July, August and September (sum over sum, checked).
- SPF passes. The welcome, abandoned-cart and post-purchase flows have exit rules.

Not checked:
- Store or order revenue (no file), so GA4 revenue is not reconciled to orders.
- Paid spend, so the CAC of 82 cannot be verified and the 20% uplift cannot be sized in money.
- GA4 settings (data retention, key events, attribution model), which are not in the export.
- Flow performance (sends, opens, clicks, complaints by flow) beyond send counts.
- Unsubscribe link and postal address compliance.
- The hard versus soft bounce split, and the exact definition of "dormant" used for the engaged segment.

Fix 1 first: the sending domain fails DKIM and has no DMARC policy, so every send, including the Q4 promotional sends, is exposed on the check mailbox providers make before placing mail. Fix 2 and 3 (the dormant send and the flash complaints) before any Q4 send, then 4 to 6 before the budget decision.
````
