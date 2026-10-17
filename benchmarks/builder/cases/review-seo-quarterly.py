"""Review a quarterly organic search report (Alder & Pine Home, Q3 2026 plus the
first two weeks of October).

Planted problems (5): "organic down 3x% this week, emergency" built on the
last 3 days that Search Console has not finished reporting (MUST); the top
guide page by sessions celebrated ("double down on guides") though it barely
converts, while a high-converting product page with few sessions sits on the
CRO rewrite list (MUST); linen cluster CTR as the mean of query CTRs;
demand for "linen duvet cover" sized by summing query+page impressions; a
position-2 query with ~1% CTR bucketed "defend, build links".
Decoys (2): GSC clicks above GA4 organic sessions, explained as normal;
linen cluster average position printed impression-weighted (recomputes)."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "review-seo-quarterly"
rng = random.Random(55023)

# ---------- GSC daily: 1 Jul to 13 Oct 2026; last 3 days not fully reported ----------
start = dt.date(2026, 7, 1)
end = dt.date(2026, 10, 13)
LAG = {dt.date(2026, 10, 11): 0.22, dt.date(2026, 10, 12): 0.30, dt.date(2026, 10, 13): 0.38}
WEEKDAY = [1.06, 1.08, 1.05, 1.02, 0.94, 0.88, 0.97]
daily, D = [], {}
d = start
while d <= end:
    base = 1240 * WEEKDAY[d.weekday()] * rng.uniform(0.96, 1.04)
    clicks = int(round(base * LAG.get(d, 1.0)))
    imps = int(round(clicks / rng.uniform(0.031, 0.035)))
    daily.append([d.isoformat(), clicks, imps])
    D[d] = clicks
    d += dt.timedelta(days=1)
q3_clicks = sum(c for dd, c in D.items() if dd.month in (7, 8, 9))
this_week = [dt.date(2026, 10, 7) + dt.timedelta(days=i) for i in range(7)]
last_week = [x - dt.timedelta(days=7) for x in this_week]
tw, lw = sum(D[x] for x in this_week), sum(D[x] for x in last_week)
wk_change = tw / lw - 1                                                  # planted
comp_tw = sum(D[x] for x in this_week[:4]); comp_lw = sum(D[x] for x in last_week[:4])
like_change = comp_tw / comp_lw - 1                                      # truth (7-10 Oct vs 30 Sep-3 Oct)

# ---------- GSC queries ----------
# query: (impressions, ctr, position)
Q = {
    "linen bedding": (47800, 0.011, 2.4),
    "linen duvet cover": (10300, 0.064, 4.6),
    "linen sheets": (22600, 0.048, 5.3),
    "how to care for linen": (61000, 0.071, 1.8),
    "how to wash linen sheets": (24000, 0.062, 2.9),
    "linen pillowcases": (8700, 0.039, 7.2),
    "stonewashed linen bedding": (3100, 0.052, 6.1),
    "linen bedding uk": (2400, 0.044, 8.4),
    "alder and pine linen": (420, 0.62, 1.1),
    "linen duvet cover king size": (180, 0.21, 3.9),
    "washed linen fitted sheet 160x200": (60, 0.30, 4.4),
    "linen quilt cover sage": (45, 0.27, 5.2),
    "oak bedside table": (14200, 0.031, 9.8),
    "wooden bed frame": (26500, 0.018, 12.4),
    "alder and pine": (9100, 0.48, 1.0),
    "alder & pine home": (2600, 0.51, 1.0),
    "wool throw blanket": (11800, 0.027, 8.9),
    "ceramic table lamp": (7400, 0.022, 11.3),
    "jute rug": (19300, 0.014, 14.6),
    "cotton waffle towels": (6800, 0.036, 6.7),
}
qrows, QD = [], {}
for q, (imps0, ctr, pos) in Q.items():
    imps = int(imps0 * rng.uniform(0.97, 1.03))
    clicks = int(round(imps * ctr * rng.uniform(0.95, 1.05)))
    p = round(pos * rng.uniform(0.97, 1.03), 1)
    QD[q] = dict(imps=imps, clicks=clicks, pos=p)
    qrows.append([q, clicks, imps, round(clicks / imps, 4), p])
linen = [q for q in Q if "linen" in q and not q.startswith("alder")]
lin_ctr_mean = sum(QD[q]["clicks"] / QD[q]["imps"] for q in linen) / len(linen)          # planted
lin_ctr_true = sum(QD[q]["clicks"] for q in linen) / sum(QD[q]["imps"] for q in linen)
lin_pos_w = sum(QD[q]["pos"] * QD[q]["imps"] for q in linen) / sum(QD[q]["imps"] for q in linen)  # decoy, correct
lin_pos_mean = sum(QD[q]["pos"] for q in linen) / len(linen)

# ---------- GSC query+page for "linen duvet cover" (two own pages show) ----------
ldc = QD["linen duvet cover"]
both = int(ldc["imps"] * 0.64)            # searches where both pages showed
p1_imps = ldc["imps"]                     # duvet cover page shows on (nearly) every search
p2_imps = both                            # the guide shows on part of them
p1_clicks = int(round(ldc["clicks"] * 0.86)); p2_clicks = ldc["clicks"] - p1_clicks
qp_rows = [["linen duvet cover", "/bedding/linen-duvet-covers", p1_clicks, p1_imps, round(ldc["pos"], 1)],
           ["linen duvet cover", "/journal/linen-bedding-buying-guide", p2_clicks, p2_imps, round(ldc["pos"] + 6.3, 1)],
           ["linen bedding", "/bedding/linen", QD["linen bedding"]["clicks"], QD["linen bedding"]["imps"], QD["linen bedding"]["pos"]],
           ["how to care for linen", "/journal/how-to-care-for-linen", QD["how to care for linen"]["clicks"], QD["how to care for linen"]["imps"], QD["how to care for linen"]["pos"]]]
ldc_summed = p1_imps + p2_imps            # planted demand

# ---------- GA4 organic landing pages, Q3 ----------
# page: (share of sessions, cvr, aov)
LP = {
    "/journal/how-to-care-for-linen": (0.100, 0.0012, 120),
    "/": (0.095, 0.018, 165),
    "/bedding/linen": (0.080, 0.021, 190),
    "/journal/linen-bedding-buying-guide": (0.060, 0.004, 150),
    "/furniture/bed-frames": (0.075, 0.012, 640),
    "/bedding/linen-sheets": (0.065, 0.024, 170),
    "/furniture/bedside-tables": (0.050, 0.014, 310),
    "/bath/waffle-towels": (0.040, 0.019, 85),
    "/bedding/linen-duvet-covers": (0.0085, 0.036, 210),
    "(other)": (0.4265, 0.011, 140),
}
ga_sessions_total = int(q3_clicks * 0.905)
lp_rows, L = [], {}
for page, (share, cvr, aov) in LP.items():
    s = int(round(ga_sessions_total * share))
    eng = int(round(s * rng.uniform(0.52, 0.68)))
    tr = max(1, int(round(s * cvr)))
    rev = round(tr * aov * rng.uniform(0.95, 1.05), 2)
    L[page] = dict(s=s, tr=tr, rev=rev)
    lp_rows.append([page, s, eng, tr, rev])
ga_total = sum(v["s"] for v in L.values())
site_cvr = sum(v["tr"] for v in L.values()) / ga_total
guide, duvet = L["/journal/how-to-care-for-linen"], L["/bedding/linen-duvet-covers"]
guide_cvr, duvet_cvr = guide["tr"] / guide["s"], duvet["tr"] / duvet["s"]

lb = QD["linen bedding"]

# ---------- asserts ----------
assert wk_change < -0.28, wk_change
assert abs(like_change) < 0.05, like_change
assert lin_ctr_mean / lin_ctr_true > 2.0, (lin_ctr_mean, lin_ctr_true)
assert ldc_summed / ldc["imps"] > 1.5
assert lb["pos"] < 3 and lb["clicks"] / lb["imps"] < 0.015 and lb["imps"] > 40000
assert max((p for p in L if p != "(other)"), key=lambda p: L[p]["s"]) == "/journal/how-to-care-for-linen"
assert guide_cvr < site_cvr / 5 and duvet_cvr > 2 * site_cvr and duvet["s"] < guide["s"] / 10
assert q3_clicks > ga_total * 1.05
assert abs(lin_pos_w - lin_pos_mean) > 0.5   # weighting matters, and the report used the weighted one

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x: f"€{x:,.0f}"

artefact = f"""# Alder & Pine Home: Organic Search Report, Q3 2026

Prepared 14 October 2026 by the content and SEO team. Sources: Google Search Console and GA4.

## Headlines

- **Urgent: organic clicks fell {pc(-wk_change, 0)} this week** ({tw:,} clicks, 7-13 October, against {lw:,} the week before). We recommend pausing the content calendar and bringing in an SEO agency for a penalty audit this month.
- Q3 organic clicks: {q3_clicks:,}.
- Our best organic page is **/journal/how-to-care-for-linen**, with {guide['s']:,} sessions in Q3, more than any other page. Guides work: we will double down and write eight more care guides in Q4.

## Linen cluster

| Metric | Q3 |
|---|---|
| Queries in cluster | {len(linen)} |
| Clicks | {sum(QD[q]['clicks'] for q in linen):,} |
| Impressions | {sum(QD[q]['imps'] for q in linen):,} |
| CTR | {pc(lin_ctr_mean)} |
| Average position (weighted by impressions) | {lin_pos_w:.1f} |

The linen cluster CTR of {pc(lin_ctr_mean)} is well above the site average, so the cluster is in good shape.

**Demand for "linen duvet cover"**: {ldc_summed:,} impressions in Q3 across our pages ({p1_imps:,} on /bedding/linen-duvet-covers plus {p2_imps:,} on /journal/linen-bedding-buying-guide). That is the size of the opportunity for the duvet range.

## Query priorities

| Query | Impressions | CTR | Position | Bucket |
|---|---|---|---|---|
| linen bedding | {lb['imps']:,} | {pc(lb['clicks'] / lb['imps'])} | {lb['pos']} | Defend: already top 3, build links to hold the position |
| linen sheets | {QD['linen sheets']['imps']:,} | {pc(QD['linen sheets']['clicks'] / QD['linen sheets']['imps'])} | {QD['linen sheets']['pos']} | Push: content refresh |
| wooden bed frame | {QD['wooden bed frame']['imps']:,} | {pc(QD['wooden bed frame']['clicks'] / QD['wooden bed frame']['imps'])} | {QD['wooden bed frame']['pos']} | Push: new buying guide |

## Conversion

Organic sessions converted at {pc(site_cvr, 2)} in Q3. The duvet cover page (/bedding/linen-duvet-covers) had only {duvet['s']:,} sessions, so it goes on the CRO list for a full page rewrite in November.

## Tracking note

Search Console shows {q3_clicks:,} organic clicks for Q3 and GA4 shows {ga_total:,} organic sessions. The two count different things in different systems (a click on Google's results page versus a consented, tagged session on our site), so they will never match and we do not try to reconcile them.

## Recommendations

1. Pause the content calendar and commission a penalty audit.
2. Write eight more care guides in Q4.
3. Build links to /bedding/linen to defend the linen bedding ranking.
4. Rewrite the duvet cover page in November.
"""

files = {
    "resources/organic_search_report_q3_2026.md": artefact,
    "resources/gsc_daily_2026-07-01_2026-10-13.csv": to_csv(["date", "clicks", "impressions"], daily),
    "resources/gsc_queries_q3_2026.csv": to_csv(["query", "clicks", "impressions", "ctr", "position"], qrows),
    "resources/gsc_query_pages_q3_2026.csv": to_csv(["query", "page", "clicks", "impressions", "position"], qp_rows),
    "resources/ga4_organic_landing_pages_q3_2026.csv": to_csv(
        ["landing_page", "sessions", "engaged_sessions", "transactions", "purchase_revenue"], lp_rows),
}

prompt = """
Our SEO team's quarterly report is in resources/organic_search_report_q3_2026.md, with the Search Console and GA4 exports behind it in resources/. It asks for an agency budget and a Q4 content plan, so I want to be sure it's right before it goes to the leadership meeting. Can you check it and tell me in report.md whether it holds up and what needs fixing?
"""

g_recall = f"""
The report under review (organic_search_report_q3_2026.md) contains 5 planted problems. Answer key:

1. False "crash" from reporting lag. "Organic clicks fell {pc(-wk_change, 0)} this week" compares 7-13 Oct ({tw:,}) with 30 Sep-6 Oct ({lw:,}), but the last three days (11, 12, 13 Oct: {D[dt.date(2026, 10, 11)]}, {D[dt.date(2026, 10, 12)]}, {D[dt.date(2026, 10, 13)]} clicks against about 1,100-1,350 on normal days) are not fully reported yet; Search Console lags 2-3 days. Comparing the complete days (7-10 Oct vs 30 Sep-3 Oct) gives {comp_tw:,} vs {comp_lw:,} ({'+' if like_change >= 0 else ''}{pc(like_change)}), essentially flat. Counts as found if report.md says the drop is in the last 2-3 days / reporting lag (or that like-for-like days are flat) and the penalty audit is not justified.
2. Wrong page celebrated, starved winner rewritten. /journal/how-to-care-for-linen has the most sessions ({guide['s']:,}) but converts at {pc(guide_cvr, 2)} ({guide['tr']} transactions) against a site organic rate of {pc(site_cvr, 2)}; /bedding/linen-duvet-covers converts at {pc(duvet_cvr, 2)} on only {duvet['s']:,} sessions and is put on the CRO rewrite list. The guide page needs links into product pages (it does not sell), and the duvet page needs more traffic, not a rewrite. Counts as found if report.md flags either half with numbers: the guide's very low conversion (so "double down on guides" is not supported by revenue) or the duvet page's high conversion (so it should get traffic, not a rewrite). Both halves is ideal; one with numbers counts.
3. Averaged cluster CTR. The linen cluster CTR {pc(lin_ctr_mean)} is the mean of the {len(linen)} query CTRs, inflated by tiny long-tail queries; total clicks / total impressions = {pc(lin_ctr_true)}. Counts as found if report.md gives a cluster CTR within 0.3 points of {pc(lin_ctr_true)} or says the figure is an average of query rates that must be recomputed from totals.
4. Demand double counted. "Linen duvet cover" demand of {ldc_summed:,} adds query+page rows; when two of our pages show for one search, each logs an impression. Query-level impressions are {ldc['imps']:,}. The overlap ({p2_imps:,}) is a sign the buying guide competes with the product page (cannibalisation). Counts as found if report.md gives demand of about {ldc['imps']:,} or says the page rows double count.
5. Snippet problem bucketed as "defend, build links". "linen bedding" ranks at position {lb['pos']} with {lb['imps']:,} impressions but only {pc(lb['clicks'] / lb['imps'])} CTR; a top-three result normally gets well above 10%. The fix is the title and meta description (snippet), not links. Counts as found if report.md flags the low CTR at a top-3 position and recommends a title/snippet rewrite instead of (or before) link building.

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention does not count).
FAIL if it identifies fewer than 4.
"""

g_rank = f"""
Two of the problems are Must-fix because they drive the report's money decisions:
- A. The "{pc(-wk_change, 0)} crash this week" that triggers pausing the content calendar and paying for a penalty audit; it comes from the last 2-3 days of Search Console data not being fully reported (complete days are flat, {'+' if like_change >= 0 else ''}{pc(like_change)}).
- B. The Q4 plan to "double down" on care guides because /journal/how-to-care-for-linen has the most sessions, while it converts at {pc(guide_cvr, 2)} (vs {pc(site_cvr, 2)} site), and the {pc(duvet_cvr, 2)}-converting duvet cover page is sent for a rewrite.
The lesser problems are: the averaged cluster CTR, the double-counted duvet demand, and the "linen bedding" snippet bucketed as link building.

PASS if report.md flags both A and B (for B, either half with its numbers is enough), places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the report can go out as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves the report unchanged.
"""

g_decoy = f"""
The report contains two statements that are correct and must not be flagged:
- D1. Search Console Q3 clicks ({q3_clicks:,}) are higher than GA4 organic sessions ({ga_total:,}), and the report says the two will not match and does not reconcile them. That is correct: they are different events in different systems.
- D2. The linen cluster average position {lin_pos_w:.1f} is labelled as weighted by impressions, and it is: the impression-weighted mean of the cluster's query positions is {lin_pos_w:.1f} (a simple mean of the rows would be {lin_pos_mean:.1f}).

PASS if report.md does not present D1 or D2 as an error or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it calls the clicks vs sessions gap lost traffic or a tracking problem, or says the {lin_pos_w:.1f} position is wrong.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: week {wk_change:.3f} vs like-for-like {like_change:.3f}; cluster CTR mean {lin_ctr_mean:.4f} vs {lin_ctr_true:.4f}; "
      f"ldc demand {ldc_summed} vs {ldc['imps']}; guide cvr {guide_cvr:.4f} duvet {duvet_cvr:.4f} site {site_cvr:.4f}; "
      f"pos w {lin_pos_w:.2f} vs mean {lin_pos_mean:.2f}")
