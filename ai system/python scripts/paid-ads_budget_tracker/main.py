from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd

# Allow `python main.py` from this directory (imports config, loaders, …)
_PKG = Path(__file__).resolve().parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from config import (  # noqa: E402
    allocation_config,
    load_env_files,
    paths,
    resolve_repo_path,
    workspace_root,
)
from loaders import (  # noqa: E402
    load_campaign_mapping,
    load_campaign_playbook,
    load_campaign_snapshot,
    write_budget_changes,
    write_daily_tracker,
)
from pacing_allocation import (  # noqa: E402
    allocate_channel,
    build_channel_frame,
    month_context_for,
)
from redistribution import (  # noqa: E402
    apply_playbook_redistribution,
    merge_playbook_with_snapshot,
    split_live_and_nonlive,
)
from spreadsheet_output import write_pacing_workbook  # noqa: E402
from analysis_report import write_analysis_markdown  # noqa: E402
from pipeline_roi import attach_pipeline_roi  # noqa: E402

DEFAULT_USE_LIVE = os.environ.get("BUDGET_TRACKER_USE_LIVE", "1").lower() in (
    "1",
    "true",
    "yes",
)


def _annotate_nonlive_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Attach pacing columns for campaigns in playbook but not live (for transparency)."""
    out = df.copy()
    out["forecast_month_spend"] = 0.0
    out["pacing_delta_campaign"] = -out["monthly_budget_playbook"].astype(float)
    out["cpl_mtd"] = None
    out["performance_score"] = None
    out["performance_bucket"] = "n/a"
    out["allocation_delta_daily"] = 0.0
    out["recommended_daily_budget"] = 0.0
    out["recommended_daily_budget_capped"] = 0.0
    out["daily_budget_delta"] = 0.0
    out["pct_budget_change"] = 0.0
    out["allocation_share_pct"] = 0.0
    out["pipeline_amount"] = 0.0
    out["closed_won_amount"] = 0.0
    out["sql_count"] = 0.0
    out["roi_priority_weight"] = 0.0
    out["ctr_mtd"] = None
    out["cvr_mtd"] = None
    out["engagement_score"] = None
    out["conversion_score"] = None
    out["cost_score"] = None
    out["volume_score"] = None
    out["note"] = (
        "Not live this month — playbook dollars for this campaign are redistributed "
        "to live campaigns in the same channel (proportional to playbook share)."
    )
    if "platform_campaign_name" not in out.columns:
        out["platform_campaign_name"] = "—"
    else:
        out["platform_campaign_name"] = out["platform_campaign_name"].fillna("—")
    return out


def _portfolio_warnings(
    meta_df: pd.DataFrame,
    meta_s,
    google_df: pd.DataFrame,
    google_s,
) -> list[str]:
    w: list[str] = []
    tol = 0.05

    def check(name: str, df: pd.DataFrame, s):
        if df.empty:
            return
        mb = float(df["monthly_budget"].sum())
        if abs(mb - s.monthly_budget_total) > tol:
            w.append(f"{name}: monthly budget sum row check != summary ({mb} vs {s.monthly_budget_total})")
        # Channel forecast uses full-portfolio spend + daily budgets; row sum is playbook-only — do not compare.

    check("Meta", meta_df, meta_s)
    check("Google", google_df, google_s)

    # Portfolio: Meta TOTAL + Google TOTAL should match portfolio block (computed from summaries)
    if not meta_df.empty and not google_df.empty:
        tm = float(meta_df["recommended_daily_budget_capped"].sum())
        tg = float(google_df["recommended_daily_budget_capped"].sum())
        # informational only
        _ = tm + tg
    return w


def run_for_date(
    as_of: date,
    currency: str = "USD",
    *,
    use_live: bool | None = None,
    pipeline_report_path: str | None = None,
) -> Path:
    """Run pacing + allocation; write CSVs and Excel workbook."""
    if use_live is None:
        use_live = DEFAULT_USE_LIVE

    load_env_files()

    month_ctx = month_context_for(as_of)

    playbook = load_campaign_playbook()
    _ = load_campaign_mapping()  # validate file exists; mapping optional for v1 pacing

    as_of_str = as_of.isoformat()
    out_dir = resolve_repo_path(paths.daily_tracker_output_dir) / as_of_str
    out_dir.mkdir(parents=True, exist_ok=True)

    live_pull_succeeded = False
    live_api_warnings: list[str] = []
    live_full: pd.DataFrame | None = None
    if use_live:
        try:
            from live_portfolio_fetch import (  # noqa: WPS433
                build_live_snapshot_dataframe,
                build_snapshot_from_playbook_and_live,
            )

            live_full = build_live_snapshot_dataframe(as_of)
            warns = live_full.attrs.get("fetch_warnings") or []
            live_api_warnings = list(warns)
            for w in warns:
                print(f"[budget-tracker] Live pull warning: {w}")
            if "meta_account_spend_mtd" in live_full.attrs:
                print(
                    f"[budget-tracker] Meta account MTD spend (insights API): "
                    f"${float(live_full.attrs['meta_account_spend_mtd']):,.2f}"
                )
            if "meta_campaign_rows_spend_sum" in live_full.attrs:
                print(
                    f"[budget-tracker] Meta sum of campaign rows in pull: "
                    f"${float(live_full.attrs['meta_campaign_rows_spend_sum']):,.2f}"
                )
            raw_path = out_dir / f"live_portfolio_pull_{as_of_str}.csv"
            live_full.to_csv(raw_path, index=False)
            print(f"[budget-tracker] Wrote raw live pull: {raw_path}")
            snapshot = build_snapshot_from_playbook_and_live(playbook, live_full)
            snap_path = out_dir / f"campaign_snapshot_from_live_{as_of_str}.csv"
            snapshot.to_csv(snap_path, index=False)
            print(f"[budget-tracker] Wrote playbook-shaped snapshot: {snap_path}")
            live_pull_succeeded = True
        except Exception as e:
            print(f"[budget-tracker] Live pull failed ({e}); falling back to CSV snapshot.")
            live_full = None
            snapshot = load_campaign_snapshot()
    else:
        snapshot = load_campaign_snapshot()

    merged = merge_playbook_with_snapshot(playbook, snapshot, live_full=live_full)
    merged = apply_playbook_redistribution(merged)
    live_merged, nonlive_merged = split_live_and_nonlive(merged)

    # Channel-level pacing uses full-account spend + all campaign daily budgets from the live pull
    # (playbook-matched rows alone omit non-playbook spend).
    meta_kw: dict = {}
    google_kw: dict = {}
    if live_full is not None and not live_full.empty:
        from live_portfolio_fetch import platform_channel_totals  # noqa: WPS433

        ms, md = platform_channel_totals(live_full, "meta")
        if live_full.attrs.get("meta_account_spend_mtd") is not None:
            ms = float(live_full.attrs["meta_account_spend_mtd"])
        meta_kw["channel_spend_mtd_total"] = ms
        meta_kw["channel_daily_budget_sum"] = md
        gs, gd = platform_channel_totals(live_full, "google")
        google_kw["channel_spend_mtd_total"] = gs
        google_kw["channel_daily_budget_sum"] = gd
        print(
            "[budget-tracker] Channel totals (all campaigns in pull, incl. not in playbook): "
            f"Meta spend MTD=${ms:,.2f}, Σ daily (active campaigns, deduped)=${md:,.2f}; "
            f"Google spend MTD=${gs:,.2f}, Σ daily (ENABLED + shared-budget deduped)=${gd:,.2f}"
        )

    meta_raw, meta_s = build_channel_frame(
        live_merged, "meta", month_ctx, merged_all=merged, **meta_kw
    )
    google_raw, google_s = build_channel_frame(
        live_merged, "google", month_ctx, merged_all=merged, **google_kw
    )
    if pipeline_report_path:
        meta_raw = attach_pipeline_roi(meta_raw, pipeline_report_path) if not meta_raw.empty else meta_raw
        google_raw = (
            attach_pipeline_roi(google_raw, pipeline_report_path) if not google_raw.empty else google_raw
        )
        print(f"[budget-tracker] Applied ROI weighting from pipeline report: {pipeline_report_path}")

    meta_df = allocate_channel(meta_raw, meta_s, allocation_config) if not meta_raw.empty else meta_raw
    google_df = (
        allocate_channel(google_raw, google_s, allocation_config)
        if not google_raw.empty
        else google_raw
    )

    total_target = 0.0
    if not meta_df.empty:
        total_target += float(meta_df["recommended_daily_budget_capped"].sum())
    if not google_df.empty:
        total_target += float(google_df["recommended_daily_budget_capped"].sum())

    warnings = _portfolio_warnings(meta_df, meta_s, google_df, google_s)
    if live_api_warnings:
        warnings.extend(live_api_warnings)
    if not nonlive_merged.empty:
        by_plat = nonlive_merged.groupby("platform")["monthly_budget_playbook"].sum()
        warnings.append(
            "Non-live playbook $ (reallocated to live in-channel): "
            + ", ".join(f"{p}=${v:,.0f}" for p, v in by_plat.items())
        )

    # Combined CSV: live pacing rows + non-live playbook rows (transparency)
    combined: pd.DataFrame | None = None
    pieces = [df for df in (meta_df, google_df) if df is not None and not df.empty]
    if not nonlive_merged.empty:
        pieces.append(_annotate_nonlive_rows(nonlive_merged))
    if pieces:
        combined = pd.concat(pieces, ignore_index=True)
        write_daily_tracker(combined, as_of_str, output_dir=out_dir)
        changes = combined[
            combined["daily_budget_delta"].abs() > 0.01
        ].copy() if "daily_budget_delta" in combined.columns else pd.DataFrame()
        write_budget_changes(changes, as_of_str, output_dir=out_dir)

    xlsx_path = out_dir / f"paid_ads_budget_pacing_{as_of_str}.xlsx"
    write_pacing_workbook(
        xlsx_path,
        as_of,
        currency,
        meta_df,
        meta_s,
        google_df,
        google_s,
        total_target_daily=total_target,
        portfolio_warnings=warnings or None,
    )

    # Markdown analysis (targets, state, recommendations, artifact index)
    _root = workspace_root().resolve()

    def _rel(p: Path) -> str:
        rp = p.resolve()
        try:
            return str(rp.relative_to(_root))
        except ValueError:
            return str(rp)

    artifacts: dict[str, str] = {
        "Pacing workbook (Excel)": _rel(out_dir / f"paid_ads_budget_pacing_{as_of_str}.xlsx"),
        "Campaign playbook (input)": _rel(resolve_repo_path(paths.campaign_playbook)),
    }
    if combined is not None:
        artifacts["Combined campaign table (CSV)"] = _rel(out_dir / f"daily_budget_tracker_{as_of_str}.csv")
        artifacts["Material budget changes only (CSV)"] = _rel(
            out_dir / f"proposed_budget_changes_{as_of_str}.csv"
        )
    if live_pull_succeeded:
        artifacts["Raw live portfolio pull (CSV)"] = _rel(out_dir / f"live_portfolio_pull_{as_of_str}.csv")
        artifacts["Snapshot matched to playbook (CSV)"] = _rel(
            out_dir / f"campaign_snapshot_from_live_{as_of_str}.csv"
        )
    else:
        artifacts["Campaign snapshot (CSV input)"] = _rel(resolve_repo_path(paths.campaign_snapshot))

    md_path = out_dir / f"budget_pacing_analysis_{as_of_str}.md"
    artifacts["Analysis summary (Markdown)"] = _rel(md_path)
    write_analysis_markdown(
        md_path,
        as_of,
        currency,
        month_ctx,
        playbook,
        merged,
        combined,
        meta_df,
        google_df,
        meta_s,
        google_s,
        nonlive_merged,
        warnings,
        artifacts,
        live_pull_succeeded=live_pull_succeeded,
    )

    return xlsx_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paid ads budget pacing tracker")
    parser.add_argument(
        "--no-live",
        action="store_true",
        help="Do not call Meta/Google APIs; use campaign_snapshot_latest.csv only.",
    )
    parser.add_argument(
        "--as-of",
        type=str,
        default=os.environ.get("BUDGET_PACING_AS_OF", date.today().isoformat()),
        help="ISO date (default: today or BUDGET_PACING_AS_OF)",
    )
    parser.add_argument(
        "--pipeline-report",
        type=str,
        default=os.environ.get("PAID_ADS_PIPELINE_REPORT_PATH", "").strip() or None,
        help="Path to paid ads opportunity report XLSX for ROI-prioritized redistribution weighting.",
    )
    args = parser.parse_args()
    as_of_d = date.fromisoformat(args.as_of)
    p = run_for_date(as_of_d, use_live=not args.no_live, pipeline_report_path=args.pipeline_report)
    print(f"Wrote: {p}")
    md = (
        resolve_repo_path(paths.daily_tracker_output_dir)
        / as_of_d.isoformat()
        / f"budget_pacing_analysis_{as_of_d.isoformat()}.md"
    )
    print(f"Wrote: {md}")
