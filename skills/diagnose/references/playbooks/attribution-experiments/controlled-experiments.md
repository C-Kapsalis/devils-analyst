---
title: Controlled experiments for ad effectiveness
question: How do you prove an ad actually caused sales, rather than harvesting buyers who would have bought anyway
order: 2
---

A dashboard can say a campaign converted at 10%; it cannot say how many of those shoppers would have bought anyway, because a dashboard only records the world that happened. A randomized controlled experiment, run in the ad platform's own experiment tools, supplies the counterfactual, and for awareness spend whose sale closes days later through a search or direct visit, it is the only method that settles the causal question.

## The framework

1. **Respect the natural-buyer trap.** Regular customers buy after seeing an ad that changed nothing. Worse, comparing ad-viewers against non-viewers is biased by design: platforms aim ads at the people most likely to buy, so a 20% vs 9% gap proves targeting, not effect.
2. **Build the PSA holdout.** Split one target audience at random: treatment sees the branded ad; control sees a neutral public service announcement in the same slots. The PSA is a receipt: it proves the control shopper was actually reachable, and the neutral spend is the fee for a clean answer.
3. **Count shoppers, not clicks**, across an impression-based attribution window, so a control shopper who buys days later via search still counts to the control baseline.
4. **Read lift, not the raw gap**, then convert to incremental conversions and incremental value.
5. **Check balance, then segment.** Verify the randomization held, then break the average down by day, device, and frequency, and confirm eye-catching splits formally before betting budget on them.

## Metrics that matter, and their traps

- **Lift**: (treatment rate − control rate) / control rate. A 9.0% control against a 20.3% treatment is not "up 11 points"; it is +125% against the natural baseline. Trap: raw point gaps flatter small numbers.
- **Incremental conversions**: treatment conversions minus (control rate × treatment size). If 400 treated shoppers convert 81 times against a 9% baseline (~36 natural buyers), the ad caused ~45. Trap: banking all 81 as the campaign's work.
- **Incremental value**: the recorded on-site value of those incremental orders. Trap: calling it profit; that needs margin data.
- **Balance-check p-values**: high is good news: above 0.05 means the groups are indistinguishable on that variable, so the ad is the only explanation left for the gap.
- **Segment lift**: averages hide sign flips: an ad can run +188% lift on weekdays and roughly zero on weekends. Frequency follows an inverted U, negligible at 1–10 exposures, peaking mid-range, sagging where the ad reads as spam. Trap: comparing segments on raw rate gaps, and trusting a dramatic split before it clears significance.

## Interview prep

**"Ad viewers converted at 20%, non-viewers at 9%. The ad works, right?"**
No, the platform hand-picked the viewers for intent, so the crowds were never comparable. A strong candidate proposes a randomized holdout, where random assignment makes the ad the sole difference between groups.

**"Why show the control group a PSA instead of nothing?"**
The PSA proves the control shopper was online and reachable in that slot, keeping the groups comparable moment for moment. With "nothing" you cannot distinguish a genuine non-converter from someone who was never advertisable, and the PSA cost is the price of the clean answer.

**"Your test shows +125% average lift. What do you check before reporting it?"**
Balance first (the split held on age, prior purchases, visit depth), then segments: where lift is at or below zero the ad is not working, and where a split looks dramatic, a formal test decides whether it is proven or merely suggestive.

**"How would you use an experiment to set a frequency cap?"**
Read lift by exposure band and find the inverted-U peak: too few exposures and nobody notices, too many and you pay to annoy people already sold.
