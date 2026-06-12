# Personal LLM Wiki Harness

Markdown files in, searchable wiki out.

This repository combines three parts into one runnable product:

- **Harness**: agent rules, page schema, and a reusable wiki-maintainer Skill.
- **LLM Wiki**: `raw/`, `wiki/`, and `schema/` folders for durable Markdown knowledge.
- **Visualization Tool**: local viewer plus a small stdio MCP server that agents can call.

No API key is required. The MVP uses local scripts, Markdown files, and a dependency-free MCP server.

## 30-Minute Quick Start

### 1. Clone and enter the repository

```bash
git clone <your-public-repo-url>
cd <repo-folder>
```

### 2. Check Python

```bash
python3 --version
```

Python 3.10 or newer is recommended. Text/Markdown ingest has no external dependency. PDF ingest is optional and needs `pypdf`.

### 3. Add one source

Put one `.md` or `.txt` file in:

```text
raw/sources/text/
```

Example:

```bash
cp /path/to/your-note.md raw/sources/text/my-note.md
```

### 4. Build the wiki

```bash
python3 scripts/ingest_sources.py
python3 scripts/maintenance_lint.py
python3 scripts/build_graph.py
python3 tools/build_viewer_data.py
```

### 5. Open the viewer

```bash
python3 -m http.server 8765
```

Then open:

```text
http://localhost:8765/tools/viewer.html
```

You should see the wiki page list, the selected Markdown page, and an agent panel showing the MCP-style tool flow.

## MCP Server

Run the MCP server directly:

```bash
python3 tools/wiki_mcp_server.py
```

Example client config:

```json
{
  "mcpServers": {
    "personal-llm-wiki": {
      "command": "python3",
      "args": ["tools/wiki_mcp_server.py"]
    }
  }
}
```

## MCP Tool List

| Tool | What it does |
|---|---|
| `wiki.list_pages` | Lists Markdown pages under `wiki/` |
| `wiki.get_page` | Reads one Markdown wiki page |
| `wiki.search` | Searches wiki pages and raw text snapshots |
| `wiki.query` | Routes a user question to relevant evidence pages |
| `wiki.maintenance_report` | Returns the latest maintenance report |
| `wiki.graph` | Returns the Mermaid wiki graph |

## How The Pieces Work Together

1. `raw/sources/text/` stores source snapshots that can be inspected by humans and agents.
2. `scripts/ingest_sources.py` creates one source page per raw text file under `wiki/sources/`.
3. `wiki/index.md` becomes the entry point for users and agents.
4. `tools/wiki_mcp_server.py` exposes the wiki through MCP-style JSON-RPC tools.
5. `tools/viewer.html` reads `tools/wiki-data.json` and renders the wiki in a browser.
6. `skills/wiki-maintainer/SKILL.md` tells an agent how to query and maintain the wiki safely.

## Updating With Your Own Material

Use this request pattern with an agent:

```text
I added raw/sources/text/my-note.md.
Please ingest it into the wiki, run maintenance, rebuild the graph, rebuild viewer data, and summarize what changed.
```

The expected commands are:

```bash
python3 scripts/ingest_sources.py
python3 scripts/maintenance_lint.py
python3 scripts/build_graph.py
python3 tools/build_viewer_data.py
```

## Verification

Run these checks before publishing or submitting:

```bash
python3 scripts/query_wiki.py "harness skill"
python3 scripts/maintenance_lint.py
python3 scripts/build_graph.py
python3 tools/build_viewer_data.py
python3 tools/demo_client.py
```

Expected results:

- query command prints relevant wiki pages and raw text snapshots.
- maintenance report shows missing frontmatter, broken links, and orphan pages counts.
- graph command writes `wiki/maintenance/wiki-graph.md`.
- viewer data command writes `tools/wiki-data.json`.
- demo client lists 6 tools and calls `wiki.query`.

## Demo

The `demo/` folder contains one screenshot of this product rendering a real wiki:

```text
demo/wiki-mvp.png
```

## Repository Package Checklist

- Harness: `AGENTS.md`, `RULES.md`, `schema/page-schema.md`, `skills/wiki-maintainer/SKILL.md`
- LLM Wiki: `raw/`, `wiki/`, `schema/`
- Visualization Tool: `tools/wiki_mcp_server.py`, `tools/viewer.html`, `tools/build_viewer_data.py`
- README: this file
- Demo: `demo/wiki-mvp.png`

