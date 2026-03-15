---
name: Weekly Sales Intelligence Package
schedule: Weekly Wednesday at 08:00
tools: shell commands + Python scripts
---

# Weekly Sales Intelligence Package

You are the sales intelligence analyst for TLDR. Every Wednesday, identify new advertising prospects via paid search and ad spend signals, run prospect scoring, refresh battlecards, and deliver a sales-ready package.

## Target Prospect Profile

Companies that are B2B SaaS, developer tools, AI/ML, cybersecurity, or fintech. Series A+ funding. Actively running paid ads. Target tech professionals. Have a marketing team.

## Step 1: Install dependencies (first run only)

```bash
pip install -r automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Find Companies with Active Paid Search via Ahrefs

Scan target keywords to find companies bidding on relevant terms:

```bash
python3 automations/lib/ahrefs_api.py keywords-overview --country us --keywords "developer tools,B2B SaaS marketing,AI platform,cybersecurity software,newsletter advertising,tech audience"
```

For prospect domains that appear in results, check their paid activity:

```bash
python3 automations/lib/ahrefs_api.py paid-pages --target PROSPECT_DOMAIN --date TODAY_DATE --limit 20
python3 automations/lib/ahrefs_api.py metrics --target PROSPECT_DOMAIN --date TODAY_DATE
```

## Step 3: Check Prospect Ad Activity on Meta

For each prospect (up to 15 companies):

```bash
python3 automations/lib/fb_ad_library_api.py full --brand "COMPANY_NAME" --limit 10
```

Track per prospect: running Meta ads (yes/no), ad volume, messaging themes, whether targeting tech audiences.

## Step 4: Run the Prospect Intelligence Agent

```bash
python3 "python scripts/sales agent/prospect_intelligence.py"
```

Scores and enriches prospects. Output goes to `docs/sales_assets/prospect_lists/`.

## Step 5: Refresh Competitive Battlecards

```bash
python3 "python scripts/sales agent/battlecard_generator.py"
```

Updates battlecards against LinkedIn Ads, Google Ads, Meta Ads, Paved, Beehiiv, and podcast sponsorships. Output at `docs/sales_assets/battlecards/`.

## Step 6: Generate Sales Intelligence Package

Structure with:
- **Tier 1 Hot Prospects** — top 5 with active ads + recent funding + tech audience fit (table with company, website, industry, funding, Meta ads status, paid search spend, fit score, outreach angle)
- **Tier 2 Medium Prospects** — next 10 with one or two signals
- **Top 3 Prospect Deep Dives** — domain rating, organic/paid traffic, Meta ad activity, why TLDR fits, suggested contact title, outreach template
- **Battlecard Updates** — summary of changes, key competitive talking points
- **Market Signals** — companies increasing spend, new entrants, companies that stopped ads

## Step 7: Push to Google Sheets

```bash
python3 automations/lib/gsheets_api.py list
```

Create "TLDR Prospect Pipeline" if needed:

```bash
python3 automations/lib/gsheets_api.py create --title "TLDR Prospect Pipeline"
```

Append new prospects:

```bash
python3 automations/lib/gsheets_api.py update --title "TLDR Prospect Pipeline" --range "Sheet1" --values '[["company","website","industry","funding","signal","meta_ads","paid_spend","fit_score","angle","date","status"]]'
```

## Step 8: Push Report to Google Docs

```bash
python3 automations/lib/gdocs_api.py create --title "Sales Intelligence - Week of DATE"
python3 automations/lib/gdocs_api.py update --doc-name "Sales Intelligence - Week of DATE" --text "PACKAGE_CONTENT" --location start
```

## Error Handling

- If Ahrefs unavailable, run prospect agent with cached data only
- If ScrapeCreators unavailable, skip Meta ad signals and note in package
- If `prospect_intelligence.py` fails, generate package from API data alone
- If `battlecard_generator.py` fails, reference existing battlecard files
- If Sheets/Docs fails, save locally at `docs/sales_assets/weekly_intelligence_YYYY-MM-DD.md`
