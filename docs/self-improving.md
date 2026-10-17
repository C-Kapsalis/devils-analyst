# A local loop that improves the house rules

**Status: planned; shares an engine with SecondReadOS.** Nothing on this page
is built. It is a design note, so the house-rules layer is shaped for it from
the start. If you have run something like this on a real team, I would like
to hear what broke.

## The problem

House rules grow when someone remembers to write one. Most lessons are never
written: a reviewer corrects an analysis in a comment, the analyst fixes the
number, and six months later a new colleague makes the same mistake. The
records that would teach the rule already exist. Nobody has time to turn them
into rules, and nobody wants an agent rewriting its own instructions
unsupervised.

## The idea

A loop in the style of WikiSkill (arXiv:2608.27454): keep raw records, distil
them into a wiki of patterns, and let a proposer change a skill one small step
at a time, keeping a change only when it scores better on held-out cases. I
take the shape of that loop, not its numbers; read the paper for its own
claims. The differences here are deliberate limits: the loop runs locally, it
edits only the team's house rules, and a person approves every change.

## Parts

1. **Raw records.** Append-only, local, one file per analysis: the question,
   the data sources and scope line, the answer, the decision taken, the
   outcome when it is known, and every reviewer correction with its reason.
   Nothing leaves the machine.
2. **Maintainer.** Reads new records and writes patterns to a local wiki:
   "three times this quarter, a reviewer replaced Shopify gross revenue with
   finance net revenue". A pattern cites the records it came from. The wiki
   is notes, not rules; the agent does not read it during an analysis.
3. **Proposer.** Turns one pattern into one change to `house-rules/`: a new
   rule from the template, a changed threshold, a retired rule. One change at
   a time, so a result can be traced to it. It may edit only files in the
   team's `house-rules/` folder. It never edits the shipped skills, their
   checks, the hooks or the benchmark.
4. **Held-out set.** The team's own past cases with known right answers: an
   analysis, its data, and what the reviewer said the answer should have
   been. Kept apart from the records the maintainer reads, so a change is not
   graded on the cases that suggested it.
5. **Keep or roll back.** Run the held-out set with and without the change.
   Keep it only if it scores better and breaks no case that passed before;
   otherwise roll it back and log why.
6. **Weekly diff.** Kept changes collect into one diff a person reads once a
   week, with the pattern, its records and the held-out result next to each
   change. Nothing reaches `house-rules/` without that approval. A rejected
   change is logged so it is not proposed again.

## What it will not do

- Edit the shipped core. Upstream changes go through
  [CONTRIBUTING.md](../CONTRIBUTING.md), with a planted-problem case and a
  review, like any other contribution.
- Learn from a single record. A pattern needs several records, or one
  incident a person marks as a rule.
- Grade itself on its own training data. The held-out set is separate, and
  small held-out sets are noisy: a change that wins one case out of twenty is
  not evidence, and the diff should say so.
- Send records anywhere. The loop is local by design; the records contain
  the team's numbers and decisions.

## Open questions

- How many held-out cases a team needs before keep-or-rollback means
  anything. My guess is dozens, which many teams will not have at first.
- How to record an outcome that arrives months after the decision.
- Whether the maintainer should run on a small local model, so the records
  never reach a hosted one.
