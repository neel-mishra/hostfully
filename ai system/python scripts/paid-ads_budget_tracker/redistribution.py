"""
Redistribute monthly playbook budgets from non-live campaigns to live campaigns
so channel totals match the playbook while pacing only reflects spend from live ads.
"""

from __future__ import annotations

import pandas as pd
from config import allocation_config


def merge_playbook_with_snapshot(
    playbook: pd.DataFrame,
    snapshot: pd.DataFrame,
    live_full: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Left-join playbook to snapshot. Campaigns missing from snapshot are not live.

    Optional snapshot column: is_live (bool). If absent, presence in snapshot = live.
    """
    pb = playbook.copy()
    snap = snapshot.copy()
    if "leads_mtd" not in snap.columns:
        snap["leads_mtd"] = 0
    if "clicks_mtd" not in snap.columns:
        snap["clicks_mtd"] = 0
    if "impressions_mtd" not in snap.columns:
        snap["impressions_mtd"] = 0
    # Name as shown in Meta / Google (optional); defaults to snapshot join key for CSV-only runs
    if "platform_campaign_name" not in snap.columns:
        snap["platform_campaign_name"] = snap["campaign_id"].astype(str)
    else:
        snap["platform_campaign_name"] = snap["platform_campaign_name"].fillna(
            snap["campaign_id"].astype(str)
        )
    # Playbook is source of truth for platform; avoid duplicate column on merge
    snap = snap.drop(columns=[c for c in ("platform",) if c in snap.columns], errors="ignore")

    key = "campaign_id"
    merged = pb.merge(snap, on=key, how="left", indicator=True)

    if "is_live" in snap.columns:
        merged["is_live"] = merged["is_live"].fillna(False).astype(bool)
    else:
        merged["is_live"] = merged["_merge"] == "both"

    merged = merged.drop(columns=["_merge"], errors="ignore")

    merged["current_daily_budget"] = merged["current_daily_budget"].fillna(0).astype(float)
    merged["spend_mtd"] = merged["spend_mtd"].fillna(0).astype(float)
    merged["leads_mtd"] = merged["leads_mtd"].fillna(0).astype(float)
    merged["clicks_mtd"] = merged["clicks_mtd"].fillna(0).astype(float)
    merged["impressions_mtd"] = merged["impressions_mtd"].fillna(0).astype(float)
    merged["monthly_budget_playbook"] = merged["monthly_budget"].astype(float)
    merged["source"] = "playbook"
    merged["platform"] = merged["platform"].str.lower()
    if "platform_campaign_name" in merged.columns:
        merged["platform_campaign_name"] = merged["platform_campaign_name"].fillna(
            merged["campaign_id"].astype(str)
        )
    else:
        merged["platform_campaign_name"] = merged["campaign_id"].astype(str)
    # No platform row → show em dash (playbook id is still in campaign_id)
    merged.loc[~merged["is_live"], "platform_campaign_name"] = "—"

    # Non-live campaigns do not spend in-platform
    merged.loc[
        ~merged["is_live"],
        ["current_daily_budget", "spend_mtd", "leads_mtd", "clicks_mtd", "impressions_mtd"],
    ] = 0.0

    # Include live campaigns that exist in platform pulls but not in the playbook.
    # They are included in redistribution/allocation analysis with source=non-playbook.
    if live_full is not None and not live_full.empty:
        needed = {
            "platform",
            "campaign_id",
            "platform_campaign_id",
            "current_daily_budget",
            "spend_mtd",
            "leads_mtd",
            "is_live",
        }
        if needed.issubset(set(live_full.columns)):
            lf = live_full.copy()
            lf["platform"] = lf["platform"].astype(str).str.lower()
            lf = lf[lf["platform"].isin(["meta", "google"])]
            lf = lf[lf["is_live"].fillna(False).astype(bool)]

            existing_platform_ids = set(
                merged["platform_campaign_id"].fillna("").astype(str).str.strip().tolist()
            )
            lf["platform_campaign_id"] = lf["platform_campaign_id"].fillna("").astype(str).str.strip()
            lf = lf[~lf["platform_campaign_id"].isin(existing_platform_ids)]

            if not lf.empty:
                extras = pd.DataFrame(
                    {
                        "campaign_id": lf["campaign_id"].astype(str),
                        "campaign_name": lf["campaign_id"].astype(str),
                        "platform": lf["platform"].astype(str),
                        "target_kpi_type": None,
                        "target_kpi_value": None,
                        "monthly_budget_playbook": 0.0,
                        "monthly_budget": 0.0,
                        "platform_campaign_id": lf["platform_campaign_id"].astype(str),
                        "platform_campaign_name": lf["campaign_id"].astype(str),
                        "current_daily_budget": lf["current_daily_budget"].fillna(0).astype(float),
                        "spend_mtd": lf["spend_mtd"].fillna(0).astype(float),
                        "leads_mtd": lf["leads_mtd"].fillna(0).astype(float),
                        "clicks_mtd": lf["clicks_mtd"].fillna(0).astype(float)
                        if "clicks_mtd" in lf.columns
                        else 0.0,
                        "impressions_mtd": lf["impressions_mtd"].fillna(0).astype(float)
                        if "impressions_mtd" in lf.columns
                        else 0.0,
                        "is_live": True,
                        "source": "non-playbook",
                    }
                )
                merged = pd.concat([merged, extras], ignore_index=True, sort=False)

    return merged


def apply_playbook_redistribution(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Per platform: pool = sum(playbook $ for non-live); split pool across live rows
    proportional to each live row's playbook share.

    Sets monthly_budget_effective (0 for non-live); then sets monthly_budget = monthly_budget_effective
    for use in pacing.
    """
    out = merged.copy()
    out["redistribution_received"] = 0.0
    out["monthly_budget_effective"] = 0.0

    for plat in out["platform"].dropna().unique():
        mask = out["platform"] == plat
        sub = out.loc[mask]
        live = sub["is_live"]
        non_live_pool = float(sub.loc[~live, "monthly_budget_playbook"].sum())
        live_mask = mask & out["is_live"]
        live_weights = out.loc[live_mask, "monthly_budget_playbook"].astype(float).copy()
        # Non-playbook rows have 0 playbook budget; use current daily budget so they
        # can participate in channel redistribution/allocation context.
        fallback = out.loc[live_mask, "current_daily_budget"].astype(float)
        live_weights = live_weights.where(live_weights > 0, fallback)
        if bool(allocation_config.redistribute_use_weighted):
            roi = pd.to_numeric(out.loc[live_mask, "roi_priority_weight"], errors="coerce").fillna(0.0)
            winner = pd.to_numeric(out.loc[live_mask, "has_winning_angle"], errors="coerce").fillna(0.0)
            roi_med = float(roi[roi > 0].median()) if (roi > 0).any() else 0.0
            roi_norm = (roi / roi_med).clip(lower=0.25, upper=4.0) if roi_med > 0 else pd.Series(1.0, index=roi.index)
            winner_norm = 1.0 + winner
            w = (
                float(allocation_config.redistribute_weight_playbook) * live_weights
                + float(allocation_config.redistribute_weight_roi) * roi_norm
                + float(allocation_config.redistribute_weight_winner_affinity) * winner_norm
            )
            # Tier floor protection.
            tier = out.loc[live_mask, "campaign_priority_tier"].astype(str).str.upper() if "campaign_priority_tier" in out.columns else pd.Series("", index=w.index)
            floor = pd.Series(1.0, index=w.index)
            floor = floor.where(tier != "A", float(allocation_config.redistribute_tier_floor_A))
            floor = floor.where(tier != "B", float(allocation_config.redistribute_tier_floor_B))
            floor = floor.where(tier != "C", float(allocation_config.redistribute_tier_floor_C))
            live_weights = (w * floor).clip(lower=0.01)
        live_sum = float(live_weights.sum())

        out.loc[mask & ~out["is_live"], "monthly_budget_effective"] = 0.0

        if not live_mask.any():
            continue

        if live_sum <= 1e-9:
            n = int(live_mask.sum())
            share = non_live_pool / max(n, 1)
            for idx in out.index[live_mask]:
                base = float(out.at[idx, "monthly_budget_playbook"])
                out.at[idx, "redistribution_received"] = share
                out.at[idx, "monthly_budget_effective"] = base + share
            continue

        for idx in out.index[live_mask]:
            base = float(out.at[idx, "monthly_budget_playbook"])
            weight = float(live_weights.loc[idx])
            share = non_live_pool * (weight / live_sum) if live_sum > 1e-9 else 0.0
            out.at[idx, "redistribution_received"] = share
            out.at[idx, "monthly_budget_effective"] = base + share

    out["monthly_budget"] = out["monthly_budget_effective"]
    return out


def split_live_and_nonlive(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    live = df[df["is_live"]].copy()
    nonlive = df[~df["is_live"]].copy()
    return live, nonlive
