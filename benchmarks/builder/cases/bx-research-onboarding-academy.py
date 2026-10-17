"""Customer-academy pilot read-out (Quillstack, B2B accounting software):
should the academy be made mandatory for all at-risk accounts?

Planted subtle problems (5):
P1 graduates vs everyone else: completion of a demanding 4-module course
   selects engaged accounts (graduates had far more Q1 logins). The pilot
   randomised the invitation, so the fair read is invited vs not invited
   (intent to treat): ~+3 pts renewal, not graduates' ~+20.
P2 the pilot picked the lowest Q1 health scores; the health "rebound" is
   regression to the mean: the randomly not-invited at-risk accounts rose by
   about the same.
P3 satisfaction question changed between waves (overall product -> support
   received); both groups jumped.
P4 "Enterprise graduates 100% renewal" from a handful of accounts.
P5 ITT lift is tested against nothing; the CS cost implies a 5-pt break-even
   and the ITT is below it and not significant.
Decision: do not make the academy mandatory / do not hire for rollout; the
causal effect (ITT) is below break-even; redesign and re-test larger.
Naive: roll out (graduates renew 20 pts more, health +11, CSAT up).
Decoys: invited vs not-invited balanced at baseline (300/300 by random draw);
blank health_score_q2 for accounts closed before scoring (documented).
"""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-research-onboarding-academy"
rng = random.Random(61)

N = 1200
COST_PER_INVITE = 150
RENEWAL_VALUE = 3000
K = COST_PER_INVITE / RENEWAL_VALUE  # break-even renewal lift per invited account (5 pts)


def clip(x, lo, hi):
    return max(lo, min(hi, x))


acc = []
for i in range(N):
    T = rng.gauss(62, 12)
    seg = rng.choices(["SMB", "Mid-market", "Enterprise"], [0.70, 0.24, 0.06])[0]
    q1 = clip(round(T + rng.gauss(0, 13)), 5, 100)
    logins = max(0, round(rng.gauss(6 + 0.25 * (T - 55), 3.5)))
    acc.append({"T": T, "seg": seg, "q1": q1, "logins": logins})

order = sorted(range(N), key=lambda k: (acc[k]["q1"], rng.random()))
elig = set(order[:600])
thr = max(acc[k]["q1"] for k in elig) + 1
elig_list = sorted(elig)
rng.shuffle(elig_list)
invited = set(elig_list[:300])

for k, a in enumerate(acc):
    a["elig"] = k in elig
    a["inv"] = k in invited
    if a["inv"]:
        pc = clip(0.06 * a["logins"] - 0.05, 0.03, 0.90)
        a["mods"] = 4 if rng.random() < pc else rng.choice([0, 0, 1, 1, 2, 3])
    else:
        a["mods"] = None
    grad = a["mods"] == 4
    p = clip(0.70 + 0.02 * (a["T"] - 55), 0.25, 0.97) + (0.075 if grad else 0.0)
    a["ren"] = 1 if rng.random() < p else 0
    if grad and a["seg"] == "Enterprise":
        a["ren"] = 1
    closed_early = a["ren"] == 0 and rng.random() < 0.12
    a["q2"] = None if closed_early else clip(round(a["T"] + rng.gauss(0, 9) + (3 if grad else 0)), 5, 100)

ids = list(range(N))
rng.shuffle(ids)
rows = []
for j, k in enumerate(ids):
    a = acc[k]
    rows.append([f"QS{10001 + j}", a["seg"], a["q1"], a["logins"], int(a["elig"]), int(a["inv"]),
                 "" if a["mods"] is None else a["mods"], "" if a["q2"] is None else a["q2"], a["ren"]])


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs)


inv = [a for a in acc if a["inv"]]
ctl = [a for a in acc if a["elig"] and not a["inv"]]
grads = [a for a in inv if a["mods"] == 4]
nongrad_inv = [a for a in inv if a["mods"] != 4]
everyone_else = [a for a in acc if a["elig"] and a["mods"] != 4]

r_inv, r_ctl = mean(a["ren"] for a in inv), mean(a["ren"] for a in ctl)
r_grad, r_else = mean(a["ren"] for a in grads), mean(a["ren"] for a in everyone_else)
itt = r_inv - r_ctl
se_itt = math.sqrt(r_inv * (1 - r_inv) / len(inv) + r_ctl * (1 - r_ctl) / len(ctl))
p_itt0 = math.erfc(abs(itt / se_itt) / math.sqrt(2))
p_vs_k = 0.5 * math.erfc(((itt - K) / se_itt) / math.sqrt(2))
lo, hi = itt - 1.96 * se_itt, itt + 1.96 * se_itt
naive_gap = r_grad - r_else
comp_rate = len(grads) / len(inv)
cace = itt / comp_rate

log_grad, log_non = mean(a["logins"] for a in grads), mean(a["logins"] for a in nongrad_inv)

h_inv = [a for a in inv if a["q2"] is not None]
h_ctl = [a for a in ctl if a["q2"] is not None]
hq1_inv, hq2_inv = mean(a["q1"] for a in h_inv), mean(a["q2"] for a in h_inv)
hq1_ctl, hq2_ctl = mean(a["q1"] for a in h_ctl), mean(a["q2"] for a in h_ctl)
hq1_inv_all, hq1_ctl_all = mean(a["q1"] for a in inv), mean(a["q1"] for a in ctl)
lg_inv, lg_ctl = mean(a["logins"] for a in inv), mean(a["logins"] for a in ctl)

ent_grads = [a for a in grads if a["seg"] == "Enterprise"]
ent_ctl = [a for a in ctl if a["seg"] == "Enterprise"]
n_closed = sum(1 for a in acc if a["q2"] is None)

# CSAT survey summary (aggregated, as the CS tool exports it)
CS = {("invited", "Q1"): (118, 3.38), ("not_invited", "Q1"): (112, 3.41),
      ("invited", "Q2"): (131, 4.06), ("not_invited", "Q2"): (104, 3.97)}
WORD = {"Q1": "How satisfied are you with Quillstack overall? (1-5)",
        "Q2": "How satisfied are you with the support you received from Quillstack this quarter? (1-5)"}
cs_rows = [[q, g, WORD[q], n, m] for (g, q), (n, m) in sorted(CS.items(), key=lambda x: (x[0][1], x[0][0]))]

# ---------- asserts ----------
assert naive_gap > 0.15, naive_gap
assert 0.01 < itt < 0.045 and p_itt0 > 0.2 and p_vs_k > 0.65, (itt, p_itt0, p_vs_k)
assert log_grad > 1.5 * log_non
assert (hq2_inv - hq1_inv) > 7 and abs((hq2_inv - hq1_inv) - (hq2_ctl - hq1_ctl)) < 3, (hq2_inv - hq1_inv, hq2_ctl - hq1_ctl)
assert abs(hq1_inv_all - hq1_ctl_all) < 2 and abs(lg_inv - lg_ctl) < 1
assert 3 <= len(ent_grads) <= 10 and all(a["ren"] == 1 for a in ent_grads)
assert 0.25 < comp_rate < 0.5

pct = lambda x: f"{100 * x:.1f}%"

files = {}
files["resources/accounts_pilot.csv"] = to_csv(
    ["account_id", "segment", "health_score_q1", "logins_q1", "at_risk_q1", "academy_invited", "academy_modules_completed",
     "health_score_q2", "renewed"], rows)
files["resources/csat_survey_summary.csv"] = to_csv(["wave", "group", "question_text", "responses", "mean_score"], cs_rows)
files["resources/academy_pilot_readout.md"] = f"""# Quillstack Academy pilot: results (Customer Success)

## Set-up
- Q1 2026: the 600 accounts with the lowest health score (all below {thr}) were flagged at risk.
- 300 of them were drawn at random and invited to the Academy, a 4-module live course (about 6 hours over 4 weeks). The other 300 at-risk accounts carried on as usual.
- Renewal measured at each account's Q2 renewal date. health_score_q2 is blank for accounts closed before the Q2 scoring run.

## Results
1. **Academy graduates renew far more.** Accounts that completed all 4 modules renewed at {pct(r_grad)} vs {pct(r_else)} for the other at-risk accounts (+{100 * naive_gap:.0f} pts).
2. **Health scores bounced back.** Invited accounts' average health score rose from {hq1_inv:.0f} in Q1 to {hq2_inv:.0f} in Q2 (+{hq2_inv - hq1_inv:.0f}).
3. **Customers are happier.** CSAT among invited accounts rose from {CS[('invited', 'Q1')][1]:.2f} to {CS[('invited', 'Q2')][1]:.2f}.
4. **Enterprise loves it.** {len(ent_grads)} of {len(ent_grads)} Enterprise graduates renewed (100%).

## Proposal
Make the Academy mandatory for every at-risk account from Q4, starting with Enterprise, and hire two more CS trainers. Fully loaded cost about GBP {COST_PER_INVITE} per account invited.
"""
files["resources/finance_inputs.md"] = f"""# Finance inputs for the Academy decision

- Average annual contribution from a renewed account: GBP {RENEWAL_VALUE:,}.
- Academy cost per invited account (trainer time, materials, CSM follow-up): GBP {COST_PER_INVITE}.
"""

prompt = """
Our Customer Success team ran an Academy pilot for at-risk accounts and wants to make it mandatory and hire two trainers. Their read-out is resources/academy_pilot_readout.md; the account-level export, the CSAT summary and finance's inputs are also in resources/. I have to give the COO a recommendation on Monday. Does the pilot support rolling it out? Put your answer and the numbers in report.md.
"""

g_recall = f"""
The materials contain 5 planted problems. Answer key (computed from accounts_pilot.csv and the other files):

1. Graduates are self-selected. Completing a 4-week course selects engaged accounts: graduates averaged {log_grad:.1f} Q1 logins vs {log_non:.1f} for invited non-graduates. The invitation was randomised, so the fair comparison is invited ({len(inv)}) vs not-invited at-risk accounts ({len(ctl)}): renewal {pct(r_inv)} vs {pct(r_ctl)}, +{100 * itt:.1f} pts, not the +{100 * naive_gap:.0f} pts graduates vs other at-risk accounts. Counts as found if report.md says the graduate comparison is biased by self-selection/engagement AND gives the invited vs not-invited comparison (any figure between +0 and +6 pts, or the two renewal rates).
2. Health rebound is regression to the mean. The pilot picked the lowest Q1 health scores; the not-invited at-risk accounts also rose from {hq1_ctl:.0f} to {hq2_ctl:.0f} (+{hq2_ctl - hq1_ctl:.0f}) vs invited {hq1_inv:.0f} to {hq2_inv:.0f} (+{hq2_inv - hq1_inv:.0f}). Counts as found if report.md says the control group rose about as much, or names regression to the mean / selection on low scores, with a number.
3. CSAT question changed. Q1 asked satisfaction with "Quillstack overall"; Q2 asked about "the support you received this quarter". Not-invited accounts also rose ({CS[('not_invited', 'Q1')][1]:.2f} to {CS[('not_invited', 'Q2')][1]:.2f}). Counts as found if report.md notes the wording change or that the not-invited group rose similarly.
4. Enterprise 100% is {len(ent_grads)} accounts. Counts as found if report.md flags the Enterprise claim as based on too few accounts (quotes the n, or says too small to act on).
5. Effect vs break-even. At GBP {COST_PER_INVITE} per invited account and GBP {RENEWAL_VALUE:,} per renewal, the Academy pays only if it lifts renewal by at least {100 * K:.0f} pts per invited account. The randomised lift is +{100 * itt:.1f} pts (95% CI {100 * lo:+.1f} to {100 * hi:+.1f}; p vs zero about {p_itt0:.2f}), below break-even. Counts as found if report.md compares the invited-vs-not-invited lift (or its value per account) with the {100 * K:.0f}-pt break-even or with the GBP {COST_PER_INVITE} cost.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 5 problems, each with evidence (a number, column or quote).
FAIL if fewer than 3 are identified with evidence.
"""

g_decision = f"""
Decision: make the Academy mandatory for at-risk accounts and hire two trainers, or not.

Ground truth: the only unbiased comparison is the randomised one: invited {pct(r_inv)} vs not invited {pct(r_ctl)} renewal, +{100 * itt:.1f} pts (95% CI {100 * lo:+.1f} to {100 * hi:+.1f}, not significant). Value per invited account is about GBP {itt * RENEWAL_VALUE:,.0f} vs GBP {COST_PER_INVITE} cost; break-even needs +{100 * K:.0f} pts. (Effect per graduate, ITT / completion rate {pct(comp_rate)}, is about +{100 * cace:.0f} pts; acceptable as context, but the cost is per invited account.) Correct main recommendation: do not make it mandatory or hire for a rollout on this evidence; redesign (e.g. shorter format to raise completion, lower cost) and/or run a larger randomised test against the {100 * K:.0f}-pt break-even.

Naive wrong recommendation: roll it out because graduates renew {100 * naive_gap:.0f} pts more, health rose +{hq2_inv - hq1_inv:.0f} and CSAT rose.

PASS if report.md's main recommendation is not to roll out/mandate it now (hold, redesign, or re-test before committing) AND the reasoning rests on the invited-vs-not-invited comparison or on the effect falling short of the cost.
FAIL if report.md recommends rolling out / mandating the Academy or hiring the trainers (even with caveats), or rests the decision on the graduates-vs-others gap.
"""

g_decoys = f"""
Two things could look wrong but are fine and must not be presented as problems:
- D1. The randomisation worked. Invited and not-invited at-risk accounts are 300 vs 300 and are balanced at baseline: Q1 health {hq1_inv_all:.1f} vs {hq1_ctl_all:.1f}, Q1 logins {lg_inv:.1f} vs {lg_ctl:.1f}. Saying the two randomised groups are not comparable, or that the split is suspicious, is a false alarm. (Saying graduates are not comparable to non-graduates is correct and is NOT a false alarm.)
- D2. {n_closed} accounts have blank health_score_q2. The read-out says these accounts closed before the Q2 scoring run; all of them have renewed = 0, so renewal is complete. Calling this a data-quality defect or missing renewal data is a false alarm. (Noting that health averages exclude closed accounts is fine.)

PASS if report.md presents neither D1 nor D2 as a problem.
FAIL if it says the invited and not-invited groups are unbalanced/not comparable or the randomisation failed, OR treats the blank health_score_q2 values as a data error that undermines the renewal analysis.
"""

assert all(a["ren"] == 0 for a in acc if a["q2"] is None)

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoys)])
print(f"{NAME}: grads {r_grad:.3f} vs else {r_else:.3f} (+{naive_gap:.3f}); ITT {r_inv:.3f}-{r_ctl:.3f}={itt:.3f} [{lo:.3f},{hi:.3f}] p0 {p_itt0:.2f}; "
      f"completion {comp_rate:.2f}; health inv {hq1_inv:.0f}->{hq2_inv:.0f} ctl {hq1_ctl:.0f}->{hq2_ctl:.0f}; ent grads {len(ent_grads)}; logins {log_grad:.1f}/{log_non:.1f}")
