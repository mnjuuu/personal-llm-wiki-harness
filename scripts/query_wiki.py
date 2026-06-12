#!/usr/bin/env python3
"""Search wiki pages and raw text snapshots for a user query."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RAW_TEXT = ROOT / "raw" / "sources" / "text"
TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]+")


def tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if len(token) > 1]


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def score(query_tokens: list[str], text: str) -> int:
    counts = Counter(tokens(text))
    return sum(counts[token] for token in query_tokens)


def snippet(text: str, query_tokens: list[str]) -> str:
    for line in [line.strip() for line in text.splitlines() if line.strip()]:
        lowered = line.lower()
        if any(token in lowered for token in query_tokens):
            return line[:220]
    return ""


def ranked(root: Path, query_tokens: list[str]) -> list[tuple[int, Path, str]]:
    rows = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rows.append((score(query_tokens, text), path, text))
    return sorted(rows, reverse=True, key=lambda item: item[0])


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 scripts/query_wiki.py \"question\"")
        return 1
    query = " ".join(argv[1:])
    query_tokens = tokens(query)
    print(f"# Query\n\n{query}\n")
    print("## Relevant Wiki Pages")
    for item_score, path, text in ranked(WIKI, query_tokens)[:8]:
        if item_score:
            print(f"- `{path.relative_to(ROOT)}` score={item_score}: {snippet(text, query_tokens)}")
    print("\n## Relevant Raw Text Snapshots")
    for item_score, path, text in ranked(RAW_TEXT, query_tokens)[:5]:
        if item_score:
            print(f"- `{path.relative_to(ROOT)}` score={item_score}: {snippet(text, query_tokens)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

