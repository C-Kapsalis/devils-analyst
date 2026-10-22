"""Count what the README claims, from the files, so no number is typed by hand.

  python3 scripts/count.py

Numbered checks: rows of the check tables whose first cell is an id such as
GA1, U4 or PS12, in the audit references (one file per area), and such as
RV-A1 in the review checklist (prefixed so review ids never clash with the
audit area letters). Benchmark cases: folders in benchmarks/cases/ with a
case.yaml; "generated" have a script in benchmarks/builder/cases/.

It also checks every skill's frontmatter description against the Agent Skills
limit of 1,024 characters, and that every review check id carries the RV-
prefix, and exits 1 if either fails.
Stdlib only.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\| ?(?:RV-)?[A-Z]{1,5}[0-9]{1,3}[a-z]? ?\|", re.M)
UNPREFIXED = re.compile(r"^\| ?([A-Z]{1,5}[0-9]{1,3}[a-z]?) ?\|", re.M)
DESC_LIMIT = 1024  # Agent Skills: description, at most 1,024 characters


def description(skill_md: Path) -> str:
    """The frontmatter description: a plain or quoted line, or a folded
    (>, >-) or literal (|, |-) block. Enough YAML for SKILL.md files."""
    lines = skill_md.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return ""
        if not line.startswith("description:"):
            continue
        value = line[len("description:"):].strip()
        if value[:1] in (">", "|"):
            block = []
            for nxt in lines[i + 1:]:
                if nxt.strip() == "---" or (nxt and not nxt[0].isspace()):
                    break
                block.append(nxt.strip())
            sep = " " if value[0] == ">" else "\n"
            return sep.join(block).strip()
        if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        return value
    return ""


def rows(path: Path) -> int:
    return len(ROW.findall(path.read_text(encoding='utf-8')))


def main() -> int:
    skills = sorted(p.parent.name for p in (REPO / "skills").glob("*/SKILL.md"))
    audit = {p.stem: rows(p) for p in sorted((REPO / "skills/audit/references").glob("*.md"))}
    checklist = REPO / "skills/review/references/review-checklist.md"
    review = rows(checklist)
    bare = UNPREFIXED.findall(checklist.read_text(encoding='utf-8'))
    playbooks = list((REPO / "skills/diagnose/references/playbooks").rglob("*.md"))
    cases = sorted(p.parent.name for p in (REPO / "benchmarks/cases").glob("*/case.yaml"))
    scripts = {p.stem for p in (REPO / "benchmarks/builder/cases").glob("*.py")}
    generated = [c for c in cases if c in scripts]
    breadth = [c for c in cases if c.startswith("bx-")]
    audits_reviews = [c for c in cases if c.startswith(("audit-", "review-"))]

    print(f"skills: {len(skills)}")
    print(f"numbered checks: {sum(audit.values()) + review} "
          f"(audit {sum(audit.values())} in {len([v for v in audit.values() if v])} areas, review {review})")
    for area, n in audit.items():
        print(f"  audit/{area}: {n}")
    print(f"diagnose playbooks: {len(playbooks)}")
    print(f"benchmark cases: {len(cases)} (generated {len(generated)}, "
          f"hand-written {len(cases) - len(generated)})")
    print(f"  breadth (bx-*): {len(breadth)}")
    print(f"  audits and reviews: {len(audits_reviews)}")
    print(f"  focused trap cases: {len(cases) - len(breadth) - len(audits_reviews)}")

    lengths = {p.parent.name: len(description(p)) for p in sorted((REPO / "skills").glob("*/SKILL.md"))}
    longest = max(lengths, key=lengths.get)
    print(f"longest skill description: {longest}, {lengths[longest]} characters (limit {DESC_LIMIT})")
    over = {k: v for k, v in lengths.items() if v > DESC_LIMIT}
    for name, n in over.items():
        print(f"too long: skills/{name}/SKILL.md description is {n} characters (limit {DESC_LIMIT})")
    for cid in bare:
        print(f"unprefixed review id: {cid} in skills/review/references/review-checklist.md "
              f"(write RV-{cid}; bare letters clash with the audit areas)")
    return 1 if over or bare else 0


if __name__ == "__main__":
    sys.exit(main())
