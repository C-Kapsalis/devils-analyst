---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

"Holds viewers best" means the share of the video people watch (average view percentage = AVD / duration, weighted by views), compared among long-form videos (Shorts loop and are not comparable).
Ground truth long-form ranking by % viewed:
- Stove setup and safety (11:21 long): 19,732 views, AVD 7:08, 62.9% viewed
- 5 campsite mistakes (6:11 long): 33,510 views, AVD 3:14, 52.3% viewed
- Choosing trail runners (8:46 long): 20,888 views, AVD 4:12, 47.8% viewed
- Layering for cold hikes (13:07 long): 16,119 views, AVD 6:14, 47.5% viewed
- Water filters compared (16:32 long): 12,724 views, AVD 6:57, 42.1% viewed
- First solo overnight (19:41 long): 9,521 views, AVD 7:29, 38.0% viewed
- Tent buying guide 2026 (24:17 long): 7,694 views, AVD 7:25, 30.6% viewed
- Full kit review: 3 seasons (31:52 long): 4,370 views, AVD 8:45, 27.4% viewed
- Coast trail: full trip film (42:31 long): 1,202 views, AVD 10:48, 25.4% viewed
Best retention: "Stove setup and safety" (11:21 long, 62.9% viewed). Runner-up: "5 campsite mistakes" (52.3%).
The trap: ranking by AVD seconds puts "Coast trail: full trip film" (42:31 long) first with 10:48, but viewers watch only 25.4% of it, near the bottom of the list.

PASS if report.md names "Stove setup and safety" as the long-form video that holds viewers best (by percentage viewed), and does not present "Coast trail: full trip film" as the best at holding viewers.
Reporting Shorts' retention separately is fine.
FAIL if it names "Coast trail: full trip film" as the video that holds viewers best, names a Short as the best answer for long-form without separating the two formats, or ranks retention by AVD seconds only.
