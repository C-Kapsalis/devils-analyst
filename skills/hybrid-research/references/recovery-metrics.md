# Recovery metrics: synthetic vs human

Load when comparing a synthetic panel with human answers on the same items.

## 1. Preconditions

- Same items, same wording, same scale on both sides.
- Synthetic personas matched to the human sample's demographics (1:1 for a
  replication). Show the comparison table; a mismatch makes every metric below
  a comparison of different populations.
- Respondent-level data on both sides (respondent x item), not only summary
  means. Without it variance and correlations cannot be checked: say so.
- Missing synthetic answers (failed after retries) excluded, counted, reported.

## 2. The metrics

| Metric | Computation | Pass |
|---|---|---|
| Mean bias | for each item `abs(mean_h - mean_s)`; MAE = their mean | MAE < 0.5 on 5 points |
| Variance ratio | for each item `var_s / var_h` | 0.7 to 1.3 |
| Correlation MAE | for each item pair `abs(r_h - r_s)`; their mean | < 0.2 |
| Distribution | chi-square test on the counts per answer option, human vs synthetic | p > .05 |
| Winner | top concept on the outcome item | same concept |
| Rank order | Spearman rho between the human and synthetic ranking of items or concepts | >= .80 |

Note the variance ratio uses variances. An SD ratio of 0.6 is a variance
ratio of 0.36: a fail.

Other scales: the 0.5 MAE threshold is stated for a 5-point scale. For a
7-point item, rescale the gap to 5 points (gap x 4/6) before comparing.

```python
import numpy as np, pandas as pd
from scipy import stats
items = [...]                                    # Likert columns
mae = np.mean([abs(H[c].mean() - S[c].mean()) for c in items])
vr  = {c: S[c].var(ddof=1) / H[c].var(ddof=1) for c in items}
rh, rs = H[items].corr(), S[items].corr()
iu = np.triu_indices(len(items), 1)
corr_mae = np.mean(np.abs(rh.values[iu] - rs.values[iu]))
chi = {c: stats.chi2_contingency(pd.crosstab(
        np.r_[np.zeros(len(H)), np.ones(len(S))],
        np.r_[H[c].values, S[c].values]))[1] for c in items}
```

## 3. Reading order and interpretation

1. **Variance ratio per item.** The usual failure. Below 0.7 means the panel
   is too uniform: any segment difference, driver analysis, correlation or
   power calculation from it is understated.
2. **Correlation MAE.** Near-zero synthetic correlations against strong human
   ones mean each answer was drawn on its own, not by a coherent person. Fix
   with response history, then RAG.
3. **Distribution.** Means can match while shapes differ (human bimodal,
   synthetic unimodal). Look at histograms, not only the test.
4. **Mean bias.** Direction usually right; the size of the miss tends to be
   about 0.5-0.7 points toward the extremes in zero-shot runs. Context does
   not fix it. A correction needs a calibration rule from past studies in the
   same category.
5. **Winner and rank order.** For concept tests the business cares about the
   ranking. A match on one study is one data point for the repository, not a
   licence.

A panel passes only when every key item passes variance, the correlation MAE
passes, and the mean passes. A good MAE alone is the classic false pass.

## 4. Sample size from a synthetic pilot

Per arm, for a difference delta in means of an item: `n = 16 x sigma^2 / delta^2`
(80% power, 5% two-sided). Synthetic sigma^2 runs low, so n from it is too
small. Use `sigma^2_human_est = sigma^2_synthetic / variance_ratio` with the
variance ratio from the repository (same category and configuration). Without
a ratio, report the synthetic n as a minimum and a range using a plausible
human variance from any past wave on similar items.

## 5. Qual-side metrics (for completeness)

| Metric | Use | Read |
|---|---|---|
| SMOG, Gunning Fog, Flesch-Kincaid | readability | LLM text usually reads harder; ask for plain, conversational language if it matters |
| Unique tokens per document | information density | self-moderated LLM interviews tend to be highest |
| Topic coherence (LDA) | are there interpretable themes | higher is better |
| Embedding cosine (e.g. SBERT), UMAP map | similarity to human answers | >= .5 is high; clusters in one source only are the complementary insights |
| Blind human rating (clarity, relevance, depth, insightfulness) | research-objective fit | mixed-effects model controlling for question, length, rater |
| Theme recovery | share of human-baseline themes found | >= 80% |
| New theme rate | share of themes not in the baseline | a feature; label as hypotheses |
