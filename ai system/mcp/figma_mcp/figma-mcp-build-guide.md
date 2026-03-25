# Figma MCP Build Guide

## What is set up in this repo
- Cursor MCP server config includes `figma` pointing to `https://mcp.figma.com/mcp`.
- Crawl artifacts for Figma MCP docs are stored in `ai system/mcp/figma_mcp/mirror/`.
- Crawl metadata and link coverage are in `crawl-index.json` and `coverage-report.md`.

## Cursor setup (already configured)
1. Open Cursor settings MCP panel to verify server `figma` is enabled.
2. Ensure you are authenticated when prompted by Cursor.
3. In agent chat, run `#get_design_context` to confirm tool visibility.

## VS Code manual setup
Use `MCP:Add Server` with:
- Type: `HTTP`
- URL: `https://mcp.figma.com/mcp`
- Server ID: `figma`

## Claude Code manual setup
Run:
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

## Common Figma MCP flow
1. Run `get_design_context` for selected frame/layer URL.
2. Run `get_screenshot` for fidelity checks.
3. Run `get_variable_defs` to map tokens and styles.
4. Use Code Connect tools (`get_code_connect_map`, suggestions/mappings) for component reuse.

## Rate-limit notes
- Starter / View / Collab seats may be limited to a small monthly call quota.
- Dev/Full seats on paid plans generally use per-minute API-style limits.
