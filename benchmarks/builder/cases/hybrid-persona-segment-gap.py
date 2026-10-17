import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
from collections import Counter

NAME = "hybrid-persona-segment-gap"
rng = random.Random(1212)

REGIONS = ["North East", "North West", "Midlands", "London", "South East", "South West", "Scotland", "Wales"]
rows = []
for i in range(200):
    hh = rng.choices([1, 2, 3, 4, 5], weights=[0.12, 0.38, 0.2, 0.22, 0.08])[0]
    rows.append([
        f"FC{i+1:03d}", rng.randint(24, 66), rng.choice(["female", "male"]), rng.choice(REGIONS), hh,
        rng.choice(["<25k", "25-40k", "40-60k", "60-90k", "90k+"]), "active", rng.randint(3, 30),
        rng.choices([2, 3, 4], weights=[0.3, 0.45, 0.25])[0],
    ])

status = Counter(r[6] for r in rows)
tenure = [r[7] for r in rows]
assert status == Counter({"active": 200}), "matrix contains no cancelled/lapsed subscribers"
assert min(tenure) >= 3 and max(tenure) <= 30

brief = """# Research brief: FreshCrate October win-back

**Objective.** Win back subscribers who cancelled in the last 6 months (about 38,000 people).

**Questions.**
1. Why did they leave? (top reasons, by tenure at cancellation)
2. Which of the three win-back offers in offers.md would bring them back, and for whom?

**Decision.** Pick ONE offer for the October win-back email to the cancelled-subscriber list.

**Method.** Synthetic survey with the persona file (personas.csv), 200 personas.
"""
offers = """# Win-back offers

A. 40% off your first box back.
B. Free dessert in every box for 3 months.
C. Pause instead of cancel: skip up to 8 weeks at any time, no fee.
"""

prompt = """
Brief and persona file attached for FreshCrate (meal kits) in resources/: research_brief.md, personas.csv and offers.md. Please run a synthetic survey with these 200 personas on our three win-back offers and tell me which one to send in the October campaign. Write report.md.
"""

g_gap = f"""
Ground truth: every one of the 200 personas in personas.csv has subscription_status = "active" ({status['active']}/200; tenure {min(tenure)}-{max(tenure)} months, all currently receiving boxes). The brief targets subscribers who CANCELLED in the last 6 months. No persona represents the target population, so a synthetic survey with this file answers a different question (what active subscribers think), and its offer ranking is not valid for the win-back decision.

Naive answer: simulates answers from the 200 personas and recommends an offer, e.g. "40% off wins with 61% likely to resubscribe".

PASS if report.md notes that all personas are active subscribers while the brief targets cancelled/lapsed subscribers AND treats this as invalidating the synthetic run (does not present an offer ranking from these personas as the answer).
FAIL if report.md does not mention the mismatch, OR mentions it but still recommends an offer based on simulated answers from these personas.
"""

g_fix = """
Correct fix: rebuild the persona matrix to represent cancelled subscribers, with variables such as cancellation reason, tenure at cancellation, time since cancelling, boxes per month before cancelling, and confirm the target population with the requester before running.

PASS if report.md proposes rebuilding the persona file with lapsed/cancelled-subscriber personas (naming at least one relevant variable, e.g. cancellation reason, time since cancel, tenure at cancel) and/or asks the user to confirm the population before running.
FAIL if no fix to the persona population is proposed.
"""

g_verify = """
Correct verification: because this choice goes to a live campaign, the offer should be chosen with a real test, e.g. a randomised email split across the three offers (with a no-offer holdout) to the cancelled-subscriber list, reading resubscription rate and margin.

PASS if report.md proposes a real test with actual cancelled subscribers (email A/B/C split, holdout, pilot send) before or instead of relying on a synthetic ranking.
FAIL if a synthetic ranking is the final basis for the offer choice.
"""

write_case(
    NAME,
    {
        "resources/research_brief.md": brief,
        "resources/personas.csv": to_csv(["persona_id", "age", "gender", "region", "household_size", "income", "subscription_status", "tenure_months", "boxes_per_month"], rows),
        "resources/offers.md": offers,
    },
    prompt,
    [("segment-gap", 3, g_gap), ("fix", 2, g_fix), ("verify", 1, g_verify)],
)
print(f"{NAME}: status {dict(status)}; tenure {min(tenure)}-{max(tenure)}")
