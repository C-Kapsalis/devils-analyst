---
title: Cohort analysis, measure before you model
question: When should you model customer value, and when should you simply measure it
order: 2
---

Once a team accepts that lifetime value is a guess, the instinct is to reach for a better guess: more model, more parameters, applied to every customer on the books, including the ones who were never silent in the first place. That is the trap. Whether you can know a customer's future comes down to how often they tell you they are still there, and the method should be decided by that signal density before any math.

## The framework

1. **Sort customers by how loudly they tell you they are there.** Three settings: **contract** (subscription customers: they pay every cycle and cancellation is an event with a date; lifetime is bookkeeping), **heartbeat** (replenishment buyers: coffee, pet food, skincare on a rhythm; nobody cancels, but a stopped drumbeat is loud all by itself), and **silence** (considered purchases: apparel, furniture, a coat every other winter; quiet between orders means two opposite things you cannot tell apart).
2. **Measure where the signal is dense; model only where it is sparse.** A subscriber's lifetime is read off renewal history; a replenishment buyer's churn is watched in the order rhythm. Only the genuinely silent customer needs buy-till-you-die mathematics. A fancy model applied to data you could have counted isn't rigor: it replaces a fact you owned with an estimate you invented, and a measured number you can defend beats a modeled one you have to caveat.
3. **Measure the flow, not just the pulse.** A heartbeat can keep beating while the customer quietly leaves: the coffee order still arrives, so "are they active?" says yes, but the gap has stretched from three weeks to six and the basket is half the size. Meaningful churn in a split-wallet business is erosion, not a clean death.
4. **Read the shape of the decline, because it names the action.** Quiet every summer is seasonal, not lost. A drop that starts with a refund or support ticket is a fixable experience problem. Steady erosion with no incident is a competitor eating your lunch. A hard stop is a goodbye. Four futures, four actions.
5. **Keep the guess and the fact in different boxes.** A measured lifetime and an inferred one aren't the same kind of number; never average them into one figure that hides which is which.

## Metrics that matter, and their traps

- **Repeat rate by cohort:** holding cohort after cohort is health; slipping a little with every cohort is quiet erosion. Trap: one pooled rate hides the trend.
- **Order frequency (gap between orders):** a stretching gap is churn in progress that an activity flag will never show.
- **Average order value:** a still-"active" customer with shrinking baskets has moved their wallet elsewhere. Trap: counting them as retained.
- **"Active customer" flags:** the easy question ("are they alive?") and the wrong one. The real question is "how much of them do we still have?"
- **Modeled LTV on dense-signal customers:** a red flag in itself: if the order history could answer the question by counting, the model is dressing a fact as an estimate.

## Interview prep

**"Would you build a probabilistic churn model for our subscription customers?"**
No: subscribers have a cancel event; lifetime is read off renewals. A strong candidate reserves modeling for silent, considered-purchase customers: the simplest honest method the signal allows wins.

**"Retention looks fine, 80% of last year's customers are still active. What is wrong with that read?"**
It measures the pulse, not the flow. They would check order frequency and basket size by cohort: customers can stay "active" while wallet share erodes to a competitor.

**"A replenishment customer's orders went quiet for three months. Lost?"**
Depends on the shape: seasonal quiet recurs on schedule; a stop after a refund is an experience problem; steadily stretching gaps suggest a competitor. Each future gets a different action.

**"How do you present measured and modeled customer value together?"**
In separate, labeled boxes (measured lifetimes for contract and heartbeat customers, modeled estimates with stated uncertainty for the silent), never averaged into one figure that hides which is which.
