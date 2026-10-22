---
name: marketing-models
description: >-
  Use this skill when a marketer asks a question that needs a model, not just a
  metric: "what price should we charge", "are we underpriced", "what will sales be
  next month or next quarter", "is the business really growing under the seasonality",
  "how fast will unit cost fall as we scale", "what drives sales", "which regression
  should we trust", "does the effect differ by group", "who should get the retention
  offer", "which customers will churn or convert", "is the churn model any good",
  "segment our customers", "what do our survey ratings boil down to", "are these two
  things related", "is this investment worth it", "how much can we pay to acquire a
  customer". Picks the method (NPV and CLV, elasticity, forecasting, regression,
  chi-square, logit, factor and cluster analysis), runs it with exact formulas, checks
  it, and turns the numbers into a decision. Did a change cause a result: use
  evidence-check. Defining a metric: metric-definitions. Survey design:
  research-design.
---

# marketing-models

A right number can still lead to the wrong decision. This skill picks the
model that fits the question, runs it in code, and reads it the way the
decision needs: profit not revenue, cost-weighted thresholds not 0.5, fit
judged against a naive baseline, effects tested before they are sized.

Two rules run through every method:

- **Beat the naive baseline.** R² compares with the mean, the logit
  likelihood-ratio test with the intercept-only model, the lift curve with
  random picking. A model that does not beat its baseline says nothing.
- **Significance before size.** Test that an effect exists (F, chi-square,
  likelihood ratio, t) before you interpret how big it is.

## 0. What the human owns

The question and the decision are the user's. Before modelling, ask (do not
assume) what is unknown here:

| Ask | Why |
|---|---|
| What decision rides on this, and what does each kind of mistake cost? | Sets the classification threshold and the price objective (profit, not revenue) |
| Unit variable cost or margin per unit? | Price and CLV decisions are wrong without it |
| Discount rate and horizon? | NPV, IRR and CLV depend on both |
| Length of the seasonal cycle? | Sets the moving-average order |

If the user cannot answer, state the assumption you used and show how the
answer changes if it is wrong.

## 1. Pick the method

| The question | Dependent variable / data | Method | Reference |
|---|---|---|---|
| Is this investment worth it? Max acquisition cost? Minimum retention? | Cash flows over time | NPV, IRR, CLV | [valuing.md](references/valuing.md) |
| Is the price too high or too low? Best price? | Price, quantity, unit cost | Elasticity, PV ratio, P* | the `pricing-promotions` skill owns price and promotion decisions (promo controls, stock-up around price changes, test steps); use [pricing.md](references/pricing.md) only for the model fit itself |
| Next period's sales; trend under seasonality | Time series | Moving average of order = cycle | [forecasting.md](references/forecasting.md) |
| Constant % growth or decay (new product revenue, awareness after ads stop) | Series over time | Exponential, ln Y on t | [forecasting.md](references/forecasting.md) |
| Unit cost vs cumulative volume; constant elasticity demand | Two variables, % to % | Power model, ln Y on ln X | [forecasting.md](references/forecasting.md) |
| What drives a quantity? Does the effect differ by group? | Continuous Y | Linear regression, dummies, interactions, partial F | [regression.md](references/regression.md) |
| Are two categorical variables related? Equal rates across groups? | Cross-tab of counts | Chi-square | [regression.md](references/regression.md) |
| Will this case be 1 or 0, and what do we do? | Binary Y | Binary logit + cost-based classification + lift | [logit.md](references/logit.md) |
| Which of 3+ options will each segment choose? | Choice among >2 | Multinomial logit | [logit.md](references/logit.md) |
| Many correlated ratings; who belongs together | Ratings or part-worths per respondent | Factor analysis, then K-means on factor scores | [segmenting.md](references/segmenting.md) |
| Did B beat A? Did the change work? | Experiment or before/after | Not here: **evidence-check** | |

Several categorical predictors at once: logit, not a stack of chi-square
tests (separate cross-tabs can each look significant and vanish together).

## 2. Check the data before fitting

| Method | The data must contain | Refuse or caveat when |
|---|---|---|
| Pricing | Price, units at each price, unit variable cost | No variable cost: give elasticity only, no price advice |
| NPV / CLV | Cash flow per period (margin, not revenue), discount rate, retention | Revenue given instead of margin: say CLV is overstated |
| Moving average | At least 2 full cycles; cycle length | Fewer than n points: no MA exists yet (first MA at t = n) |
| Regression | n well above the number of coefficients; no duplicated rows | Duplicated rows inflate n and shrink standard errors |
| Chi-square | Counts (not percentages) per cell | Any expected count < 1, or < 80% of cells with expected ≥ 5 |
| Logit | One row per independent case; both outcomes present | Rows for related people repeated: likelihood assumption broken |
| Factor / cluster | Respondent x item matrix, items on comparable scales | Raw correlated items fed straight into K-means |

## 3. Run it: exact formulas

| Need | Formula |
|---|---|
| NPV | Σ V_t / (1 + I)^t |
| IRR | I such that Σ V_t / (1 + I)^t = 0 (exists, unique and positive only if V_0 < 0, later V_t > 0 and their sum > abs(V_0)) |
| CLV | Σ V_t R^t / (1 + I)^t − AQ = Σ V_t / (1 + ρ)^t − AQ, with ρ = (1 + I − R) / R. Use one form, never both |
| Max acquisition cost | AQ_max = Σ V_t R^t / (1 + I)^t |
| Minimum retention | R_min = (1 + I) / (1 + IRR), IRR of (−AQ, V_1..V_T) |
| Elasticity (two points) | ε = (ΔQ/Q) / (ΔP/P); E = abs(ε). Many points: slope of ln Q on ln P |
| PV ratio | PV = (P − VC) / P; a 1% price rise adds 1/PV % to unit margin and costs E % of volume |
| Optimal price | Constant elasticity, E > 1: P* = VC · E / (E − 1). Linear Q = A − BP: P* = A/(2B) + VC/2 |
| Moving average | MA_t = (X_t + ... + X_{t−n+1}) / n, n = cycle length; MA_t forecasts t+1; MA_t − MA_{t−1} = trend per period |
| Exponential | ln Y = ln A + b t; % change per period = e^b − 1 |
| Power / experience | ln Y = ln A − a ln X; cost after a doubling = 2^−a of before; a = −log2(learning rate); C = C_0 (Q/Q_0)^−a |
| R², adjusted R² | R² = 1 − SSE/SST; adj = 1 − (1 − R²)(n − 1)/(n − m − 1) |
| Partial F | F = [(R²_full − R²_restricted) / (1 − R²_full)] · (n − m − 1)/k vs F_α(k, n − m − 1) |
| Chi-square | E_ij = row_i · col_j / n; χ² = Σ (O − E)²/E; df = (R − 1)(C − 1) |
| Logit | I = b_0 + Σ b_j X_j; P(Y=1) = 1/(1 + e^−I); odds R = e^I; +1 unit of X_j multiplies odds by e^{b_j} |
| LR test | deviance_restricted − deviance_full vs χ²_α(k) |
| Classify | Assign 1 iff R ≥ c, c = C(1\|0)/C(0\|1); equivalently P(Y=1) ≥ c/(1 + c) |
| Multinomial | I_1 = 0; P_j = e^{I_j} / (1 + Σ_{k≥2} e^{I_k}) |
| Factors kept | Eigenvalue ≥ 1; variance explained = Σ kept eigenvalues / m; item belongs to a factor if abs(loading) ≥ 0.5 |
| K-means | Minimise Σ WCSS; choose K at the elbow of total WCSS vs K |

Compute in code. Show the table of inputs so the reader can redo it.

## 4. Decision rules

| Situation | Rule |
|---|---|
| Price | 1/PV < E: overpriced, cut. 1/PV > E: underpriced, raise. Equal: optimal. E < 1: raising price always raises profit |
| Elastic demand (E > 1) | Says revenue falls with price, **not** that profit falls. Decide on 1/PV vs E |
| Price move size | The 1/PV vs E test is local (about 1%). Move a step, re-measure E, repeat. Do not jump to P* far outside observed prices |
| Investment | Invest iff NPV ≥ 0; choose the highest NPV; customer: invest iff ρ ≤ IRR |
| Forecast with seasonality | MA order must equal the cycle; any other order leaves seasonality in |
| Model choice | Same Y only. Higher adjusted R², or a significant partial F for the added block. Never raw R² |
| Reading a regression | F-test first (stop if not significant), then R², then each coefficient |
| Dummy coefficient | A difference in group averages vs the base level, not "a one-point increase" |
| Interaction model | The main-effect coefficient is the effect for the base group only. Effect in group g = main + interaction |
| Classification | Threshold from costs, not 0.5. 0.5 assumes both errors cost the same |
| Logit coefficient | Changes log-odds; the probability effect depends on where the case sits on the S-curve |
| Model usefulness for targeting | Lift curve: actual positives in the top i ranked vs i · base rate; closer to the "all positives first" curve is better |
| Chi-square not significant | No evidence of a relationship, not evidence of none. Significance grows with n (double the counts, double χ²) |
| Segments | Factor analysis first, K-means on factor scores; factor scores are standardised, so 0 = average, not "none" |

## 5. Write the answer

```
Verdict: [decision in one line]
Deciding number: [the figure and the test that decides it]
Naive read and why it is wrong: [one line]
Action: [what to do now] · How to verify: [the test, data or re-measurement that confirms it]
Assumptions: [costs, rates, cycle length used, and what flips the decision]
```

## 6. Adversary for every move

Each step gets attacked before it stands. Run the check; if it fails, do the
fix before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Frame the decision | "Is this the user's decision, or one I invented?" | The decision and the error costs come from the user or are stated as assumptions | Ask the user; do not model yet |
| Pick the method | "Does the method match the type of Y?" | Section 1 table: continuous → regression, binary → logit, >2 → multinomial, two categoricals → chi-square | Switch method |
| Pick the method | "Is this really a causal question?" | Wording like "did it work", "caused", "after we changed" | Hand to evidence-check |
| Load the data | "Margin or revenue? Units or currency?" | Column definitions; VC or margin present | Ask for cost; caveat or stop the price/CLV advice |
| Fit the model | "Does it beat the naive baseline?" | F-test, LR test vs null deviance, or lift vs random | Report "no evidence the model helps"; stop |
| Size the effect | "Is the effect significant before I size it?" | p-value or test statistic vs critical value | Report as not established |
| Chi-square | "Is the table valid?" | All E ≥ 1 and ≥ 80% of E ≥ 5 | Merge neighbouring categories (keep ≥ 2x2), recompute |
| Choose a model | "Did fit rise only because I added variables?" | Adjusted R² and partial F on the added block | Keep the smaller model |
| Interaction | "Am I reading the base-group effect as the effect for all?" | Write each group's effect = main + interaction | Recompute per group |
| Price advice | "Am I deciding on revenue instead of profit?" | Contribution (P − VC) · Q at each price; 1/PV vs E | Redo on contribution |
| Price advice | "Is P* an extrapolation?" | P* inside or near the tested price range | Recommend a step and a re-test instead |
| Forecast | "Is seasonality leaking into the trend?" | MA order = cycle length; compare same season | Refit with order = cycle |
| Exponential fit | "Did I report b as the % change?" | % change = e^b − 1 | Correct it |
| CLV / NPV | "Did I count churn twice or use revenue?" | Only one of R^t or ρ; V_t is margin | Recompute |
| IRR | "Does a positive IRR even exist?" | Outflow first, inflows sum > outflow | Report NPV only |
| Classification | "Why this threshold?" | c = C(1\|0)/C(0\|1) from stated costs; threshold P ≥ c/(1 + c) | Recompute; show who changes group |
| Segments | "Are clusters built on duplicated items?" | Factors with eigenvalue ≥ 1, varimax, K from the elbow | Refit on factor scores |
| Recommend | "What does it cost if this is wrong, and what would the CFO ask?" | Downside in money and a way to verify (test, holdout, re-measure) | Add the test or shrink the bet |

## 7. Score-and-probe gate before handover

1. Confirm every adversary check above passed (or its fix was applied).
   Any open failure: fix it first; do not score.
2. Score the draft 0 to 100 on four dimensions (the moderation rubric of the
   user's hybrid-research notes):
   - **Clarity**: one reading gives the verdict, number and action.
   - **Relevance**: answers the user's decision, not a neighbouring one.
   - **Depth**: shows the deciding calculation and its assumptions.
   - **Insightfulness**: says what the naive read misses and what flips the decision.
3. Any score below 80: write the probe question that would raise it (for
   example "what happens to the decision if variable cost is 10% higher?"),
   answer it from the data, revise, and re-score. At most 2 loops; then hand
   over and name what is still weak.
