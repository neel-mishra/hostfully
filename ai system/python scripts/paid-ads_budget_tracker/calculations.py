from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from config import MonthContext


@dataclass
class PortfolioSummary:
    portfolio_monthly_budget: float
    portfolio_spend_to_date: float
    portfolio_run_rate: float
    portfolio_forecast_spend_eom: float
    portfolio_gap_total: float
    required_portfolio_daily_run_rate: float


def enrich_campaign_level(
    campaign_playbook: pd.DataFrame,
    campaign_perf: pd.DataFrame,
    month_ctx: MonthContext,
) -> Tuple[pd.DataFrame, PortfolioSummary]:
    """
    Compute per-campaign budget tracking metrics and portfolio summary.

    campaign_playbook: must contain campaign_id, monthly_budget,
                       planned_start_date, planned_end_date.
    campaign_perf: per-day performance already joined with campaign_id.
    """
    if campaign_perf.empty:
        # still compute portfolio from playbook
        portfolio_monthly_budget = float(campaign_playbook["monthly_budget"].sum())
        portfolio_spend_to_date = 0.0
    else:
        campaign_perf = campaign_perf.copy()
        campaign_perf["date"] = pd.to_datetime(campaign_perf["date"]).dt.date
        mask_current_month = (
            (campaign_perf["date"] >= month_ctx.month_start)
            & (campaign_perf["date"] <= month_ctx.today)
        )
        campaign_perf = campaign_perf.loc[mask_current_month]
        portfolio_spend_to_date = float(campaign_perf["spend"].sum())
        portfolio_monthly_budget = float(campaign_playbook["monthly_budget"].sum())

    days_elapsed = max(month_ctx.days_elapsed, 1)
    portfolio_run_rate = portfolio_spend_to_date / days_elapsed
    portfolio_forecast_spend_eom = portfolio_run_rate * month_ctx.days_in_month
    portfolio_gap_total = portfolio_monthly_budget - portfolio_forecast_spend_eom

    if month_ctx.days_remaining > 0:
        required_daily = (portfolio_monthly_budget - portfolio_spend_to_date) / month_ctx.days_remaining
    else:
        required_daily = 0.0

    portfolio_summary = PortfolioSummary(
        portfolio_monthly_budget=portfolio_monthly_budget,
        portfolio_spend_to_date=portfolio_spend_to_date,
        portfolio_run_rate=portfolio_run_rate,
        portfolio_forecast_spend_eom=portfolio_forecast_spend_eom,
        portfolio_gap_total=portfolio_gap_total,
        required_portfolio_daily_run_rate=required_daily,
    )

    # Per-campaign breakdown
    if campaign_perf.empty:
        per_campaign = campaign_playbook.copy()
        per_campaign["spend_to_date"] = 0.0
        per_campaign["leads_to_date"] = 0.0
        per_campaign["cpl_to_date"] = None
    else:
        grouped = campaign_perf.groupby("campaign_id", as_index=False).agg(
            spend_to_date=("spend", "sum"),
            leads_to_date=("leads", "sum"),
        )

        per_campaign = campaign_playbook.merge(grouped, on="campaign_id", how="left")
        per_campaign["spend_to_date"] = per_campaign["spend_to_date"].fillna(0.0)
        per_campaign["leads_to_date"] = per_campaign["leads_to_date"].fillna(0.0)

    # CPL and performance bucket (simple v1)
    per_campaign["cpl_to_date"] = per_campaign.apply(
        lambda r: (r["spend_to_date"] / r["leads_to_date"]) if r["leads_to_date"] > 0 else None,
        axis=1,
    )

    def perf_bucket(row) -> str:
        target = row.get("target_kpi_value")
        cpl = row.get("cpl_to_date")
        if target is None or pd.isna(target) or cpl is None or pd.isna(cpl):
            return "unknown"
        if cpl <= 0.9 * target:
            return "good"
        if cpl <= 1.1 * target:
            return "average"
        return "poor"

    per_campaign["performance_bucket"] = per_campaign.apply(perf_bucket, axis=1)

    # Simple run rate and forecast per campaign
    per_campaign["camp_run_rate"] = per_campaign["spend_to_date"] / days_elapsed
    per_campaign["camp_forecast_spend_eom"] = per_campaign["camp_run_rate"] * month_ctx.days_in_month
    per_campaign["camp_gap_total"] = per_campaign["monthly_budget"] - per_campaign["camp_forecast_spend_eom"]

    return per_campaign, portfolio_summary

