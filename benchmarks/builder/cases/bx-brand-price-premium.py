"""Board brand-health slide (Larchwood Coffee Roasters) proposing a 6% list
price rise on the strength of the brand.

Planted subtle problems (4):
  P1 "#1 brand, 24% market share" is unit share of online specialty coffee in
     the 3 served regions; national all-channel revenue share is ~2%.
  P2 "Price premium +19%" compares our LIST price per kg with the category's
     average PAID price; our paid price premium is only a few percent.
  P3 Promo dependence: revenue on discounted orders rose to ~48% of revenue
     (above the ~40% line) and keeps climbing.
  P4 NPS up (31 -> 38), but full-price 90-day repeat fell for each cohort while
     any-price repeat held: loyalty is being bought with coupons.
Decision: do not approve the +6% list rise now; cut promo depth/frequency first
(raises realised price) and test a price step in one region with a holdout.
Decoys: aided awareness 60% -> 61% correctly called stable; Q3 revenue -9% vs
Q2 correctly called seasonal (same dip last year)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-brand-price-premium"
rng = random.Random(90413)
BRAND = "Larchwood"
LIST_PRICE = 38.0

# ---------------- market panel H1 2026 ----------------
REGIONS = ["North", "East", "Central", "South", "West", "Islands"]
SERVED = ["North", "East", "Central"]
CHANNELS = {"online_specialty": 31.5, "grocery": 17.0, "cafe_retail": 27.0}  # avg paid EUR/kg
REG_SIZE = {"North": 1.0, "East": 0.8, "Central": 1.2, "South": 1.5, "West": 1.3, "Islands": 0.4}
CH_SIZE = {"online_specialty": 60000, "grocery": 520000, "cafe_retail": 150000}  # kg per unit region size
COMP = ["Copperpot", "Fieldhouse", "Morrow & Daughters", "Tinder Roast", "private_label", "other"]
mk = []
for reg in REGIONS:
    for ch, avgp in CHANNELS.items():
        tot = CH_SIZE[ch] * REG_SIZE[reg] * rng.uniform(0.95, 1.05)
        own = 0.0
        if ch == "online_specialty" and reg in SERVED:
            own = tot * rng.uniform(0.23, 0.25)
        elif ch == "grocery" and reg in SERVED:
            own = tot * rng.uniform(0.004, 0.006)
        rest = tot - own
        w = [rng.uniform(0.6, 1.4) for _ in COMP]
        sw = sum(w)
        if own:
            own_p = 33.0 * rng.uniform(0.99, 1.01) if ch == "online_specialty" else 21.0
            mk.append(["2026-H1", reg, ch, BRAND, round(own), round(own * own_p, 2)])
        for b, wi in zip(COMP, w):
            u = rest * wi / sw
            pr = avgp * (0.7 if b == "private_label" else rng.uniform(0.95, 1.08))
            mk.append(["2026-H1", reg, ch, b, round(u), round(u * pr, 2)])

def sm(f, col):
    return sum(r[col] for r in mk if f(r))
served_os = lambda r: r[1] in SERVED and r[2] == "online_specialty"
unit_share_served = sm(lambda r: served_os(r) and r[3] == BRAND, 4) / sm(served_os, 4)
rev_share_served = sm(lambda r: served_os(r) and r[3] == BRAND, 5) / sm(served_os, 5)
rev_share_nat = sm(lambda r: r[3] == BRAND, 5) / sm(lambda r: True, 5)
unit_share_nat = sm(lambda r: r[3] == BRAND, 4) / sm(lambda r: True, 4)
comp_os_price = sm(lambda r: served_os(r) and r[3] != BRAND, 5) / sm(lambda r: served_os(r) and r[3] != BRAND, 4)
cat_os_price = sm(served_os, 5) / sm(served_os, 4)
rank_served = sorted(((sm(lambda r, b=b: served_os(r) and r[3] == b, 4), b) for b in [BRAND] + COMP if b not in ("other",)), reverse=True)

# ---------------- own D2C orders by quarter ----------------
QUARTERS = ["2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"]
SEAS = {"Q1": 0.98, "Q2": 1.0, "Q3": 0.90, "Q4": 1.18}
disc_share_orders = [0.24, 0.27, 0.30, 0.33, 0.40, 0.42, 0.45, 0.48]
ord_rows = []
for i, q in enumerate(QUARTERS):
    orders = int(15800 * (1 + 0.035 * i) * SEAS[q[-2:]] * rng.uniform(0.985, 1.015))
    if q == "2025-Q3":
        orders = int(ord_prev_q2 * 0.895)
    if q == "2026-Q3":
        orders = int(ord_prev_q2 * 0.905)
    if q.endswith("Q2"):
        ord_prev_q2 = orders
    kg = round(orders * rng.uniform(0.99, 1.01) * 0.95, 1)
    d = disc_share_orders[i]
    dorders = int(orders * d)
    depth = 0.20 + 0.01 * i
    list_value = kg * LIST_PRICE
    disc_kg = kg * d * 1.15  # discounted orders are slightly bigger baskets
    dpaid = disc_kg * LIST_PRICE * (1 - depth)
    full_paid = (kg - disc_kg) * LIST_PRICE * 0.995
    paid = dpaid + full_paid
    ord_rows.append([q, orders, kg, round(list_value, 2), round(paid, 2), dorders, round(dpaid, 2)])
paid_price = {r[0]: r[4] / r[2] for r in ord_rows}
promo_share = {r[0]: r[6] / r[4] for r in ord_rows}
rev = {r[0]: r[4] for r in ord_rows}
h1 = [r for r in ord_rows if r[0] in ("2026-Q1", "2026-Q2")]
paid_h1 = sum(r[4] for r in h1) / sum(r[2] for r in h1)
premium_deck = LIST_PRICE / cat_os_price - 1
premium_paid_cat = paid_h1 / cat_os_price - 1
premium_paid_comp = paid_h1 / comp_os_price - 1
q3_qoq = rev["2026-Q3"] / rev["2026-Q2"] - 1
q3_qoq_ly = rev["2025-Q3"] / rev["2025-Q2"] - 1
yoy_q3 = rev["2026-Q3"] / rev["2025-Q3"] - 1

# ---------------- cohorts ----------------
COH = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"]
fp = [0.34, 0.325, 0.31, 0.29, 0.27, 0.255]
anyr = [0.415, 0.41, 0.42, 0.415, 0.41, 0.42]
coh_rows = []
for c, f, a in zip(COH, fp, anyr):
    n = int(rng.uniform(5200, 6400))
    coh_rows.append([c, n, round(n * a), round(n * f)])
fp_rate = {r[0]: r[3] / r[1] for r in coh_rows}
any_rate = {r[0]: r[2] / r[1] for r in coh_rows}

# ---------------- tracker ----------------
trk = []
for wave, n, aw, prom, det in [("2025-09", 1004, 602, 446, 135), ("2026-09", 1011, 617, 497, 113)]:
    trk.append([wave, n, aw, prom, n - prom - det, det])
aw1, aw2 = trk[0][2] / trk[0][1], trk[1][2] / trk[1][1]
nps1 = round(100 * (trk[0][3] - trk[0][5]) / trk[0][1]); nps2 = round(100 * (trk[1][3] - trk[1][5]) / trk[1][1])
se_aw = math.sqrt(aw1 * (1 - aw1) / trk[0][1] + aw2 * (1 - aw2) / trk[1][1])
p_aw = math.erfc(abs(aw2 - aw1) / se_aw / math.sqrt(2))

# ---------------- asserts ----------------
assert 0.22 < unit_share_served < 0.26 and rank_served[0][1] == BRAND, (unit_share_served, rank_served[:2])
assert rev_share_nat < 0.08, rev_share_nat
assert premium_deck > 0.15 and premium_paid_cat < 0.07, (premium_deck, premium_paid_cat)
assert promo_share["2026-Q3"] > 0.45 and promo_share["2024-Q4"] < 0.30
assert all(fp_rate[COH[i]] > fp_rate[COH[i + 1]] for i in range(5)) and max(any_rate.values()) - min(any_rate.values()) < 0.02
assert nps2 - nps1 >= 6
assert p_aw > 0.4
assert -0.11 < q3_qoq < -0.07 and abs(q3_qoq - q3_qoq_ly) < 0.02 and yoy_q3 > 0

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
k = lambda x: f"{x:,.0f}"

slide = f"""# Larchwood Coffee Roasters — Brand health (board pack, October 2026)

## The brand is strong enough to price up

| Signal | Value | Read |
|---|---|---|
| Market position | **#1 brand, {pc(unit_share_served, 0)} market share** | Leader (market panel, H1 2026) |
| Price premium | **+{pc(premium_deck, 0)}** vs category average (EUR {LIST_PRICE:.2f}/kg vs EUR {cat_os_price:.2f}/kg) | Customers pay for the brand |
| NPS | **{nps1} -> {nps2}** (Sep 2025 -> Sep 2026) | Loyalty rising |
| Aided awareness | {pc(aw1, 0)} -> {pc(aw2, 0)} | Stable (change within the survey's +/-3 pt margin) |
| Customers who reorder within 90 days | {pc(any_rate['2025-Q1'], 0)} -> {pc(any_rate['2026-Q2'], 0)} (2025-Q1 vs 2026-Q2 cohorts) | Holding |
| D2C revenue Q3 | EUR {k(rev['2026-Q3'])}, {pc(q3_qoq, 0)} vs Q2 | Seasonal: Q3 2025 was {pc(q3_qoq_ly, 0)} vs Q2 2025; +{pc(yoy_q3, 0)} year on year |

## Proposal for approval
Raise list prices by 6% on all whole-bean and ground SKUs from 1 January 2027. At flat volume this adds about EUR {k(0.06 * sum(rev[q] for q in QUARTERS[-4:]))} revenue a year.

Sources (resources/): market_panel_2026h1.csv (syndicated panel, kg and EUR by region, channel, brand), d2c_orders_by_quarter.csv (our shop), repeat_cohorts.csv (90-day reorder by first-order quarter), brand_tracker.csv (annual tracker).
"""

files = {
    "resources/board_brand_health.md": slide,
    "resources/market_panel_2026h1.csv": to_csv(["period", "region", "channel", "brand", "units_kg", "revenue_eur"], mk),
    "resources/d2c_orders_by_quarter.csv": to_csv(["quarter", "orders", "kg_sold", "list_value_eur", "paid_revenue_eur", "discounted_orders", "discounted_orders_revenue_eur"], ord_rows),
    "resources/repeat_cohorts.csv": to_csv(["first_order_quarter", "new_customers", "reordered_90d", "reordered_90d_full_price"], coh_rows),
    "resources/brand_tracker.csv": to_csv(["wave", "respondents", "aided_aware", "promoters", "passives", "detractors"], trk),
}

prompt = """
This is the brand health page for next week's board pack (resources/board_brand_health.md), with the data behind it in resources/. It asks the board to approve a 6% list price rise from January. Does the page hold up, and should we go ahead with the price rise? Write it up in report.md.
"""

g_recall = f"""
The board page has 4 planted problems. Answer key (computed from the data files):

1. Market share without its denominator. "#1 brand, {pc(unit_share_served, 0)} market share" is Larchwood's share of KG in the online_specialty channel in the 3 regions it serves (North, East, Central). Across all regions and channels Larchwood has {pc(rev_share_nat)} of revenue ({pc(unit_share_nat)} of kg); in the served online channel its revenue share is {pc(rev_share_served)}. Found if report.md says the 24% is a served-market / one-channel / unit share and gives or describes the much smaller national or all-channel share (anything under 8%), or demands the denominator be labelled.
2. Price premium uses list price. The +{pc(premium_deck, 0)} compares Larchwood's LIST price (EUR {LIST_PRICE:.2f}/kg) with the category's average PAID price (EUR {cat_os_price:.2f}/kg, served online specialty). Larchwood's average paid price in H1 2026 was EUR {paid_h1:.2f}/kg (d2c_orders_by_quarter.csv: paid revenue / kg), a premium of {pc(premium_paid_cat)} over the category (or {pc(premium_paid_comp)} over competitors only). Found if report.md says the premium is list vs paid and gives a paid premium in the 3-11% range or the paid price around EUR {paid_h1:.0f}-{paid_h1 + 1:.0f}/kg.
3. Promo dependence. Revenue from discounted orders rose from {pc(promo_share['2024-Q4'], 0)} (2024-Q4) to {pc(promo_share['2026-Q3'], 0)} (2026-Q3) of D2C revenue, above the ~40% level where customers are trained to wait for deals. Found if report.md computes or describes the rising discounted share (any figure from 40-50% for recent quarters, or the trend).
4. NPS up but full-price loyalty down. NPS rose {nps1} -> {nps2}, and the slide's 90-day reorder rate "holds" ({pc(any_rate['2025-Q1'])} -> {pc(any_rate['2026-Q2'])}), but 90-day full-price reorder fell every cohort from {pc(fp_rate['2025-Q1'])} (2025-Q1) to {pc(fp_rate['2026-Q2'])} (2026-Q2). Found if report.md points out the full-price repeat decline (or that repeat is increasingly discount-driven) as contradicting the loyalty story.

List which were found in your reasoning, with evidence.
PASS if at least 3 of the 4 are identified with evidence (a number, a column, a file). Vague remarks ("check the share definition") without the substance do not count.
FAIL if 2 or fewer.
"""

g_decision = f"""
The page asks the board to approve a 6% list price rise from January.

Correct call: do NOT approve the 6% list rise as proposed now. The realised premium is only about {pc(premium_paid_cat, 0)}-{pc(premium_paid_comp, 0)} (not {pc(premium_deck, 0)}), {pc(promo_share['2026-Q3'], 0)} of revenue already comes on discounted orders, and full-price repeat is falling, so a list rise mostly widens the gap to the discounted price or loses full-price buyers. Acceptable main recommendations: hold list price and first reduce discount frequency/depth (which raises realised price); and/or run a controlled price test (one region, channel or SKU set, with a holdout and a stated break-even volume loss) before any across-the-board rise; or postpone the decision until such a test. Any of these is PASS.

Naive wrong answer: approve the 6% rise because the brand is "#1 with {pc(unit_share_served, 0)} share", has a "+{pc(premium_deck, 0)} premium" and NPS is up.

PASS if report.md's main recommendation is not to approve the across-the-board 6% rise now (one of the acceptable alternatives above).
FAIL if report.md recommends approving the 6% list rise as proposed (even with minor caveats), or gives no recommendation.
"""

g_decoy = f"""
Two lines on the page are correct and must not be flagged as problems:
- D1. Aided awareness {pc(aw1, 0)} -> {pc(aw2, 0)} called "stable". With n = {trk[0][1]} and {trk[1][1]}, the change ({pc(aw2 - aw1)}) is well within sampling error (p = {p_aw:.2f}); "stable" is the right reading.
- D2. Q3 D2C revenue {pc(q3_qoq, 0)} vs Q2 called seasonal: Q3 2025 was {pc(q3_qoq_ly, 0)} vs Q2 2025 and Q3 2026 is +{pc(yoy_q3, 0)} year on year.

PASS if report.md does not present the awareness reading or the Q3 dip as a problem (e.g. "awareness is stagnating, a warning sign" or "Q3 revenue is falling") . Saying they are fine, or not mentioning them, is a PASS.
FAIL if report.md treats the flat awareness as a brand weakness requiring action, or presents the Q3 vs Q2 decline as a demand problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: unit share served {unit_share_served:.3f}, rev share national {rev_share_nat:.3f}; premium deck {premium_deck:.3f} vs paid {premium_paid_cat:.3f}; "
      f"promo share {promo_share['2024-Q4']:.2f}->{promo_share['2026-Q3']:.2f}; FP repeat {fp_rate['2025-Q1']:.3f}->{fp_rate['2026-Q2']:.3f}; NPS {nps1}->{nps2}; Q3 {q3_qoq:.3f} vs LY {q3_qoq_ly:.3f}")
