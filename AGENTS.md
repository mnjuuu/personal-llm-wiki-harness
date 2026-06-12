# Agent Operating Guide

This repository is a local LLM Wiki harness. Your job is to preserve useful knowledge in Markdown so both humans and agents can inspect it.

## Default Workflow

1. Read `wiki/index.md`.
2. Search `wiki/` before reading raw source snapshots.
3. Use raw text only when the wiki does not contain enough evidence.
4. Cite wiki pages or raw snapshots by path.
5. If you ingest or edit pages, run maintenance and rebuild viewer data.

## Allowed Actions

- Read `raw/sources/text/`, `wiki/`, `schema/`, `tools/`, and `skills/`.
- Create or update pages under `wiki/`.
- Run scripts under `scripts/` and `tools/`.
- Update `wiki/log.md` after meaningful changes.

## Restricted Actions

- Do not silently delete wiki pages.
- Do not modify optional originals under `raw/sources/pdf/`.
- Do not add API keys or secrets.
- Do not invent citations.

## Useful Commands

```bash
python3 scripts/ingest_sources.py
python3 scripts/query_wiki.py "your question"
python3 scripts/maintenance_lint.py
python3 scripts/build_graph.py
python3 tools/build_viewer_data.py
python3 tools/demo_client.py
```

