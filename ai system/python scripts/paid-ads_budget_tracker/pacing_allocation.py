from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from config import AllocationConfig, MonthContext
from performance_scores import (
    add_scores_and_buckets,
    eligible_for_decrease,
    eligible_for_increase,
    normalize_weights,
)


@dataclass
class ChannelPacingSummary:
    platform: str
    monthly_budget_total: float  # playbook live rows only
    spend_mtd_total: float  # full channel when overrides used (all campaigns in live pull)
    sum_current_daily_budget: float  # full channel when overrides used
    forecast_month_spend: float
    pacing_delta: float  # monthly - forecast (positive = underspend)
    daily_pool: float  # target sum of daily budget deltas across channel
    days_remaining: int
    required_daily_run_rate: float  # (B - S) / d_rem


def _month_end(d: date) -> date:
    if d.month == 12:
        nxt = date(d.year + 1, 1, 1)
    else:
        nxt = date(d.year, d.month + 1, 1)
    return date.fromordinal(nxt.toordinal() - 1)


def month_context_for(as_of: date) -> MonthContext:
    ms = as_of.replace(day=1)
    me = _month_end(as_of)
    return MonthContext(month_start=ms, month_end=me, today=as_of)


def _forecast_row(spend_mtd: float, daily_budget: float, d_rem: int) -> float:
    return float(spend_mtd) + float(daily_budget) * d_rem


def build_channel_frame(
    merged: pd.DataFrame,
    platform: str,
    month_ctx: MonthContext,
    *,
    merged_all: Optional[pd.DataFrame] = None,
    channel_spend_mtd_total: Optional[float] = None,
    channel_daily_budget_sum: Optional[float] = None,
) -> Tuple[pd.DataFrame, ChannelPacingSummary]:
    """Filter rows to platform and add pacing + score columns.

    ``merged`` is **live** playbook rows only (``live_merged``). Optional ``merged_all`` is the
    full playbook join after redistribution — used when there are no live rows in-channel but we
    still need the channel monthly budget total (non-live playbook $).

    When ``channel_spend_mtd_total`` / ``channel_daily_budget_sum`` are set (full-portfolio
    pull), they override the sums used for **channel-level** pacing (summary, forecast, pool).
    Per-row metrics still use playbook-matched spend/daily only. This captures spend from
    campaigns that are not in the playbook but ran in the account during the month.
    """
    plat = platform.lower()
    df = merged[merged["platform"].str.lower() == plat].copy()
    if df.empty:
        has_full = channel_spend_mtd_total is not None or channel_daily_budget_sum is not None
        if has_full and merged_all is not None and not merged_all.empty and "platform" in merged_all.columns:
            B_ch = float(merged_all.loc[merged_all["platform"].str.lower() == plat, "monthly_budget"].sum())
            S = float(channel_spend_mtd_total or 0)
            b_sum = float(channel_daily_budget_sum or 0)
            d_rem = month_ctx.days_remaining
            F = S + b_sum * d_rem
            gap = B_ch - F
            daily_pool = gap / d_rem if d_rem > 0 else 0.0
            req_daily = (B_ch - S) / d_rem if d_rem > 0 else 0.0
            summary = ChannelPacingSummary(
                platform=platform,
                monthly_budget_total=B_ch,
                spend_mtd_total=S,
                sum_current_daily_budget=b_sum,
                forecast_month_spend=F,
                pacing_delta=gap,
                daily_pool=daily_pool,
                days_remaining=d_rem,
                required_daily_run_rate=req_daily,
            )
            return df, summary
        if has_full:
            S = float(channel_spend_mtd_total or 0)
            b_sum = float(channel_daily_budget_sum or 0)
            d_rem = month_ctx.days_remaining
            F = S + b_sum * d_rem
            B_ch = 0.0
            gap = B_ch - F
            daily_pool = gap / d_rem if d_rem > 0 else 0.0
            req_daily = (B_ch - S) / d_rem if d_rem > 0 else 0.0
            summary = ChannelPacingSummary(
                platform=platform,
                monthly_budget_total=B_ch,
                spend_mtd_total=S,
                sum_current_daily_budget=b_sum,
                forecast_month_spend=F,
                pacing_delta=gap,
                daily_pool=daily_pool,
                days_remaining=d_rem,
                required_daily_run_rate=req_daily,
            )
            return df, summary
        return df, ChannelPacingSummary(
            platform=platform,
            monthly_budget_total=0.0,
            spend_mtd_total=0.0,
            sum_current_daily_budget=0.0,
            forecast_month_spend=0.0,
            pacing_delta=0.0,
            daily_pool=0.0,
            days_remaining=month_ctx.days_remaining,
            required_daily_run_rate=0.0,
        )

    d_rem = month_ctx.days_remaining
    df["forecast_month_spend"] = df.apply(
        lambda r: _forecast_row(r["spend_mtd"], r["current_daily_budget"], d_rem), axis=1
    )
    # monthly_budget is effective target (includes redistribution from non-live campaigns)
    df["pacing_delta_campaign"] = df["monthly_budget"].astype(float) - df["forecast_month_spend"]

    B = float(df["monthly_budget"].sum())
    S = float(df["spend_mtd"].sum())
    b_sum = float(df["current_daily_budget"].sum())
    if channel_spend_mtd_total is not None:
        S = float(channel_spend_mtd_total)
    if channel_daily_budget_sum is not None:
        b_sum = float(channel_daily_budget_sum)
    F = S + b_sum * d_rem
    gap = B - F
    daily_pool = gap / d_rem if d_rem > 0 else 0.0
    req_daily = (B - S) / d_rem if d_rem > 0 else 0.0

    df = add_scores_and_buckets(df)

    summary = ChannelPacingSummary(
        platform=platform,
        monthly_budget_total=B,
        spend_mtd_total=S,
        sum_current_daily_budget=b_sum,
        forecast_month_spend=F,
        pacing_delta=gap,
        daily_pool=daily_pool,
        days_remaining=d_rem,
        required_daily_run_rate=req_daily,
    )
    return df, summary


def _attach_blended_and_tiebreak_columns(out: pd.DataFrame, cfg: AllocationConfig) -> pd.Series:
    """Core 85/15 blend + tie-break decomposition (audit columns on ``out``). Returns final blended weights."""
    roi = pd.to_numeric(out.get("roi_priority_weight", 0.0), errors="coerce").fillna(0.0)
    roi_norm = roi.copy()
    pos = roi_norm > 0
    if pos.any():
        med = float(roi_norm[pos].median())
        if med > 0:
            roi_norm[pos] = (roi_norm[pos] / med).clip(lower=0.25, upper=4.0)
    roi_norm[~pos] = 1.0
    perf_norm = pd.to_numeric(out.get("performance_score", 1.0), errors="coerce").fillna(1.0)
    pm = float(perf_norm[perf_norm > 0].median()) if (perf_norm > 0).any() else 1.0
    if pm > 0:
        perf_norm = (perf_norm / pm).clip(lower=0.25, upper=4.0)
    blended_core = 0.15 * perf_norm + 0.85 * roi_norm
    has_winning_angle = pd.to_numeric(out.get("has_winning_angle", 0.0), errors="coerce").fillna(0.0)
    fatigue_flag = pd.to_numeric(out.get("fatigue_flag", 0.0), errors="coerce").fillna(0.0)
    volatility_flag = pd.to_numeric(out.get("volatility_flag", 0.0), errors="coerce").fillna(0.0)
    low_confidence_flag = pd.to_numeric(out.get("low_confidence_flag", 0.0), errors="coerce").fillna(0.0)
    d_win = float(cfg.winning_angle_bonus) * has_winning_angle
    d_fat = -float(cfg.fatigue_penalty) * fatigue_flag
    d_vol = -float(cfg.volatility_penalty) * volatility_flag
    d_lc = -float(cfg.low_confidence_penalty) * low_confidence_flag
    modifier_stage1 = (
        1.0
        + float(cfg.winning_angle_bonus) * has_winning_angle
        - float(cfg.fatigue_penalty) * fatigue_flag
        - float(cfg.volatility_penalty) * volatility_flag
        - float(cfg.low_confidence_penalty) * low_confidence_flag
    ).clip(
        lower=float(getattr(cfg, "tie_break_modifier_min", 0.85)),
        upper=float(getattr(cfg, "tie_break_modifier_max", 1.15)),
    )
    max_impact = float(getattr(cfg, "tie_break_max_net_impact_pct", 0.15))
    modifier_final = modifier_stage1.clip(lower=1.0 - max_impact, upper=1.0 + max_impact)
    out["blended_core_85_15"] = blended_core
    out["tie_break_delta_winning_angle"] = d_win
    out["tie_break_delta_fatigue"] = d_fat
    out["tie_break_delta_volatility"] = d_vol
    out["tie_break_delta_low_confidence"] = d_lc
    out["tie_break_modifier_before_net_cap"] = modifier_stage1
    out["tie_break_modifier"] = modifier_final
    blended_final = (blended_core * modifier_final).clip(lower=0.1, upper=10.0)
    return blended_final


def allocate_channel(
    df: pd.DataFrame,
    summary: ChannelPacingSummary,
    cfg: AllocationConfig,
) -> pd.DataFrame:
    """Apply daily_pool to high performers (increase) or low performers (decrease)."""
    if df.empty:
        return df

    out = df.copy()
    d_rem = summary.days_remaining
    pool = summary.daily_pool

    out["allocation_delta_daily"] = 0.0
    out["recommended_daily_budget"] = out["current_daily_budget"].astype(float)
    out["allocation_share_pct"] = 0.0

    blended = _attach_blended_and_tiebreak_columns(out, cfg)

    if d_rem <= 0 or abs(pool) < 1e-9:
        out["note"] = "Month ending or no pacing gap at channel level; no daily redistribution."
        out = _apply_caps_and_notes(out, cfg)
        out["pct_budget_change"] = out.apply(_pct_change, axis=1)
        return out

    if pool > 0:
        elig = eligible_for_increase(out)
        if not elig.any():
            elig = out["performance_score"] >= out["performance_score"].median()
        sub = out.loc[elig]
        if sub.empty:
            out["note"] = "Underspend but no eligible campaigns; check CPL data."
            return _apply_caps_and_notes(out, cfg)
        scores = blended.loc[sub.index].to_numpy(dtype=float)
        w = normalize_weights(scores, cfg.weight_alpha, cfg.epsilon)
        out.loc[sub.index, "allocation_delta_daily"] = pool * w
        out.loc[sub.index, "allocation_share_pct"] = 100.0 * w
        out["recommended_daily_budget"] = out["current_daily_budget"].astype(float) + out[
            "allocation_delta_daily"
        ]
        out["note"] = out.apply(
            lambda r: _note_increase(r, bool(elig.at[r.name]), pool, summary.monthly_budget_total, summary.forecast_month_spend),
            axis=1,
        )
        out = _apply_caps_and_notes(out, cfg)
        out = _reconcile_channel_delta_to_pool(out, pool)
        out["pct_budget_change"] = out.apply(_pct_change, axis=1)
        return out

    elig = eligible_for_decrease(out)
    if not elig.any():
        elig = out["performance_score"] <= out["performance_score"].median()
    sub = out.loc[elig]
    if sub.empty:
        out["note"] = "Overspend but no eligible campaigns; check CPL data."
        return _apply_caps_and_notes(out, cfg)
    base = blended.loc[sub.index].to_numpy(dtype=float)
    inv = 1.0 / np.maximum(base, cfg.epsilon)
    w = normalize_weights(inv, cfg.weight_alpha, cfg.epsilon)
    out.loc[sub.index, "allocation_delta_daily"] = pool * w
    out.loc[sub.index, "allocation_share_pct"] = 100.0 * w
    out["recommended_daily_budget"] = out["current_daily_budget"].astype(float) + out[
        "allocation_delta_daily"
    ]
    out["note"] = out.apply(
        lambda r: _note_decrease(r, bool(elig.at[r.name]), pool, summary.monthly_budget_total, summary.forecast_month_spend),
        axis=1,
    )
    out = _apply_caps_and_notes(out, cfg)
    out = _reconcile_channel_delta_to_pool(out, pool)
    out["pct_budget_change"] = out.apply(_pct_change, axis=1)
    return out


def _note_increase(
    r: pd.Series,
    is_elig: bool,
    pool: float,
    monthly_total: float,
    forecast_total: float,
) -> str:
    if not is_elig:
        return (
            "Channel underspend but this campaign received no increase: outside high-performer set "
            "(or insufficient ROI/performance vs peers) for this run."
        )
    s = float(r.get("performance_score") or 0)
    b = str(r.get("performance_bucket", "unknown"))
    roi = float(r.get("roi_priority_weight") or 0)
    share = float(r.get("allocation_share_pct") or 0)
    delta = float(r.get("allocation_delta_daily") or 0)
    pipe = float(r.get("pipeline_amount") or 0)
    won = float(r.get("closed_won_amount") or 0)
    return (
        f"Underspend logic: channel gap allocated by ROI-dominant weighting (85% ROI, 15% in-platform performance). "
        f"Inputs: perf={s:.2f} ({b}), pipeline=${pipe:,.0f}, closed_won=${won:,.0f}, roi_weight={roi:,.0f}. "
        f"Campaign share={share:.1f}% of pool ${pool:,.2f} -> daily change ${delta:,.2f}. "
        f"Channel forecast ${forecast_total:,.2f} vs target ${monthly_total:,.2f}."
    )


def _note_decrease(
    r: pd.Series,
    is_elig: bool,
    pool: float,
    monthly_total: float,
    forecast_total: float,
) -> str:
    if not is_elig:
        return (
            "Channel overspend but this campaign held flat: outside low-performer cut set "
            "(or protected by relative ROI/performance) for this run."
        )
    s = float(r.get("performance_score") or 0)
    b = str(r.get("performance_bucket", "unknown"))
    roi = float(r.get("roi_priority_weight") or 0)
    share = float(r.get("allocation_share_pct") or 0)
    delta = float(r.get("allocation_delta_daily") or 0)
    pipe = float(r.get("pipeline_amount") or 0)
    won = float(r.get("closed_won_amount") or 0)
    return (
        f"Overspend logic: channel cut allocated by inverse ROI-dominant weighting (85% ROI, 15% in-platform performance). "
        f"Inputs: perf={s:.2f} ({b}), pipeline=${pipe:,.0f}, closed_won=${won:,.0f}, roi_weight={roi:,.0f}. "
        f"Campaign share={share:.1f}% of pool ${pool:,.2f} -> daily change ${delta:,.2f}. "
        f"Channel forecast ${forecast_total:,.2f} vs target ${monthly_total:,.2f}."
    )


def _apply_caps_and_notes(
    out: pd.DataFrame,
    cfg: AllocationConfig,
) -> pd.DataFrame:
    if "recommended_daily_budget" not in out.columns:
        out["recommended_daily_budget"] = out["current_daily_budget"].astype(float)
    cap = cfg.max_daily_change_pct

    def cap_row(r: pd.Series) -> float:
        cur = float(r["current_daily_budget"])
        prop = float(r["recommended_daily_budget"])
        if cur <= 0:
            return max(0.0, max(cfg.min_daily_budget, min(prop, cfg.max_daily_budget)))
        lo, hi = cur * (1 - cap), cur * (1 + cap)
        return max(0.0, float(np.clip(prop, lo, hi)))

    out["recommended_daily_budget_capped"] = out.apply(cap_row, axis=1)
    out["daily_budget_delta"] = out["recommended_daily_budget_capped"] - out["current_daily_budget"]

    def append_clamp(r: pd.Series) -> str:
        base = str(r.get("note", ""))
        raw = float(r.get("recommended_daily_budget", 0))
        capv = float(r.get("recommended_daily_budget_capped", raw))
        if abs(raw - capv) > 0.01:
            return base + " Guardrail: change capped by max_daily_change_pct."
        return base

    if "note" in out.columns:
        out["note"] = out.apply(append_clamp, axis=1)
    return out


def _reconcile_channel_delta_to_pool(out: pd.DataFrame, target_pool: float) -> pd.DataFrame:
    """Force Σ daily_budget_delta to equal channel target pool (pacing delta / remaining days)."""
    cur_total = float(out["daily_budget_delta"].sum())
    residual = float(target_pool - cur_total)
    if abs(residual) <= 0.01:
        return out

    for _ in range(8):
        cur_total = float(out["daily_budget_delta"].sum())
        residual = float(target_pool - cur_total)
        if abs(residual) <= 0.01:
            break

        if residual > 0:
            capacity = 100000.0 - pd.to_numeric(out["recommended_daily_budget_capped"], errors="coerce").fillna(0.0)
        else:
            capacity = pd.to_numeric(out["recommended_daily_budget_capped"], errors="coerce").fillna(0.0)
        eligible = capacity > 0.01
        if not eligible.any():
            break

        w = pd.to_numeric(out.get("allocation_share_pct", 0.0), errors="coerce").fillna(0.0)
        if float(w[eligible].sum()) <= 0:
            w = pd.to_numeric(out.get("performance_score", 1.0), errors="coerce").fillna(1.0)
        w = w.where(eligible, 0.0)
        denom = float(w.sum())
        if denom <= 0:
            w = eligible.astype(float)
            denom = float(w.sum())
        w = w / max(denom, 1e-9)

        adj = (residual * w).clip(lower=-capacity, upper=capacity)
        out["recommended_daily_budget_capped"] = (
            pd.to_numeric(out["recommended_daily_budget_capped"], errors="coerce").fillna(0.0) + adj
        ).clip(lower=0.0)
        out["daily_budget_delta"] = out["recommended_daily_budget_capped"] - pd.to_numeric(
            out["current_daily_budget"], errors="coerce"
        ).fillna(0.0)
    return out


def _pct_change(r: pd.Series) -> float:
    cur = float(r.get("current_daily_budget") or 0.0)
    new = float(r.get("recommended_daily_budget_capped") or 0.0)
    if cur <= 0:
        return 0.0
    return 100.0 * (new - cur) / cur
