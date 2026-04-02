from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm_str(v: object) -> str:
    return str(v or "").strip()


def _normalize_utm_campaign(v: object) -> str:
    s = _norm_str(v)
    if not s or s.lower() == "brand":
        return ""
    if s.lower() in {"{campaign_name}", "campaign_name"}:
        return "__PMAX_PLACEHOLDER__"
    if s.isdigit() and len(s) >= 4:
        return "__PMAX_PLACEHOLDER__"
    if " - " in s and s.rsplit(" - ", 1)[-1].isdigit():
        s = s.rsplit(" - ", 1)[0].strip()
    return s


def _actions_to_map(actions: object) -> dict[str, float]:
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


def _pick_results(actions_map: dict[str, float], preferred_action: str) -> float:
    """
    Pick a single 'results' proxy similar to the intelligence agent logic.
    Prefer lead-ish actions; otherwise 0.
    """
    preferred = (preferred_action or "").strip()
    if preferred and preferred in actions_map:
        return float(actions_map.get(preferred) or 0.0)
    # Common fallback when a custom-event label is configured but exported under generic custom action.
    if preferred.endswith("lead_email-valid") and "offsite_conversion.fb_pixel_custom" in actions_map:
        return float(actions_map.get("offsite_conversion.fb_pixel_custom") or 0.0)

    for k in (
        "lead",
        "offsite_conversion.fb_pixel_lead",
        "offsite_conversion.fb_pixel_complete_registration",
        "onsite_conversion.total_messaging_connection",
        "offsite_conversion.fb_pixel_custom",
    ):
        if k in actions_map:
            return float(actions_map.get(k) or 0.0)
    return 0.0


def _insights_rows_to_df(insights: dict[str, Any], *, preferred_action: str) -> pd.DataFrame:
    rows = insights.get("insights") or []
    if not isinstance(rows, list):
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    # numeric conversions
    for c in ("spend", "impressions", "clicks", "ctr"):
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0.0)
    out["actions_map"] = out.get("actions", None).apply(_actions_to_map)
    out["results"] = out["actions_map"].apply(lambda m: _pick_results(m, preferred_action))
    return out


def _asset_breakdown_df(path: Path, asset_key: str, *, preferred_action: str) -> pd.DataFrame:
    d = _read_json(path)
    df = _insights_rows_to_df(d, preferred_action=preferred_action)
    if df.empty:
        return df
    if asset_key in df.columns:
        df = df.rename(columns={asset_key: "asset_raw"})
    else:
        df["asset_raw"] = None

    def asset_text(v: object) -> str:
        if isinstance(v, dict):
            # Most common breakdown payloads
            for k in ("text", "name", "title"):
                if v.get(k):
                    return str(v.get(k)).strip()
            # Fallback: json dump
            return json.dumps(v, ensure_ascii=False)
        if isinstance(v, list):
            return json.dumps(v, ensure_ascii=False)
        return _norm_str(v)

    df["asset"] = df["asset_raw"].map(asset_text)
    return df


def _write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ads_json", required=True, help="meta list_ads output json")
    p.add_argument("--ad_insights_json", required=True, help="meta ad-level insights json")
    p.add_argument("--body_json", required=True, help="meta body_asset breakdown json")
    p.add_argument("--title_json", required=True, help="meta title_asset breakdown json")
    p.add_argument("--cta_json", required=True, help="meta call_to_action_asset breakdown json")
    p.add_argument("--image_json", required=True, help="meta image_asset breakdown json")
    p.add_argument("--video_json", required=True, help="meta video_asset breakdown json")
    p.add_argument("--roi_csv", required=True, help="roi_weights_by_utm_campaign.csv")
    p.add_argument(
        "--meta_result_action",
        default="offsite_conversion.fb_pixel_custom.lead_email-valid",
        help="Meta action_type to treat as primary result",
    )
    p.add_argument("--out_md", default="docs/context_repository/paid_ads/winning_angles/meta_mar2026_onward.md")
    args = p.parse_args()

    ads = _read_json(Path(args.ads_json)).get("ads") or []
    ads_df = pd.json_normalize(ads)
    # Standardize columns we care about
    keep = {
        "id": "ad_id",
        "name": "ad_name",
        "campaign_id": "campaign_id",
        "adset_id": "adset_id",
        "creative.id": "creative_id",
        "creative.body": "creative_body",
        "ad_copy_preview.body": "creative_body_preview",
        "creative.title": "creative_title",
        "creative.name": "creative_name",
    }
    for src, dst in keep.items():
        if src in ads_df.columns and dst not in ads_df.columns:
            ads_df = ads_df.rename(columns={src: dst})
    for c in ("ad_id", "campaign_id", "adset_id", "creative_id"):
        if c in ads_df.columns:
            ads_df[c] = ads_df[c].map(_norm_str)
    # Prefer explicit creative.body; fall back to ad_copy_preview.body.
    if "creative_body" in ads_df.columns and "creative_body_preview" in ads_df.columns:
        ads_df["creative_body"] = ads_df["creative_body"].where(
            ads_df["creative_body"].notna() & (ads_df["creative_body"].astype(str).str.strip() != ""),
            ads_df["creative_body_preview"],
        )

    ad_insights = _insights_rows_to_df(
        _read_json(Path(args.ad_insights_json)),
        preferred_action=args.meta_result_action,
    )
    if "ad_id" in ad_insights.columns:
        ad_insights["ad_id"] = ad_insights["ad_id"].map(_norm_str)

    roi = pd.read_csv(args.roi_csv)
    roi = roi[roi["utm_source"] == "meta"].copy()
    roi["utm_campaign_norm"] = roi["utm_campaign_norm"].map(_normalize_utm_campaign)

    # Join campaign_name -> ROI will be done later (requires campaign_name in insights).
    # For now, we attach ROI by matching utm_campaign_norm to campaign_id if it looks like playbook id.
    # This is intentionally conservative.
    ad_joined = ad_insights.merge(ads_df, on="ad_id", how="left")

    # Aggregate asset breakdowns: top by results then spend
    body_df = _asset_breakdown_df(Path(args.body_json), "body_asset", preferred_action=args.meta_result_action)
    title_df = _asset_breakdown_df(Path(args.title_json), "title_asset", preferred_action=args.meta_result_action)
    cta_df = _asset_breakdown_df(Path(args.cta_json), "call_to_action_asset", preferred_action=args.meta_result_action)
    image_df = _asset_breakdown_df(Path(args.image_json), "image_asset", preferred_action=args.meta_result_action)
    video_df = _asset_breakdown_df(Path(args.video_json), "video_asset", preferred_action=args.meta_result_action)

    def top_assets(df: pd.DataFrame, label: str, n: int = 25) -> str:
        if df.empty:
            return "- (no data)"
        g = (
            df.groupby("asset", dropna=False)[["spend", "impressions", "clicks", "results"]]
            .sum()
            .reset_index()
            .sort_values(["results", "spend", "clicks", "impressions"], ascending=False)
        )
        out = []
        for _, r in g.head(n).iterrows():
            a = str(r.get("asset") or "").strip()
            if not a:
                continue
            out.append(
                f"- **{label}**: “{a}” — results={float(r.get('results',0)):.0f}, "
                f"spend=${float(r.get('spend',0)):.2f}, clicks={int(r.get('clicks',0))}, impr={int(r.get('impressions',0))}"
            )
        return "\n".join(out) if out else "- (no assets parsed)"

    # Top ads by results then spend
    ad_rank = (
        ad_joined.groupby(["ad_id", "ad_name", "creative_id", "creative_title", "creative_body"], dropna=False)[
            ["spend", "impressions", "clicks", "results"]
        ]
        .sum()
        .reset_index()
        .sort_values(["results", "spend", "clicks"], ascending=False)
    )

    def fmt_top_ads(df: pd.DataFrame, n: int = 15) -> str:
        out = []
        for _, r in df.head(n).iterrows():
            out.append(
                f"- ad_id={r.get('ad_id')} spend=${float(r.get('spend',0)):.2f} results={float(r.get('results',0)):.0f} "
                f"clicks={int(r.get('clicks',0))} impr={int(r.get('impressions',0))}\n"
                f"  - title: {str(r.get('creative_title') or '').strip()}\n"
                f"  - body: {str(r.get('creative_body') or '').strip()}"
            )
        return "\n".join(out) if out else "- (no ads ranked)"

    md = f"""
## Meta — Winning angles (Mar 2026 onward)

### ROI-heavy campaign keys (from Salesforce)
Top by `roi_priority_weight = pipeline + 2× closed_won`:

{roi.sort_values('roi_priority_weight', ascending=False).head(20).to_string(index=False)}

### Top ads by platform results (ad-level insights)
{fmt_top_ads(ad_rank, 20)}

### Top copy assets (breakdowns)

#### Primary text (body_asset)
{top_assets(body_df, 'body_asset', 30)}

#### Headlines (title_asset)
{top_assets(title_df, 'title_asset', 30)}

#### CTA (call_to_action_asset)
{top_assets(cta_df, 'call_to_action_asset', 30)}

#### Images (image_asset)
{top_assets(image_df, 'image_asset', 25)}

#### Videos (video_asset)
{top_assets(video_df, 'video_asset', 25)}

### Notes / gaps
- The current Meta MCP insights are aggregated at `2026-03-01 → 2026-03-25` (not per-day). Next iteration: pull **daily** by adding time breakdowns or looping date ranges.
- ROI join to Meta campaigns is not yet robust because Meta insights here do not include UTM tags; we’ll map ROI to campaigns via playbook `campaign_id`/naming conventions (as budget tracker does) and/or click-id joins (`fbclid`) where possible.
- Primary result action configured: `{args.meta_result_action}` (falls back to `offsite_conversion.fb_pixel_custom` when label-specific custom events are exported generically).
"""
    _write_md(Path(args.out_md), md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

