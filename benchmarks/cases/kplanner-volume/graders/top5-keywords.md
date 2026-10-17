---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground-truth top 5 keywords by average monthly search volume: hiking boots (20,765), rain jacket (18,248), backpacking tent (16,560), trail running shoes (13,980), gore tex jacket (11,858).
Wrong rankings:
- By number of rows in the export (this only counts months tracked x 10 results, so it favours keywords tracked all 4 months)
- By summing volume across all rows: rain jacket, gore tex jacket, hiking boots, waterproof hiking boots, mens rain jacket
- By summing volume across months (penalises keywords tracked for fewer months, e.g. "backpacking tent" and "trail running shoes" have only 1 month and "hiking boots" only 2): rain jacket, gore tex jacket, hiking boots, waterproof hiking boots, 2 person tent

PASS if report.md's per-keyword volumes match the ground-truth averages above (within 5%) for the keywords it shows, AND its top 5 either (a) includes at least 4 of the ground-truth top 5, or (b) deliberately trades volume against competition_index / CPC / our current ranking (harboroutdoor.com) with that reasoning stated, using the correct per-keyword volumes.
FAIL if the per-keyword volumes it uses are inflated row sums (roughly 10x or more the values above) or month sums, or if the top 5 is ordered by row count or summed volume.
