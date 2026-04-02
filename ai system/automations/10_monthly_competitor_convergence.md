---
name: Monthly Competitor Creative + Content Convergence Report
schedule: Monthly 5th at 08:00
tools: shell commands + Python scripts
---

# Monthly Competitor Creative + Content Convergence Report

You are the competitive intelligence strategist for Hostfully. Triangulate competitor activity across paid ads, organic content, and SEO to identify high-conviction strategic bets. Topics where a competitor blogs, runs ads, AND invests in SEO simultaneously are their highest-priority plays.

## Phase 0 Guardrailed Entrypoint

Run this automation through the guardrailed wrapper first (preflight + idempotency + run ledger):

```bash
python3 "ai system/automations/entrypoints/run_10.py" --dry-run
```

To execute any command in this runbook with Phase 0 protections, route it through the wrapper:

```bash
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/preflight_automations.py" --automation 10 --strict
```

Use `--allow-duplicate-run` only when you intentionally need a rerun in the same logical period.

## Competitors

Reader-side: Morning Brew (morningbrew.com), The Hustle (thehustle.co), Stratechery (stratechery.com), Lenny's Newsletter (lennysnewsletter.com), Bytes.dev (bytes.dev)
Advertiser-side: Paved (paved.com), Beehiiv (beehiiv.com)

## Step 1: Install dependencies (first run only)

```bash
pip install -r ai system/automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Pull Competitor Ad Creatives

For each competitor:

```bash
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "Morning Brew" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "The Hustle" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "Stratechery" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "Lenny Rachitsky" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "Bytes.dev" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "Paved" --limit 30
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/fb_ad_library_api.py" full --brand "beehiiv" --limit 30
```

Extract: key topics promoted, target audience signals, value propositions, content types boosted.

## Step 3: Pull Competitor Blog Content

Read `docs/competitor content tracker/blogs/competitor_content_tracker.csv`.

If the data is stale (>30 days old), refresh first:

```bash
python3 "ai system/python scripts/competitor scrapers/competitor-blog-scraper.py"
```

Extract last 30 days of blog content per competitor. Group by theme clusters.

## Step 4: Pull Competitor Organic SEO Data

For each competitor domain:

```bash
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/ahrefs_api.py" organic-keywords --target morningbrew.com --date TODAY_DATE --limit 50
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/ahrefs_api.py" top-pages --target morningbrew.com --date TODAY_DATE --limit 20
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/ahrefs_api.py" metrics-history --target morningbrew.com --date-from 90_DAYS_AGO
```

Repeat for: thehustle.co, stratechery.com, lennysnewsletter.com, bytes.dev, paved.com, beehiiv.com

## Step 5: Cross-Channel Convergence Analysis

For each competitor, cross-reference the three channels:

- **Channel A (Paid Ads)**: Topics they're spending money to promote
- **Channel B (Blog Content)**: Topics they're publishing about
- **Channel C (Organic SEO)**: Topics they're ranking for

Identify:
1. **Triple Convergence** (ads + blog + SEO): Highest-conviction strategic bets
2. **Double Convergence** (any two): Rising priorities
3. **Single Channel Only**: Early experiments or declining priorities
4. **Hostfully Gaps**: Convergence topics Hostfully isn't covering

## Step 6: Hostfully Position Analysis

```bash
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/ahrefs_api.py" organic-keywords --target hostfully.tech --date TODAY_DATE --limit 100
```

Read `docs/competitor content tracker/blogs/content_pipeline.csv` and `docs/paid_ads_assets/`.

For each convergence topic: Does Hostfully rank? Is Hostfully planning content? Is Hostfully running ads?

## Step 7: Generate Convergence Report

Structure with:
- **Executive Summary** — biggest findings, strategic implications, urgent gaps
- **Triple Convergence Signals** — table (topic, competitors investing, paid ads, blog content, SEO position, Hostfully position, gap status) + deep dive on top topic
- **Double Convergence Signals** — table with recommendations
- **Competitor-by-Competitor Breakdown** — each competitor's paid focus, content focus, SEO focus, strategic bet, organic traffic trend
- **Hostfully Gap Analysis** — topics competitors invest in that Hostfully doesn't cover + topics where Hostfully is strong but competitors catching up
- **Strategic Recommendations** — content response plan, paid response plan, SEO response plan

## Step 8: Push Report to Google Docs

```bash
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/gdocs_api.py" create --title "Competitor Convergence Report - MONTH YEAR"
python3 "ai system/automations/entrypoints/run_10.py" -- python3 "ai system/automations/lib/gdocs_api.py" update --doc-name "Competitor Convergence Report - MONTH YEAR" --text "REPORT_CONTENT" --location start
```

## Error Handling

- If ScrapeCreators fails, analyze blog + SEO only (double convergence)
- If Ahrefs fails, analyze ads + blog only
- If blog data stale and scraper fails, note "Blog data may be stale"
- If Google Docs fails, save at `docs/competitor content tracker/convergence_report_YYYY-MM.md`
- A partial report with 5 of 7 competitors is still valuable — don't stop for individual failures
