#!/usr/bin/env python3
"""Dependency-free stdio MCP-style server for the local Markdown wiki."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RAW_TEXT = ROOT / "raw" / "sources" / "text"
TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]+")


@dataclass
class ToolResult:
    text: str

    def as_mcp(self) -> dict[str, Any]:
        return {"content": [{"type": "text", "text": self.text}]}


def tokens(value: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(value) if len(token) > 1}


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def safe_wiki_path(path_value: str) -> Path:
    candidate = (ROOT / path_value).resolve()
    if WIKI.resolve() not in candidate.parents and candidate != WIKI.resolve():
        raise ValueError("Only files under wiki/ can be read.")
    if candidate.suffix != ".md":
        raise ValueError("Only Markdown pages can be read.")
    if not candidate.exists():
        raise FileNotFoundError(path_value)
    return candidate


def tool_list_pages(_: dict[str, Any]) -> ToolResult:
    lines = ["# Wiki Pages"]
    lines.extend(f"- `{relative(path)}`" for path in markdown_files(WIKI))
    return ToolResult("\n".join(lines))


def tool_get_page(args: dict[str, Any]) -> ToolResult:
    path = safe_wiki_path(str(args.get("path", "")))
    return ToolResult(path.read_text(encoding="utf-8", errors="ignore"))


def tool_search(args: dict[str, Any]) -> ToolResult:
    query = str(args.get("query", ""))
    query_tokens = tokens(query)
    rows = []
    for root in [WIKI, RAW_TEXT]:
        for path in markdown_files(root):
            text = path.read_text(encoding="utf-8", errors="ignore")
            score = sum(text.lower().count(token) for token in query_tokens)
            if score:
                preview = next((line.strip() for line in text.splitlines() if line.strip()), "")
                rows.append((score, relative(path), preview[:160]))
    rows.sort(reverse=True)
    lines = [f"# Search: {query}", ""]
    lines.extend(f"- score={score} `{path}` - {preview}" for score, path, preview in rows[:10])
    if len(lines) == 2:
        lines.append("- No matches.")
    return ToolResult("\n".join(lines))


def tool_query(args: dict[str, Any]) -> ToolResult:
    question = str(args.get("question", ""))
    return ToolResult(
        "# Wiki Query Routing\n\n"
        f"Question: {question}\n\n"
        "Use these evidence pages first:\n\n"
        + tool_search({"query": question}).text
    )


def tool_maintenance(_: dict[str, Any]) -> ToolResult:
    path = WIKI / "maintenance" / "latest-maintenance-report.md"
    if path.exists():
        return ToolResult(path.read_text(encoding="utf-8", errors="ignore"))
    return ToolResult("No maintenance report exists. Run `python3 scripts/maintenance_lint.py`.")


def tool_graph(_: dict[str, Any]) -> ToolResult:
    path = WIKI / "maintenance" / "wiki-graph.md"
    if path.exists():
        return ToolResult(path.read_text(encoding="utf-8", errors="ignore"))
    return ToolResult("No graph exists. Run `python3 scripts/build_graph.py`.")


TOOLS = {
    "wiki.list_pages": {
        "description": "List all Markdown wiki pages.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_list_pages,
    },
    "wiki.get_page": {
        "description": "Read one Markdown page under wiki/.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
        "handler": tool_get_page,
    },
    "wiki.search": {
        "description": "Search wiki pages and raw text snapshots.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        "handler": tool_search,
    },
    "wiki.query": {
        "description": "Route a user question to relevant wiki evidence.",
        "inputSchema": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"],
        },
        "handler": tool_query,
    },
    "wiki.maintenance_report": {
        "description": "Return the latest wiki maintenance report.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_maintenance,
    },
    "wiki.graph": {
        "description": "Return the Mermaid wiki graph.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_graph,
    },
}


def response(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return response(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "personal-llm-wiki", "version": "1.0.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return response(
            request_id,
            {
                "tools": [
                    {
                        "name": name,
                        "description": meta["description"],
                        "inputSchema": meta["inputSchema"],
                    }
                    for name, meta in TOOLS.items()
                ]
            },
        )
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in TOOLS:
            return error_response(request_id, -32602, f"Unknown tool: {name}")
        try:
            return response(request_id, TOOLS[name]["handler"](args).as_mcp())
        except Exception as exc:  # noqa: BLE001 - JSON-RPC boundary
            return error_response(request_id, -32000, str(exc))
    return error_response(request_id, -32601, f"Unknown method: {method}")


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            result = handle(json.loads(line))
        except Exception as exc:  # noqa: BLE001 - JSON-RPC boundary
            result = error_response(None, -32700, str(exc))
        if result is not None:
            print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

