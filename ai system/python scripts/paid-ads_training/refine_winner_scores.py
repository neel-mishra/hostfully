from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def _norm(v: object) -> str:
    return str(v or "").strip()


def _norm_campaign(v: object) -> str:
    s = _norm(v)
    if " - " in s and s.rsplit(" - ", 1)[-1].isdigit():
        s = s.rsplit(" - ", 1)[0].strip()
    if s.lower() in {"{campaign_name}", "campaign_name"}:
        return "__PMAX_PLACEHOLDER__"
    return s


def _platform_from_source(v: object) -> str:
    s = _norm(v).lower()
    if "meta" in s or s in {"fb", "ig", "facebook", "instagram"}:
        return "meta"
    if "google" in s:
        return "google"
    return s


def _actions_map(actions: object) -> dict[str, float]:
    out: dict[str, float] = {}
    if not isinstance(actions, list):
        return out
    for a in actions:
        if not isinstance(a, dict):
            continue
        t = str(a.get("action_type") or "").strip()
        if not t:
            continue
        try:
            v = float(a.get("value") or 0.0)
        except Exception:
            v = 0.0
        out[t] = out.get(t, 0.0) + v
    return out


def _meta_result(actions: dict[str, float], preferred: str) -> float:
    if preferred in actions:
        return float(actions.get(preferred) or 0.0)
    if preferred.endswith("lead_email-valid") and "offsite_conversion.fb_pixel_custom" in actions:
        return float(actions.get("offsite_conversion.fb_pixel_custom") or 0.0)
    return float(actions.get("lead") or 0.0)


def _normalize_series(s: pd.Series, clip_low: float = 0.25, clip_high: float = 4.0) -> pd.Series:
    pos = s[s > 0]
    if pos.empty:
        return pd.Series(1.0, index=s.index)
    med = float(pos.median())
    if med <= 0:
        return pd.Series(1.0, index=s.index)
    return (s / med).replace([float("inf"), float("-inf")], 1.0).fillna(1.0).clip(clip_low, clip_high)


def refine_meta(
    ads_json: Path,
    campaigns_json: Path,
    ad_insights_json: Path,
    roi_csv: Path,
    preferred_action: str,
    min_impr: int,
    min_clicks: int,
    min_results: float,
    strict_mode: bool,
) -> pd.DataFrame:
    ads = json.loads(ads_json.read_text(encoding="utf-8")).get("ads") or []
    ads_df = pd.json_normalize(ads)
    campaigns = json.loads(campaigns_json.read_text(encoding="utf-8")).get("campaigns") or []
    camp_df = pd.DataFrame(campaigns)
    if not camp_df.empty:
        if "id" in camp_df.columns and "campaign_id" not in camp_df.columns:
            camp_df = camp_df.rename(columns={"id": "campaign_id"})
        if "name" in camp_df.columns and "campaign_name" not in camp_df.columns:
            camp_df = camp_df.rename(columns={"name": "campaign_name"})
        for c in ("campaign_id", "campaign_name"):
            if c in camp_df.columns:
                camp_df[c] = camp_df[c].map(_norm)
    keep = {
        "id": "ad_id",
        "campaign_id": "campaign_id",
        "name": "ad_name",
        "creative.body": "body",
        "ad_copy_preview.body": "body_preview",
        "creative.title": "title",
    }
    for src, dst in keep.items():
        if src in ads_df.columns and dst not in ads_df.columns:
            ads_df = ads_df.rename(columns={src: dst})
    if "body" in ads_df.columns and "body_preview" in ads_df.columns:
        ads_df["body"] = ads_df["body"].where(
            ads_df["body"].notna() & (ads_df["body"].astype(str).str.strip() != ""),
            ads_df["body_preview"],
        )
    for c in ("ad_id", "campaign_id"):
        if c in ads_df.columns:
            ads_df[c] = ads_df[c].map(_norm)

    rows = json.loads(ad_insights_json.read_text(encoding="utf-8")).get("insights") or []
    m = pd.DataFrame(rows)
    for c in ("ad_id", "campaign_id", "campaign_name"):
        if c in m.columns:
            m[c] = m[c].map(_norm)
    for c in ("spend", "impressions", "clicks", "ctr"):
        if c in m.columns:
            m[c] = pd.to_numeric(m[c], errors="coerce").fillna(0.0)
    m["actions_map"] = m.get("actions", None).apply(_actions_map)
    m["results"] = m["actions_map"].apply(lambda a: _meta_result(a, preferred_action))
    m["perf_eff"] = m.apply(lambda r: (r["results"] / r["spend"]) if float(r["spend"]) > 0 else 0.0, axis=1)
    m["perf_signal"] = 0.7 * _normalize_series(m["perf_eff"]) + 0.3 * _normalize_series(m["ctr"])

    roi = pd.read_csv(roi_csv)
    roi = roi.copy()
    roi["utm_source"] = roi["utm_source"].map(_platform_from_source)
    roi = roi[roi["utm_source"] == "meta"].copy()
    roi["utm_campaign_norm"] = roi["utm_campaign_norm"].map(_norm_campaign)
    # Map campaign_id -> campaign_name then join to ROI keys by normalized name.
    if not camp_df.empty and "campaign_id" in m.columns:
        m = m.merge(camp_df[["campaign_id", "campaign_name"]], on="campaign_id", how="left")
    if "campaign_name" not in m.columns:
        m["campaign_name"] = ""
    m["campaign_name_norm"] = m["campaign_name"].map(_norm_campaign)
    m = m.merge(
        roi[["utm_campaign_norm", "roi_priority_weight"]],
        left_on="campaign_name_norm",
        right_on="utm_campaign_norm",
        how="left",
    )
    m["roi_priority_weight"] = pd.to_numeric(m["roi_priority_weight"], errors="coerce").fillna(0.0)
    m["roi_norm"] = _normalize_series(m["roi_priority_weight"])
    m["blended_score"] = 0.85 * m["roi_norm"] + 0.15 * m["perf_signal"]

    m = m[(m["impressions"] >= min_impr) & (m["clicks"] >= min_clicks) & (m["results"] >= min_results)].copy()
    if strict_mode:
        m = m[(m["ctr"] >= 0.7) & (m["perf_eff"] >= m["perf_eff"].median())].copy()
    m = m.merge(ads_df[["ad_id", "ad_name", "body", "title"]], on="ad_id", how="left")
    if "ad_name_x" in m.columns or "ad_name_y" in m.columns:
        m["ad_name"] = m.get("ad_name_x").fillna(m.get("ad_name_y"))
    return m.sort_values(["blended_score", "results", "spend"], ascending=False)


def refine_google(
    google_joined_csv: Path,
    min_impr: int,
    min_clicks: int,
    min_results: float,
    strict_mode: bool,
    google_strict_ctr_min: float,
) -> pd.DataFrame:
    g = pd.read_csv(google_joined_csv)
    for c in ("metrics.clicks", "metrics.conversions", "metrics.impressions", "metrics.ctr", "roi_priority_weight"):
        if c in g.columns:
            g[c] = pd.to_numeric(g[c], errors="coerce").fillna(0.0)
    g["perf_eff"] = g.apply(
        lambda r: (float(r.get("metrics.conversions", 0.0)) / float(r.get("metrics.clicks", 0.0)))
        if float(r.get("metrics.clicks", 0.0)) > 0
        else 0.0,
        axis=1,
    )
    g["perf_signal"] = 0.7 * _normalize_series(g["perf_eff"]) + 0.3 * _normalize_series(g["metrics.ctr"])
    g["roi_norm"] = _normalize_series(g["roi_priority_weight"])
    g["blended_score"] = 0.85 * g["roi_norm"] + 0.15 * g["perf_signal"]
    g = g[
        (g["metrics.impressions"] >= min_impr)
        & (g["metrics.clicks"] >= min_clicks)
        & (g["metrics.conversions"] >= min_results)
    ].copy()
    if strict_mode:
        g = g[(g["metrics.ctr"] >= google_strict_ctr_min) & (g["perf_eff"] >= g["perf_eff"].median())].copy()
    return g.sort_values(["blended_score", "metrics.conversions", "metrics.clicks"], ascending=False)


def write_top10(meta_df: pd.DataFrame, google_df: pd.DataFrame, out_path: Path) -> None:
    lines: list[str] = []
    lines.append("## Top 10 Reusable Angles (Mar 2026 onward)")
    lines.append("")
    lines.append("Scoring: 85% ROI (`pipeline + 2×closed_won`) + 15% performance (efficiency + engagement).")
    lines.append("")
    lines.append("### Meta")
    m = meta_df.head(5)
    for _, r in m.iterrows():
        lines.append(
            f"- blended={r['blended_score']:.2f} | results={float(r['results']):.0f} | "
            f"ctr={float(r['ctr']):.4f} | ad={r.get('ad_name','')} | "
            f"title={str(r.get('title') or '').strip()[:80]} | body={str(r.get('body') or '').strip()[:140]}"
        )
    lines.append("")
    lines.append("### Google")
    g = google_df.head(5)
    for _, r in g.iterrows():
        lines.append(
            f"- blended={r['blended_score']:.2f} | conv={float(r.get('metrics.conversions',0)):.2f} | "
            f"ctr={float(r.get('metrics.ctr',0)):.4f} | field={r.get('adGroupAdAssetView.fieldType','')} | "
            f"asset={str(r.get('asset.textAsset.text') or '').strip()[:140]}"
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_strict_winners(meta_df: pd.DataFrame, google_df: pd.DataFrame, out_path: Path) -> None:
    lines: list[str] = []
    lines.append("## Strict Winners Only (Mar 2026 onward)")
    lines.append("")
    lines.append("This file uses elevated confidence bands and minimum-result gates for production prompting.")
    lines.append("")
    lines.append("### Meta strict winners")
    if meta_df.empty:
        lines.append("- No rows met strict confidence criteria.")
    else:
        for _, r in meta_df.head(10).iterrows():
            lines.append(
                f"- blended={r['blended_score']:.2f} | results={float(r['results']):.0f} | ctr={float(r['ctr']):.4f} | "
                f"ad={r.get('ad_name','')} | body={str(r.get('body') or '').strip()[:150]}"
            )
    lines.append("")
    lines.append("### Google strict winners")
    if google_df.empty:
        lines.append("- No rows met strict confidence criteria.")
    else:
        for _, r in google_df.head(10).iterrows():
            lines.append(
                f"- blended={r['blended_score']:.2f} | conv={float(r.get('metrics.conversions',0)):.2f} | "
                f"ctr={float(r.get('metrics.ctr',0)):.4f} | field={r.get('adGroupAdAssetView.fieldType','')} | "
                f"asset={str(r.get('asset.textAsset.text') or '').strip()[:150]}"
            )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--meta_ads_json", required=True)
    p.add_argument("--meta_campaigns_json", required=True)
    p.add_argument("--meta_ad_insights_json", required=True)
    p.add_argument("--roi_csv", required=True)
    p.add_argument("--google_joined_csv", required=True)
    p.add_argument("--meta_result_action", default="offsite_conversion.fb_pixel_custom.lead_email-valid")
    p.add_argument("--min_impressions", type=int, default=1000)
    p.add_argument("--min_clicks", type=int, default=20)
    p.add_argument("--min_results", type=float, default=1.0)
    p.add_argument(
        "--min_results_google",
        type=float,
        default=None,
        help="Minimum conversions for Google only; defaults to --min_results when omitted.",
    )
    p.add_argument("--strict_mode", action="store_true")
    p.add_argument("--google_strict_ctr_min", type=float, default=0.03)
    p.add_argument("--out_dir", default="outputs/training_data/paid_ads/joined")
    p.add_argument(
        "--top10_out",
        default="docs/context_repository/paid_ads/winning_angles/top10_reusable_angles_mar2026_onward.md",
    )
    p.add_argument(
        "--strict_out",
        default="docs/context_repository/paid_ads/winning_angles/strict_winners_mar2026_onward.md",
    )
    args = p.parse_args()

    meta_df = refine_meta(
        Path(args.meta_ads_json),
        Path(args.meta_campaigns_json),
        Path(args.meta_ad_insights_json),
        Path(args.roi_csv),
        args.meta_result_action,
        args.min_impressions,
        args.min_clicks,
        args.min_results,
        args.strict_mode,
    )
    google_min_results = (
        args.min_results_google if args.min_results_google is not None else args.min_results
    )
    google_df = refine_google(
        Path(args.google_joined_csv),
        args.min_impressions,
        args.min_clicks,
        google_min_results,
        args.strict_mode,
        args.google_strict_ctr_min,
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_df.to_csv(out_dir / "meta_ads_refined_scored.csv", index=False)
    google_df.to_csv(out_dir / "google_assets_refined_scored.csv", index=False)
    write_top10(meta_df, google_df, Path(args.top10_out))
    write_strict_winners(meta_df, google_df, Path(args.strict_out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

