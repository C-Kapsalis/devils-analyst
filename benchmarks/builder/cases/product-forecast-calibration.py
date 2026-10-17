"""Year-one units from a concept test: the naive forecast uses the top-two-box
share (45%) as the purchase probability (and often skips awareness and
distribution). Calibrated: N x awareness x availability x (0.4 F_def + 0.2
F_prob) ~ 15k units, not 54k (or 180k)."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "product-forecast-calibration"
rng = random.Random(8906)
COUNTS = [("definitely would buy", 43), ("probably would buy", 65), ("might or might not buy", 70),
          ("probably would not buy", 40), ("definitely would not buy", 22)]
labels = [c for c, n in COUNTS for _ in range(n)]; rng.shuffle(labels)
rows = [[f"R_{5000 + i}", "Yes", rng.choice(["18-34", "35-54", "55+"]), lab] for i, lab in enumerate(labels)]
pi_csv = to_csv(["response_id", "q1_rides_weekly", "age_band", "pi_smartlock_at_89"], rows)
plan = to_csv(["item", "value", "note"], [
    ["target_households", 400000, "households in launch markets with a bike ridden weekly"],
    ["planned_aided_awareness_y1", 0.50, "media plan target"],
    ["retail_distribution_coverage_y1", 0.60, "share of target households near a stocking retailer or reachable online"],
    ["price", 89, "USD"], ["launch", "2027-04", ""], ["units_per_buyer", 1, "durable, no repeat purchase in year one"]])

N = len(rows)
fd = sum(r[3] == "definitely would buy" for r in rows) / N
fp = sum(r[3] == "probably would buy" for r in rows) / N
HH, AW, AV = 400000, 0.50, 0.60
A = AW * AV
P = 0.4 * fd + 0.2 * fp
Q = HH * A * P
q_lo = HH * A * (0.1 * fd + 0.0 * fp); q_hi = HH * A * (0.5 * fd + 0.25 * fp)
naive_t2b = HH * A * (fd + fp); naive_t2b_noA = HH * (fd + fp); naive_tb = HH * A * fd
assert naive_t2b > 3 * Q and naive_tb > Q * 1.3
print(f"{NAME}: F_def {fd:.3f} F_prob {fp:.3f}; Q {Q:,.0f} (range {q_lo:,.0f}-{q_hi:,.0f}); naive T2B {naive_t2b:,.0f} / {naive_t2b_noA:,.0f}; top-box {naive_tb:,.0f}")

prompt = """
We're launching the Ridgeline SmartLock at $89 next spring. resources/ has the respondent-level purchase-intent answers from our concept test (pi_results.csv) and our launch plan (launch_plan.csv). How many units should we plan to sell in the first year? Put the forecast and how you got it in report.md.
"""
g_fc = f"""
Ground truth. Of {N} qualified respondents, {100*fd:.1f}% said "definitely" and {100*fp:.1f}% "probably" would buy. Stated intent must be calibrated before it is used as a purchase probability: typical weights are about 0.4 for "definitely" and 0.2 for "probably" (documented ranges roughly 0.1-0.5 and 0-0.25), giving P = {P:.3f}.
Availability-adjusted reach = awareness 0.50 x distribution 0.60 = {A:.2f}.
Forecast = {HH:,} households x {A:.2f} x {P:.3f} = about {Q:,.0f} units (revenue about ${Q*89/1e6:.2f}M). Any calibration within the documented ranges gives roughly {q_lo:,.0f} to {q_hi:,.0f} units.
Naive wrong forecasts: top-two-box share as the probability, {HH:,} x {A:.2f} x {fd+fp:.2f} = {naive_t2b:,.0f} (or {naive_t2b_noA:,.0f} ignoring awareness and distribution); top-box share as the probability, {naive_tb:,.0f}.

PASS if the base-case forecast in report.md is between 2,000 and 19,000 units AND is built from households x awareness x availability x a purchase probability that discounts the "definitely" and "probably" answers.
FAIL if it uses the raw top-box or top-two-box share as the purchase probability, omits awareness or distribution, or the base forecast is above 19,000 units.
"""
g_cav = """
Ground truth: a single-point forecast from stated intent is fragile. A good report gives a range or sensitivity (e.g. low/base/high calibration weights, or awareness/distribution scenarios) and explains why stated intent overstates purchases (hypothetical money, wish to please the interviewer, polished concept stimulus, no competing products shown, etc.).

PASS if report.md gives a range or sensitivity around the forecast AND names at least one reason stated intent overstates real buying.
FAIL otherwise.
"""
write_case(NAME, {"resources/pi_results.csv": pi_csv, "resources/launch_plan.csv": plan}, prompt,
           [("forecast", 3, g_fc), ("caveats", 1, g_cav)])
