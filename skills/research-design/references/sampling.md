# Sampling, sample size and inference

## Choosing the method

| You have | Method |
|---|---|
| No idea of the variance | Sequential: small pilot, estimate σ, add units until precise enough |
| A list, distinct subgroups that behave differently, a list per subgroup | Stratified (proportional; optimal if σ_h and costs known) |
| A list sortable by a continuous proxy, no cycles along it | Systematic: k = N/n, random start R, take R, R + k, ... |
| A list, nothing else | Simple random sampling |
| No list; a trait linked to the answer with known population % | Quota |
| No list; a sub-population judged typical (test-market city) | Judgement |
| No list; a rare group whose members know each other | Snowball |
| No list, nothing else | Convenience, after the bias test |

**Convenience-bias test.** Name the exact factor that made each person likely
to be included. If it relates to what you measure, the estimate is biased
(newsletter subscribers on "interest in our new line"; social followers on
"brand awareness"). If not, it can be fine.

Systematic sampling on a list where the quantity cycles with period k
captures one phase of the cycle: worse than random.

## Sample size

| Case | Formula |
|---|---|
| Mean, absolute error E | n ≥ (z_{α/2} σ/E)² |
| σ unknown, plausible range known | σ ≈ (high − low)/6 |
| Mean, relative error r (E = rμ) | n ≥ (z_{α/2}/r)² (σ/μ)²; borrow σ/μ from a proportional proxy |
| Proportion | n ≥ z²_{α/2} π(1 − π)/E²; π = 0.5 if no prior (safe, may overspend) |
| A total N·π or N·μ within ± NE | E = NE/N, then the formulas above |
| Back out n from a reported margin m | n = z²_{α/2} p(1 − p)/m² |

- Always round up.
- n ∝ 1/E². Halving the margin multiplies n by 4; tightening ±6 to ±3 is not
  "double the sample".
- Each subgroup that needs its own read at margin E needs its own n.
- Stratifying on groups that really differ lowers the σ that matters, so it
  needs fewer interviews for the same precision; groups that do not differ
  add cost for nothing.

Illustration: a prior read of 30% and a target of ±2.5 points at 95%:
n ≥ 3.8416 × 0.21/0.000625 = 1,290.8 → 1,291. For ±5 points: 323.

## Stratified estimates

x̄_s = Σ (N_h/N) x̄_h; SE = √(Σ (N_h/N)² s_h²/n_h); n_h ≥ 30 for means,
n_h p_h ≥ 5 and n_h(1 − p_h) ≥ 5 for proportions.
Stratification removes the between-group part of SRS variance.
Allocation: proportional n_h = (N_h/N) n; optimal n_h/n =
(N_h σ_h/√c_h)/Σ(N_j σ_j/√c_j).

## Correcting non-response

Non-respondents often differ from respondents on the very thing asked
(interested people reply). Respondents-only estimates are biased, and more
replies of the same kind do not help.

1. Treat respondents and non-respondents as two strata.
2. Get a random follow-up sample of non-respondents to answer (named list:
   contact a random subset; anonymous survey: re-contact about a third of the
   whole sample with a "did you submit?" screener).
3. Weights: N_1/N = response rate, N_2/N = 1 − response rate.
4. Stratified estimate, SE, CI; report next to the uncorrected figure.

Illustration: 2,000 invited, 300 replied (15%), 58% interested; follow-up of
120 non-respondents, 15% interested. Corrected: 0.15 × 0.58 + 0.85 × 0.15 =
0.215. SE = √(0.0225 × 0.58 × 0.42/300 + 0.7225 × 0.15 × 0.85/120) = 0.028;
95% CI 21.5% ± 5.5. The respondents-only 58% overstates by 2.7x. Pooling the
two waves unweighted (192/420 = 46%) is also wrong.

No follow-up exists: say the respondents' figure is likely overstated when the
reason to reply relates to the answer (interest, satisfaction), and recommend
a follow-up sample before the number drives a decision.

## Correcting non-coverage

When the procedure favours some types (intercepts at a venue favour frequent
visitors; followers and openers favour engaged customers):

1. Split the sample into the groups (clustering can reveal them).
2. f = 1 for the less likely group, f = x for the group x times more likely
   (from secondary data or the visit-frequency ratio).
3. N_1/N = (n_1/f_1)/(n_1/f_1 + n_2/f_2); then the stratified estimate.

## Confidence intervals

x̄ ± z_{α/2} s/√n (n < 30: t); p ± z_{α/2} √(p(1 − p)/n); totals: multiply
estimate and margin by N. Conditions: n/N < 0.05, n ≥ 30, n·p and n(1 − p)
≥ 5. The width shrinks with √n, not n.

## Testing against a business threshold

1. H0 is the status quo, written as Par ≤ K; Ha: Par > K (the claim that
   would justify acting). Reorder differences so the claim is "> K".
2. K from the break-even; totals become per-unit (K = total/N).
3. Reject if est > K + z_α SE (one-sided z_α: 1.645 at 95%, 2.33 at 99%).
   Proportion test SE uses K: √(K(1 − K)/n). p-value = P(Z ≥ (est − K)/SE).
4. Then give a two-sided CI for the size.

| Comparison | SE |
|---|---|
| One mean | s/√n (t with df n − 1 if n < 30) |
| One proportion | √(K(1 − K)/n) |
| Two independent groups | √(s_1²/n_1 + s_2²/n_2); small samples t with df n_1 + n_2 − 2 |
| Same units twice / matched | s_d/√n on the differences |

Pitfalls: z_{α/2} in a one-sided test; p instead of K in the proportion test
SE; paired data tested as independent; stratified weights used to compare two
groups (weights belong to estimating one population).
