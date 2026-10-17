# Decomposition reference

Three methods, each exact: the parts add up to the change being explained.
Period 0 is the comparison period, period 1 the current one.

## 1. Contribution (sums)

For a total T = sum of T_i over segments i:

```
contribution_i  = T_i1 - T_i0
share_i         = contribution_i / (T_1 - T_0)
```

Shares can exceed 100% or be negative when segments move in opposite
directions; that is information, not an error. Report the top movers both ways
(largest gain, largest loss). If the total barely moved, do not report shares
(dividing by a near-zero change); report the absolute contributions.

## 2. Mix vs rate (ratios)

Any rate R = N / D (CTR = clicks / delivered, CVR = conversions / sessions,
CPA = spend / conversions) is a weighted average of segment rates:

```
R  = sum_i  w_i * r_i        where  w_i = D_i / D   and   r_i = N_i / D_i
```

So R can change because segment rates changed (**rate effect**) or because the
volume moved between segments with different rates (**mix effect**). The exact,
symmetric split, per segment:

```
R_bar   = (R_0 + R_1) / 2
r_bar_i = (r_i0 + r_i1) / 2
w_bar_i = (w_i0 + w_i1) / 2

rate_i  = (r_i1 - r_i0) * w_bar_i
mix_i   = (w_i1 - w_i0) * (r_bar_i - R_bar)

sum_i (rate_i + mix_i) = R_1 - R_0        (exact)
```

`mix_i` is positive when volume shifts toward a segment that converts above
average, negative when it shifts toward one below average.

**Segments that appear or disappear.** A segment with no volume in one period
has no rate there. Set its missing rate equal to its other-period rate, so all
of its effect is mix. Say so: "the new VIP segment adds 0.56 points of mix".

**Never average segment rates.** The average of 3.6% and 5.1% is not the
combined CTR. Always recompute R from summed numerators and denominators.

## 3. Driver tree (products)

When a metric is a product of drivers, M = d_1 x d_2 x ... x d_k, use the log
(LMDI) split:

```
L          = (M_1 - M_0) / ln(M_1 / M_0)           (logarithmic mean)
contrib_j  = L * ln(d_j1 / d_j0)
sum_j contrib_j = M_1 - M_0                         (exact)
```

Requirements: every driver positive in both periods. If M_1 = M_0, report each
driver's percent change instead (L is undefined).

Common marketing driver trees (check the identity holds on the data before
using it; if the product does not reproduce the metric, a definition is off):

| Metric | Drivers |
|---|---|
| E-commerce revenue | sessions x conversion rate x average order value |
| Email revenue | delivered x CTR x click-to-order x average order value |
| Paid conversions | spend / CPC x CVR (= clicks x CVR) |
| Paid revenue | spend x ROAS |
| Organic clicks (GSC) | impressions x CTR |
| Pipeline (CRM) | leads x lead-to-opportunity rate x average deal size |
| New customers | sessions x new-visitor share x new-visitor conversion rate |

## 4. Noise

A rate measured on a small denominator moves a lot by chance. For a proportion
p measured on n (clicks / delivered, conversions / sessions):

```
SE(p)            = sqrt( p * (1 - p) / n )
change is clear  if  |p_1 - p_0|  >  2 * sqrt( SE_0^2 + SE_1^2 )
```

This is a screen, not a test: it assumes independent trials, which email and
web data only approximate. Use it to keep noise out of the headline, not to
claim significance. For sums (revenue, sessions), compare the change with the
typical week-to-week swing over the last 8 periods; inside that swing, call it
"within normal variation".

Minimum volumes before reporting a rate change for a segment: about 100
conversions-or-clicks in the numerator, or 1,000 in the denominator. Below
that, fold the segment into "Other".

## 5. Worked example (email)

Previous period: Newsletter 14,000 delivered / 504 clicks (3.6%), Active 5,000 /
255 (5.1%), no VIP send. Current: Newsletter 14,500 / 464 (3.2%), Active 5,300 /
339 (6.4%), VIP 850 / 153 (18.0%).

Overall CTR: 759 / 19,000 = 3.99% to 956 / 20,650 = 4.63%, **+0.635 points**.

| Segment | Weight | CTR | Mix (pts) | Rate (pts) | Total (pts) |
|---|---|---|---|---|---|
| Newsletter | 0.737 to 0.702 | 3.6% to 3.2% | +0.032 | -0.288 | -0.256 |
| Active | 0.263 to 0.257 | 5.1% to 6.4% | -0.009 | +0.337 | +0.328 |
| VIP (new) | 0 to 0.041 | 18.0% | +0.563 | 0 | +0.563 |
| **Total** | | | **+0.586** | **+0.049** | **+0.635** |

Noise screen: Newsletter changed -0.40 points against a 2 x SE band of 0.43
points, so it is not a clear change. Active changed +1.30 points against 0.92,
so it is clear.

Insight: "CTR rose 0.64 points, almost all of it mix from the new VIP send.
Like for like, only Active customers clicked more."

Driver tree for revenue on the same sends: delivered 19,000 to 20,650, CTR
4.0% to 4.6%, click-to-order 12% to 10%, AOV $37 to $41. Revenue $3,374 to
$3,895, **+$520**:

| Driver | Change | Contribution |
|---|---|---|
| Delivered | +8.7% | +$302 |
| CTR | +15% | +$507 |
| Click to order | -17% | -$662 |
| AOV | +11% | +$372 |
| **Total** | | **+$520** |

Insight: "Revenue grew $520, but click-to-order fell from 12% to 10% and cost
$662. More people clicked; fewer of them bought. Check the landing page and the
offer before sending more traffic." Then hand "click-to-order declining" to the
`diagnose` skill.
