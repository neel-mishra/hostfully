"""Merge structured intelligence/training hints into pacing rows.

This bridge keeps pacing's core ROI/performance logic intact and only provides
tie-break modifiers derived from shared signals artifacts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def load_lead_analysis_optional(path: Optional[Path]) -> Optional[dict[str, Any]]:
    if path is None or not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _norm_campaign(v: object) -> str:
    s = str(v or "").strip()
    if " - " in s and s.rsplit(" - ", 1)[-1].isdigit():
        s = s.rsplit(" - ", 1)[0].strip()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_shared_signals_optional(path: Optional[Path]) -> pd.DataFrame:
    if path and path.exists():
        if path.suffix == ".parquet":
            return pd.read_parquet(path)
        if path.suffix == ".jsonl":
            return pd.read_json(path, lines=True)
    root = Path(__file__).resolve().parent.parent.parent.parent
    pq = root / "outputs" / "training_data" / "paid_ads" / "signals" / "signals_latest.parquet"
    jl = root / "outputs" / "training_data" / "paid_ads" / "signals" / "signals_latest.jsonl"
    if pq.exists():
        return pd.read_parquet(pq)
    if jl.exists():
        return pd.read_json(jl, lines=True)
    return pd.DataFrame()


def _campaign_modifiers(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame()
    s = signals.copy()
    s["platform"] = s.get("platform", "").astype(str).str.lower()
    s["campaign_name_norm"] = s.get("campaign_name", "").map(_norm_campaign)
    s["blended_score"] = pd.to_numeric(s.get("blended_score", 0.0), errors="coerce").fillna(0.0)
    threshold = float(s["blended_score"].quantile(0.75)) if not s.empty else 0.0
    s["confidence_class"] = s.get("confidence_class", "").astype(str)
    s["has_winning_angle"] = (
        (s["blended_score"] >= threshold) & (~s["confidence_class"].isin(["insufficient", "low"]))
    ).astype(float)
    s["fatigue_flag"] = s.get("fatigue_flag", False).astype(bool).astype(float)
    s["volatility_flag"] = s.get("volatility_flag", False).astype(bool).astype(float)
    s["low_confidence_flag"] = s["confidence_class"].isin(["insufficient", "low"]).astype(float)
    g = (
        s.groupby(["platform", "campaign_name_norm"], dropna=False)[
            ["has_winning_angle", "fatigue_flag", "volatility_flag", "low_confidence_flag"]
        ]
        .mean()
        .reset_index()
    )
    return g


def merge_intelligence_hints(
    df: pd.DataFrame,
    lead_analysis: Optional[dict],
    signals_path: Optional[Path] = None,
) -> pd.DataFrame:
    if df.empty:
        return df
    signals = load_shared_signals_optional(signals_path)
    mods = _campaign_modifiers(signals)
    if mods.empty:
        return df
    out = df.copy()
    out["platform_norm"] = out.get("platform", "").astype(str).str.lower()
    campaign_col = "platform_campaign_name" if "platform_campaign_name" in out.columns else "campaign_name"
    if campaign_col not in out.columns:
        out["campaign_name_norm"] = ""
    else:
        out["campaign_name_norm"] = out[campaign_col].map(_norm_campaign)
    out = out.merge(
        mods,
        left_on=["platform_norm", "campaign_name_norm"],
        right_on=["platform", "campaign_name_norm"],
        how="left",
    )
    for c in ("has_winning_angle", "fatigue_flag", "volatility_flag", "low_confidence_flag"):
        out[c] = pd.to_numeric(out.get(c, 0.0), errors="coerce").fillna(0.0)
    return out.drop(columns=[c for c in ("platform_norm", "platform_y") if c in out.columns], errors="ignore")
