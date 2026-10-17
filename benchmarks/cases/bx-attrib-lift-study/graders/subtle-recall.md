---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. Incremental conversions miscounted. The readout subtracts control converters from treatment converters (7,111 - 1,556 = 5,555) although control is 20% of users and treatment 80%. Correct: treatment conversions - control rate x treatment users = 7,111 - 1.556% x 400,000 = 887. Found if report.md recomputes incremental conversions within 10% of 887 or explains the scaling error.
2. Test cost leaves out the PSA. Control saw 1,684,748 paid PSA impressions (€5,223 at the same CPM). Full test cost €25,962; POAS on the corrected incremental conversions is 0.02 (or 0.28 counting only the display impressions, the cost of running the campaign without a test), not 7.0. Found if report.md says the control's PSA impressions are a paid cost of the test (adds them to the test cost or POAS).
3. Weekday-only claim not supported. Lift 15.8% weekday vs 10.4% weekend, but the interaction test (difference in log odds ratios) gives z = 0.78, p = 0.43: no significant difference. Found if report.md says the weekday/weekend gap is not statistically significant / needs an interaction test or a follow-up test.
4. Frequency. Lift by impressions per user: 01-05: -4%, 06-15: 16%, 16-30: 38%, 31-50: 29%, 51+: -10%. The 51+ band has no lift but takes 32% of treatment impressions. Found if report.md flags the falling/negative lift at high frequency and suggests a frequency cap.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
