"""YouTube video-day export: average_view_duration per row cannot be averaged
(weight by views: minutes*60/views); Shorts and long-form must be separated;
'holds viewers best' is % of the video watched, not AVD seconds (which
favours the 42-minute video)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "youtube-retention"
rng = random.Random(6604)

# video_id: (title, type, duration s, base daily views, avg view fraction)
VIDEOS = {
    "hX3k9TqLm2A": ("Tent pitch in 60 seconds", "short", 52, 3900, 0.84),
    "pQ8vN1rWz7c": ("Knot of the week: bowline", "short", 31, 5200, 1.04),
    "aZ5yB6uKe0d": ("Headlamp vs lantern", "short", 44, 2600, 0.79),
    "mW2cR8sJh4f": ("Rain test: shell jacket", "short", 58, 3100, 0.72),
    "tE7gL3nVx9b": ("Pack a daypack fast", "short", 27, 4400, 0.91),
    "Lk4dF9pRa1Q": ("5 campsite mistakes", "video", 371, 980, 0.52),
    "Bv7nH2qTc8W": ("Choosing trail runners", "video", 526, 720, 0.48),
    "Rj1sM6wYe3Z": ("Stove setup and safety", "video", 681, 610, 0.63),
    "Ng8uC4kXo5P": ("Layering for cold hikes", "video", 787, 520, 0.47),
    "Fy2tA7dGi6S": ("Water filters compared", "video", 992, 410, 0.42),
    "Qc5wE1zUb2N": ("First solo overnight", "video", 1181, 300, 0.38),
    "Hm9pK3vDf7R": ("Tent buying guide 2026", "video", 1457, 240, 0.31),
    "Wd6rT8cLs4Y": ("Full kit review: 3 seasons", "video", 1912, 140, 0.27),
    "Zs3gY5bNq1M": ("Coast trail: full trip film", "video", 2551, 38, 0.245),
}

rows = []
for d in range(1, 31):
    date = f"2026-09-{d:02d}"
    wk = 1.12 if (d + 1) % 7 in (5, 6) else 1.0  # weekend bump (Sep 5/6 is Sat/Sun)
    for vid, (title, vt, dur, base, frac) in VIDEOS.items():
        views = max(4, int(base * wk * math.exp(rng.gauss(0, 0.18))))
        noise = rng.gauss(0, 0.05 + 0.6 / math.sqrt(views))
        avd = max(5, int(round(dur * frac * (1 + noise))))
        minutes = round(views * avd / 60)
        avd = int(round(minutes * 60 / views))
        avp = round(100 * avd / dur, 2)
        rows.append([date, vid, title, vt, dur, views, minutes, avd, avp])

header = ["date", "video_id", "title", "video_type", "duration_seconds", "views", "estimated_minutes_watched",
          "average_view_duration", "average_view_percentage"]
yt_csv = to_csv(header, rows)

# ---- ground truth ----
def wavd(rr):
    return sum(r[6] for r in rr) * 60 / sum(r[5] for r in rr)

long_rows = [r for r in rows if r[3] == "video"]
short_rows = [r for r in rows if r[3] == "short"]
avd_long = wavd(long_rows)
avd_short = wavd(short_rows)
avd_all_w = wavd(rows)
avd_all_mean = sum(r[7] for r in rows) / len(rows)
avd_long_mean = sum(r[7] for r in long_rows) / len(long_rows)
for bad in (avd_all_w, avd_all_mean, avd_long_mean):
    assert abs(bad - avd_long) / avd_long > 0.15, (bad, avd_long)

per = {}
for vid, (title, vt, dur, *_rest) in VIDEOS.items():
    rr = [r for r in rows if r[1] == vid]
    a = wavd(rr)
    per[vid] = dict(title=title, type=vt, dur=dur, views=sum(r[5] for r in rr), avd=a, pct=100 * a / dur)
longv = {k: v for k, v in per.items() if v["type"] == "video"}
best_pct = max(longv, key=lambda k: longv[k]["pct"])
best_sec = max(longv, key=lambda k: longv[k]["avd"])
assert per[best_pct]["title"] == "Stove setup and safety" and per[best_sec]["dur"] > 2400
rank_pct = sorted(longv, key=lambda k: -longv[k]["pct"])
assert rank_pct.index(best_sec) >= 6
second = rank_pct[1]

mmss = lambda s: f"{int(s // 60)}:{int(round(s % 60)):02d}"
long_table = "\n".join(
    f"- {v['title']} ({mmss(v['dur'])} long): {v['views']:,} views, AVD {mmss(v['avd'])}, {v['pct']:.1f}% viewed"
    for k, v in sorted(longv.items(), key=lambda kv: -kv[1]["pct"]))

prompt = """
resources/youtube_video_daily.csv is our YouTube Studio export for September 2026 (one row per video per day). What's our average view duration, and which videos hold viewers best? We're planning next quarter's long-form videos, so tell me what kind of video we should make more of. Write report.md.
"""

g_avd = f"""
Average view duration must be weighted by views (estimated_minutes_watched * 60 / views) and long-form videos (video_type = video) must be reported separately from Shorts.
Ground truth, September 2026:
- Long-form AVD: {avd_long:.0f} seconds ({mmss(avd_long)})
- Shorts AVD: {avd_short:.0f} seconds
Wrong answers:
- Simple average of the average_view_duration column over all rows: {avd_all_mean:.0f} s ({mmss(avd_all_mean)})
- Simple average of average_view_duration over long-form rows: {avd_long_mean:.0f} s ({mmss(avd_long_mean)})
- Weighted AVD with Shorts and long-form mixed together: {avd_all_w:.0f} s ({mmss(avd_all_w)})

PASS if report.md gives a long-form AVD of {avd_long:.0f} s (within 5%, i.e. {0.95 * avd_long:.0f}-{1.05 * avd_long:.0f} s), reported separately from Shorts.
FAIL if the headline or long-form AVD is one of the wrong values above (or otherwise outside 5%), or if only a single blended Shorts + long-form figure is given.
"""

g_best = f"""
"Holds viewers best" means the share of the video people watch (average view percentage = AVD / duration, weighted by views), compared among long-form videos (Shorts loop and are not comparable).
Ground truth long-form ranking by % viewed:
{long_table}
Best retention: "{per[best_pct]['title']}" ({mmss(per[best_pct]['dur'])} long, {per[best_pct]['pct']:.1f}% viewed). Runner-up: "{per[second]['title']}" ({per[second]['pct']:.1f}%).
The trap: ranking by AVD seconds puts "{per[best_sec]['title']}" ({mmss(per[best_sec]['dur'])} long) first with {mmss(per[best_sec]['avd'])}, but viewers watch only {per[best_sec]['pct']:.1f}% of it, near the bottom of the list.

PASS if report.md names "{per[best_pct]['title']}" as the long-form video that holds viewers best (by percentage viewed), and does not present "{per[best_sec]['title']}" as the best at holding viewers.
Reporting Shorts' retention separately is fine.
FAIL if it names "{per[best_sec]['title']}" as the video that holds viewers best, names a Short as the best answer for long-form without separating the two formats, or ranks retention by AVD seconds only.
"""

g_plan = f"""
Ground truth: the share of the video watched peaks at mid-length and falls with length beyond that; the best-retaining long-form videos are about 6-13 minutes (top: "{per[best_pct]['title']}" at {mmss(per[best_pct]['dur'])}), while 24-43 minute videos keep only {longv[rank_pct[-1]]['pct']:.0f}-{longv[rank_pct[-3]]['pct']:.0f}% and get few views.

PASS if report.md's long-form recommendation favours mid-length / practical how-to videos like "{per[best_pct]['title']}" (or explicitly says longer videos lose viewers), consistent with the percentage-viewed ranking.
FAIL if it recommends making longer (30-40+ minute) videos because they have the highest average view duration, or recommends Shorts-style content as the long-form plan based on Shorts' high percentages.
"""

write_case(NAME, {"resources/youtube_video_daily.csv": yt_csv},
           prompt, [("avd-weighted", 3, g_avd), ("best-retention", 3, g_best), ("longform-plan", 1, g_plan)])
print(f"{NAME}: long AVD {avd_long:.0f}s (naive all-row mean {avd_all_mean:.0f}, long mean {avd_long_mean:.0f}, "
      f"blended {avd_all_w:.0f}); best % {per[best_pct]['title']} {per[best_pct]['pct']:.1f}%; best secs {per[best_sec]['title']}")
