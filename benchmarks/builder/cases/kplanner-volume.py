"""SERP crawl export: one row per tracked query x month x SERP result, with the
Keyword Planner volume (related_kplanner_searches) repeated on every row.
Volume must be taken once per query-month, averaged over the months a query
has data, then summed. Summing rows inflates ~10x; ranking by row count or
summed volume favours queries with more ads / more tracked months."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "kplanner-volume"
rng = random.Random(3391)
MONTHS = ["2026-06", "2026-07", "2026-08", "2026-09"]
OUR = "harboroutdoor.com"
# query: (base monthly volume, months tracked (last n), n ads typical, cpc_low, cpc_high, competition_index)
QUERIES = {
    "hiking boots":                 (20000, 2, 4, 0.55, 1.90, 100),
    "waterproof hiking boots":      (9900, 4, 3, 0.48, 1.70, 92),
    "rain jacket":                  (18000, 4, 4, 0.40, 1.45, 88),
    "mens rain jacket":             (6600, 4, 3, 0.42, 1.38, 85),
    "womens rain jacket":           (5400, 4, 4, 0.40, 1.30, 90),
    "backpacking tent":             (16000, 1, 2, 0.60, 2.10, 74),
    "2 person tent":                (6600, 4, 1, 0.35, 1.20, 61),
    "merino hiking socks":          (2900, 4, 4, 0.30, 0.95, 97),
    "trail running shoes":          (14800, 1, 4, 0.50, 1.75, 100),
    "packable down jacket":         (4400, 4, 2, 0.45, 1.60, 70),
    "hiking backpack 30l":          (2400, 4, 4, 0.38, 1.25, 83),
    "trekking poles":               (5400, 4, 0, 0.28, 0.90, 55),
    "camping stove":                (3600, 3, 1, 0.30, 1.05, 66),
    "sleeping bag 3 season":        (1900, 4, 3, 0.33, 1.10, 79),
    "gore tex jacket":              (12100, 4, 4, 0.52, 1.95, 94),
    "hiking boots wide fit":        (1300, 4, 4, 0.36, 1.20, 81),
}
DOMAINS = ["trailgear.co", "summitsupply.com", "outdoorhub.net", "peakandpine.com", "wildpath.org",
           "camplife.io", "ridgeline.shop", "basecamp-review.com", "mountainmag.com", "gearlab.net",
           "roamwell.com", "northtrail.store"]

rows, vol = [], {}
for q, (base, nmon, nads, lo, hi, comp) in QUERIES.items():
    seas = rng.uniform(-0.12, 0.12)
    for mi, m in enumerate(MONTHS[-nmon:]):
        v = int(round(base * (1 + seas * (mi - 1.5) / 1.5) * rng.uniform(0.95, 1.05), -1))
        vol[(q, m)] = v
        ads = max(0, nads + rng.choice([-1, 0, 0, 1])) if nads else 0
        ads = min(ads, 4)
        doms = rng.sample(DOMAINS, 10)
        if rng.random() < 0.5:
            doms[rng.randint(3, 9)] = OUR
        idx = 1
        for a in range(ads):
            rows.append([m, q, idx, rng.choice(DOMAINS), "ad", v, lo, hi, comp]); idx += 1
        for d in doms[:10 - ads]:
            rows.append([m, q, idx, d, "organic", v, lo, hi, comp]); idx += 1
# crawl gaps: blank volume on a few rows (never on all rows of a query-month)
for r in rng.sample(rows, 25):
    if r[2] != 1:
        r[5] = None
rows.sort(key=lambda r: (r[0], r[1], r[2]))
csv_text = to_csv(["month", "query", "result_index", "domain", "result_type", "related_kplanner_searches",
                   "cpc_low", "cpc_high", "competition_index"], rows)

# ---- ground truth ----
qm = {}
for r in rows:
    if r[5] is not None:
        qm[(r[1], r[0])] = max(qm.get((r[1], r[0]), 0), r[5])
assert qm == vol
avg = {q: sum(v for (qq, m), v in qm.items() if qq == q) / sum(1 for (qq, m) in qm if qq == q) for q in QUERIES}
total = sum(avg.values())
top5 = sorted(avg, key=lambda q: -avg[q])[:5]

naive_rows = sum(r[5] for r in rows if r[5] is not None)
naive_rows_per_month = naive_rows / len(MONTHS)
summed = {q: sum(v for (qq, m), v in qm.items() if qq == q) for q in QUERIES}
naive_unique_sum = sum(summed.values())               # query-months summed, not averaged
naive_div4 = naive_unique_sum / len(MONTHS)           # divided by 4 even when a query has fewer months
rowcount = {q: sum(1 for r in rows if r[1] == q) for q in QUERIES}
rowvol = {q: sum(r[5] for r in rows if r[1] == q and r[5] is not None) for q in QUERIES}
top5_rows = sorted(rowcount, key=lambda q: -rowcount[q])[:5]
top5_rowvol = sorted(rowvol, key=lambda q: -rowvol[q])[:5]
top5_summed = sorted(summed, key=lambda q: -summed[q])[:5]

assert 7 < naive_rows_per_month / total < 13, naive_rows_per_month / total
assert len(set(top5) - set(top5_rowvol)) >= 2, (top5, top5_rowvol)
assert len(set(top5) - set(top5_summed)) >= 2, (top5, top5_summed)
assert abs(naive_div4 - total) / total > 0.12
size = len(csv_text)
assert size < 60000, size

f0 = lambda x: f"{x:,.0f}"
avg_lines = "\n".join(f"- {q}: {f0(avg[q])} ({sum(1 for k in qm if k[0] == q)} month(s) of data)" for q in sorted(avg, key=lambda q: -avg[q]))

prompt = """
resources/serp_tracking.csv is our monthly SERP tracking export for the keywords we follow (June–September 2026), including the Keyword Planner search volume and CPC range for each keyword. What's the total monthly search volume for our tracked keywords, and which 5 keywords should we target first? Write report.md with the total, a per-keyword table, and your top 5.
"""

g_total = f"""
The volume (related_kplanner_searches) is repeated on every SERP row (10 SERP result rows per keyword per month). Correct method: take the value once per keyword-month, average across the months each keyword has data (some keywords were tracked for fewer months), then sum across keywords.
Ground truth total average monthly search volume across the {len(QUERIES)} tracked keywords: {f0(total)}.
Per keyword average monthly volume:
{avg_lines}
Wrong totals:
- Summing the column over all rows: {f0(naive_rows)}; divided by 4 months: {f0(naive_rows_per_month)}
- Summing one value per keyword-month without averaging over months: {f0(naive_unique_sum)}
- Summing one value per keyword-month and dividing by 4 for every keyword (ignoring that some have fewer months): {f0(naive_div4)}

PASS if report.md gives total monthly search volume within 3% of {f0(total)} (a total based on the latest month only, i.e. September 2026 values, is also acceptable if clearly labelled as such: {f0(sum(qm[(q, '2026-09')] for q in QUERIES if (q, '2026-09') in qm))}).
FAIL if the total is near any of the wrong totals, or no total is given.
"""
g_top5 = f"""
Ground-truth top 5 keywords by average monthly search volume: {', '.join(f'{q} ({f0(avg[q])})' for q in top5)}.
Wrong rankings:
- By number of rows in the export (this only counts months tracked x 10 results, so it favours keywords tracked all 4 months)
- By summing volume across all rows: {', '.join(top5_rowvol)}
- By summing volume across months (penalises keywords tracked for fewer months, e.g. "backpacking tent" and "trail running shoes" have only 1 month and "hiking boots" only 2): {', '.join(top5_summed)}

PASS if report.md's per-keyword volumes match the ground-truth averages above (within 5%) for the keywords it shows, AND its top 5 either (a) includes at least 4 of the ground-truth top 5, or (b) deliberately trades volume against competition_index / CPC / our current ranking (harboroutdoor.com) with that reasoning stated, using the correct per-keyword volumes.
FAIL if the per-keyword volumes it uses are inflated row sums (roughly 10x or more the values above) or month sums, or if the top 5 is ordered by row count or summed volume.
"""

write_case(NAME, {"resources/serp_tracking.csv": csv_text}, prompt,
           [("total-volume", 3, g_total), ("top5-keywords", 2, g_top5)])
print(f"{NAME}: total {total:,.0f}; naive rows {naive_rows:,} (/4 {naive_rows_per_month:,.0f}), month-sum {naive_unique_sum:,}, div4 {naive_div4:,.0f}; top5 {top5} vs rowvol {top5_rowvol}; {size} bytes")
