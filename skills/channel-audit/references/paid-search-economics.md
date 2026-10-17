# Paid search and PPC economics

PPC is a pricing and bidding mechanism, not a channel: it runs search, display,
video and remarketing. SEM = PPC (paid) + SEO (unpaid). Spending on ads does
not lift organic rank.

## The auction

- Every query runs an auction. Ad Rank = max CPC bid x Quality Score; the
  highest bidder does not always win.
- Quality Score (1-10) = expected CTR + ad relevance + landing-page
  experience. Roughly: QS 10 about 50% lower CPC; QS 1 about 400% higher
  CPC than the neutral middle.
- Actual CPC = (Ad Rank of the advertiser below / your QS) + 0.01. You pay
  enough to beat the next ad, usually well under your max bid; a higher QS
  lowers the price for the same position.

## Metrics by layer

| Layer | Metrics | Broken means |
|---|---|---|
| Visibility | impressions, impression share, top impression rate, IS lost to rank, IS lost to budget | Rank: quality or bid. Budget: money |
| Attractiveness | clicks, CTR | Copy, extensions, targeting, offer |
| Profitability | conversions, CVR, CPA, ROAS, POAS | Landing page, offer, audience-message match, price |

Universal: CTR = clicks / impressions; CVR = conversions / clicks; CPC = cost
/ clicks; CPA = cost / conversions. ROAS = conversion value / spend. POAS
uses profit (margin) instead of revenue and is the number that matters when
products carry different margins.

## Break-even maths

```
Break-even CPC = margin per conversion x CVR
Profit per campaign = conversions x margin per conversion - cost
Break-even ROAS = 1 / gross margin rate
```

Worked shape (not from a case): margin $30 per order, CVR 4% gives a
break-even CPC of $1.20; paying $1.50 loses $0.30 per click on average.

## Reading impression share

| IS lost to budget | IS lost to rank | CPC vs break-even | Do |
|---|---|---|---|
| High | Low | Below | Raise budget: profitable demand left on the table |
| High | Low | Above | Do not add budget; cut bids or fix CVR first |
| Low | High | Below | Improve QS (relevance, landing page); bid up only while CPC stays under break-even |
| Low | High | Above | Fix quality or pause; bidding up makes losses larger |

## Structure

Account -> campaigns (budget, geo, schedule, network; one goal each) -> ad
groups (one tight theme: related keywords, tailored copy, dedicated landing
page, negatives). Negative keywords block waste and stop your own ad groups
competing. One ad group with hundreds of unrelated keywords drags relevance,
QS and CPC.

## Assets

Headlines carry the keyword; descriptions = keyword + value proposition + call
to action; extensions (sitelinks, callouts, promotions) raise CTR and QS. The
platform rotates the combinations you supply.

## Benchmarks (WordStream 2024, ~17,000 campaigns)

Search CTR about 3.17%, display about 0.46%; average CVR near 7%; display CPC
around $0.63 vs several dollars on search. For buying-intent keywords, ads
take about 65% of clicks vs 35% organic.

## Brand keywords

Brand terms show low CPC and high QS, and look like the best campaign. A
well-known marketplace experiment found branded paid clicks largely
non-incremental (organic would have caught them). Arguments to keep them:
blocking competitors, message control. Verdict: test incrementality before
deciding (see `evidence-check` pause tests).

## Platforms

Google Ads (search, display, YouTube, shopping); Meta (interest and lookalike
targeting); Microsoft Ads (older, higher-income desktop audience, cheaper
clicks, fewer competitors); TikTok; LinkedIn (B2B job targeting); X.
