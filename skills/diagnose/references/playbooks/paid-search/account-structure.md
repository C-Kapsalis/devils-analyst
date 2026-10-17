---
title: Account structure and clusters
question: How do I localize a paid search problem instead of averaging the whole account
order: 3
---

A soft number at the top of an account is never evenly spread underneath; it sits in one branch, and the structure is the map that takes you there. Reading by structure turns "the account softened" into "one market's generic-outerwear ad group softened"; without it you average everything and learn nothing.

## The framework

Every account carries the same four-level skeleton, readable with zero setup. Work top down:

1. **Service**: Google Ads next to Microsoft Advertising. The same terms rarely cost the same on both; Microsoft's cheaper inventory often converts at a lower CPA, so ignoring it leaves money on the table.
2. **Account**: brands commonly run one per market or label. Reading account by account stops a strong home market from masking a weak one it quietly subsidizes in the blended total.
3. **Campaign**: holds the budget and targeting. This is where you find an uncapped generic campaign running 28% over budget at a poor cost per sale while a cheaply converting brand campaign sits pinned at its cap. Fix the caps before touching a keyword.
4. **Ad group**: a set of closely related keywords and the ads that answer them.

On top of the native structure, an optional **cluster overlay** groups campaigns and queries by the categories the business actually thinks in (product line, region, intent). A healthy-looking category aggregate can hide one line burning budget at 1.3x return while another quietly carries it; only the line-level read surfaces that.

## Metrics that matter (and their traps)

- **Ad group size**: Google's guidance is one narrow theme per group, commonly five to fifteen closely related keywords ([Google Ads Help](https://support.google.com/google-ads/answer/6372655)). Trap: the one giant ad group (fifty loose keywords under one generic ad) sags CTR and pays more per click for worse placement. Splitting a grab-bag into tight themed groups can roughly triple CTR at under half the CPC, purely from relevance.
- **Quality score**: fed directly by tight theming. A top score can roughly halve CPC; a bottom score can multiply it nearly fivefold.
- **Category-level aggregates**: useful, but never a verdict. Trap: reading the aggregate and stopping; the leak lives one level down.
- **Search-term visibility**: since a 2020 privacy change, the platform only reports terms searched by a significant number of users. Measured visibility of click-driving queries dropped from roughly 75–85% to around 40–60%. Trap: treating the search-terms report as a census. It is a strong sample; act on it directionally and lean on campaign and ad-group levels, which are complete, for spend decisions.

## Interview prep

**"CTR softened account-wide. How do you find where?"**
A strong candidate drills the hierarchy (service, account, campaign, ad group) rather than tuning the account average, and asks whether multiple markets or engines are blended in the top-line figure.

**"What is wrong with a fifty-keyword ad group, concretely?"**
One ad must answer every keyword, so it answers none: relevance drops, CTR sags, quality score falls, and every click costs more. They cite the fix: tight themes of five to fifteen keywords with copy mirroring the query.

**"Would you trust a query-level analysis of wasted spend?"**
Directionally yes, exhaustively no. They know the visible terms are real and actionable, but a meaningful chunk of spend pools in the hidden long tail, so "these are all the terms we spent on" is a claim the data no longer supports.

**"Why compare Google and Microsoft side by side?"**
Same terms, different auctions. Cheaper clicks that convert on the smaller engine justify shifting a slice of budget, but only if the comparison uses consistently defined metrics, not two exports with mismatched conversion scoping.
