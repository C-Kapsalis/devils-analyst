---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Engagement = reactions + comments + shares. Ground truth from the post data:
- Post type drives engagement. Engagement rate (total engagements / total reach, pooled): video 6.43%, image 3.32%, link 1.87%. Video is best.
- Hashtags do NOT drive engagement. Across all posts, n_hashtags correlates with engagements (r = 0.65), but only because videos carry more hashtags (average hashtags: video 6.8, image 2.8, link 1.3). Within each post type the correlation is about zero (video r = -0.15, image r = -0.09, link r = 0.04).

PASS if report.md identifies video (post type) as the main driver of performance AND does not recommend adding more hashtags as a way to lift engagement (it may say hashtags show no effect once post type is accounted for, or simply not recommend them).
FAIL if it recommends using more hashtags (or a hashtag count) to boost engagement, or claims hashtags drive engagement based on the raw cross-post correlation.
