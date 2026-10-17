---
title: Impression share and quality score
question: How do I read the visibility layer that sits above the click
order: 7
---

Standard reports start counting at the click, but the richest diagnostics sit one step earlier: of all the searches you were eligible to appear on, what fraction did you show up for, and why did you miss the rest? Optimize the click without reading the eligibility behind it and you are tuning a number downstream of the real leak.

## The framework

1. **Impression share first**: impressions received divided by impressions you were eligible for. It answers the blunt question underneath everything else: are we even showing up? An account showing for 11% of eligible searches lets nine in ten winnable searches go by unseen; no CTR tuning recovers them.
2. **Split the loss.** Lost share divides into two causes with opposite fixes. Lost to **rank**: ad rank (bid times quality) too low to enter the auction; lift quality score or raise the bid. Lost to **budget**: competitive but the daily cap ran dry; raise the cap on a campaign already paying back. This is the cleanest diagnostic in the channel; one half says fix quality, the other says spend more.
3. **Read quality score by component**, not the rolled-up 1–10 number: expected CTR points at the headline and offer; ad relevance at tighter ad groups and keyword-in-copy; landing-page experience at message match, speed, and mobile.
4. **Premium placement**: top impression rate (above organic results) and absolute top rate (the first ad slot) answer "are we showing *well*?" Position matters most on mobile.
5. **Auction insights**: when share is lost to rank, someone specific took it. This report names the competitor overlapping and outranking you.

Above these sit the harder disciplines: which creative earned the click (a rolling ad-and-asset test), whether the ad caused the sale (a holdout experiment), and how credit splits across touchpoints (a modeling choice: compare last-click against data-driven attribution on the same conversions).

## Metrics that matter (and their traps)

- **Impression share**: core terms should sit high; Google's guidance points to the high tens of a percent on queries that matter ([Google Ads Help](https://support.google.com/google-ads/answer/2497703)). Trap: the platform buckets extreme values (under 10%, over 90%), clamping the finest slices.
- **Share lost to rank vs budget**: the two sum with impression share to the full eligible pool. Trap: pouring quality work into a budget-starved account, or raising caps on one being outranked.
- **Quality score**: a top score can roughly halve CPC; a bottom score can multiply it nearly fivefold. Trap: reading the single number instead of the component distribution; you need to know *which* component drags.
- **Aggregation**: account-level figures must be weighted by eligible impressions, or a tiny keyword counts as much as a flagship one.

## Interview prep

**"Impression share on our core terms is 11%. What do you do?"**
A strong candidate asks how the lost 89% splits: rank or budget. If mostly budget on a converting campaign, the move is cap money, not quality work; if rank, quality-score components or bids.

**"Quality score is 4/10 account-wide. Where do you start?"**
With the components as distributions: what share of keywords grade below average on each. A run of poor landing-page grades sends you to the site, not the auction.

**"How is a conversion counted different from a conversion caused?"**
Counted means a conversion followed a click; caused means it would not have happened without the ad. The gap is the money you could stop spending, and only a randomized holdout measures it.

**"A competitor started outranking us. How do you confirm and respond?"**
Auction insights for overlap and outranking share, then the rank equation: raise quality before raising bids.
