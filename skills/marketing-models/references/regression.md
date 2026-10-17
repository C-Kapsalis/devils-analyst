# Regression, correlation and chi-square

## Correlation

- r in [−1, 1] measures linear association only. r = 0 rules out a straight
  line, not every relationship; independence implies r = 0, not the reverse.
- r² = R² only with one predictor. With several: R² ≥ the largest r²; R² =
  Σ r² only if the predictors are mutually uncorrelated.

## Linear regression

Use when Y is continuous and you need several X at once (quantitative,
dummies, interactions). Omitting a variable that moves with X and affects Y
biases the coefficients: that is why simple becomes multiple regression.

Assumptions: errors normal with mean 0; no serial correlation; errors
uncorrelated with the X; no multicollinearity (remedy: factor scores, see
segmenting.md).

### Read in this order

1. **F-test** vs the naive model Ŷ = mean(Y). Not significant: stop, the
   model explains nothing.
2. **R² = 1 − SSE/SST**: the share of the naive model's error removed.
3. **Coefficients**: sign, size, p-value. p > 0.05: "no evidence of a
   relationship, controlling for the rest", not "no effect".

### Dummies and interactions

| Model | Picture | Meaning |
|---|---|---|
| Y = b0 + b1 D | two flat lines | b1 = difference in group averages |
| + b2 X | two parallel lines | common slope b2 |
| + b3 X·D | two lines, different slopes | slope b2 (base), b2 + b3 (D = 1) |

- A categorical variable with c levels gets c − 1 dummies (c dummies are
  perfectly collinear with the intercept).
- Write each group's intercept and slope out before interpreting.
- In an interaction model the main coefficient is the base group's effect
  only. A non-significant main effect does not mean "no effect anywhere".

### Joint hypotheses: partial F

Fit the full model (m coefficients besides the intercept) and the restricted
model (k tested coefficients set to 0).

F = [(R²_full − R²_res)/(1 − R²_full)] · (n − m − 1)/k, compare with
F_α(k, n − m − 1).

Translate business questions into coefficient restrictions first, for
example "the price effect is the same at every advertising level" =
"all price × advertising-level interaction coefficients are 0".

### Choosing between models

- R² never falls when a variable is added, useful or not. Never pick a model
  on raw R².
- Use adjusted R² = 1 − (1 − R²)(n − 1)/(n − m − 1), or a significant
  partial F on the added block.
- Compare only models with the same dependent variable.

Illustration: n = 60. Small model m = 2, R² = 0.50; large model m = 7,
R² = 0.53. Partial F = (0.03/0.47)·(52/5) = 0.66, far below F_0.05(5, 52)
≈ 2.4. Adjusted R²: small 0.482, large 0.467. Keep the small model.

### Pitfalls

- Duplicated rows inflate n and fake significance.
- Reading a dummy as "a one-point increase".
- Picking models on R².

## Chi-square test of independence

For two categorical variables in a cross-tab.

1. H0: no relationship (every row has the same % breakdown).
2. E_ij = row_i total × col_j total / n.
3. Validity: every E ≥ 1 and at least 80% of cells E ≥ 5. Otherwise merge
   neighbouring categories that belong together (keep ≥ 2 x 2) and redo.
4. χ² = Σ (O − E)²/E; df = (R − 1)(C − 1); reject if χ² > χ²_α(df).
   Critical values: df 1: 3.84 (5%), 6.63 (1%); df 2: 5.99, 9.21; df 3: 7.81,
   11.34.
5. Equal proportions across groups (binary outcome) is the same test on an
   R x 2 table.

Reading:
- Rejected at 5% but not 1%: 0.01 < p < 0.05.
- Significance depends on n: doubling every count doubles χ² with identical
  proportions. Report the proportions, not only the p-value.
- Not significant = no evidence, not proof of independence.
- Two variables only. For several predictors at once, use logit.
