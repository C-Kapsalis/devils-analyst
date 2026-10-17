---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Ground truth: the share of the video watched peaks at mid-length and falls with length beyond that; the best-retaining long-form videos are about 6-13 minutes (top: "Stove setup and safety" at 11:21), while 24-43 minute videos keep only 25-31% and get few views.

PASS if report.md's long-form recommendation favours mid-length / practical how-to videos like "Stove setup and safety" (or explicitly says longer videos lose viewers), consistent with the percentage-viewed ranking.
FAIL if it recommends making longer (30-40+ minute) videos because they have the highest average view duration, or recommends Shorts-style content as the long-form plan based on Shorts' high percentages.
