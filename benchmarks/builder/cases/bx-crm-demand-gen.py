"""Breadth: next quarter's demand-gen budget from a CRM review (Quillstack, B2B SaaS, Jan-Sep 2026).

Planted problems (5): sources ranked on cost per lead; on cost per
opportunity and revenue per lead (mature cohorts) the order inverts, content
syndication is cheapest per lead and worst per opportunity, paid search the
reverse (DECISION); the "MQL to SQL 9%" comes from today's lifecycle snapshot,
not from stage-entry counts by cohort; webinars (started August) judged on
customers before their leads could close; a May badge-scan list import counted
as event leads; deals created without an amount leave pipeline understated
for one source.
Decoys (2): sales cycle quoted as a median well under the mean; win rate
computed as won / (won + lost), excluding open deals."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-crm-demand-gen"
rng = random.Random(82010)
MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]
# source: leads/mo, p_mql, p_sql|mql, p_opp|sql, p_win|opp, deal, spend/mo, start month index
SRC = {
    "paid_search": (120, 0.55, 0.50, 0.82, 0.30, 24000, 30000, 0),
    "linkedin_ads": (260, 0.45, 0.25, 0.70, 0.22, 18000, 31000, 0),
    "content_syndication": (600, 0.35, 0.06, 0.55, 0.15, 15000, 21000, 0),
    "webinar": (180, 0.60, 0.42, 0.78, 0.27, 21000, 9000, 7),
    "events": (90, 0.50, 0.40, 0.72, 0.25, 22000, 14000, 0),
    "organic_search": (140, 0.40, 0.35, 0.75, 0.25, 19000, 0, 0),
    "referral": (40, 0.70, 0.60, 0.82, 0.40, 26000, 0, 0),
}
def frac_opp(age):   # share of eventual opportunities already created at this cohort age (months)
    return min(1.0, (age + 0.3) / 2.0)
def frac_won(age):
    return max(0.0, min(1.0, (age - 1.5) / 3.0))

coh, spend = [], []
for mi, m in enumerate(MONTHS):
    age = 8 - mi + 0.5
    for s, (n, pm, ps, po, pw, deal, sp, st) in SRC.items():
        if mi < st:
            continue
        methods = [("form", int(n * rng.uniform(0.9, 1.1)))]
        if s == "events" and m == "2026-05":
            methods.append(("import", 1400))
        for meth, leads in methods:
            q = 0.08 if meth == "import" else 1.0
            mql = int(leads * pm * q * rng.uniform(0.95, 1.05))
            sql = int(mql * (ps * (0.2 if meth == "import" else 1)) * min(1, (age + 0.5) / 1.0) * rng.uniform(0.92, 1.08))
            opp_eventual = sql * po
            opp = int(round(opp_eventual * frac_opp(age) * rng.uniform(0.92, 1.08)))
            won = int(round(opp * pw * frac_won(age) / max(frac_opp(age), 1e-9) * rng.uniform(0.9, 1.1))) if frac_won(age) > 0 else 0
            won = min(won, opp)
            amt = round(won * deal * rng.uniform(0.9, 1.1), 2)
            opp_amt_missing = int(opp * (0.45 if s == "linkedin_ads" else 0.04))
            coh.append([m, s, meth, leads, mql, sql, opp, opp_amt_missing, won, amt])
        if sp:
            spend.append([m, s, round(sp * (3.0 if s == "events" and m == "2026-05" else 1) * rng.uniform(0.95, 1.05), 2)])

def agg(s, months=None, meth=None):
    rows = [r for r in coh if r[1] == s and (months is None or r[0] in months) and (meth is None or r[2] == meth)]
    return [sum(r[i] for r in rows) for i in range(3, 10)]
def sp(s, months=None):
    return sum(r[2] for r in spend if r[1] == s and (months is None or r[0] in months))
MATURE = MONTHS[:5]   # Jan-May cohorts, 4+ months old
paid = ["paid_search", "linkedin_ads", "content_syndication", "events"]
cpl = {s: sp(s) / agg(s)[0] for s in paid + ["webinar"]}
cpo = {s: sp(s, MATURE) / agg(s, MATURE)[3] for s in paid}
rpl = {s: agg(s, MATURE)[6] / agg(s, MATURE)[0] for s in paid}
roi = {s: agg(s, MATURE)[6] / sp(s, MATURE) for s in paid}
cpl_rank = sorted(paid, key=lambda s: cpl[s])
cpo_rank = sorted(paid, key=lambda s: cpo[s])

# snapshot: current lifecycle stage (closed-lost opportunities go back to "other")
snap = []
for s in SRC:
    L, M, S, O, miss, W, A = agg(s)
    lost = int((O - W) * 0.55)
    cur = {"lead": L - M, "marketingqualifiedlead": M - S, "salesqualifiedlead": S - O, "opportunity": O - W - lost, "customer": W, "other": lost}
    for st, v in cur.items():
        snap.append([s, st, v])
tot_snap = lambda st: sum(r[2] for r in snap if r[1] == st)
snap_rate = tot_snap("salesqualifiedlead") / tot_snap("marketingqualifiedlead")
tot_M = sum(agg(s, MATURE)[1] for s in SRC); tot_S = sum(agg(s, MATURE)[2] for s in SRC)
true_rate = tot_S / tot_M

web = agg("webinar")
web_opp_rate = web[3] / web[0]
ps_age_match = [r for r in coh if r[1] == "paid_search" and r[0] in ("2026-08", "2026-09")]
ps_young_opp_rate = sum(r[6] for r in ps_age_match) / sum(r[3] for r in ps_age_match)
imp = agg("events", meth="import"); evf = agg("events", meth="form")
li_missing = agg("linkedin_ads")[4] / agg("linkedin_ads")[3]

# deals for cycle / win rate decoys
cycles = sorted([int(rng.lognormvariate(math.log(52), 0.6)) for _ in range(140)])
med_cycle = cycles[len(cycles) // 2]; mean_cycle = sum(cycles) / len(cycles)
won_n = sum(agg(s)[5] for s in SRC); lost_n = sum(int((agg(s)[3] - agg(s)[5]) * 0.55) for s in SRC)
open_n = sum(agg(s)[3] for s in SRC) - won_n - lost_n
win_rate = won_n / (won_n + lost_n)

assert cpl_rank[0] == "content_syndication" and cpl_rank[-1] in ("paid_search", "events")
assert cpo_rank[0] == "paid_search" and cpo_rank[-1] == "content_syndication", cpo_rank
assert cpo["content_syndication"] > 2.5 * cpo["paid_search"]
assert snap_rate < 0.5 * true_rate, (snap_rate, true_rate)
assert web[5] == 0 and web_opp_rate > 0.6 * ps_young_opp_rate
assert imp[0] == 1400 and imp[0] > 2 * evf[0] / 9
pipe = {s: (agg(s)[3] - agg(s)[4]) * SRC[s][5] for s in paid}
pipe_per_dollar = {s: pipe[s] / sp(s) for s in paid}
li_pipe_full = agg("linkedin_ads")[3] * SRC["linkedin_ads"][5]
assert li_missing > 0.35
assert pipe_per_dollar["linkedin_ads"] < 0.5 * pipe_per_dollar["paid_search"], pipe_per_dollar
assert med_cycle < mean_cycle * 0.9

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=0: f"{100 * x:.{d}f}%"

tbl = "\n".join(f"| {s} | {usd(sp(s))} | {agg(s)[0]:,} | {usd(cpl[s])} |" for s in cpl_rank)
review = f"""# Demand generation review, Jan-Sep 2026 (marketing ops)

## Cost per lead by source
| Source | Spend | Leads | Cost per lead |
|---|---|---|---|
{tbl}

## Funnel
- MQL to SQL conversion is only {pc(snap_rate)} (lifecycle stage report, today): sales is not working our MQLs.
- Webinars have produced {web[5]} customers since launch in August.
- Pipeline created Jan-Sep (sum of opportunity amounts): {', '.join(f'{k} {usd(v)}' for k, v in pipe.items())}. LinkedIn Ads creates ${pipe_per_dollar['linkedin_ads']:.1f} of pipeline per dollar against ${pipe_per_dollar['paid_search']:.1f} for paid search; we plan to cut it in Q1.
- Win rate {pc(win_rate)} (won / (won + lost)); median sales cycle {med_cycle} days.

## Recommendation for Q4
Move the paid search budget ({usd(sp('paid_search') / 9)} a month) into content syndication, our cheapest lead source, and stop webinars.
"""

notes = """# Notes
- Quillstack sells workflow software to finance teams; annual contracts.
- lead_cohorts_by_source.csv: contacts by creation month and original source, with how many of them have ever entered each lifecycle stage (from the stage entry date properties), as of 30 September 2026. create_method shows form fills vs list imports.
- lifecycle_stage_snapshot.csv: contacts by their current lifecycle stage today.
"""

files = {
    "resources/notes.md": notes,
    "resources/demand_gen_review.md": review,
    "resources/lead_cohorts_by_source.csv": to_csv(["create_month", "original_source", "create_method", "leads", "reached_mql", "reached_sql", "reached_opportunity",
                                                    "opportunities_without_amount", "closed_won_deals", "closed_won_amount"], coh),
    "resources/lifecycle_stage_snapshot.csv": to_csv(["original_source", "current_lifecycle_stage", "contacts"], snap),
    "resources/marketing_spend_by_source.csv": to_csv(["month", "source", "spend"], spend),
    "resources/closed_won_cycle_days.csv": to_csv(["deal_index", "days_create_to_close"], [[i + 1, c] for i, c in enumerate(cycles)]),
}

prompt = """
Marketing ops put together a demand gen review with a Q4 budget recommendation (resources/demand_gen_review.md). The CRM and spend exports are in resources/. Where should next quarter's demand gen budget go? Please write your recommendation in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. Cost per lead ranks sources backwards. On mature cohorts (created January-May), cost per opportunity is paid_search {usd(cpo['paid_search'])}, linkedin_ads {usd(cpo['linkedin_ads'])}, events {usd(cpo['events'])}, content_syndication {usd(cpo['content_syndication'])}; closed-won revenue per lead is paid_search {usd(rpl['paid_search'])} vs content_syndication {usd(rpl['content_syndication'])}. Content syndication has the lowest cost per lead ({usd(cpl['content_syndication'])}) but the highest cost per opportunity. Counts as found if report.md compares sources on cost per opportunity, revenue per lead or return on spend and shows content syndication is weak / paid search strong.
2. MQL-to-SQL from the wrong count. The {pc(snap_rate)} uses contacts currently at SQL vs currently at MQL; contacts who moved on to opportunity or customer drop out. By stage-entry counts for January-May cohorts it is about {pc(true_rate)}. Counts as found if report.md says the snapshot understates conversion and recomputes it (roughly {pc(true_rate)}, or from reached_* columns).
3. Webinars judged too early. Webinar leads exist only from August; deals take months to close, so {web[5]} customers is expected. Their opportunity rate so far ({pc(web_opp_rate, 1)}) is comparable to paid search leads of the same age ({pc(ps_young_opp_rate, 1)}). Counts as found if report.md says webinars are too young to judge on customers.
4. List import counted as event leads. In May, events include a create_method = import of 1,400 contacts (badge scans) that barely convert, against about {evf[0] // 9} event form leads a month. Counts as found if report.md flags the import inflating event lead counts.
5. Pipeline understated for LinkedIn. {pc(li_missing)} of LinkedIn Ads opportunities have no amount, so the review's {usd(pipe['linkedin_ads'])} LinkedIn pipeline understates it (about {usd(li_pipe_full)} if those opportunities carried a typical amount). Counts as found if report.md flags the missing amounts.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct recommendation: do not move paid search money into content syndication. Judged on cost per opportunity or revenue per lead, paid search is the strongest paid source ({usd(cpo['paid_search'])} per opportunity) and content syndication the weakest ({usd(cpo['content_syndication'])} per opportunity). Budget should go toward paid search (or at least be kept there) and away from content syndication; webinars should continue until their cohorts are old enough to judge.

Naive answer: follow the review and shift budget to content syndication because of its {usd(cpl['content_syndication'])} cost per lead (and stop webinars).

PASS if report.md's main recommendation keeps or increases paid search and reduces (or does not increase) content syndication, based on opportunity- or revenue-level metrics.
FAIL if report.md endorses moving budget into content syndication, or ranks sources on cost per lead.
"""

g_decoy = f"""
Two things are correct in the review and must not be presented as errors:
- D1. The sales cycle is quoted as a median ({med_cycle} days); the mean is {mean_cycle:.0f} days because a few deals take very long. The median is the right typical value.
- D2. Win rate {pc(win_rate)} is computed as won / (won + lost), excluding {open_n:,} open opportunities. That is the correct definition.

PASS if report.md does not say the cycle should be the mean or that the win rate should include open deals. Agreeing with either, or not mentioning them, is fine.
FAIL if either is presented as a mistake.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: CPL {{{', '.join(f'{k}:{v:.0f}' for k, v in cpl.items())}}}; CPO {{{', '.join(f'{k}:{v:.0f}' for k, v in cpo.items())}}}; "
      f"snap {snap_rate:.3f} true {true_rate:.3f}; webinar opp {web_opp_rate:.3f} vs ps young {ps_young_opp_rate:.3f}; li missing {li_missing:.2f}; cycle {med_cycle}/{mean_cycle:.0f}")
