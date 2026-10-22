"""Copy AGENTS.md into every rules-file adapter, with each agent's frontmatter,
build the ChatGPT instructions from the compact rules, and bundle the skills
into ten ChatGPT knowledge files.

Sources (edit these, never the copies):

  AGENTS.md                          rules-file adapters (Cursor, Cline, Copilot
                                     Chat, Kiro, OpenClaw)
  adapters/windsurf/devils-analyst.md   the compact version: Windsurf caps a
                                     rule file at 6,000 characters; the ChatGPT
                                     instructions start from it too
  skills/*/                          the ChatGPT knowledge bundles
  house-rules/README.md, TEMPLATE.md

Relative links in the knowledge copies are rewritten: to the knowledge file
and section that carries the target, or to the file on GitHub.

  python3 scripts/sync-adapters.py          # write the copies
  python3 scripts/sync-adapters.py --check  # exit 1 if any copy is stale

Stdlib only.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DESC = ("Devil's Analyst: the devil's advocate on your marketing team. Argues with "
        "the marketing data your agent pulls (GA4, ads platforms, Search Console, email, "
        "CRM, Shopify, warehouses, Power BI) before you act on it.")

ADAPTERS = {
    ".cursor/rules/devils-analyst.mdc":
        f"---\ndescription: {DESC}\nglobs:\nalwaysApply: true\n---\n\n",
    ".clinerules/devils-analyst.md": "",
    ".github/copilot-instructions.md": "",
    ".kiro/steering/devils-analyst.md":
        "---\ntitle: Devil's Analyst, argue with the data before you act on it\ninclusion: always\n---\n\n",
    ".openclaw/skills/devils-analyst/SKILL.md":
        f'---\nname: devils-analyst\ndescription: "{DESC} Use when the user asks about marketing '
        'data, a marketing report, dashboard or deck, or a decision that rests on those numbers."\n'
        "homepage: https://github.com/C-Kapsalis/devils-analyst\nlicense: MIT\n---\n\n",
}

WINDSURF_SRC = REPO / "adapters" / "windsurf" / "devils-analyst.md"
WINDSURF_DST = ".windsurf/rules/devils-analyst.md"
WINDSURF_LIMIT = 6000

CHATGPT = REPO / "adapters" / "chatgpt"
KNOWLEDGE = CHATGPT / "knowledge"
GPT_LIMIT = 8000  # the commonly cited custom GPT instructions limit

# Ten knowledge files: OpenAI's pages give both 10 and 20 as the file limit.
BUNDLES = {
    "01-route-and-define.md": ["route-question", "metric-definitions"],
    "02-whats-changed-and-evidence.md": ["whats-changed", "evidence-check"],
    "03-diagnose-and-playbooks.md": ["diagnose"],
    "04-audit.md": ["audit"],
    "05-review.md": ["review"],
    "06-dashboards.md": ["marketing-dashboard"],
    "07-power-bi.md": ["power-bi-definitions"],
    "08-pricing-channels-brand.md": ["pricing-promotions", "channel-audit", "brand-health"],
    "09-product-and-models.md": ["product-decisions", "marketing-models"],
    "10-research.md": ["research-design", "hybrid-research"],
}

GPT_KNOWLEDGE_NOTE = """
## Knowledge files

The full method is in the knowledge files. Before answering, search the one
that matches the job:

- 01-route-and-define: routing, connectors, the metric catalog, source traps,
  SQL patterns, and the house-rules template
- 02-whats-changed-and-evidence: why a number moved; did it work
- 03-diagnose-and-playbooks: the likely cause and what to do, 59 playbooks
- 04-audit: account and setup audits, the numbered checks per area
- 05-review: reviewing a report, deck or dashboard, and the decoy list
- 06-dashboards: building a dashboard or report
- 07-power-bi: reading a Power BI model's measures
- 08-pricing-channels-brand: pricing and promotions, channel economics,
  brand health
- 09-product-and-models: concept tests, business cases, regression, CLV,
  forecasting
- 10-research: survey and research design, synthetic respondents

There are no files to read in a chat unless the user uploads them: ask for
the export, or for the house rules as text.
"""


GITHUB = "https://github.com/C-Kapsalis/devils-analyst/blob/main/"
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
HOUSE_RULES_FILES = ("README.md", "TEMPLATE.md")


def sections():
    """{repo-relative path: (knowledge file, section title)} for every file
    the knowledge bundles carry."""
    where = {}
    for fname, skills in BUNDLES.items():
        for name in skills:
            root = REPO / "skills" / name
            for ref in sorted(root.rglob("*.md")):
                rel = ref.relative_to(REPO).as_posix()
                title = f"Skill: {name}" if ref.name == "SKILL.md" else f"File: {name}/{ref.relative_to(root).as_posix()}"
                where[rel] = (fname, title)
        if fname.startswith("01-"):
            for extra in HOUSE_RULES_FILES:
                where[f"house-rules/{extra}"] = (fname, f"File: house-rules/{extra}")
    return where


def unlink(text, source, where):
    """Relative links do not resolve in an uploaded knowledge file: point each
    one at the knowledge file and section that carries the target, or at the
    file on GitHub."""
    def fix(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"[a-z][a-z0-9+.-]*:|#", target):
            return m.group(0)
        path = (source.parent / target.split("#")[0]).resolve()
        try:
            rel = path.relative_to(REPO).as_posix()
        except ValueError:
            return label
        if rel in where:
            fname, title = where[rel]
            ref = f'section "{title}" in {fname}'
            return ref if label.strip("`") == target else f"{label} ({ref})"
        return f"[{label}]({GITHUB}{rel})"
    return LINK.sub(fix, text)


def bundle(skills, where):
    parts = []
    for name in skills:
        root = REPO / "skills" / name
        skill_md = root / "SKILL.md"
        parts.append(f"# Skill: {name}\n\n{unlink(skill_md.read_text().strip(), skill_md, where)}\n")
        for ref in sorted(root.rglob("*.md")):
            if ref.name == "SKILL.md":
                continue
            rel = ref.relative_to(root)
            parts.append(f"## File: {name}/{rel}\n\n{unlink(ref.read_text().strip(), ref, where)}\n")
    return "\n---\n\n".join(parts)


def knowledge_copies():
    where = sections()
    for fname, skills in BUNDLES.items():
        text = bundle(skills, where)
        if fname.startswith("01-"):
            for extra in HOUSE_RULES_FILES:
                src = REPO / "house-rules" / extra
                body = unlink(src.read_text().strip(), src, where)
                text += f"\n---\n\n## File: house-rules/{extra}\n\n{body}\n"
        yield KNOWLEDGE / fname, text


def chatgpt_copies(compact):
    gpt = compact.rstrip() + "\n" + GPT_KNOWLEDGE_NOTE
    yield CHATGPT / "custom-gpt-instructions.md", gpt
    yield CHATGPT / "project-instructions.md", gpt


def main() -> int:
    check = "--check" in sys.argv
    body = (REPO / "AGENTS.md").read_text()
    compact = WINDSURF_SRC.read_text()
    if len(compact) >= WINDSURF_LIMIT:
        print(f"too long: {WINDSURF_SRC.relative_to(REPO)} is {len(compact)} characters "
              f"(Windsurf limit {WINDSURF_LIMIT})")
        return 1
    targets = [(REPO / rel, head + body) for rel, head in ADAPTERS.items()]
    targets.append((REPO / WINDSURF_DST, compact))
    targets += list(chatgpt_copies(compact))
    targets += list(knowledge_copies())
    gpt_len = len(dict(chatgpt_copies(compact))[CHATGPT / "custom-gpt-instructions.md"])
    if gpt_len >= GPT_LIMIT:
        print(f"too long: custom GPT instructions are {gpt_len} characters (limit {GPT_LIMIT})")
        return 1

    stale = []
    for path, want in targets:
        rel = path.relative_to(REPO)
        if check:
            if not path.exists() or path.read_text() != want:
                stale.append(str(rel))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(want)
        print(f"wrote {rel}")
    for rel in stale:
        print(f"stale: {rel} (run python3 scripts/sync-adapters.py)")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
