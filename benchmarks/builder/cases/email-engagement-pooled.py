import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

# Harbor Outdoor Q3 2026 email campaigns: five small targeted segments sent every
# two weeks with 4-6% unique click rate, plus one huge weekly catch-all blast at ~1%.
NAME = "email-engagement-pooled"
rng = random.Random(4101)

SEGMENTS = [
    ("restock_alert_trail_runners", 6500),
    ("vip_early_access", 4200),
    ("cart_followup_weekly", 3100),
    ("new_arrivals_hikers", 9400),
    ("loyalty_points_reminder", 11800),
]
BLAST = "weekly_all_subscribers"

import datetime as dt
start = dt.date(2026, 7, 2)
rows = []  # campaign, sent, bounces, delivered, opens, unique_opens, clicks, unique_clicks, unsubscribes
kinds = {}
for w in range(13):
    d = start + dt.timedelta(days=7 * w)
    sent = int(rng.uniform(232000, 241000))
    bounces = round(sent * rng.uniform(0.012, 0.018))
    delivered = sent - bounces
    uo = round(delivered * rng.uniform(0.135, 0.155))
    uc = round(delivered * rng.uniform(0.0092, 0.0108))
    name = f"{d.isoformat()}_{BLAST}"
    rows.append([name, sent, bounces, delivered, round(uo * rng.uniform(1.4, 1.7)), uo,
                 round(uc * rng.uniform(1.3, 1.55)), uc, round(delivered * rng.uniform(0.0030, 0.0038))])
    kinds[name] = "blast"
    if w % 2 == 0:
        for i, (seg, base) in enumerate(SEGMENTS):
            dd = d + dt.timedelta(days=1 + i % 3)
            sent = int(base * rng.uniform(0.92, 1.08))
            bounces = round(sent * rng.uniform(0.003, 0.009))
            delivered = sent - bounces
            uo = round(delivered * rng.uniform(0.36, 0.46))
            uc = round(delivered * rng.uniform(0.042, 0.059))
            name = f"{dd.isoformat()}_{seg}"
            rows.append([name, sent, bounces, delivered, round(uo * rng.uniform(1.4, 1.8)), uo,
                         round(uc * rng.uniform(1.3, 1.6)), uc, round(delivered * rng.uniform(0.0008, 0.0014))])
            kinds[name] = "segment"
rows.sort(key=lambda r: r[0])
header = ["campaign", "sent", "bounces", "delivered", "opens", "unique_opens", "clicks", "unique_clicks", "unsubscribes"]

def S(rs, i):
    return sum(r[i] for r in rs)

blast = [r for r in rows if kinds[r[0]] == "blast"]
seg = [r for r in rows if kinds[r[0]] == "segment"]
# truth: pooled, unique, on delivered
ctr = S(rows, 7) / S(rows, 3)
ctor = S(rows, 7) / S(rows, 5)
open_rate = S(rows, 5) / S(rows, 3)
ctr_b, ctr_s = S(blast, 7) / S(blast, 3), S(seg, 7) / S(seg, 3)
ctor_b, ctor_s = S(blast, 7) / S(blast, 5), S(seg, 7) / S(seg, 5)
unsub_b, unsub_s = S(blast, 8) / S(blast, 3), S(seg, 8) / S(seg, 3)
blast_send_share = S(blast, 3) / S(rows, 3)
# naive
mean_ctr = sum(r[7] / r[3] for r in rows) / len(rows)
mean_ctor = sum(r[7] / r[5] for r in rows) / len(rows)
ctr_sent = S(rows, 7) / S(rows, 1)
ctr_total = S(rows, 6) / S(rows, 3)
ctr_total_sent = S(rows, 6) / S(rows, 1)
ctor_total = S(rows, 6) / S(rows, 4)

assert mean_ctr > 2.5 * ctr, (mean_ctr, ctr)
assert ctr_total > 1.25 * ctr
assert abs(ctr_sent - ctr) > 0.0001
assert 0.04 <= ctr_s <= 0.06 and 0.008 <= ctr_b <= 0.012
assert ctor >= 0.05 and ctor_s > 0.10
assert blast_send_share > 0.9

pct = lambda x, n=2: f"{100 * x:.{n}f}%"
print(f"{NAME}: pooled unique CTR {pct(ctr)} CTOR {pct(ctor)}; segments {pct(ctr_s)} blast {pct(ctr_b)}; naive mean CTR {pct(mean_ctr)}")

prompt = """
We're Harbor Outdoor. resources/email_campaigns.csv is our email platform's campaign export for last quarter (July-September 2026). How is our email engagement doing, and what should we change? Write report.md with our click rate and the main recommendation.
"""

g1 = f"""
Ground truth for Harbor Outdoor email engagement, July-September 2026 (all campaigns pooled: sum of unique_clicks / sum of delivered, and sum of unique_clicks / sum of unique_opens):
- Pooled unique click rate (CTR) on delivered: {pct(ctr)}
- Pooled click-to-open rate (CTOR, unique clicks / unique opens): {pct(ctor, 1)}
- Pooled unique open rate on delivered: {pct(open_rate, 1)}

Wrong numbers produced by common mistakes:
- Simple average of the per-campaign click rates: {pct(mean_ctr)} (overstates; ignores that the weekly blast is >90% of volume)
- Average of per-campaign CTOR: {pct(mean_ctor, 1)}
- Total (non-unique) clicks / delivered: {pct(ctr_total)}; total clicks / sent: {pct(ctr_total_sent)}
- Unique clicks / sent: {pct(ctr_sent, 3)} (small difference, acceptable only if labelled as per-sent)
- Total clicks / total opens as CTOR: {pct(ctor_total, 1)}

PASS if report.md states an overall click rate within 0.10 percentage points of {pct(ctr)} (unique clicks / sent at {pct(ctr_sent, 3)} is also acceptable) AND either reports CTOR within 1.0 percentage point of {pct(ctor, 1)} or does not report an overall CTOR at all.
FAIL if the headline overall click rate is the averaged per-campaign rate (around {pct(mean_ctr)}) or a total-clicks rate (around {pct(ctr_total)}), or if no overall click rate is given.
"""

g2 = f"""
Ground truth breakdown:
- The weekly catch-all blast ("weekly_all_subscribers", 13 sends) is {pct(blast_send_share, 0)} of all delivered email. Its unique click rate is {pct(ctr_b)}, CTOR {pct(ctor_b, 1)}, unsubscribe rate {pct(unsub_b)} of delivered.
- The five targeted segment campaigns (restock alerts, VIP early access, cart follow-up, new arrivals, loyalty reminders) have a pooled unique click rate of {pct(ctr_s)}, CTOR {pct(ctor_s, 1)}, unsubscribe rate {pct(unsub_s)}.
- So the low pooled click rate is caused by one send: the catch-all blast. The targeted program is healthy (roughly {ctr_s / ctr_b:.0f}x the blast's click rate).

PASS if report.md identifies the weekly all-subscribers blast as the drag on engagement (contrasted with the much stronger targeted segments) AND its main recommendation is to fix that send (e.g. segment it, suppress unengaged subscribers, cut its frequency or audience, or shift volume to the targeted programs).
FAIL if report.md concludes that email engagement is weak across the board, recommends a generic overhaul of all emails (subject lines, design, templates for everything) without singling out the blast, or does not distinguish the blast from the targeted campaigns.
"""

g3 = f"""
PASS if report.md gives separate click rates for the weekly blast and the targeted campaigns that are each within 0.5 percentage points of the ground truth: blast {pct(ctr_b)}, targeted segments pooled {pct(ctr_s)} (individual segment rates between 4% and 6% are also acceptable in place of the pooled segment figure).
FAIL if no separate rates are given, or if they are off by more than 0.5 percentage points.
"""

write_case(NAME, {"resources/email_campaigns.csv": to_csv(header, rows)}, prompt,
           [("pooled-rates", 3, g1), ("blast-is-the-problem", 2, g2), ("segment-split", 1, g3)])
