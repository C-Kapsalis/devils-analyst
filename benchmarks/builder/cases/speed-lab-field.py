import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

# Northwind Coffee PageSpeed export (Lighthouse lab = section "performance", CrUX field p75 =
# section "performance_google"), two monthly snapshots, mobile + desktop. The highest-traffic
# pages fail field mobile LCP (p75 > 2500 ms) while most low-traffic pages pass and lab values
# look fine. Some failed audits are recorded with 0 values.
NAME = "speed-lab-field"
rng = random.Random(4606)

PAGES = [  # landing_page, sessions (Q3), latest field mobile LCP p75 target
    ("/", 182400, 3480), ("/collections/coffee-beans", 96300, 3920), ("/products/house-blend", 61800, 3150),
    ("/collections/subscriptions", 44700, 2870), ("/products/espresso-roast", 28900, 2710),
    ("/blog/how-to-brew-pour-over", 9400, 2140), ("/collections/brewing-gear", 8100, 2290),
    ("/products/decaf-colombia", 6200, 1980), ("/pages/about", 4100, 1720), ("/blog/cold-brew-guide", 3800, 2210),
    ("/products/gift-card", 3300, 1850), ("/pages/wholesale", 2700, 2050), ("/blog/coffee-grind-size", 2400, 2380),
    ("/pages/contact", 1900, 1640), ("/products/moka-pot", 1600, 2440), ("/pages/shipping", 1200, 1590),
    ("/blog/water-temperature", 1050, 1930), ("/pages/careers", 600, 1700),
]
DATES = ["2026-09-01", "2026-10-01"]
LATEST = DATES[-1]
WEIGHTS = {"largest-contentful-paint": 0.25, "first-contentful-paint": 0.10, "total-blocking-time": 0.30}

def lcp_score(ms):  # Lighthouse-style log-normal scoring, mobile control points p10=2500, median=4000
    mu = math.log(4000); sigma = (math.log(4000) - math.log(2500)) / 1.2816
    return round(0.5 * math.erfc((math.log(max(ms, 1)) - mu) / (sigma * math.sqrt(2))), 2)

rows = []
fail_slots = {("2026-09-01", "mobile", "performance", "/collections/coffee-beans"),
              ("2026-09-01", "desktop", "performance_google", "/"),
              ("2026-10-01", "mobile", "performance", "/products/house-blend"),
              ("2026-10-01", "desktop", "performance", "/collections/subscriptions"),
              ("2026-09-01", "mobile", "performance_google", "/products/house-blend"),
              ("2026-10-01", "desktop", "performance", "/")}
for date in DATES:
    for strat in ("mobile", "desktop"):
        for page, sess, field_lcp in PAGES:
            drift = 1.0 if date == LATEST else rng.uniform(0.96, 1.06)
            sm = 1.0 if strat == "mobile" else 0.55
            for section in ("performance", "performance_google"):
                failed = (date, strat, section, page) in fail_slots
                if section == "performance":  # lab: throttled synthetic run, looks fine
                    vals = {"largest-contentful-paint": rng.uniform(1700, 2400) * sm,
                            "first-contentful-paint": rng.uniform(900, 1500) * sm,
                            "total-blocking-time": rng.uniform(80, 260) * sm}
                else:  # field p75 from CrUX
                    vals = {"largest-contentful-paint": field_lcp * drift * sm * rng.uniform(0.98, 1.02),
                            "first-contentful-paint": field_lcp * 0.55 * drift * sm * rng.uniform(0.95, 1.05),
                            "interaction-to-next-paint": rng.uniform(120, 260) * (1 if strat == "mobile" else 0.6)}
                for metric, v in vals.items():
                    v = 0.0 if failed else round(v)
                    score = 0 if failed else (lcp_score(v) if metric == "largest-contentful-paint" else round(rng.uniform(0.75, 0.99), 2))
                    w = WEIGHTS.get(metric, 0) if section == "performance" else ""
                    rows.append([date, strat, page, section, metric, v, score, w, "false" if failed else "true"])
header = ["date", "strategy", "landing_page", "section_name", "metric_id", "audit_numeric_value", "audit_score", "metric_weight", "is_audit_successful"]
traffic = [[p, s] for p, s, _ in sorted(PAGES, key=lambda x: x[0])]

LCP = "largest-contentful-paint"
lcp_rows = [r for r in rows if r[4] == LCP]
field = {r[2]: r[5] for r in lcp_rows if r[0] == LATEST and r[1] == "mobile" and r[3] == "performance_google" and r[8] == "true"}
sess = {p: s for p, s, _ in PAGES}
assert len(field) == len(PAGES)
tot_s = sum(sess.values())
pass_pages = [p for p in field if field[p] <= 2500]
fail_pages = sorted([p for p in field if field[p] > 2500], key=lambda p: -sess[p])
share_sess_pass = sum(sess[p] for p in pass_pages) / tot_s
share_pages_pass = len(pass_pages) / len(field)
w_p75 = sum(field[p] * sess[p] for p in field) / tot_s  # traffic-weighted average of page p75s (indicative)
# naive
naive_mean_all = sum(r[5] for r in lcp_rows) / len(lcp_rows)
naive_mean_success = sum(r[5] for r in lcp_rows if r[8] == "true") / sum(1 for r in lcp_rows if r[8] == "true")
lab_latest_mobile = [r[5] for r in lcp_rows if r[0] == LATEST and r[1] == "mobile" and r[3] == "performance" and r[8] == "true"]
naive_lab = sum(lab_latest_mobile) / len(lab_latest_mobile)
naive_field_unweighted = sum(field.values()) / len(field)

assert share_sess_pass < 0.15 and share_pages_pass > 0.7, (share_sess_pass, share_pages_pass)
assert naive_mean_all < 2500 and naive_lab < 2500 and naive_field_unweighted < 2500
assert fail_pages[:3] == ["/", "/collections/coffee-beans", "/products/house-blend"]
assert any(r[5] == 0 for r in lcp_rows)

pct = lambda x, n=0: f"{100 * x:.{n}f}%"
print(f"{NAME}: {pct(share_sess_pass, 1)} of sessions on passing pages ({len(pass_pages)}/{len(field)} pages pass); naive mean LCP {naive_mean_all:.0f} ms")

prompt = """
We're Northwind Coffee. resources/pagespeed_export.csv is our PageSpeed / Core Web Vitals export (last two monthly runs) and resources/page_traffic.csv has sessions by landing page for last quarter. Does our site pass Core Web Vitals on LCP, and which pages should engineering fix first? Write report.md with the verdict and a prioritised fix list.
"""

fail_list = "\n".join(f"  {i + 1}. {p}: field mobile LCP p75 {field[p]:,} ms, {sess[p]:,} sessions ({pct(sess[p] / tot_s, 1)} of traffic)" for i, p in enumerate(fail_pages))

g1 = f"""
Ground truth: Core Web Vitals pass/fail is judged on FIELD data (section_name = performance_google, the real-user CrUX p75), mobile, latest run ({LATEST}), successful audits only. The LCP threshold is p75 <= 2,500 ms.
- {len(pass_pages)} of {len(field)} pages pass ({pct(share_pages_pass)} of pages), but they are the low-traffic pages: only {pct(share_sess_pass, 1)} of sessions land on a passing page; {pct(1 - share_sess_pass, 1)} of sessions land on pages that FAIL LCP.
- The site therefore does NOT pass LCP for most real visitors.

Wrong answers produced by common mistakes:
- Mean of all LCP rows (lab + field, mobile + desktop, both dates, including failed audits recorded as 0): {naive_mean_all:,.0f} ms -> "passes".
- Mean of successful LCP rows: {naive_mean_success:,.0f} ms -> "passes".
- Lab (Lighthouse, section performance) mobile LCP average on the latest run: {naive_lab:,.0f} ms -> "passes".
- Unweighted average of page-level field mobile p75s: {naive_field_unweighted:,.0f} ms, or "{pct(share_pages_pass)} of pages pass" -> "mostly passing".

PASS if report.md concludes that the site does NOT pass (or mostly fails) LCP on mobile field data because the highest-traffic pages fail, citing either the traffic share (roughly {pct(share_sess_pass)} of sessions on passing pages / {pct(1 - share_sess_pass)} on failing pages, within 5 percentage points) or naming the top failing pages with their field p75 values above 2,500 ms.
FAIL if report.md says the site passes LCP, or bases the verdict on any of the averaged values above, on lab data, or on the share of pages passing without weighting by traffic.
"""

g2 = f"""
Ground truth fix priority (pages failing field mobile LCP on {LATEST}, ordered by sessions):
{fail_list}
All other pages pass field mobile LCP.

PASS if report.md's prioritised fix list starts with "/", "/collections/coffee-beans" and "/products/house-blend" (these three in its top three, in any order), and does not put passing low-traffic pages ahead of them.
FAIL if the top of the list is driven by lab scores or by the slowest low-traffic pages, or if any of those three pages is missing from the top three.
"""

g3 = """
PASS if report.md shows awareness that some audit rows failed (is_audit_successful = false, recorded with 0 values) and excluded them, OR its numbers clearly come only from successful latest-run field rows (no 0 ms values used).
FAIL if it reports any page's LCP as 0 ms or treats 0 values as fast pages.
"""

write_case(NAME, {"resources/pagespeed_export.csv": to_csv(header, rows),
                  "resources/page_traffic.csv": to_csv(["landing_page", "sessions"], traffic)},
           prompt, [("lcp-verdict", 3, g1), ("fix-priority", 2, g2), ("failed-audits", 1, g3)])
