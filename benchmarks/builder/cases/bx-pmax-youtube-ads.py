"""Breadth benchmark, video: YouTube ads readout before a CMO meeting (Brightwell Bikes, September 2026).

Subtle problems (4): the cheapest-CPV ad ("Trail Story 45s") shows the brand
at second 38 and its audience collapses after the first quartile; per
impression that reaches the brand moment it is the most expensive (DECISION: scale "Saddle Up 20s"
instead); the "viewers convert 2.9x non-viewers" claim compares exposed with
unexposed people, not a randomised holdout; weekly frequency rose from ~2 to
~7 while view rate fell (wear-out); a quarter of impressions ran on
made-for-kids channels, which are not excluded.
Decoys (2): bumper ads have no views or CPV (6-second non-skippable format);
video CTR around 0.3%."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-pmax-youtube-ads"
rng = random.Random(51840)

# ad: format, duration, brand_first_sec, impressions, view rate, cpv, q25, q50, q75, q100, ctr
ADS = {
    "Trail Story 45s": ("skippable_instream", 45, 38, 820000, 0.11, 0.018, 0.21, 0.13, 0.09, 0.05, 0.0026),
    "Saddle Up 20s": ("skippable_instream", 20, 2, 610000, 0.30, 0.034, 0.78, 0.55, 0.40, 0.30, 0.0034),
    "Commute Hack 30s": ("skippable_instream", 30, 4, 540000, 0.25, 0.040, 0.66, 0.45, 0.33, 0.25, 0.0031),
    "Spin Bumper A 6s": ("bumper", 6, 0, 900000, None, None, 0.92, 0.86, 0.81, 0.77, 0.0012),
    "Spin Bumper B 6s": ("bumper", 6, 0, 760000, None, None, 0.91, 0.85, 0.80, 0.76, 0.0011),
}
BUMPER_CPM = 5.4
ad_rows, st = [], {}
for ad, (fmt, dur, bfs, imps0, vr, cpv, q25, q50, q75, q100, ctr) in ADS.items():
    imps = int(imps0 * rng.uniform(0.97, 1.03))
    if vr is None:
        views = None; cost = round(imps * BUMPER_CPM / 1000 * rng.uniform(0.98, 1.02), 2); avg_cpv = None; view_rate = None
    else:
        views = int(imps * vr * rng.uniform(0.97, 1.03)); cost = round(views * cpv * rng.uniform(0.98, 1.02), 2)
        avg_cpv = round(cost / views, 4); view_rate = round(views / imps, 4)
    clicks = int(imps * ctr * rng.uniform(0.92, 1.08))
    ad_rows.append([ad, fmt, dur, bfs, imps, views, view_rate, avg_cpv, cost, clicks,
                    round(100 * q25, 1), round(100 * q50, 1), round(100 * q75, 1), round(100 * q100, 1)])
    st[ad] = dict(fmt=fmt, imps=imps, views=views, cost=cost, clicks=clicks, q25=q25, q75=q75, q100=q100, bfs=bfs)

# weekly frequency
weeks = ["2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21"]
fq = [2.1, 2.6, 3.2, 3.9, 4.6, 5.4, 6.1, 6.9]
vrs = [0.29, 0.28, 0.26, 0.24, 0.21, 0.19, 0.16, 0.14]
freq_rows = []
for w, f, v in zip(weeks, fq, vrs):
    reach = int(rng.uniform(118000, 126000))
    freq_rows.append([w, reach, int(reach * f), f, round(100 * v, 1)])

# placements (channels)
PL = [("KidsToons Express", "yes", 0.09), ("Fun Cartoons for Kids", "yes", 0.08), ("Toy Unboxing Planet", "yes", 0.07),
      ("CycleTech Reviews", "no", 0.13), ("Global Mountain Bike Channel Fans", "no", 0.11), ("Urban Commuter Vlog", "no", 0.10),
      ("Fitness at Home", "no", 0.09), ("Weekend DIY", "no", 0.08), ("Outdoor Adventure TV", "no", 0.13), ("Daily News Clips", "no", 0.12)]
tot_imps = sum(v["imps"] for v in st.values()); tot_cost = sum(v["cost"] for v in st.values())
pl_rows = []
for ch, mfk, sh in PL:
    imps = int(tot_imps * sh * rng.uniform(0.97, 1.03))
    pl_rows.append([ch, mfk, imps, round(tot_cost * sh * rng.uniform(0.95, 1.05), 2)])

# ---------- ground truth ----------
TS, SU, CH = "Trail Story 45s", "Saddle Up 20s", "Commute Hack 30s"
skip = [a for a in ADS if ADS[a][0] == "skippable_instream"]
cpv = {a: st[a]["cost"] / st[a]["views"] for a in skip}
# share of impressions still playing when the brand first appears (quartile % is of impressions);
# brand inside the first quarter -> use the 25% figure (conservative); otherwise interpolate between quartiles
def brand_share(a):
    d = ADS[a][1]; f = st[a]["bfs"] / d
    pts = [(0.25, st[a]["q25"]), (0.5, ADS[a][7]), (0.75, st[a]["q75"]), (1.0, st[a]["q100"])]
    if f <= 0.25: return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= f <= x1: return y0 + (y1 - y0) * (f - x0) / (x1 - x0)
bshare = {a: brand_share(a) for a in skip}
cpb = {a: st[a]["cost"] / (st[a]["imps"] * bshare[a]) * 1000 for a in skip}   # cost per 1,000 brand-exposed impressions
c75 = {a: st[a]["cost"] / (st[a]["imps"] * st[a]["q75"]) for a in skip}
mfk_share = sum(r[2] for r in pl_rows if r[1] == "yes") / sum(r[2] for r in pl_rows)
ctr_all = sum(v["clicks"] for v in st.values()) / tot_imps
EXPO = dict(viewers=48200, viewer_conv=0.032, nonviewers=391000, nonviewer_conv=0.011)
ratio = EXPO["viewer_conv"] / EXPO["nonviewer_conv"]

assert cpv[TS] == min(cpv.values()) and cpb[TS] == max(cpb.values()) and cpb[SU] == min(cpb.values())
assert cpb[TS] > 1.7 * cpb[SU] and bshare[TS] < 0.1
assert fq[-1] > 3 * fq[0] and vrs[-1] < 0.55 * vrs[0]
assert 0.2 < mfk_share < 0.3 and 0.002 < ctr_all < 0.004

pc = lambda x, d=0: f"{100 * x:.{d}f}%"
eur = lambda x, d=2: f"€{x:,.{d}f}"

deck = f"""# Brightwell Bikes: YouTube September readout (agency draft for the CMO)

1. Hero creative: "Trail Story 45s" has our lowest cost per view ({eur(cpv[TS], 3)}). Plan: put 60% of October's video budget behind it.
2. YouTube works: people who watched our ads converted at {pc(EXPO['viewer_conv'], 1)} vs {pc(EXPO['nonviewer_conv'], 1)} for site visitors who did not ({ratio:.1f}x). Source: GA4 audience comparison, September ({EXPO['viewers']:,} viewers, {EXPO['nonviewers']:,} non-viewers).
3. Reach is growing steadily week on week.
"""

files = {
    "resources/agency_youtube_readout.md": deck,
    "resources/youtube_ads_sep2026.csv": to_csv(
        ["ad_name", "ad_format", "duration_sec", "brand_first_shown_sec", "impressions", "views", "view_rate", "avg_cpv", "cost", "clicks",
         "video_played_to_25_pct", "video_played_to_50_pct", "video_played_to_75_pct", "video_played_to_100_pct"], ad_rows),
    "resources/youtube_weekly_frequency.csv": to_csv(["week_start", "unique_users", "impressions", "avg_frequency", "view_rate_pct"], freq_rows),
    "resources/youtube_placements_sep2026.csv": to_csv(["channel", "made_for_kids", "impressions", "cost"], pl_rows),
}

prompt = """
I'm presenting our YouTube results to the CMO tomorrow. We're Brightwell Bikes (city and trail bikes). The agency's draft readout and the September Google Ads video exports are in resources/. Anything I'm missing? I need to say which creative we back in October and why, in report.md.
"""

N = 4; K = math.ceil(0.6 * N)
g_recall = f"""
The exports contain {N} planted problems. Answer key (computed from the files):

1. The cheapest-CPV ad hides the brand. "Trail Story 45s" has the lowest CPV ({eur(cpv[TS], 3)}) but only {pc(st[TS]['q25'])} of impressions play to 25%, and the brand first appears at second {st[TS]['bfs']} of 45, which only about {pc(bshare[TS], 1)} of impressions reach. Cost per 1,000 impressions that reached the brand moment: Trail Story {eur(cpb[TS])}, Saddle Up 20s {eur(cpb[SU])} (brand at second 2), Commute Hack 30s {eur(cpb[CH])}. Found if report.md points to the quartile drop-off together with the late brand reveal (or a retention/brand-exposure-adjusted cost) and says cheap CPV is the wrong yardstick.
2. Viewers vs non-viewers is not an ad effect. The {ratio:.1f}x comparison (viewers {pc(EXPO['viewer_conv'], 1)} vs non-viewers {pc(EXPO['nonviewer_conv'], 1)}) compares people the platform targeted (likely buyers) with people it did not; it needs a randomised holdout / lift test. Found if report.md rejects or caveats the 2.9x claim as selection / not causal and suggests a lift test or holdout.
3. Frequency wear-out. Weekly frequency rose from {fq[0]} to {fq[-1]} while view rate fell from {pc(vrs[0])} to {pc(vrs[-1])}, with unique users flat (so "reach is growing" is not true). Found if report.md flags rising frequency with falling view rate (or flat unique reach) and suggests a cap or creative refresh.
4. Made-for-kids placements. {pc(mfk_share)} of impressions ran on channels marked made_for_kids. Found if report.md flags these placements and suggests excluding them.

List which ones were found in your reasoning.
PASS if report.md identifies at least {K} of the {N} with the specific evidence.
FAIL if fewer than {K}.
"""

g_decision = f"""
Correct main recommendation: back "Saddle Up 20s" in October (brand in the first 2 seconds; lowest cost per 1,000 brand-exposed impressions, {eur(cpb[SU])} vs {eur(cpb[TS])} for Trail Story; best retention, {pc(st[SU]['q25'])} to 25% and {pc(st[SU]['q100'])} to 100%), not "Trail Story 45s". Re-cutting Trail Story so the brand and hook appear in the first 5 seconds is a fine secondary action.

Naive wrong answer: put 60% of the budget behind "Trail Story 45s" because it has the lowest cost per view ({eur(cpv[TS], 3)}).

PASS if report.md's main creative recommendation is "Saddle Up 20s" (alone or clearly as the lead creative) and it does not back Trail Story 45s as the hero in its current cut.
FAIL if it backs Trail Story 45s as the main creative, or names Commute Hack 30s or the bumpers as the lead creative. (Commute Hack as a clear second behind Saddle Up is fine.)
"""

g_decoy = f"""
Two patterns are normal and must not be presented as problems:
- D1. The bumper ads ("Spin Bumper A 6s", "Spin Bumper B 6s") have blank views, view rate and CPV. Bumpers are 6-second non-skippable ads bought on CPM; they do not record views.
- D2. Video CTR is about {pc(ctr_all, 2)} overall. Normal for video; clicks are not the job of a video ad.

PASS if report.md does not call the blank bumper views a tracking/data error and does not call the CTR weak or a reason to cut.
FAIL if either is presented as a problem to fix.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: cpv {', '.join(f'{a} {v:.3f}' for a, v in cpv.items())}; cpb {', '.join(f'{a} {v:.1f}' for a, v in cpb.items())} bshare {bshare[TS]:.3f}; mfk {mfk_share:.2f}; ctr {ctr_all:.4f}")
