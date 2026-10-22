# channel-seo-keyword-focus

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/channel-audit/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/channel-seo-keyword-focus/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> resources/keyword_rankings.csv is our Semrush organic positions export for northpeak.com (domain authority 34). We have one content person this quarter. Which keywords should our SEO work focus on? Pick up to 8 and say what to do for each in report.md.
> 
> Save report.md in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `bands` | PASS | PASS | A: 8 of 8 in positions 4-20; B: 7 of 8 (one pick at position 3), no excluded keyword |
| `cannibal` | PASS | PASS | both: category page owns "waterproof trail running shoes" |

## Arm A answer (with skill)

````markdown
# northpeak.com SEO keyword focus

Source: resources/keyword_rankings.csv (Semrush organic export, 20 keywords, domain authority 34, one content person this quarter).

## Verdict
Eight keywords, in this order:
1. waterproof trail running shoes: fix (two URLs compete; consolidate first).
2. trail shoe size guide: quick win, push from rank 4 into the top 3.
3. best trail running shoes for beginners: push from rank 7.
4. zero drop trail shoes: push from rank 5.
5. trail running vest: push from rank 9; largest volume in the band.
6. trail running shoes wide toe box: push from rank 11; dedicated page exists.
7. how to clean running shoes: push from rank 17; large volume, low difficulty, but awareness intent.
8. trail running gaiters: push from rank 13; low difficulty, low volume.

Leave alone this quarter: rank 1-3 terms (maintain), rank 50+ head terms, and the action-intent sale term.

## Selection rule
Per channel-audit section 5: rank 4-20 first, then intent matching a funnel stage, then difficulty against domain authority 34, then volume as tie-breaker. Rank 50+ is out of reach this quarter ("running shoes" 64, "trail running shoes" 57, "marathon training plan" 72, "running socks" 88).

## The eight keywords
| # | Keyword | Rank | Volume | KD | Intent | Current URL | Action |
|---|---|---|---|---|---|---|---|
| 1 | waterproof trail running shoes | 14 and 19 | 3600 | 33 | transactional | /trail-running-shoes/waterproof (14); /blog/waterproof-vs-breathable (19) | Fix cannibalization. Make the category page the single owner: fold the blog's waterproof content into it, link the blog to it, and re-aim the blog at "waterproof vs breathable running shoes" (volume not in export; check first). |
| 2 | trail shoe size guide | 4 | 1300 | 15 | informational | /size-guide | Quick win. Refresh the guide, match title and H1 to the term, add a sizing FAQ. |
| 3 | best trail running shoes for beginners | 7 | 4400 | 31 | commercial | /blog/best-trail-shoes-beginners | Refresh: comparison table, current model year, links to recommended product pages. Target top 3. |
| 4 | zero drop trail shoes | 5 | 1900 | 22 | commercial | /trail-running-shoes/zero-drop | Add a short zero-drop explainer above the grid; link from the beginners post. |
| 5 | trail running vest | 9 | 5400 | 29 | transactional | /vests | Product detail copy and fit notes; link from trail shoe pages. |
| 6 | trail running shoes wide toe box | 11 | 2900 | 27 | commercial | /trail-running-shoes/wide | Deepen existing page (fit guidance, who it suits); link from size guide. |
| 7 | how to clean running shoes | 17 | 6600 | 21 | informational | /blog/clean-shoes | Add links to care products; check conversions before investing more (awareness intent). |
| 8 | trail running gaiters | 13 | 1600 | 19 | transactional | /accessories/gaiters | Fit and use copy; link from trail shoe pages. |

## Excluded, with reason
- trail running shoes sale (rank 6, volume 2400, KD 24, transactional): action intent, expiring sale URLs; usually bought through paid search.
- how to start trail running (rank 3, volume 8100): maintain only.
- Brand terms "northpeak running" (1), "northpeak shoes" (2), "northpeak trail x2 review" (2): maintain.
- best running shoes for flat feet (rank 24) and carbon plate running shoes (rank 41): outside 4-20; next quarter at earliest.
- running shoes (64), trail running shoes (57), marathon training plan (72), running socks (88): rank 50+.

## Sequence for one content person
- Weeks 1-2: fix #1 and refresh #2 (edits, not new pages).
- Weeks 3-8: refresh #3 and #4.
- Weeks 9-12: #5 to #8, then re-check ranks.

## Verify
- Track the eight keywords monthly in the same Semrush project.
- Target: each keyword in the top 3 within the quarter; #1 owned by one URL with no second URL in the top 20.
- Check organic sessions and conversions per landing page in GA4 at quarter end.

## Caveats
- The export has no conversions, margin or revenue per keyword. Picks rest on rank band, difficulty, intent and volume, not profit. For a profit ranking, send margin per order and conversions per landing page.
- Difficulty is Semrush's estimate; competitor pages are not in the export. Check the top 3 results for the top picks before writing.
- Volumes are monthly estimates; relative ranking holds even if absolute numbers are off.
- Intent for "how to clean running shoes" is informational; whether an awareness post is worth the content person's time is the team's call.
- The top-3 click share (about 68.7%, from 39.8%, 18.7%, 10.2%) is a general benchmark, not measured on this site.
````

## Arm B answer (without skill)

````markdown
# SEO keyword focus for northpeak.com

Source: resources/keyword_rankings.csv, a Semrush organic positions export of 21 rows. It has no date, no traffic or click data, and no CTR, so no click estimates are made. Priority uses position, search volume and keyword difficulty (KD) only.

## Why these eight
With DA 34 and one content person, focus on pages already close to the top with low difficulty. Head terms are out of reach this quarter: "running shoes" (position 64, volume 201,000, KD 91), "trail running shoes" (position 57, volume 49,500, KD 78), "marathon training plan" (position 72, volume 40,500, KD 84). Brand terms ("northpeak running" at 1, "northpeak shoes" at 2, "northpeak trail x2 review" at 2) already rank well; keep them healthy, no focus work needed.

## The eight keywords
1. how to start trail running (position 3, volume 8,100, KD 35, informational, /blog/start-trail-running): highest volume already in the top 3. Refresh the post, add a first-week plan and FAQ, aim for position 1.
2. best trail running shoes for beginners (position 7, volume 4,400, KD 31, commercial, /blog/best-trail-shoes-beginners): push into the top 3. Update the shortlist and comparison table, link each pick to its product page.
3. trail running shoes wide toe box (position 11, volume 2,900, KD 27, commercial, /trail-running-shoes/wide): page 2, small on-page push can reach page 1. Add a plain-language toe box fit section; link from the trail shoes category page.
4. waterproof trail running shoes (positions 14 and 19, volume 3,600, KD 33, transactional): two URLs compete (/trail-running-shoes/waterproof at 14, /blog/waterproof-vs-breathable at 19). Make the category page the single target, fold or link the comparison content into it, and give the blog post a different angle.
5. how to clean running shoes (position 17, volume 6,600, KD 21, informational, /blog/clean-shoes): easy and large, on page 2. Refresh with step-by-step trail shoe cleaning and a care section.
6. trail running vest (position 9, volume 5,400, KD 29, transactional, /vests): near the top 3. Add a capacity and fit comparison; make title and H1 use the exact phrase.
7. zero drop trail shoes (position 5, volume 1,900, KD 22, commercial, /trail-running-shoes/zero-drop): top 5 with low KD. Add a what-is-zero-drop explainer and a list of qualifying models.
8. trail running shoes sale (position 6, volume 2,400, KD 24, transactional, /sale/trail): unstable target. Keep current models and dates up to date, only if the sale runs regularly.

Not in the eight: trail running gaiters (position 13, volume 1,600, KD 19) is a next-quarter candidate; trail shoe size guide (position 4, volume 1,300, KD 15) needs only light upkeep.

## Open points for the team
- The export has no date and no traffic data. Re-run it and pull clicks from Search Console before setting targets.
- "waterproof trail running shoes" is a duplicate keyword mapped to two URLs. Item 4 assumes the team agrees to consolidate.
- Volume and KD are Semrush estimates and may not match real demand for northpeak's products.
````
