# Contributing

Thanks for reading this far. The most useful contributions, in order:

1. **A case where Devil's Analyst is wrong.** A real problem it missed, a
   correct detail it flagged, a number it got wrong, a decision it called the
   wrong way. Open an issue with the export (remove anything private, or
   simulate a version with the same shape), what it said, and what it should
   have said. If you can, include the host and model you used.
2. **A check proposed upstream.** Something a senior analyst on your team
   knows that the shipped checks do not cover, and that would hold for most
   teams, not just yours. See below.
3. **A report from another agent.** Most adapters are untested (see
   [INSTALL.md](INSTALL.md)). If you install one, tell me whether it loaded
   and whether the analysis followed the method.
4. **A change to an existing check.** A threshold that is out of date, a
   platform setting that moved, a red flag that fires on normal data. Cite
   the source.

## Proposing a check upstream

A team's own rule belongs in its `house-rules/` folder (see
[house-rules/README.md](house-rules/README.md)). A rule that would save most
teams money belongs in the shipped checks. To propose one:

1. **Write it with the template.** Fill in
   [house-rules/TEMPLATE.md](house-rules/TEMPLATE.md): area, check, where to
   look (the exact column, setting or report), the red flag threshold, why it
   costs money, the fix, the source, and you as owner. Write the red flag so
   two analysts would agree whether it fired. Name the area's reference file
   in `skills/audit/references/` (or `skills/review/references/` for a
   report check) where it would go, and the id it would take there (review
   ids carry the RV- prefix, for example RV-C8).
2. **Give it a source.** A platform's documentation, a published study, a
   regulation, or an incident you can describe without naming a client or an
   employer. "Everyone knows" is not a source.
3. **Plant the problem in a benchmark case.** Add a script to
   `benchmarks/builder/cases/`, following the cases around it (the `bx-*`
   scripts are the best model):
   - simulate the exports with a fixed seed (`random.Random(<seed>)`), with
     fictional brands and `.example` domains;
   - plant the problem your check catches, next to at least one decoy that
     looks similar but is normal;
   - compute the true answer in code and `assert` that the naive answer
     differs from it;
   - write graders that quote the computed numbers: one that passes when the
     problem is found with evidence, one that fails if the decoy is flagged,
     and one for the decision it should change.

   Then rebuild and check that only your case changed:
   ```bash
   python3 benchmarks/builder/build_all.py
   git status --short benchmarks/cases
   ```
4. **Show it fails without the check.** Run your case in both arms (copy it
   into its own folder and point `--eval-dir` at it) and paste the summary.
   A check that the model already passes without the plugin is still useful
   documentation, but it does not need to be in the shipped checks.
5. **Open a pull request** with the check row, the case, and the run
   summary. I review the threshold, the source and the case; a reviewer who
   works in that platform is welcome to weigh in. Expect questions about the
   decoy: a check that fires on normal data costs more trust than it saves.

## Before you open a pull request

- Edit `AGENTS.md` or `adapters/windsurf/devils-analyst.md`, not the copies,
  then run `python3 scripts/sync-adapters.py` (CI-style check: `--check`).
- Edit the skills in `skills/`; the ChatGPT knowledge bundles and the release
  zips are generated from them (`scripts/sync-adapters.py`,
  `scripts/package.sh`).
- Run `claude plugin validate .`.
- If you change a count the README states, run `python3 scripts/count.py`
  and update the README from its output.
- If you change a skill, say whether you re-ran the benchmark, on which
  cases, and paste the summary from `benchmarks/report.py`.
- Never use a client's or an employer's data, names or dashboards, even
  anonymised. Simulate it.
- Plain writing: short sentences, no em-dashes, no hype words.

## Disagreeing

If you think a number in the README is wrong, say so in an issue with the
log or the case. I will try to reproduce it and update the README either way.
