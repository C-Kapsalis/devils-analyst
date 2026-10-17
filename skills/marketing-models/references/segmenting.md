# Segmenting: factor analysis, then K-means

## When

- Many correlated ratings per respondent (importance of features, Likert
  items) and you want a few interpretable dimensions.
- You want groups of customers with similar needs (benefit segments).
- A regression has multicollinearity: replace correlated regressors with
  uncorrelated factor scores.
- Checking whether a Likert summated scale is valid (one dominant factor =
  unidimensional attitude, the scale is fine).

## Factor analysis

1. Run on the m items.
2. Keep factors with eigenvalue ≥ 1 (each explains at least one item's worth
   of variance). Eigenvalues sum to m; share explained = Σ kept / m.
3. Rotate with varimax so each item loads clearly high or low on each factor.
4. Name each factor from items with abs(loading) ≥ 0.5 and their signs.
   Loading = correlation of item and factor.
5. Communality of an item = Σ squared loadings on kept factors = R² of the
   item on the factors. Low communality: the factors miss that item.
6. Save factor scores: mean 0, variance 1, uncorrelated.

## K-means on factor scores

1. Pick K; start from K random points; assign each respondent to the nearest
   centroid (Euclidean); recompute centroids; repeat until no change.
2. Total WCSS = Σ over clusters of squared distances to the centroid. It
   always falls as K rises; choose K at the elbow, where it stops falling
   sharply.
3. K-means is a heuristic that depends on the start: rerun with several
   starts before trusting one solution.

## Profiling

Read the cluster-means table (clusters x factors). Factor scores are
standardised: > 0 above average, < 0 below, 0 = average (not "none"). Mark
each cluster's highest and lowest factors, name the segment, give its size.

To explain original (often yes/no) items by the factors, regress (or logit)
each item on the factor scores and read significance and sign.

Conjoint route: cluster respondents on their individual part-worths; each
cluster's most important attribute is the one with the largest part-worth
range (see research-design, measures.md).

## Pitfalls

- Keeping factors with eigenvalue < 1.
- Naming factors from unrotated loadings.
- K-means on raw correlated items (near-duplicate items get double weight).
- Choosing K without the elbow, or trusting one run.
