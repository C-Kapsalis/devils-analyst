---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key:

1. Post-purchase is not incremental. It has the most attributed revenue ($170,158), but in the holdout report profiles receiving it buy at 8.0% against 7.8% for the holdout: no measurable lift. Abandoned checkout converts 15.4% vs 9.1% for its holdout, roughly $41,340 incremental in Q3. Counts as found if report.md uses the holdout to say post-purchase adds little or nothing, or that abandoned checkout is the flow with proven lift.
2. Open-based attribution. Attribution is "opened or clicked within 5 days", and 85% of post-purchase attributed revenue is open-only (opens can be fired by privacy proxies and these customers just bought anyway). Counts as found if report.md says attributed revenue is inflated by open-based attribution (or reads flows on click-attributed revenue instead).
3. Win-back with no real exit. The flow sends six messages to profiles with no order in 180 days; exit is only "placed order". WB4-WB6 complaint rates are 0.14%, 0.17%, 0.17% (above the 0.1% line) and bounce rates 3.1%, 3.4%, 3.6%. Counts as found if report.md flags the late win-back messages' complaint or bounce rates, or the lack of an exit / suppression rule for non-responders.
4. One welcome message drives unsubscribes. W3 "Bestsellers" unsubscribes at 0.85%, above about 0.5%, while the welcome flow overall is 0.38%. Counts as found if report.md flags W3 specifically.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 4, each with evidence (a number or message name).
FAIL if fewer than 3.
