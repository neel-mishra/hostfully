# Paid ads budget pacing (Meta + Google)

Single utility in this folder: reads **playbook** + **live snapshot** (daily budget + MTD spend + leads), computes **forecast** \(S + \sum b_i \cdot d_{rem}\), then **redistributes daily budget** on underspend (top performers) or overspend (weak performers) **within each channel**.

## Inputs (repo root–relative)

| File | Purpose |
|------|---------|
| `docs/paid_ads_assets/campaign_playbook_monthly.csv` | `campaign_id`, `campaign_name`, `platform`, `monthly_budget`, `priority_tier`, `target_kpi_value`, dates — **must match platform campaign names** (e.g. Hostfully `ca-us_pms_prospecting_website-conv`). See `docs/paid_ads_assets/README.md` and the archived source workbook `Hostfully_Campaign_Playbook_March2026_Campaign_Structure_and_Budget.csv`. |
| `docs/analytics_reports/campaign_snapshot_latest.csv` | `campaign_id`, `current_daily_budget`, `spend_mtd`, `leads_mtd`, optional **`is_live`** (`true`/`false`), optional **`platform_campaign_name`** (exact name in Meta/Google UI; defaults to `campaign_id`). Campaigns **in the playbook but not in this file** are treated as **not live**. |

## Live vs not-live campaigns

- The playbook is **left-joined** to the snapshot. Any playbook campaign **missing** from the snapshot is **not live** (no spend in-platform).
- If **`is_live`** is present and `false`, the row is not live even when present in the snapshot (paused / not launched).
- **Non-live** monthly playbook dollars are **pooled per channel (Meta / Google)** and **redistributed to live campaigns** in that channel, **in proportion to each live campaign’s original playbook share** (so the channel’s total planned spend still matches the sum of playbook rows).
- Pacing and daily-budget recommendations run on **live** rows only; **non-live** rows are appended to the CSV with a short note that their budget was reallocated.
| `data/config/campaign_mapping.csv` | Optional validation; required for older MCP-normalized flows |

Override snapshot path: `CAMPAIGN_SNAPSHOT_PATH=/path/to.csv`.

## Live portfolio pull (Meta + Google APIs)

By default each run **pulls live** campaign budgets and MTD spend/leads via the same stack as
[`paid_ads_intelligence_agent.py`](../paid%20ads%20intelligence%20agent/paid_ads_intelligence_agent.py)
(Graph API + Google Ads GAQL). That matches what **`google_ads_mcp`** and Meta tooling use for credentials,
without spawning MCP stdio from this script.

**Requirements:** Credentials in **`miscellaneous/.env`** (or repo root `.env`; `miscellaneous/.env` wins if both exist). Typical keys:

- Meta: `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`
- Google: `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_DEVELOPER_TOKEN`, OAuth / refresh token fields (see intelligence agent)

**Matching:** playbook `campaign_id` must match the **campaign name** in Meta / Google **case-insensitively**. If there is still no row, the tracker tries a **canonical geo key** so pairs like **`uk-au_*` ↔ `au-uk_*`** (and `uk+au` / `au+uk` variants) resolve to the same campaign (`campaign_name_match.py`).

**Meta MTD spend (accuracy):** Campaign insights are **aggregated across all insight rows and all pages** (Meta often returns daily rows and/or paginated responses). Using only the first row undercounts vs Ads Manager. Archived campaigns that spent in-period are included in the campaign list (`ACTIVE`, `PAUSED`, `ARCHIVED`). A live run prints **account-level MTD** vs **sum of campaign rows** for a quick reconcile.

**Channel spend vs playbook:** In **live** runs, **Spend MTD** and **Σ daily budgets** in the channel summary and portfolio roll-up use **all campaigns** returned in the API pull for that platform (including spend from campaigns **not** in the playbook). Meta **spend** prefers **account-level insights** when available; playbook-matched rows still drive monthly targets and per-campaign recommendations.

**Google Ads (403):** The intelligence agent retries GAQL with **no `login-customer-id`**, **search vs searchStream**, and each **`listAccessibleCustomers`** id as `login-customer-id`. If you still see 403: confirm the OAuth user has access to `GOOGLE_ADS_CUSTOMER_ID`; for **MCC-managed** clients set **`GOOGLE_ADS_MANAGER_ID`** to the manager account (or clear it for direct-linked accounts); ensure the **developer token** is approved for the account (not test-only on wrong account).

**Monthly totals:** The tracker sums **`monthly_budget` in the playbook CSV only**. If your March plan is **$60,000** but the file sums to less, add rows or fix amounts until the CSV matches your plan (there is no separate override).

**Outputs (extra):**

- `live_portfolio_pull_<date>.csv` — raw API-aligned rows  
- `campaign_snapshot_from_live_<date>.csv` — one row per playbook campaign after matching  

**Disable live pull** (CSV only): `BUDGET_TRACKER_USE_LIVE=0` or `python3 main.py --no-live`.

## Run

```bash
cd "ai system/python scripts/paid-ads_budget_tracker"
python3 -m pip install -r requirements.txt
BUDGET_PACING_AS_OF=2026-03-17 python3 main.py
# CSV-only:
python3 main.py --no-live --as-of 2026-03-17
```

Outputs in `docs/analytics_reports/`:

- `paid_ads_budget_pacing_<date>.xlsx` — **primary**: portfolio KPI block, Meta table, Google table  
- `daily_budget_tracker_<date>.csv` — combined rows  
- `proposed_budget_changes_<date>.csv` — rows with material delta  
- `budget_pacing_analysis_<date>.md` — **narrative summary**: playbook targets, effective targets after redistribution, non-live reallocation, channel + portfolio pacing, per-campaign recommendations, checks/warnings, and an index of this run’s artifacts  

## Intelligence

`performance_scores.py` derives CPL vs `target_kpi_value`. Extend `intelligence_bridge.py` to merge `lead_analysis.json` from the paid ads intelligence agent when you want richer modifiers.
