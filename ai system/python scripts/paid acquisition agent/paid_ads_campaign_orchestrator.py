"""
Generic paid ads campaign orchestrator.

Goal:
    Given a small set of inputs (channel, campaign name, objective, month),
    scaffold the full paid-ads asset pack under outputs/docs/paid_ads_assets/:

        - Campaign structure file
        - Ad creative file for the month
        - Stubs for visual creative briefs (directory only; briefs are separate agents)
        - Landing page & CRO doc
        - Tracking implementation & QA doc
        - Channel-specific build sheet
        - Experiment (A/B test) plan

Supported channels (folder names):
    - "meta"
    - "google"
    - "linkedin"
    - "tiktok"
    - "x"
    - "reddit"

This script does NOT talk to ad APIs. It just creates Markdown templates that
the paid-ads-structure-agent, ad-creative-agent, visual-creative-brief-agent,
cro_hypothesis_agent, analytics-tracking-agent, social/search ads agents,
and ab-test-agent can then fill in or extend.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
from pathlib import Path
from textwrap import dedent

# Repository root (orchestrator lives at ai system/python scripts/paid acquisition agent/)
REPO_ROOT = Path(__file__).resolve().parents[3]
ASSETS_ROOT = REPO_ROOT / "outputs" / "docs" / "paid_ads_assets"


def _today_iso() -> str:
    return _dt.date.today().isoformat()


def _month_label(date: _dt.date | None = None) -> str:
    d = date or _dt.date.today()
    return d.strftime("%b %Y")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content.strip() + "\n", encoding="utf-8")


def _normalise_channel(channel: str) -> str:
    c = channel.strip().lower()
    mapping = {
        "facebook": "meta",
        "instagram": "meta",
        "fb": "meta",
        "google ads": "google",
        "adwords": "google",
        "twitter": "x",
        "reddit ads": "reddit",
    }
    return mapping.get(c, c)


def scaffold_campaign(
    channel: str,
    campaign_name: str,
    objective: str,
    month_slug: str,
    description: str | None = None,
) -> Path:
    """
    Create all core Markdown scaffolds for a new paid ads campaign.

    Returns the path to the campaign folder.
    """
    channel_norm = _normalise_channel(channel)
    if channel_norm not in {"meta", "google", "linkedin", "tiktok", "x", "reddit"}:
        raise SystemExit(f"Unsupported channel '{channel_norm}'. "
                         "Supported: meta, google, linkedin, tiktok, x, reddit.")

    today = _dt.date.today()
    campaign_dir = ASSETS_ROOT / channel_norm / campaign_name
    _ensure_dir(campaign_dir)

    # Also ensure subfolders exist for each asset type.
    structure_dir = campaign_dir / "campaign-structure"
    ad_creative_dir = campaign_dir / "ad-creative"
    cro_dir = campaign_dir / "landing-page-and-cro"
    tracking_dir = campaign_dir / "tracking-implementation-and-qa"
    build_sheet_dir = campaign_dir / "build-sheet"
    ab_test_dir = campaign_dir / "ab-test-plan"
    creative_briefs_dir = campaign_dir / "creative-briefs" / month_slug
    creative_deliverables_dir = campaign_dir / "creative-deliverables" / month_slug
    for d in (
        structure_dir,
        ad_creative_dir,
        cro_dir,
        tracking_dir,
        build_sheet_dir,
        ab_test_dir,
        creative_briefs_dir,
        creative_deliverables_dir,
    ):
        _ensure_dir(d)

    human_month = _month_label(today)
    desc = description or f"Paid {channel_norm} campaign for {objective}."

    # 1) Campaign structure
    structure_path = structure_dir / f"{campaign_name}_campaign-structure.md"
    _write_if_missing(
        structure_path,
        dedent(
            f"""
            ---
            title: "Campaign Structure: {campaign_name}"
            date_created: "{_today_iso()}"
            last_updated: "{_today_iso()}"
            status: "Draft"
            platform: "{channel_norm}"
            objective: "{objective}"
            description: "{desc}"
            ---

            # Campaign Structure: {campaign_name}

            <!--
            This file is intended to be populated by paid-ads-structure-agent.
            Fill in platform-specific campaign/ad set/ad group structure,
            bidding, budgets, audiences, placements, tracking, and checklists.
            -->

            ## Metadata

            | Field | Value |
            |-------|-------|
            | **Platform** | {channel_norm} |
            | **Objective** | {objective} |
            | **Monthly Budget** | TODO |
            | **Date Created** | {_today_iso()} |
            | **Status** | Draft |

            ## Companion Assets

            | Asset | Link |
            |-------|------|
            | **Ad Creative (current)** | [ad-creative/{campaign_name}_ad-creative_{month_slug}.md](ad-creative/{campaign_name}_ad-creative_{month_slug}.md) |
            | **Creative Briefs (current)** | [creative-briefs/{month_slug}/](creative-briefs/{month_slug}/_index.md) |
            | **Creative deliverables (current)** | [creative-deliverables/{month_slug}/](creative-deliverables/{month_slug}/_index.md) |
            | **Campaign Master Index** | [_index.md](_index.md) |
            """
        ),
    )

    # 2) Ad creative
    creative_path = ad_creative_dir / f"{campaign_name}_ad-creative_{month_slug}.md"
    _write_if_missing(
        creative_path,
        dedent(
            f"""
            ---
            title: "Ad Creative – {campaign_name}"
            campaign: "{campaign_name}"
            platform: "{channel_norm}"
            objective: "{objective}"
            month: "{human_month}"
            status: "Draft"
            ---

            # Ad Creative – {campaign_name} ({human_month})

            <!--
            This file is intended to be populated by ad-creative-agent.
            Define creative angles, primary text, headlines, descriptions,
            per-platform/ad-type specs, and mapping to ad sets/ad groups.
            -->

            ## Creative Brief (Condensed)

            | Field | Value |
            |-------|-------|
            | **Campaign** | `{campaign_name}` |
            | **Objective** | {objective} |
            | **Platform** | {channel_norm} |
            | **Key Message** | TODO |
            | **Primary Personas** | TODO |
            | **Number of Core Angles** | TODO |
            | **Primary CTA** | TODO |
            """
        ),
    )

    # 3) Visual creative briefs index stub for this month
    briefs_index = creative_briefs_dir / "_index.md"
    _write_if_missing(
        briefs_index,
        dedent(
            f"""
            ---
            title: "Visual Creative Briefs – {campaign_name} – {human_month}"
            campaign: "{campaign_name}"
            platform: "{channel_norm}"
            month: "{human_month}"
            status: "Draft"
            ---

            # Visual Creative Briefs – {campaign_name} ({human_month})

            This folder is intended to be filled by visual-creative-brief-agent.
            Create one brief per ad ID defined in `{campaign_name}_ad-creative_{month_slug}.md`.
            """
        ),
    )

    deliverables_index = creative_deliverables_dir / "_index.md"
    _write_if_missing(
        deliverables_index,
        dedent(
            f"""
            ---
            title: "Creative Deliverables – {campaign_name} – {human_month}"
            campaign: "{campaign_name}"
            platform: "{channel_norm}"
            month: "{human_month}"
            status: "Draft"
            ---

            # Creative Deliverables – {campaign_name} ({human_month})

            Place **built** assets here: Canva/Figma handoff markdown, export links, `canva_mcp_sync_plan.json`, etc.
            **Designer briefs** stay in `creative-briefs/{month_slug}/`.

            ## Companion assets

            | Asset | Link |
            |-------|------|
            | **Creative briefs** | [../../creative-briefs/{month_slug}/_index.md](../../creative-briefs/{month_slug}/_index.md) |
            | **Ad creative** | [../../ad-creative/{campaign_name}_ad-creative_{month_slug}.md](../../ad-creative/{campaign_name}_ad-creative_{month_slug}.md) |
            | **Campaign index** | [../../_index.md](../../_index.md) |
            """
        ),
    )

    # 4) Landing page & CRO doc
    cro_path = cro_dir / f"{campaign_name}_landing-page-and-cro_{month_slug}.md"
    _write_if_missing(
        cro_path,
        dedent(
            f"""
            ---
            title: "Landing Page & CRO – {campaign_name}"
            campaign: "{campaign_name}"
            agent: "cro_hypothesis_agent + landing_page_agent"
            status: "Draft"
            date_created: "{_today_iso()}"
            ---

            # Landing Page & CRO – {campaign_name}

            <!--
            To be populated by cro_hypothesis_agent and landing_page_agent.
            Define funnel, landing-page structure, hypotheses, and test backlog.
            -->

            ## Funnel Definition

            - **Traffic source:** {channel_norm}
            - **Offer:** TODO
            - **Core promise:** TODO

            ## Recommended Landing Page Structure

            TODO – hero, social proof, what-you-get, FAQ/objections.
            """
        ),
    )

    # 5) Tracking implementation & QA
    tracking_path = tracking_dir / f"{campaign_name}_tracking-implementation-and-qa_{month_slug}.md"
    _write_if_missing(
        tracking_path,
        dedent(
            f"""
            ---
            title: "Tracking Implementation & QA – {campaign_name}"
            campaign: "{campaign_name}"
            agent: "analytics-tracking-agent"
            status: "Draft"
            date_created: "{_today_iso()}"
            ---

            # Tracking Implementation & QA – {campaign_name}

            <!--
            To be populated by analytics-tracking-agent.
            Specify events, UTMs, pixels/tags, server-side tracking,
            data flow into GA4/CRM, and QA steps.
            -->

            ## Event Architecture

            TODO – define platform + analytics events.
            """
        ),
    )

    # 6) Channel-specific build sheet stub
    build_sheet_path = build_sheet_dir / f"{campaign_name}_{channel_norm}-build-sheet.md"
    _write_if_missing(
        build_sheet_path,
        dedent(
            f"""
            ---
            title: "{channel_norm.title()} Build Sheet – {campaign_name}"
            campaign: "{campaign_name}"
            platform: "{channel_norm}"
            status: "Draft"
            date_created: "{_today_iso()}"
            ---

            # {channel_norm.title()} Build Sheet – `{campaign_name}`

            <!--
            To be populated by social_ads_agent / search_ads_agent or
            equivalent channel build agent.
            Provide field-by-field setup steps for {channel_norm}.
            -->

            ## 1. Prerequisites

            TODO – account, billing, tags/pixels.
            """
        ),
    )

    # 7) Experiment / A/B test plan stub
    ab_test_path = ab_test_dir / f"{campaign_name}_ab-test-plan_{month_slug}.md"
    _write_if_missing(
        ab_test_path,
        dedent(
            f"""
            ---
            title: "Experiment Plan – {campaign_name}"
            campaign: "{campaign_name}"
            agent: "ab-test-agent"
            status: "Draft"
            date_created: "{_today_iso()}"
            ---

            # Experiment Plan – {campaign_name}

            <!--
            To be populated by ab-test-agent.
            Define sequential tests (creative, audience, bidding, landing page),
            KPIs, guardrails, and decision rules.
            -->

            ## 1. Experiment Framework

            - **Primary KPI:** TODO
            - **Secondary KPIs:** TODO
            """
        ),
    )

    return campaign_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold paid ads campaign assets for any supported channel."
    )
    parser.add_argument(
        "--channel",
        required=True,
        help="Channel: meta, google, linkedin, tiktok, x (aliases like 'facebook' allowed).",
    )
    parser.add_argument(
        "--campaign-name",
        required=True,
        help="Folder-safe campaign name, e.g. us-ca_meta_leads_reader-acquisition_mar26",
    )
    parser.add_argument(
        "--objective",
        required=True,
        help="Business objective, e.g. 'Leads – Newsletter Signups'.",
    )
    parser.add_argument(
        "--month-slug",
        required=True,
        help="Short month slug used in filenames, e.g. mar26.",
    )
    parser.add_argument(
        "--description",
        help="Optional human description of the campaign.",
    )

    args = parser.parse_args()
    campaign_dir = scaffold_campaign(
        channel=args.channel,
        campaign_name=args.campaign_name,
        objective=args.objective,
        month_slug=args.month_slug,
        description=args.description,
    )
    print(f"Scaffolded paid ads campaign assets at: {campaign_dir}")


if __name__ == "__main__":
    main()

