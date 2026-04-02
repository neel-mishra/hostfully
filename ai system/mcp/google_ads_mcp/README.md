# Google Ads MCP

Project-local Google Ads MCP server for Cursor, built from the `cohnen/mcp-google-ads` pattern and extended for:

- Campaign, ad group, ad, landing page, and device analysis
- Search term and keyword analysis
- Auction insights-compatible reporting
- Asset inventory and asset performance analysis
- Keyword Planner access
- Generic GAQL reporting and field discovery

## Files

- `google_ads_server.py`: MCP server entrypoint
- `requirements.txt`: Python dependencies
- `.env.example`: environment variable template
- `tests/`: quick local validation scripts

## Setup

1. Create a virtual environment:

```bash
cd "/Users/neelmishra/antigravity/synthetic growth/Hostfully/ai system/python scripts/google_ads_mcp"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your Google Ads credentials.

3. Make sure the service account or OAuth setup has Google Ads API access and a valid developer token.

4. Cursor should load the repo-local `.cursor/mcp.json` entry for `google_ads_mcp`.

## Auth modes

- `service_account`: default in this repo; expects `GOOGLE_ADS_CREDENTIALS_PATH`
- `oauth`: supported if you provide either an OAuth client JSON at `GOOGLE_ADS_CREDENTIALS_PATH` or `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET`

## Tool families

- Discovery: `healthcheck`, `list_accounts`, `list_resources`, `list_fields`, `build_report_query`
- Reporting: `run_gaql`, `execute_gaql_query`, `get_campaign_performance`, `get_ad_performance`
- Search + keywords: `get_search_term_performance`, `get_campaign_search_terms`, `get_keyword_performance`, `get_search_term_to_keyword_mapping`, `get_auction_insights`
- Assets: `get_asset_inventory`, `get_asset_usage_map`, `get_rsa_asset_performance`, `get_rsa_combination_performance`, `get_sitelink_performance`, `get_lead_form_asset_performance`, `get_lead_form_submissions`
- Planning: `generate_keyword_ideas`, `generate_keyword_historical_metrics`, `generate_ad_group_themes`, `generate_keyword_forecast_metrics`, `list_keyword_plans`

## Notes

- Cost fields are returned in micros.
- The Google Ads API does not expose every single report or insight visible in the Google Ads web UI.
- Keyword Planner endpoints are more heavily rate-limited than standard reporting endpoints.
