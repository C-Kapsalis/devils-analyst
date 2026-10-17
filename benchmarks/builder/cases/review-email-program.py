"""Review a quarterly email program report (Juniper Lane Tea, Q3 2026).

Planted problems (5): clearance blast crowned "best campaign" on clicks while
it has the lowest revenue and revenue per order (MUST); subject-line test
recommended for a send whose delivery rate is under 95% (MUST); "list is
healthy" while net list growth turned negative; newsletter bounce rate rising
send after send at flat volume called healthy because each is under 2%; the
newest send (1 day old) ranked bottom on lifetime clicks.
Decoys (2): GA4 sessions a few % under clicks on every send, called normal;
unsubscribe rates 0.1-0.35% called normal."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "review-email-program"
rng = random.Random(77311)
REPORT_DATE = "2026-10-01"

# name: (date, segment, sent, bounce, open_rate, click_rate(of delivered), unsub, orders, aov)
NL_BOUNCE = [0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.017]
NL_DATES = ["2026-07-02", "2026-07-16", "2026-07-30", "2026-08-13", "2026-08-27", "2026-09-10", "2026-09-24"]
SENDS = []
for i, (d, b) in enumerate(zip(NL_DATES, NL_BOUNCE)):
    SENDS.append((d, f"Newsletter #{31 + i}", "All subscribers", 24000, b, 0.34, 0.027, 0.0022, 28, 64))
SENDS += [
    ("2026-07-09", "Iced tea summer edit", "Engaged last 90 days", 8200, 0.005, 0.44, 0.048, 0.0015, 41, 58),
    ("2026-07-23", "VIP early access", "VIP customers", 2100, 0.003, 0.58, 0.121, 0.0016, 72, 81),
    ("2026-08-06", "Matcha lovers: ceremonial grade", "Matcha buyers", 4800, 0.004, 0.49, 0.066, 0.0012, 54, 69),
    ("2026-08-20", "Clearance blast", "All subscribers + lapsed", 31500, 0.011, 0.27, 0.044, 0.0034, 57, 21.5),
    ("2026-09-03", "Autumn launch", "All subscribers + trade show leads", 27300, 0.074, 0.13, 0.019, 0.0029, 36, 74),
    ("2026-09-17", "VIP autumn tasting", "VIP customers", 2150, 0.003, 0.57, 0.117, 0.0012, 68, 83),
    ("2026-09-30", "Harvest Oolong preview", "Oolong and matcha buyers", 4650, 0.004, 0.31, 0.046, 0.0013, 19, 77),
]
SENDS.sort(key=lambda s: s[0])

rows, ga_rows, S = [], [], {}
for (d, name, seg, sent0, b, orate, crate, ur, orders0, aov) in SENDS:
    sent = int(sent0 * rng.uniform(0.99, 1.01))
    bounced = int(round(sent * b))
    delivered = sent - bounced
    opens = int(round(delivered * orate * rng.uniform(0.97, 1.03)))
    clicks = int(round(delivered * crate * rng.uniform(0.97, 1.03)))
    unsub = max(1, int(round(delivered * ur)))
    compl = int(round(delivered * rng.uniform(0.0002, 0.0005)))
    orders = int(round(orders0 * rng.uniform(0.95, 1.05)))
    rev = round(orders * aov * rng.uniform(0.97, 1.03), 2)
    sess = int(round(clicks * rng.uniform(0.93, 0.975)))
    S[name] = dict(date=d, seg=seg, sent=sent, bounced=bounced, delivered=delivered, opens=opens, clicks=clicks,
                   unsub=unsub, compl=compl, orders=orders, rev=rev, sess=sess)
    rows.append([d, name, seg, sent, delivered, bounced, opens, clicks, unsub, compl, orders, rev])
    ga_rows.append([name.lower().replace(" ", "_").replace(":", "").replace("#", "no"), name, sess])

# ---------- list growth ----------
LIST = [("2026-07", 25480, 820, 410, 260), ("2026-08", None, 690, 560, 310), ("2026-09", None, 640, 600, 330)]
list_rows, net = [], []
start = LIST[0][1]
for m, _, new, uns, cl in LIST:
    end = start + new - uns - cl
    list_rows.append([m, start, new, uns, cl, end])
    net.append((end - start) / start)
    start = end

# ---------- derived ----------
by_clicks = sorted(S, key=lambda n: -S[n]["clicks"])
by_rev = sorted(S, key=lambda n: -S[n]["rev"])
rpo = {n: S[n]["rev"] / S[n]["orders"] for n in S}
clear = S["Clearance blast"]
aut = S["Autumn launch"]
prev = S["Harvest Oolong preview"]
aut_deliv = aut["delivered"] / aut["sent"]
nl = [n for n in S if n.startswith("Newsletter")]
nl_bounce = [S[n]["bounced"] / S[n]["sent"] for n in sorted(nl, key=lambda n: S[n]["date"])]
nl_sent = [S[n]["sent"] for n in nl]
total_rev = sum(v["rev"] for v in S.values())
avg_open = sum(v["opens"] for v in S.values()) / sum(v["delivered"] for v in S.values())
months = {}
for v in S.values():
    m = v["date"][:7]
    months.setdefault(m, [0, 0])
    months[m][0] += v["clicks"]; months[m][1] += v["opens"]
ctor_m = {m: c / o for m, (c, o) in sorted(months.items())}
unsub_rates = {n: S[n]["unsub"] / S[n]["delivered"] for n in S}
sess_ratio = {n: S[n]["sess"] / S[n]["clicks"] for n in S}

# ---------- asserts ----------
assert by_clicks[0] == "Clearance blast", by_clicks[:3]
assert by_rev[-1] == "Clearance blast", [(n, S[n]["rev"]) for n in by_rev]
assert min(rpo, key=rpo.get) == "Clearance blast"
assert by_rev[0] in ("VIP early access", "VIP autumn tasting", "Matcha lovers: ceremonial grade")
assert S[by_rev[0]]["rev"] > 2.5 * clear["rev"]
assert aut_deliv < 0.94 and all(S[n]["delivered"] / S[n]["sent"] > 0.98 for n in S if n != "Autumn launch")
assert net[0] > 0 and net[1] < 0 and net[2] < 0
assert all(b2 > b1 for b1, b2 in zip(nl_bounce, nl_bounce[1:])) and max(nl_bounce) < 0.02 and nl_bounce[-1] > 3 * nl_bounce[0]
assert max(nl_sent) / min(nl_sent) < 1.03
assert min(S, key=lambda n: S[n]["clicks"]) == "Harvest Oolong preview"
assert max(ctor_m.values()) - min(ctor_m.values()) < 0.035
assert all(0.001 <= u <= 0.0036 for u in unsub_rates.values()), unsub_rates
assert all(0.92 < r < 0.98 for r in sess_ratio.values())
assert all(v["compl"] / v["delivered"] < 0.0006 for v in S.values())

eur = lambda x: f"€{x:,.0f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

table = "\n".join(
    f"| {v['date']} | {n} | {v['seg']} | {v['sent']:,} | {pc(v['delivered'] / v['sent'])} | {pc(v['opens'] / v['delivered'])} | "
    f"{v['clicks']:,} | {pc(v['clicks'] / v['delivered'], 2)} | {pc(v['clicks'] / v['opens'])} | {pc(unsub_rates[n], 2)} | {eur(v['rev'])} |"
    for n, v in sorted(S.items(), key=lambda kv: kv[1]["date"]))
ctor_txt = ", ".join(f"{m} {pc(c)}" for m, c in ctor_m.items())
min_r, max_r = min(sess_ratio.values()), max(sess_ratio.values())

artefact = f"""# Juniper Lane Tea: Email Program Review, Q3 2026

Prepared {REPORT_DATE}. Source: email platform export and GA4. All revenue figures are GA4 revenue from email sessions.

## Summary

- 14 sends in Q3 earned **{eur(total_rev)}** in revenue.
- **Best campaign of the quarter: Clearance blast**, with {clear['clicks']:,} clicks, the most of any send. We recommend making the clearance blast a monthly send from October.
- The list is healthy: engagement was stable all quarter (click-to-open rate by month: {ctor_txt}).

## All sends

| Send date | Campaign | Segment | Sent | Delivered | Open rate | Clicks | Click rate | CTOR | Unsub rate | Revenue |
|---|---|---|---|---|---|---|---|---|---|---|
{table}

Click rate = unique clicks / delivered. CTOR (click-to-open rate) = unique clicks / unique opens. Open rates are inflated by mail privacy features, so we use them only as a trend.

## What worked and what did not

**Clearance blast** was the top performer: {clear['clicks']:,} clicks, {clear['clicks'] - S[by_clicks[1]]['clicks']:,} more than the next best send ({by_clicks[1]}).

**Autumn launch** disappointed: an open rate of {pc(aut['opens'] / aut['delivered'])} against a quarter average of {pc(avg_open)}. The subject line ("Autumn is steeping") was too vague. Next launch we will A/B test two subject lines to fix the open rate.

**Harvest Oolong preview** was the weakest send of the quarter with only {prev['clicks']:,} clicks. We suggest dropping the preview format.

## Deliverability and list health

- Newsletter bounce rates stayed under 2% on every send this quarter ({', '.join(pc(b) for b in nl_bounce)}). Healthy.
- Unsubscribe rates ran between {pc(min(unsub_rates.values()), 2)} and {pc(max(unsub_rates.values()), 2)} per send, within the normal range.
- No spam complaint rate above 0.06% on any send.

## Tracking

GA4 shows slightly fewer email sessions than the platform shows clicks on each send ({pc(1 - max_r, 0)} to {pc(1 - min_r, 0)} fewer). That is normal: some clicks never load the page (security scanners, people closing the tab) and consent banners drop others. No action needed.

## Recommendations

1. Make the clearance blast monthly from October.
2. A/B test subject lines on the next launch email.
3. Drop the preview format.
4. Keep the current newsletter cadence; the list is in good shape.
"""

files = {
    "resources/email_review_q3_2026.md": artefact,
    "resources/email_campaigns_q3_2026.csv": to_csv(
        ["send_date", "campaign_name", "segment", "sent", "delivered", "bounced", "unique_opens", "unique_clicks",
         "unsubscribes", "spam_complaints", "orders", "revenue"], rows),
    "resources/list_growth_monthly_q3_2026.csv": to_csv(
        ["month", "start_size", "new_subscribers", "unsubscribed", "cleaned", "end_size"], list_rows),
    "resources/ga4_email_sessions_q3_2026.csv": to_csv(["session_campaign", "campaign_name", "sessions"], ga_rows),
}

prompt = """
I put together our Q3 email review (resources/email_review_q3_2026.md) from the exports in resources/ (email platform campaigns, monthly list numbers, and GA4 sessions). Can you check it before I send it to my boss? Tell me if it's OK to send and what I need to fix, in report.md.
"""

top = by_rev[0]
g_recall = f"""
The report under review (email_review_q3_2026.md) contains 5 planted problems. Answer key:

1. Best campaign crowned on clicks. Clearance blast is called the best campaign ({clear['clicks']:,} clicks, the most) and the report recommends repeating it monthly. On revenue it is the lowest of all 14 sends ({eur(clear['rev'])}) and has the lowest revenue per order ({eur(rpo['Clearance blast'])} vs {eur(rpo[top])} for {top}); the top revenue send is {top} ({eur(S[top]['rev'])}). Counts as found if report.md says sends should be ranked on revenue (or revenue per order / per recipient) and that Clearance blast is weak or the worst on that basis, so making it monthly is not supported.
2. Subject-line test on a send that did not deliver. Autumn launch delivered only {pc(aut_deliv)} of {aut['sent']:,} sent ({aut['bounced']:,} bounced, {pc(aut['bounced'] / aut['sent'])}); every other send delivered above 98%. Below 95% delivered, the problem is the list (the added trade show leads), authentication or reputation, not the subject line. Counts as found if report.md flags the delivery rate (under 95%, or the bounce rate of about {pc(aut['bounced'] / aut['sent'], 0)}) and says to fix the list or deliverability before testing subject lines.
3. List not healthy. Net list growth (new - unsubscribed - cleaned) / start size was {pc(net[0], 2)} in July, {pc(net[1], 2)} in August and {pc(net[2], 2)} in September: the list is shrinking while rates look stable, because rates only measure who is left. Counts as found if report.md says net list growth turned negative in August and/or September (or the list shrank from {list_rows[0][1]:,} to {list_rows[-1][5]:,}).
4. Bounce trend. Newsletter bounce rates rose every send ({', '.join(pc(b) for b in nl_bounce)}) at flat volume (about {min(nl_sent):,}-{max(nl_sent):,} sent). Each is under 2% but the steady rise is the warning sign of list decay. Counts as found if report.md flags the rising trend (not just the level).
5. Newest send judged too early. Harvest Oolong preview was sent {prev['date']}, one day before the report date ({REPORT_DATE}), so its {prev['clicks']:,} clicks are one day of accrual compared against sends with weeks of lifetime clicks. Counts as found if report.md says the preview cannot be compared yet (unequal age / measurement window) and dropping the format is premature.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention such as "look at revenue too" without saying the ranking changes does not count).
FAIL if it identifies fewer than 4.
"""

g_rank = f"""
Two of the problems are Must-fix because they drive the report's main recommendations:
- A. Clearance blast crowned best on clicks and recommended monthly, while it has the lowest revenue ({eur(clear['rev'])}) and lowest revenue per order of all sends.
- B. A subject-line A/B test recommended for Autumn launch, whose delivery rate was {pc(aut_deliv)} (under 95%): deliverability and list quality must be fixed first.
The lesser problems are: negative net list growth, the rising bounce trend, and the one-day-old preview send ranked last.

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the report can be sent as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves sending the report unchanged.
"""

g_decoy = f"""
The report contains two statements that are correct and must not be flagged:
- D1. GA4 email sessions are slightly below platform clicks on every send ({pc(1 - max_r, 0)} to {pc(1 - min_r, 0)} fewer), called normal. Sessions running a few percent under clicks on every row is expected (scanner clicks, early exits, consent); no send has clicks with zero sessions.
- D2. Unsubscribe rates of {pc(min(unsub_rates.values()), 2)} to {pc(max(unsub_rates.values()), 2)} per send, called normal. That is within the usual 0.1-0.4% band; no send is near 0.5%.

PASS if report.md does not present D1 or D2 as an error, a tracking problem, or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it flags D1 as lost tracking or a problem to investigate, or flags the unsubscribe rates as too high.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: clearance clicks {clear['clicks']} rev {clear['rev']:.0f} (top rev {top} {S[top]['rev']:.0f}); "
      f"autumn delivered {aut_deliv:.3f}; net growth {[round(x, 4) for x in net]}; nl bounce {[round(b, 4) for b in nl_bounce]}; "
      f"preview clicks {prev['clicks']}")
