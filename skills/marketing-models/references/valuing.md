# Valuing investments and customers: NPV, IRR, CLV

Metric definitions of CLV, CLV:CAC and payback live in metric-definitions
(catalog "Customer value"). This file covers the decision method.

## NPV

Put alternatives whose payoffs arrive at different times on one basis:
today's money.

1. List periods t and cash flows V_t (outflows negative). Say whether the
   investment sits at t = 0 or t = 1.
2. Discount factor 1/(1 + I)^t; keep 4+ decimals (rounded factors drift on
   large flows).
3. NPV = Σ V_t/(1 + I)^t. Invest iff NPV ≥ 0; between options, highest NPV.

## IRR

The compound rate at which NPV = 0: the highest rate at which the investment
still breaks even.

- Check existence first: the first flow is the outflow, later flows are
  inflows, and the inflows add up to more than the outflow. If the inflows
  sum to less, NPV is negative at every non-negative rate: no positive IRR,
  report NPV only.
- Solve numerically (bisection or a spreadsheet goal seek).

## CLV: NPV with churn risk

A customer's future margin arrives only if the customer is still active.

| Term | Meaning |
|---|---|
| R | retention: probability an active customer is active next period |
| R^t | survival to period t |
| V_t R^t | expected cash flow in t |
| ρ = (1 + I − R)/R | discount rate that adds churn risk to the time value of money; ρ = I when R = 1 |

CLV = Σ V_t R^t/(1 + I)^t − AQ = Σ V_t/(1 + ρ)^t − AQ.

Pitfalls:
- Discounting V_t R^t at ρ counts churn twice. Use one form.
- V_t must be margin (contribution), not revenue.
- AQ sits at t = 0 and is outside the sum.

Decision thresholds:

| Question | Answer |
|---|---|
| Most we can pay to acquire | AQ_max = Σ V_t R^t/(1 + I)^t (CLV = 0) |
| Is acquiring worth it | ρ < IRR of (−AQ, V_1..V_T): yes; ρ = IRR: indifferent; ρ > IRR: no |
| Minimum retention | R_min = (1 + I)/(1 + IRR) |

Levers (each ceteris paribus): higher AQ or higher I lower CLV; higher R
raises it.

### Worked method (illustrative numbers)

Margin $60 a year while active, R = 0.8, I = 0.05, 3-year horizon.
ρ = (1.05 − 0.8)/0.8 = 0.3125.
PVs: 60/1.3125 = 45.71; 60/1.3125² = 34.83; 60/1.3125³ = 26.54. Sum = 107.08.
AQ_max ≈ $107. At AQ = $90, CLV = $17; IRR of (−90, 60, 60, 60) ≈ 44.6%,
so R_min = 1.05/1.446 ≈ 0.726. Current R = 0.8 clears it.

## Write-up lines

- "At I = __, the NPV is $__; [invest / do not invest]."
- "With retention __ and rate __, ρ = __; future margin is worth $__, so
  acquisition can cost at most $__."
- "IRR of the customer's flows is __%; the investment holds for retention of
  at least (1 + I)/(1 + IRR) = __."
