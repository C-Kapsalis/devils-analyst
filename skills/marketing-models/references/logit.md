# Logit: predicting, classifying, ranking

## Binary logit

I = b0 + b1 X1 + ... + bm Xm; P(Y=1) = 1/(1 + e^{−I}); odds R = e^I;
P(Y=1) = R/(R + 1).

| I | P(Y=1) | R |
|---|---|---|
| 0 | 0.5 | 1 |
| > 0 | > 0.5 | > 1 |
| < 0 | < 0.5 | < 1 |

- Fitted by maximum likelihood; rows must be independent cases.
- Naive model: b0 = ln(p/(1 − p)), p = sample share of Y = 1.
- Two cases have the same probability iff they have the same I. Trade-off
  between predictors: Δ X1 equivalent to a dummy = b_dummy / b1.
- b_j changes log-odds by b_j; odds multiply by e^{b_j}. Several changes:
  R' = R · e^{Σ ΔX_j b_j}. The probability change depends on the starting
  point (S-curve), so never read b_j as a probability change.
- Logit separates cases better at the extremes; probit around the mean.

### Testing

Software reports deviance = −2 ln L (null deviance = naive model).

LR = deviance_restricted − deviance_full (always ≥ 0), compare with
χ²_α(k), k = coefficients set to 0. Whole model vs naive: use the null
deviance, k = m. ln L is not comparable across samples of different size;
use LR tests or lift.

## Classifying a case: the cost rule

1. Say in words what "assign to 1" and "assign to 0" mean as actions
   (send the offer / do not; call the lead / skip).
2. Costs: C(1|0) = cost of acting on a case that is truly 0; C(0|1) = cost
   of not acting on a case that is truly 1.
3. Assign 1 iff P(Y=0)·C(1|0) ≤ P(Y=1)·C(0|1), equivalently R ≥ c with
   c = C(1|0)/C(0|1), equivalently P(Y=1) ≥ c/(1 + c).
4. Sensitivity: the most a wrong "1" can cost and still justify acting is
   C(1|0) ≤ R·C(0|1).

A default 0.5 cut-off assumes the two errors cost the same. A cheap action
against an expensive miss pushes the threshold far below 0.5.

Illustration: retention credit $10; a churner who would be saved by it is
worth $90 of margin. c = 10/90 = 0.111; threshold P ≥ 0.111/1.111 = 0.10.
Every customer above a 10% churn probability gets the credit, not only those
above 50%. If the credit saves only some churners, C(0|1) is the expected
margin saved (save rate × margin).

## Is the model good enough to target with: the lift curve

1. Score every case (Î), sort from highest to lowest.
2. At each rank i: n1 = actual 1s among the top i; n2 = i × base rate (random
   picking).
3. Plot both. The ideal curve rises with slope 1 until all positives are in,
   then is flat. The closer n1 sits to it, and the farther above n2, the more
   the model is worth for targeting.

Report: "In the top __ ranked cases the model finds __ actual positives vs
__ by chance."

## Multinomial logit (more than two outcomes)

- Base outcome I_1 = 0; one indicator per other outcome with its own
  coefficients.
- P_1 = 1/(1 + Σ_{k≥2} e^{I_k}); P_j = e^{I_j}/(1 + Σ_{k≥2} e^{I_k}).
- Typical use: predicted brand shares by segment (evaluate each segment
  profile). Keep the minus signs in the exponents.
- "Does variable Z matter at all?": all of Z's coefficients across the
  non-base equations are 0, LR test with k = number of outcomes − 1.

## Pitfalls

- Assigning by P > 0.5 by default.
- Reading b as a probability change.
- LR statistic with the sign flipped.
- Repeated rows for related people (dependent observations).
