# Figma MCP Setup (TLDR Repo)

This directory contains the local setup and crawl artifacts for the hosted Figma MCP server.

## What was configured

- Cursor MCP config updated in `.cursor/mcp.json`:
  - Server name: `figma`
  - URL: `https://mcp.figma.com/mcp`

## Crawl and mirror docs

Run:

```bash
python3 "ai system/mcp/figma_mcp/scrape_figma_mcp.py"
```

This generates:

- `mirror/`: local mirror of in-scope pages/files
- `crawl-index.json`: per-URL crawl metadata
- `coverage-report.md`: high-level crawl coverage
- `figma-mcp-build-guide.md`: practical setup + usage guide
- `figma-mcp-crawl-spec.md`: crawler spec and rerun details

## Scope

The crawler starts from:

- `https://github.com/mcp/com.figma.mcp/mcp`
- `https://github.com/figma/mcp-server-guide`
- `https://developers.figma.com/docs/figma-mcp-server/`

and follows in-scope internal links for:

- `github.com/mcp/com.figma.mcp/mcp`
- `github.com/figma/mcp-server-guide`
- `raw.githubusercontent.com/figma/mcp-server-guide/*`
- `api.github.com/repos/figma/mcp-server-guide/*`
- `developers.figma.com/docs/figma-mcp-server/*`
