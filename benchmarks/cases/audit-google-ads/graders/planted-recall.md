---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The account export contains 7 planted problems. Answer key (September 2026, margin per sale $31.50, target CPA $30):

1. Micro actions counted as conversions. Newsletter signup and Account created are included in Conversions (include_in_conversions TRUE). Account conversions 1,439, of which purchases 572. CPA on all conversions $5.00; CPA on purchases $12.57. Counts as found if report.md says only purchases should count as the conversion (or Smart Bidding is optimising toward sign-ups) and gives a purchase CPA within 5% of $12.57 or per-campaign purchase CPAs.
2. Brand leakage. Generic campaigns serve brand queries (tidewater swimsuits, tidewater swim sale, tidewater goggles): $252 of generic cost and 61 of 171 generic purchases (36%). Generic purchase CPA is $35.05 as reported but $52.19 without brand queries. The brand campaign also serves the generic query "swimming costume". Counts as found if report.md flags brand terms inside generic campaigns (brand negatives needed); the reverse case or the ex-brand CPA is a bonus, not required.
3. Search-term waste. Informational or irrelevant terms with zero purchases: how to wash a swimsuit, swimsuit model jobs, how to stop goggles fogging, free kids swim lessons, second hand wetsuit, wetsuit repair, wetsuit hire near me; total $696. Counts as found if report.md names at least three of these terms (or the clusters) and recommends negatives; a total within 10% of $696 is a bonus.
4. Profitable campaign capped by budget. Generic - Goggles: purchase CPA $13.24 ($19.56 without its brand query, still below target), loses 49% of impression share to budget and spends its full cap ($662 on a $22 daily budget), while Generic - Swimsuits is uncapped at a purchase CPA of $37.97 (over target) and loses impression share to rank, not budget. Counts as found if report.md recommends more budget for Goggles (or moving budget from Swimsuits to Goggles) citing the budget-lost share.
5. CPC above break-even. Generic - Kids Swimwear is called efficient for clicks under a dollar, but its CPC $0.93 is above its break-even CPC of $0.74 (margin $31.50 x purchase CVR 2.34%); purchase CPA $39.97. Counts as found if report.md says Kids Swimwear loses money per click or its CPA is above target/margin despite the low CPC.
6. Device modifiers on Target CPA. -30% mobile (and -20% tablet) modifiers sit on Generic - Swimsuits and Generic - Goggles, which use Target CPA; automated bidding does not apply them as set, so the "saved us money" claim is not supported. Counts as found if report.md says these modifiers have little or no effect under Target CPA.
7. Broad match plan. Broad has the lowest CPC ($0.63) but the worst cost per sale ($86.34 vs exact $37.64 and phrase $21.90), so shifting budget to broad for cheap clicks is wrong. Counts as found if report.md rejects the broad-match plan on cost per sale.

List which ones were found in your reasoning.
PASS if report.md identifies at least 6 of the 7 problems, each with its substance (a vague mention such as "review search terms" does not count).
FAIL if it identifies fewer than 6.
