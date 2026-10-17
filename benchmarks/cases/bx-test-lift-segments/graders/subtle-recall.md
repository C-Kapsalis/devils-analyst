---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The readout contains 4 planted problems. Ground truth (computed from lift_by_segment.csv):

1. Incremental conversions on the wrong base. Incremental = test converters - control rate x test users = 2,788 - 1.172% x 209,874 = about 329, not lift x control conversions = 141 (the control cell is only 30% of users). Incremental CPA is about EUR 28 and POAS about +0.45, not -0.38: the campaign makes money. Counts as found if report.md recomputes incremental conversions on the test cell (any figure within 10% of 329) or gives a positive POAS / profit.
2. Device split is not a tested difference. Mobile lift 18.0% vs desktop 6.2%; the test of the difference (interaction) gives z = 1.43, p = 0.15. Counts as found if report.md says the device gap is not statistically established (or is within noise / needs an interaction test) so stopping desktop is not supported.
3. 65+ cell too small. 65+ has 545 control users and 4 control converters (17 in test); the 83% lift is unreadable. Counts as found if report.md flags the tiny 65+ sample/converter count.
4. Frequency read as cause. Users with 10+ exposures convert at 2.27% in test but 2.38% in the PSA control too: lift at 10+ is -4.6% (95% CI -17% to 9%) vs 20.8% below 10 exposures (difference p = 0.0034), while 10+ users take 38% of test impressions. Heavy-exposure users are likely buyers anyway. Counts as found if report.md compares 10+ test vs control (or says the high conversion rate is selection, not exposure) and says raising the cap is not supported.

List which were found, with the evidence quoted.
PASS if report.md identifies at least 3 of the 4, each with its substance (a number or the specific comparison). FAIL otherwise.
