# Paid ads budget pacing — 2026-03-23

## Scope

- **Calendar month:** 2026-03-01 → 2026-03-31
- **As-of date:** 2026-03-23
- **Currency:** USD
- **Time math:** 23 day(s) elapsed in month, 8 day(s) remaining in month after as-of.
- **Live data:** API pull (Meta + Google)
- **Playbook file (only source of monthly targets):** `docs/paid_ads_assets/campaign_playbook_monthly.csv`

## Original targets (playbook)

The **portfolio total** below is **only** the sum of `monthly_budget` in that CSV (**15** row(s) → **$60,000.00**). It is **not** read from slides, GTM docs, or a separate $60k figure.

> **If you expect March = $60,000** but see a lower number here, the playbook file is incomplete or amounts are wrong. Add every campaign row (with `ca-us_…`-style `campaign_id`s) and adjust `monthly_budget` until the file sums to $60,000.

### By channel (rollup)

| Channel | Planned monthly budget (playbook) |
|---------|-------------------------------------|
| META | $31,500.00 |
| GOOGLE | $28,500.00 |
| **Portfolio** | **$60,000.00** |

### By campaign (every playbook row)

**Matching:** `campaign_id` is matched to the live campaign name **case-insensitively** first; if missing, **canonical geo aliases** are used (e.g. playbook `uk-au_pms_*` ↔ platform `au-uk_pms_*`). Optional column `platform_campaign_name` in the snapshot CSV copies the UI name when it differs.

| Playbook `campaign_id` | Playbook `campaign_name` | Channel | `monthly_budget` |
|-------------------------|---------------------------|---------|-------------------|
| ca-us_pms_prospecting_website-conv | CA+US PMS Prospecting (LAL A/B) | meta | $14,000.00 |
| ca-us_pms_retargeting_website-conv | CA+US PMS Retargeting (30d visitors) | meta | $5,300.00 |
| uk-au_pms_prospecting_website-conv | UK+AU PMS Prospecting | meta | $5,500.00 |
| uk-au_pms_retargeting_website-conv | UK+AU PMS Retargeting (30d visitors) | meta | $2,000.00 |
| ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | meta | $2,000.00 |
| br_pms_prospecting_website-conv | Brazil PMS Prospecting | meta | $1,500.00 |
| mx_pms_prospecting_website-conv | Mexico PMS Prospecting | meta | $1,200.00 |
| ca-us_brand_search | CA+US Brand Search | google | $5,000.00 |
| ca-us_pms_pmax | CA+US PMS Performance Max | google | $11,000.00 |
| uk-au_brand_search | UK+AU Brand Search | google | $2,000.00 |
| uk-au_pms_pmax | UK+AU PMS Performance Max | google | $6,000.00 |
| mx_pms_search_website-conv | Mexico PMS Search | google | $3,000.00 |
| br_brand_search | Brazil Brand Search | google | $500.00 |
| fr_brand_search | France Brand Search | google | $500.00 |
| fr_pms_search | France PMS Search | google | $500.00 |

### Effective monthly target (after redistribution)

Playbook **effective** amounts include non-live dollars reallocated to live campaigns in-channel.

| Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook | Redistribution | Effective | Live |
|-------------------------|---------------------------|------------------------------|---------|----------|----------------|-----------|------|
| ca-us_pms_prospecting_website-conv | CA+US PMS Prospecting (LAL A/B) | ca-us_pms_prospecting_website-conv | meta | $14,000.00 | $2,455.22 | $16,455.22 | yes |
| ca-us_pms_retargeting_website-conv | CA+US PMS Retargeting (30d visitors) | ca-us_pms_retargeting_website-conv | meta | $5,300.00 | $929.48 | $6,229.48 | yes |
| uk-au_pms_prospecting_website-conv | UK+AU PMS Prospecting | au-uk_pms_prospecting_website-conv | meta | $5,500.00 | $964.55 | $6,464.55 | yes |
| uk-au_pms_retargeting_website-conv | UK+AU PMS Retargeting (30d visitors) | au-uk_pms_retargeting_website-conv | meta | $2,000.00 | $350.75 | $2,350.75 | yes |
| ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | $2,000.00 | $0.00 | $0.00 | no |
| br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | $1,500.00 | $0.00 | $0.00 | no |
| mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | $1,200.00 | $0.00 | $0.00 | no |
| ca-us_brand_search | CA+US Brand Search | ca-us_brand_search | google | $5,000.00 | $937.50 | $5,937.50 | yes |
| ca-us_pms_pmax | CA+US PMS Performance Max | ca-us_pms_pmax | google | $11,000.00 | $2,062.50 | $13,062.50 | yes |
| uk-au_brand_search | UK+AU Brand Search | au-uk_brand_search | google | $2,000.00 | $375.00 | $2,375.00 | yes |
| uk-au_pms_pmax | UK+AU PMS Performance Max | au-uk_pms_pmax | google | $6,000.00 | $1,125.00 | $7,125.00 | yes |
| mx_pms_search_website-conv | Mexico PMS Search | — | google | $3,000.00 | $0.00 | $0.00 | no |
| br_brand_search | Brazil Brand Search | — | google | $500.00 | $0.00 | $0.00 | no |
| fr_brand_search | France Brand Search | — | google | $500.00 | $0.00 | $0.00 | no |
| fr_pms_search | France PMS Search | — | google | $500.00 | $0.00 | $0.00 | no |

## Redistribution (non-live playbook)

Non-live campaigns do not spend in-platform. Their **playbook** monthly amounts are **pooled per channel** and added to **live** rows **in proportion to each live campaign’s playbook share**.

| Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook $ (not spending) |
|-------------------------|---------------------------|------------------------------|---------|-----------------------------|
| ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | $2,000.00 |
| br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | $1,500.00 |
| mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | $1,200.00 |
| mx_pms_search_website-conv | Mexico PMS Search | — | google | $3,000.00 |
| br_brand_search | Brazil Brand Search | — | google | $500.00 |
| fr_brand_search | France Brand Search | — | google | $500.00 |
| fr_pms_search | France PMS Search | — | google | $500.00 |


## Current state (pacing) — by channel

**Channel totals:** **Spend MTD** and **Σ daily budgets** include **every campaign** in the live pull for that platform (not only playbook rows). Monthly targets and per-campaign rows remain playbook-only. Forecast uses **spend MTD + Σ(daily budget) × days remaining** after as-of. **Pacing delta** = channel effective monthly target − forecast (positive = underspend vs target).

### Meta

- **Effective monthly target (live):** $31,500.00
- **Spend MTD (all campaigns in channel):** $25,973.47
- **Sum of current daily budgets (all campaigns in channel):** $1,917.66
- **Forecast month-end spend:** $41,314.75
- **Pacing delta:** $-9,814.75 (positive = underspend)
- **Daily pacing pool (Σ daily budget deltas target):** $-1,226.84
- **Required daily run rate to hit plan:** $690.82

### Google

- **Effective monthly target (live):** $28,500.00
- **Spend MTD (all campaigns in channel):** $19,824.78
- **Sum of current daily budgets (all campaigns in channel):** $2,764.44
- **Forecast month-end spend:** $41,940.30
- **Pacing delta:** $-13,440.30 (positive = underspend)
- **Daily pacing pool (Σ daily budget deltas target):** $-1,680.04
- **Required daily run rate to hit plan:** $1,084.40

### Portfolio (Meta + Google)

- **Total effective monthly target:** $60,000.00
- **Total spend MTD:** $45,798.25
- **Total forecast month-end:** $83,255.05
- **Total pacing delta (monthly − forecast):** $-23,255.05
- **Total current daily budgets (all campaigns in pull):** $4,682.10
- **Total recommended daily budgets (sum, after caps):** $2,975.00
- **Portfolio required daily run rate (to hit plan):** $1,775.22

## Recommendations (per campaign)

Apply **recommended daily budget** in each ad platform. **Delta** = recommended − current. Notes explain pool direction (underspend vs overspend) and performance weighting.

| playbook_campaign_id | playbook_campaign_name | platform_campaign_name | channel | is_live | monthly_budget_playbook | monthly_budget_effective | current_daily_budget | spend_mtd | forecast_month_spend | pacing_delta_campaign | recommended_daily_budget_capped | daily_budget_delta | performance_bucket | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ca-us_pms_prospecting_website-conv | CA+US PMS Prospecting (LAL A/B) | ca-us_pms_prospecting_website-conv | meta | yes | $14,000.00 | $16,455.22 | $1,200.00 | $14,169.07 | $23,769.07 | $-7,313.85 | $840.00 | $-360.00 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.10). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| ca-us_pms_retargeting_website-conv | CA+US PMS Retargeting (30d visitors) | ca-us_pms_retargeting_website-conv | meta | yes | $5,300.00 | $6,229.48 | $80.00 | $1,321.22 | $1,961.22 | $4,268.26 | $56.00 | $-24.00 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.24). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| uk-au_pms_prospecting_website-conv | UK+AU PMS Prospecting | au-uk_pms_prospecting_website-conv | meta | yes | $5,500.00 | $6,464.55 | $450.00 | $4,897.42 | $8,497.42 | $-2,032.87 | $315.00 | $-135.00 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.10). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| uk-au_pms_retargeting_website-conv | UK+AU PMS Retargeting (30d visitors) | au-uk_pms_retargeting_website-conv | meta | yes | $2,000.00 | $2,350.75 | $40.00 | $601.13 | $921.13 | $1,429.62 | $28.00 | $-12.00 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.27). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| ca-us_brand_search | CA+US Brand Search | ca-us_brand_search | google | yes | $5,000.00 | $5,937.50 | $427.27 | $3,154.03 | $6,572.19 | $-634.69 | $427.27 | $0.00 | good | Channel overspend vs monthly plan; no decrease on this campaign (outside low-performer pool for this run). |
| ca-us_pms_pmax | CA+US PMS Performance Max | ca-us_pms_pmax | google | yes | $11,000.00 | $13,062.50 | $1,300.00 | $5,736.34 | $16,136.34 | $-3,073.84 | $910.00 | $-390.00 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.15). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| uk-au_brand_search | UK+AU Brand Search | au-uk_brand_search | google | yes | $2,000.00 | $2,375.00 | $90.91 | $958.87 | $1,686.15 | $688.85 | $67.83 | $-23.08 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.78). Weaker CPL vs target takes a larger share of the reduction. |
| uk-au_pms_pmax | UK+AU PMS Performance Max | au-uk_pms_pmax | google | yes | $6,000.00 | $7,125.00 | $472.72 | $2,018.02 | $5,799.78 | $1,325.22 | $330.90 | $-141.82 | poor | Overspend vs plan; share of daily cut by inverse performance (bucket=poor, score=0.12). Weaker CPL vs target takes a larger share of the reduction. Guardrail: change capped by max_daily_change_pct. |
| ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | no | $2,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-2,000.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | no | $1,500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-1,500.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | no | $1,200.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-1,200.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| mx_pms_search_website-conv | Mexico PMS Search | — | google | no | $3,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-3,000.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| br_brand_search | Brazil Brand Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| fr_brand_search | France Brand Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| fr_pms_search | France PMS Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |

## Checks & warnings

- Non-live playbook $ (reallocated to live in-channel): google=$4,500, meta=$4,700

## Output files (this run)

| File | Purpose |
|------|---------|
| `docs/analytics_reports/budget_pacing_analysis_2026-03-23.md` | Analysis summary (Markdown) |
| `docs/paid_ads_assets/campaign_playbook_monthly.csv` | Campaign playbook (input) |
| `docs/analytics_reports/daily_budget_tracker_2026-03-23.csv` | Combined campaign table (CSV) |
| `docs/analytics_reports/proposed_budget_changes_2026-03-23.csv` | Material budget changes only (CSV) |
| `docs/analytics_reports/paid_ads_budget_pacing_2026-03-23.xlsx` | Pacing workbook (Excel) |
| `docs/analytics_reports/live_portfolio_pull_2026-03-23.csv` | Raw live portfolio pull (CSV) |
| `docs/analytics_reports/campaign_snapshot_from_live_2026-03-23.csv` | Snapshot matched to playbook (CSV) |

---
*Generated by `paid-ads_budget_tracker` (`analysis_report.py`).*