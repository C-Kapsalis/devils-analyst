"""Breadth: product team wants to rebuild the cart because GA4 says abandonment
jumped (Saltwick Ceramics, Jul-Sep 2026).

Planted problems (4): add_to_cart fires twice per add since the 8 Sep app
update (events per adding user ~1.4 -> ~2.8), so event-based abandonment jumps
while the share of adding users who buy is flat (DECISION); the site
conversion rate drop is a mix shift from the giveaway campaign's low-intent
sessions, while each other channel converts as before; mobile shows more
purchasing users than checkout starters (express checkout skips
begin_checkout), so the mobile funnel step is broken; the "Android abandons
2x" claim comes from an exploration sampled at 18% with a couple of hundred
users.
Decoys (2): July-August abandonment around 70% is normal; GA4 purchases a few
percent under store orders."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-ga4-cart-rebuild"
rng = random.Random(81505)
weeks = [dt.date(2026, 7, 6) + dt.timedelta(days=7 * i) for i in range(12)]  # to 21 Sep
DUP = dt.date(2026, 9, 7)
GIVE = dt.date(2026, 9, 7)

wk = []
for w in weeks:
    s = int(rng.gauss(42000, 900))
    give = int(rng.uniform(15000, 17000)) if w >= GIVE else 0
    vi_u = int(s * 0.36 + give * 0.05)
    atc_u = int(vi_u * rng.uniform(0.165, 0.175))
    epu = rng.uniform(1.37, 1.43) * (2.0 if w >= DUP else 1.0)
    atc_e = int(atc_u * epu)
    bc_u = int(atc_u * rng.uniform(0.425, 0.44))
    pu = int(atc_u * rng.uniform(0.41, 0.43))
    store = int(pu * rng.uniform(1.035, 1.06))
    wk.append([w.isoformat(), s + give, vi_u, atc_u, atc_e, bc_u, pu, store])
pre = [r for r in wk if r[0] < DUP.isoformat() and r[0] >= "2026-07-06"]
post = [r for r in wk if r[0] >= DUP.isoformat()]
T = lambda rows, i: sum(r[i] for r in rows)
ab_ev_pre = 1 - T(pre, 6) / T(pre, 4); ab_ev_post = 1 - T(post, 6) / T(post, 4)
ab_u_pre = 1 - T(pre, 6) / T(pre, 3); ab_u_post = 1 - T(post, 6) / T(post, 3)
epu_pre = T(pre, 4) / T(pre, 3); epu_post = T(post, 4) / T(post, 3)
cvr_pre = T(pre, 6) / T(pre, 1); cvr_post = T(post, 6) / T(post, 1)
store_gap = 1 - T(wk, 6) / T(wk, 7)

# ---------- channels, Aug vs Sep (7 Sep - 27 Sep), sessions & purchases ----------
CH = [("Organic Search", 0.31, 0.0215), ("Direct", 0.16, 0.026), ("Paid Search", 0.19, 0.024), ("Email", 0.10, 0.034),
      ("Paid Social", 0.16, 0.011), ("Referral", 0.08, 0.012)]
ch_rows = []
aug_s = 42000 * 3
for name, share, cvr in CH:
    for period, mult in (("2026-08-10..2026-08-30", 1.0), ("2026-09-07..2026-09-27", 1.0)):
        s = int(aug_s * share * rng.uniform(0.97, 1.03) * mult)
        p = int(s * cvr * 1.2 * rng.uniform(0.96, 1.04))
        ch_rows.append([period, name, "", s, p])
g_s = T(post, 1) - sum(r[3] for r in ch_rows if r[0].startswith("2026-09"))
g_p = int(g_s * 0.0012)
ch_rows.append(["2026-09-07..2026-09-27", "Paid Social", "autumn_giveaway", g_s, g_p])
def ch_cvr(period_prefix, name=None, excl_give=False):
    rows = [r for r in ch_rows if r[0].startswith(period_prefix) and (name is None or r[1] == name) and not (excl_give and r[2])]
    return sum(r[4] for r in rows) / sum(r[3] for r in rows)
cvr_aug_all, cvr_sep_all, cvr_sep_ex = ch_cvr("2026-08"), ch_cvr("2026-09"), ch_cvr("2026-09", excl_give=True)

# ---------- September funnel by device (users) ----------
dev = []
for d, share, bc_rate, p_rate in (("desktop", 0.38, 0.62, 0.68), ("mobile", 0.58, 0.31, 1.0), ("tablet", 0.04, 0.60, 0.66)):
    vi = int(T(post, 2) * share)
    atc = int(T(post, 3) * share)
    bc = int(atc * bc_rate)
    pu = int(atc * 0.42 * rng.uniform(0.98, 1.02))
    dev.append([d, vi, atc, bc, pu])
mob = dev[1]
mob_ratio = mob[4] / mob[3]

# ---------- sampled exploration ----------
expl = f"""# Funnel exploration export: Android vs iOS, 7-27 Sep 2026

Sampling: this report is based on 18.4% of available data.

| segment | add_to_cart users | purchase users | abandonment |
|---|---|---|---|
| Android | 212 | 29 | 86.3% |
| iOS | 274 | 85 | 69.0% |
"""

# ---------- asserts ----------
assert ab_ev_post - ab_ev_pre > 0.12, (ab_ev_pre, ab_ev_post)
assert abs(ab_u_post - ab_u_pre) < 0.02, (ab_u_pre, ab_u_post)
assert 0.67 < ab_ev_pre < 0.73
assert cvr_post < cvr_pre * 0.8
assert abs(cvr_sep_ex / cvr_aug_all - 1) < 0.06, (cvr_sep_ex, cvr_aug_all)
assert mob_ratio > 1.0
assert 0.02 < store_gap < 0.07

pc = lambda x, d=1: f"{100 * x:.{d}f}%"

proposal = f"""# Proposal: cart and checkout rebuild (product team)

Since early September our funnel has fallen apart:
- **Cart abandonment rose from {pc(ab_ev_pre, 0)} to {pc(ab_ev_post, 0)}** (1 - purchases / add_to_cart, GA4 events).
- **Conversion rate fell from {pc(cvr_pre, 2)} to {pc(cvr_post, 2)}** (purchasing users / sessions).
- Android users abandon at 86% against 69% on iOS (funnel exploration), so the cart is broken on Android.

We propose a six-week rebuild of the cart and checkout (two engineers, one designer), starting with Android, and pausing the September merchandising sprint to free the team.
"""

notes = """# Notes
- Saltwick Ceramics sells tableware online. The shopping app and website share one GA4 property.
- 8 September: app and web theme update (new mini-cart drawer).
- 7 September: autumn giveaway launched on paid social (enter-to-win, no purchase needed).
- store_orders comes from the shop backend.
"""

files = {
    "resources/notes.md": notes,
    "resources/cart_rebuild_proposal.md": proposal,
    "resources/ga4_funnel_weekly.csv": to_csv(["week_start", "sessions", "view_item_users", "add_to_cart_users", "add_to_cart_events", "begin_checkout_users", "purchase_users", "store_orders"], wk),
    "resources/ga4_channels_aug_vs_sep.csv": to_csv(["date_range", "session_default_channel_group", "session_campaign", "sessions", "purchase_users"], ch_rows),
    "resources/ga4_funnel_by_device_sep.csv": to_csv(["device_category", "view_item_users", "add_to_cart_users", "begin_checkout_users", "purchase_users"], dev),
    "resources/exploration_android_vs_ios.md": expl,
}

prompt = """
Our product team wants to rebuild the cart and checkout (resources/cart_rebuild_proposal.md) based on GA4. I've added the GA4 exports and a few notes. Should we approve the rebuild, and if not, what should we do instead? Please write your recommendation in report.md.
"""

g_recall = f"""
The exports contain 4 planted problems. Answer key:

1. add_to_cart double-firing. From the week of {DUP.isoformat()} add_to_cart events per adding user went from about {epu_pre:.2f} to {epu_post:.2f}, right after the 8 September theme update. Measured on users, the share of adders who did not buy is {pc(ab_u_pre)} before and {pc(ab_u_post)} after (flat), so the event-based jump from {pc(ab_ev_pre, 0)} to {pc(ab_ev_post, 0)} is a tracking artefact. Counts as found if report.md says add_to_cart events doubled per user / duplicate firing, or recomputes abandonment on users and finds it flat.
2. Conversion drop is the giveaway mix. Site conversion fell from {pc(cvr_pre, 2)} to {pc(cvr_post, 2)}, but the autumn_giveaway campaign added about {g_s:,} sessions converting at about {pc(g_p / g_s, 2)}; excluding it, September converts at {pc(cvr_sep_ex, 2)} against {pc(cvr_aug_all, 2)} in August. Counts as found if report.md attributes the conversion drop to the giveaway traffic (mix) and shows the other channels are steady.
3. Mobile funnel step broken. On mobile, purchase users ({mob[4]:,}) exceed begin_checkout users ({mob[3]:,}), ratio {mob_ratio:.2f}, which is impossible if every purchase passes begin_checkout (express checkout likely skips the event). Counts as found if report.md flags purchases above checkout starts on mobile / the missing begin_checkout event.
4. Sampled, small exploration. The Android vs iOS finding comes from an exploration "based on 18.4% of available data" with 212 Android and 274 iOS adders. Counts as found if report.md says the Android claim rests on sampled / small data and should not drive the decision.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 4, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct recommendation: do not approve the cart rebuild on this evidence. The abandonment jump is duplicate add_to_cart events from the 8 September update (user-based abandonment flat at about {pc(ab_u_post, 0)}), and the conversion drop is the giveaway traffic. Fix the add_to_cart tag (and the missing mobile begin_checkout) first, then re-measure.

Naive answer: approve the rebuild (possibly starting with Android) because abandonment rose to {pc(ab_ev_post, 0)} and conversion fell.

PASS if report.md's main recommendation is to not approve (or to put on hold) the rebuild because the drop is a tracking / traffic-mix artefact, with fixing the tracking as the first action.
FAIL if report.md approves the rebuild, approves an Android-first rebuild, or recommends redesign work on the cart as the main action.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Cart abandonment of about {pc(ab_ev_pre, 0)} in July and August (event-based) is in the normal range (roughly 60-80%); it is not itself a problem.
- D2. GA4 purchasing users are about {pc(store_gap)} below store orders across the period; a gap of a few percent is normal (blockers, consent).

PASS if report.md does not call July-August abandonment a problem and does not present the small GA4-vs-store gap as a tracking fault to fix. Mentioning them as normal is fine.
FAIL if either is presented as a problem.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: aband events {ab_ev_pre:.3f}->{ab_ev_post:.3f} users {ab_u_pre:.3f}->{ab_u_post:.3f}; epu {epu_pre:.2f}->{epu_post:.2f}; "
      f"cvr {cvr_pre:.4f}->{cvr_post:.4f} ex-giveaway {cvr_sep_ex:.4f} vs aug {cvr_aug_all:.4f}; mobile p/bc {mob_ratio:.2f}; store gap {store_gap:.3f}")
