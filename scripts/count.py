"""Count what the README claims, from the files, so no number is typed by hand.

  python3 scripts/count.py

Numbered checks: rows of the check tables whose first cell is an id such as
GA1, U4 or PS12, in the audit references (one file per area) and in the
review checklist. Benchmark cases: folders in benchmarks/cases/ with a
case.yaml; "generated" have a script in benchmarks/builder/cases/.
Stdlib only.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\| ?[A-Z]{1,5}[0-9]{1,3}[a-z]? ?\|", re.M)


def rows(path: Path) -> int:
    return len(ROW.findall(path.read_text()))


def main() -> None:
    skills = sorted(p.parent.name for p in (REPO / "skills").glob("*/SKILL.md"))
    audit = {p.stem: rows(p) for p in sorted((REPO / "skills/audit/references").glob("*.md"))}
    review = rows(REPO / "skills/review/references/review-checklist.md")
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


if __name__ == "__main__":
    main()
