"""Audit a Google Ads account export (Tidewater Swim, September 2026).

Planted problems (7): newsletter and account sign-ups counted as primary
conversions (MUST); generic campaigns serving brand queries, plus one generic
query in the brand campaign (MUST); zero-sale informational search terms;
a profitable Target CPA campaign capped by budget while an uncapped one runs
over target; a line called efficient whose CPC is above break-even; device
modifiers on Target CPA campaigns credited with savings; plan to move budget
to broad match for cheaper clicks.
Decoys (3): brand CTR ~35% and lowest CPA; -10% mobile modifier on the Manual
CPC Kids campaign (applied as set); brand impression share ~93%."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "audit-google-ads"
rng = random.Random(77311)
AOV, MARGIN, TARGET_CPA = 70.0, 0.45, 30.0
MPS = AOV * MARGIN  # margin per sale 31.50

# kind: brand (brand query), gen (generic query), waste (informational, no sales)
CPC = {"exact": 1.0, "phrase": 1.22, "broad": 0.68}
CVR = {"exact": 0.044, "phrase": 0.046, "broad": 0.012}
TERMS = {
    "Brand - Tidewater Swim": [
        ("tidewater swim", "exact", "brand", 1450), ("tidewater swimwear", "exact", "brand", 820),
        ("tidewater discount code", "exact", "brand", 390), ("tidewater swim returns", "exact", "brand", 160),
        ("swimming costume", "phrase", "gen", 110),
    ],
    "Generic - Swimsuits": [
        ("womens swimsuits", "phrase", "gen", 640), ("one piece swimsuit", "exact", "gen", 520),
        ("chlorine resistant swimsuit", "phrase", "gen", 380), ("racerback swimsuit", "exact", "gen", 260),
        ("tidewater swimsuits", "phrase", "brand", 220), ("tidewater swim sale", "phrase", "brand", 120),
        ("how to wash a swimsuit", "broad", "waste", 150), ("swimsuit model jobs", "broad", "waste", 95),
    ],
    "Generic - Goggles": [
        ("swim goggles", "exact", "gen", 360), ("anti fog swim goggles", "phrase", "gen", 210),
        ("prescription swim goggles", "exact", "gen", 120), ("tidewater goggles", "phrase", "brand", 140),
        ("how to stop goggles fogging", "broad", "waste", 85),
    ],
    "Generic - Kids Swimwear": [
        ("kids swimsuit", "exact", "gen", 520), ("girls swimsuit", "exact", "gen", 410),
        ("boys swim shorts", "exact", "gen", 360), ("toddler swimwear", "phrase", "gen", 240),
        ("free kids swim lessons", "broad", "waste", 130),
    ],
    "Generic - Wetsuits": [
        ("wetsuit", "broad", "gen", 980), ("open water wetsuit", "broad", "gen", 420),
        ("triathlon wetsuit", "broad", "gen", 310), ("second hand wetsuit", "broad", "waste", 260),
        ("wetsuit repair", "broad", "waste", 190), ("wetsuit hire near me", "broad", "waste", 170),
    ],
}
CAMP_CPC = {"Brand - Tidewater Swim": 0.36, "Generic - Swimsuits": 1.05, "Generic - Goggles": 0.72,
            "Generic - Kids Swimwear": 0.93, "Generic - Wetsuits": 0.92}
CAMP_CVR = {"Brand - Tidewater Swim": 1.0, "Generic - Swimsuits": 0.27, "Generic - Goggles": 0.95,
            "Generic - Kids Swimwear": 0.55, "Generic - Wetsuits": 1.0}
CTR = {"brand": 0.42, "gen": 0.055, "waste": 0.03}

term_rows, tr = [], []
for camp, terms in TERMS.items():
    for term, mt, kind, clicks0 in terms:
        clicks = int(clicks0 * rng.uniform(0.92, 1.08))
        if kind == "brand":
            cpc = (0.36 if camp.startswith("Brand") else 0.55) * rng.uniform(0.9, 1.1)
            cvr = 0.13 * rng.uniform(0.9, 1.1)
        else:
            base = CAMP_CPC[camp] if camp != "Brand - Tidewater Swim" else 1.10
            cpc = base * CPC[mt] * rng.uniform(0.93, 1.07)
            cvr = 0.0 if kind == "waste" else CVR[mt] * CAMP_CVR[camp] * rng.uniform(0.9, 1.1)
        cost = round(clicks * cpc, 2)
        pur = int(round(clicks * cvr))
        ctr0 = 0.09 if (camp.startswith("Brand") and kind == "gen") else CTR[kind]
        imps = int(round(clicks / (ctr0 * rng.uniform(0.85, 1.15))))
        tr.append(dict(camp=camp, term=term, mt=mt, kind=kind, clicks=clicks, cost=cost, pur=pur, imps=imps))
        term_rows.append([camp, term, mt, imps, clicks, cost, pur])

CAMPS = list(TERMS)
SETTINGS = {  # bid strategy, daily budget, IS, budget lost, rank lost
    "Brand - Tidewater Swim": ("Manual CPC", 60, 0.93, 0.02, 0.05),
    "Generic - Swimsuits": ("Target CPA", 220, 0.41, 0.0, 0.59),
    "Generic - Goggles": ("Target CPA", None, 0.44, 0.49, 0.07),
    "Generic - Kids Swimwear": ("Manual CPC", 120, 0.52, 0.04, 0.44),
    "Generic - Wetsuits": ("Maximize clicks", 150, 0.47, 0.03, 0.50),
}
agg = {}
for c in CAMPS:
    rs = [t for t in tr if t["camp"] == c]
    agg[c] = dict(clicks=sum(t["clicks"] for t in rs), cost=round(sum(t["cost"] for t in rs), 2),
                  pur=sum(t["pur"] for t in rs), imps=sum(t["imps"] for t in rs))
    agg[c]["nl"] = int(round(agg[c]["clicks"] * (0.012 if c.startswith("Brand") else 0.075) * rng.uniform(0.9, 1.1)))
    agg[c]["acc"] = int(round(agg[c]["clicks"] * (0.010 if c.startswith("Brand") else 0.038) * rng.uniform(0.9, 1.1)))
    agg[c]["val"] = round(agg[c]["pur"] * AOV * rng.uniform(0.95, 1.05), 2)
    agg[c]["allc"] = agg[c]["pur"] + agg[c]["nl"] + agg[c]["acc"]
gog_daily = round(agg["Generic - Goggles"]["cost"] / 30.4 + 0.3, 0)

camp_rows, act_rows = [], []
for c in CAMPS:
    bs, db, iss, bl, rl = SETTINGS[c]
    db = gog_daily if db is None else db
    a = agg[c]
    camp_rows.append([c, "Search", bs, db, a["imps"], a["clicks"], a["cost"], a["allc"], a["val"], iss, bl, rl])
    act_rows += [[c, "Purchase", "TRUE", a["pur"], a["val"]], [c, "Newsletter signup", "TRUE", a["nl"], 0],
                 [c, "Account created", "TRUE", a["acc"], 0]]

bid_rows = [["Generic - Swimsuits", "Mobile", -0.30], ["Generic - Swimsuits", "Tablet", -0.20],
            ["Generic - Goggles", "Mobile", -0.30], ["Generic - Kids Swimwear", "Mobile", -0.10]]

# ---------- ground truth ----------
cost = sum(a["cost"] for a in agg.values())
allc = sum(a["allc"] for a in agg.values())
pur = sum(a["pur"] for a in agg.values())
cpa_all, cpa_pur = cost / allc, cost / pur
gen = [c for c in CAMPS if c.startswith("Generic")]
gen_cost = sum(agg[c]["cost"] for c in gen)
gen_pur = sum(agg[c]["pur"] for c in gen)
gen_allc = sum(agg[c]["allc"] for c in gen)
leak = [t for t in tr if t["camp"] in gen and t["kind"] == "brand"]
leak_cost, leak_pur = sum(t["cost"] for t in leak), sum(t["pur"] for t in leak)
gen_x_cost, gen_x_pur = gen_cost - leak_cost, gen_pur - leak_pur
gen_cpa_pur, gen_cpa_xbrand = gen_cost / gen_pur, gen_x_cost / gen_x_pur
rev_leak = [t for t in tr if t["camp"].startswith("Brand") and t["kind"] == "gen"][0]
waste = [t for t in tr if t["kind"] == "waste"]
waste_cost = sum(t["cost"] for t in waste)
camp_cpa = {c: agg[c]["cost"] / agg[c]["pur"] for c in CAMPS}
gog_rs = [t for t in tr if t["camp"] == "Generic - Goggles" and t["kind"] != "brand"]
gog_xbrand = sum(t["cost"] for t in gog_rs) / sum(t["pur"] for t in gog_rs)
gog, swim, kids = agg["Generic - Goggles"], agg["Generic - Swimsuits"], agg["Generic - Kids Swimwear"]
kids_cpc, kids_cvr = kids["cost"] / kids["clicks"], kids["pur"] / kids["clicks"]
kids_be = MPS * kids_cvr
mt = {}
for m in ("exact", "phrase", "broad"):
    rs = [t for t in tr if t["camp"] in gen and t["mt"] == m]
    mt[m] = dict(clicks=sum(t["clicks"] for t in rs), cost=round(sum(t["cost"] for t in rs), 2), pur=sum(t["pur"] for t in rs),
                 imps=sum(t["imps"] for t in rs))
    mt[m]["cpc"] = mt[m]["cost"] / mt[m]["clicks"]
    mt[m]["cps"] = mt[m]["cost"] / mt[m]["pur"]
mt_rows = [[m, v["imps"], v["clicks"], v["cost"], v["pur"]] for m, v in mt.items()]
brand = agg["Brand - Tidewater Swim"]
brand_ctr = brand["clicks"] / brand["imps"]

# ---------- asserts ----------
assert cpa_pur / cpa_all > 2.2, (cpa_pur, cpa_all)
assert cpa_all < TARGET_CPA * 0.5
assert leak_pur / gen_pur > 0.2, leak_pur / gen_pur
assert gen_cpa_xbrand > TARGET_CPA * 1.15 and gen_cpa_xbrand > gen_cpa_pur * 1.2, (gen_cpa_pur, gen_cpa_xbrand)
assert waste_cost > 500 and all(t["pur"] == 0 for t in waste)
assert camp_cpa["Generic - Goggles"] < TARGET_CPA * 0.85 and gog_xbrand < TARGET_CPA * 0.8, (camp_cpa, gog_xbrand)
assert camp_cpa["Generic - Swimsuits"] > TARGET_CPA * 1.2, camp_cpa
assert gog["cost"] <= gog_daily * 30.4 and gog["cost"] > gog_daily * 30.4 * 0.97
assert kids_cpc > kids_be * 1.15, (kids_cpc, kids_be)
assert mt["broad"]["cpc"] < min(mt["exact"]["cpc"], mt["phrase"]["cpc"])
assert mt["broad"]["cps"] > 2 * max(mt["exact"]["cps"], mt["phrase"]["cps"]), mt
assert SETTINGS["Generic - Kids Swimwear"][0] == "Manual CPC"
assert brand_ctr > 0.33 and camp_cpa["Brand - Tidewater Swim"] == min(camp_cpa.values())

usd = lambda x: f"${x:,.0f}"
usd2 = lambda x: f"${x:,.2f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

notes = f"""# Tidewater Swim: Google Ads handover notes

- Business: online swimwear shop (US). Goal: online purchases. Average order value about ${AOV:.0f}, gross margin {MARGIN:.0%}.
- Target CPA: ${TARGET_CPA:.0f} per purchase.
- Exports cover September 2026 (1-30 September).
- Notes from the previous agency:
  - "Kids Swimwear is one of our efficient lines: clicks under a dollar."
  - "Mobile bid adjustments of -30% on Swimsuits and Goggles saved us money on weaker mobile traffic."
  - "Plan for Q4: shift generic budget toward broad match, which has the cheapest clicks in the account."
"""

files = {
    "resources/account_notes.md": notes,
    "resources/campaigns_sep2026.csv": to_csv(
        ["campaign", "campaign_type", "bid_strategy", "daily_budget", "impressions", "clicks", "cost", "conversions",
         "conv_value", "search_impression_share", "search_budget_lost_impression_share", "search_rank_lost_impression_share"], camp_rows),
    "resources/conversions_by_action_sep2026.csv": to_csv(
        ["campaign", "conversion_action", "include_in_conversions", "conversions", "conv_value"], act_rows),
    "resources/search_terms_sep2026.csv": to_csv(
        ["campaign", "search_term", "keyword_match_type", "impressions", "clicks", "cost", "purchases"], term_rows),
    "resources/match_type_generic_sep2026.csv": to_csv(
        ["keyword_match_type", "impressions", "clicks", "cost", "purchases"], mt_rows),
    "resources/bid_adjustments.csv": to_csv(["campaign", "device", "bid_modifier"], bid_rows),
}

prompt = """
We just took over the Google Ads account for Tidewater Swim from another agency. The September exports and their handover notes are in resources/. Can you audit the account and tell us what's wrong and what we should fix first? Put it in report.md.
"""

g_recall = f"""
The account export contains 7 planted problems. Answer key (September 2026, margin per sale {usd2(MPS)}, target CPA {usd(TARGET_CPA)}):

1. Micro actions counted as conversions. Newsletter signup and Account created are included in Conversions (include_in_conversions TRUE). Account conversions {allc:,}, of which purchases {pur:,}. CPA on all conversions {usd2(cpa_all)}; CPA on purchases {usd2(cpa_pur)}. Counts as found if report.md says only purchases should count as the conversion (or Smart Bidding is optimising toward sign-ups) and gives a purchase CPA within 5% of {usd2(cpa_pur)} or per-campaign purchase CPAs.
2. Brand leakage. Generic campaigns serve brand queries (tidewater swimsuits, tidewater swim sale, tidewater goggles): {usd(leak_cost)} of generic cost and {leak_pur} of {gen_pur} generic purchases ({pc(leak_pur / gen_pur, 0)}). Generic purchase CPA is {usd2(gen_cpa_pur)} as reported but {usd2(gen_cpa_xbrand)} without brand queries. The brand campaign also serves the generic query "swimming costume". Counts as found if report.md flags brand terms inside generic campaigns (brand negatives needed); the reverse case or the ex-brand CPA is a bonus, not required.
3. Search-term waste. Informational or irrelevant terms with zero purchases: {', '.join(t['term'] for t in waste)}; total {usd(waste_cost)}. Counts as found if report.md names at least three of these terms (or the clusters) and recommends negatives; a total within 10% of {usd(waste_cost)} is a bonus.
4. Profitable campaign capped by budget. Generic - Goggles: purchase CPA {usd2(camp_cpa['Generic - Goggles'])} ({usd2(gog_xbrand)} without its brand query, still below target), loses 49% of impression share to budget and spends its full cap ({usd(gog['cost'])} on a {usd(gog_daily)} daily budget), while Generic - Swimsuits is uncapped at a purchase CPA of {usd2(camp_cpa['Generic - Swimsuits'])} (over target) and loses impression share to rank, not budget. Counts as found if report.md recommends more budget for Goggles (or moving budget from Swimsuits to Goggles) citing the budget-lost share.
5. CPC above break-even. Generic - Kids Swimwear is called efficient for clicks under a dollar, but its CPC {usd2(kids_cpc)} is above its break-even CPC of {usd2(kids_be)} (margin {usd2(MPS)} x purchase CVR {pc(kids_cvr, 2)}); purchase CPA {usd2(camp_cpa['Generic - Kids Swimwear'])}. Counts as found if report.md says Kids Swimwear loses money per click or its CPA is above target/margin despite the low CPC.
6. Device modifiers on Target CPA. -30% mobile (and -20% tablet) modifiers sit on Generic - Swimsuits and Generic - Goggles, which use Target CPA; automated bidding does not apply them as set, so the "saved us money" claim is not supported. Counts as found if report.md says these modifiers have little or no effect under Target CPA.
7. Broad match plan. Broad has the lowest CPC ({usd2(mt['broad']['cpc'])}) but the worst cost per sale ({usd2(mt['broad']['cps'])} vs exact {usd2(mt['exact']['cps'])} and phrase {usd2(mt['phrase']['cps'])}), so shifting budget to broad for cheap clicks is wrong. Counts as found if report.md rejects the broad-match plan on cost per sale.

List which ones were found in your reasoning.
PASS if report.md identifies at least 6 of the 7 problems, each with its substance (a vague mention such as "review search terms" does not count).
FAIL if it identifies fewer than 6.
"""

g_rank = f"""
Two problems are Must-fix because they corrupt every number the account is judged and bid on:
- A. Newsletter signup and Account created counted as conversions: purchase CPA {usd2(cpa_pur)}, not {usd2(cpa_all)}.
- B. Brand leakage into generic campaigns: generic purchase CPA without brand queries is {usd2(gen_cpa_xbrand)}, not {usd2(gen_cpa_pur)}.
The lesser problems are: the capped Goggles campaign, Kids Swimwear CPC above break-even, device modifiers on Target CPA, and the broad-match plan. (Search-term waste may sit in either group.)

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its closing "fix first" line (or explicit first priority) names A or B.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), listed after one of the lesser problems, or if the first fix named is something other than A or B.
"""

g_decoy = f"""
The export contains three things that are normal and must not be flagged as problems:
- D1. Brand - Tidewater Swim has a {pc(brand_ctr, 0)} CTR and the lowest purchase CPA ({usd2(camp_cpa['Brand - Tidewater Swim'])}). A 30-50% CTR and a low CPA are normal for brand search.
- D2. Generic - Kids Swimwear has a -10% mobile bid modifier. That campaign uses Manual CPC, so the modifier is applied as set; it is a legitimate setting (unlike the modifiers on the Target CPA campaigns).
- D3. Brand impression share is 93% with only 5% lost to rank. Nothing to fix.

PASS if report.md does not present D1, D2 or D3 as an error or something to fix (saying they are normal or fine is a PASS; suggesting an optional brand incrementality test is a PASS as long as the brand CTR and CPA are not called wrong).
FAIL if it calls the brand CTR or CPA suspicious or wrong, says the Kids Swimwear mobile modifier has no effect or should be removed because of automated bidding, or recommends fixing brand impression share or rank.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: CPA all {cpa_all:.2f} vs purchase {cpa_pur:.2f}; generic {gen_cpa_pur:.2f} vs ex-brand {gen_cpa_xbrand:.2f} "
      f"(leak {leak_pur}/{gen_pur}); waste {waste_cost:.0f}; goggles CPA {camp_cpa['Generic - Goggles']:.2f}, swimsuits {camp_cpa['Generic - Swimsuits']:.2f}; "
      f"kids CPC {kids_cpc:.2f} vs BE {kids_be:.2f}; broad cps {mt['broad']['cps']:.2f} exact {mt['exact']['cps']:.2f} phrase {mt['phrase']['cps']:.2f}")
