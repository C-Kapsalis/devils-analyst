"""Larkspur Home (UK online homeware store): where should next quarter's Google Shopping
budget go? Product-level Q3 export, catalogue with costs, conversion-action settings.

Planted subtle problems (5):
 P1 ROAS ranking ignores margin: phone & tech accessories top the ROAS table but carry
    ~25% margin; kitchen has the lowest ROAS and the best profit per pound (decision-changing).
 P2 Conversion value is the order total incl. 20% VAT and shipping (conversion_actions.csv
    setting), while catalogue prices are ex VAT: reported ROAS is ~25% too high, which by
    itself flips accessories from profit to loss.
 P3 Return rates differ: bedding ~26% vs accessories 4%; bedding's profit is much lower than
    its ROAS suggests.
 P4 Thin sample: the LED strip has ROAS ~14 on 3 conversions; "scale it" is noise.
 P5 Stock: the most profitable SKU has ~1 week of cover, so
    more budget there needs a restock first.
Decoys (2): the stand mixer has by far the highest CPC (it is a GBP 349 item and profitable);
kitchen's conversion rate is lower than accessories' (expected for higher-priced items).
Decision: shift budget out of accessories into kitchen (and lighting), not the reverse.
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-commerce-shopping-budget"
rng = random.Random(61402)

VAT, SHIP_CHARGE, PICKPACK, RET_HANDLING = 0.20, 4.95, 2.40, 6.0

# category: (target reported ROAS, margin ex VAT, return rate, cvr, units per order)
CATS = {
    "Phone & Tech Accessories": (6.2, 0.25, 0.04, 0.042, 1.30),
    "Small Appliances":        (4.4, 0.31, 0.09, 0.016, 1.02),
    "Bedding":                 (3.9, 0.50, 0.26, 0.019, 1.15),
    "Lighting":                (3.7, 0.44, 0.10, 0.021, 1.10),
    "Kitchen":                 (3.1, 0.60, 0.05, 0.017, 1.08),
}
SKUS = {
    "Phone & Tech Accessories": [("USB-C braided cable 2m", 12.49), ("65W GaN charger", 29.99), ("MagSafe car mount", 19.99),
                                 ("Wireless charging pad", 22.49), ("Phone case clear", 9.99), ("Power bank 20000mAh", 34.99)],
    "Small Appliances": [("Tilt-head stand mixer", 349.00), ("Air fryer 5.5L", 109.00), ("Electric kettle glass", 44.99),
                         ("Hand blender set", 54.99), ("4-slice toaster", 59.99), ("Cordless handheld vacuum", 129.00)],
    "Bedding": [("Linen duvet cover double", 89.00), ("Percale sheet set king", 74.00), ("Waffle blanket", 59.00),
                ("Down-alternative pillow pair", 39.00), ("Mattress topper double", 119.00), ("Cotton throw", 45.00)],
    "Lighting": [("Rattan pendant shade", 49.00), ("Brass table lamp", 79.00), ("Floor lamp arc", 139.00),
                 ("Smart bulb 3-pack", 34.99), ("LED strip 5m", 24.99), ("Outdoor wall light", 59.00)],
    "Kitchen": [("Ashby 7-piece knife block", 129.00), ("Cast iron casserole 26cm", 99.00), ("Ceramic pan set 3pc", 89.00),
                ("Bamboo chopping board set", 34.00), ("Glass storage jars 6pc", 29.00), ("Linen tea towels 4pc", 22.00)],
}

products = []
iid = 41000
for cat, skus in SKUS.items():
    troas, margin, rr, cvr, upo = CATS[cat]
    for title, price in skus:
        iid += 7
        clicks = int(rng.uniform(2600, 9000))
        c_cvr = cvr * rng.uniform(0.85, 1.15)
        conv = max(1, round(clicks * c_cvr))
        u = upo * rng.uniform(0.95, 1.05)
        val_per_conv = price * (1 + VAT) * u + SHIP_CHARGE
        conv_value = round(conv * val_per_conv * rng.uniform(0.98, 1.02), 2)
        cost = round(conv_value / (troas * rng.uniform(0.9, 1.1)), 2)
        m = margin * rng.uniform(0.94, 1.06)
        products.append(dict(item_id=f"LH-{iid}", title=title, cat=cat, price=price, unit_cost=round(price * (1 - m), 2),
                             rr=round(rr * rng.uniform(0.85, 1.15), 3), clicks=clicks, conv=conv, conv_value=conv_value,
                             cost=cost, upo=u))

# special: thin-sample LED strip
led = next(p for p in products if p["title"] == "LED strip 5m")
led["clicks"] = 64
led["conv"] = 3
led["conv_value"] = round(3 * (led["price"] * 1.2 * 1.1 + SHIP_CHARGE), 2)
led["cost"] = round(led["conv_value"] / 14.2, 2)
# stand mixer: high CPC decoy
mixer = next(p for p in products if p["title"] == "Tilt-head stand mixer")
mixer["unit_cost"] = round(mixer["price"] * 0.62, 2)   # better margin than its category

for p in products:
    p["impr"] = int(p["clicks"] / rng.uniform(0.006, 0.014))
    p["units"] = p["conv"] * p["upo"]
    p["rev_ex"] = (p["conv_value"] - SHIP_CHARGE * p["conv"]) / (1 + VAT)
    kept = 1 - p["rr"]
    p["contrib"] = (p["rev_ex"] * kept - p["unit_cost"] * p["units"] * kept - PICKPACK * p["conv"]
                    - RET_HANDLING * p["conv"] * p["rr"] - p["cost"])
    p["naive_vat_profit"] = p["conv_value"] * (1 - p["unit_cost"] / p["price"]) - p["cost"]  # margin applied to reported value
    p["roas"] = p["conv_value"] / p["cost"]
    p["cpc"] = p["cost"] / p["clicks"]

# stock (knife block = most profitable SKU, ~1 week cover)
top = max(products, key=lambda p: p["contrib"])
for p in products:
    weekly = p["units"] / 13 * rng.uniform(1.6, 2.2)  # all channels
    cover = rng.uniform(4, 12)
    if p is top:
        cover = 1.1
    p["weekly_units"] = round(weekly)
    p["stock"] = int(round(weekly * cover))

cats = {}
for cat in CATS:
    ps = [p for p in products if p["cat"] == cat]
    cost = sum(p["cost"] for p in ps)
    cats[cat] = dict(cost=cost, value=sum(p["conv_value"] for p in ps), contrib=sum(p["contrib"] for p in ps),
                     naive_vat=sum(p["naive_vat_profit"] for p in ps), rev_ex=sum(p["rev_ex"] for p in ps),
                     conv=sum(p["conv"] for p in ps), clicks=sum(p["clicks"] for p in ps),
                     rr=sum(p["rr"] * p["rev_ex"] for p in ps) / sum(p["rev_ex"] for p in ps))
    c = cats[cat]
    c["roas"] = c["value"] / c["cost"]
    c["roas_ex"] = c["rev_ex"] / c["cost"]
    c["poas"] = c["contrib"] / c["cost"]      # contribution after ads per GBP of ad spend
    c["cvr"] = c["conv"] / c["clicks"]
    c["margin"] = 1 - sum(p["unit_cost"] * p["units"] for p in ps) / sum(p["price"] * p["units"] for p in ps)

by_roas = sorted(cats, key=lambda k: -cats[k]["roas"])
by_poas = sorted(cats, key=lambda k: -cats[k]["poas"])
acc, kit, bed = cats["Phone & Tech Accessories"], cats["Kitchen"], cats["Bedding"]
total_cost = sum(c["cost"] for c in cats.values())
total_value = sum(c["value"] for c in cats.values())
total_rev_ex = sum(c["rev_ex"] for c in cats.values())
vat_inflation = total_value / total_rev_ex - 1

# ---------- asserts ----------
assert by_roas[0] == "Phone & Tech Accessories" and by_roas[-1] == "Kitchen", by_roas
assert by_poas[0] == "Kitchen", by_poas
assert acc["contrib"] < 0 < acc["naive_vat"], (acc["contrib"], acc["naive_vat"])   # VAT error alone flips accessories
assert kit["contrib"] > 0 and kit["poas"] > 0.15
assert bed["roas"] > kit["roas"] and bed["poas"] < kit["poas"] * 0.6
assert led["roas"] > 12 and led["conv"] == 3
assert mixer["cpc"] == max(p["cpc"] for p in products) and mixer["contrib"] > 0
assert kit["cvr"] < acc["cvr"]
assert 0.22 < vat_inflation < 0.30

gbp = lambda x: ("-" if x < 0 else "") + f"£{abs(x):,.0f}"

export = to_csv(["item_id", "product_title", "product_type_l1", "impressions", "clicks", "cost", "conversions", "conv_value"],
                [[p["item_id"], p["title"], p["cat"], p["impr"], p["clicks"], p["cost"], p["conv"], p["conv_value"]] for p in products])
catalog = to_csv(["item_id", "product_title", "price_ex_vat", "unit_cost", "return_rate_90d", "stock_on_hand", "avg_weekly_units_all_channels"],
                 [[p["item_id"], p["title"], p["price"], p["unit_cost"], p["rr"], p["stock"], p["weekly_units"]] for p in products])
actions = to_csv(["conversion_action", "source", "category", "include_in_conversions", "count", "value_setting", "click_through_window_days"], [
    ["Purchase (website)", "Google tag", "Purchase", "Yes", "Every", "Use transaction-specific value: dataLayer ecommerce.value (order total incl. VAT and delivery)", 30],
    ["Add to basket", "Google tag", "Add to cart", "No", "Every", "Don't use a value", 30],
    ["Newsletter sign-up", "Google tag", "Sign-up", "No", "One", "Don't use a value", 30],
])
plan = f"""# Shopping plan draft (performance marketing, 6 Oct 2026)

Q3 Google Shopping: spend {gbp(total_cost)}, conversion value {gbp(total_value)}, ROAS {total_value / total_cost:.2f}.

| product_type_l1 | ROAS |
|---|---|
""" + "\n".join(f"| {k} | {cats[k]['roas']:.2f} |" for k in by_roas) + f"""

Draft for Q4 (budget +20%): put the extra into Phone & Tech Accessories (best ROAS) and the
LED strip 5m (ROAS {led['roas']:.1f}), trim Kitchen (lowest ROAS).
"""

files = {
    "resources/google_shopping_products_q3_2026.csv": export,
    "resources/product_catalogue.csv": catalog,
    "resources/conversion_actions.csv": actions,
    "resources/q4_shopping_plan_draft.md": plan,
}

prompt = """
I run paid for Larkspur Home (UK homeware, online only). Q4 Google Shopping budget goes up 20% and I need to say where it goes. resources/ has the Q3 product-level Shopping export, our product catalogue (prices are ex VAT; unit cost is landed cost), the conversion actions page from Google Ads, and the draft plan my colleague wrote. Pick and pack costs us about £2.40 an order and handling a return about £6.

Where should next quarter's Shopping budget go, and is the draft plan right? Write it up in report.md with the numbers.
"""

rows_txt = "\n".join(f"- {k}: reported ROAS {cats[k]['roas']:.2f}, ROAS on revenue ex VAT/delivery {cats[k]['roas_ex']:.2f}, margin {100 * cats[k]['margin']:.0f}%, return rate {100 * cats[k]['rr']:.0f}%, contribution after ad spend {gbp(cats[k]['contrib'])} ({cats[k]['poas']:+.2f} per £1 of spend)"
                     for k in by_poas)

recall = f"""
Ground truth by product type, Q3 (computed from the files; pick/pack £2.40 per order, £6 per return):
{rows_txt}

The data contains 5 planted problems:
1. Ranking on ROAS ignores margin. Accessories have the highest reported ROAS ({acc['roas']:.2f}) but ~{100 * acc['margin']:.0f}% margin; Kitchen has the lowest ROAS ({kit['roas']:.2f}) but ~{100 * kit['margin']:.0f}% margin and the best contribution per £ of spend. Found if the report ranks or judges product types on margin/profit (POAS, break-even ROAS, contribution) and shows accessories are weak or loss-making despite top ROAS.
2. Conversion value includes VAT and delivery. conversion_actions.csv says the Purchase value is "order total incl. VAT and delivery", while catalogue prices are ex VAT: reported revenue is about {100 * vat_inflation:.0f}% higher than revenue ex VAT/delivery. Found if the report notes the VAT (and/or delivery) inclusion and adjusts or flags ROAS as overstated.
3. Returns differ by product type. Bedding returns ~{100 * bed['rr']:.0f}% vs accessories ~{100 * acc['rr']:.0f}%, so bedding's ROAS ({bed['roas']:.2f}) overstates its profit (contribution {bed['poas']:+.2f} per £ vs Kitchen {kit['poas']:+.2f}). Found if the report uses return_rate_90d to discount revenue or profit, naming bedding's high return rate.
4. Thin sample. LED strip 5m: ROAS {led['roas']:.1f} from {led['conv']} conversions and {led['clicks']} clicks; the draft plan wants to scale it. Found if the report says this is too few conversions to act on.
5. Stock cover. The most profitable SKU, {top['title']}, has {top['stock']} units on hand vs ~{top['weekly_units']} sold per week (about one week of cover). Found if the report flags the low stock of this SKU before adding budget to it.

In your reasoning list which of the 5 the report identifies with evidence (a number, a column or a quote).
PASS if at least 3 of the 5 are identified with evidence. FAIL otherwise.
"""

decision = f"""
Ground truth: ranked on contribution after ad spend (revenue ex VAT and delivery, minus landed cost, returns, pick/pack and ad cost), the order is {", ".join(by_poas)}. Phone & Tech Accessories LOSE money ({gbp(acc['contrib'])} in Q3, {acc['poas']:+.2f} per £) despite the best ROAS; Kitchen earns the most per £ ({kit['poas']:+.2f}) despite the lowest ROAS. Even applying the margin to the VAT-inclusive conversion value would make accessories look profitable ({gbp(acc['naive_vat'])}), so only the ex-VAT view gets this right.

The naive answer (the draft plan) puts the extra budget into Accessories and the LED strip and trims Kitchen, because it ranks on ROAS.

PASS if report.md's main recommendation moves budget toward Kitchen (optionally also Lighting or other margin-positive lines) and away from, or at least not into, Phone & Tech Accessories, and rejects the draft's plan to trim Kitchen.
FAIL if it recommends adding budget to Accessories, trimming Kitchen, or scaling the LED strip as the main move, or if it ranks product types on ROAS alone.
"""

decoys = f"""
Two things look odd but are fine and must not be flagged as problems:
- D1. The Tilt-head stand mixer has by far the highest CPC (£{mixer['cpc']:.2f}). It is a £349 item with a good margin and positive contribution after ads ({gbp(mixer['contrib'])}); a high CPC on an expensive item is not overbidding.
- D2. Kitchen's conversion rate ({100 * kit['cvr']:.1f}%) is lower than Accessories' ({100 * acc['cvr']:.1f}%). Higher-priced, considered purchases convert less often; this is not a landing-page or feed problem.

PASS if report.md does not recommend cutting or bid-capping the stand mixer because of its CPC and does not present Kitchen's lower conversion rate as a problem to fix.
FAIL if it does either.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, recall), ("decision", 3, decision), ("no-false-alarms", 2, decoys)])
print(f"{NAME}: roas order {by_roas}; poas order {by_poas}; acc contrib {acc['contrib']:,.0f} (naive-vat {acc['naive_vat']:,.0f}); "
      f"kitchen poas {kit['poas']:.2f}; bedding poas {bed['poas']:.2f}; vat infl {vat_inflation:.3f}; led {led['roas']:.1f}; top {top['title']}")
