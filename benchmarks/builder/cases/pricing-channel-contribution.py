import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "pricing-channel-contribution"
rng = random.Random(55)

COGS = 9.0
DTC_PRICE, AMZ_PRICE, WS_PRICE = 34.0, 29.99, 17.0
SHIP_PER_ORDER, UNITS_PER_ORDER = 6.50, 1.4
REFERRAL, FBA_FEE, AMZ_OTHER = 0.15, 5.60, 0.45
COOP, FREIGHT = 0.04, 0.80
ADS = {"Shopify": 31000.0, "Amazon": 26000.0, "Wholesale": 0.0}
days = [dt.date(2026, 9, 1) + dt.timedelta(days=i) for i in range(30)]

# --- Shopify: daily orders/units/refunds -> payouts
shop_rows, shop_units, shop_orders, shop_ret = [], 0, 0, 0
for d in days:
    units = int(round(rng.gauss(5200 / 30, 12)))
    orders = int(round(units / UNITS_PER_ORDER + rng.gauss(0, 3)))
    ret = sum(1 for _ in range(units) if rng.random() < 0.05)
    charges = round(units * DTC_PRICE, 2)
    refunds = round(-ret * DTC_PRICE, 2)
    fees = round(-(0.029 * charges + 0.30 * orders), 2)
    shop_rows.append([d.isoformat(), "paid", charges, refunds, 0.0, fees, round(charges + refunds + fees, 2)])
    shop_units += units; shop_orders += orders; shop_ret += ret

# --- Amazon: settlement lines per day
amz_rows, amz_units, amz_ret = [], 0, 0
for d in days:
    units = int(round(rng.gauss(9800 / 30, 15)))
    ret = sum(1 for _ in range(units) if rng.random() < 0.09)
    princ = round(units * AMZ_PRICE, 2)
    comm = round(-REFERRAL * princ, 2)
    amz_rows += [
        [d.isoformat(), "Order", "ItemPrice", "Principal", units, princ],
        [d.isoformat(), "Order", "ItemFees", "Commission", units, comm],
        [d.isoformat(), "Order", "ItemFees", "FBAPerUnitFulfillmentFee", units, round(-FBA_FEE * units, 2)],
    ]
    if ret:
        rp = round(ret * AMZ_PRICE, 2)
        amz_rows += [
            [d.isoformat(), "Refund", "ItemPrice", "Principal", ret, -rp],
            [d.isoformat(), "Refund", "ItemFees", "Commission", ret, round(0.8 * REFERRAL * rp, 2)],  # referral refunded less 20% admin fee
        ]
    amz_units += units; amz_ret += ret
amz_rows.append([days[-1].isoformat(), "other-transaction", "other", "Storage Fee", "", round(-0.30 * amz_units, 2)])
amz_rows.append([days[-1].isoformat(), "other-transaction", "other", "Inbound Transportation Fee", "", round(-0.15 * amz_units, 2)])

# --- Wholesale
ws_units = 6100
ws_ret = 61
ws_rev = ws_units * WS_PRICE

channel = to_csv(
    ["channel", "units", "orders", "revenue", "returns", "ad_spend"],
    [
        ["Shopify", shop_units, shop_orders, round(shop_units * DTC_PRICE, 2), shop_ret, ADS["Shopify"]],
        ["Amazon", amz_units, "", round(amz_units * AMZ_PRICE, 2), amz_ret, ADS["Amazon"]],
        ["Wholesale", ws_units, 14, ws_rev, ws_ret, ADS["Wholesale"]],
    ],
)
amazon = to_csv(["posted_date", "transaction_type", "amount_type", "amount_description", "quantity", "amount"], amz_rows)
shopify = to_csv(["payout_date", "status", "charges", "refunds", "adjustments", "fees", "total"], shop_rows)

# --- ground truth contribution (returned units refunded and written off)
shop_net = sum(r[6] for r in shop_rows)
amz_net = sum(r[5] for r in amz_rows)
c = {
    "Shopify": shop_net - SHIP_PER_ORDER * shop_orders - COGS * shop_units - ADS["Shopify"],
    "Amazon": amz_net - COGS * amz_units - ADS["Amazon"],
    "Wholesale": ws_rev - ws_ret * WS_PRICE - COOP * ws_rev - FREIGHT * ws_units - COGS * ws_units,
}
units = {"Shopify": shop_units, "Amazon": amz_units, "Wholesale": ws_units}
rev = {"Shopify": shop_units * DTC_PRICE, "Amazon": amz_units * AMZ_PRICE, "Wholesale": ws_rev}
per_unit = {k: c[k] / units[k] for k in c}
pre_ads = {k: (c[k] + ADS[k]) / units[k] for k in c}
roas = {k: rev[k] / ADS[k] for k in ("Shopify", "Amazon")}
amz_share = rev["Amazon"] / sum(rev.values())

assert max(rev, key=rev.get) == "Amazon" and amz_share > 0.45
assert roas["Amazon"] > 1.7 * roas["Shopify"], "naive ROAS ranking favours Amazon"
assert min(per_unit, key=per_unit.get) == "Amazon" and max(per_unit, key=per_unit.get) == "Shopify"
assert per_unit["Shopify"] > 1.9 * per_unit["Amazon"]
assert max(c, key=c.get) == "Shopify"

prompt = """
Tidepool Bottles sells one product, a $34 insulated water bottle, in three channels: our Shopify store, Amazon FBA, and wholesale to outdoor retailers (who sell it at our $34 list price). resources/ has channel_sales_sept.csv (channel, units, orders, revenue, returns, ad_spend), amazon_settlement_sept.csv and shopify_payouts_sept.csv for September 2026.

Wholesale price is $17 per unit, retailers get a 4% co-op allowance, and freight is $0.80 per unit. Shopify orders cost us $6.50 each to ship. Landed cost is $9 per bottle, and returned bottles are refunded and written off.

Amazon is now our biggest channel. Where should we put our 2027 growth money? Write report.md with the numbers by channel and your recommendation.
"""

table = "\n".join(
    f"- {k}: revenue ${rev[k]:,.0f}, units {units[k]:,}, contribution per unit before ads ${pre_ads[k]:.2f}, after ads ${per_unit[k]:.2f}, monthly contribution ${c[k]:,.0f}"
    for k in c
)

g_rank = f"""
Ground truth (September 2026; contribution = net payout or revenue after refunds and channel fees, minus shipping/freight/co-op, minus $9 landed cost on every unit sold, minus ad spend):
{table}

Amazon is the biggest channel by revenue ({amz_share*100:.0f}% of revenue) and has the best platform ROAS ({roas['Amazon']:.1f}x vs Shopify {roas['Shopify']:.1f}x), but keeps the LEAST per unit (${per_unit['Amazon']:.2f} after ads) because of the lower $29.99 price, 15% referral fee, FBA fees and ~9% returns. Shopify keeps about {per_unit['Shopify']/per_unit['Amazon']:.1f}x as much per unit (${per_unit['Shopify']:.2f}).

Naive answers: ranking channels by revenue or ROAS (Amazon first).

PASS if report.md ranks or compares channels on contribution/profit after fees, returns, product cost and ads (per unit or in total), showing Shopify highest per unit and Amazon lowest (or near-lowest) per unit, with per-unit figures within about 15% of the ground truth.
FAIL if report.md ranks channels by revenue, units or ROAS, or does not deduct Amazon's fees and product cost.
"""

g_conflict = f"""
Ground truth: Amazon sells at $29.99, below both our own store ($34) and the retailers' $34 shelf price, which undercuts our own store and our wholesale partners (channel conflict / price parity risk).

PASS if report.md flags that the Amazon price undercuts the own store and/or the retailers (channel conflict, price parity, MAP).
FAIL if report.md does not mention it.
"""

g_rec = f"""
Correct recommendation: direct growth money first to the own Shopify store (highest contribution per unit, ${per_unit['Shopify']:.2f} vs Amazon ${per_unit['Amazon']:.2f}), ideally tested on marginal returns before scaling; fix Amazon pricing/parity (raise toward $34 or cut fees/returns) before growing it. Do not prioritise Amazon because it is biggest by revenue or ROAS. A recommendation conditioned on measuring contribution per extra unit / incremental return per channel is acceptable.

PASS if report.md directs 2027 growth investment to the own store, or makes channel allocation explicitly conditional on contribution per extra unit (not revenue), and does not put Amazon first on revenue/ROAS grounds.
FAIL if report.md recommends prioritising Amazon because it is the biggest channel or has the best ROAS.
"""

write_case(
    NAME,
    {
        "resources/channel_sales_sept.csv": channel,
        "resources/amazon_settlement_sept.csv": amazon,
        "resources/shopify_payouts_sept.csv": shopify,
    },
    prompt,
    [("contribution-ranking", 3, g_rank), ("price-conflict", 1, g_conflict), ("recommendation", 2, g_rec)],
)
print(f"{NAME}: " + "; ".join(f"{k} rev {rev[k]:,.0f} unit {per_unit[k]:.2f} total {c[k]:,.0f}" for k in c) + f"; ROAS amz {roas['Amazon']:.1f} shop {roas['Shopify']:.1f}")
