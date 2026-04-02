# Paid Ads — Implementation Notes (Source of Truth)

## Budget pacing source of truth

The current budget pacing outputs in `docs/analytics_reports/budget pacing/` are produced by:

- `ai system/python scripts/paid-ads_budget_tracker/main.py`
  - uses `pacing_allocation.allocate_channel()` (ROI-dominant redistribution logic)
  - uses `performance_scores.add_scores_and_buckets()` for the 45/10/10/35 in-platform score (`AllocationConfig.perf_weight_*`)
  - optionally uses `pipeline_roi.attach_pipeline_roi()` when a pipeline report path is provided

## Known “gaps” / placeholders

- `ai system/python scripts/paid-ads_budget_tracker/intelligence_bridge.py`
  - Placeholder only; **not currently used** in `main.py`
  - Intended future: merge richer signals from paid ads intelligence outputs (e.g. `lead_analysis.json`)

## Legacy allocator path (not currently used for pacing reports)

- `ai system/python scripts/paid-ads_budget_tracker/allocation.py`
  - Implements a simpler allocation model (monthly_budget × perf_multiplier × priority_multiplier)
  - `main.py` does **not** call this allocator; the pacing reports align to `pacing_allocation.py`

