from __future__ import annotations

from typing import Tuple

import pandas as pd

from config import AllocationConfig
from calculations import PortfolioSummary


def allocate_daily_budgets(
    per_campaign: pd.DataFrame,
    portfolio_summary: PortfolioSummary,
    cfg: AllocationConfig,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compute recommended daily budgets and a compact budget changes table.

    Expects per_campaign to include:
      - campaign_id, platform, ad_account_id, campaign_name
      - monthly_budget, performance_bucket, priority_tier
    """
    if per_campaign.empty:
        return per_campaign, pd.DataFrame()

    df = per_campaign.copy()

    # Basic weights: monthly_budget * perf_multiplier * priority_multiplier
    perf_mult = {"good": 1.3, "average": 1.0, "poor": 0.6}
    df["perf_multiplier"] = df["performance_bucket"].map(perf_mult).fillna(1.0)

    priority_mult = {"A": 1.2, "B": 1.0, "C": 0.8}
    df["priority_multiplier"] = df["priority_tier"].map(priority_mult).fillna(1.0)

    df["weight_raw"] = df["monthly_budget"] * df["perf_multiplier"] * df["priority_multiplier"]
    total_weight = df["weight_raw"].sum()

    if total_weight <= 0:
        df["weight_normalized"] = 1.0 / len(df)
    else:
        df["weight_normalized"] = df["weight_raw"] / total_weight

    target_daily_spend = portfolio_summary.required_portfolio_daily_run_rate
    df["recommended_daily_budget_raw"] = df["weight_normalized"] * target_daily_spend

    # Apply guardrails
    df["recommended_daily_budget"] = df["recommended_daily_budget_raw"].clip(
        lower=cfg.min_daily_budget, upper=cfg.max_daily_budget
    )

    if "current_daily_budget" not in df.columns:
        df["current_daily_budget"] = df["recommended_daily_budget"]

    # Cap daily percentage change
    def cap_change(row) -> float:
        current = float(row["current_daily_budget"] or 0.0)
        proposed = float(row["recommended_daily_budget"])
        if current <= 0:
            return proposed
        delta = proposed - current
        max_abs_delta = cfg.max_daily_change_pct * current
        if delta > max_abs_delta:
            return current + max_abs_delta
        if delta < -max_abs_delta:
            return current - max_abs_delta
        return proposed

    df["recommended_daily_budget_capped"] = df.apply(cap_change, axis=1)
    df["daily_budget_delta"] = df["recommended_daily_budget_capped"] - df["current_daily_budget"]

    # Build compact changes table
    change_mask = df["daily_budget_delta"].abs() > 0.01
    changes_cols = [
        "campaign_id",
        "campaign_name",
        "platform",
        "ad_account_id",
        "current_daily_budget",
        "recommended_daily_budget_capped",
        "daily_budget_delta",
    ]
    available_cols = [c for c in changes_cols if c in df.columns]
    budget_changes = df.loc[change_mask, available_cols].copy()

    return df, budget_changes

