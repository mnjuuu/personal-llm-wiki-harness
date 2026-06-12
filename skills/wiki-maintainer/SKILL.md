---
name: wiki-maintainer
description: Maintain a Markdown-only LLM Wiki through ingest, query routing, linting, graph generation, and MCP tool usage.
---

# Wiki Maintainer Skill

Use this skill when an agent needs to work with this LLM Wiki.

## Purpose

This skill makes the wiki reusable as an agent harness. Treat the Markdown wiki as durable project memory and the MCP server as the tool boundary for reading, searching, querying, and validating that memory.

## Workflow

1. Read `wiki/index.md`.
2. Search with `wiki.search` or `python3 scripts/query_wiki.py`.
3. Read relevant concept, workflow, source, or query pages.
4. Answer with citations to wiki paths.
5. If new source material was added, run ingest and maintenance.
6. Rebuild viewer data so the browser UI reflects the latest wiki.

## MCP Tools

- `wiki.list_pages`: enumerate wiki pages.
- `wiki.get_page`: read one page.
- `wiki.search`: search wiki and raw text snapshots.
- `wiki.query`: route a user question to evidence pages.
- `wiki.maintenance_report`: inspect validation status.
- `wiki.graph`: inspect the wiki relationship graph.

## Guardrails

- Do not modify optional originals under `raw/sources/pdf/`.
- Keep generated knowledge under `wiki/`.
- Update `wiki/log.md` after meaningful edits.
- Run maintenance after structural changes.
- Do not add API keys or secrets.

