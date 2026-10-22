# Install

Pick your agent below. Not listed? Most agents read [`AGENTS.md`](AGENTS.md):
copy it into your project, or ask your agent to install the folders in
[`skills/`](skills/) as skills, starting with
[`skills/route-question/`](skills/route-question/) and
[`skills/metric-definitions/`](skills/metric-definitions/).

Devil's Analyst argues with data, so it needs data: connectors or MCP servers
for your platforms, a warehouse connection, or exported files. Wherever you
install it, put your team's house rules in a `house-rules/` folder at the
root of the project (see [house-rules/README.md](house-rules/README.md)).

Every adapter loads the same prompt. `AGENTS.md` is the source for the
rules-file copies; `python3 scripts/sync-adapters.py` regenerates them.

## What I have tested

I have run early benchmark cases only in Claude Code. Everywhere else, the file
formats copy those of a working multi-agent plugin
([Ponytail](https://github.com/DietrichGebert/ponytail)), but I have not
installed Devil's Analyst there myself. If you try one, please open an issue
with what happened, working or not.

| Agent | Adapter | Status |
|---|---|---|
| Claude Code (CLI, Desktop Code tab) | `.claude-plugin/`, `skills/`, `hooks/` | Tested: `claude plugin validate`; first benchmark run: benchmarks/results/2026-10-17-breadth.md |
| Claude (web and Desktop chat) | `dist/devils-analyst-plugin.zip`, skill zips | Zip structure checked locally; upload untested |
| ChatGPT | `adapters/chatgpt/` | Untested |
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | Untested |
| GitHub Copilot CLI | `.github/plugin/`, `hooks/copilot-hooks.json` | Untested |
| GitHub Copilot Chat (editor) | `.github/copilot-instructions.md` | Untested |
| Gemini CLI | `gemini-extension.json`, `commands/*.toml` | Untested |
| OpenCode | `AGENTS.md`, `.opencode/command/` | Untested |
| Cursor | `.cursor/rules/devils-analyst.mdc` | Untested |
| Windsurf | `.windsurf/rules/devils-analyst.md` | Untested |
| Cline | `.clinerules/devils-analyst.md` | Untested |
| Kiro | `.kiro/steering/devils-analyst.md` | Untested |
| OpenClaw | `.openclaw/skills/devils-analyst/` | Untested |

Menu labels in the Claude and ChatGPT apps change between versions. If a
label below does not match what you see, look for the nearest equivalent.

## Claude Code

As two separate prompts:

```
/plugin marketplace add C-Kapsalis/devils-analyst
```
```
/plugin install devils-analyst@devils-analyst
```

The same two commands work in the Code tab of the Claude Desktop app, which
behaves like Claude Code. A session hook loads the routing table and seven
core rules at the start of every session, and the skills load by the job:
`route-question` first, then the one that fits.

## Claude (web and Desktop chat)

Code execution and file creation must be on (in Settings; Capabilities in
the versions I have seen), or skills will not run. Then pick one of three routes.

**a. Add the marketplace.** In Customize > Plugins, choose Add marketplace,
enter `C-Kapsalis/devils-analyst`, then install `devils-analyst`.

**b. Upload the plugin.** Download `devils-analyst-plugin.zip` from the
[latest release](https://github.com/C-Kapsalis/devils-analyst/releases/latest) and upload it in Customize > Plugins. The release
zips are built by [.github/workflows/release.yml](.github/workflows/release.yml)
from `scripts/package.sh` each time a `v*` tag is pushed. Until a release
exists, or to build from your own copy, run the script yourself; it writes
`dist/` and needs `sh` and `zip`:

```bash
sh scripts/package.sh
```
```powershell
# Windows: run it under WSL, from the repository folder
wsl sh scripts/package.sh
```

**c. Upload single skills.** `devils-analyst-skills.zip` holds one zip per
skill (`devils-analyst-route-question.zip`, `devils-analyst-audit.zip` and so
on). Upload the ones you need in Customize > Skills; start with
`route-question` and `metric-definitions`. Each zip holds one folder with its
`SKILL.md` and `references/`.

Skills hand over to each other by name, and one reads another's files, so
upload these together:

| If you upload | Also upload | Why |
|---|---|---|
| any skill | `route-question`, `metric-definitions` | every analysis starts with routing and definitions |
| `audit` | `review` | audit's dashboard checks use review's `references/chart-checks.md` |
| `power-bi-definitions` | `marketing-dashboard` | it hands the translated metrics to marketing-dashboard to build |

Each single-skill zip is renamed `devils-analyst-<skill>`, so the relative
links between skills that work in the plugin do not resolve there; the skill
names do. If you want every cross-reference to work, use route a or b.

The session hook does not run in chat. A skill loads when your message
matches its description, so name the job: "Audit our Google Ads export",
"Is this September report right?". Anthropic's help article on custom skills
gives a 200-character limit for a skill description, while the Agent Skills
format allows 1,024. The single-skill zips therefore carry a short
description (under 200 characters); the plugin keeps the longer one. If an
upload is still rejected, please open an issue.

House rules in chat: there is no project folder to read, so add your rule
files to the project's knowledge or paste them into the message.

## ChatGPT

OpenAI is moving ChatGPT from custom GPTs to plugins, and ChatGPT plugins can
carry Agent Skills (the same `SKILL.md` folders). That makes the plugin the
main route; the custom GPT and Project setups below are fallbacks. I have not
tested any of them.

**Plugin or skills (main route).**

1. Download the assets from the [latest release](https://github.com/C-Kapsalis/devils-analyst/releases/latest), or build them
   with `sh scripts/package.sh` (PowerShell: `wsl sh scripts/package.sh`).
2. To add Devil's Analyst as skills: in ChatGPT, open Plugins in the
   sidebar, then the Skills tab (earlier versions: Skills > Create), and
   upload the single-skill zips from `devils-analyst-skills.zip`, starting
   with `route-question` and `metric-definitions`. ChatGPT scans an uploaded
   skill first and may mark it "Needs Review". On Enterprise and Edu, an
   admin has to allow skill uploads.
3. `devils-analyst-chatgpt.zip` is the package for the ChatGPT Plugin Directory
   (a `plugin.json` plus `skills/`, no hooks). Listing it is a separate step;
   see [PUBLISHING.md](PUBLISHING.md).

**Custom GPT (fallback).** OpenAI's help center says personal plans (Free,
Go, Plus, Pro) can no longer create new GPTs and that GPTs are being retired
in favor of plugins, so this only fits a workspace that still allows them.

1. Explore GPTs > Create > Configure.
2. Name: Devil's Analyst. Description: "The devil's advocate on your
   marketing team."
3. Instructions: paste
   [`adapters/chatgpt/custom-gpt-instructions.md`](adapters/chatgpt/custom-gpt-instructions.md)
   (about 4,300 characters; the commonly cited 8,000-character limit comes
   from community posts, not from OpenAI's docs).
4. Knowledge: upload the ten files in
   [`adapters/chatgpt/knowledge/`](adapters/chatgpt/knowledge/). Each bundles
   one or more skills with their references. OpenAI's pages give both 10 and
   20 as the file limit; ten fits both.
5. Conversation starters: "Audit this Google Ads export", "Is this report
   right?", "Did version B win?".
6. Visibility: keep it to Only me or Anyone with the link. A public listing
   in the GPT Store is your choice to make; it needs a builder profile.

**Project (fallback, every plan).**

1. Create a project, open its settings, and paste
   [`adapters/chatgpt/project-instructions.md`](adapters/chatgpt/project-instructions.md)
   into the instructions.
2. Add the files from `adapters/chatgpt/knowledge/`. Free plans allow 5
   files per project: add `01-route-and-define.md`,
   `02-whats-changed-and-evidence.md` and the ones for your work (for
   example `04-audit.md`, `05-review.md`).
3. Add your house rules to the project files, and start each analysis in
   that project.

## Codex

```bash
codex plugin marketplace add C-Kapsalis/devils-analyst
codex plugin add devils-analyst@devils-analyst
```

Run `codex`, open `/hooks`, review and trust the session hook, and start a
new thread. Codex also reads `AGENTS.md` from the project root, so copying it
into a project works without the plugin.

## GitHub Copilot CLI

```bash
copilot plugin marketplace add C-Kapsalis/devils-analyst
copilot plugin install devils-analyst@devils-analyst
```

The plugin loads the skills and the session hook. It has no slash command
for Copilot CLI: GitHub's plugin reference does not document the format of
a plugin command file, so I have not shipped one. Name the job in your
message instead ("audit our GA4 setup").

## GitHub Copilot Chat (VS Code, JetBrains, Visual Studio)

Copy [`.github/copilot-instructions.md`](.github/copilot-instructions.md) to
the same path in your repository.

## Gemini CLI

```bash
gemini extensions install https://github.com/C-Kapsalis/devils-analyst
```

Loads `AGENTS.md` as always-on context and adds `/devils-analyst`. The Claude session hook lives at
`hooks/claude-hooks.json`, not `hooks/hooks.json`, so Gemini does not try to
load it.

## OpenCode

OpenCode reads `AGENTS.md` from the project root: copy it into your project.
For the `/devils-analyst` command, copy
[`.opencode/command/`](.opencode/command/) into your project's
`.opencode/command/`.

## Cursor

Copy [`.cursor/rules/devils-analyst.mdc`](.cursor/rules/devils-analyst.mdc) into
your project's `.cursor/rules/`.

## Windsurf

Copy [`.windsurf/rules/devils-analyst.md`](.windsurf/rules/devils-analyst.md) into
your project's `.windsurf/rules/`. Windsurf caps a rule file at 6,000
characters, so this one is a compact version of `AGENTS.md` (about 3,400
characters): house rules, routing, the definition rules, evidence checks,
audits, decoys, the adversary and the output format, with a pointer to the
full skills.

## Cline

Copy [`.clinerules/devils-analyst.md`](.clinerules/devils-analyst.md) into your
project's `.clinerules/`.

## Kiro

Copy [`.kiro/steering/devils-analyst.md`](.kiro/steering/devils-analyst.md) to
`~/.kiro/steering/` (every project) or `.kiro/steering/` in one project.

## OpenClaw

Copy [`.openclaw/skills/devils-analyst`](.openclaw/skills/) into
`~/.openclaw/skills/`. It is not on ClawHub.

## Any other agent

Copy [`AGENTS.md`](AGENTS.md) into the agent's rules or instructions file.
For agents that support Agent Skills, install the folders in `skills/` as
skills.

## Uninstall

| Host | Command |
|---|---|
| Claude Code | `/plugin remove devils-analyst` |
| Claude (web, Desktop) | Customize > Plugins or Customize > Skills, then remove |
| ChatGPT | Remove the skills, the GPT or the project |
| Codex | `codex plugin remove devils-analyst` |
| Copilot CLI | `copilot plugin uninstall devils-analyst` |
| Gemini CLI | `gemini extensions uninstall devils-analyst` |
| Rules files (Cursor, Windsurf, Cline, Kiro, Copilot Chat, OpenCode, OpenClaw) | Delete the copied file |

Devil's Analyst writes no state outside its own folder, except the reports
you ask it to save.
