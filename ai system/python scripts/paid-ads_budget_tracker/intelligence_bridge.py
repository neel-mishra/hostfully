"""
Optional hook: merge richer signals from paid ads intelligence outputs (lead_analysis.json).

v1: scores are computed from CPL vs target in pacing_allocation + performance_scores.
When present, load JSON and merge extra columns by campaign_id / platform_campaign_id.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def load_lead_analysis_optional(path: Optional[Path]) -> Optional[dict[str, Any]]:
    if path is None or not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge_intelligence_hints(df: pd.DataFrame, lead_analysis: Optional[dict]) -> pd.DataFrame:
    """Placeholder for future multi-granularity modifiers; returns df unchanged if no data."""
    if not lead_analysis:
        return df
    return df
