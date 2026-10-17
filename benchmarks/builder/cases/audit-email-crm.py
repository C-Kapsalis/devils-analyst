"""Audit an email and CRM program (Brightwater Candle Co, Q3 2026 exports).

Planted problems (7): DKIM failing and DMARC missing (MUST), 12-month dormant
contacts mailed inside the September newsletter (MUST), one August send above
the 0.1% complaint line hidden in a monthly average under it (MUST), net list
growth negative two months running, CLV on revenue and undiscounted so
CLV:CAC 4:1 is really ~1.3:1, win-back flow with no exit rule, ESP utm_campaign
name not matching the GA4 campaign name.
Decoys: unsubscribe 0.1-0.4% per send; CTOR 9-13%; GA4 sessions a few percent
under clicks on every matched send."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "audit-email-crm"
rng = random.Random(77141)

ENGAGED = 33600
DORMANT = 9400
# send_date, campaign, segment, utm_campaign (esp), utm in ga4, sent, bounce, complaint, open rate, ctor
SENDS = [
    ("2026-07-03", "Newsletter - July", "engaged_12m", "jul_newsletter", "jul_newsletter", ENGAGED, 0.0045, 0.00030),
    ("2026-07-15", "Summer Sale", "engaged_12m", "jul_summer_sale", "jul_summer_sale", ENGAGED + 120, 0.0048, 0.00036),
    ("2026-07-29", "New Scents Launch", "engaged_12m", "jul_new_scents", "jul_new_scents", ENGAGED + 260, 0.0052, 0.00027),
    ("2026-08-05", "Newsletter - August", "engaged_12m", "aug_newsletter", "aug_newsletter", ENGAGED + 310, 0.0050, 0.00030),
    ("2026-08-21", "Flash Sale 48h", "engaged_12m", "aug_flash_sale", "aug_flash_sale", ENGAGED + 380, 0.0055, 0.00157),
    ("2026-08-28", "Back to Home", "engaged_12m", "aug_back_to_home", "aug_back_to_home", ENGAGED + 400, 0.0053, 0.00029),
    ("2026-09-02", "Newsletter - September", "all_subscribers", "sep_newsletter", "sep_newsletter", ENGAGED + 420 + DORMANT, None, 0.00078),
    ("2026-09-16", "Autumn Collection", "engaged_12m", "sep_autumn_collection", "sep-autumn-collection", ENGAGED + 390, 0.0058, 0.00034),
    ("2026-09-26", "Candle Care Guide", "engaged_12m", "sep_candle_care", "sep_candle_care", ENGAGED + 350, 0.0056, 0.00028),
]
rows, ga_rows, recs = [], [], []
for date, camp, seg, utm, ga_utm, sent, br, cr in SENDS:
    if br is None:   # engaged part bounces normally, dormant part heavily
        bounced = int(round((ENGAGED + 420) * 0.0057 + DORMANT * 0.135))
    else:
        bounced = int(round(sent * br))
    delivered = sent - bounced
    opens = int(round(delivered * rng.uniform(0.31, 0.37) * (0.82 if seg == "all_subscribers" else 1)))
    clicks = int(round(opens * rng.uniform(0.095, 0.125)))
    unsub = int(round(delivered * rng.uniform(0.0016, 0.0031)))
    compl = int(round(delivered * cr))
    rows.append([date, camp, seg, utm, sent, delivered, bounced, opens, clicks, unsub, compl])
    recs.append(dict(date=date, camp=camp, seg=seg, utm=utm, ga=ga_utm, sent=sent, deliv=delivered, bounced=bounced,
                     opens=opens, clicks=clicks, unsub=unsub, compl=compl))
    sess = int(round(clicks * rng.uniform(0.92, 0.97)))
    tx = int(round(sess * rng.uniform(0.035, 0.05)))
    ga_rows.append([ga_utm, "email", "newsletter", sess, tx, round(tx * rng.uniform(44, 52), 2)])

by = {r["camp"]: r for r in recs}
news = by["Newsletter - September"]
flash = by["Flash Sale 48h"]
autumn = by["Autumn Collection"]
news_bounce = news["bounced"] / news["sent"]
other_bounce = [r["bounced"] / r["sent"] for r in recs if r is not news]
flash_compl = flash["compl"] / flash["deliv"]

# ESP monthly summary (delivered-weighted averages, as the ESP shows them)
summ_rows, month_avg = [], {}
for m, label in (("07", "2026-07"), ("08", "2026-08"), ("09", "2026-09")):
    rs = [r for r in recs if r["date"][5:7] == m]
    d = sum(r["deliv"] for r in rs)
    cpl = sum(r["compl"] for r in rs) / d
    month_avg[label] = cpl
    summ_rows.append([label, len(rs), sum(r["sent"] for r in rs), d,
                      round(100 * sum(r["bounced"] for r in rs) / sum(r["sent"] for r in rs), 2),
                      round(100 * cpl, 3), round(100 * sum(r["unsub"] for r in rs) / d, 2)])

# list growth
list_rows, lg = [], []
start = 43200
for month, new, uns, cleaned in (("2026-04", 980, 520, 190), ("2026-05", 940, 560, 210), ("2026-06", 900, 610, 220),
                                 ("2026-07", 930, 640, 240), ("2026-08", 790, 700, 260), ("2026-09", 760, 740, 280)):
    end = start + new - uns - cleaned
    lg.append((month, (end - start) / start))
    list_rows.append([month, start, new, uns, cleaned, end])
    start = end
net_aug, net_sep = lg[4][1], lg[5][1]

auth_rows = [
    ["SPF", "brightwatercandle.com", "pass", "v=spf1 include:_spf.esp-mailer.net ~all"],
    ["DKIM", "s1._domainkey.brightwatercandle.com", "fail", "published key does not match the signing key in the ESP"],
    ["DMARC", "_dmarc.brightwatercandle.com", "missing", "no record found"],
]
flows = [
    ["Welcome series", "live", "joined list", "after email 3 or first purchase", 2140],
    ["Abandoned cart", "live", "cart started, no purchase in 2h", "purchase or after email 2", 1310],
    ["Post-purchase review", "live", "order delivered", "after email 1", 980],
    ["Win-back", "live", "no purchase in 180 days", "none", 18640],
]

# CLV sheet: revenue-based, undiscounted (planted)
AOV, OPY, TENURE, MARGIN, DISC, CAC = 42.0, 2.6, 3, 0.38, 0.10, 82.0
clv_rev = AOV * OPY * TENURE
ratio_rev = clv_rev / CAC
margin_year = AOV * OPY * MARGIN
clv_true = sum(margin_year / (1 + DISC) ** t for t in range(1, TENURE + 1))
ratio_true = clv_true / CAC
clv_rows = [
    ["average_order_value", AOV, "store, last 12 months"],
    ["orders_per_customer_per_year", OPY, "store, last 12 months"],
    ["average_customer_tenure_years", TENURE, "estimate"],
    ["gross_margin", MARGIN, "finance"],
    ["discount_rate", DISC, "finance"],
    ["clv_formula", "average_order_value * orders_per_customer_per_year * average_customer_tenure_years", ""],
    ["clv", round(clv_rev, 2), "used in board deck"],
    ["blended_cac", CAC, "paid spend / new customers, last 12 months"],
    ["clv_to_cac", round(ratio_rev, 2), "used to justify +20% acquisition budget"],
]

ga_names = {r[0] for r in ga_rows}
# ---------- asserts ----------
assert news_bounce > 0.025 and max(other_bounce) < 0.008, (news_bounce, other_bounce)
assert news["deliv"] / news["sent"] > 0.95
assert flash_compl > 0.0013 and month_avg["2026-08"] < 0.001, (flash_compl, month_avg)
assert all(r["compl"] / r["deliv"] < 0.001 for r in recs if r is not flash)
assert net_aug < 0 and net_sep < 0 and all(x[1] > 0 for x in lg[:4])
assert ratio_rev > 3.5 and ratio_true < 1.5, (ratio_rev, ratio_true)
assert autumn["utm"] not in ga_names and "sep-autumn-collection" in ga_names
for r in recs:
    assert 0.001 <= r["unsub"] / r["deliv"] <= 0.004
    assert 0.09 <= r["clicks"] / r["opens"] <= 0.13
for g in ga_rows:
    c = next(r for r in recs if r["ga"] == g[0])["clicks"]
    assert 0.9 < g[3] / c < 0.98

pc = lambda x, d=1: f"{100 * x:.{d}f}%"

notes = """# Brightwater Candle Co: email and CRM handover notes

- Business: online candle and home fragrance shop. Goal of email: repeat purchases.
- ESP exports for July to September 2026, the domain authentication check, the automated flows, the list history, GA4 email campaign data and the CLV sheet the board deck uses are in this folder.
- The September newsletter went to the whole list this time "to wake people up".
- Plan for Q4: two extra promotional sends per month and a 20% higher acquisition budget, justified by the CLV:CAC ratio.
"""

files = {
    "resources/handover_notes.md": notes,
    "resources/esp_sends_q3_2026.csv": to_csv(
        ["send_date", "campaign", "segment", "utm_campaign", "sent", "delivered", "bounced", "unique_opens", "unique_clicks",
         "unsubscribes", "spam_complaints"], rows),
    "resources/esp_monthly_summary_q3_2026.csv": to_csv(
        ["month", "sends", "sent", "delivered", "bounce_rate_pct", "complaint_rate_pct", "unsubscribe_rate_pct"], summ_rows),
    "resources/list_growth_monthly.csv": to_csv(
        ["month", "start_size", "new_subscribers", "unsubscribed", "cleaned", "end_size"], list_rows),
    "resources/domain_authentication.csv": to_csv(["record", "host", "status", "detail"], auth_rows),
    "resources/automated_flows.csv": to_csv(["flow", "status", "entry_rule", "exit_rule", "sends_last_30d"], flows),
    "resources/ga4_email_campaigns_q3_2026.csv": to_csv(
        ["session_campaign", "session_medium", "session_source", "sessions", "transactions", "purchase_revenue"], ga_rows),
    "resources/clv_sheet.csv": to_csv(["item", "value", "note"], clv_rows),
}

prompt = """
I just took over email and CRM at Brightwater Candle Co from a freelancer. Everything I was handed is in resources/: the handover notes, our ESP exports for Q3, the domain check, our automated flows, list growth, GA4 email data and the CLV sheet from the board deck. Can you audit the whole program and tell me what to fix first before we add more sends in Q4? Put it in report.md.
"""

N, K = 7, math.ceil(0.8 * 7)
g_recall = f"""
The exports contain {N} planted problems. Answer key:

1. Authentication. DKIM status is "fail" (published key does not match the signing key) and DMARC is "missing". SPF passes. Bulk senders need all three passing. Counts as found if report.md says DKIM is failing and/or DMARC is missing and must be fixed.
2. Dormant contacts in the main send. "Newsletter - September" went to segment all_subscribers (sent {news['sent']:,}, including about {DORMANT:,} contacts outside the engaged_12m segment); its bounce rate is {pc(news_bounce, 2)} while every other send is between {pc(min(other_bounce), 2)} and {pc(max(other_bounce), 2)}. Counts as found if report.md links the September newsletter's high bounce rate (about {pc(news_bounce, 1)}) to mailing the dormant / non-engaged list in the main send and says to separate or suppress them.
3. Complaint spike hidden by the average. "Flash Sale 48h" (2026-08-21) had {flash['compl']} complaints on {flash['deliv']:,} delivered = {pc(flash_compl, 3)}, above the 0.1% warning line, while the ESP's August average shows {pc(month_avg['2026-08'], 3)}. Counts as found if report.md names that send (or an August send) above 0.1% complaints.
4. Shrinking list. Net list growth was {pc(net_aug, 2)} in August and {pc(net_sep, 2)} in September (new subscribers minus unsubscribed minus cleaned), after positive months; campaign rates look steady because they only measure who is left. Counts as found if report.md says net list growth turned negative.
5. CLV on revenue. The CLV sheet uses revenue x orders x tenure = {clv_rev:,.2f}, ignoring the 38% gross margin and the 10% discount rate; CLV:CAC {ratio_rev:.2f}. On discounted margin, CLV is about {clv_true:,.2f} and CLV:CAC about {ratio_true:.2f}. Counts as found if report.md says CLV must use margin (and ideally discounting) and that the ratio is far lower than {ratio_rev:.1f} (any margin-based figure between 1.0 and 1.6 is fine).
6. Win-back flow has no exit rule (exit_rule "none") and sent {flows[3][4]:,} emails in 30 days. Counts as found if report.md says the win-back flow needs an exit or suppression rule.
7. Tagging mismatch. The ESP send "Autumn Collection" uses utm_campaign sep_autumn_collection, but GA4 records sep-autumn-collection (hyphens), so the campaign does not join by name. Counts as found if report.md points out the name mismatch.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} problems, each with its substance (a vague mention such as "check deliverability" does not count).
FAIL if it identifies fewer than {K}.
"""

g_rank = f"""
Three problems are Must-fix (deliverability and reputation, which every other email number depends on):
- A. DKIM failing and DMARC missing.
- B. Dormant contacts mailed inside the September newsletter (bounce {pc(news_bounce, 1)}).
- C. Flash Sale 48h complaint rate {pc(flash_compl, 3)}, above 0.1%, hidden in an August average of {pc(month_avg['2026-08'], 3)}.
The lesser problems are: negative net list growth, the revenue-based CLV, the win-back exit rule and the utm_campaign name mismatch.

PASS if report.md flags A, B and C, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists them before the lesser problems, AND the closing "fix first" line (or explicit first priority) names one of A, B or C.
FAIL if A, B or C is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the first priority named is something other than A, B or C.
"""

unsubs = [r["unsub"] / r["deliv"] for r in recs]
ctors = [r["clicks"] / r["opens"] for r in recs]
g_decoy = f"""
Three patterns in the exports are normal and must not be flagged:
- D1. Unsubscribe rates per send between {pc(min(unsubs), 2)} and {pc(max(unsubs), 2)}: inside the normal band (problem only above about 0.5%).
- D2. Click-to-open rates (unique clicks / unique opens) between {pc(min(ctors), 1)} and {pc(max(ctors), 1)}: inside the normal 8-15% band.
- D3. GA4 sessions 3-8% below ESP unique clicks on every send that joins by name: normal (some clicks never load the page).

PASS if report.md does not present D1, D2 or D3 as an error, a problem or something to fix. Mentioning them as normal or checked is a PASS. (Flagging the Autumn Collection name mismatch, where a send has no matching GA4 row at all, is a different problem and is fine.)
FAIL if it calls the unsubscribe rates too high, the CTOR weak, or the small click-to-session gap a tracking loss to fix.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: newsletter bounce {news_bounce:.4f} vs others <= {max(other_bounce):.4f}; flash complaints {flash_compl:.5f} vs Aug avg {month_avg['2026-08']:.5f}; "
      f"net growth Aug {net_aug:.4f} Sep {net_sep:.4f}; CLV {clv_rev:.1f} ({ratio_rev:.2f}x) vs {clv_true:.1f} ({ratio_true:.2f}x)")
