from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import pandas as pd

from config import paths, resolve_repo_path, workspace_root


def load_campaign_playbook() -> pd.DataFrame:
    """Load the monthly campaign playbook."""
    csv_path = resolve_repo_path(paths.campaign_playbook)
    if not csv_path.exists():
        raise FileNotFoundError(f"Campaign playbook not found at {csv_path}")
    return pd.read_csv(csv_path)


def load_campaign_mapping() -> pd.DataFrame:
    """Load mapping between platform campaign IDs and canonical campaign_id."""
    csv_path = resolve_repo_path(paths.campaign_mapping)
    if not csv_path.exists():
        raise FileNotFoundError(f"Campaign mapping file not found at {csv_path}")
    return pd.read_csv(csv_path)


def load_campaign_snapshot(path: str | None = None) -> pd.DataFrame:
    """
    Load live snapshot: current_daily_budget, spend_mtd, optional leads_mtd per campaign_id.

    Override path with env CAMPAIGN_SNAPSHOT_PATH or argument.
    """
    p = path or os.environ.get("CAMPAIGN_SNAPSHOT_PATH")
    if p:
        csv_path = Path(p)
        if not csv_path.is_absolute():
            csv_path = workspace_root() / p
    else:
        csv_path = resolve_repo_path(paths.campaign_snapshot)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Campaign snapshot not found at {csv_path}. "
            "Populate from Meta/Google (MCP) or set CAMPAIGN_SNAPSHOT_PATH."
        )
    return pd.read_csv(csv_path)


def write_daily_tracker(df: pd.DataFrame, as_of_date: str, output_dir: Path | None = None) -> Path:
    """Write the daily budget tracker for a given date."""
    output_dir = output_dir or resolve_repo_path(paths.daily_tracker_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"daily_budget_tracker_{as_of_date}.csv"
    df.to_csv(out_path, index=False)
    return out_path


def write_budget_changes(df: pd.DataFrame, as_of_date: str, output_dir: Path | None = None) -> Path:
    """Write the proposed budget changes for a given date."""
    output_dir = output_dir or resolve_repo_path(paths.daily_tracker_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"proposed_budget_changes_{as_of_date}.csv"
    df.to_csv(out_path, index=False)
    return out_path


NormalizedPlatform = Literal["meta", "google"]


def empty_daily_performance_frame() -> pd.DataFrame:
    """Return an empty daily performance frame with the normalized schema."""
    columns = [
        "date",
        "platform",
        "ad_account_id",
        "platform_campaign_id",
        "campaign_name_raw",
        "status_actual",
        "spend",
        "impressions",
        "clicks",
        "leads",
        "revenue",
    ]
    return pd.DataFrame(columns=columns)
