# Paid Ads Phase 2 Implementation Checklist

This checklist translates Phase 2 opportunities into a build sequence with concrete tasks, parameter names/defaults, and acceptance criteria.

Scope: paid ads multi-agent system, Mar 2026 onward.

---

## Phase 2 goals

- Expand explicit model weighting controls beyond current pacing + winners pipeline.
- Increase reliability of joins/mappings so weighted decisions are based on cleaner data.
- Bring retrieval-driven and weighted logic to **search copy**, **structure**, and **visual briefs**.
- Use competitor saturation as a formal decision constraint.

---

## Workstream A — Data reliability and join quality

### A1. Weighted campaign matching
- **Files**
  - `ai system/python scripts/paid-ads_budget_tracker/campaign_name_match.py`
  - `ai system/python scripts/paid-ads_budget_tracker/pipeline_roi.py`
- **Build tasks**
  - Add match scoring function that returns:
    - `match_type` (`exact`, `canonical`, `fuzzy`, `none`)
    - `match_score` (`0.0-1.0`)
  - Add fuzzy fallback only when exact/canonical fail.
  - Store match diagnostics in output CSV for QA.
- **New parameters (defaults)**
  - `match_weight_exact=1.00`
  - `match_weight_canonical=0.90`
  - `match_weight_fuzzy=0.70`
  - `match_min_score=0.75`
- **Acceptance criteria**
  - Unmatched + low-score rows are explicitly flagged.
  - ROI attribution is reproducible with deterministic match metadata.

### A2. Source reliability weighting for live pulls
- **Files**
  - `ai system/python scripts/paid-ads_budget_tracker/live_portfolio_fetch.py`
  - `ai system/python scripts/paid-ads_budget_tracker/main.py`
- **Build tasks**
  - Add reliability score per source pull (API, fallback snapshot).
  - Add coverage diagnostics (% spend captured, missing campaigns).
  - Expose reliability in pacing analysis markdown.
- **New parameters (defaults)**
  - `source_reliability_api=1.00`
  - `source_reliability_snapshot=0.80`
  - `coverage_warning_threshold=0.90`
- **Acceptance criteria**
  - Report includes reliability/coverage block.
  - Low-coverage runs generate warning and conservative modifier.

---

## Workstream B — Allocation enhancements (still ROI-first)

### B1. Redistribution weighting for non-live playbook dollars
- **Files**
  - `ai system/python scripts/paid-ads_budget_tracker/redistribution.py`
  - `ai system/python scripts/paid-ads_budget_tracker/config.py`
- **Build tasks**
  - Add optional weighted redistribution strategy:
    - base by playbook share
    - modulate by ROI + winner affinity + tier floor.
  - Keep fallback to current proportional behavior.
- **New parameters (defaults)**
  - `redistribute_use_weighted=True`
  - `redistribute_weight_playbook=0.50`
  - `redistribute_weight_roi=0.35`
  - `redistribute_weight_winner_affinity=0.15`
  - `redistribute_tier_floor_A=0.90`
  - `redistribute_tier_floor_B=0.70`
  - `redistribute_tier_floor_C=0.50`
- **Acceptance criteria**
  - Weighted redistribution is explainable in notes.
  - Channel totals still reconcile exactly.

### B2. Calibrated tie-break governance
- **Files**
  - `ai system/python scripts/paid-ads_budget_tracker/pacing_allocation.py`
  - `ai system/python scripts/paid-ads_budget_tracker/config.py`
- **Build tasks**
  - Add explicit cap on total tie-break influence vs core blended score.
  - Emit column-level decomposition for each campaign.
- **New parameters (defaults)**
  - `tie_break_modifier_min=0.85`
  - `tie_break_modifier_max=1.15`
  - `tie_break_max_net_impact_pct=0.15`
- **Acceptance criteria**
  - Core 85/15 remains dominant.
  - Decomposition columns visible in daily tracker outputs.

---

## Workstream C — Intelligence scoring formalization

### C1. Meta/Google analyzer weighted anomaly scoring
- **Files**
  - `ai system/python scripts/paid ads intelligence agent/report_analyzers/meta_ads_analyzer.py`
  - `ai system/python scripts/paid ads intelligence agent/report_analyzers/google_ads_analyzer.py`
  - `ai system/python scripts/paid ads intelligence agent/paid_ads_intelligence_agent.py`
- **Build tasks**
  - Add explicit anomaly score per campaign/entity:
    - efficiency degradation
    - engagement decline
    - spend spike/dip.
  - Add structured “action_priority” output to signals.
- **New parameters (defaults)**
  - `anomaly_weight_cpl=0.45`
  - `anomaly_weight_ctr=0.25`
  - `anomaly_weight_cpm=0.15`
  - `anomaly_weight_spend=0.15`
  - `wow_materiality_pct=15.0`
  - `fatigue_ctr_drop_pct=12.0`
  - `fatigue_cpl_rise_pct=15.0`
- **Acceptance criteria**
  - Reports include ranked anomaly table.
  - `signals.jsonl` includes `action_priority_score`.

---

## Workstream D — Search ads retrieval + weighted generation

### D1. Retrieval-driven search copy
- **Files**
  - `ai system/python scripts/paid acquisition agent/search_ads_agent.py`
- **Build tasks**
  - Load:
    - `docs/context_repository/paid_ads/winning_angles/google_mar2026_onward.md`
    - `docs/context_repository/paid_ads/winning_angles/top10_reusable_angles_mar2026_onward.md`
    - `outputs/training_data/paid_ads/signals/signals_latest.jsonl`
  - Bias headline/description generation by proven angle families.
  - Keep strict character validation post-generation.
- **New parameters (defaults)**
  - `search_weight_keyword_intent=0.40`
  - `search_weight_hist_ctr=0.25`
  - `search_weight_hist_conv=0.35`
  - `search_exploration_ratio=0.20`
- **Acceptance criteria**
  - Output CSV includes angle tag per ad group.
  - At least 80% of variants reference proven patterns.

---

## Workstream E — Creative mapping + structure/brief weighting

### E1. Angle-family weighting map
- **Files**
  - `ai system/python scripts/paid acquisition agent/creative_mapping.py`
- **Build tasks**
  - Add platform/funnel angle priors from winners library.
  - Emit angle score table reusable by `social_ads_agent.py` + `search_ads_agent.py`.
- **New parameters (defaults)**
  - `angle_prior_weight_hist=0.70`
  - `angle_prior_weight_message_fit=0.30`
- **Acceptance criteria**
  - Mapping outputs deterministic top-N angle families per platform/funnel.

### E2. Weighted prompts in structure + visual brief markdown agents
- **Files**
  - `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md`
  - `ai system/agents/gtm team/marketing/paid ads/visual-creative-brief-agent.md`
  - `ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md`
- **Build tasks**
  - Add a “weighting config” section to each agent spec with defaults.
  - Add retrieval references to winners/signals files where missing.
- **New parameters (defaults)**
  - `proven_pattern_ratio=0.80`
  - `exploration_ratio=0.20`
  - `visual_format_weight_static=0.50`
  - `visual_format_weight_video=0.50` (platform-overridden where needed)
- **Acceptance criteria**
  - Agent output templates include explicit weighting assumptions.
  - Same ratio language used across all three specs.

---

## Workstream F — Competitive saturation as formal constraint

### F1. Saturation index weighting
- **Files**
  - `ai system/python scripts/competitive creative tracker/config.py`
  - `ai system/python scripts/competitive creative tracker/competitive_tracker.py`
  - `ai system/python scripts/paid acquisition agent/social_ads_agent.py`
- **Build tasks**
  - Add weighted “saturation index” per angle/platform.
  - Feed index into social ad generator prompt as constraint.
- **New parameters (defaults)**
  - `saturation_threshold_high=0.70`
  - `saturation_penalty_weight=0.25`
  - `hostfully_outperformance_override=0.15`
- **Acceptance criteria**
  - `market_saturation_summary_mar2026_onward.json` contains index scores.
  - Social ads output notes when an angle is deprioritized for saturation.

---

## Validation checklist (end of Phase 2)

- [ ] No regressions in existing pacing outputs (daily budget totals reconcile).
- [ ] Same campaign under same inputs produces identical weighted outputs (deterministic).
- [ ] `signals_latest` and pacing tie-break columns align for winner/fatigue/confidence flags.
- [ ] Search + social generators both consume winners/signals.
- [ ] Competitive saturation constraint appears in generated creative rationale.
- [ ] Documentation updated:
  - `.cursor/guides/paid_ads_multi_agent_architecture.md`
  - `docs/context_repository/paid_ads/shared_signals_schema.md`

---

## Suggested build order (2-week sprint)

1. **Week 1**
   - A1, A2, B1, B2
2. **Week 2**
   - C1, D1, E1, F1, then E2 docs pass

---

## Notes for implementation discipline

- Keep all new weights in config (not scattered in business logic).
- Add defaults that preserve existing behavior when toggles are off.
- For every new weighted score, output the decomposed components for auditability.

