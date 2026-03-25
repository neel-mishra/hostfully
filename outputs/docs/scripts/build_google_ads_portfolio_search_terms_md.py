#!/usr/bin/env python3
"""Build markdown: one table per ENABLED campaign (search terms, LAST_7_DAYS, cost > $1, targeting NONE)."""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

# All ENABLED campaigns in account 2565189582 (Hostfully) at export time — includes campaigns with no matching rows.
ENABLED_CAMPAIGNS: list[tuple[int, str, str]] = [
    (23139103905, "[Rede de Display] | hostfully | pt-br", "DISPLAY"),
    (23144283317, "[Rede de Pesquisa] | hostfully | pt-br", "SEARCH"),
    (23619221250, "au-uk_brand_search", "SEARCH"),
    (23619267350, "ca-us_pms_pmax", "PERFORMANCE_MAX"),
    (23619357777, "au-uk_pms_pmax", "PERFORMANCE_MAX"),
    (23622401230, "ca-us_brand_search", "SEARCH"),
    (23657942340, "ca-us_pms_search", "SEARCH"),
    (23658078636, "au-uk_pms_search", "SEARCH"),
]


def usd_micros(x: str | None) -> str:
    if x is None or x == "":
        return "—"
    return f"${float(x) / 1e6:.2f}"


def pct(x: str | None) -> str:
    if x is None or x == "":
        return "—"
    return f"{float(x) * 100:.2f}%"


def usd_currency(x: str | None) -> str:
    if x is None or x == "":
        return "—"
    return f"${float(x):.2f}"


def table_for_rows(rows: list[dict]) -> str:
    lines = [
        "| # | Search term | Impr. | Clicks | CTR | Interact. | Int. rate | Cost | Avg. CPC | Conv. | Conv. value | Cost / conv. | Value / conv. |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i, row in enumerate(rows, 1):
        clicks = int(row["metrics.clicks"])
        conv = float(row["metrics.conversions"] or 0)
        vpc = row.get("metrics.valuePerConversion")
        cost = float(row["metrics.costMicros"])
        cpc = float(row["metrics.averageCpc"] or 0)
        cpa = row.get("metrics.costPerConversion")
        cv = float(row["metrics.conversionsValue"] or 0)
        val_conv = usd_currency(vpc) if conv else "—"
        lines.append(
            f"| {i} | {row['campaignSearchTermView.searchTerm']} | {row['metrics.impressions']} | {clicks} | "
            f"{pct(row['metrics.ctr'])} | {row['metrics.interactions']} | {pct(row['metrics.interactionRate'])} | "
            f"{usd_micros(str(cost))} | {usd_micros(str(cpc))} | {conv:g} | {cv:g} | "
            f"{usd_micros(cpa) if cpa else '—'} | {val_conv} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: build_google_ads_portfolio_search_terms_md.py <input.csv> <output.md>", file=sys.stderr)
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    rows = list(csv.DictReader(inp.open(newline="", encoding="utf-8")))
    by_id: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_id[str(r["campaign.id"])].append(r)
    for k in by_id:
        by_id[k].sort(key=lambda r: -float(r["metrics.costMicros"]))

    total_cost = sum(float(r["metrics.costMicros"]) for r in rows) / 1e6
    total_conv = sum(float(r["metrics.conversions"] or 0) for r in rows)
    total_cv = sum(float(r["metrics.conversionsValue"] or 0) for r in rows)

    lines: list[str] = []
    lines.append("# Google Ads portfolio — search terms by campaign\n\n")
    lines.append("Account: **Hostfully** (`2565189582`) · Currency: **USD** · Time zone: **America/Los_Angeles**\n\n")
    lines.append("**Scope:** All **ENABLED** campaigns in this account. **Account `5933229194`** has no ENABLED campaigns in the linked portfolio (no rows).\n\n")
    lines.append("**Filters (same as your prior report):**\n\n")
    lines.append("- Date: `segments.date` **DURING LAST_7_DAYS**\n")
    lines.append("- Spend: `metrics.cost_micros > 1_000_000` (\\> **\\$1.00**)\n")
    lines.append("- Targeting: `segments.search_term_targeting_status = NONE` (not added as keyword, not excluded)\n\n")
    lines.append(
        f"**Portfolio totals (matching rows only):** **{len(rows)}** search-term rows · "
        f"**${total_cost:,.2f}** cost · **{total_conv:g}** conv. · **${total_cv:g}** conv. value\n\n"
    )
    lines.append("---\n\n")

    for idx, (cid, cname, ctype) in enumerate(sorted(ENABLED_CAMPAIGNS, key=lambda x: x[0])):
        sid = str(cid)
        camp_rows = by_id.get(sid, [])
        if idx > 0:
            lines.append("\n")
        lines.append(f"## {cname}\n\n")
        lines.append(f"- **Campaign ID:** `{cid}` · **Channel:** `{ctype}`\n\n")
        if not camp_rows:
            lines.append(
                "*No search terms in this window met the filters* (common for **Display** campaigns, or when no term spent \\> \\$1 with status **NONE**).\n\n"
            )
            continue
        sub_cost = sum(float(r["metrics.costMicros"]) for r in camp_rows) / 1e6
        sub_conv = sum(float(r["metrics.conversions"] or 0) for r in camp_rows)
        sub_cv = sum(float(r["metrics.conversionsValue"] or 0) for r in camp_rows)
        lines.append(
            f"**This campaign:** {len(camp_rows)} terms · **${sub_cost:,.2f}** · **{sub_conv:g}** conv. · **${sub_cv:g}** conv. value\n\n"
        )
        lines.append("Column groups: **Engagement** · **Cost** · **Conversion**\n\n")
        lines.append(table_for_rows(camp_rows))

    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
