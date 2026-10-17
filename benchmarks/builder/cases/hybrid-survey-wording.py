import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "hybrid-survey-wording"
rng = random.Random(1313)

FEATURES = ["budgeting", "bill_reminders", "savings_goals", "spending_insights", "shared_accounts"]
OPEN = ["", "", "", "Love the app", "More bank integrations please", "Dark mode", "Keep it up", "Export to spreadsheet would help", ""]


def clip(x, lo, hi):
    return max(lo, min(hi, int(round(x))))


rows = []
for i in range(40):
    q3 = 5 if i not in (7, 29) else 4
    rank = FEATURES[:]
    rng.shuffle(rank)
    if rng.random() < 0.7:  # budgeting usually first
        rank.remove("budgeting"); rank.insert(0, "budgeting")
    rows.append([
        f"SP{i+1:02d}",
        clip(rng.gauss(4.0, 0.75), 1, 5),
        rng.choices(["daily", "weekly", "monthly", "less often"], weights=[0.45, 0.4, 0.1, 0.05])[0],
        q3,
        clip(rng.gauss(3.9, 0.8), 1, 5),
        clip(rng.gauss(4.3, 0.55), 1, 5),
        clip(rng.gauss(8.2, 1.0), 0, 10),
        "yes" if i not in (3, 18, 33) else "no",
        clip(rng.gauss(3.6, 0.85), 1, 5),
        ">".join(rank),
        clip(rng.gauss(3.8, 0.8), 1, 5),
        clip(rng.gauss(4.1, 0.75), 1, 5),
        rng.choice(OPEN),
    ])


def sd(x):
    m = sum(x) / len(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


q3_fives = sum(r[3] == 5 for r in rows)
q5_mean = sum(r[5] for r in rows) / 40
q7_yes = sum(r[7] == "yes" for r in rows) / 40
clean_sd = {k: sd([r[j] for r in rows]) for k, j in (("Q1", 1), ("Q4", 4), ("Q8", 8), ("Q10", 10), ("Q11", 11))}
q3_sd = sd([r[3] for r in rows])

assert q3_fives == 38 and q3_sd < 0.25
assert q7_yes > 0.9 and 4.1 < q5_mean < 4.5
assert all(0.55 < v < 1.0 for v in clean_sd.values()), clean_sd

survey = """# Lumo customer survey - draft v3

Intro: "Thanks for helping us improve Lumo! This takes about 5 minutes."

Q1. Overall, how satisfied are you with Lumo? (1 = very dissatisfied, 5 = very satisfied)
Q2. How often do you use Lumo? (daily / weekly / monthly / less often)
Q3. How much did you enjoy our new, faster bank sync? (1 = not at all, 5 = a great deal)
Q4. How easy is it to find what you need in the app? (1 = very difficult, 5 = very easy)
Q5. "The app is fast and easy to use." (1 = strongly disagree, 5 = strongly agree)
Q6. How likely are you to recommend Lumo to a friend or colleague? (0-10)
Q7. Do you follow the latest tech trends? (Yes / No)
Q8. How would you rate the value for money of Lumo Plus? (1 = very poor, 5 = very good)
Q9. Rank these five features from most to least important to you: budgeting, bill reminders, savings goals, spending insights, shared accounts.
Q10. How satisfied are you with Lumo customer support? (1 = very dissatisfied, 5 = very satisfied)
Q11. How reliable is the app for you (crashes, errors, failed syncs)? (1 = very unreliable, 5 = very reliable)
Q12. Is there anything else you'd like to tell us? (open text)
"""

prompt = """
resources/ has our customer survey draft for the Lumo budgeting app (survey_draft.md) and a 40-respondent synthetic pilot we ran on it (synthetic_pilot.csv). The pilot looks clean, no weird answers.

Is the survey ready to field to 800 customers next week? Write report.md with your verdict and anything we should change.
"""

g_dbl = """
Ground truth: Q5 ("The app is fast and easy to use.") is double-barrelled: it asks about two different attributes (speed and ease of use) in one item, so an answer cannot be interpreted. Fix: split into two items (one on speed, one on ease of use).

PASS if report.md flags Q5 as asking two things at once (double-barrelled) and recommends splitting it.
FAIL otherwise.
"""

g_lead = f"""
Ground truth: Q3 ("How much did you enjoy our new, faster bank sync?") is leading/loaded: it presumes the respondent enjoyed it and asserts the bank sync is "faster". In the synthetic pilot {q3_fives} of 40 answered 5 (SD {q3_sd:.2f}), a symptom of the wording, not proof of delight. Fix: neutral wording, e.g. "How would you rate the speed of bank sync?" or "How satisfied are you with bank sync?", without praising the change.

PASS if report.md flags Q3 as leading / loaded / presumptive (it assumes enjoyment and/or calls the sync faster) AND proposes neutral wording.
FAIL if Q3 is not flagged, or is only dropped/flagged for low variance without naming the wording problem.
"""

g_fmt = """
Ground truth: Q7 asks an attitude/behaviour as a yes/no (better as a 5- or 7-point frequency/agreement scale, and its relevance is unclear); Q9 is a 5-item forced ranking (hard on mobile, gives only relative order; better as an importance rating per feature or a top-pick question).

PASS if report.md flags at least one of Q7 (binary format for a graded attitude) or Q9 (ranking format) with a concrete fix.
FAIL if neither is flagged.
"""

g_verdict = f"""
Ground truth: the survey is NOT ready as is (Q3 leading, Q5 double-barrelled, plus format issues). The "clean" synthetic pilot cannot certify the survey: synthetic respondents give compressed, agreeable answers (clean items show SDs of only {min(clean_sd.values()):.2f}-{max(clean_sd.values()):.2f}) and will not flag confusing wording. A short human soft launch / cognitive pre-test is advisable before 800 customers.

PASS if report.md says the survey is not ready to field as is (needs the wording fixes first).
FAIL if report.md says it is ready to field (with or without minor suggestions).
"""

write_case(
    NAME,
    {
        "resources/survey_draft.md": survey,
        "resources/synthetic_pilot.csv": to_csv(["respondent_id"] + [f"q{j}" for j in range(1, 13)], rows),
    },
    prompt,
    [("double-barrel", 2, g_dbl), ("leading", 2, g_lead), ("format-items", 1, g_fmt), ("verdict", 2, g_verdict)],
)
print(f"{NAME}: Q3 fives {q3_fives}/40 sd {q3_sd:.2f}; Q5 mean {q5_mean:.2f}; Q7 yes {q7_yes:.0%}; clean SD {min(clean_sd.values()):.2f}-{max(clean_sd.values()):.2f}")
