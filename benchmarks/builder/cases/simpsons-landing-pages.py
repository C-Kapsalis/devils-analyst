import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

# Harbor Outdoor GA4 landing-page report, Q3 2026, weekly x landing page x device.
# /lp-a beats /lp-b on every device, but /lp-a's traffic is ~85% mobile (low-converting)
# while /lp-b's is mostly desktop, so the blended rate makes /lp-a look ~2x worse (Simpson's paradox).
NAME = "simpsons-landing-pages"
rng = random.Random(4707)

# page -> device -> (weekly sessions mean, true conversion rate)
SPEC = {
    "/lp-a": {"mobile": (3900, 0.0160), "desktop": (420, 0.061), "tablet": (260, 0.032)},
    "/lp-b": {"mobile": (620, 0.0112), "desktop": (3300, 0.050), "tablet": (240, 0.026)},
}
weeks = [dt.date(2026, 6, 29) + dt.timedelta(days=7 * i) for i in range(13)]
rows = []
for w in weeks:
    for page, devs in SPEC.items():
        for dev, (mu, cr) in devs.items():
            s = max(1, round(rng.gauss(mu, mu * 0.08)))
            c = max(0, round(rng.gauss(s * cr, math.sqrt(s * cr * (1 - cr)))))
            rows.append([w.isoformat(), page, dev, s, c])
header = ["week_start", "landing_page", "device_category", "sessions", "conversions"]

agg = {}
for _, p, d, s, c in rows:
    a = agg.setdefault((p, d), [0, 0]); a[0] += s; a[1] += c
DEV = ["mobile", "desktop", "tablet"]
cr = {k: v[1] / v[0] for k, v in agg.items()}
tot = {p: [sum(agg[(p, d)][0] for d in DEV), sum(agg[(p, d)][1] for d in DEV)] for p in SPEC}
blend = {p: tot[p][1] / tot[p][0] for p in SPEC}
mix_a = {d: agg[("/lp-a", d)][0] / tot["/lp-a"][0] for d in DEV}
mix_b = {d: agg[("/lp-b", d)][0] / tot["/lp-b"][0] for d in DEV}
all_s = sum(tot[p][0] for p in SPEC)
mix_pool = {d: sum(agg[(p, d)][0] for p in SPEC) / all_s for d in DEV}
std = {p: sum(mix_pool[d] * cr[(p, d)] for d in DEV) for p in SPEC}
std_on_b = {p: sum(mix_b[d] * cr[(p, d)] for d in DEV) for p in SPEC}
std_on_a = {p: sum(mix_a[d] * cr[(p, d)] for d in DEV) for p in SPEC}

def z_two_prop(c1, n1, c2, n2):
    p = (c1 + c2) / (n1 + n2)
    return (c1 / n1 - c2 / n2) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
z = {d: z_two_prop(agg[("/lp-a", d)][1], agg[("/lp-a", d)][0], agg[("/lp-b", d)][1], agg[("/lp-b", d)][0]) for d in DEV}

A, B = "/lp-a", "/lp-b"
assert all(cr[(A, d)] > cr[(B, d)] for d in DEV)
assert blend[B] > 1.8 * blend[A], (blend[A], blend[B])
assert std[A] > std[B] and std_on_a[A] > std_on_a[B] and std_on_b[A] > std_on_b[B]
assert z["mobile"] > 2.5 and z["desktop"] > 2.5, z

pct = lambda x, n=2: f"{100 * x:.{n}f}%"
print(f"{NAME}: blended A {pct(blend[A])} vs B {pct(blend[B])}; at pooled mix A {pct(std[A])} vs B {pct(std[B])}; mobile {pct(cr[(A,'mobile')])}/{pct(cr[(B,'mobile')])} desktop {pct(cr[(A,'desktop')])}/{pct(cr[(B,'desktop')])}")

prompt = """
We're Harbor Outdoor. resources/ga4_landing_pages.csv is our GA4 landing page report for Q3 2026 (weekly sessions and conversions by landing page and device). Which landing page converts better, /lp-a or /lp-b? We're about to send all paid traffic to the winner. Write report.md with the conversion rates and which page we should use.
"""

dev_tbl = "\n".join(
    f"- {d}: /lp-a {pct(cr[(A, d)])} ({agg[(A, d)][1]:,}/{agg[(A, d)][0]:,}) vs /lp-b {pct(cr[(B, d)])} ({agg[(B, d)][1]:,}/{agg[(B, d)][0]:,}), z = {z[d]:.1f}"
    for d in DEV)

g1 = f"""
Ground truth conversion rate (conversions / sessions) by device, Q3 2026:
{dev_tbl}
/lp-a converts better on EVERY device. Its blended rate is lower only because {pct(mix_a['mobile'], 0)} of its sessions are mobile (the lowest-converting device) versus {pct(mix_b['mobile'], 0)} for /lp-b.
At the same device mix (both pages' combined mix: {', '.join(f'{d} {pct(mix_pool[d], 0)}' for d in DEV)}): /lp-a {pct(std[A])} vs /lp-b {pct(std[B])}.

Wrong answer produced by the common mistake: blended totals, /lp-a {pct(blend[A])} vs /lp-b {pct(blend[B])}, so "/lp-b converts about {blend[B] / blend[A]:.1f}x better; send all paid traffic to /lp-b".

PASS if report.md picks /lp-a as the better-converting page (or the page to send paid traffic to) because it wins within each device / at a comparable device mix.
FAIL if report.md picks /lp-b, or declares /lp-b the better converter based on the blended rates, or gives no clear answer.
"""

g2 = f"""
PASS if report.md reports device-level conversion rates for both pages for at least mobile and desktop, each within 0.3 percentage points of: mobile /lp-a {pct(cr[(A, 'mobile')])}, /lp-b {pct(cr[(B, 'mobile')])}; desktop /lp-a {pct(cr[(A, 'desktop')])}, /lp-b {pct(cr[(B, 'desktop')])}.
FAIL if device-level rates are missing for either page or any of these four is off by more than 0.3 percentage points.
"""

g3 = f"""
Blended (all devices) conversion rates are /lp-a {pct(blend[A])} and /lp-b {pct(blend[B])}; the gap is caused by device mix (/lp-a {pct(mix_a['mobile'], 0)} mobile, /lp-b {pct(mix_b['mobile'], 0)} mobile).
PASS if report.md explains that the blended comparison is misleading because the two pages receive different device mixes (mix effect / Simpson's paradox / traffic composition), OR notes that the outcome for paid traffic depends on the paid traffic's device mix and /lp-a still wins on each device.
FAIL if report.md presents the blended rates as the fair comparison without mentioning device mix.
"""

write_case(NAME, {"resources/ga4_landing_pages.csv": to_csv(header, rows)}, prompt,
           [("winner", 3, g1), ("device-rates", 2, g2), ("mix-explained", 1, g3)])
