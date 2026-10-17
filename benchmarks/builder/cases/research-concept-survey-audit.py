"""A draft concept survey with 7 planted design errors. Cheap reviews catch the
double-barrel and overlapping ranges but miss that the cover email names the
brand and concept, that aided awareness comes before unaided, and that the raw
Q6 yes share will overstate subscribers."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "research-concept-survey-audit"
survey = """# EcoFill customer survey - DRAFT v3

Audience: 5,000 customers from our CRM (bought in the last 12 months). Field: online, 1 week. Incentive: entry into a GBP 100 voucher draw.

## Invitation email

Subject: Help EcoFill shape its new refill subscription!

Hi {first_name},

We're getting ready to launch a refill subscription that saves you money and keeps plastic out of landfill, and we'd love your input. The survey takes about 6 minutes.

[Start the survey]

The EcoFill team

## Questions

**Q1. Which of these refill brands have you heard of?** (select all that apply)
- EcoFill
- Purely Refill
- GreenCap

**Q2. When you think of refill cleaning products, which brands come to mind?** (open text)

**Q3. How often do you buy cleaning products?**
- 0-2 times a month
- 2-4 times a month
- 4 or more times a month

**Q4. How satisfied are you with the price and scent of your current cleaner?**
- Very satisfied / Satisfied / Neither / Dissatisfied / Very dissatisfied

**Q5. Given how much plastic waste refills save, how interested are you in EcoFill's refill subscription?**
- Extremely interested / Very interested / Interested

**Q6. Would you subscribe to the EcoFill refill subscription at GBP 12 a month?**
- Yes
- No

**Q7. Anything else you'd like to tell us?** (open text)

## Analysis plan

- Forecast year-one subscribers = Q6 "Yes" share x 180,000 active customers.
- Report Q5 top-box as "interest in the concept".
"""
ERRORS = 7
assert survey.count("**Q") == 7 and "None of these" not in survey
print(f"{NAME}: {ERRORS} planted errors")

prompt = """
Before we send this to 5,000 customers, can you check our survey for the new EcoFill refill subscription? The draft is in resources/draft_survey.md. We'll use the yes share from Q6 to forecast subscribers. Write report.md with what to change.
"""
g_order = """
Two planted errors bias every later answer:
1. The invitation email (subject "Help EcoFill shape its new refill subscription!" and body text about the subscription saving money and plastic) names the brand and the concept before anyone answers. This sensitises respondents: brand awareness (Q1/Q2) and interest (Q5/Q6) will be inflated. Fix: neutral invitation that does not name the brand or the concept (e.g. "a short survey about household cleaning").
2. Q1 (aided list of brands, including EcoFill) is asked BEFORE Q2 (unaided "which brands come to mind"). Showing the list first contaminates the unaided answer. Fix: ask unaided (Q2) before aided (Q1).

PASS if report.md flags BOTH (a) the brand/concept named in the invitation email as biasing answers, AND (b) the aided-before-unaided order of Q1/Q2.
FAIL if either one is missed.
"""
g_fc = """
Ground truth: Q6 ("Would you subscribe? Yes/No") plus the plan "forecast = yes share x 180,000" will overstate subscribers badly. Stated purchase intent overstates behaviour (hypothetical money, politeness, sensitised and self-selected respondents), and a yes/no question has no gradation. Fix: use a graded purchase-likelihood scale (definitely / probably / might / probably not / definitely not) and apply calibration/deflation factors, and/or validate with a behavioural test (pre-order, waitlist with deposit, smoke test).

PASS if report.md says the Q6 yes share will overstate subscribers AND proposes deflating/calibrating it, a graded likelihood scale with calibration, or a behavioural test.
FAIL if it accepts the raw yes share as the forecast or only suggests rewording Q6.
"""
g_cov = """
The 7 planted errors (each needs a reasonable fix):
1. Invitation email names the brand and concept (sensitises respondents) -> neutral invite.
2. Aided awareness (Q1) before unaided (Q2) -> unaided first.
3. Q3 ranges overlap (0-2 / 2-4 / 4 or more: 2 and 4 fall in two options) -> mutually exclusive ranges (e.g. 0-1, 2-3, 4+), ideally including "never/less than monthly".
4. Q4 is double-barrelled (price AND scent in one question) -> split into two questions.
5. Q5 is leading and one-sided (premise "how much plastic waste refills save"; answer options are all positive, no "not interested") -> neutral wording and a balanced scale.
6. Q6 yes share used directly as the forecast -> graded scale, calibration/deflation or behavioural test.
7. Q1 has no "none of these" / "don't know" option -> add one.

PASS if report.md identifies at least 5 of the 7 errors with a sensible fix for each.
FAIL if it identifies 4 or fewer.
"""
write_case(NAME, {"resources/draft_survey.md": survey}, prompt,
           [("order-and-cover", 3, g_order), ("forecast-misuse", 2, g_fc), ("coverage", 1, g_cov)])
