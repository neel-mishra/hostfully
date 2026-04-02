# Environment Variables for Automations

The utility scripts need these environment variables. Set them in **two places**:

1. **Cloud Agent Environment** -- Click "Manage" next to "Use Configured Environment" in each automation
2. **Local `.env`** -- For testing scripts locally before deploying to automations

## Required Variables

Copy these values from your `~/.cursor/mcp.json` into the Cloud Agent Environment settings.

### Ahrefs (automations 1, 5, 7, 8, 9, 10)
```
AHREFS_API_KEY=<from mcp.json env or .env>
```

### Google Sheets (automations 1, 4, 6, 7)
```
GSHEETS_CLIENT_EMAIL=<from mcp.json "gsheets" > "env" > "GSHEETS_CLIENT_EMAIL">
GSHEETS_PRIVATE_KEY=<from mcp.json "gsheets" > "env" > "GSHEETS_PRIVATE_KEY">
DRIVE_FOLDER_ID_SHEETS=<from mcp.json "gsheets" > "env" > "DRIVE_FOLDER_ID_SHEETS">
```

### Google Docs (automations 2, 3, 4, 5, 6, 7, 8, 9, 10)
```
GOOGLE_CLIENT_ID=<from mcp.json "google_docs" > "env" > "GOOGLE_CLIENT_ID">
GOOGLE_CLIENT_SECRET=<from mcp.json "google_docs" > "env" > "GOOGLE_CLIENT_SECRET">
GOOGLE_REFRESH_TOKEN=<from mcp.json "google_docs" > "env" > "GOOGLE_REFRESH_TOKEN">
DRIVE_FOLDER_ID_DOCS=<from mcp.json "google_docs" > "env" > "DRIVE_FOLDER_ID_DOCS">
```

### Meta Ads Portfolio (automations 3, 4, 6, 9)
```
META_ACCESS_TOKEN=<from mcp.json "meta_ads_portfolio" > "env" > "META_ACCESS_TOKEN">
META_AD_ACCOUNT_ID=<from mcp.json "meta_ads_portfolio" > "env" > "META_AD_ACCOUNT_ID">
```

### Google Ads Portfolio (automations 3, 4, 6, 9)
```
GOOGLE_ADS_CLIENT_ID=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_CLIENT_ID">
GOOGLE_ADS_CLIENT_SECRET=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_CLIENT_SECRET">
GOOGLE_ADS_DEVELOPER_TOKEN=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_DEVELOPER_TOKEN">
GOOGLE_ADS_REFRESH_TOKEN=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_REFRESH_TOKEN">
GOOGLE_ADS_CUSTOMER_ID=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_CUSTOMER_ID">
GOOGLE_ADS_MANAGER_ID=<from mcp.json "google_ads_portfolio" > "env" > "GOOGLE_ADS_MANAGER_ID">
```

### Meta Ad Library / ScrapeCreators (automations 3, 7, 10)
```
SCRAPECREATORS_API_KEY=<from .env or mcp.json>
```

### Google Search Console (automations 5, 8; scripts: search_ranking_agent, seo_auditor, gsc_api.py)
Set these to use live GSC data. If unset, automations and scripts use mock data or sitemap-only fallbacks. See `docs/GSC_GA4_SETUP.md` for setup.
```
GSC_SITE_URL=https://hostfully.tech
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

### LLM APIs (used by existing Python agent scripts)
```
ANTHROPIC_API_KEY=<your Anthropic API key>
GEMINI_API_KEY=<your Gemini API key>
OPENROUTER_API_KEY=<your OpenRouter API key>
```

## Phase 0 Preflight (recommended)

Run centralized dependency checks before scheduled runs:

```bash
python3 "ai system/automations/lib/preflight_automations.py"
```

Strict mode (fails if any required env/path is missing):

```bash
python3 "ai system/automations/lib/preflight_automations.py" --strict
```

## Phase 0 Automation Entrypoints

Use wrapper entry scripts to enforce preflight + idempotency + run ledger before running automation steps.

Examples:

```bash
python3 "ai system/automations/entrypoints/run_01.py" --dry-run
python3 "ai system/automations/entrypoints/run_04.py" -- python3 "ai system/automations/lib/meta_ads_api.py" account-summary --date-preset last_7d
python3 "ai system/automations/entrypoints/run_09.py" --allow-duplicate-run --dry-run
```

Notes:
- Default behavior is idempotent by logical period.
- Use `--allow-duplicate-run` for intentional reruns in the same period.
- If you pass a command, put it after `--`.
