---
title: True ROAS across every paid channel
question: How do you compare return across paid channels when every platform claims the same sale
order: 7
---

Close one sale and by Monday every platform has claimed it: Google reports its return on Google's attribution, Meta on Meta's, each telling the truth about itself and nothing about the others. Their ROAS figures can never simply be stacked: you would be double-counting the same orders and flattering every channel at once. The honest cross-channel return needs one shared denominator.

## The framework

1. **Build the measured read**: every paid channel's cost against one shared value (the on-site value your own web analytics recorded, matched to each line by campaign name), drillable from account service down through account, campaign type, and individual campaign.
2. **Read it as an honest floor, not the truth.** The shared read is last-click: it credits the value to the final recorded touch. That makes it real and comparable, but it systematically understates upper-funnel lines, whose sale usually closes through a later search or direct visit.
3. **Model past the floor.** Attribution is credit, not proof: last-click is a rule for splitting a sale, not evidence a channel caused it. A data-based attribution model spreads credit across the touches that moved the buyer; a marketing-mix model estimates how sales respond to spend per channel over time, including reach that never earns a click. The same per-campaign spend-and-value table that produced the measured read is the model's input.

## Metrics that matter, and their traps

- **Platform-reported ROAS**: each platform's self-graded homework on its own attribution and window. Trap: stacking them across platforms; the same sale is counted twice and every channel looks like it paid for itself.
- **Measured ROAS on one denominator**: recorded on-site value over cost, matched by campaign name. Trap: forgetting it is a floor, and cutting awareness lines whose contribution arrives sideways through a later click.
- **Campaign-name matching**: the join that makes cross-channel comparison possible at all. Trap: sloppy or inconsistent campaign naming silently breaks the reconciliation, and the "comparable" view stops being comparable.
- **Modeled contribution**: the estimate of what each channel truly caused. Trap: treating any attribution model's output as proof; the causal check is a controlled experiment, and the model choice itself depends on the shape of the business.

## Interview prep

**"Google says 5x ROAS, Meta says 4x, and finance says total revenue does not support either. Explain."**
Both platforms credit the same conversions on their own attribution, so their claims overlap. A strong candidate proposes one shared denominator (the value the site's own analytics recorded, matched per campaign) and expects each platform's number to shrink once the double-count collapses.

**"On the shared last-click read, display shows the worst ROAS in the account. Cut it?"**
Not on that number alone: last-click is a conservative floor that is lowest precisely for upper-funnel lines. They would flag it for a mix model or a holdout experiment before reallocating, because the measured floor and the true contribution diverge most at the top of the funnel.

**"What is the difference between attribution and incrementality?"**
Attribution is a rule for splitting credit among recorded touches; incrementality is whether the sale would have happened without the channel. A model reassigns credit; only an experiment proves cause. Strong candidates never present a reassigned credit split as proof.

**"How would you set up the data to make channels comparable?"**
One cost row per campaign per channel, one recorded on-site value matched by campaign name, consistent naming enforced upstream, and a drill path from the whole program down to a single campaign: the tidy spend-and-outcome table a mix model can consume later.
