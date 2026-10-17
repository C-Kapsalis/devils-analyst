"""Review an e-commerce dashboard (Saltmarsh Skincare, weeks 36-39 2026, HTML).

Planted problems (6): truncated bar axis behind "Email nearly double Paid
Social" (MUST); mean AOV inflated by wholesale orders used to set a $200
free-shipping threshold (MUST); TikTok landing-page CVR tile from 41 sessions
with no volume; cumulative YTD line "still climbing" while each of the last 4
weeks fell; "Google Ads is X% of revenue" with the Paid filter on; 9-slice pie.
Decoys (2): week-over-week heat table on a diverging scale centred at 0;
daily orders with a labelled 7-day moving average."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "review-ecom-dashboard"
rng = random.Random(77311)
START = dt.date(2026, 8, 31)          # Monday of ISO week 36
WEEKS = [36, 37, 38, 39]
WEEK_ORDERS = [98, 82, 67, 53]        # retail orders per week, declining
CHANNEL_ORDERS = {"Google Ads": 95, "Email": 52, "Paid Social": 50, "Organic Search": 38, "Direct": 30,
                  "Affiliates": 12, "TikTok Ads": 9, "Referral": 8, "Pinterest Ads": 6}
PAID = ["Google Ads", "Paid Social", "TikTok Ads", "Pinterest Ads"]
assert sum(WEEK_ORDERS) == sum(CHANNEL_ORDERS.values())


def value():
    return round(min(220, max(18, math.exp(rng.gauss(math.log(60), 0.45)))), 2)


# retail orders: channel list shuffled, assigned to weeks in order
chans = [c for c, n in CHANNEL_ORDERS.items() for _ in range(n)]
rng.shuffle(chans)
orders = []
i = 0
for wk, n in zip(WEEKS, WEEK_ORDERS):
    for _ in range(n):
        day = START + dt.timedelta(days=7 * (wk - 36) + rng.randint(0, 6))
        orders.append([day, chans[i], "retail", value()])
        i += 1


def rev_by(ch):
    return sum(o[3] for o in orders if o[1] == ch)


# nudge Email vs Paid Social so the true gap is 5-10%
for _ in range(400):
    ratio = rev_by("Email") / rev_by("Paid Social")
    if 1.05 <= ratio <= 1.10:
        break
    tgt = "Email" if ratio < 1.05 else "Paid Social"
    for o in orders:
        if o[1] == tgt:
            o[3] = value()
            break
    rng.shuffle(orders)
ratio = rev_by("Email") / rev_by("Paid Social")
assert 1.05 <= ratio <= 1.10, ratio

# wholesale orders (invoiced, not web store)
for k in range(5):
    day = START + dt.timedelta(days=rng.randint(0, 27))
    orders.append([day, "Wholesale", "wholesale", round(rng.uniform(7600, 10400), 2)])
orders.sort(key=lambda o: (o[0], o[3]))
order_rows = [[f"SS-{40211 + j}", o[0].isoformat(), o[1], o[2], o[3]] for j, o in enumerate(orders)]

retail = [o for o in orders if o[2] == "retail"]
retail_rev = sum(o[3] for o in retail)
all_vals = sorted(o[3] for o in orders)
n_all = len(all_vals)
mean_all = sum(all_vals) / n_all                       # planted AOV
median_all = (all_vals[n_all // 2] if n_all % 2 else (all_vals[n_all // 2 - 1] + all_vals[n_all // 2]) / 2)
rvals = sorted(o[3] for o in retail)
median_retail = (rvals[len(rvals) // 2 - 1] + rvals[len(rvals) // 2]) / 2
mean_retail = retail_rev / len(retail)
share_over_200 = sum(1 for v in rvals if v >= 200) / len(rvals)

# channel revenue (web store)
ch_rev = {c: rev_by(c) for c in CHANNEL_ORDERS}
email, ps, gads = ch_rev["Email"], ch_rev["Paid Social"], ch_rev["Google Ads"]
axis_min = 50 * math.ceil((2 * ps - email) / 50)
visual_ratio = (email - axis_min) / (ps - axis_min)
paid_rev = sum(ch_rev[c] for c in PAID)
g_share_paid = gads / paid_rev                         # planted
g_share_all = gads / retail_rev                        # truth
shares = {c: ch_rev[c] / retail_rev for c in CHANNEL_ORDERS}

# weekly revenue (web store) for the year: weeks 36-39 from orders
wk_rev = {wk: sum(o[3] for o in retail if (o[0] - START).days // 7 + 36 == wk) for wk in WEEKS}
weekly = {}
for wk in range(1, 36):
    weekly[wk] = round(3400 + 62 * wk + rng.uniform(-180, 180), 2)
weekly[35] = round(wk_rev[36] * 1.07, 2)
weekly.update({wk: round(v, 2) for wk, v in wk_rev.items()})
week_rows = [[(dt.date(2025, 12, 29) + dt.timedelta(days=7 * (wk - 1))).isoformat(), wk, weekly[wk]] for wk in range(1, 40)]
ytd = []
run = 0
for wk in range(1, 40):
    run += weekly[wk]
    ytd.append(run)

# TikTok landing page tile (sessions file)
lp_rows = [
    ["2026-08", "/", 6120, 101], ["2026-08", "/collections/serums", 3410, 88], ["2026-08", "/products/tidepool-serum", 2280, 71],
    ["2026-08", "/lp/tiktok-glow", 30, 2],
    ["2026-09", "/", 5730, 88], ["2026-09", "/collections/serums", 3190, 76], ["2026-09", "/products/tidepool-serum", 2110, 64],
    ["2026-09", "/lp/tiktok-glow", 41, 4],
]
tt_sep = 4 / 41
tt_aug = 2 / 30
tt_delta = tt_sep - tt_aug

# daily orders + 7-day trailing average (decoy, retail web orders)
days = [START + dt.timedelta(days=d) for d in range(28)]
daily = [sum(1 for o in retail if o[0] == d) for d in days]
ma7 = [None if j < 6 else sum(daily[j - 6:j + 1]) / 7 for j in range(28)]

# week-over-week change by channel (decoy, correct)
top_ch = ["Google Ads", "Email", "Paid Social", "Organic Search", "Direct"]
cw = {(c, wk): sum(o[3] for o in retail if o[1] == c and (o[0] - START).days // 7 + 36 == wk) for c in top_ch for wk in WEEKS}
wow = {(c, wk): cw[(c, wk)] / cw[(c, wk - 1)] - 1 for c in top_ch for wk in WEEKS[1:]}

# ---------- asserts ----------
assert visual_ratio > 1.9 and ratio < 1.11, (visual_ratio, ratio)
assert mean_all > 2.8 * median_all and 190 < mean_all < 260, (mean_all, median_all)
assert 50 < median_all < 75 and share_over_200 < 0.03
assert g_share_paid > 0.55 and g_share_all < 0.40, (g_share_paid, g_share_all)
assert all(weekly[w] < weekly[w - 1] for w in range(36, 40)), [weekly[w] for w in range(35, 40)]
assert all(ytd[k] > ytd[k - 1] for k in range(1, 39))
assert abs(tt_delta - 0.031) < 0.001
assert all(cw[(c, wk)] > 0 for c in top_ch for wk in WEEKS)
assert len(CHANNEL_ORDERS) == 9

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=1: f"{100 * x:.{d}f}%"

# ---------- HTML ----------
def bar_svg():
    W, H, top, bot = 420, 240, 20, 200
    vmax = 100 * math.ceil(gads / 100 / 5) * 5
    def y(v):
        return bot - (v - axis_min) / (vmax - axis_min) * (bot - top)
    parts = [f'<svg width="{W}" height="{H}" role="img" aria-label="Web store revenue by channel, top 3 channels. Y axis from {axis_min:,} to {vmax:,}.">',
             f'<line x1="60" y1="{bot}" x2="400" y2="{bot}" stroke="#555"/><line x1="60" y1="{top}" x2="60" y2="{bot}" stroke="#555"/>',
             f'<text x="54" y="{bot + 4}" text-anchor="end" font-size="11">{axis_min:,}</text>',
             f'<text x="54" y="{top + 4}" text-anchor="end" font-size="11">{vmax:,}</text>']
    for k, (c, v) in enumerate([("Google Ads", gads), ("Email", email), ("Paid Social", ps)]):
        x = 90 + k * 105
        parts.append(f'<rect x="{x}" y="{y(v):.1f}" width="70" height="{bot - y(v):.1f}" fill="#2f6fb0"><title>{c}: {usd(v)}</title></rect>')
        parts.append(f'<text x="{x + 35}" y="{y(v) - 5:.1f}" text-anchor="middle" font-size="11">{usd(v)}</text>')
        parts.append(f'<text x="{x + 35}" y="{bot + 16}" text-anchor="middle" font-size="11">{c}</text>')
    parts.append("</svg>")
    return "\n".join(parts)

pie_colors = ["#2f6fb0", "#e07b39", "#3a9d5d", "#c94f6d", "#8a6bbe", "#d4b13f", "#4fb3c9", "#9c7a54", "#7f7f7f"]
pie_legend = "\n".join(f'<li><span class="sw" style="background:{pie_colors[k]}"></span>{c}: {pc(shares[c])}</li>'
                       for k, c in enumerate(CHANNEL_ORDERS))

def pie_svg():
    cx, cy, r = 110, 110, 100
    a0 = -math.pi / 2
    parts = ['<svg width="220" height="220" role="img" aria-label="Pie chart, 9 slices, revenue share by channel">']
    for k, c in enumerate(CHANNEL_ORDERS):
        a1 = a0 + 2 * math.pi * shares[c]
        large = 1 if a1 - a0 > math.pi else 0
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        parts.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f} Z" fill="{pie_colors[k]}"><title>{c}</title></path>')
        a0 = a1
    parts.append("</svg>")
    return "\n".join(parts)

def ytd_svg():
    W, H, top, bot = 520, 220, 15, 190
    vmax = ytd[-1] * 1.05
    pts = " ".join(f"{50 + k * 11.5:.1f},{bot - ytd[k] / vmax * (bot - top):.1f}" for k in range(39))
    return (f'<svg width="{W}" height="{H}" role="img" aria-label="Cumulative web store revenue, week 1 to week 39 2026">'
            f'<line x1="50" y1="{bot}" x2="500" y2="{bot}" stroke="#555"/><line x1="50" y1="{top}" x2="50" y2="{bot}" stroke="#555"/>'
            f'<text x="46" y="{bot + 4}" text-anchor="end" font-size="11">0</text>'
            f'<polyline points="{pts}" fill="none" stroke="#2f6fb0" stroke-width="2"/>'
            f'<text x="{50 + 38 * 11.5:.1f}" y="{bot - ytd[-1] / vmax * (bot - top) - 6:.1f}" text-anchor="end" font-size="11">Week 39: {usd(ytd[-1])}</text>'
            f'<text x="{50 + 34 * 11.5:.1f}" y="{bot - ytd[34] / vmax * (bot - top) + 16:.1f}" text-anchor="end" font-size="11">Week 35: {usd(ytd[34])}</text>'
            '</svg>')

def heat_color(v):
    s = min(1.0, abs(v) / 0.40)
    base = (47, 111, 176) if v > 0 else (224, 123, 57)
    r, g, b = (int(255 + (cc - 255) * s) for cc in base)
    return f"rgb({r},{g},{b})"

heat_rows = "\n".join(
    "<tr><th>" + c + "</th>" + "".join(
        f'<td style="background:{heat_color(wow[(c, wk)])}">{"+" if wow[(c, wk)] > 0 else ""}{100 * wow[(c, wk)]:.0f}%</td>' for wk in WEEKS[1:]) + "</tr>"
    for c in top_ch)

ma_rows = "\n".join(
    f"<tr><td>{d.isoformat()}</td><td>{n}</td><td>{'' if m is None else f'{m:.1f}'}</td></tr>" for d, n, m in zip(days, daily, ma7))
ma_pts_raw = " ".join(f"{40 + j * 16},{170 - daily[j] * 8}" for j in range(28))
ma_pts = " ".join(f"{40 + j * 16},{170 - ma7[j] * 8:.1f}" for j in range(6, 28))

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Saltmarsh Skincare: September dashboard</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #222; }}
.tiles {{ display: flex; gap: 16px; flex-wrap: wrap; }}
.tile {{ border: 1px solid #ccc; border-radius: 6px; padding: 12px 16px; min-width: 190px; }}
.tile .v {{ font-size: 26px; font-weight: bold; }}
.card {{ border: 1px solid #ddd; border-radius: 6px; padding: 12px; margin-top: 18px; }}
.sw {{ display: inline-block; width: 10px; height: 10px; margin-right: 6px; }}
table {{ border-collapse: collapse; font-size: 12px; }} td, th {{ border: 1px solid #ddd; padding: 3px 8px; }}
.note {{ font-size: 12px; color: #555; }}
</style></head>
<body>
<h1>Saltmarsh Skincare: September performance</h1>
<p class="note">Period: ISO weeks 36-39 (31 Aug to 27 Sep 2026). Page filters: Date = weeks 36-39. Source: Shopify orders export (orders_sep2026.csv), weekly web store revenue (weekly_web_revenue_2026.csv), GA4 landing pages (landing_pages_2026.csv). Web store revenue excludes wholesale invoices.</p>

<div class="tiles">
  <div class="tile"><div>Web store revenue</div><div class="v">{usd(retail_rev)}</div><div class="note">{len(retail)} web orders</div></div>
  <div class="tile"><div>Average order value</div><div class="v">{usd(mean_all)}</div><div class="note">All orders ({n_all})</div></div>
  <div class="tile"><div>TikTok landing page conversion rate</div><div class="v">{pc(tt_sep)}</div><div class="note">+{100 * tt_delta:.1f} pts vs August</div></div>
  <div class="tile"><div>Google Ads share of revenue</div><div class="v">{pc(g_share_paid, 0)}</div><div class="note">Filter: Channel group = Paid</div></div>
</div>

<div class="card">
<h2>Email revenue nearly double Paid Social</h2>
<p class="note">Web store revenue by channel, top 3 channels, weeks 36-39. Y axis starts at {axis_min:,}.</p>
{bar_svg()}
</div>

<div class="card">
<h2>Revenue share by channel</h2>
<p class="note">Share of web store revenue, weeks 36-39, all 9 channels.</p>
{pie_svg()}
<ul style="list-style:none;padding:0">{pie_legend}</ul>
</div>

<div class="card">
<h2>Revenue year to date: still climbing</h2>
<p class="note">Cumulative web store revenue by week, 2026 (running total).</p>
{ytd_svg()}
</div>

<div class="card">
<h2>Week-over-week revenue change by channel</h2>
<p class="note">Colour: diverging scale centred at 0% (white). Blue = growth, orange = decline; full colour at +40% / -40%, symmetric.</p>
<table><tr><th>Channel</th>{"".join(f"<th>Week {wk}</th>" for wk in WEEKS[1:])}</tr>
{heat_rows}
</table>
</div>

<div class="card">
<h2>Daily web orders</h2>
<p class="note">Grey line: daily web orders. Blue dashed line: 7-day moving average (trailing 7 days, first shown on 6 Sep).</p>
<svg width="500" height="190" role="img" aria-label="Daily orders and 7-day moving average">
<polyline points="{ma_pts_raw}" fill="none" stroke="#999"/>
<polyline points="{ma_pts}" fill="none" stroke="#2f6fb0" stroke-dasharray="5,3" stroke-width="2"/>
</svg>
<table><tr><th>Date</th><th>Orders</th><th>7-day moving average</th></tr>
{ma_rows}
</table>
</div>

<div class="card">
<h2>Actions</h2>
<ul>
<li>Shift 15% of the Paid Social budget into Email: Email earns nearly twice as much.</li>
<li>Raise the free-shipping threshold to $200 from 1 October, in line with our typical order of {usd(mean_all)}.</li>
<li>Scale the TikTok landing page: it converts at {pc(tt_sep)}, our best page.</li>
<li>Keep Google Ads as the core channel: {pc(g_share_paid, 0)} of revenue.</li>
</ul>
</div>
</body></html>
"""

files = {
    "resources/dashboard_sep2026.html": html,
    "resources/orders_sep2026.csv": to_csv(["order_id", "order_date", "channel", "customer_type", "order_value"], order_rows),
    "resources/weekly_web_revenue_2026.csv": to_csv(["week_start", "iso_week", "web_store_revenue"], week_rows),
    "resources/landing_pages_2026.csv": to_csv(["month", "landing_page", "sessions", "orders"], lp_rows),
}

prompt = """
I built our September dashboard (resources/dashboard_sep2026.html) from the Shopify orders export and a couple of other files that are also in resources/. It goes to the founders on Friday and they'll act on the action list at the bottom. Can you check it before I send it? Tell me if it's OK to send and exactly what to change. Put it in report.md.
"""

g_recall = f"""
The dashboard (dashboard_sep2026.html) contains 6 planted problems. Answer key:

1. Truncated bar axis behind a false headline. The bar chart of the top 3 channels starts its y axis at {axis_min:,}, and its title says "Email revenue nearly double Paid Social". Email is {usd(email)} and Paid Social {usd(ps)}: Email is only {pc(ratio - 1, 0)} higher. Counts as found if report.md says the axis does not start at zero (or the bars exaggerate) AND that the real gap is small (about {pc(ratio - 1, 0)}, or quotes both values), so the headline and the "shift 15% of Paid Social into Email" action are not supported.
2. Average order value inflated by wholesale. The tile shows {usd(mean_all)} (the mean of all {n_all} orders, including 5 wholesale invoices of $7,600 to $10,400). The median order is {usd(median_all)} (retail median {usd(median_retail)}, retail mean {usd(mean_retail)}). Only {pc(share_over_200, 1)} of web orders are $200 or more, so a $200 free-shipping threshold set "in line with our typical order" is wrong. Counts as found if report.md says the AOV is pulled up by the wholesale orders (or quotes a median or retail figure between $55 and $75) and challenges the $200 threshold.
3. Rate without volume. The TikTok landing page tile "{pc(tt_sep)}, +{100 * tt_delta:.1f} pts" comes from 41 sessions and 4 orders (August: 30 sessions, 2 orders). Counts as found if report.md says the base is too small to read (cites the 41 sessions or 4 orders) or that the tile needs its volume, and that "scale it" is not supported.
4. Cumulative chart hiding a decline. "Revenue year to date: still climbing" is a running total; the weekly file shows each of the last four weeks fell (week 35 {usd(weekly[35])}, then {usd(weekly[36])}, {usd(weekly[37])}, {usd(weekly[38])}, {usd(weekly[39])}). Counts as found if report.md says the weekly revenue has been falling for several weeks and the cumulative line hides it.
5. Filtered percent of total. "Google Ads share of revenue {pc(g_share_paid, 0)}" is computed with the filter Channel group = Paid; Google Ads is {pc(g_share_all, 0)} of all web store revenue ({usd(gads)} of {usd(retail_rev)}). Counts as found if report.md says the share uses the paid-only denominator and gives a figure between {100 * g_share_all - 2:.0f}% and {100 * g_share_all + 2:.0f}% or says it must be relabelled as share of paid revenue.
6. Pie chart with 9 slices for revenue share. Counts as found if report.md recommends replacing the 9-slice pie with sorted bars (or similar).

List which ones were found in your reasoning.
PASS if report.md identifies at least 5 of the 6 problems, each with its substance (a vague mention such as "double-check the charts" does not count).
FAIL if it identifies fewer than 5.
"""

g_rank = f"""
Two of the problems are Must-fix because the founders will act on them:
- A. The bar chart's y axis starts at {axis_min:,}, so Email ({usd(email)}) looks about twice Paid Social ({usd(ps)}) when the gap is {pc(ratio - 1, 0)}; the headline and the budget shift rest on it.
- B. Average order value {usd(mean_all)} is the mean including 5 wholesale orders; the typical (median) order is about {usd(median_all)}, so the $200 free-shipping threshold is set on a typical order that does not exist.
The lesser problems are: the TikTok tile with no volume, the cumulative year-to-date line, the paid-filtered Google share, and the 9-slice pie.

PASS if report.md flags both A and B and places each in its highest-severity group (Must fix, critical, or equivalent), or, if it uses no groups, lists both among its first three findings; other problems may share that group. The verdict must not say the dashboard can be sent as is.
FAIL if A or B is missing, is labelled lower severity (Should fix, Nice to have, minor) than any of the lesser problems, or if the verdict approves sending it unchanged.
"""

wow_ex = f"{top_ch[0]} week 37 {100 * wow[(top_ch[0], 37)]:+.0f}%"
g_decoy = f"""
The dashboard contains two elements that are correct and must not be flagged:
- D1. The week-over-week revenue change table uses a diverging colour scale centred at 0% (white), blue for growth, orange for decline, symmetric at +/-40%. The percentages are computed correctly from the orders (for example {wow_ex}).
- D2. The daily orders chart shows the raw daily series together with a dashed 7-day moving average whose window is stated (trailing 7 days); the table values are correct.

PASS if report.md does not present D1 or D2 as an error or something to fix. Mentioning either as correct or fine is a PASS.
FAIL if it says the heat table's colour scale is wrong or misleading, says its percentages are wrong, or flags the moving average (window, smoothing, or values) as a problem.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: email {email:.0f} vs PS {ps:.0f} (gap {ratio - 1:.3f}, visual {visual_ratio:.2f}x, axis {axis_min}); "
      f"AOV mean {mean_all:.0f} vs median {median_all:.0f}; google share paid {g_share_paid:.2f} vs all {g_share_all:.2f}; "
      f"weeks 35-39 {[round(weekly[w]) for w in range(35, 40)]}")
