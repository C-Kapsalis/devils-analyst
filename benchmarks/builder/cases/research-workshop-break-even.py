"""26% x 22,000 = 5,720 > 5,000 break-even looks like a go, but break-even is
22.7% and with n=250 the 26% is not significantly above it (z~1.2, p~0.11);
the CI straddles break-even, and 'would attend' overstates attendance."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "research-workshop-break-even"
rng = random.Random(6620)
N, YES, BASE, BE = 250, 65, 22000, 5000
ans = [1] * YES + [0] * (N - YES); rng.shuffle(ans)
rows = []
for i, a in enumerate(ans):
    rows.append([f"C{rng.randint(100000, 999999)}", rng.choice(["North", "South", "East", "West", "London"]),
                 rng.choice(["< 1 year", "1-3 years", "3+ years"]), a])
csv_text = to_csv(["customer_id", "region", "customer_tenure", "would_attend"], rows)

p = sum(r[3] for r in rows) / N
K = BE / BASE
se0 = math.sqrt(K * (1 - K) / N)
z = (p - K) / se0
pval = 0.5 * math.erfc(z / math.sqrt(2))
crit = K + 1.645 * se0
se = math.sqrt(p * (1 - p) / N)
lo, hi = p - 1.96 * se, p + 1.96 * se
assert p < crit and pval > 0.05 and lo * BASE < BE < p * BASE
print(f"{NAME}: p {p:.3f} K {K:.3f} z {z:.2f} p {pval:.3f}; CI {lo*BASE:,.0f}-{hi*BASE:,.0f}")

prompt = """
We're thinking of launching a paid in-person workshop for Brightleaf Gardening customers. It breaks even at 5,000 attendees, and we have 22,000 customers. We surveyed 250 randomly chosen customers and 26% said they'd attend (resources/workshop_survey.csv). Should we go ahead? Write report.md with your recommendation.
"""
g_dec = f"""
Ground truth. Break-even share = 5,000 / 22,000 = {100*K:.1f}%. Survey: {YES} of {N} = {100*p:.0f}% would attend.
- Test of H0 "true share <= {100*K:.1f}%": standard error {se0:.4f}, z = {z:.2f}, one-sided p = {pval:.2f}. The 5% one-sided critical share is {100*crit:.1f}%; {100*p:.0f}% is below it, so the survey does NOT show the share is above break-even.
- 95% CI for the share: {100*lo:.1f}% to {100*hi:.1f}% -> {lo*BASE:,.0f} to {hi*BASE:,.0f} attendees, which includes the 5,000 break-even.
Naive wrong answer: "26% x 22,000 = {p*BASE:,.0f} > 5,000, so launch."

PASS if report.md does NOT recommend an unconditional launch, because {100*p:.0f}% is not significantly above the {100*K:.1f}% break-even (or the confidence interval includes break-even / the margin is within sampling error), AND proposes a validation step (pre-sale, deposit, larger sample, pilot) before committing.
FAIL if it recommends launching because {p*BASE:,.0f} > 5,000, or treats the 26% as a precise estimate without considering sampling error.
"""
g_int = """
Ground truth: "would attend" in a survey overstates real attendance (no money or time committed, wish to please), so even a 26% stated share would likely translate into fewer actual attendees.

PASS if report.md notes that stated intent to attend overstates real attendance (or needs to be discounted / validated with paid sign-ups).
FAIL otherwise.
"""
write_case(NAME, {"resources/workshop_survey.csv": csv_text}, prompt, [("decision", 3, g_dec), ("intent", 1, g_int)])
