# Finding examples

Synthetic examples. They show the shape and the level of proof each finding
needs.

## One Must fix finding

```
1. **Total ROAS counts the same sales twice** (summary, "Blended ROAS 5.4x")
   - **What it says:** Paid media returned 5.4x: Google 61,200 plus Meta
     48,900 in revenue on 20,400 of spend.
   - **What is wrong:** Google and Meta each report sales they touched, on
     their own windows, so the same order is often claimed by both. Their sum
     (110,100) is above the store's total revenue for the month (84,300),
     which includes organic and email. Against the store total, all revenue
     on paid spend is at most 84,300 / 20,400 = 4.1x, and the paid share is
     lower still.
   - **Fix:** Replace the line with "Store revenue 84,300 on 20,400 paid
     spend (4.1x, all channels). Platform claims: Google 61,200, Meta 48,900;
     they overlap." Judge each channel against the store or analytics total,
     not its own claim.
   - **If you skip it:** The plan to raise paid budget by 30% rests on a
     return that does not exist; at 4.1x or lower the extra spend may not pay
     back at the 35% margin.
```

What makes it a good finding: the claim is quoted with its number, the
recomputation uses figures the reader can find, the fix is ready to paste,
and the cost is a decision, not "accuracy".

## A finding that should be dropped

"The report uses a pie chart for device split." There are three slices, all
labelled with percentages, and nobody decides anything from it. Not a
finding.

"Search Console shows 12,400 clicks but GA4 shows 10,900 organic sessions,
so 1,500 visits are missing." The report itself says the two will not match.
Decoy; list it under "Checked and fine" if at all.

## A clean verdict

```
Verdict: Send it.

What this report says: Paid search CPA on purchases fell from 41.20 to 38.90
in September while spend held at 18,000; the report credits lower generic
CPCs and recommends keeping budgets flat.
Who decides what: the marketing lead decides whether to keep budgets flat.

Checked and fine: totals and every CPA and CTR recompute from the export
(ratio of sums); conversions are scoped to purchases; brand and generic are
split; September is compared with August per day and with September last
year; the CPC claim matches the auction data; the recommendation names the
number to watch (generic CPA under 45) and when (mid-October).
Not checked: revenue against the store total (no store export provided).
```

No padding: a clean report gets a short review.
