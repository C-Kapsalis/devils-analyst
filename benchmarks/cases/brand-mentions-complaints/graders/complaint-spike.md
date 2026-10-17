---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: Brightwell mentions Q2 4,000 -> Q3 6,400 (+60%); share of voice 33.3% -> 42.4%. But negative mentions rose 600 -> 2,300 and net sentiment ((positive - negative) / total) fell from +25.0% to -6.2%. Delivery-tagged mentions went 300 -> 2,500 (1,950 of them negative in Q3, concentrated from mid-July), accounting for about 92% of the mention increase. Competitors' sentiment was stable (Lunara +23% -> +23%, Kitecraft +23% -> +23%).

Naive answer: "mentions +60%, share of voice 42%, the campaign was a success".

PASS if report.md shows that most of the mention growth is negative and/or delivery-related AND that net sentiment fell (or turned negative).
FAIL if report.md presents the +60% mentions or the share-of-voice gain as evidence of campaign success without this breakdown.
