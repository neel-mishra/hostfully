from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Inputs:
    roi_weights_csv: Path
    meta_insights_json: Path
    google_rsa_asset_table: Path


def _read_google_table(path: Path) -> pd.DataFrame:
    """
    The google ads MCP tools often return an ASCII table saved to a .txt file.
    We parse it by locating the header separator line and then splitting on '|'.
    """
    txt = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    # Find header row (contains '|') and a divider line after it.
    header_idx = None
    for i, line in enumerate(txt[:50]):
        if "campaign.resourceName" in line and "|" in line:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find Google table header in file")

    header = [h.strip() for h in txt[header_idx].split("|")]
    data_lines = []
    for line in txt[header_idx + 2 :]:  # skip divider line
        if not line.strip():
            continue
        if line.startswith("---"):
            continue
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != len(header):
            continue
        data_lines.append(parts)

    df = pd.DataFrame(data_lines, columns=header)
    return df


def _read_meta_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_google_angles(roi: pd.DataFrame, google_assets: pd.DataFrame) -> str:
    roi_g = roi[roi["utm_source"] == "google"].copy()
    roi_g = roi_g.sort_values("roi_priority_weight", ascending=False)
    top_roi = roi_g.head(20)

    # Pull top text assets by conversions then clicks.
    ga = google_assets.copy()
    # numeric casts
    for c in ["metrics.clicks", "metrics.conversions", "metrics.impressions"]:
        if c in ga.columns:
            ga[c] = pd.to_numeric(ga[c], errors="coerce").fillna(0.0)
    if "metrics.ctr" in ga.columns:
        ga["metrics.ctr"] = pd.to_numeric(ga["metrics.ctr"], errors="coerce").fillna(0.0)

    # Keep only headline/description
    keep = ga["adGroupAdAssetView.fieldType"].isin({"HEADLINE", "DESCRIPTION"})
    ga = ga[keep].copy()
    ga = ga.sort_values(["metrics.conversions", "metrics.clicks", "metrics.impressions"], ascending=False)

    # Attach a rough campaign join: campaign.name equals utm_campaign_norm in SF when present.
    if "campaign.name" in ga.columns and "utm_campaign_norm" in roi_g.columns:
        ga = ga.merge(
            roi_g[["utm_campaign_norm", "roi_priority_weight"]],
            left_on="campaign.name",
            right_on="utm_campaign_norm",
            how="left",
        )
    ga["roi_priority_weight"] = pd.to_numeric(ga.get("roi_priority_weight", 0.0), errors="coerce").fillna(0.0)

    def fmt_rows(df: pd.DataFrame, n: int) -> str:
        out = []
        for _, r in df.head(n).iterrows():
            txt = str(r.get("asset.textAsset.text") or "").strip()
            if not txt:
                continue
            out.append(
                f"- **{r.get('adGroupAdAssetView.fieldType','')}**: “{txt}” — "
                f"clicks={int(r.get('metrics.clicks',0))}, conv={float(r.get('metrics.conversions',0)):.2f}, "
                f"impr={int(r.get('metrics.impressions',0))}"
            )
        return "\n".join(out) if out else "- (no rows parsed)"

    return f"""
## Google Ads — Winning angles (Mar 2026 onward)

### ROI-heavy campaigns (from Salesforce, Mar 2026 onward)
Top by `roi_priority_weight = pipeline + 2× closed_won`:

{top_roi.to_string(index=False)}

### Top-performing RSA text assets (30d lookback; filter to Mar 2026 onward downstream)

These are ranked by conversions then clicks from the MCP RSA asset view pull.

#### Headlines
{fmt_rows(ga[ga['adGroupAdAssetView.fieldType']=='HEADLINE'], 25)}

#### Descriptions
{fmt_rows(ga[ga['adGroupAdAssetView.fieldType']=='DESCRIPTION'], 25)}

### Notes / gaps
- ROI join is exact-match on `utm_campaign_norm` ⇄ `campaign.name` for now. We’ll improve mapping using `gclid` joins and campaign normalization rules (`__PMAX_PLACEHOLDER__`).
"""


def build_meta_angles(roi: pd.DataFrame, meta: dict) -> str:
    roi_m = roi[roi["utm_source"] == "meta"].copy().sort_values("roi_priority_weight", ascending=False)
    perf = meta.get("performance") or {}
    primary = meta.get("primary_result") or {}
    conv = meta.get("conversion_action") or {}

    return f"""
## Meta — Winning angles (Mar 2026 onward)

### ROI-heavy campaigns (from Salesforce, Mar 2026 onward)
Top by `roi_priority_weight = pipeline + 2× closed_won`:

{roi_m.head(20).to_string(index=False)}

### Platform performance snapshot (Meta MCP insights pull)
- **Date range**: {perf.get('date_range', {}).get('start')} → {perf.get('date_range', {}).get('end')}
- **Spend**: {perf.get('total_spend')}
- **Impressions**: {perf.get('total_impressions')}
- **Clicks**: {perf.get('total_clicks')}
- **Avg CTR**: {perf.get('average_ctr')}
- **Avg CPC**: {perf.get('average_cpc')}
- **Avg CPM**: {perf.get('average_cpm')}
- **Avg Frequency**: {perf.get('average_frequency')}
- **Primary result**: {primary.get('results')} @ {primary.get('cost_per_result')} ({primary.get('label')})

### Notes / next extraction step
- This snapshot contains **ad-level performance + breakdowns**, but not full creative text (primary/headline/description) for each ad.
- Next we’ll pull **creative objects** (or map ad_id → creative_id) and attach:
  - Primary text, headline, description, CTA
  - Creative type (image/video)
  - Winning-by-ROI segments
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--roi", required=True, help="ROI weights CSV (from salesforce_ingest.py)")
    p.add_argument("--meta_insights", required=True, help="Meta insights JSON snapshot (agent-tools file)")
    p.add_argument("--google_rsa_assets", required=True, help="Google RSA asset performance table txt (agent-tools file)")
    p.add_argument("--out_dir", default="docs/context_repository/paid_ads/winning_angles", help="Output dir for md files")
    p.add_argument(
        "--tables_out_dir",
        default="outputs/training_data/paid_ads/joined",
        help="Output dir for joined tables (csv)",
    )
    args = p.parse_args()

    roi = pd.read_csv(args.roi)
    meta = _read_meta_json(Path(args.meta_insights))
    google_assets = _read_google_table(Path(args.google_rsa_assets))

    out_dir = Path(args.out_dir)
    _write_md(out_dir / "meta_mar2026_onward.md", build_meta_angles(roi, meta))
    _write_md(out_dir / "google_mar2026_onward.md", build_google_angles(roi, google_assets))

    # Write joined tables (lightweight CSVs) for downstream iteration.
    tables_out = Path(args.tables_out_dir)
    tables_out.mkdir(parents=True, exist_ok=True)

    roi_g = roi[roi["utm_source"] == "google"].copy()
    google_joined = google_assets.copy()
    if "campaign.name" in google_joined.columns and "utm_campaign_norm" in roi_g.columns:
        google_joined = google_joined.merge(
            roi_g[["utm_campaign_norm", "roi_priority_weight"]],
            left_on="campaign.name",
            right_on="utm_campaign_norm",
            how="left",
        )
    google_joined.to_csv(tables_out / "google_rsa_assets_with_roi.csv", index=False)

    roi_m = roi[roi["utm_source"] == "meta"].copy()
    roi_m.to_csv(tables_out / "meta_roi_weights.csv", index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

