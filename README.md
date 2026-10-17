<h1 align="center">Devil's Analyst</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/checks-229%20numbered-111111?style=flat-square" alt="229 numbered checks">
  <img src="https://img.shields.io/badge/benchmark-110%20cases-111111?style=flat-square" alt="110 benchmark cases">
</p>

Teams now act on numbers their agents pull through connectors: GA4, Google
Ads, Meta, Search Console, an email platform, a CRM, Shopify, a warehouse, a
Power BI model. The model already knows generic analysis. It can take an
average, draw a chart and write the SQL. What it lacks is the marketing
judgement around those steps, across the whole chain:

- **How each platform reports.** Attribution windows, which conversion
  actions sit in "Conversions", report levels that overlap, sampled
  explorations, consent gaps, a Search Console that lags two to three days.
- **How channels interact.** Brand search harvesting demand that other
  channels created, retargeting buying people who would have bought anyway,
  a promotion pulling next month's sales into this one.
- **What a number is worth to the business.** Margin, not revenue.
  Incremental sales, not platform credit. Payback, not ROAS.
- **What to do next.** One action per finding, and a way to check next month
  whether it worked.

I wrote that judgement down from my study of marketing: academic sources I
read on my own, and my notes from my M.S. in Marketing at Syracuse
University, which I studied as a Fulbright scholar. Devil's Analyst is **the
devil's advocate on your marketing team**. It argues with the data before
you act on it.

<p align="center">
  <em>The model can do the maths; this makes it ask the questions.</em>
</p>

Here is one benchmark case (synthetic data). A draft report calls September
a record month: sessions up 39% on July, GA4 revenue up 36%. The exports
behind it show users up 3.6% and store revenue up 3.9%. The session timeout
was cut from 30 to 5 minutes on 18 August, and purchase events have fired
twice since a theme release on 31 August. The draft proposes raising Q4
targets by 25%.

It is a set of 16 skills and a session hook, packaged for Claude Code and
other agents. Personal project.

---

## What it knows that a general model does not

The audit checks are tables with five columns: where to look (a column, a
setting, a report), the red flag, why it costs money, the fix, and a tier
for urgency. The other disciplines live in the skills as worked formulas
and adversary questions. Two examples from each, with the check id where
there is one:

| Discipline | Two of its checks |
|---|---|
| Paid search | PS1: the Conversions column mixes newsletter sign-ups and add-to-carts with purchases, so CPA looks tiny. PS9: average CPC above break-even CPC (margin per sale x conversion rate) on a line called "efficient". |
| Performance Max, display, video | PM2: much of PMax's credit sits on brand searches you already rank first for organically, with no brand exclusion. DV6: the cheapest cost-per-view line, with completion collapsing after 25%. |
| Meta and paid social | M1: campaigns on different attribution windows compared side by side, view-through on some only. M9: account reach equal to the sum of ad set reach. |
| SEO and Search Console | S2: demand sized from summed query-and-page rows. S14: a dip in the last two to three days read as a drop. |
| GA4 and UTMs | GA2: data-driven attribution selected while a key event has a few hundred conversions a month. U1: one campaign key in several spellings (spring_sale, Spring_Sale, spring-sale). |
| Email and lifecycle | E3: a send above 0.1% complaints, even when the monthly average is under. E7: campaigns ranked or judged on opens. |
| CRM and pipeline | C1: CLV built on revenue, with no margin, servicing cost or discount rate. C13: leads counted by today's lifecycle stage, not the date each stage was entered. |
| E-commerce revenue | R1: revenue claimed by each platform sums above the store total. R7: test orders, refunds and cancellations counted as revenue. |
| Pricing and promotions | "Is 60% a margin or a markup?", rebuilt from cost lines before any break-even. A promotion's window runs until orders recover; the promo-week lift alone is not the answer. |
| Brand and organic social | Before crediting or blaming the brand: did the category or competitors move the same way (share of search)? Engagement rate pooled across posts, because averaging per-post rates lets tiny posts win. |
| Experiments | X1: sample ratio mismatch (chi-square on assignment counts above 10.8). X4: no minimum detectable effect, stopped when it "looked significant". |
| Attribution and incrementality | A3: platform conversions summed across platforms. A9: retargeting, brand search and PMax brand share credited at full value with no test. |
| Research and product | Sample size scales with 1/E²: halving the margin of error needs four times the sample. Stated purchase intent counted as sales in a forecast. |
| Power BI models | P1: `AVERAGEX` over a rate. P4: a toggle whose default (no selection) differs from the agreed definition, such as gross instead of net revenue. |

Each area also lists what **not** to flag. A brand search CTR of 40%,
Search Console clicks above GA4 sessions, Direct at 15% of sessions: all
normal. A check that fires on a decoy costs the reader's trust.

`python3 scripts/count.py` counts the checks from the files: 185 audit
checks in 12 areas, 44 review checks for someone else's report (numbers,
definitions, comparisons, causal claims, actions, the "why" section), and
59 diagnosis playbooks.

## The whole chain

A checklist on its own catches problems after the fact. The skills carry
the same judgement through every step of an analysis:

1. **Route the question to the data you have.** `route-question` lists what
   the agent can reach (connectors, a warehouse, files, a Power BI model)
   and rewrites the question into one request: platform, account,
   conversion action, window and comparison, grain, report level,
   attribution window. Then it answers, answers in part and says what is
   missing, reframes to the nearest question the data can answer, or
   declines the method (a forecast from two months of data).
2. **Define before querying.** `metric-definitions` gives every metric a
   formula, a source and a grain first. Rates are ratios of summed parts.
   Users and reach do not add across days. Two sources meet only after each
   is aggregated.
3. **What changed, and why.** `whats-changed` splits a move into drivers
   (sessions x conversion rate x order value) and into mix versus rate, and
   screens out noise.
4. **Evidence checks.** `evidence-check` asks what would have happened
   anyway: A/B checks, controls, Simpson's paradox, holdouts, promotion
   pull-forward.
5. **Diagnosis.** `diagnose` turns the move into a likely cause, the
   evidence for and against it, an action and a way to verify it, using
   funnel and brand diagnostics and 59 playbooks. Pricing, channel
   economics, brand health, product decisions, marketing models and
   research design each have their own skill.
6. **Review and audit.** `review` checks a report, deck or dashboard
   someone else made. `audit` checks a whole account or setup, in the order
   that matters (conversions before devices).
7. **Write the answer.** The number first, then at most three findings
   ranked by money at stake, each cause labelled as a hypothesis until
   tested, each action paired with a check. Correct things are left alone.

**An adversary for every move.** Each skill ends with a table: the move,
what the adversary asks ("what else would produce this number?"), the check
that settles it, and what to do if it fails.

**When a Power BI model is connected,** `power-bi-definitions` treats it as
the team's statement of what each number means, audits the measures the
question needs, and either queries them live through a Power BI MCP
connector or translates them to SQL. A translation is not the model: it
reconciles one number against Power BI before you rely on it.

## Where the checks come from

The domain knowledge is digital marketing across disciplines, taken from my
personal study of academic marketing sources and from my notes from my M.S.
in Marketing, which I studied as a Fulbright scholar. I wrote it down as
**229 numbered checks** plus the formulas, playbooks and adversary tables in
the skills. Course material is paraphrased, not copied.
[docs/sources/](docs/sources/) maps each rule in seven of the skills to the
note it came from. The notes themselves are private, so the map shows the
trail, not the text.

I tested it on **110 scenarios modelled on real marketing situations**, all
with synthetic data. So far I have run 36 of them, with and without the
plugin. The results are below, and they are more modest than you might
expect.

## The benchmark

The 110 cases are in [benchmarks/cases/](benchmarks/cases/), in the format
`claude plugin eval` reads:

- **62 focused cases.** A clean export built around one named trap.
- **36 breadth cases.** A draft report, memo or proposal with the exports
  behind it, four to six subtle problems, usually two decoys, and a
  decision to make. The September report above is one of them.
- **12 audits and reviews.** Account and setup exports to audit and
  reports to review, with planted problems, decoys and one clean control.

105 cases are generated by scripts in [benchmarks/builder/](benchmarks/builder/)
that simulate the exports with a fixed seed, compute the true answer in
code and assert that the naive answer differs. Five early cases are
hand-written.

### The breadth run

36 breadth cases, 3 runs per case per arm, 216 runs in all, on 17 October
2026. Claude Haiku 5.5 in Claude Code was the model under test, and Claude
Haiku was the judge (three votes per grader, majority wins).

| Share of runs that pass | With Devil's Analyst | Without |
|---|--:|--:|
| Subtle problems found (3 or more, with evidence) | 100% (108/108) | 99% (107/108) |
| Right decision on the proposal | 97% (105/108) | 95% (103/108) |
| No false alarms (decoys left alone) | 80% (86/108) | 81% (88/108) |
| Every grader passed | 77% (83/108) | 78% (84/108) |
| Mean score (0 to 1) | 0.94 | 0.93 |

Mean difference per case: +0.01. A Devil's Analyst skill fired in 107 of
the 108 with-plugin runs.

**What this says.** Claude Haiku 5.5 already finds most planted problems in
clean exports, with or without the plugin. On these cases, Devil's Analyst
did not move the score much. Its value is elsewhere: the checks are written
down, applied every time in the same order, extendable by your team, and
carried into routing, definitions and decisions. A model that happens to
catch a problem today is not the same as a written check your team can
read, change and audit.

**Where it helped most:**

- `bx-commerce-tier-price-rise`, +0.42. Store units fell 28% after a price
  rise and the sales team wanted to roll it back. Adjusted for season and
  stock-outs, the rise was profitable; the leak was a lower Amazon price.
  Without the plugin, two of three runs recommended the rollback.
- `bx-social-creative-test`, +0.25. A UGC video "won" on CTR and ROAS, but
  on the fair window the two creatives were close (p = 0.47). Without the
  plugin, two of three runs declared a winner; with it, one did.
- `bx-pmax-marginal`, +0.17. Reported PMax ROAS beat target, but the last
  budget increase returned 0.75x at the margin. Both arms rejected the
  budget rise; the difference came from decoys, flagged in all three runs
  without the plugin and in one with it.

**Where it did worse:** three SEO cases. `bx-seo-cmo-update` (-0.17)
presented a decoy as a problem in all three runs with the plugin, against
one without. `bx-seo-content-roadmap` (-0.13) and `bx-seo-replatform`
(-0.13) each missed the decision in one run with the plugin. Outside SEO,
`bx-brand-social-quarterly` (-0.17) flagged a decoy in two runs with the
plugin.

Per-case table: [benchmarks/results/2026-10-17-breadth.md](benchmarks/results/2026-10-17-breadth.md).
Full log: [benchmarks/eval-breadth.log](benchmarks/eval-breadth.log). What
each grader checks: [benchmarks/METHOD.md](benchmarks/METHOD.md). The
focused cases and the audits and reviews have not been run yet. To run it
yourself:

```bash
claude plugin eval . --eval-dir benchmarks/cases --scaffold --allow-tools Write Bash --model haiku -j 6 --runs 3 --trust-plugin --no-publish | tee benchmarks/eval.log
python3 benchmarks/report.py benchmarks/eval.log
```

## House rules

The shipped checks know what goes wrong in most marketing data. They cannot
know that your revenue of record is finance net revenue, that campaigns
starting `BR_` are brand, or that your payment page lives on another
domain. Put those in a `house-rules/` folder in your project, one rule per
file, using [house-rules/TEMPLATE.md](house-rules/TEMPLATE.md).
`route-question` and `metric-definitions` read them before anything else.

Precedence, highest first: what you say in the conversation, your house
rules, your governed definitions (a Power BI model, a metric dictionary),
the shipped defaults. A house rule can replace a definition, a threshold or
a default. It cannot make an averaged rate correct: the agent shows both
numbers and says why they differ. Findings cite the rule id that changed
them. Two fictional examples are in [house-rules/](house-rules/).

## Growing it

- **Your team's rules.** Write one after every incident, with the incident
  as its source. After a review correction, ask whether it was a one-off or
  a rule. Re-read old rules each quarter; a renamed column makes a rule
  wrong without anyone noticing.
- **Community rules.** A rule that would hold for most teams belongs
  upstream. [CONTRIBUTING.md](CONTRIBUTING.md) says how to propose it, with
  a source and a benchmark case that plants the problem.
- **A local loop (planned, not built).** A loop that proposes house-rule
  changes from your own past analyses, one change at a time, kept only if
  it scores better on your own held-out cases and only with your approval.
  The design is in [docs/self-improving.md](docs/self-improving.md).

## Install

**Claude Code**, as two separate prompts:

```
/plugin marketplace add C-Kapsalis/devils-analyst
```
```
/plugin install devils-analyst@devils-analyst
```

Then connect your data and ask the way you normally would: "How did paid
search do last month, and what should we change?" A session hook loads the
routing table and seven core rules into every session. The Code tab of the
Claude Desktop app works the same way.

**Claude (web and Desktop chat):** add the marketplace
`C-Kapsalis/devils-analyst` under Customize > Plugins, upload
`devils-analyst-plugin.zip` there, or upload single skills from
`devils-analyst-skills.zip` under Customize > Skills. Code execution must
be on. There is no session hook in chat, so name the job ("audit our GA4
setup", "is this report right?"). House rules go in the project's knowledge
or in the message.

**ChatGPT:** upload the skill zips, or use the custom GPT or Project
instructions and the ten knowledge files in
[adapters/chatgpt/](adapters/chatgpt/). Untested.

**Codex, Copilot, Gemini CLI, OpenCode, Cursor, Windsurf, Cline, Kiro,
OpenClaw** and anything that reads `AGENTS.md`: step by step in
**[INSTALL.md](INSTALL.md)**, with what I have and have not tested. The
release zips are built by `sh scripts/package.sh`.

## Limits

- **Synthetic data.** Every export was simulated with problems planted on
  purpose. Real exports are messier, and the hardest questions (is this the
  right goal? the right margin?) cannot be planted.
- **One group run so far.** The numbers above cover the 36 breadth cases.
  The 62 focused cases and the 12 audits and reviews have not been run.
- **No measurable lift on these cases.** A mean difference of +0.01 is
  within noise. I do not claim the plugin makes Haiku score higher.
- **Decoys are not solved.** Both arms left the decoys alone in about 80%
  of runs. In `bx-seo-cmo-update` one decoy is Search Console clicks above
  GA4 sessions, which the plugin's own Search Console checks list as
  normal, and the with-plugin arm still flagged a decoy in all three runs.
- **Small n.** Three runs per case per arm. One run moves a case's score by
  a third.
- **An LLM judge.** The graders carry the computed answer, but a judge can
  still pass a vague report or fail a correct one. I have not measured
  agreement with a human grader.
- **It checks what it can see.** It can tell you a session timeout changed
  in the settings export; it cannot tell you about a change nobody
  exported. A check without the data it needs is reported as "not
  checked", not as fine.
- **One model, one host.** The benchmark runs on Haiku in Claude Code. The
  other adapters load the same method but are not benchmarked.
- **Same author.** I wrote the cases and the skills. Cases from other
  people would make the numbers more trustworthy.

If you have an export where Devil's Analyst got it wrong, a problem it
should have caught, or a decoy it should have left alone, please
[open an issue](https://github.com/C-Kapsalis/devils-analyst/issues). A
counterexample is worth more to me than a star. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

- The domain knowledge comes from my own study of academic marketing
  sources and my M.S. in Marketing notes, paraphrased. The playbooks, the
  funnel and brand diagnostics and most metric definitions are also
  published on [Cohortica](https://www.cohortica.studio), my own free
  marketing interview-prep site. Standard definitions added where my notes
  are silent are marked `[std]` in the references.
- Frameworks and studies the skills cite by name: Keller's customer-based
  brand equity (CBBE) pyramid in the brand diagnostic; Binet and Field on
  share of voice against share of market; the eBay brand-search experiment
  ([Blake, Nosko and Tadelis](https://www.nber.org/papers/w20171)) and
  Google's Search Ads Pause studies on brand incrementality; WordStream
  benchmarks for CTR and paid search, quoted as heuristics.
- The repository layout and the multi-agent adapters follow
  [Ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert.
- The planned self-improving loop takes its shape from WikiSkill
  (arXiv:2608.27454).
- `power-bi-definitions` documents four of my open-source tools for PBIP
  and TMDL models:
  [tmdl-preflight](https://github.com/C-Kapsalis/tmdl-preflight),
  [pbip-model-forge](https://github.com/C-Kapsalis/pbip-model-forge),
  [tmdl-drift-doctor](https://github.com/C-Kapsalis/tmdl-drift-doctor) and
  [pbi-plot-styler](https://github.com/C-Kapsalis/pbi-plot-styler).

Personal project. It is not affiliated with, or endorsed by, any employer.

## License

[MIT](LICENSE).
