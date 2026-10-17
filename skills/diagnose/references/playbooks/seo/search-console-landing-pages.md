---
title: Search Console: coverage gaps and the snippet shortlist
question: Which pages need work, and what work
order: 9
---

Use this when the question is "which pages need work, and what work?" The goal is two page-level fix lists: pages that never surface (coverage gaps) and pages that surface but nobody clicks (the snippet shortlist), each with a concrete action attached.

## The framework

1. Open Search Console's **Performance report** and switch to the **Pages** tab, with impressions, clicks, CTR, and average position enabled.
2. **Coverage gaps first.** Compare your sitemap against the pages appearing here: any page in your sitemap with zero or absent impressions never surfaces at all: it is not indexed, blocked, or so off-target Google never shows it. Fix path: confirm indexability (check for stray `noindex`, use URL Inspection), give it real content, and point descriptive internal links at it.
3. **Snippet shortlist.** Sort by impressions descending and scan CTR. High-impression, low-CTR pages are the highest-ROI rewrites on the site: the ranking is already won, only the title and meta description are failing.
4. **Drill each shortlisted page to its queries** (filter by page, then view queries) to confirm it surfaces for what it was built for. If it ranks for another page's intent, you have keyword cannibalization: consolidate to one page per intent rather than rewriting two snippets.

## Metrics that matter, and their traps

- **Zero-impression sitemap pages**: the silent failure almost nobody checks. Trap: Search Console will not volunteer the list; you have to bring the sitemap and find the absences. A classic cause is a `noindex` left on after a launch.
- **Impressions × CTR per page**: a page at 210,000 impressions, position 4.7, and 0.2% CTR is the top of the snippet shortlist; one meta rewrite there beats a quarter of link-building.
- **Position 4-20 on a page's target query**: the rank-push list: content depth and internal anchors, not snippet work.
- **Page-to-query match**: a page can earn impressions on an intent it cannot serve; the CTR looks like a snippet problem but the fix is a different page. Always drill before prescribing.

## Interview prep

**"How do you find pages that are invisible in search?"**
Diff the sitemap against pages earning impressions: Search Console never volunteers the absences. Then triage each gap: indexability first (noindex, blocks), then thin content, then internal linking. These pages cost nothing to find and a lot to ignore.

**"What makes a page the highest-ROI fix on a site?"**
High impressions, decent position, terrible CTR: the rank is paid for and the snippet is refusing the click. A title and meta rewrite is hours of work against a quarter of link-building for the same click gain.

**"A page's CTR is low. How do you know whether it is the snippet or the page?"**
Drill to its queries. If it surfaces for its own intent, rewrite the snippet. If it surfaces for another page's intent, or alongside a sibling page, it is cannibalization or a mismatch, and the fix is consolidating or building the right page.
