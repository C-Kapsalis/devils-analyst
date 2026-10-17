"""Control: a correct weekly paid search + email report (Fernhill Garden Supply,
week of 5 October 2026). Every number recomputes from the CSVs; rates are
ratios of sums; brand and generic are split; comparisons are to the prior week
and the same week last year; causal language is hedged; each recommendation
names its metric and check date. Suspicious-but-correct items: brand CTR ~40%,
GA4 google/cpc sessions ~6% below Google clicks, median order value labelled as
median and well below the mean (a few large orders)."""
import sys, random, math, csv, io; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "review-clean-control"
rng = random.Random(55120)
TARGET_CPA = 35.0
WEEKS = ["2025-10-06", "2026-09-28", "2026-10-05"]   # same week last year, prior week, this week

# campaign: (type, impressions, ctr, cpc, cvr, aov)
C = {
    "Brand - Fernhill": ("Brand", 5200, 0.40, 0.28, 0.13, 58),
    "Generic - Seeds and Bulbs": ("Generic", 41000, 0.058, 0.62, 0.026, 41),
    "Generic - Garden Tools": ("Generic", 33000, 0.051, 0.88, 0.024, 67),
    "Generic - Planters": ("Generic", 27000, 0.047, 0.79, 0.022, 74),
}
# generic CPA improves this week (fewer wasted clicks); spend roughly flat
WEEK_ADJ = {"2025-10-06": (0.85, 1.0, 0.95), "2026-09-28": (1.0, 1.0, 1.0), "2026-10-05": (1.0, 0.97, 1.12)}
rows = []
for w in WEEKS:
    ia, ca, va = WEEK_ADJ[w]
    for name, (typ, im0, ctr, cpc, cvr, aov) in C.items():
        im = int(im0 * ia * rng.uniform(0.96, 1.04))
        cl = int(round(im * ctr * rng.uniform(0.96, 1.04)))
        cost = round(cl * cpc * (ca if typ == "Generic" else 1) * rng.uniform(0.98, 1.02), 2)
        conv = int(round(cl * cvr * (va if typ == "Generic" else 1) * rng.uniform(0.95, 1.05)))
        val = round(conv * aov * rng.uniform(0.96, 1.04), 2)
        rows.append([w, name, typ, "Purchase", im, cl, cost, conv, val])
ADS_H = ["week_start", "campaign", "campaign_type", "conversion_action", "impressions", "clicks", "cost", "conversions", "conv_value"]
ads_csv = to_csv(ADS_H, rows)

# recompute from the CSV text itself (what the analyst sees)
parsed = list(csv.DictReader(io.StringIO(ads_csv)))
def agg(week, typ=None):
    rs = [r for r in parsed if r["week_start"] == week and (typ is None or r["campaign_type"] == typ)]
    im = sum(int(r["impressions"]) for r in rs); cl = sum(int(r["clicks"]) for r in rs)
    co = sum(float(r["cost"]) for r in rs); cv = sum(int(r["conversions"]) for r in rs)
    va = sum(float(r["conv_value"]) for r in rs)
    return dict(im=im, cl=cl, co=co, cv=cv, va=va, ctr=cl / im, cpc=co / cl, cpa=co / cv, roas=va / co)
cur, prev, ly = WEEKS[2], WEEKS[1], WEEKS[0]
A = {(w, t): agg(w, t) for w in WEEKS for t in ("Brand", "Generic", None)}
gc, gp, gl = A[(cur, "Generic")], A[(prev, "Generic")], A[(ly, "Generic")]
bc = A[(cur, "Brand")]
tc, tp = A[(cur, None)], A[(prev, None)]

# GA4 sessions (this week)
ga_cpc = int(round(tc["cl"] * 0.941))
email_clicks_cur = []

# email sends: two last week, two this week
E = [("2026-09-29", "Autumn bulb planting guide", 18400, 0.33, 0.105, 0.021, 0.0021, 52),
     ("2026-10-02", "Weekend tool offer", 18350, 0.31, 0.092, 0.017, 0.0024, 63),
     ("2026-10-06", "Seed saving how-to", 18290, 0.34, 0.112, 0.020, 0.0019, 47),
     ("2026-10-09", "Planter clearance", 18260, 0.30, 0.098, 0.022, 0.0027, 61)]
erows = []
for d, name, dl, orate, ctor, ocr, unsub, aov in E:
    op = int(round(dl * orate * rng.uniform(0.98, 1.02)))
    ck = int(round(op * ctor * rng.uniform(0.97, 1.03)))
    od = int(round(ck * ocr * 3.1))
    rev = round(od * aov * rng.uniform(0.95, 1.05), 2)
    us = int(round(dl * unsub))
    erows.append([d, name, dl, op, ck, us, od, rev])
EM_H = ["send_date", "campaign", "delivered", "unique_opens", "unique_clicks", "unsubscribes", "orders", "revenue_from_tagged_sessions"]
em_csv = to_csv(EM_H, erows)
ep = list(csv.DictReader(io.StringIO(em_csv)))
def eagg(rs):
    dl = sum(int(r["delivered"]) for r in rs); ck = sum(int(r["unique_clicks"]) for r in rs)
    op = sum(int(r["unique_opens"]) for r in rs); rev = sum(float(r["revenue_from_tagged_sessions"]) for r in rs)
    us = sum(int(r["unsubscribes"]) for r in rs)
    return dict(dl=dl, ck=ck, op=op, rev=rev, cr=ck / dl, ctor=ck / op, us=us / dl)
ecur = eagg([r for r in ep if r["send_date"] >= "2026-10-05"])
eprev = eagg([r for r in ep if r["send_date"] < "2026-10-05"])
ga_email = int(round(ecur["ck"] * 0.955))

ga_rows = [["google / cpc", ga_cpc], ["newsletter / email", ga_email], ["google / organic", 6120], ["(direct) / (none)", 3310]]
ga_csv = to_csv(["session_source_medium", "sessions"], ga_rows)

# orders this week (all channels)
orows = []
for i in range(960):  # every channel: must exceed what Google Ads and email each claim
    v = round(math.exp(rng.gauss(3.72, 0.42)), 2)
    orows.append([f"FH-{40211 + i}", f"2026-10-{5 + i % 7:02d}", v])
orows[17][2] = 1249.00
orows[41][2] = 1189.00
ord_csv = to_csv(["order_id", "order_date", "order_value"], orows)
vals = sorted(float(r["order_value"]) for r in csv.DictReader(io.StringIO(ord_csv)))
n = len(vals)
median = (vals[n // 2 - 1] + vals[n // 2]) / 2 if n % 2 == 0 else vals[n // 2]
mean = sum(vals) / n
store_rev = sum(vals)
assert n > tc["cv"] + sum(int(r["orders"]) for r in ep if r["send_date"] >= "2026-10-05"), "store orders must cover platform claims"
assert store_rev > tc["va"] + ecur["rev"], "store revenue must cover platform claims"

# ---------- asserts: report is correct and the suspicious items look suspicious ----------
assert gc["cpa"] < gp["cpa"] * 0.93 and gc["cpa"] < TARGET_CPA, (gc["cpa"], gp["cpa"])
assert abs(tc["co"] / tp["co"] - 1) < 0.06
assert bc["ctr"] > 0.36
assert 0.92 < ga_cpc / tc["cl"] < 0.96
assert mean > median * 1.1, (mean, median)
assert ga_email < ecur["ck"]
assert all(0.0015 < float(r["unsubscribes"]) / int(r["delivered"]) < 0.003 for r in ep)

eur = lambda x: f"€{x:,.2f}"
eur0 = lambda x: f"€{x:,.0f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"
chg = lambda a, b: f"{100 * (a / b - 1):+.1f}%"

def line(lbl, a):
    return f"| {lbl} | {eur0(a['co'])} | {a['cl']:,} | {pc(a['ctr'])} | {eur(a['cpc'])} | {a['cv']} | {eur(a['cpa'])} | {a['roas']:.2f}x |"

report = f"""# Fernhill Garden Supply: Weekly Paid Search and Email Report

Week of 5 to 11 October 2026. Compared with the prior week (28 September to 4 October 2026) and the same week last year (6 to 12 October 2025).
Conversions are purchases only. All rates are totals divided by totals (for example CTR = total clicks / total impressions).

## Summary

**Generic search cost per purchase fell to {eur(gc['cpa'])}, from {eur(gp['cpa'])} the week before ({chg(gc['cpa'], gp['cpa'])}), on flat spend ({eur0(tc['co'])} vs {eur0(tp['co'])}). It is below our {eur0(TARGET_CPA)} target. Recommendation: keep budgets flat and check again on 2 November.**

## Google Ads, this week

| Segment | Cost | Clicks | CTR | CPC | Purchases | Cost per purchase | ROAS |
|---|---|---|---|---|---|---|---|
{line('Brand', bc)}
{line('Generic', gc)}
{line('Total', tc)}

| Generic, cost per purchase | Same week 2025 | Prior week | This week |
|---|---|---|---|
| | {eur(gl['cpa'])} | {eur(gp['cpa'])} | {eur(gc['cpa'])} |

- Brand CTR of {pc(bc['ctr'])} is normal for people searching our own name. We report brand separately so it does not flatter the generic numbers, and we do not read it as a reason to add brand budget.
- The generic improvement coincides with the negative keyword list added on 30 September. One week is not enough to say the list caused it; we will judge it on the four weeks to 2 November.
- Google Ads recorded {tc['cl']:,} clicks this week and GA4 recorded {ga_cpc:,} google / cpc sessions ({pc(1 - ga_cpc / tc['cl'])} fewer). A gap of 5-10% is typical (consent banners, ad blockers, people leaving before the page loads), so we have not treated it as a tracking issue; if it widens past 10% we will check the tags.

## Email

| | Prior week (2 sends) | This week (2 sends) |
|---|---|---|
| Delivered | {eprev['dl']:,} | {ecur['dl']:,} |
| Unique clicks | {eprev['ck']:,} | {ecur['ck']:,} |
| Click rate (clicks / delivered) | {pc(eprev['cr'], 2)} | {pc(ecur['cr'], 2)} |
| Click-to-open rate | {pc(eprev['ctor'])} | {pc(ecur['ctor'])} |
| Unsubscribe rate | {pc(eprev['us'], 2)} | {pc(ecur['us'], 2)} |
| Revenue from sessions tagged to the send | {eur0(eprev['rev'])} | {eur0(ecur['rev'])} |

Click rate moved from {pc(eprev['cr'], 2)} to {pc(ecur['cr'], 2)}. Unsubscribe rates sit in the normal 0.1-0.4% band. GA4 recorded {ga_email:,} newsletter sessions against {ecur['ck']:,} unique clicks; sessions running slightly under clicks is expected.

## Orders

{n} orders this week. **Median order value {eur(median)}**; the mean is {eur(mean)} because a few large orders (the two largest were {eur(1249)} and {eur(1189)}) pull it up. We use the median as the typical order.

## Recommendations

1. Keep Google Ads budgets flat. Check: generic cost per purchase stays under {eur0(TARGET_CPA)} over the four weeks to 2 November (Google Ads, purchases only).
2. Keep the negative keyword list and review the search terms report again on 2 November.
3. Keep the email schedule unchanged. Check: click rate per send stays above 2% and unsubscribe rate under 0.4% through October.
"""

files = {
    "resources/weekly_report_wk41.md": report,
    "resources/google_ads_weekly.csv": ads_csv,
    "resources/email_sends.csv": em_csv,
    "resources/ga4_sessions_wk41.csv": ga_csv,
    "resources/shopify_orders_wk41.csv": ord_csv,
}

prompt = """
Here's our weekly paid search and email report (resources/weekly_report_wk41.md), plus the Google Ads, email, GA4 and Shopify exports it's based on. Can you check it before I send it to my boss? If there's anything wrong I'd rather know now. Write report.md with your verdict and anything I need to change.
"""

g_clean = f"""
This report is correct. Every figure recomputes from the exports: rates are totals divided by totals, conversions are purchases only, brand and generic are split, comparisons are to the prior week and the same week last year, causal statements are hedged, and each recommendation names the metric and the date to check.

PASS if report.md's verdict says the report can be sent (as is, or with optional wording or presentation changes), and it raises no finding that a number is wrong or that a conclusion does not follow from the data (no Must-fix / critical / blocking finding about the numbers or the conclusions).
FAIL if the verdict says not to send it, or says it must be fixed first, or report.md lists any Must-fix / critical problem.
"""

g_nofalse = f"""
These figures and statements in the report are correct. report.md must not claim any of them is wrong:
- Generic cost per purchase this week {eur(gc['cpa'])} (cost {eur(gc['co'])} / {gc['cv']} purchases), prior week {eur(gp['cpa'])}, same week 2025 {eur(gl['cpa'])}.
- Total cost {eur(tc['co'])} vs prior week {eur(tp['co'])}; total CTR {pc(tc['ctr'])} ({tc['cl']:,} / {tc['im']:,}).
- Brand CTR {pc(bc['ctr'])}: normal for brand search, reported separately.
- GA4 google / cpc sessions {ga_cpc:,} vs {tc['cl']:,} clicks ({pc(1 - ga_cpc / tc['cl'])} fewer): within the typical range, and the report says so with a stated threshold for checking the tags.
- Email click rate this week {pc(ecur['cr'], 2)} ({ecur['ck']:,} / {ecur['dl']:,}), prior week {pc(eprev['cr'], 2)}; newsletter sessions slightly under clicks: normal.
- Median order value {eur(median)} with mean {eur(mean)} pulled up by a few large orders: correctly labelled and correctly used.\n- Store orders this week {n} (all channels) cover both Google Ads' {tc['cv']} purchases and email's tagged orders: no reconciliation problem.
- "Coincides with the negative keyword list ... one week is not enough to say the list caused it": correctly hedged.

PASS if report.md does not say any of these numbers is wrong or any of these statements is a problem to fix. Minor optional suggestions (wording, extra context) are fine.
FAIL if report.md says any listed number is miscalculated, calls the brand CTR, the clicks vs sessions gap, the sessions under email clicks, or the median vs mean a problem, or says the causal statement is unsupported.
"""

g_verify = f"""
PASS if report.md shows it checked the report against the data: it states at least two specific figures it recomputed or confirmed from the exports (for example generic cost per purchase {eur(gc['cpa'])}, total CTR {pc(tc['ctr'])}, email click rate {pc(ecur['cr'], 2)}, median order value {eur(median)}), and those figures agree with the report (within rounding).
FAIL if it confirms no specific figure from the data, or the figures it gives disagree with these values.
"""

write_case(NAME, files, prompt, [("called-clean", 3, g_clean), ("no-false-findings", 2, g_nofalse), ("verified-numbers", 1, g_verify)])
print(f"{NAME}: generic CPA {gc['cpa']:.2f} (prev {gp['cpa']:.2f}, LY {gl['cpa']:.2f}); cost {tc['co']:.0f} vs {tp['co']:.0f}; "
      f"brand CTR {bc['ctr']:.3f}; ga/clicks {ga_cpc}/{tc['cl']}; email CR {ecur['cr']:.4f} vs {eprev['cr']:.4f}; median {median:.2f} mean {mean:.2f}")
