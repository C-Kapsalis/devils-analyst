import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "brand-search-share"
rng = random.Random(606)

MONTHS = [dt.date(2024 + (9 + i) // 12, (9 + i) % 12 + 1, 1) for i in range(24)]  # Oct 2024 .. Sep 2026
SEASON = [1.00, 1.35, 1.45, 1.00, 0.85, 0.90, 0.90, 0.85, 0.80, 0.80, 0.85, 0.95]  # Oct..Sep
S_SUM = sum(SEASON)

# group: (keyword_type, competitor_name, {keyword: share}, year1 total, year2 total)
GROUPS = [
    ("brand_own", "", {"nordvik": 0.62, "nordvik jacket": 0.26, "nordvik outlet": 0.12}, 120000, 156000),
    ("brand_competitor", "Fjellmark", {"fjellmark": 0.60, "fjellmark jacket": 0.28, "fjellmark sale": 0.12}, 200000, 310000),
    ("brand_competitor", "Arcton", {"arcton": 0.58, "arcton parka": 0.30, "arcton discount code": 0.12}, 150000, 222000),
    ("brand_competitor", "Vallo", {"vallo": 0.65, "vallo coat": 0.25, "vallo outlet": 0.10}, 75000, 90000),
    ("category", "", {"rain jacket": 0.34, "waterproof jacket": 0.28, "hiking jacket": 0.22, "insulated jacket": 0.16}, 1000000, 1400000),
]

rows = []  # month, keyword, type, competitor, searches
for i, m in enumerate(MONTHS):
    yr = i // 12
    for ktype, comp, kws, y1, y2 in GROUPS:
        tot = y1 if yr == 0 else y2
        for kw, sh in kws.items():
            v = tot * sh * SEASON[i % 12] / S_SUM * rng.gauss(1, 0.03)
            v = int(round(v, -1))
            rows.append([m.strftime("%Y-%m"), kw, ktype, comp, v])


def total(pred, yr):
    lo, hi = MONTHS[12 * yr].strftime("%Y-%m"), MONTHS[12 * yr + 11].strftime("%Y-%m")
    return sum(r[4] for r in rows if lo <= r[0] <= hi and pred(r))


own = [total(lambda r: r[2] == "brand_own", y) for y in (0, 1)]
allbrand = [total(lambda r: r[2].startswith("brand"), y) for y in (0, 1)]
cat = [total(lambda r: r[2] == "category", y) for y in (0, 1)]
comps = {c: [total(lambda r, c=c: r[3] == c, y) for y in (0, 1)] for c in ("Fjellmark", "Arcton", "Vallo")}
own_g = own[1] / own[0] - 1
cat_g = cat[1] / cat[0] - 1
sos = [own[y] / allbrand[y] for y in (0, 1)]
idx = [own[y] / cat[y] for y in (0, 1)]
comp_g = {c: v[1] / v[0] - 1 for c, v in comps.items()}
faster = [c for c, g in comp_g.items() if g > own_g]


def month_own(ym):
    return sum(r[4] for r in rows if r[0] == ym and r[2] == "brand_own")


naive_seasonal = month_own("2025-12") / month_own("2025-09") - 1

assert 0.25 < own_g < 0.35
assert sos[1] < sos[0] - 0.01 and idx[1] < idx[0]
assert cat_g > own_g + 0.05 and len(faster) == 2
assert naive_seasonal > 0.7

searches = to_csv(["month", "keyword", "keyword_type", "competitor_name", "avg_monthly_searches"], rows)
yt = []
for m in MONTHS[12:]:
    cost = round(rng.gauss(15000, 300), 2)
    imps = int(cost / rng.uniform(0.0085, 0.0105))
    views = int(imps * rng.uniform(0.22, 0.28))
    yt.append([m.strftime("%Y-%m"), "Nordvik Brand - Built for Weather", cost, imps, views])
youtube = to_csv(["month", "campaign", "cost", "impressions", "views"], yt)

prompt = """
We started a YouTube brand campaign for Nordvik (outdoor jackets) in October 2025. resources/ has monthly Google search volumes from Keyword Planner for October 2024 to September 2026 (search_volumes.csv: month, keyword, keyword_type, competitor_name, avg_monthly_searches) and our monthly YouTube spend (youtube_spend.csv).

Our brand searches are up about 30%. Did the campaign build the brand, and should we double its budget? Write report.md with your numbers and recommendation.
"""

comp_txt = ", ".join(f"{c} {g*100:+.0f}%" for c, g in comp_g.items())
g_share = f"""
Ground truth (12 months Oct 2024-Sep 2025 vs Oct 2025-Sep 2026): Nordvik brand searches {own[0]:,} -> {own[1]:,} ({own_g*100:+.0f}%). But category searches grew {cat_g*100:+.0f}% ({cat[0]:,} -> {cat[1]:,}) and competitor brand searches grew {comp_txt}. Nordvik's share of brand search (own / all brand terms incl. competitors) fell from {sos[0]*100:.1f}% to {sos[1]*100:.1f}%; Nordvik searches per category search fell from {idx[0]:.3f} to {idx[1]:.3f} ({(idx[1]/idx[0]-1)*100:+.0f}%). The +30% is the market rising, not Nordvik gaining.

Naive answer: "brand searches +{own_g*100:.0f}% since the campaign started, so the campaign built the brand".

PASS if report.md benchmarks Nordvik's brand-search growth against competitors and/or category searches AND reports that Nordvik's share of search (or brand/category ratio) fell or did not rise (share figures within ~1.5 points of the above if given).
FAIL if report.md credits the campaign with the ~30% growth without a competitor or category benchmark, or says Nordvik gained share.
"""

g_budget = f"""
Ground truth: the search data do not show that the campaign grew Nordvik relative to the market (share of search fell {sos[0]*100:.1f}% -> {sos[1]*100:.1f}%; Nordvik grew slower than the category and than {' and '.join(faster)}). There is no case for doubling on this evidence. The right next step is a controlled test: geo split / matched-market holdout / on-off periods, read on branded search share and sales.

PASS if report.md does NOT recommend doubling the budget on this evidence (hold, cut, or test first are all fine) AND proposes a controlled test (geo split, holdout, matched markets, on/off) or another incrementality measurement.
FAIL if report.md recommends doubling (or materially increasing) the budget based on the raw brand-search growth.
"""

g_season = f"""
Ground truth: searches peak in November-December every year, so growth must compare the same months (year on year, or 12-month totals). Comparing, e.g., September 2025 (pre-campaign) with December 2025 would show Nordvik searches {naive_seasonal*100:+.0f}%, which is mostly seasonality.

PASS if report.md compares like-for-like periods (same months year on year, 12-month totals, or explicitly seasonally adjusted).
FAIL if report.md's headline comparison mixes seasons (e.g. pre-campaign autumn months vs the Nov-Dec peak) or reports a growth figure around {naive_seasonal*100:.0f}%.
"""

write_case(
    NAME,
    {"resources/search_volumes.csv": searches, "resources/youtube_spend.csv": youtube},
    prompt,
    [("share-of-search", 3, g_share), ("budget-decision", 2, g_budget), ("seasonality", 1, g_season)],
)
print(f"{NAME}: own {own_g:+.0%}, category {cat_g:+.0%}, comps {comp_txt}; SoS {sos[0]:.1%}->{sos[1]:.1%}; idx {idx[0]:.3f}->{idx[1]:.3f}; naive Sep->Dec {naive_seasonal:+.0%}")
