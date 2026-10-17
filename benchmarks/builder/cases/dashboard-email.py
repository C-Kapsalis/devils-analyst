"""Dashboard case on the email-mix data: graded on the page's structure, not
only its numbers (headline answer, bridge that adds up, mix vs rate, noise
screen, hypotheses, no mix-driven rise shown as good news)."""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import fixture, write_case  # noqa: E402

text = fixture("email-mix", "resources/email_sends.csv")
rows = list(csv.DictReader(text.splitlines()))
for r in rows:
    r["month"] = r["send_date"][:7]

def tot(month, seg=None):
    sel = [r for r in rows if r["month"] == month and (seg is None or r["segment"] == seg)]
    return {k: sum(float(r[k]) for r in sel) for k in ("delivered", "unique_clicks", "orders", "revenue")}

aug, sep = tot("2026-08"), tot("2026-09")
ctr_aug = aug["unique_clicks"] / aug["delivered"]
ctr_sep = sep["unique_clicks"] / sep["delivered"]
segs = sorted({r["segment"] for r in rows})
both = [s for s in segs if tot("2026-08", s)["delivered"] and tot("2026-09", s)["delivered"]]
new = [s for s in segs if s not in both]
lfl_aug = sum(tot("2026-08", s)["revenue"] for s in both)
lfl_sep = sum(tot("2026-09", s)["revenue"] for s in both)
new_rev = sum(tot("2026-09", s)["revenue"] for s in new)

# Like-for-like CTR: continuing segments only.
lfl_ctr_aug = sum(tot("2026-08", s)["unique_clicks"] for s in both) / sum(tot("2026-08", s)["delivered"] for s in both)
lfl_ctr_sep = sum(tot("2026-09", s)["unique_clicks"] for s in both) / sum(tot("2026-09", s)["delivered"] for s in both)

assert ctr_sep > ctr_aug and lfl_ctr_sep < lfl_ctr_aug, "blended CTR rises while like-for-like falls"
change = sep["revenue"] - aug["revenue"]
print(f"revenue {aug['revenue']:.0f} -> {sep['revenue']:.0f} ({change:+.0f}); new segment {new_rev:.0f}; "
      f"CTR {ctr_aug:.2%} -> {ctr_sep:.2%}, like-for-like {lfl_ctr_aug:.2%} -> {lfl_ctr_sep:.2%}")

prompt = """
resources/email_sends.csv has our email sends for August and September 2026 (one row per campaign send to one segment). Build me a dashboard as a single self-contained HTML file, dashboard.html (inline CSS and JS, no external requests), that shows how email did in September compared with August, why, and what we should do next. My team will look at it in our Monday meeting.
"""

g = []
g.append(("headline-answer", 2, f"""
Ground truth: email revenue rose from ${aug['revenue']:,.0f} to ${sep['revenue']:,.0f} ({change:+,.0f}), but a segment sent only in September ({', '.join(new)}) brought ${new_rev:,.0f}; the segments sent in both months fell from ${lfl_aug:,.0f} to ${lfl_sep:,.0f}.

PASS if the dashboard's title or opening headline (the first sentence a reader sees, above the charts) states this answer: that the overall rise comes from the new segment while the continuing segments declined.
FAIL if the title is only a topic ("Email performance", "September report") with no answer, or if the headline presents the revenue rise as general improvement.
"""))
g.append(("bridge-adds-up", 3, f"""
Ground truth: the revenue change is {change:+,.0f} (${aug['revenue']:,.0f} to ${sep['revenue']:,.0f}).

PASS if the dashboard decomposes the revenue change into driver or segment contributions (a bridge/waterfall chart or a table: e.g. delivered volume, click rate, click-to-order, order value, new segment; or one row per segment) whose amounts are shown as numbers and add up (within about 2%) to the total change of {change:+,.0f}.
FAIL if there is no decomposition of the change, if contributions are described only in words, or if the shown parts do not add up to the total change.
"""))
g.append(("mix-vs-rate", 2, f"""
Ground truth: blended click rate (unique clicks / delivered) went from {ctr_aug:.2%} to {ctr_sep:.2%}, but within the segments sent in both months it went from {lfl_ctr_aug:.2%} to {lfl_ctr_sep:.2%}: the rise is audience mix (the new high-engagement segment), not better engagement.

PASS if the dashboard separates the click-rate change (or another rate's change) into mix versus within-segment change with numbers, OR clearly shows like-for-like (continuing segments) rates next to the blended rate and says the blended rise is mix.
FAIL if the blended click-rate rise is shown as an improvement without separating mix from within-segment change.
"""))
g.append(("no-good-news-on-mix", 1, f"""
Ground truth: blended click rate rose ({ctr_aug:.2%} to {ctr_sep:.2%}) only because of mix; like-for-like it fell.

Read the KPI tiles or headline numbers. PASS if a blended click-rate (CTR) tile, if present, is not styled or labelled as good news (no green/up-good styling or "improved" label without a mix caveat on or next to the tile), or if no blended CTR tile is shown.
FAIL if a blended CTR tile is shown as an improvement (green, "up", "improved") with no mix caveat on or next to it.
"""))
g.append(("hypotheses-and-checks", 2, """
PASS if every recommended action on the dashboard is paired with a way to check it (a data source and cut, a test, or a metric to watch), AND causes the data cannot prove (inbox placement, subject lines, cannibalization by the new segment, site changes) are labelled as hypotheses / likely causes rather than stated as fact.
FAIL if any recommendation has no way to verify it, or an unproven cause is stated as fact.
"""))

write_case("dashboard-email", {"resources/email_sends.csv": text}, prompt, g, output="dashboard.html")
