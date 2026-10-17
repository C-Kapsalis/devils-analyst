# marketing-models: rule → source note

Paths are relative to ~/Documents/tost/. "MA/" =
Brain Knowledge/Marketing Analytics Brain Knowledge/; "pMA/" = Brain
Knowledge/practice_Marketing Analytics/; "MR/" = Brain Knowledge/Marketing
Research Brain Knowledge/. Worked examples in the skill are new numbers, not
the notes' examples.

| Rule in the skill | Source |
|---|---|
| Beat the naive baseline; significance before size | theoretical brains/Marketing Analytics Brain.md ("Marketing analytics at a glance") |
| Method map by question and type of Y | theoretical brains/Marketing Analytics Brain.md (Method map); practical brains/practice_Marketing Analytics.md |
| Several categorical predictors → logit, cross-tabs mislead jointly | MA/MA - Chi-Square Test of Independence.md (Limitation → logit) |
| Human owns question and decision; ask, do not assume; score-and-probe gate on clarity, relevance, depth, insightfulness, threshold 80 | Brain Knowledge/Digital Marketing Brain Knowledge/ai-human-hybrid-marketing-research.md (stages 1-2 human-led; self-moderation scoring) |
| NPV, discount factor, invest iff NPV ≥ 0, highest NPV | MA/MA - NPV and IRR.md; pMA/practice MA - Valuing Customers and Investments.md |
| IRR existence condition | MA/MA - NPV and IRR.md (Existence condition) |
| CLV with R^t or ρ = (1+I−R)/R; never both | MA/MA - Customer Lifetime Value.md; pMA/practice MA - Valuing Customers and Investments.md (Pitfalls) |
| AQ_max, ρ vs IRR, R_min = (1+I)/(1+IRR), comparative statics | MA/MA - Customer Lifetime Value.md |
| V_t must be margin | MR/Customer Lifetime Value.md (m = contribution margin) |
| Elasticity (arc and log-log), baseline demand, premium positioning | MA/MA - Price Elasticity and Optimal Price.md |
| PV ratio, 1/PV vs E table, E < 1 always raise | MA/MA - Price Elasticity and Optimal Price.md; pMA/practice MA - Pricing from Elasticity.md |
| P* = VC·E/(E−1) (E > 1), linear P* = A/2B + VC/2, FC does not affect P* | same two notes |
| 1/PV vs E is local; recompute E after large changes | pMA/practice MA - Pricing from Elasticity.md (Pitfalls) |
| E must come from comparable conditions, not a correlation | MR/MR - Causality and Experiment Notation.md (correlations insufficient) |
| MA order = cycle length, first MA at t = n, MA_t forecasts t+1, MA difference = trend | MA/MA - Moving Average and Exponential Models.md; pMA/practice MA - Forecasting Trends and Costs.md |
| Exponential: ln Y on t, % change = e^b − 1 | same two notes |
| Power model, experience curve, a = −log2(learning rate), anchored form, C is marginal cost | MA/MA - Power Model and Experience Curve.md; pMA/practice MA - Forecasting Trends and Costs.md |
| Seasonal index and deseasonalising (pointer) | MR/Temporal Demand Patterns.md |
| Correlation is linear only; r² vs R² rules | MA/MA - Correlation.md; MA/MA - Linear Regression.md (five rules) |
| Regression assumptions, omitted-variable bias | MA/MA - Linear Regression.md |
| Read F → R² → coefficients; p > 0.05 wording | MA/MA - AB Testing.md (Regression); pMA/practice MA - Building and Testing a Regression.md |
| Dummies, c − 1 dummies, interactions, group equations | MA/MA - Linear Regression.md; pMA/practice MA - Building and Testing a Regression.md |
| Main effect = base group only; launch where main + interaction > 0 | MA/MA - AB Testing.md (launch rule) |
| Partial F formula | MA/MA - Linear Regression.md (F-test nested models) |
| Never choose on R²; adjusted R²; same Y only | MA/MA - AB Testing.md (Model selection); pMA/practice MA - Building and Testing a Regression.md |
| Duplicated rows inflate n | pMA/practice MA - Building and Testing a Regression.md (Pitfalls) |
| Chi-square steps, validity (E ≥ 1, 80% ≥ 5), merge categories, df, critical values | MA/MA - Chi-Square Test of Independence.md; pMA/practice MA - Testing Association with Chi-Square.md |
| Doubling counts doubles χ²; not significant ≠ independent | same two notes |
| Logit model, odds, I = 0 table, e^{b_j}, same I ⇒ same P | MA/MA - Binary Logit.md; MA/MA - Logit Classification and Lift.md |
| Naive logit b0 = ln(p/(1−p)); deviance; LR test; ln L not comparable | MA/MA - Binary Logit.md; MA/MA - Logit Classification and Lift.md |
| Logit vs probit | MA/MA - Binary Logit.md |
| Cost rule (four forms), threshold c/(1+c), max C(1\|0), 0.5 assumes equal costs | MA/MA - Logit Classification and Lift.md; pMA/practice MA - Predicting and Classifying with Logit.md |
| Lift curve steps and reading | MA/MA - Logit Classification and Lift.md |
| Multinomial logit, base outcome, shares by segment, LR test for a variable | MA/MA - Multinomial Logit.md |
| Independent rows assumption | MA/MA - Binary Logit.md (Estimation) |
| Factor analysis: eigenvalue ≥ 1, varimax, loadings ≥ 0.5, communality | MA/MA - Factor Analysis.md |
| Factor scores fix multicollinearity | MA/MA - Factor Analysis.md (Why: multicollinearity) |
| K-means steps, WCSS, elbow, heuristic depends on start | MA/MA - Cluster Analysis.md; pMA/practice MA - Segmenting Customers.md (Pitfalls) |
| Profiles read vs 0; follow-up regressions on factors | MA/MA - Cluster Analysis.md |
| Likert check: one dominant factor | MR/MR - Attitude Measurement.md; pMA/practice MA - Segmenting Customers.md |
| Conjoint segments: cluster on part-worths | MR/MR - Conjoint Analysis.md |
| Causal questions handed to evidence-check | MR/MR - Causality and Experiment Notation.md (experiments establish cause); MA/MA - AB Testing.md |
| Output format and adversary table, CFO question | Contract (scratchpad/skill-contract.md) and hybrid note: propose, validate, retry |
