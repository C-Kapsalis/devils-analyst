# Forecasting trends and costs

## Which model

| Pattern in the data | Model | Confirm by |
|---|---|---|
| A shape that repeats every n periods | Moving average of order n | Same-season comparisons line up |
| Constant % change per period | Exponential Y = A e^{bt} | ln Y vs t is a straight line |
| Each % change in X gives a fixed % change in Y | Power Y = A X^{−a} | ln Y vs ln X is a straight line |

## Moving average (seasonal series)

1. Find the cycle length n (4 for quarters, 12 for months, 7 for days).
2. From t = n: MA_t = (X_t + ... + X_{t−n+1})/n. No MA exists before t = n.
3. MA_t is the forecast for t + 1.
4. Trend per period ≈ MA_t − MA_{t−1}.

Why the order must equal the cycle: write X_t = a·t + β_t with β_t = β_{t−n}.
Then MA_t − MA_{t−1} = (X_t − X_{t−n})/n = a: the seasonal terms cancel only
when the window spans exactly one cycle. A 3-month window on monthly data
with a December peak carries the peak into the trend and into January's
forecast.

For seasonal indices and deseasonalised growth (ratio to moving average) see
metric-definitions, "Seasonal index".

## Exponential growth or decay

1. Regress ln Y on t: slope b, intercept ln A.
2. Growth factor per period e^b; % change per period e^b − 1 (close to b only
   when b is small).
3. b > 0 growth (absolute steps get larger); b < 0 decay, such as awareness
   after advertising stops (absolute steps get smaller).

## Power model and experience curve

1. Regress ln Y on ln X: slope −a.
2. Experience curve: unit (marginal) cost after Q cumulative units.
   Learning rate = cost after a doubling / before = 2^−a; drop per doubling
   = 1 − 2^−a; a = −log2(learning rate).
3. Forecast from a known point: C = C_0 (Q/Q_0)^−a.

Illustration: 15% drop per doubling → learning rate 0.85, a = 0.234. From
$50 at 1,000 units, at 8,000 units (three doublings): 50 × 0.85³ = $30.71.

Constant-elasticity demand Q = A P^{−E} is a power model: see pricing.md.

## Pitfalls

- MA order different from the cycle.
- Reading b as the % change.
- Experience-curve C is the cost of the next unit, not the average cost.
- Successive observations depend on each other; these models describe a
  trend, not independent samples, so do not apply independent-sample tests.

## Write-up lines

- "Sales repeat every __ periods, so we use an MA of order __; the smoothed
  series moves about __ per period; the forecast for __ is __."
- "Fitted Y = __·e^{__t}: __% per period."
- "Unit cost falls __% per doubling of cumulative volume; at __ units we
  expect $__."
