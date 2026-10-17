# Decoys: things that look wrong and are fine

Flagging a correct item costs the review its credibility. Before keeping a
finding, check it is not one of these. If the report states the item
correctly, list it under "Checked and fine" instead.

| Looks wrong | Why it is fine | Flag only if |
|---|---|---|
| Search Console clicks higher than GA4 organic sessions | Different systems: Google counts the click, analytics counts a consented, tagged session | the report subtracts one from the other as "lost traffic" |
| Ad platform clicks a few percent above analytics sessions | Same reason: blockers, consent, bounces before the tag fires | the gap is over about 25% or changed suddenly |
| Sessions slightly under email clicks on every row | Normal; some clicks never load the page or are scanner clicks | a send has clicks and zero sessions (broken tagging) |
| Display CTR around 0.3-0.6% | Normal for display; it is a reach channel | display is judged or cut on CTR |
| Brand search CTR of 30-50% and the lowest CPA | Normal for brand terms | brand is blended into the account CTR or CPA, or called fully incremental |
| Phrase or exact match with the highest CPC | Precise matches cost more per click | cost per sale is also worst |
| Retargeting ROAS far above prospecting | Expected: it closes demand others created | budget is moved from prospecting on that basis |
| Direct traffic around 10-25% and stable | Bookmarks, typed URLs, apps | a sudden spike lines up with untagged campaigns |
| Direct credit identical under every attribution model | GA4 models give direct credit only when the whole path is direct | the report calls it "robust" as evidence |
| A median order value well below the mean | Expected with a few large orders; the median is the right typical value | the report quotes the mean as typical and acts on it |
| Rounding differences under 1% | Rounding | the rounded figure flips a ranking or a threshold |
| Open rate shown as a trend with a privacy caveat | Correct use of opens | opens rank campaigns or are the verdict |
| A rate computed as sum / sum that differs from the average of the row rates | The report did it right; the row average is the wrong one | never |
| A smaller period total than last period when the period is shorter | Check per-day values | per-day values also fall and the report denies it |
| Unsubscribe rate 0.1-0.4% per send | Normal band | above about 0.5% on a send |
| Complaint rate under 0.1% on every send | Normal | one send is above 0.1%, hidden in an average |
| A CTOR of 8-15% | Normal band | the report ranks sends on it with tiny opens |
| Sample split of 49.9 / 50.1 in a 50/50 test | Within chance; check with chi-square | the chi-square statistic is above 10.8 (p < 0.001) |
| Position quoted as an impression-weighted average | Correct | the average is unweighted |
| Last-click and data-driven columns that differ | Expected when DDA is active and has volume | they are identical while DDA is claimed |
| A forecast drawn dashed and labelled beyond the data | Correct | the line is solid or unlabelled |

Rule of thumb: a decoy is a pattern that has a normal, known cause. Flag it
only when the report draws a wrong conclusion from it, and then the finding is
about the conclusion, not the pattern.
