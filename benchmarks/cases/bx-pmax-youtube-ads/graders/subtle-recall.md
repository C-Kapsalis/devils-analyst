---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. The cheapest-CPV ad hides the brand. "Trail Story 45s" has the lowest CPV (€0.018) but only 21% of impressions play to 25%, and the brand first appears at second 38 of 45, which only about 7.5% of impressions reach. Cost per 1,000 impressions that reached the brand moment: Trail Story €26.44, Saddle Up 20s €13.67 (brand at second 2), Commute Hack 30s €15.38. Found if report.md points to the quartile drop-off together with the late brand reveal (or a retention/brand-exposure-adjusted cost) and says cheap CPV is the wrong yardstick.
2. Viewers vs non-viewers is not an ad effect. The 2.9x comparison (viewers 3.2% vs non-viewers 1.1%) compares people the platform targeted (likely buyers) with people it did not; it needs a randomised holdout / lift test. Found if report.md rejects or caveats the 2.9x claim as selection / not causal and suggests a lift test or holdout.
3. Frequency wear-out. Weekly frequency rose from 2.1 to 6.9 while view rate fell from 29% to 14%, with unique users flat (so "reach is growing" is not true). Found if report.md flags rising frequency with falling view rate (or flat unique reach) and suggests a cap or creative refresh.
4. Made-for-kids placements. 24% of impressions ran on channels marked made_for_kids. Found if report.md flags these placements and suggests excluding them.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
