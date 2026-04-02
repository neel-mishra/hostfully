# Cursor Automations

Each `.md` file contains the full prompt for a Cursor Automation. The `lib/` directory contains Python API wrapper scripts that replace MCP tool calls with direct API calls, so automations work in the cloud without needing remote MCP server infrastructure.

## First-Time Setup

### 1. Install Python dependencies

```bash
cd ai system/automations/lib && pip install -r requirements.txt
```

### 2. Set environment variables

The utility scripts need API credentials. Two options:

**Option A (Cloud Automations):** Click "Manage" next to "Use Configured Environment" in each automation and add the required env vars. See `lib/ENV_SETUP.md` for the full list.

**Option B (Local .env):** Add the credentials to the workspace `.env` file. The scripts load from `.env` via `python-dotenv`. Copy values from `~/.cursor/mcp.json` — see `lib/ENV_SETUP.md` for which vars map to which MCP server.

### 3. Create each automation

For each automation:
1. Go to [cursor.com/automations](https://cursor.com/automations) > **New Agent**
2. Set the **name** from the frontmatter
3. Click **+ Add Trigger** > Schedule > set the time from the frontmatter
4. Copy everything below the `---` frontmatter into the **Instructions** box
5. Leave model as **Codex 5.3 High**
6. No MCP tools needed — the scripts call APIs directly via shell commands
7. Toggle **Use Configured Environment** on
8. Click **Enable**

## Automation Index

| # | File | Schedule | Replaces |
|---|------|----------|----------|
| 1 | `01_daily_content_pipeline.md` | Daily 08:00 | `com.hostfully.contentpipeline.plist` |
| 2 | `02_weekly_content_execution.md` | Weekly Mon 09:00 | `com.hostfully.contentpipeline.weekly.plist` |
| 3 | `03_monthly_competitive_ads.md` | Monthly 28th | `com.hostfully.tech.competitivetracker.monthly.plist` |
| 4 | `04_weekly_ad_performance.md` | Weekly Mon 07:00 | -- |
| 5 | `05_weekly_seo_intelligence.md` | Weekly Tue 08:00 | -- |
| 6 | `06_biweekly_advertiser_health.md` | Bi-weekly Mon 10:00 | -- |
| 7 | `07_weekly_sales_intelligence.md` | Weekly Wed 08:00 | -- |
| 8 | `08_weekly_cro_audit.md` | Weekly Thu 09:00 | -- |
| 9 | `09_monthly_gtm_commander.md` | Monthly 1st | -- |
| 10 | `10_monthly_competitor_convergence.md` | Monthly 5th | -- |

## Utility Scripts (`lib/`)

| Script | Replaces MCP | Used By |
|--------|-------------|---------|
| `ahrefs_api.py` | `user-ahrefs` | 1, 5, 7, 8, 9, 10 |
| `gsheets_api.py` | `user-gsheets` | 1, 4, 6, 7 |
| `gdocs_api.py` | `user-google_docs` | 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| `meta_ads_api.py` | `user-meta_ads_portfolio` | 3, 4, 6, 9 |
| `google_ads_api.py` | `user-google_ads_portfolio` | 3, 4, 6, 9 |
| `fb_ad_library_api.py` | `user-fb_ad_library` | 3, 7, 10 |

## Decommissioning LaunchAgent Plists

After automations 1-3 run reliably, remove the old plists:

```bash
launchctl unload ~/Library/LaunchAgents/com.hostfully.contentpipeline.plist
launchctl unload ~/Library/LaunchAgents/com.hostfully.contentpipeline.weekly.plist
launchctl unload ~/Library/LaunchAgents/com.hostfully.tech.competitivetracker.monthly.plist
```

## Future: Remote MCP Setup

When you're ready to set up remote MCP connections (cleaner long-term approach):
1. Deploy each MCP server as an HTTP/SSE endpoint (e.g., on a VPS or cloud function)
2. In the Automations UI, click "+ Add Tool or MCP" > "MCP Server" > "+ New Connection"
3. Point each connection to the hosted server URL
4. Revert the automation instructions to use MCP tool references instead of shell commands
