<h1 align="center">Devil's Analyst</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/checks-229%20numbered-111111?style=flat-square" alt="229 numbered checks">
  <img src="https://img.shields.io/badge/benchmark-110%20cases-111111?style=flat-square" alt="110 benchmark cases">
</p>

Teams now act on numbers their agents pull through connectors: GA4, Google
Ads, Meta, Search Console, an email platform, a CRM, Shopify, a warehouse, a
Power BI model. A current model knows most of the marketing judgement
around those numbers. Ask it about attribution windows or brand search
incrementality and you get a good answer. What it does not have is that
judgement gathered in one place, across the whole chain, and applied the
same way every time:

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

I could not find this gathered anywhere. Platform docs cover one platform
each. Courses teach the theory. Checklists cover one channel. The rest lives
in senior analysts' heads. So I wrote it down, from my study of marketing:
academic sources I read on my own, and my notes from my M.S. in Marketing at
Syracuse University, which I studied as a Fulbright scholar. Because it is
written down, your team can read every check, change it, add its own, and
see which check produced a finding.

Devil's Analyst is **the devil's advocate on your marketing team**. It
argues with the data before you act on it.

<p align="center">
  <em>The model knows the questions; this makes it ask all of them, every time.</em>
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

## What it gathers in one place

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

## The benchmark

110 cases modelled on real marketing situations, all with synthetic data,
in [benchmarks/cases/](benchmarks/cases/): 62 focused traps, 36 draft
reports with the exports behind them (the September report above is one),
and 12 audits and reviews. 105 of them are generated by scripts that compute
the true answer in code; five early ones are hand-written.

In the first run, Claude Haiku 5.5 found the planted problems and made the
right call in most of the 36 report cases, with or without Devil's Analyst.
That fits the point above: the model knows most of this. What the plugin
adds is the same checks, written down, applied in the same order every
time. Results per case:
[benchmarks/results/](benchmarks/results/2026-10-17-breadth.md). How each
grader works and how to run it yourself:
[benchmarks/METHOD.md](benchmarks/METHOD.md).

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
- **One run so far.** Details in
  [benchmarks/results/](benchmarks/results/2026-10-17-breadth.md).
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
