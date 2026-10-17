"""12% answered the email survey and 65% of them are interested; a phone
follow-up of non-respondents finds only 18%. Weight the two strata by the
response rate: ~24% interested (~9.5k of 40k), not 65% (26k) or the pooled
54%. Stated interest also overstates sign-ups."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "research-membership-nonresponse"
rng = random.Random(5903)
BASE, SENT = 40000, 4000
# (wave, n, very, somewhat)
SPEC = [("email", 480, 170, 142), ("phone_followup", 150, 9, 18)]
rows, k = [], 1
for wave, n, very, some in SPEC:
    ans = ["very"] * very + ["somewhat"] * some + ["not"] * (n - very - some)
    rng.shuffle(ans)
    for a in ans:
        seg = rng.choice(["1 order", "2-4 orders", "5+ orders"])
        rows.append([f"R{k:04d}", wave, "2026-09-" + f"{rng.randint(8, 26):02d}", seg, a]); k += 1
csv_text = to_csv(["respondent_id", "wave", "completed_date", "order_history", "interest_in_membership"], rows)
fielding = to_csv(["wave", "contacted", "completed"], [["email", SENT, 480], ["phone_followup", 200, 150]])

def share(wave, levels):
    s = [r for r in rows if r[1] == wave]
    return sum(r[4] in levels for r in s) / len(s), len(s)
IN = ("very", "somewhat")
pe, ne = share("email", IN); pp, np_ = share("phone_followup", IN)
rr = ne / SENT
w = rr * pe + (1 - rr) * pp
se = math.sqrt(rr ** 2 * pe * (1 - pe) / ne + (1 - rr) ** 2 * pp * (1 - pp) / np_)
lo, hi = w - 1.96 * se, w + 1.96 * se
pe_v, _ = share("email", ("very",)); pp_v, _ = share("phone_followup", ("very",))
w_v = rr * pe_v + (1 - rr) * pp_v
pooled = sum(r[4] in IN for r in rows) / len(rows)
assert pe > 2.5 * w and pooled > 2 * w, (pe, pooled, w)
print(f"{NAME}: email {pe:.3f}, phone {pp:.3f}, weighted {w:.3f} ({w*BASE:,.0f}; CI {lo*BASE:,.0f}-{hi*BASE:,.0f}); very-only weighted {w_v:.3f}; pooled {pooled:.3f}")

prompt = """
We're thinking about launching a paid membership ($59 a year) for our customers at Harbor Outdoor. We emailed a survey to 4,000 of our 40,000 active customers; the answers are in resources/survey_responses.csv. We also phoned a random sample of people who didn't answer the email, and their answers are in the same file (wave = phone_followup). Fieldwork counts are in resources/fielding_summary.csv. How many members should we plan for at launch? Write report.md with the number and how you got there.
"""
g_w = f"""
Ground truth. The email survey got {ne} completes from {SENT:,} (response rate {100*rr:.0f}%). Email respondents are {100*pe:.0f}% very or somewhat interested; the phone follow-up of non-respondents ({np_} completes) finds only {100*pp:.0f}%. Non-respondents are {100*(1-rr):.0f}% of customers, so the two groups must be weighted by the response rate:
{rr:.2f} x {100*pe:.0f}% + {1-rr:.2f} x {100*pp:.0f}% = {100*w:.1f}% interested (95% CI about {100*lo:.0f}% to {100*hi:.0f}%) -> about {w*BASE:,.0f} of {BASE:,} customers (CI about {lo*BASE:,.0f} to {hi*BASE:,.0f}).
Also acceptable: the same weighting using only "very interested" ({100*w_v:.1f}% -> about {w_v*BASE:,.0f}).
Naive wrong answers: email respondents only, {100*pe:.0f}% -> {pe*BASE:,.0f}; pooling both waves unweighted, {100*pooled:.1f}% -> {pooled*BASE:,.0f}.

PASS if report.md's headline interest share is between {100*w_v*0.85:.0f}% and 29% (or an interested count between {w_v*BASE*0.85:,.0f} and 11,700), obtained by weighting email respondents and non-respondents by the response rate.
FAIL if the headline share is 45% or more (e.g. {100*pe:.0f}% or {100*pooled:.0f}%), or the planned figure is based on email respondents alone.
"""
g_int = f"""
Ground truth: saying you are "interested" in a survey is not paying $59. Stated interest overstates real sign-ups, so the launch plan should be below the interested count (about {w*BASE:,.0f}), e.g. by applying a conversion/deflation factor, or the interest should be validated with a behavioural test (pre-order, deposit, waitlist with payment) before committing.

PASS if report.md says stated interest overstates actual sign-ups AND either plans a member number below the interested count or proposes a pre-order / deposit / paid-waitlist style test.
FAIL if it plans members equal to the interested count with no caveat about intent versus behaviour.
"""
write_case(NAME, {"resources/survey_responses.csv": csv_text, "resources/fielding_summary.csv": fielding}, prompt,
           [("weighting", 3, g_w), ("intent-deflation", 2, g_int)])
