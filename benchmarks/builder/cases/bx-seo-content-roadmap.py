"""Breadth: SEO content roadmap for next quarter (Kettle & Kiln Coffee, Q3 2026 data).

Planted problems (5): agency roadmap ranked by search volume puts the
informational descaling hub first while the commercial grinder cluster
(positions 11-16, ~8-9% paid CVR) sits fourth (DECISION); descaling demand
sized by summing query+page rows (two own pages show, double count =
cannibalisation); a new "best burr grinder for espresso" page proposed while an
existing guide already ranks ~9 for it (deepen, do not build); the burr-grinder
explainer is the page collecting the buying queries at page two while the
/shop/grinders category page does not rank for them; "milk frothing jug" earns
paid conversions with no organic footing at all.
Decoys (2): GSC clicks above GA4 organic sessions; brand queries at 35-50% CTR."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-seo-content-roadmap"
rng = random.Random(81101)
AOV = 142.0

# query: (impressions, ctr, position, cluster)
Q = {
    "kettle and kiln": (8200, 0.47, 1.0, "brand"),
    "kettle & kiln coffee": (2900, 0.41, 1.1, "brand"),
    "kettleandkiln": (650, 0.38, 1.2, "brand"),
    "how to descale espresso machine": (14600, 0.061, 3.8, "descale"),
    "espresso machine descaler": (6100, 0.034, 6.2, "descale"),
    "descaling espresso machine with vinegar": (4300, 0.052, 4.4, "descale"),
    "how often to descale espresso machine": (3700, 0.058, 3.6, "descale"),
    "descale coffee machine citric acid": (2300, 0.041, 5.9, "descale"),
    "burr grinder sale": (3100, 0.0085, 13.4, "grinder_buy"),
    "buy burr grinder": (2200, 0.0090, 12.1, "grinder_buy"),
    "espresso grinder sale": (1900, 0.0080, 14.8, "grinder_buy"),
    "flat burr grinder price": (1500, 0.0075, 15.6, "grinder_buy"),
    "conical burr grinder buy": (1100, 0.0095, 11.7, "grinder_buy"),
    "what is a burr grinder": (5400, 0.072, 3.1, "grinder_info"),
    "burr vs blade grinder": (4800, 0.066, 3.9, "grinder_info"),
    "best burr grinder for espresso": (4200, 0.021, 9.2, "grinder_best"),
    "latte art tips": (7600, 0.031, 6.8, "latte"),
    "latte art for beginners": (4500, 0.028, 7.9, "latte"),
    "espresso tamper": (2600, 0.024, 8.4, "other"),
    "single origin espresso beans": (3900, 0.019, 10.6, "other"),
    "coffee bean storage": (2800, 0.047, 4.8, "other"),
}
QD, qrows = {}, []
for q, (imps0, ctr, pos, cl) in Q.items():
    imps = int(imps0 * rng.uniform(0.97, 1.03))
    clicks = int(round(imps * ctr * rng.uniform(0.95, 1.05)))
    p = round(pos * rng.uniform(0.98, 1.02), 1)
    QD[q] = dict(imps=imps, clicks=clicks, pos=p, cl=cl)
    qrows.append([q, clicks, imps, round(clicks / imps, 4), p])

def cl(name):
    return [q for q in QD if QD[q]["cl"] == name]

# ---------- query+page rows ----------
qp = []
for q in cl("brand"):
    qp.append([q, "/", QD[q]["clicks"], QD[q]["imps"], QD[q]["pos"]])
desc_sum = 0
for q in cl("descale"):
    d = QD[q]
    a_imps = d["imps"]
    b_imps = int(d["imps"] * rng.uniform(0.62, 0.70))
    a_cl = int(round(d["clicks"] * 0.82)); b_cl = d["clicks"] - a_cl
    qp.append([q, "/guides/descaling-your-espresso-machine", a_cl, a_imps, d["pos"]])
    qp.append([q, "/blog/descale-tips-for-home-baristas", b_cl, b_imps, round(d["pos"] + rng.uniform(4.5, 6.5), 1)])
    desc_sum += a_imps + b_imps
for q in cl("grinder_buy"):
    d = QD[q]
    qp.append([q, "/blog/what-is-a-burr-grinder", d["clicks"], d["imps"], d["pos"]])
for q in cl("grinder_info"):
    d = QD[q]
    qp.append([q, "/blog/what-is-a-burr-grinder", d["clicks"], d["imps"], d["pos"]])
d = QD["best burr grinder for espresso"]
qp.append(["best burr grinder for espresso", "/guides/grinder-buying-guide", d["clicks"], d["imps"], d["pos"]])
for q in cl("latte"):
    qp.append([q, "/guides/latte-art", QD[q]["clicks"], QD[q]["imps"], QD[q]["pos"]])
for q, page in [("espresso tamper", "/shop/accessories/tampers"), ("single origin espresso beans", "/shop/beans/single-origin"),
                ("coffee bean storage", "/blog/storing-coffee-beans")]:
    qp.append([q, page, QD[q]["clicks"], QD[q]["imps"], QD[q]["pos"]])
qp.sort(key=lambda r: -r[3])
qp_pages = {r[1] for r in qp}

desc_q = sum(QD[q]["imps"] for q in cl("descale"))
desc_overlap = desc_sum - desc_q
gb_imps = sum(QD[q]["imps"] for q in cl("grinder_buy"))
gb_pos = sum(QD[q]["imps"] * QD[q]["pos"] for q in cl("grinder_buy")) / gb_imps
gb_ctr = sum(QD[q]["clicks"] for q in cl("grinder_buy")) / gb_imps
latte_imps = sum(QD[q]["imps"] for q in cl("latte"))

# ---------- paid search terms, Q3 ----------
# term: (clicks, cpc, cvr)
P = {
    "how to descale espresso machine": (820, 0.38, 0.0049),
    "espresso machine descaler": (640, 0.55, 0.0094),
    "descaling espresso machine with vinegar": (310, 0.31, 0.0),
    "burr grinder sale": (540, 1.15, 0.091),
    "buy burr grinder": (470, 1.22, 0.087),
    "espresso grinder sale": (390, 1.08, 0.082),
    "flat burr grinder price": (260, 1.31, 0.077),
    "best burr grinder for espresso": (450, 0.94, 0.031),
    "latte art tips": (280, 0.29, 0.0036),
    "milk frothing jug": (2150, 0.62, 0.065),
    "milk jug for latte art": (720, 0.58, 0.058),
    "espresso tamper": (380, 0.71, 0.047),
    "kettle and kiln": (1900, 0.21, 0.112),
}
prow, PD = [], {}
for t, (c0, cpc, cvr) in P.items():
    c = int(c0 * rng.uniform(0.96, 1.04))
    cost = round(c * cpc * rng.uniform(0.95, 1.05), 2)
    conv = int(round(c * cvr))
    val = round(conv * AOV * rng.uniform(0.9, 1.1), 2)
    imps = int(c / rng.uniform(0.05, 0.09))
    PD[t] = dict(c=c, conv=conv)
    prow.append([t, imps, c, cost, conv, val])
def pcvr(ts):
    return sum(PD[t]["conv"] for t in ts) / sum(PD[t]["c"] for t in ts)
desc_terms = [t for t in P if "descal" in t]
gb_terms = ["burr grinder sale", "buy burr grinder", "espresso grinder sale", "flat burr grinder price"]
desc_cvr, gb_cvr = pcvr(desc_terms), pcvr(gb_terms)
jug_conv = PD["milk frothing jug"]["conv"] + PD["milk jug for latte art"]["conv"]
jug_in_gsc = any("jug" in q for q in QD)

# value if moved to a top-3 CTR of ~10%: impressions x 10% x paid CVR
val_desc = desc_q * 0.10 * desc_cvr
val_gb = gb_imps * 0.10 * gb_cvr

# ---------- GA4 organic landing pages ----------
gsc_clicks_total = sum(d["clicks"] for d in QD.values()) + 6100  # long tail not in the top-queries export
ga_org = int(gsc_clicks_total * rng.uniform(0.89, 0.92))

# ---------- asserts ----------
assert desc_sum / desc_q > 1.55, (desc_sum, desc_q)
assert 10.5 < gb_pos < 16 and gb_ctr < 0.012
assert gb_cvr > 8 * desc_cvr, (gb_cvr, desc_cvr)
assert val_gb > 3 * val_desc, (val_gb, val_desc)
assert desc_q > 3 * gb_imps
assert not jug_in_gsc and jug_conv > 120
assert "/shop/grinders" not in qp_pages
assert gsc_clicks_total > ga_org * 1.07
assert all(QD[q]["clicks"] / QD[q]["imps"] > 0.33 for q in cl("brand"))

pc = lambda x, d=1: f"{100 * x:.{d}f}%"

roadmap = f"""# Kettle & Kiln Coffee: Q4 2026 SEO content roadmap (draft from our agency)

Ranked by search demand (Search Console impressions, Q3 2026).

| Rank | Initiative | Q3 demand (impressions) | Type |
|---|---|---|---|
| 1 | Descaling hub: new pillar page plus 4 supporting articles, link building to /guides/descaling-your-espresso-machine | {desc_sum:,} | Build |
| 2 | Latte art guide expansion (video, step photos) | {latte_imps:,} | Expand |
| 3 | New page: "Best burr grinder for espresso 2026" | {QD['best burr grinder for espresso']['imps']:,} | Build |
| 4 | Grinder category page (/shop/grinders) meta refresh | {gb_imps:,} | Refresh |
| 5 | Coffee bean storage refresh | {QD['coffee bean storage']['imps']:,} | Refresh |

Notes from the agency:
- Descaling demand is the sum of impressions across all descaling rows in the query+page export.
- Search Console shows {gsc_clicks_total:,} organic clicks in Q3 against {ga_org:,} GA4 organic sessions.
- Brand queries ("kettle and kiln" and variants) are excluded from the roadmap.
"""

notes = f"""# Notes

- Kettle & Kiln sells espresso machines, grinders, accessories and beans online. Average order value about ${AOV:.0f}.
- One content writer and about 10 days a month of agency time in Q4.
- Exports are Q3 2026 (July to September). Search Console top queries are the queries with 500+ impressions; the long tail is not in the file.
"""

files = {
    "resources/notes.md": notes,
    "resources/agency_roadmap_q4.md": roadmap,
    "resources/gsc_queries_q3.csv": to_csv(["query", "clicks", "impressions", "ctr", "position"], qrows),
    "resources/gsc_query_page_q3.csv": to_csv(["query", "page", "clicks", "impressions", "position"], qp),
    "resources/google_ads_search_terms_q3.csv": to_csv(["search_term", "impressions", "clicks", "cost", "conversions", "conversion_value"], prow),
}

prompt = """
Our agency sent over the Q4 SEO content roadmap (resources/agency_roadmap_q4.md) and I have to sign it off this week. I've added our Search Console and Google Ads exports and a few notes. Where should our content effort go next quarter? Please write your recommendation in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Roadmap ranked by volume, not by what converts. The descaling cluster (informational) converts at about {pc(desc_cvr, 2)} in paid search, the grinder buying cluster ("burr grinder sale", "buy burr grinder", "espresso grinder sale", "flat burr grinder price") at about {pc(gb_cvr)}. Counts as found if report.md uses the paid conversion rates (or another conversion signal) to say the descaling hub is low value per impression and the grinder buying terms are worth more.
2. Descaling demand double counted. The roadmap's {desc_sum:,} impressions sum the query+page rows, where two own pages (/guides/descaling-your-espresso-machine and /blog/descale-tips-for-home-baristas) show for the same searches. Query-level demand is {desc_q:,}; the {desc_overlap:,} gap is overlap, i.e. the two pages cannibalise each other. Counts as found if report.md gives roughly {desc_q:,} (within 5%) as the real demand or says the {desc_sum:,} double counts, or flags the two descaling pages competing.
3. Build vs deepen. Roadmap item 3 builds a new "best burr grinder for espresso" page, but /guides/grinder-buying-guide already ranks about {QD['best burr grinder for espresso']['pos']} for that query. Counts as found if report.md says to improve the existing guide rather than build a competing page (or warns the new page would cannibalise it).
4. Wrong page ranking for buying queries. The grinder buying queries are answered by /blog/what-is-a-burr-grinder (an explainer) at positions about 11-16, average {gb_pos:.1f}, CTR {pc(gb_ctr, 2)}; /shop/grinders does not appear in the query+page export at all. Counts as found if report.md notes that the explainer, not the category or product page, is the page ranking for these buying terms and that the category page should be pointed at them.
5. Paid converter with no organic footing. "milk frothing jug" and "milk jug for latte art" bring {jug_conv} paid conversions in Q3 and no jug query appears in Search Console. Counts as found if report.md flags this as a content or category-page gap.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with its evidence (a number, query or page).
FAIL if fewer than 3.
"""

g_decision = f"""
The correct top recommendation: make the grinder buying cluster the first priority, by pointing /shop/grinders (or grinder product pages) at the buying queries ("burr grinder sale", "buy burr grinder" and similar), which sit at positions about 11-16 with {gb_imps:,} impressions and a paid conversion rate of about {pc(gb_cvr)}. Rough value at a 10% CTR: about {val_gb:.0f} orders a quarter for the grinder cluster against about {val_desc:.0f} for the whole descaling cluster.

The naive answer is to accept the agency order and lead with the descaling hub ({desc_sum:,} "impressions", conversion rate about {pc(desc_cvr, 2)}) or to build new pages.

PASS if report.md's main or first recommendation is to prioritise the commercial grinder terms (category or product page optimisation, moving item 4 up, or equivalent) over the descaling hub.
FAIL if the main recommendation is to sign off the roadmap as ranked, to lead with the descaling hub or latte art guide, or to build the new "best burr grinder" page first.
"""

g_decoy = f"""
Two things in the exports look odd but are fine and must not be presented as problems:
- D1. Search Console clicks ({gsc_clicks_total:,}) are higher than GA4 organic sessions ({ga_org:,}). Different systems (Google counts the click; GA4 needs a consented, loaded tag); a gap of about 10% is normal.
- D2. Brand queries ("kettle and kiln" and variants) have CTRs of about 38-50% at position 1. That is normal for brand searches.

PASS if report.md does not present D1 as lost traffic or a tracking problem to fix, and does not present the brand CTRs as an anomaly or error. Mentioning either as normal is fine.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: descale q {desc_q} summed {desc_sum} cvr {desc_cvr:.4f}; grinder buy {gb_imps} pos {gb_pos:.1f} cvr {gb_cvr:.3f}; "
      f"value {val_gb:.0f} vs {val_desc:.0f}; jug conv {jug_conv}; gsc {gsc_clicks_total} ga {ga_org}")
