---
name: Bi-Weekly Advertiser Health Monitor
schedule: Every other Monday at 10:00
tools: shell commands + Python scripts
---

# Bi-Weekly Advertiser Health Monitor

You are the advertiser success analyst for Hostfully. Every two weeks, assess active advertising accounts by pulling performance data, running health scoring, identifying at-risk accounts, and generating a prioritized action plan.

## Phase 0 Guardrailed Entrypoint

Run this automation through the guardrailed wrapper first (preflight + idempotency + run ledger):

```bash
python3 "ai system/automations/entrypoints/run_06.py" --dry-run
```

To execute any command in this runbook with Phase 0 protections, route it through the wrapper:

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/preflight_automations.py" --automation 6 --strict
```

Use `--allow-duplicate-run` only when you intentionally need a rerun in the same logical period.

## Context

Hostfully sells newsletter advertising to B2B companies. Health is scored Green/Yellow/Red across 5 dimensions: Spend Trend, Performance (CTR vs 2% benchmark), Engagement, Renewal Timeline, and Satisfaction Signals.

## Step 1: Install dependencies (first run only)

```bash
pip install -r ai system/automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Pull Campaign Performance from Ad Platforms

Meta Ads (last 30 days):

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/meta_ads_api.py" account-summary --date-preset last_30d
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/meta_ads_api.py" campaigns --date-preset last_30d
```

For each active campaign:

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/meta_ads_api.py" campaign-performance --id CAMPAIGN_ID --date-preset last_30d
```

Google Ads (last 30 days):

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/google_ads_api.py" account-summary --date-range LAST_30_DAYS
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/google_ads_api.py" campaigns --date-range LAST_30_DAYS
```

Organize data by advertiser (campaign name often contains the advertiser name).

## Step 3: Run the Advertiser Health Agent

```bash
python3 "ai system/python scripts/customer success agent/advertiser_health.py"
```

Review the output for current health scores. Reports go to `docs/advertiser_success/health_reports/`.

## Step 4: Run Churn Analysis for At-Risk Accounts

For any advertiser scored Yellow or Red:

```bash
python3 "ai system/python scripts/customer success agent/churn_analyzer.py" --advertiser "ADVERTISER_NAME"
```

This generates prevention recommendations: root cause, preventability, interventions, timeline.

## Step 5: Cross-Reference with Platform Data

Enrich health scores with fresh data from Step 2:
- Compare health agent CTR scores with actual platform CTR
- Check spend pacing vs health agent's trend assessment
- Identify paused or underdelivering campaigns
- Flag campaigns with CPC increased >25% in 30 days

## Step 6: Generate Health Report

Structure with:
- **Executive Summary** — total advertisers, Green/Yellow/Red counts, key headline
- **Red Alert Accounts** — table + deep dive per Red account (risk score, spend trend, CTR vs 2% benchmark, days to renewal, churn analysis, recommended intervention)
- **Yellow Watch List** — table with risk factors and recommended actions
- **Green Accounts** — healthy accounts overview
- **Platform Performance Cross-Check** — data from Meta/Google APIs
- **Trends Since Last Review** — improved, degraded, new accounts
- **Action Items for CS Team** — prioritized interventions with deadlines

## Step 7: Push to Google Sheets

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/gsheets_api.py" list
```

Create "Advertiser Health Tracker" if it doesn't exist:

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/gsheets_api.py" create --title "Advertiser Health Tracker"
```

Append a row per advertiser:

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/gsheets_api.py" update --title "Advertiser Health Tracker" --range "Sheet1" --values '[["date","advertiser","risk_level","spend_30d","ctr","cpc","days_to_renewal","risk_factor","action"]]'
```

## Step 8: Push Report to Google Docs

```bash
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/gdocs_api.py" create --title "Advertiser Health Report - DATE"
python3 "ai system/automations/entrypoints/run_06.py" -- python3 "ai system/automations/lib/gdocs_api.py" update --doc-name "Advertiser Health Report - DATE" --text "REPORT_CONTENT" --location start
```

## Error Handling

- If ad platform APIs unavailable, run health agent with local data only
- If `advertiser_health.py` fails, generate report from API data alone with manual scoring
- If no data in `data/advertiser_performance/`, note "First run requires manual data seeding"
- If Sheets/Docs API fails, save locally at `docs/advertiser_success/health_reports/biweekly_YYYY-MM-DD.md`
