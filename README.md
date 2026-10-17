<h1 align="center">Devil's Analyst</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/checks-229%20numbered-111111?style=flat-square" alt="229 numbered checks">
  <img src="https://img.shields.io/badge/benchmark-110%20cases-111111?style=flat-square" alt="110 benchmark cases">
</p>

Tech teams and marketers now act on numbers their agents pull through
connectors: GA4, Google Ads, Meta, Search Console, an email platform, a CRM,
Shopify, a warehouse, a Power BI model. The model can do the arithmetic. The
expensive mistakes are the questions nobody asked. Was the session timeout changed in August? Is "conversions" a
sale or a newsletter sign-up? Did the email revenue disappear, or did the
email platform rename its `utm_medium` so the revenue now sits in
Unassigned?

Here is one of the benchmark cases (synthetic data). A draft report calls
September a record month: sessions up 39% on July, GA4 revenue up 36%. The
exports behind it show users up 3.6% and store revenue up 3.9%. The session
timeout was cut from 30 to 5 minutes on 18 August, and purchase events have
fired twice since a theme release on 31 August. The draft proposes raising Q4
targets by 25%.

Devil's Analyst is **the devil's advocate on your marketing team**. It argues
with the data before you act on it. It writes down what senior analysts carry
in their heads and easily overlook at a cost to their company: 229 numbered
checks, an adversary for every move, and routing that reshapes the question
to the data you actually have.

<p align="center">
  <em>The model can do the maths; this makes it ask the questions.</em>
</p>

It is a set of skills and a session hook, packaged for Claude Code and other
agents. Personal project.

---

## What it checks

The checks are tables with the same five columns: where to look (a column, a
setting, a report), the red flag, why it costs money, the fix, and a tier
that says how urgent it is. `python3 scripts/count.py` counts them from the
files.

| Area | Numbered checks | Examples |
|---|--:|---|
| Paid search (Google Ads, Microsoft Ads) | 20 | a Conversions column that mixes sign-ups with sales; generic campaigns serving brand queries; a campaign beating target but capped by budget |
| GA4 and UTMs | 20 | data retention left at 2 months; data-driven attribution silently on last click at low volume; one campaign key in several spellings |
| Email | 18 | delivered under 95% of sent; campaigns judged on opens; dormant contacts in main sends |
| Search Console and SEO | 18 | demand sized from summed query-and-page rows; CTR as a mean of row CTRs; a dip in the last 2-3 days read as a drop |
| CRM and lifecycle | 17 | CLV built on revenue with no margin; leads counted by today's stage, not the date they entered it |
| Experiments | 16 | sample ratio mismatch; no minimum detectable effect, stopped when it looked significant |
| Performance Max, Demand Gen, display, video | 14 | PMax credit sitting on brand searches; placements with huge impressions and zero sessions |
| Dashboards | 14 | averages of row ratios; users summed across days; spend joined to orders row by row |
| Power BI models | 14 | `AVERAGEX` of a rate; a toggle whose default differs from the agreed definition |
| Attribution | 13 | platform conversions summed across platforms; last-click ROAS used to cut display or video |
| Meta and paid social | 11 | campaigns on different attribution windows compared side by side; reach summed across ad sets |
| E-commerce revenue | 10 | platform claims summing above the store total; test orders and refunds counted as revenue |
| Reviewing someone else's report | 44 | numbers, definitions, comparisons, charts, causal claims, recommendations |

That is 185 audit checks in 12 areas plus 44 review checks. Around them sit
the skills that do the analysis: `metric-definitions` (a catalog of formulas,
the grain each is valid at, and the per-platform export traps),
`whats-changed` (drivers, mix versus rate, noise), `evidence-check` (A/B
checks, controls, Simpson's paradox, holdouts, promotion pull-forward),
`diagnose` (funnel and brand diagnostics and 59 playbooks), and skills for
pricing and promotions, channel economics, brand health, product decisions,
marketing models and research design. 16 skills in all.

**Decoys stay alone.** A brand search CTR of 40%, Search Console clicks above
GA4 sessions, Direct at 15% of sessions, `(not set)` under 1%: all normal.
A check that fires on a decoy costs the reader's trust, so each area lists
what not to flag.

## How it argues

1. **Route first.** `route-question` lists what the agent can actually reach
   (connectors, a warehouse, files, a Power BI model) and rewrites the
   question into one request: platform, account, conversion action, window
   and comparison, grain, report level, attribution window. Then it decides:
   answer, answer partly and say what is missing, reframe to the nearest
   question the data can answer, or decline the method (a forecast from two
   months, causality from a correlation).
2. **Define before computing.** Every metric gets a formula, a source and a
   grain before the first query. Rates are ratios of summed parts. Users and
   reach do not add across days. Two sources meet only after each is
   aggregated.
3. **An adversary for every move.** Each skill ends with a table: the move,
   what the adversary asks ("what else would produce this number?"), the
   check that settles it, and what to do if it fails.
4. **Lead with the answer.** The number first, then at most three findings,
   each with a likely cause labelled as a hypothesis, an action, and how to
   verify it next month. Correct things are left alone.

### When a Power BI model is connected

A semantic model is the team's statement of what each number means, so it
takes precedence over raw sources. It is not trusted blindly: models carry
the same traps, better hidden. `power-bi-definitions` reads the measures,
relationships and toggles, audits each measure the question needs (an
averaged rate, a summed snapshot, a toggle whose default differs from its
description), and then either queries the correct measures live through a
Power BI MCP connector or translates them to SQL for the warehouse behind the
model. A translation is a translation, not the model: it reconciles one
number against Power BI before you rely on it. The same skill will also ship
in swift-pbi, my Power BI tooling.

## House rules

The shipped checks know what goes wrong in most marketing data. They cannot
know that your revenue of record is finance net revenue, that campaigns
starting `BR_` are brand, or that your payment page lives on another domain.
Put those in a `house-rules/` folder in your project, one rule per file,
using [house-rules/TEMPLATE.md](house-rules/TEMPLATE.md): id, area, check,
where to look, red flag threshold, why it costs money, fix, source, owner,
date. `route-question` and `metric-definitions` read them before anything
else.

Precedence, highest first: what you say in the conversation, your house
rules, your governed definitions (a Power BI model, a metric dictionary), the
shipped defaults. A house rule can replace a definition, a threshold or a
default. It cannot make an averaged rate correct: the agent shows both
numbers and says why they differ. Findings cite the rule id that changed
them.

To grow them: write one after every incident, with the incident as its
source; ask after every review correction whether it was a one-off or a
rule; re-read old rules each quarter, because a renamed column makes a rule
wrong without anyone noticing. Two fictional examples and the full
explanation are in [house-rules/](house-rules/). A rule that would hold for
most teams belongs upstream; [CONTRIBUTING.md](CONTRIBUTING.md) says how to
propose it with a benchmark case that plants the problem.

A local loop that proposes house-rule changes from your own past analyses,
one change at a time, kept only if it scores better on your own held-out
cases and only with your approval, is designed in
[docs/self-improving.md](docs/self-improving.md). It is planned, not built.

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
`C-Kapsalis/devils-analyst` under Customize > Plugins, or upload
`devils-analyst-plugin.zip` there, or upload single skills from
`devils-analyst-skills.zip` under Customize > Skills. Code execution must be
on. There is no session hook in chat, so name the job ("audit our GA4
setup", "is this report right?"). House rules go in the project's knowledge
or in the message.

**ChatGPT:** upload the skill zips (Plugins > Skills), or use the custom GPT
or Project instructions and the ten knowledge files in
[adapters/chatgpt/](adapters/chatgpt/). Untested.

**Codex, Copilot, Gemini CLI, OpenCode, Cursor, Windsurf, Cline, Kiro,
OpenClaw** and anything that reads `AGENTS.md`: step by step in
**[INSTALL.md](INSTALL.md)**, with what I have and have not tested. The
release zips are built by `sh scripts/package.sh`.

## The benchmark

110 cases in [benchmarks/cases/](benchmarks/cases/), in the format
`claude plugin eval` reads, each run with and without the plugin:

- **62 focused cases.** A clean export built around one named trap: daily
  users summed into monthly users, average position left unweighted, a
  sample ratio mismatch, platform revenue stacked, a promotion's pull-forward.
- **36 breadth cases.** A draft report, memo or proposal with the exports
  behind it, four to six subtle problems, usually two decoys, and a decision
  to make. The September report above is one of them.
- **12 audits and reviews.** Account and setup exports to audit and reports
  to review, with planted problems, decoys and one clean control.

105 cases are generated by scripts in
[benchmarks/builder/](benchmarks/builder/) that simulate the exports with a
fixed seed, compute the true answer in code and assert the naive answer
differs; `python3 benchmarks/builder/build_all.py` rebuilds them byte for
byte. Five early cases are hand-written.

**The early finding.** The first thing I learned surprised me. On the
focused cases, Claude Haiku 5.5 without the plugin already avoided most
single-number traps: in a clean export with the question pointing at the
trap, it summed what should be summed and weighted what should be weighted.
That is why the breadth cases exist. Real data does not arrive as one trap
in a clean file; it arrives as a confident draft with five problems and two
decoys in it.

The numbers below are filled by `benchmarks/report.py` from the first full
run; until then they are placeholders.

| Share of runs that pass | With Devil's Analyst | Without |
|---|--:|--:|
| Focused cases: every grader passed | {{DA_FOCUSED_ALLPASS_WITH}} | {{DA_FOCUSED_ALLPASS_WITHOUT}} |
| Breadth: planted problems found (3 or more, with evidence) | {{DA_BREADTH_RECALL_WITH}} | {{DA_BREADTH_RECALL_WITHOUT}} |
| Breadth: right decision on the proposal | {{DA_BREADTH_DECISION_WITH}} | {{DA_BREADTH_DECISION_WITHOUT}} |
| Breadth: decoys left alone | {{DA_BREADTH_NOFALSE_WITH}} | {{DA_BREADTH_NOFALSE_WITHOUT}} |
| Audits and reviews: planted problems found | {{DA_AUDIT_RECALL_WITH}} | {{DA_AUDIT_RECALL_WITHOUT}} |
| Audits and reviews: must-fix problems ranked first | {{DA_AUDIT_FIRST_WITH}} | {{DA_AUDIT_FIRST_WITHOUT}} |
| Audits and reviews: decoys left alone | {{DA_AUDIT_NOFALSE_WITH}} | {{DA_AUDIT_NOFALSE_WITHOUT}} |
| Mean score, all cases (0 to 1) | {{DA_SCORE_WITH}} | {{DA_SCORE_WITHOUT}} |

{{DA_MODEL}} in Claude Code, {{DA_CASE_COUNT}} cases, {{DA_RUNS}} runs per
case per arm, {{DA_RUN_TOTAL}} runs in all, measured on
{{DA_RESULTS_DATE}}. A Devil's Analyst skill fired in {{DA_SKILL_FIRED}} of
the with-plugin runs. Per-group tables and per-case scores:
[benchmarks/results/](benchmarks/results/). What each grader checks:
[benchmarks/METHOD.md](benchmarks/METHOD.md). To run it yourself:

```bash
claude plugin eval . --eval-dir benchmarks/cases --scaffold --allow-tools Write Bash --model haiku -j 6 --runs 3 --trust-plugin --no-publish | tee benchmarks/eval.log
python3 benchmarks/report.py benchmarks/eval.log
```

## Limits

- **Synthetic data.** Every export was simulated with problems planted on
  purpose. Real exports are messier, and the hardest questions (is this the
  right goal? the right margin?) cannot be planted.
- **No published numbers yet.** The table above is empty until the first
  full run. Until then, the only claim I make is the qualitative one: on
  clean single-trap exports, the model without the plugin already does well.
- **Small n.** Three runs per case per arm. One run moves a case's pass rate
  by a third.
- **An LLM judge.** The graders carry the computed answer, but a judge can
  still pass a vague report or fail a correct one. I have not measured
  agreement with a human grader.
- **It checks what it can see.** It can tell you a session timeout changed
  in the settings export; it cannot tell you about a change nobody exported.
  A check without the data it needs is reported as "not checked", not as
  fine.
- **One model, one host.** The benchmark runs on Haiku in Claude Code. The
  other adapters load the same method but are not benchmarked.
- **Same author.** I wrote the cases and the skills. Cases from other people
  would make the numbers more trustworthy.

If you have an export where Devil's Analyst got it wrong, a problem it
should have caught, or a decoy it should have left alone, please
[open an issue](https://github.com/C-Kapsalis/devils-analyst/issues). A
counterexample is worth more to me than a star. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

- The playbooks, the funnel and brand diagnostics and most metric
  definitions come from [Cohortica](https://www.cohortica.studio), my free
  marketing interview-prep site, and from my own notes. Standard definitions
  added where the playbooks are silent are marked `[std]` in the references.
- The repository layout and the multi-agent adapters follow
  [Ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert.
- The planned self-improving loop takes its shape from WikiSkill
  (arXiv:2608.27454).
- `power-bi-definitions` documents four of my open-source tools for PBIP and
  TMDL models:
  [tmdl-preflight](https://github.com/C-Kapsalis/tmdl-preflight),
  [pbip-model-forge](https://github.com/C-Kapsalis/pbip-model-forge),
  [tmdl-drift-doctor](https://github.com/C-Kapsalis/tmdl-drift-doctor) and
  [pbi-plot-styler](https://github.com/C-Kapsalis/pbi-plot-styler).

Personal project. It is not affiliated with, or endorsed by, any employer.

## License

[MIT](LICENSE).
