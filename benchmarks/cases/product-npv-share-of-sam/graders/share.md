---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Contribution per unit = $140 - $70 = $70. Break-even volume = $1.2M / $70 = 17,143 units a year = 10.7% of the 160,000-unit serviceable market (SAM). The plan assumes 30,000, 32,000, 34,000 units in years 2-4 = 18.8%, 20.0%, 21.2% of SAM, for a new entrant with 8% brand awareness against 6 competitors (a realistic new-entrant share is more like 1-5%). At 5% of SAM (8,000 units a year) NPV is about $-2,819,584; at 10% about $-1,507,017; NPV only turns positive above about 25,185 units a year (15.7% of SAM).
Naive wrong answer: "NPV +$1.1M > 0, go."

PASS if report.md computes the break-even volume (about 17,143 units, about 11% of SAM) or the plan's implied share of SAM (about 19-21%), says this exceeds what a new entrant can realistically capture, AND therefore does not recommend an unconditional go (conditional go with a pilot and kill criteria, rework the cost base, or no-go are all acceptable).
FAIL if it recommends going ahead on the positive NPV without testing the market share the plan requires.
