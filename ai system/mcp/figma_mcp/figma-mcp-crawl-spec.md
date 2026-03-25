# Figma MCP Crawl Spec

## Objective
Continuously mirror public Figma MCP docs and related repo files to support offline reference and reproducible setup.

## Scope allowlist
- `github.com/mcp/com.figma.mcp/mcp`
- `github.com/figma/mcp-server-guide`
- `raw.githubusercontent.com/figma/mcp-server-guide/*`
- `api.github.com/repos/figma/mcp-server-guide/*`
- `developers.figma.com/docs/figma-mcp-server/*`

## Crawler behavior
- URL canonicalization, deduplication, and depth-bounded traversal.
- HTML/JSON/Markdown link extraction.
- Per-URL mirrored content under `mirror/<host>/<path>`.
- Coverage index with status, hash, type, discovered links, and errors.

## Re-run
```bash
python3 "ai system/mcp/figma_mcp/scrape_figma_mcp.py"
```
