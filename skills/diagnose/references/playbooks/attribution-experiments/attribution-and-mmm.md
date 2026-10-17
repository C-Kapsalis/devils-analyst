---
title: Attribution and marketing mix modelling
question: How do you get from a last-click ROAS floor to an estimate of what each channel truly contributed
order: 1
---

A measured, last-click return (the on-site value your analytics recorded per line, against what it cost) is honest and comparable across channels, but it is a floor. Awareness and upper-funnel channels earn much of their sale through a later search or direct visit, and last-click credits that final step, not the reach that started the journey. To see what each channel actually contributed, you model the data.

## The framework

1. **Start from a clean spend-and-outcome table**: one row per campaign, reconciled across sources by campaign name, with cost, impressions, and clicks per line; the recorded on-site value (key events, transactions, revenue) matched to the same line; all of it drillable from account service down through account, campaign type, and campaign, over time. That tidy table is exactly what an attribution or mix model consumes.
2. **Understand what each model adds.** A data-based attribution model spreads a sale's credit across the touches that actually moved the buyer, instead of handing everything to the final one. A marketing-mix model goes further: it estimates how sales respond to spend per channel over time, including awareness reach that never earns a click at all.
3. **Pick the model for the shape of the business.** There is no single right model; the appropriate approach depends on factors like sales cycle, channel mix, and data granularity, and different business shapes call for different (often Bayesian) formulations.
4. **Keep the division of labor honest**: the data layer assembles the measured floor and the modeling input; choosing the model, setting the priors, and reading the result is analytical work done on top of it.

## Metrics that matter, and their traps

- **Last-click ROAS per campaign**: the measured floor and the model's calibration point. Trap: treating the floor as the verdict and cutting the upper-funnel lines it structurally understates.
- **Multi-touch attributed credit**: a fairer split of recorded touches. Trap: it still only sees recorded touches, and it is credit reassignment, not causal proof.
- **MMM channel-response estimates**: the only observational read that includes click-less reach. Trap: presenting a model's estimate with false precision; it is an estimate to validate against experiments, not a measurement.

## Interview prep

**"What data would you need to stand up a mix model?"**
A per-campaign, per-period table of spend and recorded outcome value, reconciled across every paid channel on one denominator, with enough history and spend variation for the model to learn from. A strong candidate flags that inconsistent campaign naming or platform self-reported conversions poison the input.

**"When is multi-touch attribution enough, and when do you need MMM?"**
Multi-touch helps when the journey is digitally tracked end to end; MMM is needed when meaningful contribution never earns a click (display, video, offline) or when tracking loss breaks the touch record. They are complements, not competitors.

**"How do you know your model is right?"**
You do not know, from the model alone; attribution is credit, not proof. Validate against controlled experiments where possible, and treat a model whose estimates keep contradicting holdout tests as miscalibrated.
