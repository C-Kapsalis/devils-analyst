"""Breadth benchmark, Meta: creative test readout (Ashgrove Candles, September 2026).

Subtle problems (5): the "test" was two ads in one ad set, so Meta's delivery
gave ~3/4 of spend to one ad (not a randomised split); the UGC ad started on
1 September and the studio ad on 9 September, so only UGC ran during the 5-8
September sitewide sale; the winner was picked on CTR (all clicks) while link
CTR is about equal; most of UGC's purchases are view-through (7d click + 1d
view vs 1d click); on 1-day-click purchases per 1,000 impressions outside the
sale days the difference is small and not significant.
DECISION: no winner can be declared; rerun as a proper A/B test (separate ad
sets / Experiments, same dates, equal budget) before rolling out UGC.
Decoys (2): studio CPM ~10% above UGC; link CTR 1.2-1.5%."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-social-creative-test"
rng = random.Random(46021)
SALE = {5, 6, 7, 8}
AOV = 42.0

# daily rows Sep 1-28 for two ads in one ad set
U, S = "UGC - Morning Ritual (video)", "Studio - Amber Collection (still)"
daily = []
for d in range(1, 29):
    for ad in (U, S):
        if ad == S and d < 9:
            continue
        sale = d in SALE
        spend = (118 if ad == U else 40) * rng.uniform(0.9, 1.1) * (1.25 if sale else 1.0)
        cpm = (9.4 if ad == U else 10.4) * rng.uniform(0.95, 1.05)
        imps = int(spend / cpm * 1000)
        link_ctr = (0.0136 if ad == U else 0.0131) * rng.uniform(0.92, 1.08)
        all_ratio = 2.3 if ad == U else 1.35
        link = int(imps * link_ctr); allc = int(link * all_ratio * rng.uniform(0.95, 1.05))
        p1 = (0.0170 if ad == U else 0.0185) * (2.6 if sale else 1.0)
        pur1 = sum(1 for _ in range(link) if rng.random() < p1)
        vt = (1.45 if ad == U else 0.35)
        pur7 = pur1 + sum(1 for _ in range(int(imps / 100)) if rng.random() < vt * p1 * 1.3)
        daily.append([f"2026-09-{d:02d}", "Creative Test - Sep", ad, round(spend, 2), imps, allc, link, pur1, pur7])

# ad-level totals
ad_rows, st = [], {}
for ad in (U, S):
    rr = [r for r in daily if r[2] == ad]
    t = [sum(r[i] for r in rr) for i in range(3, 9)]
    st[ad] = dict(spend=t[0], imps=t[1], allc=t[2], link=t[3], p1=t[4], p7=t[5], start=rr[0][0])
    ad_rows.append(["Creative Test - Sep", ad, rr[0][0], "2026-09-28", round(t[0], 2), t[1], t[2], t[3],
                    round(100 * t[2] / t[1], 2), t[5], t[4], round(t[5] * AOV * rng.uniform(0.97, 1.03), 2)])

# ---------- ground truth ----------
tot_spend = st[U]["spend"] + st[S]["spend"]
u_share = st[U]["spend"] / tot_spend
ctr_all = {a: st[a]["allc"] / st[a]["imps"] for a in st}
ctr_link = {a: st[a]["link"] / st[a]["imps"] for a in st}
vt_share = {a: 1 - st[a]["p1"] / st[a]["p7"] for a in st}
roas7 = {a: ad_rows[i][11] / st[a]["spend"] for i, a in enumerate((U, S))}
u_sale_p1 = sum(r[7] for r in daily if r[2] == U and int(r[0][-2:]) in SALE)
sale_share = u_sale_p1 / st[U]["p1"]
# common window: 9-28 Sep (no sale days, both ads live)
def win(ad):
    rr = [r for r in daily if r[2] == ad and int(r[0][-2:]) >= 9]
    return sum(r[4] for r in rr), sum(r[7] for r in rr)
iu, pu = win(U); is_, ps = win(S)
ru, rs = pu / iu * 1000, ps / is_ * 1000
# two-proportion z-test on purchases per impression
p_pool = (pu + ps) / (iu + is_)
z = (pu / iu - ps / is_) / math.sqrt(p_pool * (1 - p_pool) * (1 / iu + 1 / is_))
pval = math.erfc(abs(z) / math.sqrt(2))
cpm = {a: st[a]["spend"] / st[a]["imps"] * 1000 for a in st}

assert 0.7 < u_share < 0.82
assert ctr_all[U] > 1.5 * ctr_all[S] and abs(ctr_link[U] / ctr_link[S] - 1) < 0.12
assert vt_share[U] > 0.5 and vt_share[S] < 0.4 and roas7[U] > 1.3 * roas7[S]
assert sale_share > 0.2
assert pval > 0.2, pval
assert 1.05 < cpm[S] / cpm[U] < 1.2 and all(0.012 < v < 0.015 for v in ctr_link.values())

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
eur = lambda x, d=0: f"€{x:,.{d}f}"

notes = f"""# Ashgrove Candles: September creative test (social team notes)

- Set-up: both ads in one ad set "Creative Test - Sep" (Advantage+ placements, purchase optimisation, 7-day click + 1-day view).
- The studio ad went live on 9 September (approval delay); the UGC video ran from 1 September.
- 5-8 September: sitewide 20% off sale.
- Result: UGC wins clearly. CTR {pc(ctr_all[U], 2)} vs {pc(ctr_all[S], 2)}, ROAS {roas7[U]:.2f}x vs {roas7[S]:.2f}x.
- Plan: roll UGC out across all prospecting and retire studio stills.
"""

files = {
    "resources/creative_test_notes.md": notes,
    "resources/meta_creative_test_ads.csv": to_csv(
        ["adset_name", "ad_name", "start_date", "end_date", "amount_spent", "impressions", "clicks_all", "link_clicks", "ctr_all_pct",
         "purchases", "purchases_1d_click", "purchase_conversion_value"], ad_rows),
    "resources/meta_creative_test_daily.csv": to_csv(
        ["date", "adset_name", "ad_name", "amount_spent", "impressions", "clicks_all", "link_clicks", "purchases_1d_click", "purchases"], daily),
}

prompt = """
We're Ashgrove Candles. In September we tested a UGC video against our studio still on Meta. The team's notes and the Ads Manager exports are in resources/. Which creative won, and should we roll it out across prospecting? Put the answer and the numbers in report.md.
"""

N = 5; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Not a randomised split. Both ads sat in one ad set, so Meta's delivery chose who saw what and gave UGC {pc(u_share, 0)} of spend. Found if report.md says the set-up (ads in one ad set / uneven delivery) is not a valid A/B test.
2. Different dates and a sale. UGC started 1 September, studio 9 September; only UGC ran during the 5-8 September sale, which produced {pc(sale_share, 0)} of UGC's 1-day-click purchases. Found if report.md flags the different start dates and/or the sale days favouring UGC.
3. Winner picked on all-clicks CTR. CTR (all) {pc(ctr_all[U], 2)} vs {pc(ctr_all[S], 2)}, but link CTR is {pc(ctr_link[U], 2)} vs {pc(ctr_link[S], 2)} (about equal). Found if report.md says CTR should use link clicks and they are about the same.
4. View-through inflates UGC's ROAS. {pc(vt_share[U], 0)} of UGC's purchases are view-through (purchases vs purchases_1d_click) vs {pc(vt_share[S], 0)} for the studio ad. Found if report.md compares on 1-day click (or flags the view-through share).
5. Not significant on a fair comparison. On 9-28 September (both live, no sale), 1-day-click purchases per 1,000 impressions are {ru:.2f} (UGC, {pu} purchases) vs {rs:.2f} (studio, {ps} purchases); two-proportion test p = {pval:.2f}. Found if report.md says the difference on a like-for-like window is small / not statistically significant / inconclusive.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: no winner can be declared from this test. Do not roll UGC out as "the winner" on this evidence; rerun as a proper A/B test (separate ad sets or Meta's A/B test tool, same dates, equal budgets, outside sale periods, judged on 1-day-click purchases). On the fair window the two are close ({ru:.2f} vs {rs:.2f} purchases per 1,000 impressions, p = {pval:.2f}).

Naive wrong answer: "UGC won (CTR {pc(ctr_all[U], 2)} vs {pc(ctr_all[S], 2)}, ROAS {roas7[U]:.2f}x vs {roas7[S]:.2f}x); roll it out across prospecting."

PASS if report.md's main recommendation is that the test is inconclusive/invalid and should be rerun properly before rolling out (running both creatives meanwhile is fine).
FAIL if it declares UGC (or the studio ad) the winner and recommends rolling it out across prospecting.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. The studio ad's CPM ({eur(cpm[S], 2)}) is about {pc(cpm[S] / cpm[U] - 1, 0)} above UGC's ({eur(cpm[U], 2)}). Normal variation between ads and formats.
- D2. Link CTRs of {pc(ctr_link[U], 2)} and {pc(ctr_link[S], 2)}: inside the normal 0.8-2.5% band for Meta.

PASS if report.md does not treat the CPM gap as a finding or reason to pick a creative, and does not call the link CTRs weak.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: u share {u_share:.2f}; ctr all {ctr_all[U]:.4f}/{ctr_all[S]:.4f} link {ctr_link[U]:.4f}/{ctr_link[S]:.4f}; vt {vt_share[U]:.2f}/{vt_share[S]:.2f}; "
      f"roas7 {roas7[U]:.2f}/{roas7[S]:.2f}; sale share {sale_share:.2f}; fair {ru:.2f}({pu}) vs {rs:.2f}({ps}) p={pval:.2f}")
