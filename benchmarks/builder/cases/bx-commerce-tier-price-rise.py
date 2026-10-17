"""Halden Audio (headphones, own store + Amazon): the Better tier went from $129 to $145 on
the store on 6 Jul 2026; store units for Better fell ~30% (Q3 vs Q2) and the team wants to
roll it back before Q4.

Planted subtle problems (5):
 P1 Seasonality: Q3 is always weaker; in 2025 (no price change) store Better Q3/Q2 = ~0.89.
 P2 Stock-outs: store Better was out of stock 9 days in August (inventory file); part of the
    drop is lost availability, not price response (P1+P2 decide the verdict).
 P3 Amazon price not moved: Better stayed $129 on Amazon and Amazon Better units rose vs the
    2025 pattern; buyers moved to the lower-contribution channel. Fix parity.
 P4 Trade-down: store Good units rose vs the 2025 pattern after the change; those buyers were
    kept, so judge all tiers together.
 P5 unit_economics.csv "gross_margin_pct" excludes fulfilment and card fees; the break-even
    volume loss must use contribution (PV ~0.52), not 62.8%.
Decoys (2): Amazon Prime Day spikes (both years); store average selling prices sit ~2% below
list in every period (welcome code), before and after.
Decision: keep $145 on the store and raise Amazon Better to parity. Naive: roll back.
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-commerce-tier-price-rise"
rng = random.Random(70626)

START = dt.date(2025, 4, 7)
WEEKS = [START + dt.timedelta(7 * i) for i in range(78)]          # to 2026-09-28
CHANGE = dt.date(2026, 7, 6)
PRIME = {dt.date(2025, 7, 7), dt.date(2026, 7, 13)}
TIERS = {"Good": ("HA-GD-200", 79.0, 31.0), "Better": ("HA-BT-300", 129.0, 48.0), "Best": ("HA-BS-500", 199.0, 77.0)}
NEW_BETTER = 145.0
BASE = {("store", "Good"): 300, ("store", "Better"): 420, ("store", "Best"): 140,
        ("amazon", "Good"): 180, ("amazon", "Better"): 200, ("amazon", "Best"): 60}
FULFIL, CARD, CODE_SHARE = 9.0, 0.029, 0.20      # store: 20% of orders use a 10% welcome code
AMZ_REF, AMZ_FBA = 0.15, 7.80
STOCKOUT = {dt.date(2026, 8, 10): 4, dt.date(2026, 8, 17): 5}  # store Better days out of stock


def season(d):
    q3 = d.month in (7, 8, 9)
    return 0.89 if q3 else 1.0


rows = []
for w in WEEKS:
    trend = 1 + 0.08 * (w - START).days / 365
    post = w >= CHANGE
    for (ch, tier), b in BASE.items():
        lvl = b * trend * season(w)
        if ch == "amazon" and w in PRIME:
            lvl *= 1.8
        if post:
            base_better = BASE[("store", "Better")] * trend * season(w)
            if (ch, tier) == ("store", "Better"):
                lvl *= 0.88                                  # true price response
            if (ch, tier) == ("amazon", "Better"):
                lvl += 0.07 * base_better                     # leaked to Amazon at $129
            if (ch, tier) == ("store", "Good"):
                lvl += 0.045 * base_better                    # traded down
        instock = 7
        if ch == "store" and tier == "Better" and w in STOCKOUT:
            instock = 7 - STOCKOUT[w]
            lvl *= instock / 7
        units = int(round(lvl * rng.gauss(1, 0.025)))
        sku, list_p, cogs = TIERS[tier]
        if tier == "Better" and ch == "store" and post:
            list_p = NEW_BETTER
        asp = list_p * (1 - 0.10 * CODE_SHARE * rng.uniform(0.9, 1.1)) if ch == "store" else list_p
        rows.append(dict(week=w, ch=ch, tier=tier, sku=sku, list=list_p, units=units, rev=round(units * asp, 2), instock=instock, cogs=cogs))


def contrib(r):
    if r["ch"] == "store":
        return r["rev"] * (1 - CARD) - r["units"] * (r["cogs"] + FULFIL)
    return r["rev"] * (1 - AMZ_REF) - r["units"] * (r["cogs"] + AMZ_FBA)


def window(y, q):
    if q == 2:
        a, b = dt.date(y, 4, 6 if y == 2026 else 7), dt.date(y, 7, 5 if y == 2026 else 6)
    else:
        a, b = dt.date(y, 7, 6 if y == 2026 else 7), dt.date(y, 10, 4 if y == 2026 else 5)
    return [r for r in rows if a <= r["week"] < b]


def tot(rs, f=lambda r: True, key="units"):
    return sum((contrib(r) if key == "c" else r[key]) for r in rs if f(r))


sb = lambda r: r["ch"] == "store" and r["tier"] == "Better"
ab = lambda r: r["ch"] == "amazon" and r["tier"] == "Better"
sg = lambda r: r["ch"] == "store" and r["tier"] == "Good"

q2_25, q3_25, q2_26, q3_26 = window(2025, 2), window(2025, 3), window(2026, 2), window(2026, 3)
assert len({r["week"] for r in q2_26}) == 13 and len({r["week"] for r in q3_26}) == 13
assert len({r["week"] for r in q2_25}) == 13 and len({r["week"] for r in q3_25}) == 13

raw_drop = tot(q3_26, sb) / tot(q2_26, sb) - 1
seas = tot(q3_25, sb) / tot(q2_25, sb)
seas_adj = (1 + raw_drop) / seas - 1
# stock-adjusted: scale stock-out weeks to a full week
q3_26_sb_adj = sum(r["units"] * 7 / r["instock"] for r in q3_26 if sb(r))
stock_seas_adj = q3_26_sb_adj / tot(q2_26, sb) / seas - 1
stockout_days = sum(STOCKOUT.values())
raw_rev = tot(q3_26, sb, "rev") / tot(q2_26, sb, "rev") - 1

amz_b = (tot(q3_26, ab) / tot(q2_26, ab)) / (tot(q3_25, ab) / tot(q2_25, ab)) - 1
good_s = (tot(q3_26, sg) / tot(q2_26, sg)) / (tot(q3_25, sg) / tot(q2_25, sg)) - 1

c_ratio_26 = tot(q3_26, key="c") / tot(q2_26, key="c")
c_ratio_25 = tot(q3_25, key="c") / tot(q2_25, key="c")
did_total = c_ratio_26 / c_ratio_25 - 1
weekly_c_gain = (c_ratio_26 / c_ratio_25 - 1) * tot(q2_26, key="c") * c_ratio_25 / 13

store_b_asp_pre = tot(q2_26, sb, "rev") / tot(q2_26, sb)
store_b_asp_post = tot(q3_26, sb, "rev") / tot(q3_26, sb)
pv_store_b = (store_b_asp_pre * (1 - CARD) - 48 - FULFIL) / store_b_asp_pre
gm_quoted = (129 - 48) / 129
k = NEW_BETTER / 129 - 1
be_loss = k / (pv_store_b + k)
be_loss_gm = k / (gm_quoted + k)
c_unit_store = store_b_asp_post * (1 - CARD) - 48 - FULFIL
c_unit_amz = 129 * (1 - AMZ_REF) - 48 - AMZ_FBA
c_unit_amz_145 = 145 * (1 - AMZ_REF) - 48 - AMZ_FBA

# ---------- asserts ----------
assert raw_drop < -0.25, raw_drop
assert raw_rev < -0.12, raw_rev
assert -0.24 < seas_adj < -0.15 and stock_seas_adj > -0.15, (seas_adj, stock_seas_adj)
assert stock_seas_adj > -be_loss, (stock_seas_adj, be_loss)
assert amz_b > 0.05 and good_s > 0.04, (amz_b, good_s)
assert did_total > 0.0, did_total
assert c_unit_store > c_unit_amz + 20
asp_gap_pre = 1 - store_b_asp_pre / 129
asp_gap_post = 1 - store_b_asp_post / NEW_BETTER
assert abs(asp_gap_pre - asp_gap_post) < 0.004 and 0.015 < asp_gap_pre < 0.025

usd = lambda x: ("-" if x < 0 else "") + f"${abs(x):,.0f}"
pc = lambda x, d=0: f"{100 * x:+.{d}f}%"
pp = lambda x, d=0: f"{100 * x:.{d}f}%"

sales = to_csv(["week_start", "channel", "sku", "tier", "list_price", "units", "net_revenue"],
               [[r["week"].isoformat(), r["ch"], r["sku"], r["tier"], r["list"], r["units"], r["rev"]] for r in rows])
inv = to_csv(["week_start", "location", "sku", "days_in_stock", "units_on_hand_week_start"],
             [[r["week"].isoformat(), "store_warehouse" if r["ch"] == "store" else "amazon_fba", r["sku"], r["instock"],
               (0 if r["instock"] < 7 and r["week"] in STOCKOUT and STOCKOUT[r["week"]] == 5 else int(r["units"] * rng.uniform(2.5, 5)))]
              for r in rows if r["week"] >= dt.date(2026, 4, 6) and r["tier"] == "Better"])
econ = to_csv(["sku", "tier", "list_price_store", "list_price_amazon", "landed_cost", "gross_margin_pct", "store_fulfilment_per_unit",
               "card_fee_pct", "amazon_referral_pct", "amazon_fba_fee_per_unit"],
              [["HA-GD-200", "Good", 79, 79, 31, round((79 - 31) / 79, 3), FULFIL, CARD, AMZ_REF, AMZ_FBA],
               ["HA-BT-300", "Better", 145, 129, 48, round((145 - 48) / 145, 3), FULFIL, CARD, AMZ_REF, AMZ_FBA],
               ["HA-BS-500", "Best", 199, 199, 77, round((199 - 77) / 199, 3), FULFIL, CARD, AMZ_REF, AMZ_FBA]])
note = """gross_margin_pct = (list_price_store - landed_cost) / list_price_store. Better row updated 6 Jul 2026 (was 129 / 0.628).
Store net_revenue is after discount codes (10% welcome code). Amazon net_revenue is the sale price before Amazon fees."""

files = {
    "resources/weekly_sales_by_channel.csv": sales,
    "resources/inventory_weekly.csv": inv,
    "resources/unit_economics.csv": econ,
    "resources/unit_economics_notes.txt": note + "\n",
}

prompt = f"""
On 6 July we raised the price of our Better headphones (Halden Audio, HA-BT-300) from $129 to $145 on our own store. Since then store units for Better are down about {abs(round(100 * raw_drop))}% (Q3 vs Q2) and the sales team wants to go back to $129 before Q4. resources/ has weekly sales by channel and tier since April 2025, weekly inventory for Better, and our unit economics sheet.

Should we roll the price back? Give me a clear recommendation and the numbers behind it in report.md.
"""

recall = f"""
The data contains 5 planted problems. Answer key (computed from the files):

1. Seasonality. Q3 is always weaker: in 2025, with no price change, store Better units in Q3 were {pp(seas)} of Q2. The raw drop of {pc(raw_drop)} is about {pc(seas_adj)} after adjusting for that. Found if the report compares with the same quarters of 2025 (or otherwise adjusts for the seasonal Q3 dip) with a number.
2. Stock-outs. inventory_weekly.csv shows the store warehouse had Better in stock only 3 of 7 days in the week of 10 Aug and 2 of 7 in the week of 17 Aug ({stockout_days} days out of stock). Adjusting for these and seasonality, the price-driven drop is about {pc(stock_seas_adj)}. Found if the report names the stock-out days as part of the drop.
3. Amazon price not raised. Amazon Better is still $129 (list_price column; unit_economics list_price_amazon); Amazon Better units rose about {pc(amz_b)} vs the 2025 Q2-to-Q3 pattern, so some buyers moved to Amazon, where a Better unit earns about {usd(c_unit_amz)} vs {usd(c_unit_store)} on the store. Found if the report identifies the channel price gap / migration to Amazon.
4. Trade-down. Store Good units rose about {pc(good_s)} vs the 2025 pattern after the change: some Better buyers bought Good instead and were kept. Found if the report notes Good-tier gains (or judges all tiers together for that reason).
5. Margin definition. unit_economics.csv gross_margin_pct (62.8% at $129) is (price - landed cost) / price and leaves out store fulfilment ($9) and card fees (2.9%); the contribution margin at $129 after the welcome code is about {pp(pv_store_b)}, so the break-even volume loss for +{pp(k, 1)} is about {pp(be_loss)} (not {pp(be_loss_gm)}). Found if the report builds contribution from the cost lines (fulfilment and fees) rather than using gross_margin_pct as is.

In your reasoning list which of the 5 the report identifies with evidence (a number, a column or a quote).
PASS if at least 3 of the 5 are identified with evidence. FAIL otherwise.
"""

decision = f"""
Ground truth: after adjusting for the normal Q3 dip and the August stock-outs, the price rise cost about {pc(stock_seas_adj)} of store Better units, less than the ~{pp(be_loss)} break-even volume loss for a +{pp(k, 1)} price rise, and each store unit now earns about {usd(c_unit_store)}. Across all tiers and both channels, total contribution in Q3 vs Q2 2026, relative to the same ratio in 2025, is {pc(did_total, 1)} (positive). The leak is Amazon, where Better is still $129: at $145 there an Amazon unit would earn about {usd(c_unit_amz_145)} instead of {usd(c_unit_amz)}.

The naive answer: store Better units {pc(raw_drop)} and store Better revenue {pc(raw_rev)} quarter on quarter, so roll the price back to $129.

PASS if report.md's main recommendation is to keep the $145 store price (not roll back), and it also says to align the Amazon price (raise Amazon Better toward $145 / fix channel parity) or at least identifies the Amazon price gap as the thing to fix. Recommending to keep the price and monitor with a stated metric is acceptable if the Amazon gap is named.
FAIL if it recommends rolling back to $129 (or a cut), or does not give a clear keep/roll-back answer.
"""

prime_25 = tot([r for r in rows if r["week"] == dt.date(2025, 7, 7)], ab)
decoys = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Amazon units spike in the week of 7 Jul 2025 and the week of 13 Jul 2026 (all tiers, about 1.8x). That is Prime Day, which happens every July; it is not a data error and it is not evidence about the store price change on its own.
- D2. Store net revenue per unit is about 2% below list price in every period (about {usd(store_b_asp_pre)} for Better at $129 before, about {usd(store_b_asp_post)} at $145 after): the 10% welcome code used by about a fifth of orders, explained in unit_economics_notes.txt. The new price was applied in full; this is not discount leakage or a failed price change.

PASS if report.md does not call the Prime Day spikes a data error/anomaly to investigate and does not claim the $145 price was not applied or that discounting increased after the change.
FAIL if it does either.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, recall), ("decision", 3, decision), ("no-false-alarms", 2, decoys)])
print(f"{NAME}: raw {raw_drop:.3f} rev {raw_rev:.3f} seas {seas:.3f} seas_adj {seas_adj:.3f} stock+seas {stock_seas_adj:.3f} "
      f"be {be_loss:.3f}/{be_loss_gm:.3f}; amz {amz_b:.3f} good {good_s:.3f}; total DiD {did_total:.3f}; c/unit store {c_unit_store:.1f} amz {c_unit_amz:.1f}")
