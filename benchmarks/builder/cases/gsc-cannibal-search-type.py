import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

# Harbor Outdoor Search Console, Q3 2026. Two exports:
#  - gsc_query_page.csv: query x page x search_type rows. For most "hiking boots" queries two
#    pages rank (collection + blog post), so summing page rows double counts impressions.
#  - gsc_query.csv: query x search_type rows (impressions counted once per search).
# Image results add lots of low-CTR impressions. Truth: query-level, web-only.
NAME = "gsc-cannibal-search-type"
rng = random.Random(4404)

COLL = "https://www.harboroutdoor.com/collections/hiking-boots"
BLOG = "https://www.harboroutdoor.com/blog/best-hiking-boots-2026"
TOPIC = [
    "hiking boots", "best hiking boots", "waterproof hiking boots", "womens hiking boots", "mens hiking boots",
    "lightweight hiking boots", "hiking boots for wide feet", "leather hiking boots", "best waterproof hiking boots",
    "hiking boots vs trail runners", "cheap hiking boots", "hiking boots sale", "winter hiking boots",
    "ankle support hiking boots", "vegan hiking boots", "how to break in hiking boots", "hiking boots size guide",
    "best hiking boots for beginners", "mid hiking boots", "hiking boot laces",
]
OTHER = [("rain jacket", "https://www.harboroutdoor.com/collections/rain-jackets"),
         ("packable rain jacket", "https://www.harboroutdoor.com/collections/rain-jackets"),
         ("2 person tent", "https://www.harboroutdoor.com/collections/tents"),
         ("camping tent sale", "https://www.harboroutdoor.com/collections/tents"),
         ("trekking poles", "https://www.harboroutdoor.com/collections/trekking-poles")]

def pos_ctr(p):  # rough CTR curve by position
    return max(0.004, 0.32 * math.exp(-0.33 * (p - 1)))

qrows, prows = [], []
for i, q in enumerate(TOPIC):
    imp = int(rng.lognormvariate(math.log(3200), 0.9)) + 150
    cannibal = i < 15 or "best" in q
    p_coll = rng.uniform(3.5, 8.5)
    p_blog = rng.uniform(6.0, 15.0)
    # query-level web: position of our top result
    if cannibal:
        qpos = min(p_coll, p_blog)
        f_coll, f_blog = rng.uniform(0.82, 0.97), rng.uniform(0.55, 0.85)
    else:
        qpos = p_coll
        f_coll, f_blog = 1.0, 0.0
    clk = round(imp * pos_ctr(qpos) * rng.uniform(0.8, 1.2) * 0.55)
    qrows.append([q, "web", imp, clk, round(clk / imp, 4), round(qpos, 1)])
    if cannibal:
        c_share = rng.uniform(0.55, 0.8)
        c_coll = round(clk * c_share)
        for pg, f, p, c in ((COLL, f_coll, p_coll, c_coll), (BLOG, f_blog, p_blog, clk - c_coll)):
            pi = round(imp * f)
            prows.append([q, pg, "web", pi, c, round(c / pi, 4), round(p, 1)])
    else:
        prows.append([q, COLL, "web", imp, clk, round(clk / imp, 4), round(p_coll, 1)])
    # image search: many impressions, tiny CTR
    iimp = round(imp * rng.uniform(1.6, 3.0))
    ipos = rng.uniform(8, 40)
    iclk = round(iimp * rng.uniform(0.002, 0.007))
    qrows.append([q, "image", iimp, iclk, round(iclk / iimp, 4), round(ipos, 1)])
    ic = round(iclk * 0.6)
    for pg, f, c in ((COLL, rng.uniform(0.6, 0.9), ic), (BLOG, rng.uniform(0.5, 0.8), iclk - ic)):
        pi = round(iimp * f)
        prows.append([q, pg, "image", pi, c, round(c / pi, 4) if pi else 0, round(ipos + rng.uniform(0, 6), 1)])
    if i % 4 == 1:
        vimp = round(imp * rng.uniform(0.2, 0.5)); vclk = round(vimp * rng.uniform(0.003, 0.01))
        qrows.append([q, "video", vimp, vclk, round(vclk / vimp, 4), round(rng.uniform(5, 20), 1)])
        prows.append([q, BLOG, "video", vimp, vclk, round(vclk / vimp, 4), qrows[-1][5]])
for q, pg in OTHER:
    imp = int(rng.lognormvariate(math.log(4000), 0.6)); p = rng.uniform(3, 12)
    clk = round(imp * pos_ctr(p) * 0.55)
    qrows.append([q, "web", imp, clk, round(clk / imp, 4), round(p, 1)])
    prows.append([q, pg, "web", imp, clk, round(clk / imp, 4), round(p, 1)])
    iimp = round(imp * rng.uniform(1.2, 2)); iclk = round(iimp * 0.004)
    qrows.append([q, "image", iimp, iclk, round(iclk / iimp, 4), round(rng.uniform(10, 30), 1)])
    prows.append([q, pg, "image", iimp, iclk, round(iclk / iimp, 4), qrows[-1][5]])
qrows.sort(key=lambda r: (r[0], r[1])); prows.sort(key=lambda r: (r[0], r[2], r[1]))

topic = lambda q: "hiking boot" in q
qw = [r for r in qrows if topic(r[0]) and r[1] == "web"]
qa = [r for r in qrows if topic(r[0])]
pw = [r for r in prows if topic(r[0]) and r[2] == "web"]
pa = [r for r in prows if topic(r[0])]
web_imp = sum(r[2] for r in qw); web_clk = sum(r[3] for r in qw)
web_ctr = web_clk / web_imp
web_pos = sum(r[2] * r[5] for r in qw) / web_imp
all_imp_q = sum(r[2] for r in qa); all_clk_q = sum(r[3] for r in qa)
# naive
sum_pa_imp = sum(r[3] for r in pa); sum_pa_clk = sum(r[4] for r in pa)
sum_pw_imp = sum(r[3] for r in pw)
ctr_all_q = all_clk_q / all_imp_q
ctr_all_p = sum_pa_clk / sum_pa_imp
ctr_web_p = sum(r[4] for r in pw) / sum_pw_imp
mean_pos_q = sum(r[5] for r in qw) / len(qw)
mean_pos_rows = sum(r[6] for r in pa) / len(pa)
both = sorted({r[0] for r in pw if r[1] == BLOG})
blog_clk = sum(r[4] for r in pw if r[1] == BLOG); coll_clk = sum(r[4] for r in pw if r[1] == COLL)
blog_pos = sum(r[3] * r[6] for r in pw if r[1] == BLOG) / sum(r[3] for r in pw if r[1] == BLOG)
coll_pos = sum(r[3] * r[6] for r in pw if r[1] == COLL) / sum(r[3] for r in pw if r[1] == COLL)

assert sum_pa_imp > 3 * web_imp and sum_pw_imp > 1.4 * web_imp
assert web_ctr > 2.2 * ctr_all_q and web_ctr > 3 * ctr_all_p
assert 0.02 <= web_ctr <= 0.10, web_ctr
assert abs(mean_pos_rows - web_pos) > 4
assert len(both) >= 14

pct = lambda x, n=2: f"{100 * x:.{n}f}%"
print(f"{NAME}: web query-level impr {web_imp:,} CTR {pct(web_ctr)} pos {web_pos:.1f}; naive summed rows {sum_pa_imp:,} CTR {pct(ctr_all_p)}; {len(both)} cannibal queries")

prompt = """
We're Harbor Outdoor. resources/gsc_query_page.csv and resources/gsc_query.csv are our Google Search Console exports for July-September 2026. How much search demand is there for hiking boots, how are we capturing it, and what's our organic CTR? Write report.md with the numbers and what you'd do next.
"""

g1 = f"""
Ground truth for queries containing "hiking boot" (20 queries), Google web search, July-September 2026, from the query-level export gsc_query.csv (search_type = web):
- Impressions (search demand we appear for): {web_imp:,}
- Clicks: {web_clk:,}
- Organic CTR: {pct(web_ctr)}

Wrong numbers produced by common mistakes:
- Summing query x page rows (double counts searches where two of our pages appear): web-only {sum_pw_imp:,} impressions; all search types {sum_pa_imp:,} impressions.
- Including image and video search: query-level all types {all_imp_q:,} impressions with CTR {pct(ctr_all_q)}; from summed query x page rows CTR {pct(ctr_all_p)}.
- Web CTR from summed query x page rows: {pct(ctr_web_p)}.

PASS if report.md reports web-search impressions for hiking-boot queries within 3% of {web_imp:,} AND an organic CTR within 0.3 percentage points of {pct(web_ctr)}. Also reporting an all-search-types impression total of about {all_imp_q:,} is fine as long as it is not the headline CTR basis.
FAIL if the headline impressions/demand figure is a summed query x page total ({sum_pw_imp:,} or {sum_pa_imp:,}), or the headline CTR is an all-search-types figure (about {pct(ctr_all_q)} or {pct(ctr_all_p)}), or either number is missing.
"""

g2 = f"""
Ground truth: two Harbor Outdoor pages compete for the same queries (keyword cannibalization) on {len(both)} of the 20 hiking-boot queries:
- {COLL} (impression-weighted web position {coll_pos:.1f}, {coll_clk:,} web clicks)
- {BLOG} (impression-weighted web position {blog_pos:.1f}, {blog_clk:,} web clicks)

PASS if report.md identifies that the collection page and the blog post both rank for the same hiking-boot queries (cannibalization / competing pages / split signals) and recommends consolidating or differentiating them (e.g. canonical, internal linking, merging, re-targeting the blog to informational queries).
FAIL if report.md does not mention that two of our pages compete for the same queries.
"""

g3 = f"""
Ground truth average web position for hiking-boot queries, impression-weighted from the query-level export: {web_pos:.1f}.
Also acceptable: the simple mean of the web query-level positions, {mean_pos_q:.1f}.
Wrong value: simple mean over all query x page rows including image/video, {mean_pos_rows:.1f}.
PASS if report.md's average position for hiking-boot web queries is within 0.7 of {web_pos:.1f}, or it does not report an overall average position.
FAIL if it reports {mean_pos_rows:.1f} (or anything more than 0.7 away from {web_pos:.1f}) as our average position.
"""

write_case(NAME, {"resources/gsc_query_page.csv": to_csv(["query", "page", "search_type", "impressions", "clicks", "ctr", "position"], prows),
                  "resources/gsc_query.csv": to_csv(["query", "search_type", "impressions", "clicks", "ctr", "position"], qrows)},
           prompt, [("demand-and-ctr", 3, g1), ("cannibalization", 2, g2), ("position", 1, g3)])
