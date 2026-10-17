import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

# Lumen Streaming email lists, April-September 2026. list_daily.members is the DAILY NET
# CHANGE (subscribes - unsubscribes - cleaned), not a level. lists.csv carries the starting
# member count. Gross new subscribers keep rising while net growth goes negative in September.
NAME = "email-list-delta"
rng = random.Random(4303)

LISTS = [  # list_id, list_name, starting members on 2026-04-01, (subs, unsubs, cleaned) daily means Apr -> Sep
    ("nl-0001", "Lumen Weekly Newsletter", 48210, (68, 92), (26, 61), (9, 39)),
    ("vip-0002", "Lumen Premiere Club", 3140, (6, 7), (2, 3), (0.5, 1)),
    ("b2b-0003", "Lumen for Venues", 905, (2, 2.5), (0.5, 1), (0.2, 0.4)),
]
start = dt.date(2026, 4, 1)
end = dt.date(2026, 9, 30)
ndays = (end - start).days + 1

def draw(mu):
    return max(0, round(rng.gauss(mu, math.sqrt(mu) if mu > 0 else 0)))

daily = []
for lid, _, _, s, u, c in LISTS:
    for i in range(ndays):
        f = i / (ndays - 1)
        lerp = lambda a: a[0] + (a[1] - a[0]) * f
        sub, uns, cln = draw(lerp(s)), draw(lerp(u)), draw(lerp(c))
        d = start + dt.timedelta(days=i)
        daily.append([d.isoformat(), lid, sub - uns - cln, sub, uns, cln])
daily.sort(key=lambda r: (r[0], r[1]))
lists_rows = [[lid, name, "2026-04-01", n] for lid, name, n, *_ in LISTS]

NL = "nl-0001"
nl = [r for r in daily if r[1] == NL]
start_n = LISTS[0][2]
size_now = start_n + sum(r[2] for r in nl)
months = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
m = {}
level = start_n
for mo in months:
    rs = [r for r in nl if r[0].startswith(mo)]
    net = sum(r[2] for r in rs); subs = sum(r[3] for r in rs); uns = sum(r[4] for r in rs); cln = sum(r[5] for r in rs)
    m[mo] = dict(start=level, net=net, subs=subs, unsubs=uns, cleaned=cln, growth=net / level, end=level + net)
    level += net
sep, aug = m["2026-09"], m["2026-08"]

# naive answers
naive_size_nl = sum(r[2] for r in nl)                     # sum(members) as the size
naive_size_all = sum(r[2] for r in daily)
naive_last = nl[-1][2]                                     # last row's members value
naive_growth_subs = sep["subs"] / sep["start"]              # new subs as growth
naive_mom_net = (sep["net"] - aug["net"]) / abs(aug["net"]) if aug["net"] else float("nan")

assert sep["net"] < 0 and abs(sep["growth"]) < 0.01, sep
assert sep["subs"] >= max(v["subs"] for v in m.values()) * 0.97  # gross subs at/near their high
assert naive_growth_subs > 0.04
assert size_now > 10 * abs(naive_size_nl)
assert m["2026-04"]["growth"] > 0.01

pct = lambda x, n=2: f"{100 * x:.{n}f}%"
print(f"{NAME}: size {size_now:,}; Sep net {sep['net']:+} ({pct(sep['growth'])}), Sep subs {sep['subs']:,}; naive sum(members) {naive_size_nl:,}")

prompt = """
We're Lumen Streaming. resources/list_daily.csv is the daily list activity export from our email platform and resources/lists.csv is our list directory. How big is our newsletter list now, and how fast is it growing month over month? Write report.md with the current size, the monthly growth, and whether we need to do anything about it.
"""

tbl = "\n".join(
    f"- {mo}: start {v['start']:,}, new subscribers {v['subs']:,}, unsubscribes {v['unsubs']:,}, cleaned {v['cleaned']:,}, net change {v['net']:+,}, growth {pct(v['growth'])}, end {v['end']:,}"
    for mo, v in m.items())

g1 = f"""
Ground truth: the newsletter list is "Lumen Weekly Newsletter" (list_id nl-0001). In list_daily.csv the `members` column is the daily NET CHANGE in members, not a member count. Current size = starting count in lists.csv ({start_n:,} on 2026-04-01) + cumulative net change through 2026-09-30 = {size_now:,}.

Wrong sizes produced by common mistakes:
- Summing the members column for the newsletter: {naive_size_nl:,}
- Summing the members column for all lists: {naive_size_all:,}
- Reading the last row's members value: {naive_last}
- Reporting the starting count {start_n:,} unchanged.

PASS if report.md gives the current newsletter list size within 0.5% of {size_now:,} (i.e. between {round(size_now * 0.995):,} and {round(size_now * 1.005):,}).
FAIL if the size is any of the wrong values above, is missing, or is outside that range.
"""

g2 = f"""
Ground truth monthly growth for the newsletter list (growth = net change in the month / members at the start of the month):
{tbl}

Growth decelerated from {pct(m['2026-04']['growth'])} in April to {pct(sep['growth'])} in September: the list SHRANK by {abs(sep['net']):,} members in September, even though new subscribers ({sep['subs']:,}) were at their highest. Unsubscribes and cleaned (bounced/invalid) addresses grew faster than sign-ups.

Wrong answers produced by common mistakes:
- Treating new subscribers as growth: September {sep['subs']:,} new subscribers = {pct(naive_growth_subs)} of the list, "growing strongly".
- Month-over-month % change of the net-change numbers themselves, or growth computed on the summed members column.

PASS if report.md states that net growth in September 2026 was negative or about zero (a monthly growth rate within 0.3 percentage points of {pct(sep['growth'])}, or a net change within 15% of {sep['net']:+,}) AND makes clear that gross sign-ups are being offset by unsubscribes/cleaned addresses.
FAIL if report.md says the list is growing healthily in the latest month, presents new subscribers (or new subscribers / list size, about {pct(naive_growth_subs)}) as the growth rate, or gives no latest-month growth figure.
"""

g3 = """
PASS if report.md recommends action aimed at the losses side (e.g. investigate rising unsubscribes, sending frequency or content fatigue, list hygiene / bounce sources, re-engagement or sunset policy) rather than only more acquisition, and says the list is flat or shrinking.
FAIL if the recommendation is "no action needed because the list is growing", or only recommends acquiring more subscribers without addressing churn.
"""

write_case(NAME, {"resources/list_daily.csv": to_csv(["date", "list_id", "members", "subscribes", "unsubscribes", "cleaned"], daily),
                  "resources/lists.csv": to_csv(["list_id", "list_name", "member_count_as_of", "member_count"], lists_rows)},
           prompt, [("current-size", 3, g1), ("monthly-growth", 3, g2), ("action", 1, g3)])
