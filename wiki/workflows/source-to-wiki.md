---
type: workflow
status: stable
created: 2026-06-12
updated: 2026-06-12
sources:
  - ../../raw/sources/text/sample-agent-workflow.md
related:
  - ../concepts/wiki-harness.md
---

# Source To Wiki Workflow

## Summary

This workflow turns one raw source snapshot into a wiki page and visible browser output.

## Key Points

1. Add a `.md` or `.txt` file to `raw/sources/text/`.
2. Run `python3 scripts/ingest_sources.py`.
3. Run maintenance and graph scripts.
4. Run `python3 tools/build_viewer_data.py`.
5. Open `tools/viewer.html` through a local web server.

## Details

The ingest script creates source pages under `wiki/sources/`. The maintenance script checks schema, links, missing sources, orphan pages, and duplicate titles. The viewer data script packages the latest Markdown files into JSON for the browser viewer.

## Source Notes

Based on `raw/sources/text/sample-agent-workflow.md`.

## Open Questions

- Should future versions add a write-capable MCP tool with human approval?

## Maintenance Notes

- Keep source snapshots stable and auditable.

