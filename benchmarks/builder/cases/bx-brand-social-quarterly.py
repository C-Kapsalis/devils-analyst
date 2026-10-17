"""Organic social Q3 review (Fernhill Tea Co.) going to the CMO, with a proposal
to move the Instagram content budget to TikTok.

Planted subtle problems (5):
  P1 TikTok engagement rate is per VIEW (export column) but compared with the
     follower-based industry median (1.73%); per follower it is far lower.
  P2 Instagram "engagements" column = likes only (comments, shares, saves are
     separate columns), so Instagram ER is understated and ranked below median.
  P3 One TikTok giveaway video ("follow + comment to win") carries a large
     share of TikTok engagements and of Q3 follows; follows are then given back
     as unfollows after the draw. Without it TikTok sits below its median.
  P4 Brand mentions +38% QoQ called "buzz growing", but competitors grew faster:
     share of voice fell.
  P5 "Instagram reached 465K people" is the sum of per-post reach; the
     account-level unique reach for the quarter is a fraction of that.
Decision: keep the Instagram budget (Instagram beats its median like-for-like
and drives the site sessions and purchases); do not move it to TikTok.
Decoys: Instagram August reach dip (posting pause, reach per post steady);
GA4 social sessions slightly below platform link clicks."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "bx-brand-social-quarterly"
rng = random.Random(46021)
Q_START = dt.date(2026, 7, 1)
DAYS = 92
dates = [Q_START + dt.timedelta(days=i) for i in range(DAYS)]
TT_MEDIAN, IG_MEDIAN = 1.73, 0.36
GIVEAWAY_DAY = dt.date(2026, 8, 14)
DRAW_DAY = dt.date(2026, 8, 28)

# ---------------- account daily followers ----------------
acc_rows = []
ig_f, tt_f = 61800, 27900
ig_fol, tt_fol = {}, {}
tt_follows_total = tt_unf_total = 0
tt_giveaway_follows = tt_post_draw_extra_unf = 0
ig_follows_total = ig_unf_total = 0
for d in dates:
    f = rng.randint(38, 58); u = rng.randint(16, 30)
    ig_follows_total += f; ig_unf_total += u
    ig_f += f - u; ig_fol[d] = ig_f
    acc_rows.append([d.isoformat(), "instagram", ig_f, f, u])
    f = rng.randint(22, 40); u = rng.randint(12, 24)
    k = (d - GIVEAWAY_DAY).days
    if 0 <= k <= 3:
        extra = [2100, 1600, 900, 400][k]
        f += extra; tt_giveaway_follows += extra
    k2 = (d - DRAW_DAY).days
    if 0 <= k2 <= 13:
        extra = int(330 * math.exp(-k2 / 5))
        u += extra; tt_post_draw_extra_unf += extra
    tt_follows_total += f; tt_unf_total += u
    tt_f += f - u; tt_fol[d] = tt_f
    acc_rows.append([d.isoformat(), "tiktok", tt_f, f, u])

tt_start = 27900; tt_end = tt_fol[dates[-1]]
tt_net = tt_end - tt_start
tt_net_ex = tt_net - tt_giveaway_follows + tt_post_draw_extra_unf
ig_net = ig_fol[dates[-1]] - 61800

# ---------------- Instagram posts ----------------
ig_posts = []
month_counts = {7: 15, 8: 10, 9: 15}
for m, n in month_counts.items():
    days_m = sorted(rng.sample([d for d in dates if d.month == m], n))
    for j, d in enumerate(days_m):
        mt = ["reel", "carousel", "image", "reel", "carousel"][j % 5]
        reach = int(rng.gauss({"reel": 13200, "carousel": 11000, "image": 9400}[mt], 900))
        impr = int(reach * rng.uniform(1.25, 1.5))
        fol = ig_fol[d]
        likes = int(fol * rng.uniform(0.0025, 0.0036))
        comments = int(likes * rng.uniform(0.09, 0.15))
        shares = int(likes * rng.uniform(0.17, 0.27))
        saves = int(likes * rng.uniform(0.32, 0.48)) + (int(likes * 0.15) if mt == "carousel" else 0)
        eng = likes  # export "engagements" = likes only (planted)
        er = round(100 * eng / fol, 2)
        ig_posts.append([d, mt, fol, reach, impr, likes, comments, shares, saves, eng, er])
ig_posts.sort(key=lambda r: r[0])
ig_rows = [[f"IG{18400 + i}", r[0].isoformat(), *r[1:]] for i, r in enumerate(ig_posts)]

ig_likes = sum(r[5] for r in ig_posts)
ig_full = sum(r[5] + r[6] + r[7] + r[8] for r in ig_posts)
ig_fsum = sum(r[2] for r in ig_posts)
ig_er_deck = 100 * ig_likes / ig_fsum
ig_er_true = 100 * ig_full / ig_fsum
ig_reach_sum = sum(r[3] for r in ig_posts)
ig_reach_month = {m: sum(r[3] for r in ig_posts if r[0].month == m) for m in (7, 8, 9)}
ig_rpp = {m: ig_reach_month[m] / month_counts[m] for m in (7, 8, 9)}

# ---------------- TikTok videos ----------------
tt_posts = []
tt_days = sorted(rng.sample([d for d in dates if d != GIVEAWAY_DAY], 35))
for d in tt_days:
    views = int(rng.gauss(8000, 1600))
    fol = tt_fol[d]
    likes = int(views * rng.uniform(0.038, 0.049))
    comments = int(likes * rng.uniform(0.04, 0.08))
    shares = int(likes * rng.uniform(0.05, 0.09))
    saves = int(likes * rng.uniform(0.05, 0.09))
    tt_posts.append([d, "standard", fol, views, int(views * rng.uniform(0.82, 0.9)), likes, comments, shares, saves])
tt_posts.append([GIVEAWAY_DAY, "giveaway", tt_fol[GIVEAWAY_DAY], 41800, 38300, 2240, 4870, 610, 95])
tt_posts.sort(key=lambda r: r[0])
tt_rows = []
for i, r in enumerate(tt_posts):
    eng = r[5] + r[6] + r[7] + r[8]
    caption = "Win a year of tea! Follow + comment and tag 3 friends. Winner drawn 28 Aug" if r[1] == "giveaway" else rng.choice(
        ["Cold brew in 60 seconds", "Which blend are you?", "Behind the blend: Assam harvest", "Tea myths, busted",
         "3 iced tea recipes", "Packing orders with us", "Steep time test", "Rate my tea shelf"])
    tt_rows.append([f"TT{7720 + i}", r[0].isoformat(), caption, r[2], r[3], r[4], r[5], r[6], r[7], r[8], eng, round(100 * eng / r[3], 2)])

tt_eng = sum(r[10] for r in tt_rows)
tt_views = sum(r[4] for r in tt_rows)
tt_fsum = sum(r[3] for r in tt_rows)
gv = [r for r in tt_rows if r[2].startswith("Win")][0]
tt_er_deck = 100 * tt_eng / tt_views
tt_er_fol_all = 100 * tt_eng / tt_fsum
tt_er_fol_ex = 100 * (tt_eng - gv[10]) / (tt_fsum - gv[3])
gv_share_eng = gv[10] / tt_eng
gv_share_follows = tt_giveaway_follows / tt_follows_total

# ---------------- account summary (reach, link clicks) ----------------
ig_unique_q = int(ig_reach_sum * 0.215)
summ_rows = []
ig_clicks = {7: 3480, 8: 2560, 9: 3610}
tt_clicks = {7: 760, 8: 905, 9: 690}
for m in (7, 8, 9):
    summ_rows.append(["instagram", "month", f"2026-{m:02d}", int(ig_reach_month[m] * 0.36), sum(r[4] for r in ig_posts if r[0].month == m), ig_clicks[m]])
for m in (7, 8, 9):
    v = sum(r[4] for r in tt_rows if r[1][5:7] == f"{m:02d}")
    summ_rows.append(["tiktok", "month", f"2026-{m:02d}", int(v * 0.55), v, tt_clicks[m]])
summ_rows.append(["instagram", "quarter", "2026-Q3", ig_unique_q, sum(r[4] for r in ig_posts), sum(ig_clicks.values())])
summ_rows.append(["tiktok", "quarter", "2026-Q3", int(tt_views * 0.42), tt_views, sum(tt_clicks.values())])

# ---------------- GA4 sessions ----------------
ga_rows = []
ses = {}
for m in (7, 8, 9):
    s_ig = int(ig_clicks[m] * rng.uniform(0.87, 0.93)); s_tt = int(tt_clicks[m] * rng.uniform(0.86, 0.92))
    p_ig = int(s_ig * rng.uniform(0.019, 0.023)); p_tt = int(s_tt * rng.uniform(0.008, 0.011))
    ses[m] = (s_ig, s_tt, p_ig, p_tt)
    ga_rows.append([f"2026-{m:02d}", "instagram.com / social", s_ig, p_ig, round(p_ig * rng.uniform(31, 36), 2)])
    ga_rows.append([f"2026-{m:02d}", "tiktok.com / social", s_tt, p_tt, round(p_tt * rng.uniform(26, 31), 2)])
ig_purch = sum(v[2] for v in ses.values()); tt_purch = sum(v[3] for v in ses.values())
ig_sessions = sum(v[0] for v in ses.values()); tt_sessions = sum(v[1] for v in ses.values())
ig_rev = sum(r[4] for r in ga_rows if r[1].startswith("insta")); tt_rev = sum(r[4] for r in ga_rows if r[1].startswith("tik"))
click_ratio = [ses[m][0] / ig_clicks[m] for m in (7, 8, 9)]

# ---------------- listening ----------------
BR = {"Fernhill Tea Co.": (1180, 1.38), "Copperleaf": (1650, 1.62), "Mistral Teas": (1420, 1.71), "Old Quay Tea": (1050, 1.55)}
lis_rows = []
mq = {}
for b, (base, g) in BR.items():
    for m in (4, 5, 6, 7, 8, 9):
        v = int(base * (g if m >= 7 else 1.0) * rng.uniform(0.94, 1.06))
        mq[(b, m >= 7)] = mq.get((b, m >= 7), 0) + v
        lis_rows.append([f"2026-{m:02d}", b, v])
own_q2, own_q3 = mq[("Fernhill Tea Co.", False)], mq[("Fernhill Tea Co.", True)]
tot_q2 = sum(v for (b, q3), v in mq.items() if not q3); tot_q3 = sum(v for (b, q3), v in mq.items() if q3)
own_growth = own_q3 / own_q2 - 1
sov_q2, sov_q3 = own_q2 / tot_q2, own_q3 / tot_q3

# ---------------- asserts ----------------
assert tt_er_deck > 2.5 * TT_MEDIAN, tt_er_deck
assert tt_er_fol_all > TT_MEDIAN > tt_er_fol_ex, (tt_er_fol_all, tt_er_fol_ex)
assert ig_er_deck < IG_MEDIAN < ig_er_true and ig_er_true / IG_MEDIAN > 1.3, (ig_er_deck, ig_er_true)
assert gv_share_eng > 0.25 and gv_share_follows > 0.4, (gv_share_eng, gv_share_follows)
assert tt_net_ex < 0.35 * tt_net, (tt_net, tt_net_ex)
assert 0.33 < own_growth < 0.43 and sov_q3 < sov_q2 - 0.01, (own_growth, sov_q2, sov_q3)
assert ig_reach_sum > 4 * ig_unique_q
assert ig_reach_month[8] < 0.8 * ig_reach_month[7] and abs(ig_rpp[8] / ig_rpp[7] - 1) < 0.12, ig_rpp
assert all(0.85 < c < 0.95 for c in click_ratio)
assert ig_purch > 4 * tt_purch and ig_rev > 4 * tt_rev

pc = lambda x, d=1: f"{100 * x:.{d}f}%"
k = lambda x: f"{x:,.0f}"

deck = f"""# Fernhill Tea Co. — Organic social, Q3 2026 (draft for CMO)

## Headlines
- **TikTok is our standout channel.** Engagement rate {tt_er_deck:.1f}% against an industry median of {TT_MEDIAN}% for TikTok ({tt_er_deck / TT_MEDIAN:.1f}x the benchmark).
- **Instagram is underperforming.** Engagement rate {ig_er_deck:.2f}%, below the Instagram median of {IG_MEDIAN}%.
- **TikTok audience growing fast:** +{k(tt_net)} followers in Q3 (+{pc(tt_net / tt_start)}), versus +{k(ig_net)} on Instagram (+{pc(ig_net / 61800)}). Our content is landing.
- **Instagram reached {k(ig_reach_sum)} people in Q3** 
- **Buzz is growing:** brand mentions +{pc(own_growth, 0)} quarter on quarter (social listening, all public mentions incl. untagged).
- Instagram reach dipped in August ({k(ig_reach_month[8])} vs {k(ig_reach_month[7])} in July): we posted 10 times instead of 15 during the summer break. Reach per post held ({k(ig_rpp[7])} July, {k(ig_rpp[8])} August).

Benchmarks: RivalIQ 2024 median engagement rate by platform (TikTok {TT_MEDIAN}%, Instagram {IG_MEDIAN}%).
Engagement rate as reported in each platform's export (engagement_rate column), totals = total engagements / total base.

## Recommendation
Move the Instagram content budget (EUR 18,000 per quarter, incl. the freelance photographer) to TikTok from Q4 and drop Instagram to reposting TikTok videos as Reels.

## Sources (resources/)
- instagram_posts_q3.csv, tiktok_videos_q3.csv: post-level exports
- account_followers_q3.csv: daily followers, follows, unfollows
- account_summary_q3.csv: platform reach, impressions/views and link clicks by month and quarter
- ga4_social_sessions_q3.csv: GA4 sessions, purchases and revenue from social
- social_listening_mentions.csv: monthly mentions, own brand and three competitors
"""

files = {
    "resources/q3_social_review.md": deck,
    "resources/instagram_posts_q3.csv": to_csv(["post_id", "date", "media_type", "followers", "reach", "impressions", "likes", "comments", "shares", "saves", "engagements", "engagement_rate"], ig_rows),
    "resources/tiktok_videos_q3.csv": to_csv(["video_id", "date", "caption", "followers", "views", "reach", "likes", "comments", "shares", "saves", "engagements", "engagement_rate"], tt_rows),
    "resources/account_followers_q3.csv": to_csv(["date", "platform", "followers", "follows", "unfollows"], acc_rows),
    "resources/account_summary_q3.csv": to_csv(["platform", "report_level", "period", "reach", "impressions_or_views", "link_clicks"], summ_rows),
    "resources/ga4_social_sessions_q3.csv": to_csv(["month", "session_source_medium", "sessions", "purchases", "purchase_revenue"], ga_rows),
    "resources/social_listening_mentions.csv": to_csv(["month", "brand", "mentions"], lis_rows),
}

prompt = """
I'm presenting our Q3 organic social review to the CMO tomorrow. The draft is resources/q3_social_review.md and the platform exports behind it are in resources/. The big ask in it is moving the Instagram content budget to TikTok for Q4. Anything I'm missing, and is that the right call? Write it up in report.md.
"""

g_recall = f"""
The draft deck (q3_social_review.md) has 5 planted problems. Answer key (numbers computed from the exports):

1. TikTok engagement rate on the wrong base for the benchmark. The deck's TikTok {tt_er_deck:.1f}% is engagements / VIEWS (the export's engagement_rate column), compared with a follower-based median of {TT_MEDIAN}%. Per follower (total engagements / summed followers across videos) TikTok is {tt_er_fol_all:.2f}%, and {tt_er_fol_ex:.2f}% without the giveaway video. Found if report.md says the TikTok rate is per view (or reach) and not comparable to the follower-based benchmark, or recomputes it per follower (about {tt_er_fol_all:.1f}% or {tt_er_fol_ex:.1f}%).
2. Instagram "engagements" are likes only. In instagram_posts_q3.csv the engagements column equals likes; comments, shares and saves are separate. With all four, Instagram ER per follower is {ig_er_true:.2f}% (deck: {ig_er_deck:.2f}%), above the {IG_MEDIAN}% median. Found if report.md notes the likes-only definition (or the definitions differ between platforms) and/or gives a corrected Instagram rate around {ig_er_true:.2f}%.
3. Giveaway inflating TikTok. The video "Win a year of tea! Follow + comment..." ({gv[1]}) has {k(gv[10])} engagements ({pc(gv_share_eng, 0)} of all TikTok engagements in Q3, mostly comments: {k(gv[7])}). The giveaway days brought about {k(tt_giveaway_follows)} extra follows ({pc(gv_share_follows, 0)} of Q3 TikTok follows), and unfollows rose after the 28 Aug draw (about {k(tt_post_draw_extra_unf)} extra). Net TikTok growth without the giveaway is about {k(tt_net_ex)} of the reported {k(tt_net)}. Found if report.md identifies the giveaway video/period as inflating engagement and/or follower growth (any of these numbers, or a clear description with the date).
4. Share of voice fell. Own mentions +{pc(own_growth, 0)} QoQ, but all four brands' mentions grew {pc(tot_q3 / tot_q2 - 1, 0)}; Fernhill's share of voice went from {pc(sov_q2)} to {pc(sov_q3)}. Found if report.md says competitors grew faster / share of voice fell (any SOV figures near these, or the competitor growth).
5. Reach summed across posts. "Instagram reached {k(ig_reach_sum)} people" is the sum of per-post reach ({k(ig_reach_sum)}); account_summary_q3.csv gives quarterly account reach of {k(ig_unique_q)}. Found if report.md says post reach cannot be summed into people reached and/or quotes the ~{ig_unique_q / 1000:.0f}K quarterly figure.

List which ones were found in your reasoning, each with its evidence.
PASS if at least 3 of the 5 are identified with evidence (a number, a column, a post, or a specific quote). A vague "check the benchmarks" does not count.
FAIL if 2 or fewer are identified.
"""

g_decision = f"""
The deck recommends moving the Instagram content budget (EUR 18,000/quarter) to TikTok.

Correct call: do NOT move the Instagram budget to TikTok on this evidence (keep Instagram funded; at most run TikTok as a test or a smaller reallocation). Reasons from the data: like-for-like (all engagement types, per follower) Instagram is {ig_er_true:.2f}% vs its {IG_MEDIAN}% median, while TikTok is {tt_er_fol_ex:.2f}% per follower without the giveaway, below its {TT_MEDIAN}% median; and Instagram drove {k(ig_sessions)} GA4 sessions and {ig_purch} purchases (EUR {k(ig_rev)}) in Q3 vs TikTok's {k(tt_sessions)} sessions and {tt_purch} purchases (EUR {k(tt_rev)}).

Naive wrong answer: endorse the move because "TikTok {tt_er_deck:.1f}% is {tt_er_deck / TT_MEDIAN:.1f}x its benchmark and Instagram is below its median", or because TikTok followers grew +{pc(tt_net / tt_start)}.

PASS if report.md's main recommendation is not to move the Instagram budget to TikTok (keep or protect Instagram; test TikTok separately or with a small share), for reasons tied to the corrected comparison and/or the sessions/purchases.
FAIL if report.md endorses moving the Instagram budget to TikTok (fully or mostly), or gives no clear recommendation on it.
"""

g_decoy = f"""
Two things in the materials look like problems but are fine:
- D1. Instagram reach dipped in August ({k(ig_reach_month[8])} vs {k(ig_reach_month[7])} in July). It is explained by 10 posts instead of 15; reach per post held ({k(ig_rpp[7])} July vs {k(ig_rpp[8])} August). The deck says so correctly.
- D2. GA4 sessions from social are slightly below the platforms' link clicks (Instagram sessions are {pc(min(click_ratio), 0)} to {pc(max(click_ratio), 0)} of link clicks each month). A 5-15% gap between clicks and sessions is normal (bounces before the tag fires, consent, bots).

PASS if report.md does not present D1 as a performance decline or audience problem and does not present D2 as broken tracking or lost traffic. Mentioning either as fine or normal is a PASS.
FAIL if report.md says the August dip shows Instagram declining/losing audience, or says the clicks-to-sessions gap means tracking is broken or traffic is being lost.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: TT ER deck {tt_er_deck:.2f} fol {tt_er_fol_all:.2f} ex-giveaway {tt_er_fol_ex:.2f}; IG ER deck {ig_er_deck:.3f} true {ig_er_true:.3f}; "
      f"TT net {tt_net} ex {tt_net_ex}; SOV {sov_q2:.3f}->{sov_q3:.3f}; IG reach sum {ig_reach_sum} vs unique {ig_unique_q}; purch IG {ig_purch} TT {tt_purch}")
