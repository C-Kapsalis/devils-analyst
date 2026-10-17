"""Regional growth-budget slide (Copperleaf Teas) built on a retail-audit
sell-out panel, plus an "AI shopper panel".

Planted subtle problems (4):
P1 audit sell-out = opening + deliveries - closing includes shrinkage. The EPOS
   scan check shows Copperleaf's audit-derived units in Coastal 2026 are ~16%
   above scanned sales (3% in 2025, ~2-3% elsewhere): Coastal "growth" is theft.
P2 Midvale's share rise crosses an audit panel change: discounter stores (where
   Copperleaf is weak) left the panel in 2026. Like-for-like (supermarkets) the
   share is flat.
P3 "AI shopper panel" preference 4.6/5 is synthetic: the validation sheet shows
   synthetic means ~0.7 above the human pilot with a third of the spread.
P4 Copperleaf's Coastal shelf price fell ~14% in 2026 (promo-driven): even the
   audited unit growth is bought with price; scanned revenue is down.
Decision: put the growth budget into Riverside (real, scan-confirmed growth),
not Coastal; fix shrinkage with the Coastal retailers.
Naive: Coastal (highest share, fastest audited growth).
Decoys: revenue share above unit share (premium price, fine); Riverside
closing stock above opening (new listings filling the pipeline, fine).
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-research-audit-sellout"
rng = random.Random(70211)

BRANDS = ["Copperleaf", "Brindle", "Vale Farm", "Other brands"]
REGIONS = ["Coastal", "Midvale", "Riverside"]
CHANNELS = ["supermarket", "discounter"]
PERIODS = ["2025-H1", "2026-H1"]

# true (scanned) consumer sales, thousand units
TRUE = {
    ("Coastal", "supermarket"): {"Copperleaf": (300, 296), "Brindle": (310, 312), "Vale Farm": (210, 214), "Other brands": (180, 183)},
    ("Coastal", "discounter"): {"Copperleaf": (40, 39), "Brindle": (90, 92), "Vale Farm": (80, 81), "Other brands": (110, 112)},
    ("Midvale", "supermarket"): {"Copperleaf": (250, 254), "Brindle": (330, 336), "Vale Farm": (240, 243), "Other brands": (200, 204)},
    ("Midvale", "discounter"): {"Copperleaf": (25, 25), "Brindle": (120, 121), "Vale Farm": (110, 112), "Other brands": (150, 152)},
    ("Riverside", "supermarket"): {"Copperleaf": (180, 203), "Brindle": (260, 258), "Vale Farm": (200, 196), "Other brands": (170, 171)},
    ("Riverside", "discounter"): {"Copperleaf": (30, 34), "Brindle": (70, 70), "Vale Farm": (75, 74), "Other brands": (95, 96)},
}
SHRINK_DEFAULT = 0.025
SHRINK = {("Coastal", "Copperleaf", "2026-H1"): 0.20, ("Coastal", "Copperleaf", "2025-H1"): 0.03}
PRICE = {"Copperleaf": 3.60, "Brindle": 2.90, "Vale Farm": 2.70, "Other brands": 2.20}
PRICE_2026 = {("Coastal", "Copperleaf"): 3.10}
STORES = {("Coastal", "supermarket"): 42, ("Coastal", "discounter"): 14, ("Midvale", "supermarket"): 38,
          ("Midvale", "discounter"): 12, ("Riverside", "supermarket"): 34, ("Riverside", "discounter"): 10}
DROPPED = ("Midvale", "discounter", "2026-H1")   # left the audit panel


def shrink(region, brand, period):
    return SHRINK.get((region, brand, period), SHRINK_DEFAULT)


def price(region, brand, period):
    base = PRICE[brand] * (1.0 if period == "2025-H1" else 1.03)
    return round(PRICE_2026.get((region, brand), base) if period == "2026-H1" else base, 2)


audit, epos = [], []
derived = {}
for pi, per in enumerate(PERIODS):
    for reg in REGIONS:
        for ch in CHANNELS:
            if (reg, ch, per) == DROPPED:
                continue
            for b in BRANDS:
                true_k = TRUE[(reg, ch)][b][pi] * 1000
                d = round(true_k / (1 - shrink(reg, b, per)))
                opening = round(true_k * rng.uniform(0.18, 0.24))
                closing = round(opening * rng.uniform(0.95, 1.05))
                if (reg, b, per) == ("Riverside", "Copperleaf", "2026-H1"):
                    closing = round(opening * 1.35)        # new listings: pipeline fill
                deliveries = d + closing - opening
                derived[(per, reg, ch, b)] = d
                audit.append([per, reg, ch, STORES[(reg, ch)], b, opening, deliveries, closing, price(reg, b, per)])

# EPOS scan check on a sample of supermarket stores (about a quarter)
for per in PERIODS:
    for reg in REGIONS:
        for b in BRANDS:
            frac = rng.uniform(0.23, 0.27)
            pi = PERIODS.index(per)
            true_k = TRUE[(reg, "supermarket")][b][pi] * 1000 * frac
            d = true_k / (1 - shrink(reg, b, per)) * rng.uniform(0.995, 1.005)
            epos.append([per, reg, b, round(STORES[(reg, "supermarket")] * frac), round(d), round(true_k)])

# ---------- ground truth ----------
def share(per, reg=None, channels=CHANNELS, src="audit", value=False):
    num = den = 0.0
    for (p, r, c, b), d in derived.items():
        if p != per or (reg and r != reg) or c not in channels:
            continue
        pi = PERIODS.index(p)
        u = d if src == "audit" else TRUE[(r, c)][b][pi] * 1000
        w = price(r, b, p) if value else 1.0
        den += u * w
        if b == "Copperleaf":
            num += u * w
    return num / den


def units(per, reg, src="audit"):
    pi = PERIODS.index(per)
    if src == "audit":
        return sum(d for (p, r, c, b), d in derived.items() if p == per and r == reg and b == "Copperleaf")
    return sum(TRUE[(reg, c)]["Copperleaf"][pi] * 1000 for c in CHANNELS if (reg, c, per) != DROPPED)


ratio = {(e[0], e[1], e[2]): e[5] / e[4] for e in epos}
deck = {}
for reg in REGIONS:
    s25, s26 = share("2025-H1", reg), share("2026-H1", reg)
    g = units("2026-H1", reg) / units("2025-H1", reg) - 1
    deck[reg] = (s25, s26, g)

# corrected: Coastal growth = audit growth x shrink correction (scan ratio)
corr = {}
for reg in REGIONS:
    u25 = units("2025-H1", reg) * ratio[("2025-H1", reg, "Copperleaf")]
    u26 = units("2026-H1", reg) * ratio[("2026-H1", reg, "Copperleaf")]
    corr[reg] = u26 / u25 - 1
mid_lfl25 = share("2025-H1", "Midvale", ["supermarket"])
mid_lfl26 = share("2026-H1", "Midvale", ["supermarket"])
coast_ratio25 = ratio[("2025-H1", "Coastal", "Copperleaf")]
coast_ratio26 = ratio[("2026-H1", "Coastal", "Copperleaf")]
other_ratios = [v for k, v in ratio.items() if not (k[1] == "Coastal" and k[2] == "Copperleaf")]
coast_rev25 = units("2025-H1", "Coastal", "true") * price("Coastal", "Copperleaf", "2025-H1")
coast_rev26 = units("2026-H1", "Coastal", "true") * price("Coastal", "Copperleaf", "2026-H1")
coast_price_chg = price("Coastal", "Copperleaf", "2026-H1") / price("Coastal", "Copperleaf", "2025-H1") - 1
coast_true_share26 = share("2026-H1", "Coastal", src="true")
unit_share_all = share("2026-H1")
value_share_all = share("2026-H1", value=True)
riv = [a for a in audit if a[0] == "2026-H1" and a[1] == "Riverside" and a[4] == "Copperleaf"]

# synthetic validation
SYN = [["brand_preference_copperleaf", "ai_persona_panel", 500, 4.6, 0.34], ["brand_preference_copperleaf", "human_pilot", 150, 3.9, 1.08],
       ["purchase_likelihood_next_month", "ai_persona_panel", 500, 4.3, 0.31], ["purchase_likelihood_next_month", "human_pilot", 150, 3.5, 1.12],
       ["value_for_money", "ai_persona_panel", 500, 4.1, 0.38], ["value_for_money", "human_pilot", 150, 3.4, 1.15]]
mae = sum(abs(SYN[i][3] - SYN[i + 1][3]) for i in range(0, 6, 2)) / 3
vr = sum((SYN[i][4] / SYN[i + 1][4]) ** 2 for i in range(0, 6, 2)) / 3

# ---------- asserts ----------
assert deck["Coastal"][2] > 0.10 and deck["Coastal"][2] > deck["Riverside"][2] + 0.04, deck
assert max(deck, key=lambda r: deck[r][1]) == "Coastal"
assert corr["Coastal"] < 0.0 and corr["Riverside"] > 0.10, corr
assert deck["Midvale"][1] - deck["Midvale"][0] > 0.015 and abs(mid_lfl26 - mid_lfl25) < 0.005, (deck["Midvale"], mid_lfl25, mid_lfl26)
assert coast_ratio26 < 0.83 and coast_ratio25 > 0.95 and min(other_ratios) > 0.95
assert coast_rev26 < coast_rev25 * 0.9
assert value_share_all > unit_share_all
assert riv and all(a[7] > a[5] for a in riv)
assert mae > 0.6 and vr < 0.15

pct = lambda x: f"{100 * x:.1f}%"

files = {}
files["resources/audit_sellout_h1.csv"] = to_csv(
    ["period", "region", "channel", "stores_audited", "brand", "opening_stock_units", "deliveries_units", "closing_stock_units", "avg_shelf_price_gbp"], audit)
files["resources/epos_scan_check.csv"] = to_csv(
    ["period", "region", "brand", "sample_stores", "audit_derived_units_sample_stores", "scanned_units_sample_stores"], epos)
files["resources/ai_shopper_panel_validation.csv"] = to_csv(["item", "source", "n", "mean_1_to_5", "sd"], SYN)
files["resources/audit_method_note.md"] = """# Retail audit: method note (from the audit agency)

- Sell-out per brand = opening stock + deliveries - closing stock, counted in audited stores each half-year.
- Share = brand sell-out / total category sell-out in the audited stores of the region.
- Panel changes: from 2026-H1 the Midvale discounter chain stopped sharing data and its 12 stores left the panel. All other store counts unchanged.
- An EPOS scan check is run each half-year on about a quarter of supermarket stores (epos_scan_check.csv).
"""
files["resources/growth_budget_slide.md"] = f"""# Copperleaf Teas: where should the 2027 growth budget go?

Prepared by Brand team for the leadership meeting. Source: retail audit H1 2026 vs H1 2025.

| Region | Unit share H1 2025 | Unit share H1 2026 | Copperleaf sell-out growth |
|---|---|---|---|
""" + "\n".join(f"| {r} | {pct(deck[r][0])} | {pct(deck[r][1])} | {deck[r][2]:+.0%} |" for r in REGIONS) + f"""

- **Coastal is our strongest and fastest-growing region.** Highest share and the fastest sell-out growth.
- **Midvale is turning:** share up {100 * (deck['Midvale'][1] - deck['Midvale'][0]):.1f} pts.
- **Shoppers back it:** our AI shopper panel (500 personas) rates Copperleaf {SYN[0][3]}/5 on brand preference in Coastal.
- Total unit share across our three regions: {pct(unit_share_all)}; value share {pct(value_share_all)}.

## Recommendation
Put 60% of the GBP 1.5M 2027 growth budget into Coastal (more shelf space, in-store media), 25% into Midvale, 15% into Riverside.
"""

prompt = """
I'm presenting the brand team's growth-budget slide (resources/growth_budget_slide.md) to leadership next week. It's built on our retail audit; the audit export, the agency's method note, the EPOS scan check and the AI shopper panel validation sheet are also in resources/. Where should the 2027 growth budget go, and is there anything in the slide I should fix before I present it? Write it up in report.md.
"""

g_recall = f"""
The materials contain 4 planted problems. Answer key (computed from the files):

1. Audit sell-out includes shrinkage. Sell-out is opening + deliveries - closing, so stolen or damaged stock counts as sales. In epos_scan_check.csv, Copperleaf in Coastal 2026-H1 scanned only {pct(coast_ratio26)} of the audit-derived units (about {100 * (1 - coast_ratio26):.0f}% gap), vs {pct(coast_ratio25)} in 2025-H1 and over 95% for every other brand/region. Corrected for this, Coastal Copperleaf units changed by about {corr['Coastal']:+.0%} (not {deck['Coastal'][2]:+.0%}). Counts as found if report.md uses the EPOS scan vs audit gap for Coastal Copperleaf (quotes a ratio or gap, or a corrected growth figure near {corr['Coastal']:+.0%}) to say Coastal's growth is overstated.
2. Midvale panel change. The method note says Midvale's 12 discounter stores left the panel in 2026; Copperleaf is weak in discounters, so the share rise ({pct(deck['Midvale'][0])} to {pct(deck['Midvale'][1])}) is composition. Like-for-like supermarkets: {pct(mid_lfl25)} vs {pct(mid_lfl26)}, flat. Counts as found if report.md attributes the Midvale rise to the discounter stores leaving the panel (ideally with a like-for-like figure).
3. AI shopper panel is synthetic and miscalibrated. The validation sheet shows synthetic means {SYN[0][3]}, {SYN[2][3]}, {SYN[4][3]} vs human pilot {SYN[1][3]}, {SYN[3][3]}, {SYN[5][3]} (about +{mae:.1f} on a 5-point scale) and SDs around 0.3 vs 1.1. Counts as found if report.md says the 4.6/5 should not be used as shopper evidence because synthetic answers run higher and/or far less varied than the human pilot (quoting a number).
4. Coastal price cut. Copperleaf's Coastal shelf price fell from GBP {price('Coastal', 'Copperleaf', '2025-H1'):.2f} to GBP {price('Coastal', 'Copperleaf', '2026-H1'):.2f} ({coast_price_chg:+.0%}) while other brands/regions rose ~3%. Volume was bought with price; scanned-based Coastal revenue fell about {100 * (1 - coast_rev26 / coast_rev25):.0f}%. Counts as found if report.md notes the Coastal price drop for Copperleaf and that growth/revenue must be read with it.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 problems, each with its evidence (a number, a column, or a quote from the files).
FAIL if fewer than 3 are identified with evidence.
"""

g_decision = f"""
The question: where should the 2027 growth budget (GBP 1.5M) go across Coastal, Midvale and Riverside?

Ground truth. Audited growth: Coastal {deck['Coastal'][2]:+.0%}, Midvale {deck['Midvale'][2]:+.0%}, Riverside {deck['Riverside'][2]:+.0%}. After correcting with the EPOS scan ratios, Copperleaf units: Coastal about {corr['Coastal']:+.0%} (the audited growth is shrinkage, and it came with a {coast_price_chg:+.0%} price cut), Midvale flat like-for-like, Riverside about {corr['Riverside']:+.0%} (scan-confirmed, at a stable price, with new listings). Correct main recommendation: shift the weight of the budget to Riverside (the region with real growth), not Coastal; Coastal needs a shrinkage/loss-prevention and pricing fix rather than more growth money. Splitting with Riverside as the largest share, or explicitly moving budget from Coastal to Riverside, counts.

Naive wrong recommendation: put most of the budget into Coastal (slide: 60% Coastal) because it has the highest share and fastest audited growth.

PASS if report.md's main recommendation gives Riverside the largest share of the growth budget (or clearly prioritises Riverside over Coastal) AND does not keep Coastal as the top priority.
FAIL if report.md keeps Coastal as the main destination of the budget (e.g. endorses the 60/25/15 split), or prioritises Midvale based on its share rise.
"""

g_decoys = f"""
Two features look odd but are fine and must not be presented as problems:
- D1. Copperleaf's value share ({pct(value_share_all)}) is higher than its unit share ({pct(unit_share_all)}). That is expected for a premium-priced brand (Copperleaf's shelf price is the highest in the category) and is not an error.
- D2. In Riverside 2026-H1, Copperleaf's closing stock ({riv[0][7]:,} units in supermarkets) is well above its opening stock ({riv[0][5]:,}). That is stores filling shelves after new listings; the sell-out formula already nets it out, and the EPOS scan check confirms Riverside sales.

PASS if report.md does not present D1 or D2 as an error, inconsistency, or reason to distrust Riverside's growth.
FAIL if it calls the value-above-unit share gap an error or inflation, OR says the Riverside stock build means Riverside's sales/growth are overstated (channel stuffing, sell-in counted as sell-out, etc.).
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoys)])
print(f"{NAME}: deck growth {[(r, round(deck[r][2], 3)) for r in REGIONS]} shares {[(r, round(deck[r][1], 3)) for r in REGIONS]}; corrected {[(r, round(corr[r], 3)) for r in REGIONS]}; "
      f"coastal scan ratio {coast_ratio25:.3f}/{coast_ratio26:.3f}; midvale lfl {mid_lfl25:.3f}->{mid_lfl26:.3f}; coastal rev {coast_rev25:,.0f}->{coast_rev26:,.0f}")
