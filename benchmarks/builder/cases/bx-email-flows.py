"""Breadth: which email flows to invest in (Brindle Bakeware, Q3 2026, ESP exports).

Planted problems (4): the post-purchase flow tops attributed revenue but its
holdout converts like its control (no incremental revenue), while abandoned
checkout shows a large holdout lift (DECISION); attribution counts any open
within 5 days, and most of the post-purchase revenue is open-only (opens
fired by privacy proxies count); the win-back flow mails lapsed profiles six
times with no exit, its later messages over the 0.1% complaint line and
bouncing 3%+; welcome email 3 has an unsubscribe rate above 0.5% hidden in a
flow average under it.
Decoys (2): CTOR 9-15% across flows; unsubscribes 0.1-0.4% on most messages."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-email-flows"
rng = random.Random(81707)
AOV = 78.0

# flow, message, recipients, open_rate, ctor, unsub, complaint, bounce, orders_per_delivered, open_only_share
M = [
    ("Welcome", "W1 Welcome + 10% code", 21000, 0.58, 0.14, 0.0022, 0.0004, 0.006, 0.042, 0.30),
    ("Welcome", "W2 Our story", 19800, 0.49, 0.10, 0.0025, 0.0004, 0.004, 0.009, 0.35),
    ("Welcome", "W3 Bestsellers", 19100, 0.45, 0.11, 0.0082, 0.0006, 0.004, 0.011, 0.35),
    ("Welcome", "W4 Baking tips", 18300, 0.42, 0.09, 0.0024, 0.0003, 0.004, 0.005, 0.40),
    ("Abandoned Checkout", "AC1 You left something", 9400, 0.55, 0.15, 0.0021, 0.0003, 0.005, 0.098, 0.16),
    ("Abandoned Checkout", "AC2 Still thinking?", 7800, 0.50, 0.12, 0.0026, 0.0004, 0.005, 0.047, 0.18),
    ("Browse Abandonment", "BA1 Saw something you liked", 12600, 0.47, 0.11, 0.0030, 0.0004, 0.005, 0.016, 0.30),
    ("Post-Purchase", "PP1 Thank you", 18200, 0.64, 0.09, 0.0012, 0.0002, 0.003, 0.046, 0.86),
    ("Post-Purchase", "PP2 How to care for your tins", 17900, 0.58, 0.10, 0.0015, 0.0002, 0.003, 0.038, 0.87),
    ("Post-Purchase", "PP3 Complete the set", 17600, 0.55, 0.11, 0.0019, 0.0003, 0.003, 0.034, 0.83),
    ("Win-back", "WB1 We miss you", 14100, 0.31, 0.10, 0.0034, 0.0008, 0.012, 0.009, 0.45),
    ("Win-back", "WB2 15% off", 13800, 0.27, 0.11, 0.0036, 0.0009, 0.018, 0.008, 0.45),
    ("Win-back", "WB3 Last call", 13500, 0.24, 0.09, 0.0038, 0.0011, 0.024, 0.004, 0.50),
    ("Win-back", "WB4 New arrivals", 13200, 0.21, 0.092, 0.0039, 0.0014, 0.031, 0.003, 0.50),
    ("Win-back", "WB5 Still here?", 12900, 0.19, 0.091, 0.0040, 0.0016, 0.035, 0.002, 0.55),
    ("Win-back", "WB6 Goodbye?", 12700, 0.18, 0.090, 0.0041, 0.0018, 0.038, 0.002, 0.55),
]
rows, F = [], {}
for flow, msg, rcp, orr, ctor, uns, comp, bnc, opd, oos in M:
    r = int(rcp * rng.uniform(0.98, 1.02))
    bounced = int(r * bnc * rng.uniform(0.95, 1.05))
    d = r - bounced
    op = int(d * orr * rng.uniform(0.97, 1.03))
    cl = int(op * ctor * rng.uniform(0.95, 1.05))
    un = int(round(d * uns * rng.uniform(0.95, 1.05)))
    sp = int(round(d * comp * rng.uniform(0.95, 1.05)))
    orders = int(d * opd * rng.uniform(0.95, 1.05))
    rev = round(orders * AOV * rng.uniform(0.95, 1.05), 2)
    rev_open = round(rev * oos, 2)
    rows.append([flow, msg, r, d, bounced, op, cl, un, sp, orders, rev, rev_open, round(rev - rev_open, 2)])
    f = F.setdefault(flow, dict(d=0, un=0, rev=0.0, ro=0.0, rc=0.0, op=0, cl=0))
    f["d"] += d; f["un"] += un; f["rev"] += rev; f["ro"] += rev_open; f["rc"] += rev - rev_open; f["op"] += op; f["cl"] += cl

top_flow = max(F, key=lambda k: F[k]["rev"])
pp, ac = F["Post-Purchase"], F["Abandoned Checkout"]
pp_open_share = pp["ro"] / pp["rev"]
w3 = next(r for r in rows if r[1].startswith("W3"))
w3_unsub = w3[7] / w3[3]
welcome_unsub = F["Welcome"]["un"] / F["Welcome"]["d"]
wb_late = [r for r in rows if r[1][:3] in ("WB4", "WB5", "WB6")]
wb_comp = [r[8] / r[3] for r in wb_late]
wb_bnc = [r[4] / r[2] for r in wb_late]
ctors = [r[6] / r[5] for r in rows]
unsubs_other = [r[7] / r[3] for r in rows if not r[1].startswith("W3")]

# ---------- holdouts ----------
hold = []
def ho(flow, nt, nc, ct, cc):
    pt = int(nt * ct * rng.uniform(0.98, 1.02)); pc_ = int(nc * cc * rng.uniform(0.98, 1.02))
    hold.append([flow, "receives_flow", nt, pt, round(pt * AOV * rng.uniform(0.97, 1.03), 2)])
    hold.append([flow, "holdout", nc, pc_, round(pc_ * AOV * rng.uniform(0.97, 1.03), 2)])
    return pt / nt, pc_ / nc
pp_t, pp_c = ho("Post-Purchase", 16400, 1820, 0.081, 0.080)
ac_t, ac_c = ho("Abandoned Checkout", 8460, 940, 0.152, 0.091)
pp_inc = (pp_t - pp_c) * 16400 * AOV
ac_inc = (ac_t - ac_c) * 8460 * AOV

settings = [["conversion_metric", "Placed Order"], ["email_attribution", "opened or clicked within 5 days"],
            ["sms_attribution", "clicked within 1 day"], ["flow_holdout_groups", "Post-Purchase 10%, Abandoned Checkout 10%"],
            ["smart_sending", "on (16 hours)"], ["win_back_trigger", "no order in 180 days"], ["win_back_exit_condition", "placed order"]]

assert top_flow == "Post-Purchase", top_flow
assert pp_open_share > 0.8 and ac["ro"] / ac["rev"] < 0.25
assert abs(pp_t - pp_c) < 0.01 and ac_t - ac_c > 0.04
assert ac_inc > 5 * max(pp_inc, 1)
assert w3_unsub > 0.005 and welcome_unsub < 0.005
assert all(c > 0.001 for c in wb_comp) and all(b > 0.03 for b in wb_bnc)
assert all(0.08 < c < 0.16 for c in ctors), ctors
assert all(u < 0.0045 for u in unsubs_other)

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

notes = """# Notes
- Brindle Bakeware sells baking tins and tools online, average order about $78.
- We have budget for one designer and one copywriter for flows in Q4 and want to put it where it earns most.
- Exports: flow message performance Q3 2026 (with the ESP's attributed revenue split by how the order was attributed), the ESP attribution and flow settings, and the flow holdout report.
"""

files = {
    "resources/notes.md": notes,
    "resources/flow_message_performance_q3.csv": to_csv(
        ["flow_name", "message_name", "recipients", "delivered", "bounced", "unique_opens", "unique_clicks", "unsubscribes", "spam_complaints",
         "placed_order", "attributed_revenue", "attributed_revenue_open_only", "attributed_revenue_clicked"], rows),
    "resources/esp_account_settings.csv": to_csv(["setting", "value"], settings),
    "resources/flow_holdout_q3.csv": to_csv(["flow_name", "group", "profiles", "purchasers_30d", "revenue_30d"], hold),
}

prompt = """
We want to put more design and copy effort into our email flows next quarter. I've exported our Q3 flow performance, the ESP settings and the holdout report into resources/. Which flows should we invest in, and is there anything else we should change? Please write your recommendation in report.md.
"""

g_recall = f"""
The exports contain 4 planted problems. Answer key:

1. Post-purchase is not incremental. It has the most attributed revenue ({usd(pp['rev'])}), but in the holdout report profiles receiving it buy at {pc(pp_t)} against {pc(pp_c)} for the holdout: no measurable lift. Abandoned checkout converts {pc(ac_t)} vs {pc(ac_c)} for its holdout, roughly {usd(ac_inc)} incremental in Q3. Counts as found if report.md uses the holdout to say post-purchase adds little or nothing, or that abandoned checkout is the flow with proven lift.
2. Open-based attribution. Attribution is "opened or clicked within 5 days", and {pc(pp_open_share, 0)} of post-purchase attributed revenue is open-only (opens can be fired by privacy proxies and these customers just bought anyway). Counts as found if report.md says attributed revenue is inflated by open-based attribution (or reads flows on click-attributed revenue instead).
3. Win-back with no real exit. The flow sends six messages to profiles with no order in 180 days; exit is only "placed order". WB4-WB6 complaint rates are {', '.join(pc(c, 2) for c in wb_comp)} (above the 0.1% line) and bounce rates {', '.join(pc(b) for b in wb_bnc)}. Counts as found if report.md flags the late win-back messages' complaint or bounce rates, or the lack of an exit / suppression rule for non-responders.
4. One welcome message drives unsubscribes. W3 "Bestsellers" unsubscribes at {pc(w3_unsub, 2)}, above about 0.5%, while the welcome flow overall is {pc(welcome_unsub, 2)}. Counts as found if report.md flags W3 specifically.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 4, each with evidence (a number or message name).
FAIL if fewer than 3.
"""

g_decision = f"""
The correct top recommendation: put the Q4 effort into abandoned checkout (and other intent-triggered flows such as browse abandonment), which has a proven holdout lift, not into the post-purchase flow, whose attributed revenue ({usd(pp['rev'])}, the largest) is mostly open-attributed and shows no lift against its holdout ({pc(pp_t)} vs {pc(pp_c)}).

Naive answer: invest most in the post-purchase flow because it tops attributed revenue (or rank flows on attributed revenue).

PASS if report.md's main investment recommendation is abandoned checkout (or abandoned checkout plus browse abandonment), and it does not recommend post-purchase as the top investment.
FAIL if post-purchase is the top recommended investment, or the ranking is based on attributed revenue without using the holdout or click-based revenue.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Click-to-open rates range from {min(ctors) * 100:.0f}% to {max(ctors) * 100:.0f}% across flow messages; that is a normal band.
- D2. Unsubscribe rates of {min(unsubs_other) * 100:.2f}%-{max(unsubs_other) * 100:.2f}% on every message except W3 are normal (W3 at {pc(w3_unsub, 2)} is the real problem).

PASS if report.md does not present the CTOR range as a problem and does not flag unsubscribe rates on messages other than W3 as too high. Mentioning them as normal is fine.
FAIL if either is presented as a problem (for example "win-back unsubscribes are alarming" at under 0.45%, or "CTOR of 9% is poor").
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: top {top_flow} {pp['rev']:,.0f} open-only {pp_open_share:.2f}; holdout pp {pp_t:.3f}/{pp_c:.3f} ac {ac_t:.3f}/{ac_c:.3f} inc {ac_inc:,.0f}; "
      f"w3 unsub {w3_unsub:.4f}; wb comp {[round(c, 4) for c in wb_comp]}")
