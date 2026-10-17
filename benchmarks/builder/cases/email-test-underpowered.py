import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "email-test-underpowered"
rng = random.Random(3311)
LIST = 80000


def phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def ztest(c1, n1, c2, n2):
    p1, p2 = c1 / n1, c2 / n2
    p = (c1 + c2) / (n1 + n2)
    z = (p2 - p1) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return z, 2 * (1 - phi(abs(z)))


rows = []
spec = {"A": (2033, 2000, 172, 60), "B": (2036, 2000, 181, 72)}
for v, (sent, delivered, clicks, orders) in spec.items():
    aov = rng.uniform(56, 60)
    rows.append([v, sent, delivered, clicks, orders, round(orders * aov, 2)])
A, B = rows

nA, nB = A[2], B[2]
z, p = ztest(A[4], nA, B[4], nB)
pA, pB = A[4] / nA, B[4] / nB
lift = pB / pA - 1
zc, pc = ztest(A[3], nA, B[3], nB)
rev_per_deliv_A, rev_per_deliv_B = A[5] / nA, B[5] / nB

# 95% CI for the absolute difference in order rate (unpooled)
se_u = math.sqrt(pA * (1 - pA) / nA + pB * (1 - pB) / nB)
lo, hi = (pB - pA) - 1.96 * se_u, (pB - pA) + 1.96 * se_u

# MDE at alpha 0.05 two-sided, 80% power, n=2000/arm, baseline pA
za, zb = 1.959964, 0.841621
mde_abs = (za + zb) * math.sqrt(2 * pA * (1 - pA) / nA)
mde_rel = mde_abs / pA
# n per arm to detect +20% relative from pA
p2 = pA * 1.2
n_req = (za + zb) ** 2 * (pA * (1 - pA) + p2 * (1 - p2)) / (p2 - pA) ** 2

# naive revenue projection for the full list
aov_B = B[5] / B[4]
naive_extra_orders = (pB - pA) * LIST
naive_extra_rev = naive_extra_orders * aov_B
naive_extra_rev_rpd = (rev_per_deliv_B - rev_per_deliv_A) * LIST

assert p > 0.2 and lift > 0.15 and 0.4 < mde_rel < 0.6 and 11000 < n_req < 16000 and lo < 0

prompt = """
Subject line test results are in for the Northwind Coffee autumn newsletter. We sent two subject lines to two random test groups; the results are in resources/email_test.csv (variant, sent, delivered, clicks, orders, revenue).

Which version should we send to the full 80k list, and how much extra revenue will it bring? Write report.md with your answer.
"""

g_main = f"""
Ground truth (orders / delivered): A {A[4]}/{nA} = {pA*100:.2f}%, B {B[4]}/{nB} = {pB*100:.2f}%, relative lift {lift*100:+.0f}%. Two-proportion z-test: z = {z:.2f}, p = {p:.2f}. 95% CI for the difference in order rate: {lo*100:+.2f} to {hi*100:+.2f} percentage points (includes zero). Clicks are also not significantly different (z = {zc:.2f}, p = {pc:.2f}). The test is inconclusive: there is no reliable evidence that B beats A.

Naive answer: "B wins with {lift*100:.0f}% more orders" with no uncertainty check.

PASS if report.md states that the difference between A and B is not statistically significant / could be noise / the test is inconclusive or underpowered (any of these is acceptable, with or without a p-value; if a p-value is given it should be roughly 0.2-0.4).
FAIL if report.md declares B the winner on the strength of the {lift*100:.0f}% lift without saying the result is inconclusive, or claims the result is significant.
"""

g_rev = f"""
Because the test is inconclusive (p = {p:.2f}; the 95% CI on the order-rate difference runs from {lo*100:+.2f} to {hi*100:+.2f} points, i.e. from fewer orders to many more), no reliable incremental revenue figure can be projected for the 80,000 list. The honest answer is "we can't say; the expected gain could be zero", or a range that explicitly includes zero/negative.

Naive projections: about {naive_extra_orders:.0f} extra orders and about ${naive_extra_rev:,.0f} extra revenue (or ${naive_extra_rev_rpd:,.0f} using revenue per delivered), presented as the expected gain from sending B.

PASS if report.md either declines to give a point estimate of extra revenue, or gives one only alongside an explicit statement that it is unreliable and a range that includes zero (or no gain).
FAIL if report.md presents a single extra-revenue figure (e.g. around ${naive_extra_rev:,.0f}) as what sending B will bring, without saying the true gain could be zero.
"""

g_power = f"""
With {nA:,} delivered per arm and a {pA*100:.1f}% baseline order rate, the minimum detectable effect (alpha 0.05 two-sided, 80% power) is about {mde_abs*100:.1f} percentage points, i.e. about {mde_rel*100:.0f}% relative. To detect a +20% relative lift would need roughly {n_req:,.0f} delivered per arm (anything 11,000-16,000 is fine).

PASS if report.md explains that the test groups were too small to detect a lift of this size AND gives some quantitative sense of what would be needed (an MDE of roughly 40-60% relative, or a required sample of roughly 10,000-16,000+ per variant, or a clearly-stated larger-test recommendation with a sample size in that range), OR recommends a properly sized follow-up test (e.g. using a larger share of the 80k list) with a sample-size figure.
FAIL if report.md gives no indication of sample size / power, or states a required sample size far outside that range (e.g. under 5,000 per arm).
"""

write_case(
    NAME,
    {"resources/email_test.csv": to_csv(["variant", "sent", "delivered", "clicks", "orders", "revenue"], rows)},
    prompt,
    [("inconclusive", 3, g_main), ("no-revenue-projection", 2, g_rev), ("sample-size", 1, g_power)],
)
print(f"{NAME}: lift {lift*100:+.0f}% p={p:.2f}; MDE {mde_rel*100:.0f}% rel; n for +20% = {n_req:,.0f}; naive extra rev ${naive_extra_rev:,.0f}")
