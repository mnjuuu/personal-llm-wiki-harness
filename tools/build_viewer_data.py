#!/usr/bin/env python3
"""Build JSON data used by the static browser viewer."""

from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RAW_TEXT = ROOT / "raw" / "sources" / "text"
OUT = ROOT / "tools" / "wiki-data.json"


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def title_for(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def page_type(path: Path) -> str:
    parts = path.relative_to(WIKI).parts
    if len(parts) > 1:
        return parts[0]
    if path.name == "index.md":
        return "index"
    return "page"


def preview(text: str) -> str:
    stripped = re.sub(r"---.*?---", "", text, count=1, flags=re.DOTALL)
    lines = [line.strip("#- *` ") for line in stripped.splitlines() if line.strip()]
    return " ".join(lines[:3])[:220]


def main() -> int:
    pages = []
    for path in markdown_files(WIKI):
        text = path.read_text(encoding="utf-8", errors="ignore")
        pages.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "title": title_for(text, path.stem),
                "type": page_type(path),
                "preview": preview(text),
                "content": text,
            }
        )
    raw_count = len(markdown_files(RAW_TEXT))
    OUT.write_text(
        json.dumps({"pages": pages, "rawCount": raw_count}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(pages)} wiki pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

