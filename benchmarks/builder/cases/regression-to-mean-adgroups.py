"""Regression to the mean: the 10 worst-CPA ad groups in one week were picked
for an ad rewrite. Their CPA 'improves' ~35-50% afterwards, but equally bad
untouched ad groups improve just as much; true effect is zero."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
import datetime as dt

NAME = "regression-to-mean-adgroups"
rng = random.Random(16)
N_AG = 60
WEEKS = [dt.date(2026, 7, 6) + dt.timedelta(weeks=i) for i in range(11)]
WEEK_N = WEEKS[6]                      # 2026-08-17: the week the worst 10 were picked from
CHANGE_DATE = WEEKS[7]               # Mon 2026-08-24
POST = WEEKS[7:]                       # 4 weeks from the change

def poisson(lam):
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1

campaigns = ["Search - Coffee Beans", "Search - Equipment", "Search - Subscriptions", "Search - Gifts"]
themes = ["espresso", "decaf", "single origin", "dark roast", "organic", "colombian", "ethiopian", "cold brew",
          "pour over", "french press", "grinder", "moka pot", "kettle", "filters", "gift box", "subscription",
          "monthly box", "office coffee", "beans bulk", "mild roast"]
ags = []
for i in range(N_AG):
    camp = campaigns[i % 4]
    name = f"{themes[i % 20]} {['exact', 'phrase', 'broad'][i // 20]}"
    cpc = rng.uniform(0.6, 1.4)
    true_cpa = rng.uniform(26, 42)
    cvr = cpc / true_cpa
    weekly_clicks = rng.uniform(2.5, 6.0) / cvr     # expected 2.2-5.5 conversions/week
    ags.append(dict(campaign=camp, ad_group=name, cpc=cpc, cvr=cvr, clicks=weekly_clicks, ctr=rng.uniform(0.04, 0.09)))

rows = []
for w in WEEKS:
    for a in ags:
        clicks = max(1, int(rng.gauss(a["clicks"], a["clicks"] * 0.08)))
        conv = sum(1 for _ in range(clicks) if rng.random() < a["cvr"])
        cost = round(clicks * a["cpc"] * rng.uniform(0.93, 1.07), 2)
        rows.append([w.isoformat(), a["campaign"], a["ad_group"], int(clicks / a["ctr"]), clicks, cost, conv])
csv_text = to_csv(["week_start", "campaign", "ad_group", "impressions", "clicks", "cost", "conversions"], rows)

def cpa_of(ag, weeks):
    rs = [r for r in rows if r[2] == ag and r[0] in {w.isoformat() for w in weeks}]
    c, v = sum(r[5] for r in rs), sum(r[6] for r in rs)
    return c, v

wk = WEEK_N.isoformat()
weekN = {r[2]: (r[5], r[6]) for r in rows if r[0] == wk}
rank = sorted(weekN, key=lambda g: -(weekN[g][0] / weekN[g][1]) if weekN[g][1] else 1e9)
treated = rank[:10]
control = rank[10:20]          # next 10 worst, untouched
others = rank[10:]
# placebo: the 10 worst untouched ad groups in the week BEFORE week N, followed for the next 4 weeks
WEEK_P = WEEKS[5]
wkp = WEEK_P.isoformat()
weekP = {r[2]: (r[5], r[6]) for r in rows if r[0] == wkp}
rank_p = sorted([g for g in weekP if g not in treated], key=lambda g: -(weekP[g][0] / weekP[g][1]) if weekP[g][1] else 1e9)
placebo = rank_p[:10]
PLACEBO_POST = WEEKS[6:10]
changes_csv = to_csv(["change_date", "campaign", "ad_group", "change_type", "note"],
                     [[CHANGE_DATE.isoformat(), next(a["campaign"] for a in ags if a["ad_group"] == g), g,
                       "responsive_search_ad_rewrite", "New headlines and descriptions; old RSA paused"] for g in treated])

def group_cpa(groups, weeks):
    c = v = 0
    for g in groups:
        cc, vv = cpa_of(g, weeks); c += cc; v += vv
    return c / v
PRE = [w for w in WEEKS if w < WEEK_N]
t_N, t_post, t_pre = group_cpa(treated, [WEEK_N]), group_cpa(treated, POST), group_cpa(treated, PRE)
c_N, c_post, c_pre = group_cpa(control, [WEEK_N]), group_cpa(control, POST), group_cpa(control, PRE)
o_N, o_post = group_cpa(others, [WEEK_N]), group_cpa(others, POST)
t_imp = 1 - t_post / t_N
c_imp = 1 - c_post / c_N
p_W, p_post = group_cpa(placebo, [WEEK_P]), group_cpa(placebo, PLACEBO_POST)
p_imp = 1 - p_post / p_W
did = t_imp - p_imp
did_c = t_imp - c_imp
t_vs_pre = t_post / t_pre - 1
naive_conv_N = sum(weekN[g][1] for g in treated)

assert t_imp > 0.30, t_imp
assert c_imp > 0.15, c_imp
assert abs(did) < 0.08, did
assert abs(t_vs_pre) < 0.07, t_vs_pre
pc = lambda x: f"{100 * x:.0f}%"
f = lambda x: f"{x:,.2f}"
post_lbl = f"{POST[0].isoformat()} to {POST[-1].isoformat()} ({len(POST)} weeks)"

prompt = f"""
On {CHANGE_DATE.strftime('%-d %B %Y')} we rewrote the ads in our 10 worst ad groups (they had the highest CPA in the week of {WEEK_N.strftime('%-d %B')}). The weekly ad group report is in resources/adgroup_weekly.csv and the list of what we changed is in resources/changes.csv. How much did the rewrite improve performance? Write report.md with the improvement in CPA and whether we should roll the same rewrite out to the rest of the account.
"""

g_effect = f"""
The 10 rewritten ad groups were selected because they had the worst CPA in the week of {wk}, a single week with only 2–6 conversions per ad group, so that week was mostly bad luck.
Ground truth:
- Rewritten ad groups: CPA {f(t_N)} in week {wk} -> {f(t_post)} after the change ({post_lbl}): {pc(t_imp)} "improvement". This is the naive answer.
- Their CPA in the 6 weeks BEFORE week {wk} was {f(t_pre)}, i.e. after the rewrite they are simply back to their normal level ({t_vs_pre:+.0%} vs that earlier baseline).
- Placebo with the same selection rule: the 10 worst-CPA untouched ad groups in the week of {wkp} (not rewritten) went from CPA {f(p_W)} to {f(p_post)} over the following 4 weeks, a {pc(p_imp)} improvement with no change at all. Difference-in-differences vs the rewritten group: {did * 100:+.0f} percentage points, i.e. about zero.
- The next 10 worst in week {wk} (ranks 11–20, not rewritten, slightly less extreme): CPA {f(c_N)} -> {f(c_post)}, {pc(c_imp)} improvement with no change. (A residual gap of ~{did_c * 100:.0f} points vs this group is expected because they were less extreme in the selection week, not evidence of an effect.)

PASS if report.md concludes the rewrite had little or no measurable effect (or that the improvement cannot be attributed to the rewrite) because comparable untouched ad groups improved about as much and/or the rewritten ad groups were just returning to their earlier CPA (regression to the mean / selection on a bad week).
FAIL if it credits the rewrite with a ~{pc(t_imp)} (or any substantial) CPA improvement, e.g. "the rewrite cut CPA by {pc(t_imp)}".
"""
g_rollout = f"""
Untouched ad groups selected the same way improved {pc(p_imp)} versus {pc(t_imp)} for the rewritten ones (net {did * 100:+.0f} points), and the rewritten ad groups' CPA after the change ({f(t_post)}) equals their CPA before the bad week ({f(t_pre)}), so there is no evidence the rewrite works.

PASS if report.md does NOT recommend rolling the rewrite out across the account on the basis of this result; acceptable recommendations include: don't roll out, or run a proper test (randomly assign ad groups / ad variations experiment / compare against a control) before rolling out.
FAIL if it recommends rolling the rewrite out to the rest of the account because CPA improved.
"""
g_comparison = f"""
A valid evaluation needs a comparison group or baseline beyond the selection week. Numbers for reference: rewritten ad groups CPA before selection week {f(t_pre)}, selection week {f(t_N)}, after {f(t_post)}; same-rule placebo (worst untouched in week {wkp}) {f(p_W)} -> {f(p_post)}; untouched ranks 11–20 {f(c_N)} -> {f(c_post)}; all 50 untouched ad groups {f(o_N)} -> {f(o_post)}.

PASS if report.md compares the rewritten ad groups against untouched ad groups (any reasonable control, e.g. similarly bad ones, or all others) OR against the rewritten groups' own longer pre-period CPA, and reports the numbers of that comparison (within about 10% of the reference values above).
FAIL if it only compares the selection week with the weeks after the change for the 10 rewritten ad groups.
"""

write_case(NAME, {"resources/adgroup_weekly.csv": csv_text, "resources/changes.csv": changes_csv}, prompt,
           [("no-real-effect", 3, g_effect), ("rollout-decision", 2, g_rollout), ("comparison-used", 1, g_comparison)])
print(f"{NAME}: treated {t_N:.1f}->{t_post:.1f} ({t_imp:.0%}), pre {t_pre:.1f}; placebo {p_W:.1f}->{p_post:.1f} ({p_imp:.0%}); ranks11-20 {c_imp:.0%}; DiD {did*100:+.0f}pp")
