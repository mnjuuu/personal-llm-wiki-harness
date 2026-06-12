# Wiki Page Schema

Every page in `wiki/` should begin with frontmatter.

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

Recommended body:

```markdown
# Page Title

## Summary

## Key Points

## Details

## Source Notes

## Open Questions

## Maintenance Notes
```

