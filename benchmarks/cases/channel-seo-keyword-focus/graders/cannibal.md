---
type: llm
weight: 2
focus: { source: file, path: report.md }
---

Ground truth: "waterproof trail running shoes" (3,600/month, transactional intent) ranks with two different URLs: the category page /trail-running-shoes/waterproof at position 14 and the blog post /blog/waterproof-vs-breathable at position 19. The two pages compete with each other (keyword cannibalisation). One page should own the term (the category page, matching the transactional intent), with the blog post re-targeted to an informational angle and/or linking to the category page (or consolidated / canonicalised).

PASS if report.md notes that two URLs compete for "waterproof trail running shoes" and recommends that one page (ideally the category page) owns it.
FAIL if this is not mentioned.
