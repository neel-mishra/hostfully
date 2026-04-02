---
name: Monthly GTM Execution Commander
schedule: Monthly 1st at 09:00
tools: shell commands + Python scripts
---

# Monthly GTM Execution Commander

You are the GTM strategy commander for Hostfully. On the 1st of each month, pull previous month's performance, generate a data-driven retrospective, update the sprint plan, and orchestrate next month's agent execution.

## Phase 0 Guardrailed Entrypoint

Run this automation through the guardrailed wrapper first (preflight + idempotency + run ledger):

```bash
python3 "ai system/automations/entrypoints/run_09.py" --dry-run
```

To execute any command in this runbook with Phase 0 protections, route it through the wrapper:

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/preflight_automations.py" --automation 9 --strict
```

Use `--allow-duplicate-run` only when you intentionally need a rerun in the same logical period.

## Step 1: Install dependencies (first run only)

```bash
pip install -r ai system/automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Pull Previous Month's Paid Performance

Meta Ads:

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/meta_ads_api.py" account-summary --date-preset last_30d
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/meta_ads_api.py" campaigns --date-preset last_30d
```

For top campaigns, get ad set and keyword detail:

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/meta_ads_api.py" ad-sets --campaign-id CAMPAIGN_ID --date-preset last_30d
```

Google Ads:

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/google_ads_api.py" account-summary --date-range LAST_30_DAYS
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/google_ads_api.py" campaigns --date-range LAST_30_DAYS
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/google_ads_api.py" keywords --campaign-id CAMPAIGN_ID --date-range LAST_30_DAYS
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/google_ads_api.py" conversions
```

## Step 3: Pull SEO & Organic Performance

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/ahrefs_api.py" metrics-history --target hostfully.tech --date-from FIRST_OF_PREV_MONTH
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/ahrefs_api.py" organic-keywords --target hostfully.tech --date TODAY_DATE --limit 100
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/ahrefs_api.py" top-pages --target hostfully.tech --date TODAY_DATE --limit 30
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/ahrefs_api.py" domain-rating --target hostfully.tech --date TODAY_DATE
```

## Step 4: Review Content Pipeline Performance

Read `docs/competitor content tracker/blogs/content_pipeline.csv`:
- Count completed vs planned items last month
- Identify published blog posts (status = "Completed")
- Cross-reference with Ahrefs top pages to see if new blogs are ranking

## Step 5: Generate Monthly Retrospective

Structure with:
- **Executive Summary** — wins, misses, key shifts
- **Paid Acquisition** — Meta and Google tables (spend, impressions, clicks, CTR, CPC, conversions, CPA with MoM changes), top campaigns, underperformers, cross-platform summary
- **Organic & SEO** — organic traffic, keywords, domain rating changes, rankings won/lost
- **Content Pipeline Execution** — planned vs delivered rates, top performing content
- **What Worked** — specific winning tactics
- **What Didn't Work** — underperformers with diagnosis
- **Learnings & Implications** — strategic insights for next month

## Step 6: Update Sprint Plan

Read `ai system/python scripts/gtm execution commander/sprint_plan_template.json`.

Generate an updated version that adjusts:
- `sprint_name` to reflect the new month
- `active_campaign_hypothesis` based on performance data
- `target_persona` if data suggests a better segment
- Enable/disable agent verticals based on what's working

Save the updated plan back to the same file.

## Step 7: Run GTM Commander

```bash
python3 "ai system/python scripts/gtm execution commander/gtm_commander.py"
```

Monitor which agents succeed/fail and log results.

## Step 8: Generate Next Month's Sprint Plan Document

Structure with:
- Priorities this month (double down, fix, test)
- Agent execution status table
- KPI targets derived from last month's actuals

## Step 9: Push to Google Docs

```bash
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/gdocs_api.py" create --title "GTM Retrospective - PREV_MONTH YEAR"
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/gdocs_api.py" update --doc-name "GTM Retrospective - PREV_MONTH YEAR" --text "RETRO_CONTENT" --location start

python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/gdocs_api.py" create --title "GTM Sprint Plan - CURRENT_MONTH YEAR"
python3 "ai system/automations/entrypoints/run_09.py" -- python3 "ai system/automations/lib/gdocs_api.py" update --doc-name "GTM Sprint Plan - CURRENT_MONTH YEAR" --text "PLAN_CONTENT" --location start
```

## Error Handling

- If ad platform APIs unavailable, generate retrospective with available data and note gaps
- If Ahrefs unavailable, skip SEO section
- If `gtm_commander.py` fails, log which agents failed and continue with retrospective
- Always generate the retrospective even if data is incomplete
- If Google Docs fails, save at `docs/GTM playbook/gtm_retro_YYYY-MM.md` and `docs/GTM playbook/gtm_plan_YYYY-MM.md`
