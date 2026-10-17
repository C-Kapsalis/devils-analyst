---
title: Customer lifetime value vs CAC
question: How do you compare what a customer is worth against what they cost, honestly
order: 1
---

Every business wants one number: what is a customer worth? Spend less to win them than they bring you over time and you grow; spend more and you slowly bleed out. Most teams treat lifetime value as a fact to look up. It isn't: in a non-subscription business it is a guess about silence, and treating the guess as fact is how teams overpay for acquisition.

## The framework

1. **Understand the unknowable half.** Customer value is spend per order, times how many more times they buy, minus cost to serve (future money discounted). The first half is receipts; the second is the problem. A subscriber cancels; a shop customer just goes quiet, and the same three months of silence could mean "gone" or "between purchases." Every LTV number is a particular guess about what that silence means.
2. **Fence the guess.** The floor is the margin a customer has actually generated to date, money in the bank. The ceiling assumes the relationship runs forever. Report floor, ceiling and your honest estimate between them, so no single number poses as the truth. Ceiling-only reporting manufactures phantom value; floor-only reporting starves your best channels.
3. **Keep worth and cost at their honest levels.** Worth is personal: one customer's spend can be traced and totaled. Cost is shared: a campaign buys a crowd (some who would have come anyway, some nudged, some free via word of mouth), so a per-person acquisition price is a number you invented and then rounded. CAC is only real for a group won in the same stretch of time: total spend over the crowd it brought in. The honest question is never "did this customer pay back?" but "did the group we won in March pay back, and how fast?"
4. **Pick the number by the decision.** "How much can I afford to spend to acquire?" wants a near-term, conservative figure; "what is our loyal base strategically worth?" wants a longer, carefully discounted one. Letting the decision choose the horizon dissolves the which-formula-wins argument.
5. **Backtest before you trust.** Hide the last year of data, ask the model to predict it, compare. A model that cannot retro-predict the past has no business forecasting the future.

## Metrics that matter, and their traps

- **Realized margin to date (the floor):** the only assumption-free customer value. Trap: under-investing because you ignored real future value.
- **Projected LTV (the estimate):** only as good as its churn assumption. Trap: the classic one-steady-churn-rate-forever formula, undiscounted (the ceiling wearing an estimate's clothes).
- **CAC:** total spend over customers won, per group and period. Trap: dragging it down to the individual, which manufactures precision that was never there.
- **LTV:CAC ratio:** meaningful only when both sides are computed at their honest level (group worth against that same group's spend) and matched in horizon.
- **Cohort payback period:** the month a group's accumulated margin repays what it cost to win. The cleanest, most decision-ready form of the comparison, with no invented per-person cost anywhere.

## Interview prep

**"Our dashboard says LTV is €340. Is that a fact?"**
A strong candidate asks which assumption about silence produced it (what churn model, what horizon, discounted or not) and where it sits between the realized floor and the never-churn ceiling.

**"Finance wants CAC per individual customer to compare against their order history. Do you build it?"**
No: cost is shared across a crowd; any per-person allocation is invented. They reframe to the cohort: this group's total worth against this group's total spend, and payback in months.

**"Two teams computed LTV and got numbers 3x apart. Who is right?"**
Probably both, for different questions: one a near-term acquisition-budget number, the other a long-horizon strategic one. Match each number to its decision instead of crowning a formula.

**"How would you validate an LTV model before putting it in the plan?"**
Holdout backtesting: hide a year, predict it, compare. The method that survives earns the headline; the others stay as second opinions with their assumptions stated.
