---
type: llm
weight: 2
focus: { source: file, path: dashboard.html }
---

Ground truth: email revenue rose from $28,900 to $32,128 (+3,228), but a segment sent only in September (VIP repeat buyers) brought $10,400; the segments sent in both months fell from $28,900 to $21,728.

PASS if the dashboard's title or opening headline (the first sentence a reader sees, above the charts) states this answer: that the overall rise comes from the new segment while the continuing segments declined.
FAIL if the title is only a topic ("Email performance", "September report") with no answer, or if the headline presents the revenue rise as general improvement.
