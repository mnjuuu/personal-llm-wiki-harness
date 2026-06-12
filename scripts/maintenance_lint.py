#!/usr/bin/env python3
"""Run structural checks for the Markdown-only wiki."""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import date
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
OUT = WIKI / "maintenance" / "latest-maintenance-report.md"
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")


def pages() -> list[Path]:
    return sorted(path for path in WIKI.rglob("*.md") if path.is_file())


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def frontmatter(text: str) -> str:
    return text.split("\n---\n", 1)[0] if has_frontmatter(text) else ""


def missing_fields(text: str) -> list[str]:
    fm = frontmatter(text)
    required = ["type", "status", "created", "updated", "sources", "related"]
    return [field for field in required if not re.search(rf"^{field}:\s*", fm, re.MULTILINE)]


def links(path: Path, text: str) -> list[Path]:
    out = []
    for _, target in LINK_RE.findall(text):
        if target.startswith("http"):
            continue
        out.append((path.parent / target).resolve())
    return out


def reachable(graph: dict[Path, list[Path]]) -> set[Path]:
    start = (WIKI / "index.md").resolve()
    seen = set()
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        queue.extend(graph.get(current, []))
    return seen


def main() -> int:
    all_pages = pages()
    missing_frontmatter = []
    missing_schema = []
    broken = []
    title_index = defaultdict(list)
    graph = defaultdict(list)
    for path in all_pages:
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        if not has_frontmatter(text):
            missing_frontmatter.append(rel)
        else:
            missing = missing_fields(text)
            if missing:
                missing_schema.append((rel, missing))
        title_index[path.stem.replace("-", " ").lower()].append(rel)
        for target in links(path, text):
            graph[path.resolve()].append(target)
            if not target.exists():
                broken.append((rel, target))
    seen = reachable(graph)
    orphans = [
        path.relative_to(ROOT)
        for path in all_pages
        if path.resolve() not in seen and path.name != "index.md"
    ]
    duplicates = {title: paths for title, paths in title_index.items() if len(paths) > 1}
    day = date.today().isoformat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "type: maintenance",
        "status: stable",
        f"created: {day}",
        f"updated: {day}",
        "sources:",
        "  - ../../AGENTS.md",
        "related:",
        "  - wiki-graph.md",
        "---",
        "",
        "# Latest Maintenance Report",
        "",
        f"Generated: {day}",
        "",
        "## Summary",
        f"- Wiki pages checked: {len(all_pages)}",
        f"- Missing frontmatter: {len(missing_frontmatter)}",
        f"- Missing required schema fields: {len(missing_schema)}",
        f"- Broken links: {len(broken)}",
        f"- Orphan pages: {len(orphans)}",
        f"- Duplicate normalized titles: {len(duplicates)}",
        "",
        "## Details",
    ]
    for label, items in [
        ("Missing Frontmatter", missing_frontmatter),
        ("Broken Links", [f"{src} -> {dst}" for src, dst in broken]),
        ("Orphan Pages", orphans),
    ]:
        lines.extend(["", f"### {label}"])
        lines.extend([f"- `{item}`" for item in items] or ["- None"])
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

