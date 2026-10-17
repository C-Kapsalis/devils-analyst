import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import re

# Northwind Coffee Q3 2026: ESP campaign export + GA4 session export. utm_campaign
# spelling drifts (case, hyphen vs underscore, trailing space), so an exact join on
# campaign name misses most of the VIP campaign's revenue. The clearance blast has the
# most clicks but little revenue; the small VIP segment has ~3.5x its revenue.
NAME = "email-utm-revenue"
rng = random.Random(4202)

# campaign_name, sent, unique_clicks, sessions-per-click, conv rate, AOV, variant shares
CAMPAIGNS = [
    ("summer_clearance_blast", 186400, 7340, 0.016, 21.0,
     {"exact": 0.72, "Summer_Clearance_Blast": 0.18, "summer-clearance-blast": 0.10}),
    ("vip_reserve_preview", 4150, 512, 0.235, 76.0,
     {"exact": 0.14, "VIP_Reserve_Preview": 0.38, "vip-reserve-preview": 0.31, "trail": 0.17}),
    ("new_roast_launch", 61200, 2380, 0.055, 38.0,
     {"exact": 0.55, "New_Roast_Launch": 0.25, "new-roast-launch": 0.20}),
    ("subscription_winback", 24800, 905, 0.072, 44.0,
     {"exact": 0.6, "Subscription-Winback": 0.4}),
    ("brew_guide_july", 91800, 2010, 0.012, 26.0, {"exact": 0.8, "Brew_Guide_July": 0.2}),
    ("brew_guide_august", 92600, 1885, 0.013, 27.0, {"exact": 0.75, "brew-guide-august": 0.25}),
    ("brew_guide_september", 93300, 1940, 0.011, 26.0, {"exact": 0.85, "trail": 0.15}),
    ("cart_reminder_series", 14900, 1120, 0.09, 36.0,
     {"exact": 0.5, "Cart_Reminder_Series": 0.3, "cart-reminder-series": 0.2}),
]

esp = []
ga = []
for name, sent, uc, cr, aov, variants in CAMPAIGNS:
    esp.append([name, sent, uc])
    sessions_total = uc * rng.uniform(1.12, 1.3)
    for var, share in variants.items():
        label = name if var == "exact" else (name + " " if var == "trail" else var)
        s = max(1, round(sessions_total * share * rng.uniform(0.95, 1.05)))
        t = round(s * cr * rng.uniform(0.9, 1.1))
        rev = round(t * aov * rng.uniform(0.92, 1.08), 2)
        ga.append(["newsletter", "email", label, s, t, rev])

# non-email traffic so the export looks like a full GA4 source/medium/campaign table
OTHER = [("google", "organic", "(organic)", 18400, 0.021, 39), ("(direct)", "(none)", "(direct)", 12100, 0.028, 41),
         ("google", "cpc", "brand_search", 6200, 0.045, 37), ("google", "cpc", "generic_coffee_beans", 9800, 0.017, 33),
         ("facebook", "paid_social", "q3_prospecting", 7400, 0.009, 31), ("instagram", "referral", "(referral)", 2100, 0.012, 30)]
for src, med, camp, s, cr, aov in OTHER:
    t = round(s * cr)
    ga.append([src, med, camp, s, t, round(t * aov * rng.uniform(0.95, 1.05), 2)])
rng.shuffle(ga)

norm = lambda x: re.sub(r"[\s\-]+", "_", x.strip().lower())
truth = {}
exact = {}
for src, med, camp, s, t, rev in ga:
    if med != "email":
        continue
    truth.setdefault(norm(camp), [0, 0, 0.0])
    truth[norm(camp)][0] += s; truth[norm(camp)][1] += t; truth[norm(camp)][2] += rev
    exact.setdefault(camp, 0.0)
    exact[camp] += rev
rev_t = {n: truth[n][2] for n, *_ in CAMPAIGNS}
rev_x = {n: exact.get(n, 0.0) for n, *_ in CAMPAIGNS}
clicks = {n: uc for n, _, uc, *_ in CAMPAIGNS}
sent = {n: s for n, s, *_ in CAMPAIGNS}
assert set(truth) == set(rev_t)  # every drifted variant normalises onto an ESP name

rank_t = sorted(rev_t, key=rev_t.get, reverse=True)
rank_x = sorted(rev_x, key=rev_x.get, reverse=True)
rank_c = sorted(clicks, key=clicks.get, reverse=True)
V, C = "vip_reserve_preview", "summer_clearance_blast"
assert rank_t[0] == V and rank_c[0] == C and rank_x[0] != V
assert 3.0 <= rev_t[V] / rev_t[C] <= 4.2, rev_t[V] / rev_t[C]
assert rev_x[V] < 0.25 * rev_t[V]
tot_t = sum(rev_t.values()); tot_x = sum(rev_x.values())
assert tot_x < 0.8 * tot_t

money = lambda x: f"${x:,.0f}"
print(f"{NAME}: truth best {V} {money(rev_t[V])} vs clearance {money(rev_t[C])}; exact-join best {rank_x[0]}; clicks best {rank_c[0]}")

prompt = """
We're Northwind Coffee. Which of last quarter's email campaigns performed best? We want to do more of it. resources/esp_campaigns.csv is the campaign export from our email platform (July-September 2026) and resources/ga4_sessions.csv is GA4 sessions, transactions and revenue by source / medium / campaign for the same period. Write report.md with the campaign ranking and what we should do more of.
"""

tbl = "\n".join(f"- {n}: revenue {money(rev_t[n])}, unique clicks {clicks[n]:,}, sent {sent[n]:,}, revenue per send ${rev_t[n] / sent[n]:.3f}" for n in rank_t)
tbl_x = "\n".join(f"- {n}: {money(rev_x[n])}" for n in rank_x)

g1 = f"""
Ground truth (GA4 email revenue joined to ESP campaigns after normalising the utm_campaign spelling: lower-case, trim spaces, treat hyphens and underscores as the same), ranked by revenue:
{tbl}

The best campaign is vip_reserve_preview: {money(rev_t[V])} revenue from only {clicks[V]:,} unique clicks, about {rev_t[V] / rev_t[C]:.1f}x the revenue of summer_clearance_blast ({money(rev_t[C])}), which has the most clicks ({clicks[C]:,}).

Wrong answers produced by common mistakes:
- Ranking by clicks picks summer_clearance_blast.
- Joining on the exact campaign string drops the drifted rows (e.g. "VIP_Reserve_Preview", "vip-reserve-preview", "vip_reserve_preview " with a trailing space). Exact-join revenue:
{tbl_x}
  which puts {rank_x[0]} first and shows vip_reserve_preview at only {money(rev_x[V])}.

PASS if report.md names vip_reserve_preview as the best-performing campaign (on revenue, revenue per click, or revenue per send) AND recommends doing more of that kind of targeted/VIP send.
FAIL if report.md names summer_clearance_blast (or any campaign other than vip_reserve_preview) as the best, or ranks campaigns by clicks/sessions as the measure of performance.
"""

g2 = f"""
PASS if report.md reports revenue for vip_reserve_preview within 5% of {money(rev_t[V])} AND revenue for summer_clearance_blast within 5% of {money(rev_t[C])}. These figures require combining all spelling variants of each campaign name in ga4_sessions.csv.
FAIL if vip_reserve_preview revenue is shown near the exact-match-only figure {money(rev_x[V])} (or anything below {money(0.8 * rev_t[V])}), or if either figure is missing or outside 5%.
"""

g3 = f"""
Total email revenue across the eight ESP campaigns, after merging spelling variants, is {money(tot_t)}. An exact-string join only finds {money(tot_x)} ({100 * tot_x / tot_t:.0f}%).
PASS if report.md either states total email campaign revenue within 5% of {money(tot_t)}, or explicitly notes that GA4 campaign names have inconsistent spelling/case/hyphenation that had to be merged (or flags this as a tracking issue to fix).
FAIL if it reports total email revenue near {money(tot_x)} or otherwise shows no awareness that rows with variant campaign spellings were dropped.
"""

write_case(NAME, {"resources/esp_campaigns.csv": to_csv(["campaign_name", "sent", "unique_clicks"], esp),
                  "resources/ga4_sessions.csv": to_csv(["session_source", "session_medium", "session_campaign", "sessions", "transactions", "revenue"], ga)},
           prompt, [("best-campaign", 3, g1), ("normalised-revenue", 2, g2), ("join-coverage", 1, g3)])
