"""December is +40% on November, but that is season (Dec index 1.76 vs Nov
1.27); underlying growth is ~1%/month (~12-13% YoY). A January plan must put
January's seasonal dip back: ~$98k, not the 3-month MA of Oct-Dec (~$190k)
or the plain 12-month MA (~$135k)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "models-seasonal-forecast"
rng = random.Random(2412)
IDX = [0.686, 0.784, 0.882, 0.931, 0.980, 0.980, 0.931, 0.882, 0.931, 0.980, 1.273, 1.763]
rows, rev = [], []
for t in range(36):
    y, m = 2024 + t // 12, t % 12 + 1
    v = round(100000 * 1.01 ** t * IDX[m - 1] * rng.uniform(0.98, 1.02), 2)
    orders = int(v / rng.uniform(52, 56))
    rows.append([f"{y}-{m:02d}", v, orders]); rev.append(v)
csv_text = to_csv(["month", "revenue", "orders"], rows)

# ground truth: classical multiplicative decomposition from the rows
cma = [None] * 36
for t in range(6, 30):
    cma[t] = (0.5 * rev[t - 6] + sum(rev[t - 5:t + 6]) + 0.5 * rev[t + 6]) / 12
ratios = {m: [rev[t] / cma[t] for t in range(36) if cma[t] and t % 12 == m] for m in range(12)}
raw = [sum(v) / len(v) for m, v in sorted(ratios.items())]
S = [r * 12 / sum(raw) for r in raw]
des = [rev[t] / S[t % 12] for t in range(36)]
# log-linear trend on deseasonalised series
xs = list(range(36)); ly = [math.log(d) for d in des]
xb, yb = sum(xs) / 36, sum(ly) / 36
b = sum((x - xb) * (yy - yb) for x, yy in zip(xs, ly)) / sum((x - xb) ** 2 for x in xs)
a = yb - b * xb
g_m = math.exp(b) - 1
jan = math.exp(a + b * 36) * S[0]
dec_nov = rev[35] / rev[34] - 1
yoy_dec = rev[35] / rev[23] - 1
yoy_12 = sum(rev[24:]) / sum(rev[12:24]) - 1
ma3 = sum(rev[33:36]) / 3
ma12 = sum(rev[24:36]) / 12
naive_jan = rev[35] * (1 + dec_nov)
assert 0.35 < dec_nov < 0.45 and 0.007 < g_m < 0.013 and 88000 < jan < 108000, (dec_nov, g_m, jan)
assert ma3 > 1.7 * jan and ma12 > 1.25 * jan
print(f"{NAME}: Dec/Nov +{100*dec_nov:.0f}%, growth {100*g_m:.2f}%/mo, YoY {100*yoy_12:.1f}%; Jan27 {jan:,.0f}; MA3 {ma3:,.0f}; MA12 {ma12:,.0f}")

prompt = f"""
Here are 36 months of revenue for our gifting shop, Juniper & Pine (resources/monthly_revenue.csv, January 2024 to December 2026). December was our best month ever, up {100*dec_nov:.0f}% on November. Are we really growing, and what revenue should we plan for January 2027? Write report.md with the growth rate and the January number.
"""
f0 = lambda x: f"{x:,.0f}"
g_growth = f"""
Ground truth: December 2026 revenue ${f0(rev[35])} is +{100*dec_nov:.0f}% on November (${f0(rev[34])}), but every December is the seasonal peak (seasonal index about {S[11]:.2f} vs November {S[10]:.2f}). Underlying growth is about {100*g_m:.1f}% a month: December 2026 vs December 2025 is +{100*yoy_dec:.1f}%, and full-year 2026 vs 2025 is +{100*yoy_12:.1f}%.

PASS if report.md states underlying growth of roughly 0.7% to 1.3% a month or roughly 9% to 16% year on year, and attributes the +{100*dec_nov:.0f}% December jump to seasonality.
FAIL if it treats December's +{100*dec_nov:.0f}% as growth / momentum, or gives a growth rate above 25% a year.
"""
g_fc = f"""
Ground truth: January is the seasonal low (index about {S[0]:.2f}, roughly 30% below an average month). Trend level for January 2027 x January seasonal index gives about ${f0(jan)}. Anything from $85,000 to $115,000 with a seasonal method (or e.g. January 2026 ${f0(rev[24])} grown by about 12%) is correct.
Naive wrong forecasts: 3-month moving average of Oct-Dec 2026 = ${f0(ma3)}; 12-month moving average of 2026 without putting January's dip back = ${f0(ma12)}; December x 1.4 = ${f0(naive_jan)}.

PASS if the January 2027 revenue plan in report.md is between $85,000 and $115,000.
FAIL if it is above $125,000 or below $75,000, or no single January number is given.
"""
write_case(NAME, {"resources/monthly_revenue.csv": csv_text}, prompt,
           [("growth", 2, g_growth), ("forecast", 3, g_fc)])
