"""Audit a Power BI marketing model given as TMDL text (Northwind Coffee).

Planted (6): CTR = AVERAGE of a row-level ctr column (MUST); Email List Size =
SUM of a daily snapshot (MUST); Revenue toggle defaults to Gross while the
agreed definition is Net (MUST); Paid ROAS on stacked platform claims;
two CAC measures with different new-customer rules; Monthly Users = SUM of
daily active users.
Decoys (3): Conversion Rate as DIVIDE of sums; Share of Spend with
REMOVEFILTERS labelled as share of all paid channels; Store ROAS on net revenue."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "audit-powerbi-model"
rng = random.Random(77141)

# ---------- sample data, September 2026 ----------
ads = []
for d in range(1, 31):
    date = f"2026-09-{d:02d}"
    for ch, imps0, ctr0, cpc0, roas0 in (("Google Ads", 3200, 0.064, 0.92, 8.0), ("Meta", 41000, 0.0118, 0.71, 6.0)):
        imps = int(imps0 * rng.uniform(0.8, 1.2))
        clicks = int(round(imps * ctr0 * rng.uniform(0.85, 1.15)))
        cost = round(clicks * cpc0 * rng.uniform(0.92, 1.08), 2)
        val = round(cost * roas0 * rng.uniform(0.8, 1.2), 2)
        ads.append([date, ch, imps, clicks, round(clicks / imps, 4), cost, val])
imps = sum(r[2] for r in ads); clicks = sum(r[3] for r in ads); spend = sum(r[5] for r in ads)
claims = sum(r[6] for r in ads)
ctr_true = clicks / imps
ctr_avg = sum(r[4] for r in ads) / len(ads)
g_claim = sum(r[6] for r in ads if r[1] == "Google Ads"); m_claim = claims - g_claim
spend_g = sum(r[5] for r in ads if r[1] == "Google Ads")
share_g = spend_g / spend

lst, size = [], 18420
for d in range(1, 31):
    size += rng.randint(-6, 22)
    lst.append([f"2026-09-{d:02d}", size])
list_end = lst[-1][1]; list_sum = sum(r[1] for r in lst)

ga = []
for d in range(1, 31):
    au = int(rng.gauss(2150, 180)); ses = int(au * rng.uniform(1.25, 1.4)); conv = int(ses * rng.uniform(0.021, 0.027))
    ga.append([f"2026-09-{d:02d}", ses, au, conv])
users_sum = sum(r[2] for r in ga)
users_month = int(users_sum * 0.58)   # GA4's own monthly distinct count (people visit on several days)
sessions = sum(r[1] for r in ga); convs = sum(r[3] for r in ga)

# orders summary by channel group
orders_rows = []
for ch, n, aov in (("Paid", 790, 41.0), ("Organic & direct", 1050, 38.5), ("Email", 510, 36.0)):
    gross = round(n * aov * rng.uniform(0.97, 1.03), 2)
    disc = round(gross * 0.08, 2); refunds = round(gross * 0.035, 2); vat = round((gross - disc - refunds) * 0.2 / 1.2, 2)
    net = round(gross - disc - refunds - vat, 2)
    orders_rows.append([ch, n, gross, disc, refunds, vat, net])
gross_tot = sum(r[2] for r in orders_rows); net_tot = sum(r[6] for r in orders_rows)

new_cust, reactivated = 412, 196
cac_new = spend / new_cust
cac_exec = spend / (new_cust + reactivated)
store_roas = net_tot / spend
paid_roas = claims / spend

assert ctr_avg / ctr_true > 1.8, (ctr_avg, ctr_true)
assert list_sum / list_end > 25
assert gross_tot / net_tot > 1.25
assert claims > net_tot, (claims, net_tot)
assert paid_roas / store_roas > 1.4
assert cac_new / cac_exec > 1.35
assert users_sum / users_month > 1.6
assert 0.015 < convs / sessions < 0.03

eur = lambda x: f"€{x:,.0f}"
pc = lambda x, d=2: f"{100 * x:.{d}f}%"

tmdl = """// Northwind Coffee marketing model (TMDL, definition folder concatenated)

table Measures

	/// Click-through rate for paid ads.
	measure CTR = AVERAGE('Fact Ads Daily'[ctr])
		formatString: 0.00%
		displayFolder: Paid

	/// Total paid media spend.
	measure 'Total Spend' = SUM('Fact Ads Daily'[cost])
		formatString: \\€#,0
		displayFolder: Paid

	/// Share of spend within all paid channels (ignores the channel filter in the denominator).
	measure 'Share of Spend' = DIVIDE([Total Spend], CALCULATE([Total Spend], REMOVEFILTERS('Fact Ads Daily'[channel])))
		formatString: 0.0%
		displayFolder: Paid

	/// Return on paid spend, from the ad platforms' reported conversion value.
	measure 'Paid ROAS' = DIVIDE(SUM('Fact Ads Daily'[platform_conv_value]), [Total Spend])
		formatString: 0.00x
		displayFolder: Paid

	/// Net store revenue per euro of paid spend.
	measure 'Store ROAS' = DIVIDE([Net Revenue], [Total Spend])
		formatString: 0.00x
		displayFolder: Paid

	/// Revenue. Follows the Revenue Basis slicer.
	measure Revenue =
			VAR _basis = SELECTEDVALUE('Revenue Basis'[Basis], "Gross")
			RETURN
				SWITCH(_basis,
					"Gross", SUM('Fact Orders'[gross_revenue]),
					"Net", [Net Revenue])
		formatString: \\€#,0
		displayFolder: Revenue

	/// Revenue after discounts and refunds, excluding VAT.
	measure 'Net Revenue' = SUM('Fact Orders'[net_revenue])
		formatString: \\€#,0
		displayFolder: Revenue

	/// Email subscribers.
	measure 'Email List Size' = SUM('Fact Email List Daily'[list_size])
		formatString: #,0
		displayFolder: Email

	/// Website users in the period.
	measure 'Monthly Users' = SUM('Fact GA4 Daily'[active_users])
		formatString: #,0
		displayFolder: Web

	/// Sessions that converted.
	measure 'Conversion Rate' = DIVIDE(SUM('Fact GA4 Daily'[conversions]), SUM('Fact GA4 Daily'[sessions]))
		formatString: 0.00%
		displayFolder: Web

	/// First-time customers.
	measure 'New Customers' = CALCULATE(DISTINCTCOUNT('Fact Orders'[customer_id]), 'Fact Orders'[is_new_customer] = TRUE())
		formatString: #,0
		displayFolder: Customers

	/// Paid spend per new customer.
	measure CAC = DIVIDE([Total Spend], [New Customers])
		formatString: \\€#,0.00
		displayFolder: Customers

	/// Used on the Executive page.
	measure 'CAC (Exec)' = DIVIDE([Total Spend], CALCULATE(DISTINCTCOUNT('Fact Orders'[customer_id]), 'Fact Orders'[is_new_customer] = TRUE() || 'Fact Orders'[is_reactivated] = TRUE()))
		formatString: \\€#,0.00
		displayFolder: Customers

table 'Fact Ads Daily'

	column date
		dataType: dateTime
		sourceColumn: date

	column channel
		dataType: string
		sourceColumn: channel

	column impressions
		dataType: int64
		sourceColumn: impressions
		summarizeBy: sum

	column clicks
		dataType: int64
		sourceColumn: clicks
		summarizeBy: sum

	column ctr
		dataType: double
		sourceColumn: ctr

	column cost
		dataType: double
		sourceColumn: cost
		summarizeBy: sum

	column platform_conv_value
		dataType: double
		sourceColumn: platform_conv_value
		summarizeBy: sum

table 'Fact Email List Daily'

	column date
		dataType: dateTime
		sourceColumn: date

	column list_size
		dataType: int64
		sourceColumn: list_size

table 'Fact GA4 Daily'

	column date
		dataType: dateTime
		sourceColumn: date

	column sessions
		dataType: int64
		sourceColumn: sessions

	column active_users
		dataType: int64
		sourceColumn: active_users

	column conversions
		dataType: int64
		sourceColumn: conversions

table 'Fact Orders'

	column order_id
		dataType: string
		sourceColumn: order_id

	column order_date
		dataType: dateTime
		sourceColumn: order_date

	column customer_id
		dataType: string
		sourceColumn: customer_id

	column gross_revenue
		dataType: double
		sourceColumn: gross_revenue

	column net_revenue
		dataType: double
		sourceColumn: net_revenue

	column is_new_customer
		dataType: boolean
		sourceColumn: is_new_customer

	column is_reactivated
		dataType: boolean
		sourceColumn: is_reactivated

/// Slicer table for the revenue toggle. Not related to any table.
table 'Revenue Basis'

	column Basis
		dataType: string
		sourceColumn: Basis

	partition 'Revenue Basis' = calculated
		source = DATATABLE("Basis", STRING, {{"Gross"}, {"Net"}})

table Date

	column Date
		dataType: dateTime
		sourceColumn: Date

relationship 'Fact Ads Daily to Date'
	fromColumn: 'Fact Ads Daily'.date
	toColumn: Date.Date

relationship 'Fact Email List Daily to Date'
	fromColumn: 'Fact Email List Daily'.date
	toColumn: Date.Date

relationship 'Fact GA4 Daily to Date'
	fromColumn: 'Fact GA4 Daily'.date
	toColumn: Date.Date

relationship 'Fact Orders to Date'
	fromColumn: 'Fact Orders'.order_date
	toColumn: Date.Date
"""

notes = f"""# Northwind Coffee: marketing model notes

Agreed definitions (signed off by finance and marketing, March 2026):

- **Revenue** on every page means net revenue: after discounts and refunds, excluding VAT. Gross is only for the finance reconciliation page, where the Revenue Basis slicer is set to Gross on purpose.
- **CTR** = clicks / impressions.
- **Email list size** = subscribers at the end of the period.
- **Monthly users** = GA4 users in the month (GA4's own count).
- **New customer** = first order ever. Reactivated customers (returning after 12+ months) are not new.
- **CAC** = paid spend / new customers.
- **ROAS** = net store revenue / paid spend. Platform-reported values are for in-platform optimisation only.

Most report pages have no Revenue Basis slicer; the Executive page uses CAC (Exec). Paid channels in the model: Google Ads and Meta.

September 2026 reference figures from the source systems:
- Shopify: gross sales {eur(gross_tot)}, net revenue {eur(net_tot)}.
- GA4 Users (month, GA4 report): {users_month:,}.
- Email platform: subscribers on 30 September: {list_end:,}.
- New customers (first order ever): {new_cust}; reactivated customers: {reactivated}.
"""

files = {
    "resources/model.tmdl": tmdl,
    "resources/model_notes.md": notes,
    "resources/sample_ads_daily_sep2026.csv": to_csv(["date", "channel", "impressions", "clicks", "ctr", "cost", "platform_conv_value"], ads),
    "resources/sample_email_list_daily_sep2026.csv": to_csv(["date", "list_size"], lst),
    "resources/sample_ga4_daily_sep2026.csv": to_csv(["date", "sessions", "active_users", "conversions"], ga),
    "resources/orders_summary_sep2026.csv": to_csv(["channel_group", "orders", "gross_revenue", "discounts", "refunds", "vat", "net_revenue"], orders_rows),
}

prompt = """
We're handing our Power BI marketing model over to a new agency next month. The model definition is in resources/model.tmdl, our notes on how we define things are in resources/model_notes.md, and there's a month of sample data in resources/. Can you audit the model before we hand it over and tell me what we should fix first? Write it up in report.md.
"""

key = f"""
1. CTR averaged. `CTR = AVERAGE('Fact Ads Daily'[ctr])` averages daily row rates, so a Google day with about 3,000 impressions weighs as much as a Meta day with about 40,000. On the September sample it returns {pc(ctr_avg)}; clicks / impressions = {clicks:,} / {imps:,} = {pc(ctr_true)}. Fix: DIVIDE(SUM(clicks), SUM(impressions)). Counts as found if report.md says CTR must be a ratio of sums (or gives a figure within 0.1 points of {pc(ctr_true)}).
2. Email List Size summed. `SUM('Fact Email List Daily'[list_size])` adds a daily snapshot, so September shows {list_sum:,} instead of the {list_end:,} subscribers on 30 September. Fix: closing value (LASTDATE / LASTNONBLANKVALUE). Counts as found if report.md says the snapshot must not be summed over days.
3. Revenue toggle default. `SELECTEDVALUE('Revenue Basis'[Basis], "Gross")` makes every page without a slicer show gross revenue ({eur(gross_tot)} in September) while the agreed definition is net ({eur(net_tot)}), {pc(gross_tot / net_tot - 1, 0)} higher. Fix: default to "Net". Counts as found if report.md says the default (no selection) is Gross and should be Net.
4. Paid ROAS on platform claims. `Paid ROAS` divides the sum of Google's and Meta's reported conversion value ({eur(claims)}) by spend: {paid_roas:.2f}x, while the claims exceed all net store revenue ({eur(net_tot)}); the agreed ROAS is net store revenue / spend = {store_roas:.2f}x (the existing Store ROAS measure). Counts as found if report.md flags Paid ROAS as double-counted platform claims or contrary to the agreed ROAS.
5. Two CACs. `CAC (Exec)`, used on the Executive page, counts reactivated customers as new: {eur(cac_exec)} vs the agreed CAC {eur(cac_new)} ({new_cust} new customers vs {new_cust + reactivated}). Counts as found if report.md flags the two CAC definitions or the reactivated customers in CAC (Exec).
6. Monthly Users summed. `SUM('Fact GA4 Daily'[active_users])` adds daily users: {users_sum:,} for September vs GA4's monthly {users_month:,}. Counts as found if report.md says users cannot be summed across days."""

g_recall = f"""
The model contains 6 planted problems. Answer key:
{key}

List which ones were found in your reasoning.
PASS if report.md identifies at least 5 of the 6 problems, each with its substance (a vague mention such as "review your measures" does not count).
FAIL if it identifies fewer than 5.
"""

g_rank = f"""
Three problems are Must-fix because every page that uses them shows a wrong number by default:
- A. CTR as AVERAGE of the ctr column ({pc(ctr_avg)} vs true {pc(ctr_true)}).
- B. Email List Size summing a daily snapshot ({list_sum:,} vs {list_end:,}).
- C. Revenue Basis toggle defaulting to Gross instead of the agreed Net ({eur(gross_tot)} vs {eur(net_tot)}).
The lesser problems are Paid ROAS on platform claims, the duplicate CAC (Exec), and Monthly Users summed.

PASS if report.md flags A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND its closing "fix first" line (or explicit first priority) names one of A, B or C.
FAIL if any of A, B, C is missing, labelled lower severity (Should fix, Nice to have), or listed after one of the lesser problems, or if the first fix named is something else.
Note: also placing Paid ROAS or CAC (Exec) in Must fix is acceptable, as long as A, B and C are there and not ranked below them.
"""

g_decoy = f"""
Three measures are correct and must not be flagged:
- D1. `Conversion Rate = DIVIDE(SUM(conversions), SUM(sessions))`: a ratio of sums ({pc(convs / sessions)} on the sample).
- D2. `Share of Spend` uses REMOVEFILTERS on channel in the denominator and its description says it is the share within all paid channels (Google Ads {pc(share_g, 1)} of spend). That is the intended share-of-total pattern.
- D3. `Store ROAS = DIVIDE([Net Revenue], [Total Spend])` matches the agreed ROAS definition ({store_roas:.2f}x).

PASS if report.md does not present D1, D2 or D3 as an error or something to change. Mentioning them as correct, or recommending Store ROAS as the replacement for Paid ROAS, is a PASS.
FAIL if it says any of D1, D2 or D3 is wrong or needs a different formula.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: CTR avg {ctr_avg:.4f} vs {ctr_true:.4f}; list sum {list_sum} vs {list_end}; gross {gross_tot:,.0f} vs net {net_tot:,.0f}; "
      f"paid ROAS {paid_roas:.2f} vs store {store_roas:.2f}; CAC {cac_new:.2f} vs exec {cac_exec:.2f}; users {users_sum} vs {users_month}")
