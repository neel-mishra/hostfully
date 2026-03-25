from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


def workspace_root() -> Path:
    """TLDR repo root: paid-ads_budget_tracker/config.py -> 4 parents up."""
    return Path(__file__).resolve().parent.parent.parent.parent


@dataclass
class MonthContext:
    month_start: date
    month_end: date
    today: date

    @property
    def days_in_month(self) -> int:
        return (self.month_end - self.month_start).days + 1

    @property
    def days_elapsed(self) -> int:
        return (self.today - self.month_start).days + 1

    @property
    def days_remaining(self) -> int:
        """Days after *today* through month-end (inclusive of future days only)."""
        return max(0, (self.month_end - self.today).days)


@dataclass
class Paths:
    campaign_playbook: str = "docs/paid_ads_assets/campaign_playbook_monthly.csv"
    campaign_mapping: str = "data/config/campaign_mapping.csv"
    # Live campaign snapshot: current_daily_budget + spend_mtd from Meta/Google (MCP or export)
    campaign_snapshot: str = "docs/analytics_reports/campaign_snapshot_latest.csv"
    daily_tracker_output_dir: str = "docs/analytics_reports/budget pacing"


@dataclass
class AllocationConfig:
    max_daily_change_pct: float = 0.3
    min_daily_budget: float = 5.0
    max_daily_budget: float = 100000.0
    # Weight sharpness: higher = more budget to the best vs marginal good performers
    weight_alpha: float = 2.0
    epsilon: float = 0.01
    min_leads_for_tier: int = 1
    min_spend_for_tier: float = 25.0


paths = Paths()
allocation_config = AllocationConfig()


def resolve_repo_path(relative: str) -> Path:
    return workspace_root() / relative


def load_env_files() -> None:
    """
    Load env vars for API credentials. Order: repo `.env` then `miscellaneous/.env`
    (latter overrides) — matches teams that keep secrets only under miscellaneous/.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    root = workspace_root()
    load_dotenv(root / ".env")
    misc = root / "miscellaneous" / ".env"
    if misc.exists():
        load_dotenv(misc, override=True)
