from __future__ import annotations

import numpy as np
import pandas as pd

from config import allocation_config


def compute_performance_score(row: pd.Series) -> float:
    """Backward-compatible row scorer (used as fallback)."""
    target = row.get("target_kpi_value")
    cpl = row.get("cpl_mtd")
    if target is None or pd.isna(target) or float(target) <= 0:
        return 1.0
    if cpl is None or pd.isna(cpl) or float(cpl) <= 0:
        return 0.5
    ratio = float(target) / float(cpl)
    return float(np.clip(ratio, 0.1, 10.0))


def _cpl(r: pd.Series):
    spend = float(r.get("spend_mtd") or 0)
    leads = float(r.get("leads_mtd") or 0)
    if leads <= 0:
        return None
    return spend / leads


def _ctr(r: pd.Series):
    imp = float(r.get("impressions_mtd") or 0)
    clk = float(r.get("clicks_mtd") or 0)
    if imp <= 0:
        return None
    return clk / imp


def _cvr(r: pd.Series):
    clk = float(r.get("clicks_mtd") or 0)
    leads = float(r.get("leads_mtd") or 0)
    if clk <= 0:
        return None
    return leads / clk


def add_scores_and_buckets(df: pd.DataFrame) -> pd.DataFrame:
    """Adds engagement/cost/conversion signals and blended performance score.

    Composite weights (see ``AllocationConfig``): default **45% cost / 10% engagement /
    10% conversion / 35% volume**; must sum to 1.0.
    """
    out = df.copy()
    out["cpl_mtd"] = out.apply(_cpl, axis=1)
    out["ctr_mtd"] = out.apply(_ctr, axis=1)
    out["cvr_mtd"] = out.apply(_cvr, axis=1)

    target = pd.to_numeric(out.get("target_kpi_value", np.nan), errors="coerce")
    cpl = pd.to_numeric(out.get("cpl_mtd", np.nan), errors="coerce")
    cost_score = pd.Series(np.ones(len(out)), index=out.index, dtype=float)
    has_target = target.notna() & (target > 0) & cpl.notna() & (cpl > 0)
    cost_score.loc[has_target] = (target.loc[has_target] / cpl.loc[has_target]).clip(0.1, 10.0)

    ctr = pd.to_numeric(out.get("ctr_mtd", np.nan), errors="coerce")
    cvr = pd.to_numeric(out.get("cvr_mtd", np.nan), errors="coerce")
    leads = pd.to_numeric(out.get("leads_mtd", np.nan), errors="coerce").fillna(0.0)

    ctr_med = float(ctr[ctr > 0].median()) if (ctr > 0).any() else 0.0
    cvr_med = float(cvr[cvr > 0].median()) if (cvr > 0).any() else 0.0
    leads_med = float(leads[leads > 0].median()) if (leads > 0).any() else 0.0

    engagement_score = pd.Series(np.ones(len(out)), index=out.index, dtype=float)
    if ctr_med > 0:
        engagement_score = (ctr / ctr_med).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(0.25, 4.0)

    conv_score = pd.Series(np.ones(len(out)), index=out.index, dtype=float)
    if cvr_med > 0:
        conv_score = (cvr / cvr_med).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(0.25, 4.0)

    volume_score = pd.Series(np.ones(len(out)), index=out.index, dtype=float)
    if leads_med > 0:
        volume_score = (leads / leads_med).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(0.25, 4.0)

    out["cost_score"] = cost_score
    out["engagement_score"] = engagement_score
    out["conversion_score"] = conv_score
    out["volume_score"] = volume_score
    wc = float(allocation_config.perf_weight_cost)
    we = float(allocation_config.perf_weight_engagement)
    wf = float(allocation_config.perf_weight_conversion)
    wv = float(allocation_config.perf_weight_volume)
    wsum = wc + we + wf + wv
    if abs(wsum - 1.0) > 1e-6:
        raise ValueError(
            f"In-platform perf weights must sum to 1.0; got {wsum} "
            f"(cost={wc}, engagement={we}, conversion={wf}, volume={wv})"
        )
    out["performance_score"] = (
        wc * out["cost_score"]
        + we * out["engagement_score"]
        + wf * out["conversion_score"]
        + wv * out["volume_score"]
    ).clip(0.1, 10.0)

    def bucket(r) -> str:
        target = r.get("target_kpi_value")
        cpl = r.get("cpl_mtd")
        if target is None or pd.isna(target) or cpl is None or pd.isna(cpl):
            return "unknown"
        t = float(target)
        if float(cpl) <= 0.9 * t:
            return "good"
        if float(cpl) <= 1.1 * t:
            return "average"
        return "poor"

    out["performance_bucket"] = out.apply(bucket, axis=1)
    return out


def eligible_for_increase(df: pd.DataFrame) -> pd.Series:
    """High performers: good bucket, or score at/above Q75 among rows with CPL."""
    good = df["performance_bucket"] == "good"
    has_cpl = df["cpl_mtd"].notna()
    if not has_cpl.any():
        return pd.Series(True, index=df.index)
    q75 = float(df.loc[has_cpl, "performance_score"].quantile(0.75))
    return good | (has_cpl & (df["performance_score"] >= q75))


def eligible_for_decrease(df: pd.DataFrame) -> pd.Series:
    """Low performers: poor bucket, or score at/below Q25 among rows with CPL."""
    poor = df["performance_bucket"] == "poor"
    has_cpl = df["cpl_mtd"].notna()
    if not has_cpl.any():
        return pd.Series(True, index=df.index)
    q25 = float(df.loc[has_cpl, "performance_score"].quantile(0.25))
    return poor | (has_cpl & (df["performance_score"] <= q25))


def normalize_weights(scores: np.ndarray, alpha: float, epsilon: float) -> np.ndarray:
    w = np.maximum(epsilon, scores) ** alpha
    s = w.sum()
    if s <= 0:
        return np.ones_like(w) / max(len(w), 1)
    return w / s
