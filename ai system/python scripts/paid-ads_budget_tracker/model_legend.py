from __future__ import annotations

from config import allocation_config

MODEL_LEGEND_LINES = [
    "Required total daily budget delta (channel): pacing_delta / remaining_days.",
    "Performance score (in-platform): 45% cost structure (target CPL vs actual CPL) + 10% engagement (CTR) + 10% conversion performance (CVR) + 35% conversion volume (leads); tunables in config perf_weight_*.",
    "ROI weighting: roi_priority_weight = pipeline_amount + 2 × closed_won_amount from the provided opportunities sheet.",
    "Allocation rule (ROI-dominant): combined weight = 85% ROI + 15% in-platform performance; overspend channels cut by inverse(combined weight), underspend channels increase by combined weight.",
    "Phase 2 tie-break: optional modifiers (winning angle, fatigue, volatility, low confidence) multiply the blended weight after core 85/15; see CSV columns blended_core_85_15, tie_break_delta_*, tie_break_modifier.",
    f"Non-live redistribution: weighted mix playbook / ROI / winner affinity when redistribute_use_weighted={allocation_config.redistribute_use_weighted}.",
    "Live pull QA: source reliability scores and row coverage ratio appear in the analysis markdown; low coverage → conservative interpretation.",
    "Guardrails: recommended daily budget is clipped to never be below 0.",
]

