---
type: maintenance
status: stable
created: 2026-06-14
updated: 2026-06-14
sources:
  - ../../AGENTS.md
related:
  - latest-maintenance-report.md
---

# Wiki Graph

```mermaid
flowchart LR
  concepts_wiki_harness["concepts/wiki-harness"]
  index["index"]
  log["log"]
  maintenance_latest_maintenance_report["maintenance/latest-maintenance-report"]
  maintenance_wiki_graph["maintenance/wiki-graph"]
  queries_example_query["queries/example-query"]
  sources_sample_agent_workflow["sources/sample-agent-workflow"]
  workflows_source_to_wiki["workflows/source-to-wiki"]
  index --> concepts_wiki_harness
  index --> workflows_source_to_wiki
  index --> queries_example_query
  index --> sources_sample_agent_workflow
  index --> maintenance_latest_maintenance_report
  index --> maintenance_wiki_graph
  index --> log
```
