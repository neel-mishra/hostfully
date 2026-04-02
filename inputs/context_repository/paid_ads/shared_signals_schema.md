# Shared winner signals schema (Mar 2026 onward)

Canonical signal contract for pacing, intelligence, and creative agents. **Single source:** this file only (`docs/context_repository/paid_ads/shared_signals_schema.md`).

## Storage

- Base directory: `outputs/training_data/paid_ads/signals/`
- Partitioned Parquet: `platform=<meta|google>/grain=<daily|weekly|monthly>/entity_type=<...>/signals.parquet`
- Agent-friendly JSONL:
  - `signals_latest.jsonl`
  - Per-run `signals.jsonl` under intelligence week folders
  - `meta_monthly_signals.jsonl`, `google_monthly_signals.jsonl` (platform-specific monthly rollups where emitted)

## Required fields

- `platform`
- `entity_type`
- `entity_id`
- `entity_text`
- `campaign_name`
- `date_start`, `date_stop`
- `grain`
- `impressions`, `clicks`, `spend`
- `results_or_conversions`
- `ctr`
- `roi_priority_weight`, `roi_norm`, `perf_signal`, `blended_score`
- `confidence_class`
- `fatigue_flag`, `volatility_flag`

## Phase 2 extensions

- `action_priority_score` — deterministic composite for triage (efficiency + CTR + spend discipline + **batch-normalized CPM** × confidence), using weights:
  - `anomaly_weight_cpl` 0.45
  - `anomaly_weight_ctr` 0.25
  - `anomaly_weight_spend` 0.15
  - `anomaly_weight_cpm` 0.15 (CPM normalized 0–1 within the platform batch for the run)
- `anomaly_score` — same numeric composite as `action_priority_score` in current build; kept for reporting/schema clarity.
- `cpm`, `cpm_norm` — raw CPM (platform currency) and within-batch normalized CPM used in the composite.
- `fatigue_flag` — **true** when prior-period WoW exceeds thresholds: CTR drop ≥ `fatigue_ctr_drop_pct` or CPL rise ≥ `fatigue_cpl_rise_pct` (requires successful prior-period API pull).
- `wow_ctr_delta_pct`, `wow_cpl_delta_pct`, `fatigue_ctr_drop`, `fatigue_cpl_rise` — audit fields for fatigue logic.

## Tunables (`INTELLIGENCE_SIGNAL_THRESHOLDS`)

- `wow_materiality_pct` (default 15.0)
- `fatigue_ctr_drop_pct` (default 12.0)
- `fatigue_cpl_rise_pct` (default 15.0)
- Confidence bands: high / medium / low / insufficient (impressions, clicks, `results_or_conversions` thresholds as in code)

## Confidence classes

- `high`: impressions ≥ 5000 and clicks ≥ 100 and `results_or_conversions` ≥ 5  
- `medium`: impressions ≥ 2000 and clicks ≥ 40 and `results_or_conversions` ≥ 2  
- `low`: impressions ≥ 1000 and clicks ≥ 20 and `results_or_conversions` ≥ 1  
- `insufficient`: otherwise  
