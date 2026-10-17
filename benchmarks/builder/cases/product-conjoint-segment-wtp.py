"""Average WTP for a premium strap (~$2.5) beats its $1.50 cost, so the naive
call is 'add it to every unit'. Individual part-worths split: about half value
it well above cost, ~45% have negative WTP. The average describes almost no
one: offer it as an option / premium variant."""
import sys, random, math, statistics as st; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "product-conjoint-segment-wtp"
rng = random.Random(5)
rows = []
for i in range(80):
    u = rng.random()
    seg = "A" if u < 0.45 else ("B" if u < 0.85 else "C")
    strap = {"A": rng.gauss(1.5, 0.3), "B": rng.gauss(-0.9, 0.25), "C": rng.gauss(0, 0.15)}[seg]
    p19 = rng.gauss(0.8, 0.15); p29 = -rng.gauss(0.8, 0.15)
    color = rng.gauss(0.2, 0.3)
    rows.append([i + 1, seg, round(strap, 2), round(p19, 2), round(p29, 2), round(color, 2)])
AB = {"A": ["18-24", "25-34"], "B": ["35-44", "45-54", "25-34"], "C": ["35-44", "55+"]}
out = [[f"RESP{r[0]:03d}", rng.choice(AB[r[1]]), r[2], r[3], r[4], r[5]] for r in rows]
csv_text = to_csv(["respondent_id", "age_band", "pw_strap_premium", "pw_price_19", "pw_price_29", "pw_color_graphite"], out)
COST = 1.5
wtp = [r[2] / ((r[3] - r[4]) / 10) for r in rows]
agg_er = (st.mean(r[3] for r in rows) - st.mean(r[4] for r in rows)) / 10
agg_wtp = st.mean(r[2] for r in rows) / agg_er
mean_ind = st.mean(wtp)
sh_above = sum(w > COST for w in wtp) / 80
sh_neg = sum(w < 0 for w in wtp) / 80
sh_below_negcost = sum(w < -COST for w in wtp) / 80
pos_mean = st.mean(w for w in wtp if w > COST)
neg_mean = st.mean(w for w in wtp if w < 0)
assert agg_wtp > COST and sh_neg > 0.35 and 0.4 < sh_above < 0.6
assert sum(abs(w - agg_wtp) < 1.0 for w in wtp) / 80 < 0.2
print(f"{NAME}: ER {agg_er:.3f}, agg WTP {agg_wtp:.2f} (mean indiv {mean_ind:.2f}); >cost {sh_above:.2f} (mean {pos_mean:.2f}); <0 {sh_neg:.2f} (mean {neg_mean:.2f})")

prompt = """
resources/partworths.csv is the individual part-worth export from our conjoint study for the Ridgeline SmartLock (price levels $19, $24 and $29, with $24 as the baseline; plus a premium strap and a graphite colour, each against not having it). The premium strap costs us $1.50 a unit. Should we add the strap to the product? Answer in report.md.
"""
near = sum(abs(w - agg_wtp) < 1.0 for w in wtp)
g_wtp = f"""
Ground truth: price part-worths span $10 ($19 to $29), so the exchange rate is (pw_price_19 - pw_price_29)/10. Across the sample it is about {agg_er:.3f} utils per dollar. Average strap part-worth / exchange rate = average WTP for the strap of about ${agg_wtp:.2f} (mean of individual WTPs about ${mean_ind:.2f}).

PASS if report.md converts the strap part-worth into a dollar willingness to pay using the price part-worths, with an average between $2.0 and $3.2 (or reports individual WTPs consistent with it).
FAIL if no dollar WTP is computed.
"""
g_split = f"""
Ground truth (per respondent, WTP = strap part-worth / own price exchange rate):
- {100*sh_above:.0f}% of respondents value the strap above its $1.50 cost (their average WTP about ${pos_mean:.2f}).
- {100*sh_neg:.0f}% have NEGATIVE WTP (they dislike it; average about ${neg_mean:.2f}), {100*sh_below_negcost:.0f}% below -$1.50.
- Only {near} of 80 respondents are within $1 of the ${agg_wtp:.2f} average: the average describes almost no one.
The right decision is to make the strap an optional add-on, a premium variant priced several dollars higher, or target it at the segment that values it, not to put it on every unit. Adding it to the standard product would make the lock less attractive to nearly half of buyers.
Naive wrong answer: "average WTP ${agg_wtp:.2f} > $1.50 cost, add the strap to every unit."

PASS if report.md shows that preferences split (a large share, roughly 40-50%, has negative WTP / dislikes the strap while about half value it above cost) AND recommends an optional strap, a premium variant, or targeting the segment that values it.
FAIL if it recommends adding the strap to the standard product because average WTP exceeds cost, or never looks at the distribution across respondents.
"""
write_case(NAME, {"resources/partworths.csv": csv_text}, prompt, [("wtp", 1, g_wtp), ("split", 3, g_split)])
