"""Big creators bring ~5x the orders of nano creators, so 'move budget to bigger
creators' looks right. With fees and $22 margin per order, macro posts lose
~$800 each (Instagram macro ~$2k+), while TikTok nano/micro with codes are the
profitable cells."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "channel-influencer-tier-profit"
rng = random.Random(21)
MARGIN = 22
rows = []
for i in range(240):
    plat = rng.choice(["TikTok", "Instagram"])
    tier = rng.choices(["nano", "micro", "macro"], [0.25, 0.5, 0.25])[0]
    f = {"nano": rng.randint(3000, 9900), "micro": rng.randint(10000, 99000), "macro": rng.randint(100000, 600000)}[tier]
    code = 1 if rng.random() < 0.5 else 0
    fee = round(f / 1000 * {"TikTok": 2.2, "Instagram": 9.0}[plat] * rng.uniform(0.8, 1.2) + 40)
    base = 3.2 * (f / 1000) ** 0.45
    cm = 1 + (0.6 if f < 30000 else 0.35 if f < 100000 else 0.08)
    orders = max(0, round(base * (cm if code else 1) * rng.uniform(0.7, 1.3)))
    rows.append([f"CR{i + 1:03d}", plat, f, code, fee, orders, tier])
r2 = random.Random(2121)
out = [[r[0], (dt.date(2026, 7, 1) + dt.timedelta(days=r2.randint(0, 91))).isoformat(), r[1], r[2], r[3], r[4], r[5]] for r in rows]
csv_text = to_csv(["creator_id", "post_date", "platform", "followers", "promo_code", "fee_usd", "orders"], out)

def summ(sel):
    s = [r for r in rows if sel(r)]
    o = sum(r[5] for r in s); fee = sum(r[4] for r in s); prof = o * MARGIN - fee
    return dict(n=len(s), opp=o / len(s), fpp=fee / len(s), ppp=prof / len(s), poas=prof / fee)
T = {t: summ(lambda r, t=t: r[6] == t) for t in ["nano", "micro", "macro"]}
cells = {(t, p, c): summ(lambda r, t=t, p=p, c=c: r[6] == t and r[1] == p and r[3] == c)
         for t in T for p in ["TikTok", "Instagram"] for c in (0, 1)}
ALL = summ(lambda r: True)
assert T["macro"]["opp"] > 4 * T["nano"]["opp"] and T["macro"]["ppp"] < -500 and T["nano"]["ppp"] > 0 and T["micro"]["ppp"] > 0
best = max(cells, key=lambda k: cells[k]["poas"]); best_p = max(cells, key=lambda k: cells[k]["ppp"])
assert best[1] == "TikTok" and best_p[1] == "TikTok"
assert cells[("macro", "Instagram", 0)]["ppp"] < -1500 and cells[("macro", "Instagram", 1)]["ppp"] < -1500
print(f"{NAME}: " + "; ".join(f"{t} {v['opp']:.1f} ord, ${v['ppp']:.0f}/post" for t, v in T.items()) + f"; all ${ALL['ppp']:.0f}")

prompt = """
We paid 240 creators to post about our Northwind Coffee subscription last quarter (resources/creator_posts.csv). Big creators clearly drive the most orders. Our margin per order is $22. Should we move next quarter's influencer budget toward bigger creators? Answer in report.md.
"""
line = lambda name, v: f"- {name} (n={v['n']}): {v['opp']:.1f} orders/post, fee ${v['fpp']:,.0f}/post, profit ${v['ppp']:,.0f}/post, POAS {v['poas']:.2f}"
tiers = "\n".join(line(f"{t} ({lab})", T[t]) for t, lab in [("nano", "< 10K followers"), ("micro", "10K-100K"), ("macro", "100K+")])
cl = "\n".join(line(f"{t} {p} {'with code' if c else 'no code'}", v) for (t, p, c), v in cells.items())
g_p = f"""
Ground truth. Profit per post = $22 x orders - fee. POAS = profit / fee.
By follower tier:
{tiers}
- Whole program: profit ${ALL['ppp']:,.0f} per post.
Macro creators bring about {T['macro']['opp']/T['nano']['opp']:.0f}x the orders of nano creators but their fees are far larger, so they LOSE money on average; nano and micro posts are profitable.
Naive wrong answer: "macro creators average {T['macro']['opp']:.0f} orders per post vs {T['nano']['opp']:.0f} for nano, so shift budget to bigger creators."

PASS if report.md computes profit (or POAS / cost per order vs the $22 margin) per post by follower tier (and/or platform) and shows macro creators lose money (around ${T['macro']['ppp']:,.0f} per post, within 25%) while nano and micro are profitable.
FAIL if it recommends shifting budget toward bigger creators, or ranks creators by orders without accounting for fees and margin.
"""
g_w = f"""
Ground truth by cell (tier x platform x promo code):
{cl}
Best cells: {best[0]} {best[1]} {'with code' if best[2] else 'no code'} (highest POAS {cells[best]['poas']:.2f}) and {best_p[0]} {best_p[1]} {'with code' if best_p[2] else 'no code'} (highest profit per post ${cells[best_p]['ppp']:,.0f}). Instagram macro posts lose about ${min(-cells[('macro','Instagram',c)]['ppp'] for c in (0,1)):,.0f} to ${max(-cells[('macro','Instagram',c)]['ppp'] for c in (0,1)):,.0f} each, while macro TikTok posts are only marginally profitable (POAS about 0.2-0.3) (Instagram fees per 1,000 followers are about 4x TikTok's).

PASS if the recommendation concentrates next quarter's budget on TikTok nano/micro creators (ideally with promo codes) AND cuts, caps or renegotiates Instagram macro (or macro generally) posts.
FAIL otherwise, including any recommendation to increase macro creator spend.
"""
write_case(NAME, {"resources/creator_posts.csv": csv_text}, prompt, [("profit", 3, g_p), ("where", 2, g_w)])
