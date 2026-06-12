# Sample Source: Agent Workflow Notes

An agent workflow works best when the system separates durable knowledge from temporary chat context.

The durable layer should keep source snapshots, compiled wiki pages, and maintenance reports. The agent should search the compiled wiki first because it is shorter and more structured than the raw source. If the compiled wiki is not enough, the agent can inspect the raw snapshot and then update the wiki.

A practical harness includes operating rules, a reusable skill, local scripts, and a tool interface. The tool interface lets an agent list pages, read pages, search evidence, route a user question, and inspect maintenance status.

The browser viewer is useful because a human can verify whether the wiki structure makes sense without reading every Markdown file manually.

