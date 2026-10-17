---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth conversion rate (conversions / sessions) by device, Q3 2026:
- mobile: /lp-a 1.52% (766/50,314) vs /lp-b 1.10% (88/8,020), z = 2.9
- desktop: /lp-a 6.26% (338/5,398) vs /lp-b 5.05% (2,166/42,892), z = 3.8
- tablet: /lp-a 3.41% (115/3,370) vs /lp-b 2.26% (72/3,192), z = 2.8
/lp-a converts better on EVERY device. Its blended rate is lower only because 85% of its sessions are mobile (the lowest-converting device) versus 15% for /lp-b.
At the same device mix (both pages' combined mix: mobile 52%, desktop 43%, tablet 6%): /lp-a 3.65% vs /lp-b 2.85%.

Wrong answer produced by the common mistake: blended totals, /lp-a 2.06% vs /lp-b 4.30%, so "/lp-b converts about 2.1x better; send all paid traffic to /lp-b".

PASS if report.md picks /lp-a as the better-converting page (or the page to send paid traffic to) because it wins within each device / at a comparable device mix.
FAIL if report.md picks /lp-b, or declares /lp-b the better converter based on the blended rates, or gives no clear answer.
