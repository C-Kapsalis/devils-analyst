---
title: Auditing a Performance Max campaign
question: What is the step-by-step read that tells you whether Performance Max is actually working
order: 6
---

Performance Max exposes no keywords and no real ad groups (its asset groups report as a single `performance_max` pseudo ad group), so the disciplined audit is deliberately narrow: volume at what unit price, then what the campaign actually converts into. That thinness is also what makes it a clean, repeatable review.

## The framework

1. **Isolate the campaign type structurally.** Filter your reporting on the ad group type (or campaign type) enum `performance_max` rather than on campaign names. The enum is set by the platform, so the filter works on any account; name-based filters break the moment naming conventions change.
2. **Read the trend: clicks against CPC by month.** Volume at what unit price. Clicks up with flat or falling CPC is healthy scaling; clicks up with rising CPC is bought growth, acceptable only if the conversion read in step 4 keeps pace.
3. **Read the campaign table.** Per campaign: impressions, clicks, CTR, CPC, conversions, conversion value. This is the whole picture PMax allows, so read it carefully rather than wishing for the query-level detail Google withholds.
4. **Choose your conversion lens deliberately.** Conversion columns should start blank until you pick one value event: a purchase, not a blended total that mixes a signup with a large order. Read the campaigns through that single lens.

## Metrics that matter, and their traps

- **Clicks vs CPC over time**: the cleanest efficiency read available. Trap: celebrating click growth that was simply bought with a rising unit price.
- **CTR at the campaign-type level**: a scaling plausibility check (an account might show, say, millions of impressions at a ~2% CTR and a low CPC). Trap: comparing it against search-campaign CTRs; the inventory mix is different.
- **Conversions under one lens**: under a purchase lens the split gets stark: one feed-driven campaign can carry thousands of orders while a "new acquisition" campaign carries a few hundred. Trap: reading legitimate sparsity as a broken number; a campaign type that never fires a given event is telling you something, not failing to report.
- **Conversion value per campaign**: weigh campaigns on revenue returned, not on the conversion count the platform chose to headline.

## Interview prep

**"Walk me through how you would check whether PMax is working, in five minutes."**
A strong candidate names the sequence: filter to the PMax campaign type structurally, read clicks against CPC for scaling health, then the campaign table, then apply a single purchase lens. They resist the urge to hunt for keyword detail that does not exist.

**"Conversions are blank on half your PMax report. Broken data?"**
Ask which conversion lens is applied first; a blended default hides more than a blank column. And a campaign that never fires a given event is legitimate sparsity, not a pipeline bug.

**"Clicks doubled month over month. Good news?"**
Only alongside the unit price and the conversion side: doubled clicks at a doubled CPC with flat purchases is bought growth, the shape that precedes a quiet ROAS collapse.
