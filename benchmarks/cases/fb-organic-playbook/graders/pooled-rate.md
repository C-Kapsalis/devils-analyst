---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Engagement rate by post type must be pooled (sum of engagements / sum of reach): video 6.43%, image 3.32%, link 1.87%, so video is best and link posts are worst.
The trap: 6 link posts reached only 45-102 people each but have 29-44% engagement rates. Averaging per-post rates gives video 6.56%, image 3.29%, link 8.31%, which wrongly makes link posts look best.

PASS if report.md's engagement rates by type are the pooled ones (within 10% relative) or otherwise ranks video above image above link on engagement rate, AND it does not claim link posts have the highest engagement rate.
FAIL if it reports link posts as the best-engaging type or uses the per-post-average rates (video 6.56%, image 3.29%, link 8.31%) for its ranking.
