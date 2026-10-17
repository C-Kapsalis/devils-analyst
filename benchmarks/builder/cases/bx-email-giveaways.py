"""Breadth: list growth from giveaways, should we run more? (Marram Swimwear, Jan-Sep 2026).

Planted problems (5): giveaway subscribers buy at a fraction of other
sources, so the cost per purchasing subscriber from giveaways is many times
higher (DECISION: no more giveaways as run); the falling program click rate is
a mix shift toward giveaway subscribers, each source's click rate is flat (no
creative overhaul needed); the giveaway form has double opt-in off and its
sign-ups bounce and get cleaned at a high rate (typo domains); "list +40%"
is gross sign-ups, net growth after unsubscribes and cleaning is much lower;
the deck quotes the industry "$36 per $1" as the program's own ROI.
Decoys (2): CTOR in a normal 10-14% band each month; complaint rate under
0.1% every month."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-email-giveaways"
rng = random.Random(81909)
MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]
GIVE_MONTHS = {"2026-03", "2026-06", "2026-09"}
SRC = ["site_popup", "checkout_optin", "giveaway"]
CLICK = {"site_popup": 0.034, "checkout_optin": 0.041, "giveaway": 0.0062}
OPEN = {"site_popup": 0.30, "checkout_optin": 0.34, "giveaway": 0.052}
BUY = {"site_popup": 0.0042, "checkout_optin": 0.0061, "giveaway": 0.00035}   # purchasers per delivered email
UNSUB = {"site_popup": 0.012, "checkout_optin": 0.010, "giveaway": 0.05}    # monthly share of stock
CLEAN = {"site_popup": 0.006, "checkout_optin": 0.005, "giveaway": 0.03}
SENDS = 8
start_stock = {"site_popup": 21000, "checkout_optin": 14000, "giveaway": 0}

stock = dict(start_stock)
gro, eng = [], []
gross_new = 0; net = 0
start_total = sum(start_stock.values())
for m in MONTHS:
    for s in SRC:
        new = {"site_popup": int(rng.uniform(700, 800)), "checkout_optin": int(rng.uniform(420, 500)),
               "giveaway": int(rng.uniform(5000, 5600)) if m in GIVE_MONTHS else 0}[s]
        un = int(stock[s] * UNSUB[s] * rng.uniform(0.9, 1.1))
        cl = int(stock[s] * CLEAN[s] * rng.uniform(0.9, 1.1))
        if s == "giveaway" and m in GIVE_MONTHS:
            cl += int(new * rng.uniform(0.10, 0.13))          # immediate hard bounces from typo domains
        gro.append([m, s, new, un, cl])
        gross_new += new
        stock[s] += new - un - cl
        dv = stock[s] * SENDS
        op = int(dv * OPEN[s] * rng.uniform(0.97, 1.03))
        ck = int(dv * CLICK[s] * rng.uniform(0.96, 1.04))
        pu = int(dv * BUY[s] * rng.uniform(0.95, 1.05))
        comp = int(dv * rng.uniform(0.0003, 0.0006) * (2 if s == "giveaway" else 1))
        eng.append([m, s, dv, op, ck, pu, round(pu * rng.uniform(70, 80), 2), comp])
end_total = sum(stock.values())
net_growth = end_total / start_total - 1
gross_growth = gross_new / start_total

def mt(m, i):
    return sum(r[i] for r in eng if r[0] == m)
cr = {m: mt(m, 4) / mt(m, 2) for m in MONTHS}
ctor = {m: mt(m, 4) / mt(m, 3) for m in MONTHS}
comp_rate = {m: mt(m, 7) / mt(m, 2) for m in MONTHS}
src_cr = {s: [r[4] / r[2] for r in eng if r[1] == s and r[2] > 0] for s in SRC}
def src_tot(s, i):
    return sum(r[i] for r in eng if r[1] == s)
buy_per_sub_month = {s: src_tot(s, 5) / (src_tot(s, 2) / SENDS) for s in SRC}

# giveaway cost: prize + promotion
G_COST = 3 * 6500.0
g_new = sum(r[2] for r in gro if r[1] == "giveaway")
g_purch = src_tot("giveaway", 5)
pop_new = sum(r[2] for r in gro if r[1] == "site_popup")
POP_COST = 9 * 800.0   # popup tool + 10% welcome discount budget, per month
pop_purch = src_tot("site_popup", 5)
cps_g, cps_p = G_COST / g_new, POP_COST / pop_new          # cost per new subscriber
bpk = {k: 1000 * v for k, v in buy_per_sub_month.items()}  # purchasers per 1,000 subscribers per month
cost_per_buyer_g = cps_g / buy_per_sub_month["giveaway"]   # acquisition cost per subscriber-month purchaser
cost_per_buyer_p = cps_p / buy_per_sub_month["site_popup"]
g_clean = sum(r[4] for r in gro if r[1] == "giveaway")
g_unsub = sum(r[3] for r in gro if r[1] == "giveaway")

forms = [["site_popup", "on", "10% welcome code"], ["checkout_optin", "n/a (customer)", "none"], ["giveaway_landing_page", "off", "prize draw entry"]]
dom = [["giveaway", "gmail.com", 6100], ["giveaway", "gmial.com", 212], ["giveaway", "hotmial.com", 148], ["giveaway", "yahoo.com", 2300],
       ["giveaway", "outlook.com", 1500], ["giveaway", "gmail.con", 96], ["giveaway", "other", 3900],
       ["site_popup", "gmail.com", 6600], ["site_popup", "gmial.com", 4], ["site_popup", "yahoo.com", 2400], ["site_popup", "outlook.com", 1900], ["site_popup", "other", 3500]]

assert gross_growth > 0.5 and net_growth < gross_growth - 0.25, (gross_growth, net_growth)
assert cr["2026-09"] < cr["2026-01"] * 0.85, cr
assert all(max(v) / min(v) < 1.1 for v in src_cr.values()), src_cr
assert cost_per_buyer_g > 5 * cost_per_buyer_p and 0.7 < cps_g / cps_p < 1.4, (cost_per_buyer_g, cost_per_buyer_p, cps_g, cps_p)
assert all(c < 0.001 for c in comp_rate.values())
ctor_min, ctor_max = min(ctor.values()), max(ctor.values())

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
usd = lambda x: f"${x:,.0f}"

deck = f"""# Email program review, Jan-Sep 2026 (for the leadership meeting)

- **List up {pc(gross_growth, 0)} this year** ({gross_new:,} new subscribers on a starting list of {start_total:,}), thanks mainly to our three giveaways.
- Email returns **$36 for every $1 spent**, so it remains our most efficient channel.
- Click rate has drifted down from {pc(cr['2026-01'], 2)} in January to {pc(cr['2026-09'], 2)} in September. We think the creative is tired and propose a full template and copy refresh.
- Plan for Q4: a giveaway every month (October, November, December) to keep the list growing into the holidays, plus the creative refresh.
"""

notes = f"""# Notes
- Marram Swimwear sells swimwear online. We send about {SENDS} campaigns a month to the whole list.
- Each giveaway costs about {usd(G_COST / 3)} (prize plus paid social promotion). The site pop-up costs about {usd(POP_COST / 9)} a month (tool plus the welcome discount).
- Exports: list growth by signup source per month, campaign engagement by signup source per month, signup form settings, and email domains by source.
"""

files = {
    "resources/notes.md": notes,
    "resources/email_program_review.md": deck,
    "resources/list_growth_by_source.csv": to_csv(["month", "signup_source", "new_subscribers", "unsubscribed", "cleaned"], gro),
    "resources/campaign_engagement_by_source.csv": to_csv(["month", "signup_source", "delivered", "unique_opens", "unique_clicks", "purchasers", "revenue", "spam_complaints"], eng),
    "resources/signup_forms.csv": to_csv(["form", "double_opt_in", "incentive"], forms),
    "resources/subscriber_domains_by_source.csv": to_csv(["signup_source", "email_domain", "subscribers"], dom),
}

prompt = """
I'm presenting our email program review (resources/email_program_review.md) to leadership next week. The exports behind it are in resources/. How is the program really doing, and should we go ahead with the Q4 plan? Please write it up in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Giveaway subscribers barely buy. Purchasers per delivered email: giveaway {src_tot('giveaway', 5) / src_tot('giveaway', 2) * 100:.3f}% vs site_popup {src_tot('site_popup', 5) / src_tot('site_popup', 2) * 100:.2f}% (data: {src_tot('giveaway', 5):,} purchasers from giveaway subscribers vs {src_tot('site_popup', 5):,} from pop-up). Per 1,000 subscribers per month that is about {bpk['giveaway']:.1f} purchasers for giveaway vs {bpk['site_popup']:.1f} for pop-up, while each costs a similar amount to acquire (about ${cps_g:.2f} vs ${cps_p:.2f} per subscriber), so a giveaway subscriber costs roughly {cost_per_buyer_g / cost_per_buyer_p:.0f}x more per purchase. Counts as found if report.md shows giveaway subscribers purchase (or click) far less than other sources, with a number.
2. Click-rate fall is mix, not creative. Program click rate fell from {pc(cr['2026-01'], 2)} to {pc(cr['2026-09'], 2)}, but each source's click rate is flat (site_popup {pc(min(src_cr['site_popup']), 2)}-{pc(max(src_cr['site_popup']), 2)}, checkout_optin {pc(min(src_cr['checkout_optin']), 2)}-{pc(max(src_cr['checkout_optin']), 2)}, giveaway {pc(min(src_cr['giveaway']), 2)}-{pc(max(src_cr['giveaway']), 2)} across months); the drop comes from the rising share of giveaway subscribers. Counts as found if report.md says the decline is driven by list mix rather than tired creative.
3. Double opt-in off on the giveaway form. The giveaway landing page has double opt-in off; giveaway sign-ups include typo domains (gmial.com, hotmial.com, gmail.con) and {g_clean:,} giveaway addresses were cleaned (bounced/removed). Counts as found if report.md flags the missing double opt-in or the typo domains / high cleaning of giveaway sign-ups.
4. Gross vs net growth. The "{pc(gross_growth, 0)}" counts gross sign-ups; after unsubscribes and cleaning the list grew {pc(net_growth, 0)} ({start_total:,} to {end_total:,}). Counts as found if report.md gives the net growth (within a few points) or says the {pc(gross_growth, 0)} ignores unsubscribes and cleaning.
5. Borrowed ROI. "$36 for every $1" is an industry benchmark, not this program's measured return. Counts as found if report.md flags it.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct recommendation: do not run a giveaway every month in Q4 (at least not as currently run), because giveaway subscribers buy at about {bpk['giveaway']:.1f} purchasers per 1,000 a month against {bpk['site_popup']:.1f} for pop-up subscribers at a similar acquisition cost per subscriber (roughly {cost_per_buyer_g / cost_per_buyer_p:.0f}x the cost per purchase), add bounce and unsubscribe load, and drag program rates; and do not do the creative refresh on the click-rate argument, since click rate per source is flat. Acceptable variants: stop giveaways, or only with double opt-in and a purchase-intent qualifier and a separate onboarding/sunset path, with budget moved to sources that buy.

Naive answer: approve the Q4 plan (monthly giveaways plus a creative refresh).

PASS if report.md's main recommendation rejects or substantially changes the monthly-giveaway plan because giveaway subscribers do not buy (cost per purchaser / purchase rate), and does not endorse the creative refresh as the fix for the click-rate decline.
FAIL if report.md endorses monthly giveaways, or makes the creative refresh the main action.
"""

g_decoy = f"""
Two things look fine and must not be presented as problems:
- D1. Click-to-open rate each month is {pc(ctor_min)}-{pc(ctor_max)}, a normal band.
- D2. Spam complaint rate is under 0.1% every month (max {max(comp_rate.values()) * 100:.3f}%).

PASS if report.md does not present the monthly CTOR or the complaint rate as a problem. Mentioning them as normal is fine.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: gross {gross_growth:.2f} net {net_growth:.2f}; CR {cr['2026-01']:.4f}->{cr['2026-09']:.4f}; cps {cps_g:.2f}/{cps_p:.2f} buyers/1k/mo {bpk['giveaway']:.1f}/{bpk['site_popup']:.1f} ratio {cost_per_buyer_g / cost_per_buyer_p:.1f}; "
      f"ctor {ctor_min:.3f}-{ctor_max:.3f}; comp max {max(comp_rate.values()):.5f}")
