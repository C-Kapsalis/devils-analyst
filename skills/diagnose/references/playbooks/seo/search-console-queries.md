---
title: Search Console: build a query worklist
question: How do you turn Search Console query data into this month's SEO worklist
order: 8
---

Use this when the question is "where do I point this month's SEO effort?" The goal is to leave with a query worklist in three buckets: snippet rewrites, rank pushes, and leave-alone, decided from one report in under fifteen minutes.

## The framework

1. Open Search Console's **Performance report** and switch to the **Queries** tab, with impressions, clicks, CTR, and average position all enabled. Read the columns in diagnostic order: impressions, position, CTR, clicks.
2. **Sort by impressions descending.** Demand leads. Ignore anything with a handful of impressions: that is sampling dust.
3. **Bucket each high-demand query** by comparing position against CTR:
   - Strong position (1-3), weak CTR → **snippet rewrite**. You rank; people scroll past.
   - Position 4-20 → **rank push** (content depth plus internal links). The leverage zone.
   - Position 1-3 with healthy CTR → **leave alone**. Defend, do not invest.
   - Position 50+ → **leave alone**. Too far to move without a rebuild.
4. **Drill any commercial query before committing effort:** filter to the query and its close variants (spellings, plurals) to confirm the pattern holds across the whole intent, not just the one string you sorted on.

## Metrics that matter, and their traps

- **Impressions**: the demand ranking that orders your worklist. Trap: tiny-impression rows are noise; bucketing them wastes the fifteen minutes.
- **CTR against position**: the bucketing signal. Top-three positions should pull roughly a 10-40% CTR band; a top-three query far below it is a snippet failure, the cheapest win on the board because the ranking is already won.
- **Average position**: an impression-weighted average, not a fixed slot. A query at 6.4 with heavy impressions and ~1% CTR is a textbook rank push; a brand term at 1.0 and 34% CTR is a leave-alone.
- **Clicks**: the outcome column, read last. Trap: sorting by clicks first optimizes pages that were already fine and buries the high-impression, low-click rows where the work is.

## Interview prep

**"You have fifteen minutes in Search Console. What do you produce?"**
A bucketed worklist, not observations: sort queries by impressions, split snippet rewrites (rank 1-3, weak CTR) from rank pushes (4-20) from leave-alones. A strong candidate names the action per bucket (title/meta rewrite versus content-and-links) and what they deliberately ignore.

**"A query ranks third with a 0.9% CTR. Cheap win or hard problem?"**
The cheapest win available: the ranking is won and the snippet is losing the click, so rewrite title and meta to the query's intent. The trap is prescribing links or content for what is a results-page relevance problem.

**"Why not work the whole query list evenly?"**
Because effort past position fifty rarely pays without a rebuild, and top-three healthy queries need defending, not investment. Concentrating on positions 4-20 is where a modest gain crosses into clickable territory.
