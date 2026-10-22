# Power BI developer tools (Claude Code only)

Four open-source command-line tools for models kept as PBIP/TMDL in git. They
run through one wrapper that fetches each tool's tagged GitHub release into a
throwaway environment (needs [uv](https://docs.astral.sh/uv/); nothing is
installed globally):

```
T="${CLAUDE_SKILL_DIR}/scripts/devils-analyst-tool"
$T tmdl-preflight --version        # prints "tmdl-preflight 1.2.1" when ready; exit 127 = install uv first
```

The wrapper pins tag `v1.2.1`. To pin another tag, set
`DEVILS_ANALYST_TOOLS_VERSION` (for example `DEVILS_ANALYST_TOOLS_VERSION=v1.1.0 $T ...`);
`DEVILS_ANALYST_USE_LOCAL=1` prefers tools already on PATH.

The wrapper is a bash script. On Windows without Git Bash or WSL, run a tool
through `uvx` directly in PowerShell, with the same arguments:

```powershell
uvx --from git+https://github.com/C-Kapsalis/tmdl-preflight@v1.2.1 tmdl-preflight --version
uvx --from git+https://github.com/C-Kapsalis/pbip-model-forge@v1.2.1 pbip-forge --version
uvx --from git+https://github.com/C-Kapsalis/tmdl-drift-doctor@v1.2.1 drift-doctor --version
uvx --from git+https://github.com/C-Kapsalis/pbi-plot-styler@v1.2.1 pbi-plot-styler --version
```

At `v1.2.1`, each tool's own listing gives (the same as at `v1.2.0`): `tmdl-preflight rules --json`
119 rules, 25 of them auto-fixable; `pbip-forge --help` 8 commands and
`pbip-forge rules` 22 spec rules; `drift-doctor --help` 20 commands;
`pbi-plot-styler --help` 6 commands. Quote the counts the build you run
prints, not these.

Rules for all four: never hand-write TMDL a tool can generate or fix; never
claim a model opens in Power BI Desktop beyond what `tmdl-preflight check`
proves (opening it is the user's step); show the tool's counts and exit codes
instead of describing them.

## tmdl-preflight: will it open, and is it sound?

```
$T tmdl-preflight check <path> --format json   # 0 clean, 1 violations, 2 usage error
$T tmdl-preflight fix <path>                   # auto-fixes, then re-checks from disk
$T tmdl-preflight rules --json                 # the catalog: id, severity, fixable, options (119 rules at v1.2.1)
```

`fix` edits files: if the folder is not under git, ask first or copy it. CI:
`baseline <path>` then `check --baseline <path>/.tmdl-preflight-baseline.json`;
`--format github` or `--format sarif`; pre-commit hook id `tmdl-preflight` from
`https://github.com/c-kapsalis/tmdl-preflight`, rev `v1.2.1`.

## pbip-model-forge: a model from a spec

Turns a spec (a Python file with a module-level `SPEC` dict: tables, rows,
calendar, measures, relationships) into an openable PBIP with sample data and a
`handoff/SPEC.md` (data dictionary and Mermaid diagram) for data engineers.
[../assets/email_campaigns_forge_spec.py](../assets/email_campaigns_forge_spec.py)
is a complete, passing example for email campaigns; copy it into the user's
project before editing.

```
$T pbip-forge check spec.py --profile handoff          # need 0 P0, 0 P1 (22 rules; `rules` lists fixes)
$T pbip-forge build spec.py out/Model --check --profile handoff
$T tmdl-preflight check out/Model                      # need 0 errors
```

Spec rules: one hidden fact with its grain as the description; 2-4 dimensions
with one `int64` key each; foreign keys named like the key they reference; an
"Unknown" member (key -1) instead of null keys; a description on everything; a
measures table never named `Measures`; ratios as `DIVIDE` of base measures;
entity counts from the fact's foreign key. To change the model, edit the spec
and rebuild; never edit the generated TMDL.

## tmdl-drift-doctor: one template, many client models

```
$T drift-doctor capture                 # snapshot the template (after every template change)
$T drift-doctor detect --json           # 0 clean, 1 actionable drift, 3 parse error
$T drift-doctor remediate --dry-run     # unified diffs; then without --dry-run to apply
$T drift-doctor remediate --sync        # also deletions (retire.*): ask first
$T drift-doctor review --out REVIEW.md  # what needs a human
$T drift-doctor ratchet tighten|check   # CI: fail when drift rises
```

Configured by `fleet.yml`: `template`, `models` (short or long form with
`gating: advisory` and declared `overrides`), `state_dir`, and
`allowlist: {kinds: [...], expressions: [...]}`. Start the allowlist with
non-destructive kinds (`measure.missing`, `measure.expression_drift`,
`measure.property_drift`, `column.missing`, `relationship.missing`). Show
dry-run diffs and get a yes before applying.

## pbi-plot-styler: one style for every chart

For PBIR reports using the one-canvas pattern (field-parameter tables
`x-Plot Specific 1`, `x-Plot Specific 2`, `y-Plot Specific`; others via
`--table`):

```
$T pbi-plot-styler style X.Report --dry-run              # exit 1 = would change a visual
$T pbi-plot-styler style X.Report --palette "#1F6F4A" --palette "#2B6CB0"
$T pbi-plot-styler style X.Report --color "Email Measures.CTR %=#2B6CB0"
$T pbi-plot-styler check X.Report --json                 # bindings and bookmarks; --fix repairs BMK001/002
```

Ask for the brand's hex codes; never guess them. A renamed or removed measure
silently breaks the visuals and bookmarks bound to it: run `check` after model
changes.
