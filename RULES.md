# Harness Rules

These rules define how humans and agents should maintain this Markdown-only LLM Wiki.

## Ownership

- `raw/sources/text/`: source snapshots supplied by the user.
- `raw/sources/pdf/`: optional original PDFs. Treat as immutable.
- `wiki/`: generated and maintained wiki pages.
- `schema/`: page format and validation expectations.
- `tools/`: MCP server and browser viewer.
- `skills/`: reusable agent procedures.

## Source Handling

- Do not rewrite original source files unless the user explicitly asks.
- Prefer adding a new source snapshot over silently changing an old one.
- Every generated source page must cite its raw source.

## Wiki Page Requirements

Every wiki page must start with YAML frontmatter:

```yaml
---
type: concept | workflow | source | query | maintenance | index | log
status: draft | stable | needs-review | deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - ../../raw/sources/text/example.md
related:
  - ../concepts/example.md
---
```

## Agent Boundaries

- Query agents may read and search the wiki.
- Maintenance agents may run scripts and write reports.
- Editing or deleting source material requires explicit human approval.
- Prefer small, auditable Markdown changes.

## Maintenance

After ingesting or editing wiki pages, run:

```bash
python3 scripts/maintenance_lint.py
python3 scripts/build_graph.py
python3 tools/build_viewer_data.py
```

