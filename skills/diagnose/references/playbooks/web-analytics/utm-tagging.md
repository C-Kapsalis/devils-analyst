---
title: UTM tagging
question: How do you group one campaign across every channel and trace it from click to revenue
order: 4
---

"What did the spring sale earn across every channel?" is a simple question that routinely costs a day, because each platform names the same campaign its own way and there is no shared key to group on. UTM tagging is the boring, upstream discipline that gives the day back: five parameters stamped identically on every link, on every channel, so one campaign is one groupable, traceable thing instead of three things you hand-match in a spreadsheet.

## The framework

1. **Know the five parameters.** `utm_source` = the specific platform (google, meta, your email tool). `utm_medium` = the channel type (paid search, paid social, display, email). `utm_campaign` = the theme that ties one effort together across platforms (the shared key you group on). `utm_content` = which creative or placement earned the click. `utm_term` = the paid keyword. Google Analytics reads them straight off the landing URL ([Google Analytics Help](https://support.google.com/analytics/answer/10917952)).
2. **Make the campaign key boring and identical everywhere.** One house style (lowercase, underscores, never improvised) so `spring_sale` collapses into a single row no matter which channel carried the click. The shared key is the join every cross-channel read depends on, and it exists only because you wrote it consistently.
3. **Read at altitude.** Consistent tags let you cluster campaigns hierarchically: channel, then objective, then theme, then creative. The blended top is on-target and unactionable; the euro to move shows up a level down, where an over-fed prospecting push and a starved retargeting cluster stop hiding in each other's averages.
4. **Trace click to revenue.** The tags survive from the platform to the till: web analytics names the visit by the campaign, then records the session, the transaction, the revenue. In a four-channel trace, display can pull ~7,800 sessions and earn ~£5,100 while email pulls ~2,400 and earns ~£14,900: a click ranking that inverts on revenue, visible only because the key matched on every link.
5. **Tag every channel**: auto-tagged paid search must still match the house scheme; untagged banner and bio links vanish into "direct"; hand partners tagged links; even a QR code on a poster can carry UTMs.

## Metrics that matter, and their traps

- **utm_campaign consistency**: the one parameter that must be written identically everywhere. One mistyped name splinters a campaign into unmatchable rows.
- **Sessions / transactions / revenue by campaign key**: the cross-channel read itself. The trap: judging channels on sessions; the click ranking often inverts on revenue.
- **Revenue by utm_content**: which creative actually carried the campaign; without it, a winning variant hides inside the channel total.
- **The "direct" and untagged bucket**: the tell of tagging drift: buyers look like anonymous traffic and revenue lands nameless. Nothing is broken, the money is just uncredited.
- **Tagging coverage**: the share of traffic and revenue reconciling to a named campaign. A scheme is only as good as its least disciplined link.

## Interview prep

**"Design a UTM scheme for a multi-channel launch. What matters most?"**
A strong candidate makes it dull: source = platform, medium = channel type, campaign = one theme in one house style. They emphasize the campaign key's cross-platform consistency over any clever naming, because grouping is the whole point.

**"Direct traffic spiked after the campaign started. What is your first hypothesis?"**
Untagged links: banners, bio links, or a partner sending traffic under whatever they pleased. They audit link tagging before inventing a story about brand lift.

**"Paid search auto-tags. Do you still need UTMs there?"**
The campaign name still has to match the house scheme, or paid search sits in its own silo instead of grouping with the same theme on email and social.

**"How do you answer 'what did the campaign earn' when finance asks?"**
Group every tagged link on the campaign key, read on-site transactions and revenue per channel, and disclose coverage: where tagging drifted, the figure is a floor, and the fix is discipline, not a different tool.
