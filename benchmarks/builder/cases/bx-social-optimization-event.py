"""Breadth benchmark, Meta: monthly review (Linden & Fig skincare, September 2026).

Subtle problems (5): the Advantage+ prospecting campaign optimises for
add_to_cart, so its "cost per result" is cost per add to cart; per purchase it
is the most expensive prospecting line (DECISION); prospecting is split into
six interest ad sets each getting ~10-15 purchases a week and marked "Learning
limited" (well under ~50 optimisation events a week); two of them overlap
~60% (audience overlap export); the ad set with the best link CTR loses over
half its clicks before the landing page loads (landing page views / link
clicks ~45% vs ~85% elsewhere); retargeting CPM rose from ~9 to ~17 while
weekly reach fell (audience saturating).
Decoys (2): retargeting ROAS ~4x prospecting; prospecting CPM EUR 6-11."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-social-optimization-event"
rng = random.Random(28461)
AOV = 54.0

# ad set: campaign, optimisation event, spend, cpm, link ctr, lpv/click, atc per lpv, purchase per lpv, delivery
ADV = "Advantage+ Prospecting"
A = {
    "Advantage+ Audience": (ADV, "ADD_TO_CART", 9800, 6.4, 0.0118, 0.86, 0.150, 0.0105, "Active"),
    "Interest - Clean Beauty": ("Prospecting - Interests", "PURCHASE", 2300, 8.9, 0.0131, 0.85, 0.105, 0.0245, "Learning limited"),
    "Interest - Skincare Routine": ("Prospecting - Interests", "PURCHASE", 2200, 9.2, 0.0240, 0.45, 0.090, 0.0210, "Learning limited"),
    "Interest - Vegan Products": ("Prospecting - Interests", "PURCHASE", 2100, 8.4, 0.0122, 0.84, 0.100, 0.0240, "Learning limited"),
    "Interest - Yoga & Wellness": ("Prospecting - Interests", "PURCHASE", 2000, 7.8, 0.0115, 0.86, 0.098, 0.0235, "Learning limited"),
    "Interest - Natural Cosmetics": ("Prospecting - Interests", "PURCHASE", 2200, 9.6, 0.0126, 0.85, 0.104, 0.0250, "Learning limited"),
    "Interest - Sustainable Living": ("Prospecting - Interests", "PURCHASE", 1900, 8.1, 0.0119, 0.85, 0.097, 0.0238, "Learning limited"),
    "Retargeting - Visitors 30d": ("Retargeting", "PURCHASE", 3600, 15.8, 0.0190, 0.87, 0.180, 0.095, "Active"),
}
rows, st = [], {}
for a, (camp, opt, sp, cpm, ctr, lpvr, atcr, pr, deliv) in A.items():
    spend = round(sp * rng.uniform(0.98, 1.02), 2)
    imps = int(spend / cpm * 1000)
    reach = int(imps / rng.uniform(1.6, 2.4)) if camp != "Retargeting" else int(imps / rng.uniform(5.5, 6.5))
    link = int(imps * ctr * rng.uniform(0.96, 1.04))
    lpv = int(link * lpvr * rng.uniform(0.98, 1.02))
    atc = int(lpv * atcr * rng.uniform(0.95, 1.05))
    pur = int(round(lpv * pr * rng.uniform(0.95, 1.05)))
    val = round(pur * AOV * rng.uniform(0.96, 1.04), 2)
    results = atc if opt == "ADD_TO_CART" else pur
    rows.append([camp, a, opt, deliv, "7d_click_1d_view", spend, imps, reach, round(imps / reach, 2), link, lpv, atc, pur, val,
                 results, round(spend / results, 2)])
    st[a] = dict(camp=camp, spend=spend, imps=imps, link=link, lpv=lpv, atc=atc, pur=pur, val=val, results=results)

overlap = [
    ["Interest - Clean Beauty", "Interest - Natural Cosmetics", 61],
    ["Interest - Clean Beauty", "Interest - Vegan Products", 24],
    ["Interest - Skincare Routine", "Interest - Natural Cosmetics", 18],
    ["Interest - Yoga & Wellness", "Interest - Sustainable Living", 22],
    ["Interest - Vegan Products", "Interest - Sustainable Living", 27],
]
weeks = ["2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21"]
rt_cpm = [9.1, 9.8, 10.9, 12.0, 13.4, 14.6, 15.9, 17.2]
rt_reach = [21400, 20900, 20100, 19400, 18600, 17900, 17200, 16500]
rt_rows = [[w, int(r * rng.uniform(0.99, 1.01)), c, round(r * c / 1000 * rng.uniform(3.0, 3.3), 2)] for w, r, c in zip(weeks, rt_reach, rt_cpm)]

# ---------- ground truth ----------
ints = [a for a in A if a.startswith("Interest")]
pros = [ADV_A := "Advantage+ Audience"] + ints
cpr = {a: st[a]["spend"] / st[a]["results"] for a in A}
cpp = {a: st[a]["spend"] / st[a]["pur"] for a in A}
int_cpp = sum(st[a]["spend"] for a in ints) / sum(st[a]["pur"] for a in ints)
weekly_pur = {a: st[a]["pur"] / 30 * 7 for a in ints}
lpv_rate = {a: st[a]["lpv"] / st[a]["link"] for a in A}
ctr = {a: st[a]["link"] / st[a]["imps"] for a in A}
SR = "Interest - Skincare Routine"
others_lpv = sum(st[a]["lpv"] for a in A if a != SR) / sum(st[a]["link"] for a in A if a != SR)
rt = "Retargeting - Visitors 30d"
pros_roas = sum(st[a]["val"] for a in pros) / sum(st[a]["spend"] for a in pros)
rt_roas = st[rt]["val"] / st[rt]["spend"]
pros_cpm = [st[a]["spend"] / st[a]["imps"] * 1000 for a in pros]

assert cpr[ADV_A] == min(cpr.values()) and cpp[ADV_A] == max(cpp[a] for a in pros) and cpp[ADV_A] > 1.4 * int_cpp
assert all(8 <= w <= 17 for w in weekly_pur.values())
assert ctr[SR] == max(ctr[a] for a in pros) and lpv_rate[SR] < 0.5 and others_lpv > 0.8
assert cpp[SR] == max(cpp[a] for a in ints)
assert rt_cpm[-1] > 1.8 * rt_cpm[0] and rt_reach[-1] < rt_reach[0]
assert 3 < rt_roas / pros_roas < 6 and all(6 <= c <= 11 for c in pros_cpm)

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x, d=2: f"€{x:,.{d}f}"

notes = f"""# Linden & Fig: Meta September notes (in-house)

- Advantage+ Prospecting has the cheapest cost per result on the account ({eur(cpr[ADV_A])}). Idea for October: move half of the interest ad set budget into it.
- "Interest - Skincare Routine" has our best link CTR ({pc(ctr[SR], 2)}): the creative there is our winner.
- All ad sets report on 7-day click, 1-day view.
"""

files = {
    "resources/meta_notes_sep2026.md": notes,
    "resources/meta_adsets_sep2026.csv": to_csv(
        ["campaign_name", "adset_name", "optimization_goal", "delivery_status", "attribution_setting", "amount_spent", "impressions", "reach",
         "frequency", "link_clicks", "landing_page_views", "adds_to_cart", "purchases", "purchase_conversion_value", "results", "cost_per_result"], rows),
    "resources/meta_audience_overlap.csv": to_csv(["audience_a", "audience_b", "overlap_pct"], overlap),
    "resources/meta_retargeting_weekly.csv": to_csv(["week_start", "reach", "cpm", "amount_spent"], rt_rows),
}

prompt = """
We're Linden & Fig, a small skincare brand selling online. How did Meta do in September and what should we change for October? Our notes and the Ads Manager exports are in resources/. Write report.md with the numbers and what you'd change.
"""

N = 5; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. Wrong optimisation event. Advantage+ Audience optimises for ADD_TO_CART, so its cost per result ({eur(cpr[ADV_A])}) is cost per add to cart. Per purchase it costs {eur(cpp[ADV_A])} vs {eur(int_cpp)} for the purchase-optimised interest ad sets combined. Found if report.md says the Advantage+ result is add-to-cart (not purchase) and compares on purchases.
2. Fragmented, learning-limited prospecting. Six interest ad sets each get roughly {min(weekly_pur.values()):.0f}-{max(weekly_pur.values()):.0f} purchases a week and are all "Learning limited" (well below the ~50 optimisation events per week Meta needs). Found if report.md recommends consolidating ad sets because of learning-limited delivery / too few conversions per ad set.
3. Audience overlap. "Interest - Clean Beauty" and "Interest - Natural Cosmetics" overlap 61%. Found if report.md flags this overlap (bidding against yourself / merge).
4. Click-to-landing leak. "Interest - Skincare Routine" has the best link CTR ({pc(ctr[SR], 2)}) but only {pc(lpv_rate[SR])} of link clicks become landing page views (vs {pc(others_lpv)} elsewhere), and the highest cost per purchase of the interest ad sets ({eur(cpp[SR])}). Found if report.md flags the landing-page-view drop (page speed / landing page problem) rather than crowning the creative.
5. Retargeting saturating. Retargeting weekly CPM rose from €{rt_cpm[0]} to €{rt_cpm[-1]} while weekly reach fell from {rt_reach[0]:,} to {rt_reach[-1]:,}. Found if report.md flags rising CPM with shrinking reach (small/saturated audience).

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: do NOT move interest budget into Advantage+ Prospecting on its cost per result. Its result is an add to cart; per purchase it is the most expensive prospecting line ({eur(cpp[ADV_A])} vs {eur(int_cpp)}). Switch Advantage+ to optimise for purchases (or cut it back) and consolidate the interest ad sets, keeping budget on purchase-optimised prospecting.

Naive wrong answer: move half the interest budget into Advantage+ because it has the cheapest cost per result ({eur(cpr[ADV_A])}).

PASS if report.md's main recommendation rejects moving budget into Advantage+ on cost per result AND either switches its optimisation to purchase or reallocates based on cost per purchase.
FAIL if it endorses moving budget into Advantage+ as currently set up, or ranks ad sets on cost_per_result without noticing the different result types.
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. Retargeting ROAS ({rt_roas:.2f}x) is several times prospecting ROAS ({pros_roas:.2f}x). Expected: retargeting closes demand prospecting created. (Flagging retargeting's rising CPM is correct and separate.)
- D2. Prospecting CPMs between €{min(pros_cpm):.2f} and €{max(pros_cpm):.2f}: a normal range for Meta.

PASS if report.md does not treat the retargeting-vs-prospecting ROAS gap as a problem or recommend moving prospecting budget into retargeting because of it, and does not call the prospecting CPMs too high.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: adv cpr {cpr[ADV_A]:.2f} cpp {cpp[ADV_A]:.2f} vs int {int_cpp:.2f}; weekly pur {min(weekly_pur.values()):.1f}-{max(weekly_pur.values()):.1f}; "
      f"SR ctr {ctr[SR]:.4f} lpv {lpv_rate[SR]:.2f} cpp {cpp[SR]:.2f}; roas rt {rt_roas:.2f} pros {pros_roas:.2f}")
