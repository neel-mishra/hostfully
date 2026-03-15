---
name: Weekly Ad Performance Dashboard
schedule: Weekly Monday at 07:00
tools: shell commands + Python scripts
---

# Weekly Ad Performance Dashboard

You are the paid media analyst for TLDR. Every Monday before standup, pull performance from Meta and Google Ads, compare week-over-week, flag anomalies, and generate a narrative report with a running Google Sheet tracker.

## Step 1: Install dependencies (first run only)

```bash
pip install -r automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Pull Meta Ads Performance (Last 7 Days)

```bash
python3 automations/lib/meta_ads_api.py account-summary --date-preset last_7d
python3 automations/lib/meta_ads_api.py campaigns --date-preset last_7d
python3 automations/lib/meta_ads_api.py results-summary --date-preset last_7d
```

Use the **results-summary** output for Meta Results. It matches Ads Manager: **explicit date range**, **campaigns with delivery only**, and **one result per campaign** (the primary conversion for that campaign: qualified_meeting_booked, lead_email-valid, etc.). Use **one_row_total** (or **total_results**) as the single total for the report. Default is lead results only (excludes Post engagements).

Optional — Include Post engagements in the sum, or restrict to certain campaigns:

```bash
python3 automations/lib/meta_ads_api.py results-summary --date-preset last_7d --include-post-engagement
python3 automations/lib/meta_ads_api.py results-summary --date-preset last_7d --lead-campaigns-only
python3 automations/lib/meta_ads_api.py results-summary --date-preset last_7d --had-delivery-only
```

For each active campaign returned, get detailed performance:

```bash
python3 automations/lib/meta_ads_api.py campaign-performance --id CAMPAIGN_ID --date-preset last_7d
```

For top 3 campaigns by spend, get ad set detail:

```bash
python3 automations/lib/meta_ads_api.py ad-sets --campaign-id CAMPAIGN_ID --date-preset last_7d
```

## Step 3: Pull Google Ads Performance (Last 7 Days)

```bash
python3 automations/lib/google_ads_api.py account-summary --date-range LAST_7_DAYS
python3 automations/lib/google_ads_api.py campaigns --date-range LAST_7_DAYS
```

For top campaigns, get keyword data:

```bash
python3 automations/lib/google_ads_api.py keywords --campaign-id CAMPAIGN_ID --date-range LAST_7_DAYS
```

## Step 4: Pull Previous Week for Comparison

```bash
python3 automations/lib/meta_ads_api.py account-summary --date-preset last_14d
python3 automations/lib/google_ads_api.py account-summary --date-range LAST_14_DAYS
```

Subtract last_7d from last_14d to derive the prior week. Calculate WoW deltas for all metrics.

## Step 5: Anomaly Detection

Flag any of the following:
- CPC increased >20% WoW
- CTR dropped >15% WoW
- Spend >10% over or under weekly pace
- Any campaign with 0 conversions that had conversions last week
- Any campaign CPC 2x+ above account average

## Step 6: Generate Narrative Report

Create a structured report with:
- **Headlines** — 1-3 most important things this week
- **Cross-Platform Summary** — table with Meta, Google, Combined, and WoW Change columns. For Meta, include the **Results** line from `results-summary` (default = lead results only, excl. Post engagements). Use `--include-post-engagement` only if you need all result types in the report.
- **Anomalies & Flags** — any issues detected
- **Meta Ads Detail** — campaign table + notable audiences + Results (from results-summary)
- **Google Ads Detail** — campaign table + top 10 keywords by conversions
- **Recommendations** — 2-3 actionable next steps

## Step 7: Push to Google Sheets

```bash
python3 automations/lib/gsheets_api.py list
```

If "TLDR Ad Performance Tracker" doesn't exist:

```bash
python3 automations/lib/gsheets_api.py create --title "TLDR Ad Performance Tracker"
```

Append this week's row:

```bash
python3 automations/lib/gsheets_api.py update --title "TLDR Ad Performance Tracker" --range "Sheet1" --values '[["WEEK_DATE","meta_spend","meta_imp","meta_clicks","meta_ctr","meta_cpc","meta_conv","google_spend","google_imp","google_clicks","google_ctr","google_cpc","google_conv","total_spend","total_conv","blended_cpc","blended_cpa"]]'
```

## Step 8: Push Narrative to Google Docs

```bash
python3 automations/lib/gdocs_api.py create --title "TLDR Ad Performance - Week of DATE"
python3 automations/lib/gdocs_api.py update --doc-name "TLDR Ad Performance - Week of DATE" --text "REPORT_CONTENT" --location start
```

## Error Handling

- If Meta Ads API unavailable, report with Google Ads only and note gap
- If Google Ads API unavailable, report with Meta only and note gap
- If both unavailable, create placeholder doc noting the outage
- If Sheets/Docs API fails, save locally at `docs/analytics_reports/weekly_ad_performance_YYYY-MM-DD.md`
