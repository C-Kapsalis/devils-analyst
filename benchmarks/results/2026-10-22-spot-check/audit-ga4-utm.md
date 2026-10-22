# audit-ga4-utm

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/audit/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/audit-ga4-utm/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> I've just joined Orchard Row Apparel as marketing manager and I don't fully trust our GA4 numbers. I've exported the settings and reports I could find into resources/, with some notes. Can you audit our GA4 setup and tagging, tell me what's wrong and what to fix first? Please write it up in report.md.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `planted-recall` | PASS | PASS | A: 7 of 7; B: 6 of 7 (misses the data-driven fallback to last click) |
| `must-fix-first` | PASS | FAIL | A: retention, DDA on split events and scroll all Must fix, "Fix 1 and 2 first"; B: the DDA problem is missing |
| `decoys-left-alone` | PASS | FAIL | A: (not set) and the 5.3% click gap under Checked and fine; B: "(not set) ... means some tagging is missing" (borderline) |

## Arm A answer (with skill)

````markdown
# GA4 and UTM audit: Orchard Row Apparel

## Map
- **Sources:** GA4 admin settings (web property), key events (last 30 days to 30 Sep 2026), September 2026 traffic acquisition by source, medium and campaign, daily engagement (29 Jul to 25 Aug 2026), weekly display spend against GA4 sessions (3 Aug to 27 Sep 2026), and your notes.
- **Period:** September 2026 for traffic and key events; late July to late August for engagement; August to September for display.
- **Spend by channel:** display only, $9,624.40 over the four weeks from 31 Aug. The export has no search, Meta or email cost. Google Ads clicks in September: 25,250 (brand and generic).
- **Goal:** purchases (your notes). Margin, average order value and targets are not given, so this audit uses purchase revenue as the value measure and does not use margin.
- **Revenue truth:** none in the export. GA4 shows $184,443.40 purchase revenue across 131,507 September sessions. There is no store or backend total to reconcile against.
- **Missing:** store orders, Google Ads and Meta cost, your UTM link sheet, the agency's banner click URLs, page-level data for the lookbook, and funnel events other than add_to_cart and begin_checkout.

## Must fix
1. **Purchases are split over two key events** (GA admin, key events)
   - **What it is:** `purchase` has 262 events in the last 30 days and `purchase_app_checkout` has 185 (marked 3 Nov 2025). Together they are 447.
   - **Problem:** Each is below the roughly 400 per 30 days the reference uses as the volume line for data-driven credit (check current Google guidance on the threshold). Combined, 447 is above it. If one order can fire both events, the total double counts. I could not check that from the export.
   - **Fix:** Confirm in the event logs whether one order can fire both. If it can, keep one purchase key event with a parameter for the app checkout, and unmark the other.
   - **If you skip it:** Every purchase-based channel number in the monthly split. Spend is not in the export, so the money cannot be sized. It corrupts the split itself.

2. **Data-driven attribution is selected while purchase volume is low** (GA2)
   - **What it is:** Reporting attribution model is Data-driven. `sign_up` has 638 events in 30 days, `purchase` 262.
   - **Problem:** The monthly channel split is read from this report. Below the volume line, GA4 can fall back to last click without telling you, and the export does not show which model applies to each key event.
   - **Fix:** In the Advertising workspace, check the model in effect for `purchase`. Choose an explicit model (last click or a rule-based model) for purchases and write it on the monthly split. Recheck after fix 1, because the volume changes.
   - **If you skip it:** The monthly budget split for every channel. The spend is not in the export, so the money cannot be sized.

3. **Autumn Sale is spelled four ways in September traffic** (UTM campaign names)
   - **What it is:** `autumn_sale` (newsletter / email) 6,100 sessions, $17,008.36. `Autumn_Sale` (newsletter / email) 2,300 sessions, $6,722.38. `autumn-sale` (instagram / paid_social) 4,200 sessions, $4,709.68. `autumn sale ` with a trailing space (facebook / paid_social) 3,100 sessions, $4,149.85.
   - **Problem:** One campaign is spread over four names: 15,700 sessions and $32,590.27. The exact name `autumn_sale` holds $17,008.36 (52.2%). The other spellings hold $15,581.91 (47.8%). A report filtered on the exact name undercounts the sale by up to that share. There is also `newsletter / email / (not set)` with 410 sessions and $436.03, an email link with no campaign name.
   - **Fix:** Use one spelling from the link sheet (`autumn_sale`) and remove the trailing space. Fix the email template so the campaign is set. Merge the old spellings by hand for any report you compare across the sale.
   - **If you skip it:** $15,581.91 of September revenue (47.8% of the sale) can be misreported in any exact-match report.

4. **Prospecting campaign has source and medium reversed** (UTM medium and source)
   - **What it is:** `paid_social` / `facebook` / `prospecting_sep` has 5,600 sessions and $4,192.46. The correctly tagged row, `facebook` / `paid_social` / `prospecting_sep`, has 9,800 sessions and $7,384.45.
   - **Problem:** 36.4% of the campaign's sessions and 36.2% of its revenue sit in a row where the medium is not `paid_social`. A channel report will not count it as Paid Social. The row probably lands in Referral or Unassigned. The export has no channel group column, so this is a hypothesis until you check.
   - **Fix:** Find the link or ad template that swaps the two fields and correct it. Check the channel group of that row in the Traffic acquisition report.
   - **If you skip it:** $4,192.46 of September revenue (36% of the campaign) is outside Paid Social in every channel report, so Meta prospecting looks about a third smaller than it is.

5. **Scroll is a key event, and it stepped engagement up on 12 Aug** (GA5)
   - **What it is:** `scroll` became a key event on 12 Aug 2026 and has 40,176 events in 30 days. Engagement rate was 52.5% for the 14 days to 11 Aug (29,111 engaged of 55,442 sessions). It was 72.1% for the 14 days from 12 Aug (39,709 of 55,061). Sessions were flat (-0.7%) and engaged sessions rose 36.4%. The jump happens on the marking date itself: 53.6% on 11 Aug, 71.7% on 12 Aug.
   - **Problem:** A session with a key event counts as engaged, so every scroll now makes a session engaged. A step of 19.6 points on the marking day, with no ramp and no change in sessions, is the signature of this change. The content team's lookbook explanation is a hypothesis. The lookbook could add some real engagement, and the export cannot separate the two.
   - **Fix:** Unmark `scroll` as a key event and keep it as a plain event. Annotate 12 Aug in GA4. Restate the engagement trend on the same definition before anyone credits the lookbook. To test the lookbook claim, pull engagement for the lookbook pages before and after 12 Aug.
   - **If you skip it:** Every engagement trend across 12 Aug and the lookbook decision. No money figure is available from the export.

6. **Data retention is two months** (GA1)
   - **What it is:** `data_retention_event_data` is 2 months.
   - **Problem:** Explorations and funnels see only about two months back, to late August 2026 today. The Q4 plan to compare this autumn with last autumn in a 12-month funnel exploration cannot be built from event data. Last autumn's event data is probably already gone. Standard reports use aggregated data and may still show older months, so check them before concluding the history is lost.
   - **Fix:** Set retention to 14 months now. It is not retroactive. For last autumn, use the standard reports, or a warehouse export if one exists (not in the export).
   - **If you skip it:** The Q4 funnel and year-on-year comparison. No money figure.

7. **Display spend that GA4 cannot see** (UTM tagging of banner links)
   - **What it is:** Display spend is $9,624.40 over four weeks from 31 Aug to 27 Sep. GA4 shows 48 Google display sessions over those weeks (14, 11, 10 and 13) and 37 in the September file, with $0 revenue. Direct sessions averaged 4,046 a week in the four weeks before the flight and 5,864 a week during it: +1,819 a week, or +45%. Non-direct sessions moved by -154 a week (-0.7%).
   - **Problem:** The flight costs about $200 per GA4 display session. The Direct rise starts in the first flight week. Hypothesis: the agency's banner links are missing or partly missing UTM tags, so clicks land in Direct. Display CTR near 0.3-0.6% is normal, so do not judge the flight on CTR or on the 48 sessions alone.
   - **Fix:** Get the list of banner click URLs from the agency. Tag every one from the link sheet (for example `utm_medium=display`, `utm_campaign=autumn_sale`). Compare Direct for the weeks after tagging before you judge the flight.
   - **If you skip it:** $9,624.40 of display spend is judged on sessions that miss the Direct lift. As an upper bound, the lift could carry about $2,600 a week of Direct revenue (1,819 extra sessions at September's $1.45 Direct revenue per session), if those sessions convert like the average Direct session.

## Should fix
8. **Site search is off on a catalogue shop** (GA6)
   - **What it is:** `enhanced_measurement_site_search` is off.
   - **Problem:** On an apparel catalogue, search terms show what shoppers want and cannot be recovered after the fact.
   - **Fix:** Turn site search on in enhanced measurement and confirm the query parameter on the admin page matches the site's search URL.
   - **If you skip it:** Search terms are lost every day. No money figure.

9. **Brand and retargeting credit has no holdout** (causal claim, tier 5)
   - **What it is:** `google / cpc / brand_search` has 9,100 sessions and $22,635.90, which is 60.4% of GA4 paid-search revenue. `facebook / paid_social / retargeting_sep` has 2,900 sessions and $5,953.02, or $2.05 per session against $0.75 per session for prospecting.
   - **Problem:** These figures are credit, not lift. Brand's low cost per acquisition and retargeting's strong return are normal patterns. They become a problem only when budget moves on them alone, and the export has no holdout.
   - **Fix:** Test this. Run a geo or audience holdout for brand, and a holdout audience for retargeting, before moving budget on the ratios.
   - **If you skip it:** The budget split leans on credit. The spend is not in the export, so the money cannot be sized.

## Checked and fine
- Google Ads clicks (25,250) against GA4 Google cpc sessions (23,900): a 5.3% gap, under the 25% line.
- Direct share: 23,900 of 131,507 September sessions, 18.2%, inside the 10-25% band, when read across the whole month.
- `(not set)` revenue: $541.34, 0.3% of September revenue, under 1%.
- Cart abandonment on the 30-day counts: 86-92% (add_to_cart 3,120 against 447 or 262 purchases). Checkout abandonment is 65-79%. Both are short of the 95% flag. These are event counts, not sessions.
- Google Ads is linked; Google signals is on.
- Retargeting ROAS above prospecting is normal, not a finding by itself.

## Not checked
Store orders and revenue reconciliation; Google Ads and Meta cost; search and email cost; email and CRM programs; Search Console; funnel events view_item, add_shipping_info and add_payment_info; utm_content; AI assistant referrals (no AI sources in the export); the channel group column; page-level lookbook data; any BigQuery export; the time zone (set to America/New_York; confirm it matches the store's trading day so daily totals reconcile).

Fix 1 and 2 first: every monthly channel split reads a data-driven report, while purchases are split across two key events that each sit under the volume line.
````

## Arm B answer (without skill)

````markdown
# GA4 audit: Orchard Row Apparel

Scope: the six exports in resources/ (admin settings, key events for the 30 days to 30 Sep 2026, September 2026 traffic acquisition, daily engagement 29 Jul to 25 Aug, weekly display spend with GA4 sessions to 21 Sep) and the account notes. Figures are my arithmetic on those files. Nothing was changed in GA4.

## Bottom line

Three problems distort the numbers you use: scroll is counted as a key event, the data retention is 2 months, and the Autumn Sale display flight's traffic is landing in Direct. The August engagement "lift" that the content team credits to the lookbook lines up with the day scroll was made a key event, not with a change in traffic.

## Fix first, in this order

1. **Unmark `scroll` as a key event** (Admin > Events). It has 40,176 events in 30 days against 262 purchases. It inflates engaged sessions and key-event counts, and it feeds the data-driven model you use for the budget split. This takes effect going forward only, so note 12 Aug 2026 as the break in the series.
2. **Set data retention for event data to 14 months now** (Admin > Data settings). At 2 months, last autumn's event-level data is already gone (the window reaches back only to about 22 Aug 2026), so the planned 12-month funnel comparison cannot be built from GA4 explorations. Check whether a BigQuery export exists; none is in the exports. Standard reports keep aggregated history, so use those for a year-on-year view of traffic and revenue.
3. **Tag the display flight before anything else is scaled.** The agency's banner links are mostly untagged, so their visits show as Direct. Details below.
4. **Standardise campaign and source names**, then merge the variants before reading the budget split. GA4 cannot rewrite history, so the split stays in the data.
5. **Check for double-counted purchases** and reconcile revenue per purchase (below).

## Findings

### 1. Scroll is a key event, and it explains the August engagement jump (high)

- `scroll` was marked as a key event on 2026-08-12 (key events export).
- Daily engagement rate moves from 0.5363 on 11 Aug to 0.7168 on 12 Aug and stays between 0.70 and 0.74 to 25 Aug.
- Pooled over the 14 days before (29 Jul to 11 Aug) and the 14 days after (12 to 25 Aug):
  - Engagement rate: 52.5% (29,111 of 55,442 sessions) to 72.1% (39,709 of 55,061).
  - Sessions per day: 3,960 to 3,933 (-0.7%). Traffic did not change.
  - Engaged sessions per day: 2,079 to 2,836 (+36%).
- GA4 counts a session as engaged when it has a key event, so a key event on scroll mechanically lifts engagement.
- The content team says the lookbook pages caused it. The data does not support that yet. Confirm the lookbook go-live date. If it is not 12 Aug, the lift is the key-event change.

### 2. Data retention of 2 months blocks the Q4 plan (high)

- Admin shows `data_retention_event_data = 2 months`.
- The planned funnel exploration compares this autumn with last autumn over 12 months. It cannot work at 2 months, and last autumn's event data is already outside the window.
- Changing the setting protects future data only. It does not restore what was deleted.

### 3. The display flight's traffic is landing in Direct (high)

- Display spend starts in the week of 31 Aug (weekly file). Before that it is zero.
- Google display sessions tagged `autumn_display` are small: 14, 11, 10 and 13 per week, 48 in total over four weeks.
- Direct sessions per week:
  - Four weeks before the flight (3 Aug to 24 Aug): 4,172, 3,994, 4,000 and 4,016. Average 4,046.
  - Four flight weeks (31 Aug to 21 Sep): 5,868, 5,974, 5,790 and 5,825. Average 5,864.
  - Lift: about +1,819 Direct sessions a week (+45%). Total sessions rose from about 27,600 to about 29,300 a week.
- Cost per tagged session: $9,624.40 of display spend over the four weeks, 48 tagged sessions, about $201 each. The September acquisition export shows $0 revenue for the display row (37 sessions).
- The timing matches the flight start, but seasonality cannot be ruled out from these exports alone.
- Ask the agency for UTM-tagged links on every banner, and confirm whether the flight is still running.

### 4. Campaign and source names split the same campaigns (medium)

- **Autumn Sale** appears under four spellings: `autumn_sale` (6,100 sessions), `Autumn_Sale` (2,300), `autumn-sale` (4,200, Instagram), and `autumn sale ` with a trailing space (3,100, Facebook). Combined: 15,700 sessions and $32,590.27 revenue. The largest single row is 39% of that total.
- **Prospecting Sep** is split by a swapped source and medium: `facebook / paid_social` (9,800 sessions, $7,384.45) and `paid_social / facebook` (5,600 sessions, $4,192.46). Combined: 15,400 sessions and $11,576.91.
- Fix: one lowercase convention with underscores and no spaces, and a shared UTM builder. Merge the variants in the reporting layer before the monthly budget split.

### 5. Possible double count of purchases (medium, to check)

- `purchase` (262 events in 30 days, key event since 2023) and `purchase_app_checkout` (185 events, key event since Nov 2025) both exist.
- The app opens the web checkout, so one order could fire both events. Confirm the two events cannot fire for the same order.

### 6. Revenue does not reconcile to purchase counts (medium, to check)

- September purchase revenue in the acquisition export totals $184,443.40.
- Over 262 purchase events that is about $704 per purchase. Over 262 + 185 = 447 it is about $413. Both are high for an apparel shop, so either the purchase count or the revenue attribution is off.
- Reconcile against the order system before using either number for budget.

### 7. Social traffic classified as Referral (low to medium)

- `instagram / referral` (3,300 sessions) and `pinterest / referral` (1,900 sessions) use medium `referral`, so GA4 files them under Referral, not Organic Social.
- Tag social links with medium `social` (or `paid_social` for paid).

### 8. Smaller checks

- Reporting time zone is America/New_York. Confirm it matches the Google Ads account and the business's reporting day.
- Enhanced measurement site search is off. Turn it on if the site has search.
- `(not set)` rows total 670 sessions (410 email, 260 unknown). Small, but it means some tagging is missing.

## What checks out

- **Google Ads link.** September Google CPC sessions are 23,900 (brand 9,100 and generic 14,800) against 25,250 Google Ads clicks, a 94.7% match. The link is working.
- **Core key events.** `purchase` and `sign_up` were set in April 2023 and look standard.
- **Attribution.** Data-driven is set. Make sure the budget split and the traffic report use the same model.

## Open questions for the team

- When did the lookbook go live? (Decides finding 1.)
- Is a BigQuery export set up? (Decides whether last autumn can be rebuilt at event level.)
- Is the display flight still running, and does the agency control its banner links?
- Is `scroll` or `purchase_app_checkout` imported into Google Ads as a conversion? If `scroll` is, bidding is also affected.
- Does the app checkout fire `purchase` and `purchase_app_checkout` for the same order?
- Is consent mode in place? Not in the exports, so not assessed.
- Which time zone do the store and Google Ads use?
````
