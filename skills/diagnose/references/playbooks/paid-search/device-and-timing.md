---
title: Device and timing
question: When and how should device, day-part, and geo bid adjustments come into play
order: 9
---

A blended cost per click quietly averages a phone click that browses and a desktop click that buys into a single price you pay for both. Device and timing analysis undoes that error: read performance split by device and by time, then set bid adjustments so you pay more where the click is worth more. It is the fine-tuning pass: deliberately the last read, never the first.

## The framework

1. **Only tune a clean account.** A device gap read on top of an unfixed leak (brand leakage, wasted search terms) is partly an artifact of the mess, and a bid adjustment is a multiplier on a bid you must have already set correctly against the break-even ceiling.
2. **Device first**: the gap is usually widest and the data cleanest. In retail, mobile often takes the larger share of clicks at a higher CPC while desktop converts at more than double the rate: phones are where people compare, desktops are where considered purchases close. The move is a bid adjustment, not a device ban; mobile is most of the demand and much of it converts later.
3. **Day of week next**, then hour of day where volume supports it. Retail has a rhythm: weekday lunch-hour browsing, weekend-evening closing. Lift bids on days that pay back, trim days that window-shop.
4. **Geography last, and only where it resolves.** Where location data resolves cleanly to a real market you serve, adjust; where it pools to one organization-level row, leave it alone.

One caveat: device and schedule modifiers are manual-bidding levers. Automated bidding toward a target CPA or ROAS already folds these signals into every auction, so under automation, read the splits as diagnosis, not dials.

## Metrics that matter (and their traps)

- **Conversion rate and CPC by device**: the pair that sets the adjustment. Trap: a phone click costing twice as much and converting at half the rate is worth roughly a quarter of the desktop click; its low absolute CPC makes it look like a bargain.
- **Bid adjustment range**: device modifiers run from -100% to +900% ([Google Ads Help](https://support.google.com/google-ads/answer/2732132)), the same range by day and hour through ad scheduling.
- **Conversion rate by day/hour**: real signal, but demand a stable pattern across weeks before scheduling against it.
- **Geo performance**: the read that most tempts you into a confident, false number. Trap: a geo chart drawn on pooled data is one number wearing a map; performance in a country you do not ship to is noise.
- **Ad frequency**: follows an inverted-U in display and video, but search is a pull channel; frequency lives on the display and social side.

## Interview prep

**"Mobile is 60% of our clicks. Should we bid it up?"**
Share of clicks is not value. A strong candidate asks for CPC and conversion rate by device, computes what a mobile click is worth relative to desktop, and adjusts price to value without banning mobile.

**"Why is device tuning the last step of an account audit?"**
Splits read on a dirty account are artifacts, and adjustments multiply a base bid that must already be right. Hygiene, waste, and the break-even ceiling come first.

**"You set a -20% mobile modifier and nothing changed. Why?"**
The campaign likely runs automated bidding, which treats manual modifiers as advisory. Check the bid strategy before blaming the data.

**"Regional conversion rates look wildly different. Do you set location adjustments?"**
Only after confirming the location data resolves per region rather than pooling, and only for markets the business serves. Better a device adjustment you can trust than a geo adjustment you cannot.
