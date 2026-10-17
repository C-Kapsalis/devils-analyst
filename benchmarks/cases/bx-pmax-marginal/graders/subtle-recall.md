---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. Store visits in the value. PMax conv_value includes modelled "Store visits" (800 in September worth €17,600, 22% of PMax value). Purchase-only ROAS in September is 2.95x vs the reported 3.76x. Found if report.md separates store visits from purchases and reads PMax on purchases.
2. Marginal return of the last increase. August to September PMax cost rose €7,601 while purchase value rose €5,666: marginal ROAS 0.75x vs break-even 2.63x at 38% margin, although the September average purchase ROAS is 2.95x. Found if report.md computes the incremental/marginal return of the added budget (or says the extra spend returned far less than the average) with a number.
3. Cannibalisation of Standard Shopping. From July to September PMax purchases rose by 120 while Standard Shopping fell by 111; combined PMax + Shopping purchases changed 1.8% while their combined cost rose 54%. Found if report.md says PMax growth came largely from Shopping (overlap / shift) or reads the two together.
4. Display and YouTube inside PMax. In September Display + YouTube took €6,074 (28% of PMax cost) for 11 of 372 purchases (3%). Found if report.md flags this spend share vs purchase share.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
