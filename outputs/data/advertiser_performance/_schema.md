# Advertiser Performance Data

This folder stores advertiser campaign performance data extracted from native ad platforms. Data is used by:
- **Advertiser Health & Renewal Risk Agent** — flags churn risk
- **Advertiser QBR Generator** — builds quarterly business reviews
- **Sales Call Transcript Analyzer** — correlates call insights with performance

---

## Data Source

Performance data is pulled from TLDR's internal ad management systems. A future MCP integration will automate extraction from each native platform.

### MCP Integration Placeholder

When the MCP is built, it should:
1. Connect to TLDR's ad serving / campaign management platform
2. Extract per-advertiser performance metrics on a weekly cadence
3. Write CSV files to this folder following the schema below
4. Optionally push to Google Sheets via the `user-gsheets` MCP

---

## File Schema

### `campaign_performance_{YYYY-MM}.csv`

One row per advertiser per campaign per newsletter placement.

| Column | Type | Description |
|---|---|---|
| advertiser_id | string | Unique advertiser identifier |
| advertiser_name | string | Company name |
| campaign_id | string | Campaign identifier |
| campaign_name | string | Campaign name/description |
| newsletter | string | Which TLDR newsletter (Tech, AI, Dev, InfoSec, etc.) |
| placement_type | string | Primary, Secondary, or Quick Link |
| placement_date | date | Date of newsletter send (YYYY-MM-DD) |
| impressions | int | Newsletter opens (= impressions for the ad) |
| clicks | int | Click-throughs on the ad |
| ctr | float | Click-through rate (clicks / impressions) |
| spend | float | Amount charged to advertiser (USD) |
| cpc | float | Cost per click (spend / clicks) |
| conversions | int | Attributed conversions (if tracked) |
| cpl | float | Cost per lead (if tracked) |

### `advertiser_health_{YYYY-MM}.csv`

One row per advertiser. Aggregated monthly snapshot.

| Column | Type | Description |
|---|---|---|
| advertiser_id | string | Unique advertiser identifier |
| advertiser_name | string | Company name |
| contract_start | date | When they first advertised |
| contract_renewal | date | Next renewal date |
| total_spend_ltv | float | Lifetime spend (USD) |
| spend_this_quarter | float | Current quarter spend |
| spend_last_quarter | float | Previous quarter spend |
| spend_trend | string | increasing / stable / declining |
| campaigns_active | int | Currently active campaigns |
| avg_ctr | float | Average CTR across all placements |
| avg_cpc | float | Average CPC across all placements |
| last_placement_date | date | Most recent newsletter placement |
| last_contact_date | date | Last sales/CS touchpoint |
| nps_score | int | Net Promoter Score (if collected) |
| newsletters_used | string | Comma-separated list of newsletters |
| notes | string | Free-text notes |

---

## Sample Data

Sample CSVs are included for testing:

- **advertiser_health_2026-03.csv** — 3 sample advertisers (Acme Corp, Beta Labs, Gamma Inc)
- **campaign_performance_2026-03.csv** — matching campaign/placement rows

Run the Advertiser Health agent:

```bash
python3 "ai system/python scripts/customer success agent/advertiser_health.py"
```

Output is written to `docs/advertiser_success/health_reports/`. Replace the sample CSVs with real data (or connect the MCP) for production.
