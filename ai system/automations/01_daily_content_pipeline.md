---
name: Daily Content Pipeline Orchestrator
schedule: Daily at 08:00
tools: shell commands + Python scripts
---

# Daily Content Pipeline Orchestrator

You are the daily content pipeline orchestrator for Hostfully. Your job is to scan competitor blogs, score new content ideas, enrich them with SEO data, and push a daily summary to Google Sheets.

The workspace root is at the path shown when you run `pwd`. All scripts reference paths relative to this root.

## Phase 0 Guardrailed Entrypoint

Run this automation through the guardrailed wrapper first (preflight + idempotency + run ledger):

```bash
python3 "ai system/automations/entrypoints/run_01.py" --dry-run
```

To execute any command in this runbook with Phase 0 protections, route it through the wrapper:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/preflight_automations.py" --automation 1 --strict
```

Use `--allow-duplicate-run` only when you intentionally need a rerun in the same logical period.

## Step 1: Install dependencies (first run only)

```bash
pip install -r ai system/automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Run the Competitor Blog Scraper

```bash
python3 "ai system/python scripts/competitor scrapers/competitor-blog-scraper.py"
```

This scrapes blogs from Morning Brew, The Hustle, Stratechery, Lenny's Newsletter, Benedict Evans, Bytes.dev, Beehiiv, and Paved. It updates `docs/competitor content tracker/blogs/competitor_content_tracker.csv`.

If the scraper fails, log the error and continue to Step 3 with existing data.

## Step 3: Run the Pipeline Agent

```bash
cd "ai system/python scripts/content pipeline agent/planning" && python3 pipeline_agent.py && cd -
```

This reads `competitor_content_tracker.csv` and generates scored content concepts in `docs/competitor content tracker/blogs/content_pipeline.csv`.

## Step 4: Enrich Top Pipeline Items with Ahrefs Keyword Data

Read the `content_pipeline.csv` file. For each row with status "Not Started" (up to 10 items), extract the core topic keyword from the Title column.

For each keyword, run:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/ahrefs_api.py" keywords-overview --country us --keywords "KEYWORD_HERE"
```

And for related terms:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/ahrefs_api.py" keywords-matching --country us --keywords "KEYWORD_HERE"
```

Compile the keyword data (search volume, difficulty, CPC, related terms) for each pipeline item.

## Step 5: Generate Daily Summary

Create a summary of today's pipeline activity:
- Number of new competitor articles scraped
- Number of new pipeline concepts generated
- Top 5 pipeline items by weighted score, enriched with Ahrefs keyword data
- Any high-volume/low-difficulty keyword opportunities spotted

## Step 6: Push Summary to Google Sheets

Check if the tracking sheet exists:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/gsheets_api.py" list
```

If "Content Pipeline Daily Log" doesn't appear in the results, create it:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/gsheets_api.py" create --title "Content Pipeline Daily Log"
```

Then append today's summary row:

```bash
python3 "ai system/automations/entrypoints/run_01.py" -- python3 "ai system/automations/lib/gsheets_api.py" update --title "Content Pipeline Daily Log" --range "Sheet1" --values '[["DATE","new_articles","new_concepts","top_keyword","top_volume","top_difficulty","backlog_count"]]'
```

Replace the placeholder values with the actual data from Steps 2-4.

## Error Handling

- If the blog scraper fails, continue with the pipeline agent using existing data
- If Ahrefs API calls fail, skip enrichment and note "Ahrefs unavailable" in the summary
- If Google Sheets API fails, save the summary as a markdown file at `docs/analytics_reports/daily_pipeline_summary_YYYY-MM-DD.md`
- Always complete the run even if individual steps fail
