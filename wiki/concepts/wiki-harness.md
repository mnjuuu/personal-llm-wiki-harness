---
type: concept
status: stable
created: 2026-06-12
updated: 2026-06-12
sources:
  - ../../raw/sources/text/sample-agent-workflow.md
related:
  - ../workflows/source-to-wiki.md
---

# Wiki Harness

## Summary

A wiki harness is the reusable operating layer around a Markdown-only knowledge base.

## Key Points

- Source snapshots live under `raw/sources/text/`.
- Compiled wiki pages live under `wiki/`.
- Rules and skills tell an agent how to use the wiki safely.
- MCP tools expose the wiki as an agent-accessible interface.
- Viewer data makes the wiki inspectable in a browser.

## Details

The harness keeps knowledge out of temporary chat context. An agent can search the wiki, read evidence pages, route questions, and run maintenance checks without needing a database or API key.

## Source Notes

Based on `raw/sources/text/sample-agent-workflow.md`.

## Open Questions

- Which custom page types should a user add for their domain?

## Maintenance Notes

- Rebuild viewer data after changing wiki pages.

