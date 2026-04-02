# Paid ads budget pacing — 2026-03-24

## Scope

- **Calendar month:** 2026-03-01 → 2026-03-31
- **As-of date:** 2026-03-24
- **Currency:** USD
- **Time math:** 24 day(s) elapsed in month, 7 day(s) remaining in month after as-of.
- **Live data:** API pull (Meta + Google)
- **Playbook file (only source of monthly targets):** `docs/paid_ads_assets/campaign_playbook_monthly.csv`

## Model legend

- Required total daily budget delta (channel): pacing_delta / remaining_days.
- Performance score (in-platform): 45% cost structure (target CPL vs actual CPL) + 20% engagement (CTR) + 20% conversion performance (CVR) + 15% conversion volume (leads).
- ROI weighting: roi_priority_weight = pipeline_amount + 2 × closed_won_amount from the provided opportunities sheet.
- Allocation rule (ROI-dominant): combined weight = 85% ROI + 15% in-platform performance; overspend channels cut by inverse(combined weight), underspend channels increase by combined weight.
- Guardrails: recommended daily budget is clipped to never be below 0.

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

| Source | Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook | Redistribution | Effective | Live |
|--------|-------------------------|---------------------------|------------------------------|---------|----------|----------------|-----------|------|
| playbook | ca-us_pms_prospecting_website-conv | CA+US PMS Prospecting (LAL A/B) | ca-us_pms_prospecting_website-conv | meta | $14,000.00 | $2,453.61 | $16,453.61 | yes |
| playbook | ca-us_pms_retargeting_website-conv | CA+US PMS Retargeting (30d visitors) | ca-us_pms_retargeting_website-conv | meta | $5,300.00 | $928.87 | $6,228.87 | yes |
| playbook | uk-au_pms_prospecting_website-conv | UK+AU PMS Prospecting | au-uk_pms_prospecting_website-conv | meta | $5,500.00 | $963.92 | $6,463.92 | yes |
| playbook | uk-au_pms_retargeting_website-conv | UK+AU PMS Retargeting (30d visitors) | au-uk_pms_retargeting_website-conv | meta | $2,000.00 | $350.52 | $2,350.52 | yes |
| playbook | ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | $2,000.00 | $0.00 | $0.00 | no |
| playbook | br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | $1,500.00 | $0.00 | $0.00 | no |
| playbook | mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | $1,200.00 | $0.00 | $0.00 | no |
| playbook | ca-us_brand_search | CA+US Brand Search | ca-us_brand_search | google | $5,000.00 | $3,906.25 | $8,906.25 | yes |
| playbook | ca-us_pms_pmax | CA+US PMS Performance Max | ca-us_pms_pmax | google | $11,000.00 | $8,593.75 | $19,593.75 | yes |
| playbook | uk-au_brand_search | UK+AU Brand Search | — | google | $2,000.00 | $0.00 | $0.00 | no |
| playbook | uk-au_pms_pmax | UK+AU PMS Performance Max | — | google | $6,000.00 | $0.00 | $0.00 | no |
| playbook | mx_pms_search_website-conv | Mexico PMS Search | — | google | $3,000.00 | $0.00 | $0.00 | no |
| playbook | br_brand_search | Brazil Brand Search | — | google | $500.00 | $0.00 | $0.00 | no |
| playbook | fr_brand_search | France Brand Search | — | google | $500.00 | $0.00 | $0.00 | no |
| playbook | fr_pms_search | France PMS Search | — | google | $500.00 | $0.00 | $0.00 | no |
| non-playbook | [Post Promovido] \| pt-br | [Post Promovido] \| pt-br | [Post Promovido] \| pt-br | meta | $0.00 | $0.00 | $0.00 | yes |
| non-playbook | [Leads] \| hostfully \| pt-br — meeting | [Leads] \| hostfully \| pt-br — meeting | [Leads] \| hostfully \| pt-br — meeting | meta | $0.00 | $3.10 | $3.10 | yes |

## Redistribution (non-live playbook)

Non-live campaigns do not spend in-platform. Their **playbook** monthly amounts are **pooled per channel** and added to **live** rows **in proportion to each live campaign’s playbook share**.

| Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook $ (not spending) |
|-------------------------|---------------------------|------------------------------|---------|-----------------------------|
| ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | $2,000.00 |
| br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | $1,500.00 |
| mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | $1,200.00 |
| uk-au_brand_search | UK+AU Brand Search | — | google | $2,000.00 |
| uk-au_pms_pmax | UK+AU PMS Performance Max | — | google | $6,000.00 |
| mx_pms_search_website-conv | Mexico PMS Search | — | google | $3,000.00 |
| br_brand_search | Brazil Brand Search | — | google | $500.00 |
| fr_brand_search | France Brand Search | — | google | $500.00 |
| fr_pms_search | France PMS Search | — | google | $500.00 |


## Current state (pacing) — by channel

**Channel totals:** **Spend MTD** and **Σ daily budgets** include **every campaign** in the live pull for that platform (not only playbook rows). Monthly targets and per-campaign rows remain playbook-only. Forecast uses **spend MTD + Σ(daily budget) × days remaining** after as-of. **Pacing delta** = channel effective monthly target − forecast (positive = underspend vs target).

### Meta

- **Effective monthly target (live):** $31,500.00
- **Spend MTD (all campaigns in channel):** $28,327.16
- **Sum of current daily budgets (all campaigns in channel):** $627.66
- **Forecast month-end spend:** $32,720.78
- **Pacing delta:** $-1,220.78 (positive = underspend)
- **Daily pacing pool (required Σ daily budget deltas):** $-174.40
- **Required daily run rate to hit plan:** $453.26

### Google

- **Effective monthly target (live):** $28,500.00
- **Spend MTD (all campaigns in channel):** $23,334.90
- **Sum of current daily budgets (all campaigns in channel):** $650.00
- **Forecast month-end spend:** $27,884.90
- **Pacing delta:** $615.10 (positive = underspend)
- **Daily pacing pool (required Σ daily budget deltas):** $87.87
- **Required daily run rate to hit plan:** $737.87

### Portfolio (Meta + Google)

- **Total effective monthly target:** $60,000.00
- **Total spend MTD:** $51,662.06
- **Total forecast month-end:** $60,605.68
- **Total pacing delta (monthly − forecast):** $-605.68
- **Total current daily budgets (all campaigns in pull):** $1,277.66
- **Total recommended daily budgets (sum, after caps):** $1,191.13
- **Portfolio required daily run rate (to hit plan):** $1,191.13

## Recommendations (per campaign)

Apply **recommended daily budget** in each ad platform. **Delta** = recommended − current. Notes explain pool direction (underspend vs overspend) and performance weighting.

| source | playbook_campaign_id | playbook_campaign_name | platform_campaign_name | channel | is_live | monthly_budget_playbook | monthly_budget_effective | current_daily_budget | spend_mtd | forecast_month_spend | pacing_delta_campaign | recommended_daily_budget_capped | daily_budget_delta | pct_budget_change | allocation_share_pct | ctr_mtd | cvr_mtd | cpl_mtd | pipeline_amount | closed_won_amount | sql_count | roi_priority_weight | performance_bucket | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| playbook | ca-us_pms_prospecting_website-conv | CA+US PMS Prospecting (LAL A/B) | ca-us_pms_prospecting_website-conv | meta | yes | $14,000.00 | $16,453.61 | $500.00 | $15,648.05 | $19,148.05 | $-2,694.44 | $448.26 | $-51.74 | -10.35% | 1.39% | 0.01% | 0.01% | $474.18 | $27,060.00 | $0.00 | 10.00 | $27,060.00 | poor | Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=1.04 (poor), pipeline=$27,060, closed_won=$0, roi_weight=27,060. Campaign share=1.4% of pool $-174.40 -> daily change $-2.42. Channel forecast $32,720.78 vs target $31,500.00. |
| playbook | ca-us_pms_retargeting_website-conv | CA+US PMS Retargeting (30d visitors) | ca-us_pms_retargeting_website-conv | meta | yes | $5,300.00 | $6,228.87 | $50.00 | $1,419.63 | $1,769.63 | $4,459.24 | $0.00 | $-50.00 | -100.00% | 15.63% | 0.01% | 0.03% | $177.45 | $1,548.00 | $1,548.00 | 1.00 | $4,644.00 | poor | Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=1.19 (poor), pipeline=$1,548, closed_won=$1,548, roi_weight=4,644. Campaign share=15.6% of pool $-174.40 -> daily change $-27.25. Channel forecast $32,720.78 vs target $31,500.00. Guardrail: change capped by max_daily_change_pct. |
| playbook | uk-au_pms_prospecting_website-conv | UK+AU PMS Prospecting | au-uk_pms_prospecting_website-conv | meta | yes | $5,500.00 | $6,463.92 | $40.00 | $5,543.75 | $5,823.75 | $640.17 | $0.00 | $-40.00 | -100.00% | 20.52% | 0.01% | 0.00% | $1,847.92 | $3,498.00 | $540.00 | 3.00 | $4,578.00 | poor | Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=0.47 (poor), pipeline=$3,498, closed_won=$540, roi_weight=4,578. Campaign share=20.5% of pool $-174.40 -> daily change $-35.79. Channel forecast $32,720.78 vs target $31,500.00. Guardrail: change capped by max_daily_change_pct. |
| playbook | uk-au_pms_retargeting_website-conv | UK+AU PMS Retargeting (30d visitors) | au-uk_pms_retargeting_website-conv | meta | yes | $2,000.00 | $2,350.52 | $20.00 | $667.35 | $807.35 | $1,543.17 | $0.00 | $-20.00 | -100.00% | 24.05% | 0.02% | 0.02% | $222.45 | $1,260.00 | $1,260.00 | 1.00 | $3,780.00 | poor | Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=0.92 (poor), pipeline=$1,260, closed_won=$1,260, roi_weight=3,780. Campaign share=24.0% of pool $-174.40 -> daily change $-41.94. Channel forecast $32,720.78 vs target $31,500.00. Guardrail: change capped by max_daily_change_pct. |
| non-playbook | [Post Promovido] \| pt-br | [Post Promovido] \| pt-br | [Post Promovido] \| pt-br | meta | yes | $0.00 | $0.00 | $0.00 | $153.20 | $153.20 | $-153.20 | $5.00 | $5.00 | 0.00% | 0.00% | 0.00% | 0.00% | — | $0.00 | $0.00 | 0.00 | $0.00 | unknown | Channel overspend but this campaign held flat: outside low-performer cut set (or protected by relative ROI/performance) for this run. Guardrail: change capped by max_daily_change_pct. |
| non-playbook | [Leads] \| hostfully \| pt-br — meeting | [Leads] \| hostfully \| pt-br — meeting | [Leads] \| hostfully \| pt-br — meeting | meta | yes | $0.00 | $3.10 | $17.66 | $1,241.68 | $1,365.30 | $-1,362.20 | $0.00 | $-17.66 | -100.00% | 38.42% | 0.01% | 0.00% | $413.89 | $2,895.20 | $0.00 | 2.00 | $2,895.20 | unknown | Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=0.83 (unknown), pipeline=$2,895, closed_won=$0, roi_weight=2,895. Campaign share=38.4% of pool $-174.40 -> daily change $-67.01. Channel forecast $32,720.78 vs target $31,500.00. Guardrail: change capped by max_daily_change_pct. |
| playbook | ca-us_brand_search | CA+US Brand Search | ca-us_brand_search | google | yes | $5,000.00 | $8,906.25 | $250.00 | $3,736.19 | $5,486.19 | $3,420.06 | $337.87 | $87.87 | 35.15% | 100.00% | 0.21% | 0.03% | $145.09 | $0.00 | $0.00 | 0.00 | $0.00 | average | Underspend logic: channel gap allocated by ROI-dominant weighting (85% ROI, 15% in-platform performance). Inputs: perf=1.39 (average), pipeline=$0, closed_won=$0, roi_weight=0. Campaign share=100.0% of pool $87.87 -> daily change $87.87. Channel forecast $27,884.90 vs target $28,500.00. Guardrail: change capped by max_daily_change_pct. |
| playbook | ca-us_pms_pmax | CA+US PMS Performance Max | ca-us_pms_pmax | google | yes | $11,000.00 | $19,593.75 | $400.00 | $7,427.41 | $10,227.41 | $9,366.34 | $400.00 | $0.00 | 0.00% | 0.00% | 0.04% | 0.00% | $928.43 | $35,226.80 | $1,522.80 | 10.00 | $38,272.40 | poor | Channel underspend but this campaign received no increase: outside high-performer set (or insufficient ROI/performance vs peers) for this run. |
| playbook | ca-us_spring-promo_prospecting_website-conv | CA+US Spring Cleaning Promo Prospecting | — | meta | no | $2,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-2,000.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | br_pms_prospecting_website-conv | Brazil PMS Prospecting | — | meta | no | $1,500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-1,500.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | mx_pms_prospecting_website-conv | Mexico PMS Prospecting | — | meta | no | $1,200.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-1,200.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | uk-au_brand_search | UK+AU Brand Search | — | google | no | $2,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-2,000.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | uk-au_pms_pmax | UK+AU PMS Performance Max | — | google | no | $6,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-6,000.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | mx_pms_search_website-conv | Mexico PMS Search | — | google | no | $3,000.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-3,000.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | br_brand_search | Brazil Brand Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | fr_brand_search | France Brand Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |
| playbook | fr_pms_search | France PMS Search | — | google | no | $500.00 | $0.00 | $0.00 | $0.00 | $0.00 | $-500.00 | $0.00 | $0.00 | 0.00% | 0.00% | — | — | — | $0.00 | $0.00 | 0.00 | $0.00 | n/a | Not live this month — playbook dollars for this campaign are redistributed to live campaigns in the same channel (proportional to playbook share). |

## Checks & warnings

- Non-live playbook $ (reallocated to live in-channel): google=$12,500, meta=$4,700

## Output files (this run)

| File | Purpose |
|------|---------|
| `docs/analytics_reports/budget pacing/2026-03-24/budget_pacing_analysis_2026-03-24.md` | Analysis summary (Markdown) |
| `docs/paid_ads_assets/campaign_playbook_monthly.csv` | Campaign playbook (input) |
| `docs/analytics_reports/budget pacing/2026-03-24/daily_budget_tracker_2026-03-24.csv` | Combined campaign table (CSV) |
| `docs/analytics_reports/budget pacing/2026-03-24/proposed_budget_changes_2026-03-24.csv` | Material budget changes only (CSV) |
| `docs/analytics_reports/budget pacing/2026-03-24/paid_ads_budget_pacing_2026-03-24.xlsx` | Pacing workbook (Excel) |
| `docs/analytics_reports/budget pacing/2026-03-24/live_portfolio_pull_2026-03-24.csv` | Raw live portfolio pull (CSV) |
| `docs/analytics_reports/budget pacing/2026-03-24/campaign_snapshot_from_live_2026-03-24.csv` | Snapshot matched to playbook (CSV) |

---
*Generated by `paid-ads_budget_tracker` (`analysis_report.py`).*