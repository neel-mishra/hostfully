from __future__ import annotations

from typing import Iterable

import pandas as pd


def combine_daily_performance(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    """Combine multiple normalized performance DataFrames into one."""
    frames = [f for f in frames if f is not None and not f.empty]
    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def join_with_campaign_mapping(
    performance: pd.DataFrame, mapping: pd.DataFrame
) -> pd.DataFrame:
    """Attach canonical campaign_id using the mapping table."""
    if performance.empty:
        return performance

    required_cols = {"platform", "ad_account_id", "platform_campaign_id"}
    missing = required_cols - set(performance.columns)
    if missing:
        raise ValueError(f"performance missing columns: {missing}")

    mapping_required = {"campaign_id", "platform", "ad_account_id", "platform_campaign_id"}
    missing_map = mapping_required - set(mapping.columns)
    if missing_map:
        raise ValueError(f"mapping missing columns: {missing_map}")

    merged = performance.merge(
        mapping[mapping_required],
        on=["platform", "ad_account_id", "platform_campaign_id"],
        how="left",
    )
    return merged

