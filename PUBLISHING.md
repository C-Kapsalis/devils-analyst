# Publishing

How Devil's Analyst gets into the public plugin directories. Each step is
something the maintainer does by hand; requirements change. Last checked
2026-10-28.

## ClawHub OpenClaw bundle

The ClawHub bundle is built from the same root plugin archive as the Claude
plugin, with an npm-safe `package.json` at the archive root. The source metadata
is maintained in `clawhub-package.json`; `scripts/package.sh` copies it into
`devils-analyst-plugin.zip`. Keep its version aligned with the platform plugin
manifests when cutting a release. The package contains skills, house rules, and
Claude lifecycle hooks; OpenClaw consumes the skill instructions, while the
Claude-only hooks are not required by OpenClaw.

Build the archive and validate it against the target OpenClaw release before
publishing:

```sh
sh scripts/package.sh
unzip -q dist/devils-analyst-plugin.zip -d /tmp/devils-analyst-plugin
clawhub package validate /tmp/devils-analyst-plugin --openclaw-version 2026.10.8
```

## Before any submission

1. The GitHub repo `C-Kapsalis/devils-analyst` is public.
2. Validate the Claude plugin and marketplace:
   ```bash
   claude plugin validate .
   claude plugin validate --strict .claude-plugin/plugin.json
   claude plugin validate --strict .claude-plugin/marketplace.json
   ```
3. Check the rules copies are current: `python3 scripts/sync-adapters.py --check`.
4. Build the release assets and attach them to a GitHub Release: push a
   `v*` tag and `.github/workflows/release.yml` runs `sh scripts/package.sh`
   and `gh release create` with the zips in `dist/`. To check the zips
   locally first: `sh scripts/package.sh` (PowerShell: `wsl sh
   scripts/package.sh`).
5. The benchmark cases rebuild byte for byte:
   `python3 benchmarks/builder/build_all.py`, then `git status --short
   benchmarks/cases` shows nothing.
6. The README numbers come from a real run (`python3 benchmarks/report.py
   <log>`), with no `{{DA_*}}` placeholder left, and the counts match
   `python3 scripts/count.py`.

## Claude plugin directory

Source: <https://claude.com/docs/plugins/submit> and
<https://claude.com/docs/directory/publish>. The short link
`clau.de/plugin-directory-submission` redirects there. The GitHub repo
`anthropics/claude-plugins-community` is a read-only mirror of the
directory: pull requests there are not the way in.

Who can submit: anyone on a paid Claude plan (Pro, Max, Team, Enterprise).
On Team and Enterprise, an Owner, or a role with the Directory permission.

Where: claude.ai/directory/manage > Submit new > Plugin bundle. Your GitHub
account must be connected and able to push to the repo. The repo can stay
private during review (with the Claude GitHub App installed and consent to
upload the source), but it must be public before the listing goes live.

What the form asks for:

1. **Source:** repository (URL or `owner/repo`), plugin path (optional; leave
   empty, the plugin is the repo root), branch or tag (optional), then
   Validate.
2. **Listing details:** read-only, taken from `.claude-plugin/plugin.json`
   and `README.md`.
3. **Data handling:** whether the plugin reads or stores personal data,
   sends data to services it does not declare, how long it keeps data, and
   whether it is meant for people under 18. For Devil's Analyst: it reads
   the data the user's own connectors, files or warehouse give the agent and
   the house rules in the user's project; it stores nothing beyond reports
   the user asks it to save; it calls no service of its own (the optional
   Power BI tools in `power-bi-definitions` are fetched from their public
   GitHub releases only when the user runs them); it is not aimed at
   minors.
4. **Compliance:** a contact email and four acknowledgements.
5. **Review and submit:** update method (GitHub push webhook, or scheduled
   check only), an auto-publish toggle, then Submit for review.

Review: every version gets automated validation and a security scan; a
person reviews a new listing, and a version can be held for a reviewer. The
limit is 10 submissions per organization per 24 hours.

## OpenAI plugin directory (ChatGPT and Codex)

Source: <https://developers.openai.com/plugins/build/plugins>,
<https://developers.openai.com/plugins/deploy/submission> and
<https://developers.openai.com/plugins/guides/submit-claude-plugin>. OpenAI's
help center (<https://help.openai.com/en/articles/8798878>) describes the
retirement of custom GPTs in favor of plugins.

Devil's Analyst is a skills-only plugin: no MCP server, no app. It relies
on whatever data connectors the user already has. The ZIP excludes lifecycle
hooks and contains a portable `plugin.json`, listing metadata and icon.

Package: `dist/devils-analyst-chatgpt.zip`, built by `scripts/package.sh`:

```
plugin.json                                # adapters/chatgpt/plugin.json
assets/icon.png                            # listing icon
skills/devils-analyst-route-question/SKILL.md   # + references/
skills/devils-analyst-<skill>/SKILL.md         # one folder per skill
LICENSE
```

`plugin.json` declares the Agent Plugins schema
(`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`) with `name`,
`version` and `description`. OpenAI's guide for existing Claude plugins says
the portal also accepts a Claude plugin zip and converts it, as long as the
hooks are removed; the dedicated zip avoids that step.

The public directory is shared by ChatGPT and Codex. The maintainer must use
a verified publisher identity, review the metadata and skill scan, complete
the required policy attestations, submit for review and publish after
approval. Package validation does not guarantee approval.

Steps:

1. Open the plugin submission portal linked from the submission page above.
2. Upload `devils-analyst-chatgpt.zip`.
3. Fill in the listing (name, description, links: use the GitHub repo for
   the website and support).
4. Submit for review. After approval, choose when to publish.

Before submitting, read the skills once for wording that assumes a specific
host. Some do: `marketing-dashboard` has a guide to Claude Dashboards, and
`power-bi-definitions` mentions `${CLAUDE_SKILL_DIR}` and Claude Projects.
Decide whether to keep those as they are (they degrade to plain advice) or
to add a ChatGPT note.

## Other directories

- **Codex:** the repo already works as a Codex marketplace
  (`.agents/plugins/marketplace.json`); no submission needed for
  `codex plugin marketplace add C-Kapsalis/devils-analyst`.
- **Gemini CLI extensions, ClawHub (OpenClaw), skills.sh:** not submitted.
  Each has its own listing process; check its docs before you publish.
