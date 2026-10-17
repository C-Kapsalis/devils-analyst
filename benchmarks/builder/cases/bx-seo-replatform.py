"""Breadth: organic search six weeks after a replatform (Harrowbay Home, Aug-Sep 2026).

Planted problems (5): the new collection template carries meta robots noindex,
so every sitemap collection URL has zero impressions and the old category
URLs redirect into non-indexable pages (biggest click loss, DECISION); six old
product URLs were left out of the redirect map and return 404; three new
product pages canonicalise to the staging domain; four old URLs redirect with
302 so old and new URLs both collect impressions; the sitemap lists URLs that
are noindexed (sitemap and indexability disagree).
Decoys (2): /cart, /account and /search are noindex on purpose; correctly
301-redirected product pages show small position slips of under one place."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-seo-replatform"
rng = random.Random(81303)
OLD, NEW = "https://www.harrowbay.com", "https://www.harrowbay.com"
STAGING = "https://staging-harrowbay.myshopfront.dev"

COLL = ["linen-bedding", "duvet-covers", "cushions", "throws", "table-lamps", "floor-lamps", "rugs", "curtains",
        "vases", "candles", "dinnerware", "glassware", "storage-baskets", "mirrors"]
PROD = ["oslo-linen-duvet-set", "rye-waffle-throw", "ember-ceramic-lamp", "dune-jute-rug", "fern-cushion-cover", "harbour-stoneware-plate",
        "arc-floor-lamp", "tide-glass-tumbler", "moss-velvet-cushion", "salt-linen-curtain", "kiln-vase-large", "brook-storage-basket",
        "shore-round-mirror", "loom-wool-throw", "cove-candle-cedar", "pebble-bowl-set", "reed-diffuser-fig", "cairn-side-lamp",
        "isle-bath-mat", "field-table-runner", "north-pillowcase-pair", "harvest-serving-board", "quay-wine-glass", "mere-linen-napkins",
        "dale-pouf", "stone-coaster-set", "grove-planter", "ridge-wall-shelf", "hollow-bowl-large", "anchor-door-stop",
        "sail-linen-apron", "marsh-rattan-tray", "cliff-lantern", "bay-sheepskin", "fold-blanket-box", "drift-photo-frame",
        "lark-tea-towel", "wren-mug", "elm-chopping-board", "heath-cushion-pad"]
BLOG = ["how-to-wash-linen", "choosing-a-rug-size", "layering-throws", "lamp-buying-guide", "small-space-storage", "table-setting-ideas"]
N404 = set(PROD[3:9])            # left out of the redirect map
CANON = set(PROD[12:15])         # canonical to staging
R302 = set(PROD[18:22])          # 302 instead of 301

gsc, crawl, sitemap, rmap = [], [], [], []
loss = dict(coll=0, p404=0, canon=0, r302=0, ok=0)
ok_slips = []

def add_gsc(page, period, clicks, imps, pos):
    gsc.append([page, period, clicks, imps, pos])

for c in COLL:
    old, new = f"{OLD}/category/{c}", f"{NEW}/collections/{c}"
    pre = int(rng.uniform(900, 3100)); imps = int(pre / rng.uniform(0.03, 0.05)); pos = round(rng.uniform(3.5, 9.5), 1)
    add_gsc(old, "pre_6w", pre, imps, pos)
    post_old = int(pre * rng.uniform(0.03, 0.07))
    add_gsc(old, "post_6w", post_old, int(imps * 0.12), round(pos + rng.uniform(3, 7), 1))
    loss["coll"] += pre - post_old
    crawl.append([old, 301, "Non-Indexable", "Redirected", "", "", new])
    crawl.append([new, 200, "Non-Indexable", "noindex", "noindex, follow", new, ""])
    sitemap.append([new]); rmap.append([f"/category/{c}", f"/collections/{c}"])

for p in PROD:
    old, new = f"{OLD}/product/{p}.html", f"{NEW}/products/{p}"
    pre = int(rng.uniform(150, 900)); imps = int(pre / rng.uniform(0.025, 0.06)); pos = round(rng.uniform(3, 12), 1)
    add_gsc(old, "pre_6w", pre, imps, pos)
    if p in N404:
        post = int(pre * rng.uniform(0.02, 0.06))
        add_gsc(old, "post_6w", post, int(imps * 0.15), round(pos + rng.uniform(6, 12), 1))
        newp = int(pre * rng.uniform(0.08, 0.15))
        add_gsc(new, "post_6w", newp, int(imps * 0.2), round(pos + rng.uniform(8, 14), 1))
        loss["p404"] += pre - post - newp
        crawl.append([old, 404, "Non-Indexable", "Client Error", "", "", ""])
        crawl.append([new, 200, "Indexable", "", "index, follow", new, ""])
        sitemap.append([new])
    elif p in CANON:
        post = int(pre * rng.uniform(0.25, 0.4))
        add_gsc(new, "post_6w", post, int(imps * 0.45), round(pos + rng.uniform(3, 6), 1))
        loss["canon"] += pre - post
        crawl.append([old, 301, "Non-Indexable", "Redirected", "", "", new])
        crawl.append([new, 200, "Non-Indexable", "Canonicalised", "index, follow", f"{STAGING}/products/{p}", ""])
        sitemap.append([new]); rmap.append([f"/product/{p}.html", f"/products/{p}"])
    elif p in R302:
        a = int(pre * rng.uniform(0.45, 0.55)); b = int(pre * rng.uniform(0.35, 0.45))
        add_gsc(old, "post_6w", a, int(imps * 0.55), round(pos + rng.uniform(0.5, 1.5), 1))
        add_gsc(new, "post_6w", b, int(imps * 0.5), round(pos + rng.uniform(2.5, 4.5), 1))
        loss["r302"] += pre - a - b
        crawl.append([old, 302, "Non-Indexable", "Redirected", "", "", new])
        crawl.append([new, 200, "Indexable", "", "index, follow", new, ""])
        sitemap.append([new]); rmap.append([f"/product/{p}.html", f"/products/{p}"])
    else:
        post = int(pre * rng.uniform(0.92, 1.03)); slip = round(rng.uniform(0.1, 0.8), 1)
        ok_slips.append(slip)
        add_gsc(old, "post_6w", int(pre * rng.uniform(0.01, 0.03)), int(imps * 0.05), round(pos + 2, 1))
        add_gsc(new, "post_6w", post, int(imps * rng.uniform(0.93, 1.02)), round(pos + slip, 1))
        loss["ok"] += pre - post
        crawl.append([old, 301, "Non-Indexable", "Redirected", "", "", new])
        crawl.append([new, 200, "Indexable", "", "index, follow", new, ""])
        sitemap.append([new]); rmap.append([f"/product/{p}.html", f"/products/{p}"])

for b in BLOG:
    u = f"{NEW}/blog/{b}"
    pre = int(rng.uniform(400, 1600)); imps = int(pre / rng.uniform(0.03, 0.06)); pos = round(rng.uniform(2, 8), 1)
    add_gsc(u, "pre_6w", pre, imps, pos)
    add_gsc(u, "post_6w", int(pre * rng.uniform(0.95, 1.05)), int(imps * rng.uniform(0.95, 1.05)), round(pos + rng.uniform(-0.3, 0.3), 1))
    crawl.append([u, 200, "Indexable", "", "index, follow", u, ""]); sitemap.append([u])
home_pre = 5200
add_gsc(f"{NEW}/", "pre_6w", home_pre, 14100, 1.2); add_gsc(f"{NEW}/", "post_6w", int(home_pre * 1.01), 14300, 1.2)
crawl.append([f"{NEW}/", 200, "Indexable", "", "index, follow", f"{NEW}/", ""]); sitemap.insert(0, [f"{NEW}/"])
for u in ["/cart", "/account", "/account/login", "/search?q=lamp"]:
    crawl.append([f"{NEW}{u}", 200, "Non-Indexable", "noindex", "noindex, nofollow", "", ""])

pre_total = sum(r[2] for r in gsc if r[1] == "pre_6w")
post_total = sum(r[2] for r in gsc if r[1] == "post_6w")
drop = pre_total - post_total
coll_share = loss["coll"] / drop
noindex_in_sitemap = sum(1 for s in sitemap if s[0].split(".com")[1].startswith("/collections/"))
coll_post_new_imps = sum(r[3] for r in gsc if "/collections/" in r[0])

assert loss["coll"] > 2 * loss["p404"] and loss["coll"] > 2.5 * loss["canon"], loss
assert coll_share > 0.55, coll_share
assert coll_post_new_imps == 0
assert max(ok_slips) < 1.0 and abs(loss["ok"]) < 0.06 * sum(r[2] for r in gsc if r[1] == "pre_6w" and "/product/" in r[0])
assert noindex_in_sitemap == len(COLL)

rng.shuffle(crawl)
gsc.sort(key=lambda r: (r[1], -r[2]))

notes = f"""# Notes
- Harrowbay Home (homeware, online only) moved to a new shop platform on 4 August 2026. URLs changed: /category/x became /collections/x and /product/x.html became /products/x. Blog and home page URLs did not change.
- Search Console pages export compares the 6 weeks before (23 Jun - 3 Aug) with the 6 weeks after (5 Aug - 15 Sep).
- The crawl was run on 16 September from the old and new URL lists. The redirect map is what the developers implemented.
- The platform partner says organic usually takes 3-6 months to settle after a migration.
"""

files = {
    "resources/notes.md": notes,
    "resources/gsc_pages_pre_post.csv": to_csv(["page", "period", "clicks", "impressions", "position"], gsc),
    "resources/crawl_post_migration.csv": to_csv(["address", "status_code", "indexability", "indexability_status", "meta_robots", "canonical_link_element", "redirect_url"], crawl),
    "resources/sitemap_urls.csv": to_csv(["loc"], sitemap),
    "resources/redirect_map.csv": to_csv(["from_path", "to_path"], rmap),
}

prompt = """
We moved Harrowbay Home to a new shop platform on 4 August. I've put a Search Console pages export (6 weeks before and after), a site crawl, our sitemap and the redirect map in resources/. How has organic search done since the move, and what should we prioritise? Please write it up in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Collection pages are noindexed. All {len(COLL)} /collections/ URLs return 200 with meta robots "noindex, follow"; they have zero post-migration impressions, and the old /category/ URLs (which earned {sum(r[2] for r in gsc if '/category/' in r[0] and r[1] == 'pre_6w'):,} clicks in the 6 weeks before) redirect into them. Counts as found if report.md names the noindex on the collection pages.
2. Missing redirects. Six old product URLs (e.g. /product/{sorted(N404)[0]}.html) return 404 and are not in the redirect map; they lost {loss['p404']:,} clicks. Counts as found if report.md flags old product URLs returning 404 / missing from the redirect map.
3. Canonical to staging. Three new product pages ({', '.join('/products/' + p for p in sorted(CANON))}) have canonical tags pointing to {STAGING}. Counts as found if report.md flags the staging canonical.
4. 302 instead of 301. Four old product URLs redirect with 302, so old and new URLs both still collect impressions and split clicks. Counts as found if report.md flags the 302 redirects (or old and new URLs both ranking).
5. Sitemap lists non-indexable URLs. All {noindex_in_sitemap} collection URLs in sitemap_urls.csv are noindex (sitemap and indexability disagree). Counts as found if report.md notes the sitemap contains noindexed URLs (it may be folded into finding 1 if the sitemap conflict is stated).

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 with evidence (URL, status, tag or click number).
FAIL if fewer than 3.
"""

g_decision = f"""
Organic clicks fell from {pre_total:,} to {post_total:,} in the 6 weeks after the move (a loss of {drop:,}). Of that, about {loss['coll']:,} ({coll_share * 100:.0f}%) is the noindexed collection pages; the 404s cost about {loss['p404']:,}, the staging canonicals about {loss['canon']:,}, and correctly redirected product pages are essentially flat.

The correct top priority: remove the noindex from the collection template (and resubmit those URLs) first, because it is most of the loss.

Naive answers: "wait, migrations take 3-6 months to settle" (the platform partner's line), a generic link-building or content push, or leading with the 404s or a general redirect audit while missing the noindex.

PASS if report.md's first priority is removing the noindex from the /collections/ pages (stated as the main cause of the drop or the largest loss).
FAIL if it recommends waiting for the migration to settle as the main action, if the noindex is missing, or if the first priority is something else (404s, canonicals, links, content).
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. /cart, /account, /account/login and /search?q=... are noindex. That is intended; these pages should not be indexed.
- D2. Correctly 301-redirected product pages show their new URLs a little lower than the old ones (position slips of {min(ok_slips)} to {max(ok_slips)} places) with clicks within a few percent of before. That is normal settling, not a problem to fix.

PASS if report.md does not recommend indexing the cart, account or search pages and does not present the small position slips on correctly redirected pages as a problem.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: pre {pre_total} post {post_total} drop {drop}; loss {loss}; coll share {coll_share:.2f}")
