"""Turn a `claude plugin eval` text log into the benchmark results page.

Usage:
  python3 benchmarks/report.py LOG [--date YYYY-MM-DD] [--model NAME]
                                   [--out-dir DIR] [--assets-dir DIR]
                                   [--readme PATH] [--no-readme]

Reads the per-run lines of the log, for example

    bx-ga4-record-month run 2/3 [with]: score 0.75  $0.03
      ✓ subtle-recall (weight 3): judge votes: PASS PASS FAIL

and writes:

  benchmarks/results/<date>.md           overall and per-group tables, with
                                         and without the plugin, with counts
  assets/benchmark-groups-{light,dark}.svg   mean score per case group

and fills the {{DA_*}} placeholders in README.md. A filled value is wrapped in
<!--NAME-->...<!--/NAME--> markers, so running the script again on a new log
updates it in place.

Case groups, by name:
  breadth   bx-*                 a realistic draft or export with several subtle
                                 problems and decoys, and a decision to make
  audit     audit-*, review-*    an account, setup or report to audit or review
  focused   everything else      a clean export built around a named trap

A grader counts as passed for a run when its line starts with ✓ (the majority
of the judge votes). Stdlib only; Python 3.9 or later.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parents[1]
NAME = "Devil's Analyst"

# (key, label for tables, grader slugs that feed it). "allpass" is computed.
METRICS = [
    ("allpass", "Runs where every grader passed", ()),
    ("recall", "Planted problems found (enough of them, with evidence)",
     ("subtle-recall", "planted-recall")),
    ("decision", "Right decision on the proposal", ("decision",)),
    ("first", "Must-fix problems ranked first", ("must-fix-first",)),
    ("nofalse", "Correct details (decoys) left alone",
     ("no-false-alarms", "decoys-left-alone")),
    ("control", "Clean control called clean", ("called-clean",)),
]
GROUPS = ["focused", "breadth", "audit"]
GROUP_LABEL = {"focused": "Focused trap cases", "breadth": "Breadth cases",
               "audit": "Audits and reviews", "all": "All cases"}
ARMS = ("with", "without")

RUN_RE = re.compile(r"^\s+(\S+) run (\d+)/(\d+) \[(with|without)\]: score ([\d.]+)")
GRADER_RE = re.compile(r"^\s+([✓✗]) ([\w-]+) (?:\(weight (\d+)\)|\[[^\]]*\]): (.*)$")
REPORT_RE = re.compile(r"results/(\d{4}-\d{2}-\d{2})T")


def case_group(name: str) -> str:
    if name.startswith("bx-"):
        return "breadth"
    if name.startswith(("audit-", "review-")):
        return "audit"
    return "focused"


def parse(text: str) -> dict:
    """{"runs": [...], "date": str|None}. Each run:
    {"case", "arm", "run", "score", "graders": {slug: bool}, "votes": {slug: str}}"""
    runs, current, date = [], None, None
    for line in text.splitlines():
        m = RUN_RE.match(line)
        if m:
            current = {"case": m.group(1), "run": int(m.group(2)), "arm": m.group(4),
                       "score": float(m.group(5)), "graders": {}, "votes": {}}
            runs.append(current)
            continue
        g = GRADER_RE.match(line)
        if g and current is not None:
            slug = g.group(2)
            if slug == "skill-fired":
                current["skill_fired"] = g.group(1) == "✓"
            else:
                current["graders"][slug] = g.group(1) == "✓"
                current["votes"][slug] = g.group(4).strip()
            continue
        current = None  # any other line ends the run's grader block
        d = REPORT_RE.search(line)
        if d:
            date = d.group(1)
    return {"runs": runs, "date": date}


def tally(runs: list) -> dict:
    """{(group, arm): {metric: [passed, total], "score": [sum, n], "cases": set, "skill": [..]}}"""
    out = defaultdict(lambda: {"score": [0.0, 0], "cases": set(), "skill": [0, 0],
                               **{k: [0, 0] for k, *_ in METRICS}})
    for r in runs:
        for grp in (case_group(r["case"]), "all"):
            t = out[(grp, r["arm"])]
            t["score"][0] += r["score"]
            t["score"][1] += 1
            t["cases"].add(r["case"])
            if "skill_fired" in r:
                t["skill"][0] += r["skill_fired"]
                t["skill"][1] += 1
            if r["graders"]:
                t["allpass"][0] += all(r["graders"].values())
                t["allpass"][1] += 1
            for key, _, slugs in METRICS:
                for slug in slugs:
                    if slug in r["graders"]:
                        t[key][0] += r["graders"][slug]
                        t[key][1] += 1
    return out


def rate(pair):
    return pair[0] / pair[1] if pair[1] else None


def pct(pair) -> str:
    r = rate(pair)
    return "n/a" if r is None else f"{round(100 * r)}%"


def cell(pair) -> str:
    return "n/a" if not pair[1] else f"{pct(pair)} ({pair[0]}/{pair[1]})"


def mean(pair) -> str:
    return "n/a" if not pair[1] else f"{pair[0] / pair[1]:.2f}"


def table(t: dict, grp: str) -> list:
    w, wo = t[(grp, "with")], t[(grp, "without")]
    lines = [f"| Metric | With {NAME} | Without | Difference |", "|---|--:|--:|--:|"]
    for key, label, _ in METRICS:
        if not w[key][1] and not wo[key][1]:
            continue
        a, b = rate(w[key]), rate(wo[key])
        diff = "n/a" if a is None or b is None else f"{round(100 * (a - b)):+d} pts"
        lines.append(f"| {label} | {cell(w[key])} | {cell(wo[key])} | {diff} |")
    a, b = w["score"], wo["score"]
    diff = "n/a" if not a[1] or not b[1] else f"{a[0] / a[1] - b[0] / b[1]:+.2f}"
    lines.append(f"| Mean score (0 to 1) | {mean(a)} | {mean(b)} | {diff} |")
    lines.append(f"| Cases / runs | {len(w['cases'])} / {w['score'][1]} | "
                 f"{len(wo['cases'])} / {wo['score'][1]} | |")
    return lines


def results_markdown(t: dict, runs: list, log: Path, date: str, model: str) -> str:
    groups = [g for g in GROUPS if t[(g, "with")]["score"][1] or t[(g, "without")]["score"][1]]
    cases = sorted({r["case"] for r in runs})
    per_case = defaultdict(lambda: {"with": [], "without": []})
    for r in runs:
        per_case[r["case"]][r["arm"]].append(r["score"])
    sk = t[("all", "with")]["skill"]
    out = [
        f"# Benchmark results, {date}",
        "",
        f"Source log: `{log.name}`. Model under test: {model}. Judge: the `claude plugin "
        "eval` default, three votes per grader; a grader passes on a majority. Generated "
        "by `benchmarks/report.py`; method in [METHOD.md](../METHOD.md).",
        "",
        f"{len(cases)} cases, {len(runs)} runs in all. Each percentage is passed runs over "
        "graded runs for that metric, with the counts in brackets. Small counts mean wide "
        "uncertainty: one run is several points.",
        "",
    ]
    if sk[1]:
        out += [f"A {NAME} skill fired in {cell(sk)} of the with-plugin runs.", ""]
    out += ["## All cases", ""] + table(t, "all") + [""]
    for g in groups:
        out += [f"## {GROUP_LABEL[g]}", ""] + table(t, g) + [""]
    out += ["## Per case", "", "| Case | Group | With (mean) | Without (mean) | Runs with / without |",
            "|---|---|--:|--:|--:|"]
    for c in cases:
        a, b = per_case[c]["with"], per_case[c]["without"]
        fa = f"{sum(a) / len(a):.2f}" if a else "n/a"
        fb = f"{sum(b) / len(b):.2f}" if b else "n/a"
        out.append(f"| {c} | {case_group(c)} | {fa} | {fb} | {len(a)} / {len(b)} |")
    return "\n".join(out) + "\n"


# ---------- SVG chart ----------

THEMES = {
    "light": {"bg": "#ffffff", "text": "#1f2328", "muted": "#59636e", "grid": "#d1d9e0",
              "with": "#2a78d6", "without": "#a8a59c"},
    "dark": {"bg": "#0d1117", "text": "#f0f6fc", "muted": "#9198a1", "grid": "#3d444d",
             "with": "#3987e5", "without": "#6b6a64"},
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def bar_chart(rows: list, title: str, desc: str, theme: str) -> str:
    """rows: [(label, with_value or None, without_value or None)], values in 0..1."""
    c = THEMES[theme]
    width, left, right = 820, 210, 70
    bar, gap, group_gap, top = 16, 2, 22, 92
    plot_w = width - left - right
    height = top + len(rows) * (2 * bar + gap + group_gap) + 30
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">',
         f'<title id="t">{escape(title)}</title>', f'<desc id="d">{escape(desc)}</desc>',
         f'<rect width="{width}" height="{height}" fill="{c["bg"]}"/>',
         f'<g font-family="{FONT}">',
         f'<text x="24" y="34" font-size="20" font-weight="600" fill="{c["text"]}">{escape(title)}</text>']
    lx = 24
    for arm, label in (("with", f"With {NAME}"), ("without", "Without")):
        p.append(f'<rect x="{lx}" y="52" width="14" height="14" rx="3" fill="{c[arm]}"/>')
        p.append(f'<text x="{lx + 20}" y="64" font-size="14" fill="{c["muted"]}">{escape(label)}</text>')
        lx += 200
    for frac in (0, 0.5, 1):
        x = left + frac * plot_w
        p.append(f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{height - 26}" '
                 f'stroke="{c["grid"]}" stroke-width="1"/>')
        p.append(f'<text x="{x:.1f}" y="{height - 8}" font-size="12" text-anchor="middle" '
                 f'fill="{c["muted"]}">{frac:.1f}</text>')
    y = top
    for label, a, b in rows:
        p.append(f'<text x="{left - 12}" y="{y + bar + gap / 2 + 5:.1f}" font-size="14" '
                 f'text-anchor="end" fill="{c["text"]}">{escape(label)}</text>')
        for arm, v in (("with", a), ("without", b)):
            if v is None:
                p.append(f'<text x="{left + 6}" y="{y + 12}" font-size="12" fill="{c["muted"]}">n/a</text>')
            else:
                w = max(v * plot_w, 2)
                p.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar}" rx="4" fill="{c[arm]}"/>')
                p.append(f'<text x="{left + w + 6:.1f}" y="{y + 12.5}" font-size="12" '
                         f'fill="{c["text"] if arm == "with" else c["muted"]}">{v:.2f}</text>')
            y += bar + gap
        y += group_gap
    p += ["</g>", "</svg>"]
    return "\n".join(p) + "\n"


def charts(t: dict, assets: Path) -> None:
    rows = []
    for g in GROUPS + ["all"]:
        w, wo = t[(g, "with")]["score"], t[(g, "without")]["score"]
        if w[1] or wo[1]:
            rows.append((GROUP_LABEL[g], w[0] / w[1] if w[1] else None,
                         wo[0] / wo[1] if wo[1] else None))
    desc = f"Mean grader score (0 to 1) per case group, with and without {NAME}. " + "; ".join(
        f"{lab}: {'n/a' if a is None else f'{a:.2f}'} with, {'n/a' if b is None else f'{b:.2f}'} without"
        for lab, a, b in rows) + "."
    assets.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (assets / f"benchmark-groups-{theme}.svg").write_text(encoding='utf-8', data=
            bar_chart(rows, "Mean score per case group (0 to 1)", desc, theme))


# ---------- README placeholders ----------

def fill_readme(path: Path, values: dict) -> list:
    """Replace {{NAME}} (first run) or <!--NAME-->old<!--/NAME--> (later runs)."""
    text = path.read_text(encoding='utf-8')
    filled = []
    for name, value in values.items():
        wrapped = f"<!--{name}-->{value}<!--/{name}-->"
        token = "{{" + name + "}}"
        n = text.count(token)
        text = text.replace(token, wrapped)
        text, m = re.subn(rf"<!--{name}-->.*?<!--/{name}-->", lambda _: wrapped, text, flags=re.S)
        if n or m:
            filled.append(name)
    path.write_text(encoding='utf-8', data=text)
    return filled


def readme_values(t: dict, runs: list, date: str, model: str) -> dict:
    per_arm = defaultdict(int)
    for r in runs:
        per_arm[(r["case"], r["arm"])] += 1
    w, wo = t[("all", "with")], t[("all", "without")]
    values = {
        "DA_MODEL": model,
        "DA_CASE_COUNT": str(len({r["case"] for r in runs})),
        "DA_RUNS": str(max(per_arm.values())),
        "DA_RUN_TOTAL": str(len(runs)),
        "DA_RESULTS_DATE": date,
        "DA_RESULTS_FILE": f"benchmarks/results/{date}.md",
        "DA_SKILL_FIRED": pct(w["skill"]),
        "DA_SCORE_WITH": mean(w["score"]),
        "DA_SCORE_WITHOUT": mean(wo["score"]),
    }
    for g in GROUPS + ["all"]:
        G = g.upper()
        gw, gwo = t[(g, "with")], t[(g, "without")]
        values[f"DA_{G}_CASES"] = str(len(gw["cases"] | gwo["cases"]))
        values[f"DA_{G}_SCORE_WITH"] = mean(gw["score"])
        values[f"DA_{G}_SCORE_WITHOUT"] = mean(gwo["score"])
        for key, *_ in METRICS:
            K = key.upper()
            values[f"DA_{G}_{K}_WITH"] = pct(gw[key])
            values[f"DA_{G}_{K}_WITHOUT"] = pct(gwo[key])
            values[f"DA_{G}_{K}_N"] = str(gw[key][1])
    return values


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("log", type=Path)
    ap.add_argument("--date", help="results date (default: from the log's report path, else today)")
    ap.add_argument("--model", default="Claude Haiku 5.5", help="model under test")
    ap.add_argument("--out-dir", type=Path, default=REPO / "benchmarks" / "results")
    ap.add_argument("--assets-dir", type=Path, default=REPO / "assets")
    ap.add_argument("--readme", type=Path, default=REPO / "README.md")
    ap.add_argument("--no-readme", action="store_true", help="do not touch README.md")
    args = ap.parse_args(argv)

    text = args.log.read_text(encoding='utf-8', errors="replace")
    parsed = parse(text)
    runs = parsed["runs"]
    if not runs:
        print(f"no run lines found in {args.log}", file=sys.stderr)
        return 1
    date = args.date or parsed["date"] or dt.date.today().isoformat()
    t = tally(runs)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"{date}.md"
    out.write_text(encoding='utf-8', data=results_markdown(t, runs, args.log, date, args.model))
    charts(t, args.assets_dir)
    print(f"wrote {out}")
    print(f"wrote {args.assets_dir}/benchmark-groups-{{light,dark}}.svg")
    if not args.no_readme and args.readme.exists():
        filled = fill_readme(args.readme, readme_values(t, runs, date, args.model))
        left = sorted(set(re.findall(r"\{\{(DA_[A-Z_]+)\}\}", args.readme.read_text(encoding='utf-8'))))
        print(f"README: filled {len(filled)} placeholders" + (f"; still open: {', '.join(left)}" if left else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
