"""
config.py — Competitor list, platform mappings, and CSV schema.

Competitors sourced from commands/core/competitor_landscape.md.
Platforms sourced from agents/technical/paid-ads-structure-agent.md.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = WORKSPACE_ROOT / "docs" / "competitor content tracker" / "paid ads creatives"

AD_CREATIVE_LOG_CSV = DOCS_DIR / "ad_creative_log.csv"
AD_VOLUME_TRACKER_CSV = DOCS_DIR / "ad_volume_tracker.csv"

# ---------------------------------------------------------------------------
# Competitors
# ---------------------------------------------------------------------------

# Reader-side competitors (competing for subscribers)
READER_COMPETITORS: dict[str, dict] = {
    "Morning Brew": {
        "side": "reader",
        "meta_search": "Morning Brew",
        "google_search": "Morning Brew",
        "linkedin_search": "Morning Brew",
        "tiktok_search": "Morning Brew",
        "x_search": "MorningBrew",
        "description": "Daily business/finance newsletter, 4M+ subs",
    },
    "The Hustle": {
        "side": "reader",
        "meta_search": "The Hustle",
        "google_search": "The Hustle HubSpot",
        "linkedin_search": "The Hustle",
        "tiktok_search": "The Hustle",
        "x_search": "TheHustle",
        "description": "Daily business/tech newsletter, 1.5M+ subs (HubSpot)",
    },
    "Hacker News": {
        "side": "reader",
        "meta_search": "Y Combinator",
        "google_search": "Hacker News Y Combinator",
        "linkedin_search": "Y Combinator",
        "tiktok_search": "Y Combinator",
        "x_search": "ycombinator",
        "description": "YC link aggregation site, tech community homepage",
    },
    "Stratechery": {
        "side": "reader",
        "meta_search": "Stratechery",
        "google_search": "Stratechery Ben Thompson",
        "linkedin_search": "Stratechery",
        "tiktok_search": "Stratechery",
        "x_search": "stratechery",
        "description": "Paid premium tech analysis newsletter",
    },
    "Lenny's Newsletter": {
        "side": "reader",
        "meta_search": "Lenny Rachitsky",
        "google_search": "Lenny's Newsletter",
        "linkedin_search": "Lenny Rachitsky",
        "tiktok_search": "Lenny Rachitsky",
        "x_search": "lennysan",
        "description": "Product management & growth, 1.1M+ subs",
    },
    "Bytes.dev": {
        "side": "reader",
        "meta_search": "Bytes.dev",
        "google_search": "Bytes.dev JavaScript",
        "linkedin_search": "Bytes.dev",
        "tiktok_search": "Bytes.dev",
        "x_search": "ui_dev",
        "description": "Niche JS/dev newsletter digest",
    },
}

# Advertiser-side competitors (competing for ad budgets)
ADVERTISER_COMPETITORS: dict[str, dict] = {
    "LinkedIn Ads": {
        "side": "advertiser",
        "meta_search": "LinkedIn",
        "google_search": "LinkedIn Marketing Solutions",
        "linkedin_search": "LinkedIn Marketing Solutions",
        "tiktok_search": "LinkedIn",
        "x_search": "LinkedInMktg",
        "description": "Dominant B2B ad platform, $8-15+ CPCs",
    },
    "Meta Ads": {
        "side": "advertiser",
        "meta_search": "Meta for Business",
        "google_search": "Meta Business Suite",
        "linkedin_search": "Meta for Business",
        "tiktok_search": "Meta Business",
        "x_search": "MetaBusiness",
        "description": "Massive scale social ads platform",
    },
    "Paved": {
        "side": "advertiser",
        "meta_search": "Paved",
        "google_search": "Paved newsletter ads",
        "linkedin_search": "Paved",
        "tiktok_search": "Paved",
        "x_search": "paboreal",
        "description": "Newsletter ad network / marketplace",
    },
    "Beehiiv": {
        "side": "advertiser",
        "meta_search": "beehiiv",
        "google_search": "beehiiv ad network",
        "linkedin_search": "beehiiv",
        "tiktok_search": "beehiiv",
        "x_search": "beaboreal",
        "description": "Newsletter platform with built-in ad network",
    },
}

ALL_COMPETITORS = {**READER_COMPETITORS, **ADVERTISER_COMPETITORS}

# Ordered list for consistent CSV column ordering
COMPETITOR_NAMES = list(ALL_COMPETITORS.keys())

# ---------------------------------------------------------------------------
# Platforms to scrape (matches paid-ads-structure-agent)
# ---------------------------------------------------------------------------

PLATFORMS = ["Meta", "Google", "LinkedIn", "TikTok", "X"]

# Ad library URLs for reference
AD_LIBRARY_URLS = {
    "Meta": "https://www.facebook.com/ads/library/",
    "Google": "https://adstransparency.google.com/",
    "LinkedIn": "https://www.linkedin.com/ad-library/",
    "TikTok": "https://library.tiktok.com/",
    "X": "https://ads.x.com/transparency",
}

# ---------------------------------------------------------------------------
# CSV Schemas
# ---------------------------------------------------------------------------

AD_CREATIVE_LOG_COLUMNS = [
    "Date Spotted",
    "Competitor",
    "Platform",
    "Ad Format",
    "Copy Angle",
    "Headline / Primary Text",
    "Description / Body Copy",
    "Visual Style",
    "CTA",
    "Ad Library Link",
    "Video Link",
    "Notes / Observations",
    "Still Active",
    "First Seen",
]

def ad_volume_tracker_columns() -> list[str]:
    """Build the Ad Volume Tracker column list dynamically from competitors."""
    cols = ["Audit Date"]
    for name in COMPETITOR_NAMES:
        for platform in PLATFORMS:
            cols.append(f"{name} ({platform})")
    cols.extend(["Total Competitor Ads", "Notes / Trends"])
    return cols

AD_VOLUME_TRACKER_COLUMNS = ad_volume_tracker_columns()
