#!/usr/bin/env python3
"""Build a Mermaid graph from Markdown links in wiki pages."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
OUT = WIKI / "maintenance" / "wiki-graph.md"
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")


def node_id(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", path.relative_to(WIKI).with_suffix("").as_posix())


def label(path: Path) -> str:
    return path.relative_to(WIKI).with_suffix("").as_posix()


def main() -> int:
    pages = sorted(WIKI.rglob("*.md"))
    edges = []
    for path in pages:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for _, target in LINK_RE.findall(text):
            resolved = (path.parent / target).resolve()
            if resolved.exists() and WIKI.resolve() in resolved.parents:
                edges.append((path.resolve(), resolved))
    day = date.today().isoformat()
    lines = [
        "---",
        "type: maintenance",
        "status: stable",
        f"created: {day}",
        f"updated: {day}",
        "sources:",
        "  - ../../AGENTS.md",
        "related:",
        "  - latest-maintenance-report.md",
        "---",
        "",
        "# Wiki Graph",
        "",
        "```mermaid",
        "flowchart LR",
    ]
    for page in pages:
        lines.append(f'  {node_id(page)}["{label(page)}"]')
    for src, dst in edges:
        lines.append(f"  {node_id(src)} --> {node_id(dst)}")
    lines.append("```")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(edges)} edges.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

