# Paid ads — campaign playbook

## Files

| File | Role |
|------|------|
| **`campaign_playbook_monthly.csv`** | **Agent input:** one row per **campaign** in Meta or Google. `campaign_id` must match the **exact campaign name** in the ad platform (e.g. `ca-us_pms_prospecting_website-conv`). `monthly_budget` sums to the full monthly plan (March 2026: **$60,000**). |
| **`Hostfully_Campaign_Playbook_March2026_Campaign_Structure_and_Budget.csv`** | **Source workbook** exported from planning (campaign + ad set / ad group detail). Ad set / ad group budgets are **rolled up** to the campaign row in `campaign_playbook_monthly.csv` where one campaign spans multiple rows in the sheet. |

## March 2026 rollup (Hostfully)

- **Meta ($31,500):** `ca-us_pms_prospecting_website-conv` = $7,000 + $7,000 (two ad sets); other campaigns are one row each in the source.
- **Google ($28,500):** `ca-us_brand_search` = $4,000 + $1,000; `uk-au_brand_search` = $1,500 + $500; remaining campaigns one line each.

Totals: **$31,500 + $28,500 = $60,000**.

## Snapshot

Live pacing uses `docs/analytics_reports/campaign_snapshot_latest.csv` (or API). Update that file (or run live pull) so every `campaign_id` in the playbook appears with current daily budget and MTD spend.

**Naming aliases:** The budget tracker matches **`uk-au_*`** playbook IDs to Meta **`au-uk_*`** (and similar) campaign names automatically; exact match is tried first.
