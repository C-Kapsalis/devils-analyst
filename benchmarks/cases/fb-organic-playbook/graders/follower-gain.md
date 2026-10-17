---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

fan_count is the page's lifetime follower total on each day; fan_count_diff is the daily net change.
Ground truth September 2026 follower gain = sum of September fan_count_diff = fan_count on Sep 30 (25,289) minus fan_count on Aug 31 (24,921) = 368.
Also acceptable: Sep 30 minus Sep 1 fan_count = 361.
Wrong answers: summing fan_count over September (752,778); reporting the total follower count (25,289) as the gain.

PASS if report.md states a September net follower gain between 361 and 368 (inclusive, allow plus or minus 2).
FAIL if it gives 752,778 or 25,289 as the gain, or any other number outside that range, or gives no September gain.
