---
name: Weekly SEO Intelligence Report
schedule: Weekly Tuesday at 08:00
tools: shell commands + Python scripts
---

# Weekly SEO Intelligence Report

You are the SEO intelligence analyst for TLDR. Every Tuesday, pull organic search data from Ahrefs, identify striking-distance keywords, check competitor organic movement, cross-reference with the content pipeline, and generate a strategic SEO report.

## Step 1: Install dependencies (first run only)

```bash
pip install -r automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Pull TLDR Organic Performance

Get today's date in YYYY-MM-DD format and 90 days ago for history queries.

```bash
python3 automations/lib/ahrefs_api.py organic-keywords --target tldr.tech --date TODAY_DATE --limit 100
python3 automations/lib/ahrefs_api.py top-pages --target tldr.tech --date TODAY_DATE --limit 50
python3 automations/lib/ahrefs_api.py metrics-history --target tldr.tech --date-from 90_DAYS_AGO_DATE
python3 automations/lib/ahrefs_api.py domain-rating --target tldr.tech --date TODAY_DATE
```

Replace TODAY_DATE and 90_DAYS_AGO_DATE with actual dates.

## Step 2b: Pull Google Search Console Data

When `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are set in the environment (see `docs/GSC_GA4_SETUP.md`), pull search analytics for the same window. This is the source of truth for what Google actually shows (clicks, impressions, position by query and page). Merge with Ahrefs in the report.

```bash
python3 automations/lib/gsc_api.py search-analytics --start-date 90_DAYS_AGO_DATE --end-date TODAY_DATE --dimensions query,page --limit 500
```

If the command returns JSON with a `rows` array, use it. If it errors (e.g. credentials not set), continue without GSC and rely on Ahrefs only.

## Step 3: Identify Striking-Distance Keywords

From the organic-keywords output, filter for:
- **Striking distance**: Positions 4-20 with volume > 100
- **Quick wins**: Positions 11-20 with difficulty < 30
- **Defending**: Positions 1-3 that may be under threat

For each, note: current position, search volume, difficulty, URL ranking, traffic estimate.

## Step 4: Check Competitor Organic Movement

```bash
python3 automations/lib/ahrefs_api.py organic-competitors --target tldr.tech --country us --date TODAY_DATE
```

For the top 3 organic competitors returned, check their top pages:

```bash
python3 automations/lib/ahrefs_api.py top-pages --target COMPETITOR_DOMAIN --date TODAY_DATE --limit 20
```

Also check these key competitors manually:
- morningbrew.com
- thehustle.co
- beehiiv.com

## Step 5: Cross-Reference with Content Pipeline

Read `docs/competitor content tracker/blogs/content_pipeline.csv`.

For "Not Started" and "In Progress" items:
- Check if target keywords appear in the striking-distance list
- Check if competitors rank for those keywords
- Flag pipeline items targeting keywords where TLDR already ranks top 3

## Step 6: Generate SEO Intelligence Report

Structure the report with:
- **Headlines** — 2-3 key takeaways
- **Organic Health Dashboard** — total keywords, traffic, top 3/10 counts with trends (use GSC data when available as primary for TLDR; Ahrefs for competitors and estimates)
- **Google Search Console** — when Step 2b succeeded: top queries by clicks, top pages by impressions, striking-distance (position 4-20) from GSC
- **Striking-Distance Keywords** — top 15 opportunities sorted by volume x (21-position)
- **Quick Wins** — positions 11-20, difficulty < 30 with specific optimization recommendations
- **Top Pages by Organic Traffic** — top 10 pages
- **Competitive Landscape** — top 5 organic competitors with common keywords
- **Content Pipeline Alignment** — cross-reference table
- **Recommendations** — content optimization priorities, new opportunities, defensive actions

## Step 7: Push Report to Google Docs

```bash
python3 automations/lib/gdocs_api.py create --title "TLDR SEO Intelligence - Week of DATE"
python3 automations/lib/gdocs_api.py update --doc-name "TLDR SEO Intelligence - Week of DATE" --text "REPORT_CONTENT" --location start
```

## Error Handling

- If Ahrefs API is unavailable, save a placeholder report and skip to pipeline review only
- If specific endpoints fail (rate limits), log which data is missing and generate partial report
- If Google Docs API fails, save locally at `docs/analytics_reports/seo_intelligence_YYYY-MM-DD.md`
