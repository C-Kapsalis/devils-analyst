"""Facebook organic: (a) hashtags look like they drive engagement only because
videos carry more hashtags; within a post type the link is ~0. (b) Averaging
per-post engagement rates lets a few tiny-reach link posts with huge rates
make links look best; pooled rates put video first. (c) fan_count is a
lifetime snapshot; September gain is the sum of fan_count_diff (end - start)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
from datetime import date, timedelta

NAME = "fb-organic-playbook"
rng = random.Random(2723)

TYPES = {  # share, hashtag range, median reach, engagement rate
    "video": (0.30, (4, 9), 6200, 0.064),
    "image": (0.45, (1, 5), 3600, 0.031),
    "link":  (0.25, (0, 3), 2600, 0.017),
}

posts = []
d0 = date(2026, 7, 1)
pid = 0
TINY_DAYS = {9, 23, 41, 55, 70, 84}
for i in range(92):
    d = d0 + timedelta(days=i)
    n = 1 if rng.random() < 0.8 else 2
    if i in TINY_DAYS:  # small posts that barely got distributed; staff reactions dominate
        pid += 1
        reach = rng.randint(35, 110)
        eng = int(reach * rng.uniform(0.28, 0.45))
        posts.append((d, pid, "link", rng.randint(0, 2), reach, eng))
    for _ in range(n):
        pid += 1
        u = rng.random()
        t = "video" if u < 0.30 else ("image" if u < 0.75 else "link")
        _, (h0, h1), med, er = TYPES[t]
        tags = rng.randint(h0, h1)
        reach = int(med * math.exp(rng.gauss(0, 0.45)))
        eng = int(reach * er * math.exp(rng.gauss(0, 0.25)))
        posts.append((d, pid, t, tags, reach, eng))

rows = []
for d, p, t, tags, reach, eng in posts:
    shares = int(eng * rng.uniform(0.12, 0.25))
    comments = int(eng * rng.uniform(0.06, 0.12))
    reactions = eng - shares - comments
    rows.append([f"1048839201_{p:05d}", f"{d.isoformat()}T{rng.randint(8, 19):02d}:{rng.choice(['00', '15', '30', '45'])}:00",
                 t, tags, reach, reactions, comments, shares])
posts_csv = to_csv(["post_id", "created_time", "post_type", "n_hashtags", "reach", "reactions", "comments", "shares"], rows)

page = []
fans = 24180
for i in range(92):
    d = d0 + timedelta(days=i)
    diff = int(round(rng.gauss(13, 9)))
    fans += diff
    page.append([d.isoformat(), fans, diff, int(rng.gauss(5200, 900))])
page_csv = to_csv(["date", "fan_count", "fan_count_diff", "page_impressions_unique"], page)

# ---- ground truth ----
E = lambda r: r[5] + r[6] + r[7]
def pearson(xs, ys):
    n = len(xs); mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)

r_all = pearson([r[3] for r in rows], [E(r) for r in rows])
r_type = {t: pearson([r[3] for r in rows if r[2] == t], [E(r) for r in rows if r[2] == t]) for t in TYPES}
big = [r for r in rows if r[4] >= 500]
r_all_rate = pearson([r[3] for r in big], [E(r) / r[4] for r in big])
r_type_rate = {t: pearson([r[3] for r in big if r[2] == t], [E(r) / r[4] for r in big if r[2] == t]) for t in TYPES}
assert r_all > 0.45 and r_all_rate > 0.45, (r_all, r_all_rate)
assert all(abs(v) < 0.2 for v in r_type.values()) and all(abs(v) < 0.2 for v in r_type_rate.values()), (r_type, r_type_rate)

pooled = {t: sum(E(r) for r in rows if r[2] == t) / sum(r[4] for r in rows if r[2] == t) for t in TYPES}
mean_rate = {t: sum(E(r) / r[4] for r in rows if r[2] == t) / sum(1 for r in rows if r[2] == t) for t in TYPES}
cnt = {t: sum(1 for r in rows if r[2] == t) for t in TYPES}
assert max(pooled, key=pooled.get) == "video" and max(mean_rate, key=mean_rate.get) == "link", (pooled, mean_rate)
avg_tags = {t: sum(r[3] for r in rows if r[2] == t) / cnt[t] for t in TYPES}

sep = [p for p in page if p[0].startswith("2026-09")]
aug_end = [p for p in page if p[0] == "2026-08-31"][0][1]
gain = sum(p[2] for p in sep)
assert gain == sep[-1][1] - aug_end
gain_alt = sep[-1][1] - sep[0][1]
naive_sum = sum(p[1] for p in sep)
assert naive_sum > 100 * gain

tiny = [r for r in rows if r[4] < 200]
tiny_rates = [100 * E(r) / r[4] for r in tiny]
assert mean_rate["link"] > 1.2 * mean_rate["video"]
pct = lambda x: f"{100 * x:.2f}%"
pooled_line = ", ".join(f"{t} {pct(pooled[t])}" for t in TYPES)
mean_line = ", ".join(f"{t} {pct(mean_rate[t])}" for t in TYPES)
rtype_line = ", ".join(f"{t} r = {r_type[t]:.2f}" for t in TYPES)
tags_line = ", ".join(f"{t} {avg_tags[t]:.1f}" for t in TYPES)

prompt = """
resources/ has our Facebook page post export for July-September 2026 (fb_posts.csv) and the page's daily stats (fb_page_daily.csv). What makes our Facebook posts perform best, and how many followers did we gain in September? Give me 2-3 changes to our posting playbook. Write it up in report.md.
"""

g_drivers = f"""
Engagement = reactions + comments + shares. Ground truth from the post data:
- Post type drives engagement. Engagement rate (total engagements / total reach, pooled): {pooled_line}. Video is best.
- Hashtags do NOT drive engagement. Across all posts, n_hashtags correlates with engagements (r = {r_all:.2f}), but only because videos carry more hashtags (average hashtags: {tags_line}). Within each post type the correlation is about zero ({rtype_line}).

PASS if report.md identifies video (post type) as the main driver of performance AND does not recommend adding more hashtags as a way to lift engagement (it may say hashtags show no effect once post type is accounted for, or simply not recommend them).
FAIL if it recommends using more hashtags (or a hashtag count) to boost engagement, or claims hashtags drive engagement based on the raw cross-post correlation.
"""

g_rate = f"""
Engagement rate by post type must be pooled (sum of engagements / sum of reach): {pooled_line}, so video is best and link posts are worst.
The trap: {len(tiny)} link posts reached only {min(r[4] for r in tiny)}-{max(r[4] for r in tiny)} people each but have {min(tiny_rates):.0f}-{max(tiny_rates):.0f}% engagement rates. Averaging per-post rates gives {mean_line}, which wrongly makes link posts look best.

PASS if report.md's engagement rates by type are the pooled ones (within 10% relative) or otherwise ranks video above image above link on engagement rate, AND it does not claim link posts have the highest engagement rate.
FAIL if it reports link posts as the best-engaging type or uses the per-post-average rates ({mean_line}) for its ranking.
"""

g_fans = f"""
fan_count is the page's lifetime follower total on each day; fan_count_diff is the daily net change.
Ground truth September 2026 follower gain = sum of September fan_count_diff = fan_count on Sep 30 ({sep[-1][1]:,}) minus fan_count on Aug 31 ({aug_end:,}) = {gain:,}.
Also acceptable: Sep 30 minus Sep 1 fan_count = {gain_alt:,}.
Wrong answers: summing fan_count over September ({naive_sum:,}); reporting the total follower count ({sep[-1][1]:,}) as the gain.

PASS if report.md states a September net follower gain between {min(gain, gain_alt):,} and {max(gain, gain_alt):,} (inclusive, allow plus or minus 2).
FAIL if it gives {naive_sum:,} or {sep[-1][1]:,} as the gain, or any other number outside that range, or gives no September gain.
"""

write_case(NAME, {"resources/fb_posts.csv": posts_csv, "resources/fb_page_daily.csv": page_csv},
           prompt, [("drivers-hashtag-confound", 3, g_drivers), ("pooled-rate", 2, g_rate), ("follower-gain", 2, g_fans)])
print(f"{NAME}: posts {len(rows)}; r_all {r_all:.2f} within {r_type}; pooled {pooled}; per-post mean {mean_rate}; "
      f"Sep gain {gain} (alt {gain_alt}, naive {naive_sum})")
