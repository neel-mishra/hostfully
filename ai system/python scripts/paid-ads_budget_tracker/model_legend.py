from __future__ import annotations

MODEL_LEGEND_LINES = [
    "Required total daily budget delta (channel): pacing_delta / remaining_days.",
    "Performance score (in-platform): 45% cost structure (target CPL vs actual CPL) + 20% engagement (CTR) + 20% conversion performance (CVR) + 15% conversion volume (leads).",
    "ROI weighting: roi_priority_weight = pipeline_amount + 2 × closed_won_amount from the provided opportunities sheet.",
    "Allocation rule (ROI-dominant): combined weight = 85% ROI + 15% in-platform performance; overspend channels cut by inverse(combined weight), underspend channels increase by combined weight.",
    "Guardrails: recommended daily budget is clipped to never be below 0.",
]

