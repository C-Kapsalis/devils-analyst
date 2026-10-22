# product-npv-share-of-sam

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/product-decisions/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/product-npv-share-of-sam/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> Board meeting Thursday. resources/ has the cash-flow plan for the Ridgeline e-bike battery pack (cashflow_plan.csv, quarterly, 4 years), unit economics (unit_economics.csv) and the market study (market.csv). We've already put $1.4M into development. Hurdle rate is 10%. Should we go ahead? Write report.md with your recommendation.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `npv` | PASS | PASS | both +1.10M forward, sunk 1.4M excluded |
| `share` | PASS | PASS | A: no-go, 18.75-21.25% of SAM vs 1-5% realistic; B: staged release tied to demand evidence, flags 18-21% share from 8% awareness (borderline: conditional go) |

## Arm A answer (with skill)

````markdown
# Ridgeline e-bike battery pack: go or no-go on the remaining funding

Verdict: no-go on the plan as written. Do not release the remaining $1.4M on this plan. Re-scope it (a pivot or a much smaller test) unless someone shows evidence for a share of about 16% of SAM or more.

Number that decides it: the plan's NPV is +$1.10M at 10%, but only because it sells 18.75% to 21.25% of SAM. At 5% of SAM, the realistic early share, NPV is -$2.82M. Break-even volume is 10.7% of SAM, and NPV reaches zero only at about 15.7% of SAM.

Decision: whether to spend the remaining $1.4M (2027-Q1 to 2027-Q4) and then run the 2028-2030 plan, at a 10% hurdle. The $1.4M already spent (2025-Q1 to 2026-Q4) is sunk and excluded.

Inputs (resources/):
- cashflow_plan.csv: quarterly 2027-Q1 to 2030-Q4. Remaining development and launch -$350,000 per quarter for 4 quarters. From 2028-Q1, units 7,500 / 8,000 / 8,500 per quarter (30,000 / 32,000 / 34,000 per year). Net cash flow +$225k / +$260k / +$295k per quarter.
- unit_economics.csv: price $140, variable cost $70 (contribution $70), fixed costs $1.2M per year ($300k per quarter).
- market.csv: SAM 160,000 units per year, 6 competitors, our awareness 8% (2026 tracker), leader share 31%.
- Every plan row ties out (e.g. 7,500 x $140 = $1,050,000; 7,500 x $70 = $525,000; net $225,000).

Method: quarterly rate r_q = 1.10^(1/4) - 1 = 2.411%. Each quarter discounted at its quarter_index t (2027-Q1 = t1), end of period, per the file layout. NPV = sum CF_t / (1 + r_q)^t, future cash only. BEQ = 1,200,000 / 70 = 17,143 units per year. Share = units / 160,000.

Results:
- Plan as written (30,000-34,000 units/yr, 18.75%-21.25% of SAM): NPV +$1.10M at 10%; +$0.87M at 15%.
- Realistic early share, 5% of SAM (8,000 units/yr, 2,000 per quarter): NPV -$2.82M at 10%. Each quarter from 2028-Q1 is 2,000 x $70 - $300,000 = -$160,000.
- NPV zero point (constant volume, plan fixed costs): about 25,200 units/yr, about 15.7% of SAM.
- Plan NPV build at 10%: PV of development -$1,319,505; PV of 2028-2030 inflows +$2,416,800; NPV +$1,097,295. The 5% case: PV of 2028-2030 -$1,500,076; NPV -$2,819,581.

Break-even checks:
- BEQ 17,143 units/yr = 10.7% of SAM. The 5% early ceiling is 8,000 units/yr, so BEQ is about 2.1 times above it. At the ceiling the plan never breaks even (2,000 per quarter vs 4,286 quarterly BEQ).
- Price -10% (to $126): contribution $56, BEQ 21,429 units = 13.4% of SAM.
- Cost +20% (variable to $84): contribution $56, BEQ 21,429 units = 13.4% of SAM.
- Market in dollars: SAM = 160,000 x $140 = $22.4M per year. Plan 2028 revenue $4.2M = 18.75% of that.

Why the share is the problem:
- Plan 2028 volume (30,000 units/yr) is about 60% of the leader's current SAM volume (31% x 160,000 = 49,600). That makes us a top-tier seller in year one with 8% awareness.
- NPV zero needs about 16% of SAM. The business-case rule is 1-5% of SAM for years 1-3; above 5% early signals an unrealistic plan.
- No demand data was given (no concept test, intent or conversion). The go test requires validated demand, so the share assumption is untested, not just high.

Adversary checks:
- Sunk cost: excluded; the answer is about the next $1.4M plus operations.
- Rate: plan NPV positive at both 10% and 15%; the sign depends on volume, not the rate.
- Market size: only SAM given; no TAM or bottom-up cross-check.
- Fixed costs: held at $1.2M/yr in the 5% case. If they can fall with volume, the 5% NPV improves; not tested because no such plan was given.

Recommendation:
1. Do not release the remaining $1.4M on the current plan.
2. Ask the team for evidence behind 18-21% of SAM (minimum about 16% for NPV zero). Awareness is 8%, so the path from 8% awareness to that share needs explaining.
3. If the team wants an option, fund a small time-boxed test (limited channel or retailer pilot) with a measured sell-through target and pre-set kill conditions, e.g. reaching 2,000 units per quarter (the 5% share) by a set date; stop if missed.
4. Ask for a lower-fixed-cost version. Re-run NPV only if fixed costs can fall to match a 5% share.

Caveats and open questions for the board:
- Target segment and channel plan are not in the data.
- Fixed-cost behaviour at lower volume is unknown.
- No TAM or demand research was provided.
- Discounting convention (end of quarter, t1 = 2027-Q1) is an assumption from the file layout; a one-quarter shift changes NPV by about 2%.
- Pursuing a 15%+ share versus pivoting is the board's decision.
````

## Arm B answer (without skill)

````markdown
# Ridgeline e-bike battery pack: go / no-go

## Recommendation

Go ahead with the remaining development, but release the remaining $1.4M in stages tied to demand evidence. On the plan's own numbers, the forward investment clears the 10% hurdle with room to spare. The case depends on volume: it reaches zero NPV if units come in about 21% below plan.

## The numbers

- **Sunk:** $1.4M spent on development in 2025-Q1 to 2026-Q4. It is excluded from the decision because it cannot be recovered.
- **Forward NPV at 10%:** +$1.10M over the plan horizon (2027-Q1 to 2030-Q4).
- **IRR on forward cash flows:** about 50%.
- **Payback:** undiscounted during 2029-Q2; discounted during 2029-Q3.
- **Including the $1.4M already spent:** NPV is -$0.30M. The board should see both figures. The forward figure answers "go ahead"; the all-in figure shows what the project has cost to reach this point.
- **No terminal value.** Each further year at the 2030 run-rate ($1.18M a year of net cash) would add about $0.73M of PV, so the answer does not rest on the plan's end date.

| Year | Units | Revenue | Forward net cash | PV at 10% |
|---|---|---|---|---|
| 2027 | 0 | $0 | -$1.40M | -$1.32M |
| 2028 | 30,000 | $4.20M | +$0.90M | +$0.77M |
| 2029 | 32,000 | $4.48M | +$1.04M | +$0.81M |
| 2030 | 34,000 | $4.76M | +$1.18M | +$0.84M |
| **Total** | | | **+$1.72M** | **+$1.10M** |

Unit economics: $140 price, $70 variable cost, so $70 contribution per unit (50%). Fixed costs of $1.2M a year break even at 17,143 units a year, about 10.7% of the SAM.

## Where the case is fragile

- **Market share (the main risk).** The plan needs 18.75% of the 160,000-unit SAM in 2028, rising to 21.25% by 2030. The market study puts the leader at 31% across six competitors, and our brand awareness is 8% (2026 tracker). The plan therefore assumes we reach a position close to the leader's within two to three years, from 8% awareness. Test this first.
- **Volume cushion.** NPV falls to zero at about 79% of plan volume, roughly 24,000 units in 2028 instead of 30,000. At 20% below plan, NPV is still about +$0.05M, which is effectively on the line.
- **Flat price and cost.** The plan holds the $140 price and $70 variable cost for four years. It assumes no price erosion, no cost inflation and no learning-curve gains.
- **Flat market.** The SAM is held at 160,000 units with no growth. It is a single 2026 figure.
- **No launch slip.** Revenue starts in 2028-Q1, straight after the last development spend. No delay is modelled.
- **Development cost.** The remaining $1.4M is a plan figure, not a quote. No overrun is modelled.

## Before releasing the next tranche

1. Evidence that we can reach 18-21% share in our channels, given the leader's 31% and our 8% awareness.
2. Confirmation of the $140 price and $70 variable cost with retailers and suppliers.
3. A cost-to-complete estimate for development, and a launch date.

Suggested gate: release the 2027 spend quarter by quarter. Staying above the hurdle needs about 24,000 units in 2028.

## Method and checks

- Sources: `cashflow_plan.csv`, `unit_economics.csv` and `market.csv` in `resources/`.
- Consistency checks passed: revenue equals units times $140 in every quarter; variable cost equals units times $70; fixed cost is $300k a quarter, which is $1.2M a year and matches `unit_economics.csv`; net cash flow equals revenue less variable cost, fixed cost and development in every row.
- Discounting: an effective 10% a year, compounded quarterly. Quarter 1 is 2027-Q1, discounted at 1.10^(-1/4), with cash at quarter end. The valuation date is the start of 2027.
- All arithmetic was done by hand and rounded, so expect small rounding differences.
````
