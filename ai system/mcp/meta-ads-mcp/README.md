# Meta Ads MCP (local stdio)

This is a local stdio **Model Context Protocol** server for the **Meta Marketing API** (Facebook/Instagram Ads).

## Setup

1) Install deps

```bash
cd "meta-ads-mcp"
npm install
```

2) Create `.env.local`

```bash
cp .env.example .env.local
```

3) Run in dev

```bash
npm run dev
```

4) Build for Cursor

```bash
npm run build
node build/src/index.js
```

