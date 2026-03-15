"""
competitive_tracker.py — Monthly Competitive Creative Tracker

Scrapes ad libraries for all five paid-ads platforms (Meta, Google, LinkedIn,
TikTok, X) for every competitor defined in config.py. Appends results to:
  1. ad_creative_log.csv   — one row per ad creative spotted
  2. ad_volume_tracker.csv — one row per monthly audit with ad counts

Usage:
  python competitive_tracker.py                          # full run (all platforms)
  python competitive_tracker.py --platforms meta google   # specific platforms
  python competitive_tracker.py --dry-run                # print without writing CSVs
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    AD_CREATIVE_LOG_COLUMNS,
    AD_CREATIVE_LOG_CSV,
    AD_VOLUME_TRACKER_COLUMNS,
    AD_VOLUME_TRACKER_CSV,
    AD_LIBRARY_URLS,
    ALL_COMPETITORS,
    COMPETITOR_NAMES,
    DOCS_DIR,
    PLATFORMS,
)


def _resolve_env_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{name}="):
                        return line.split("=", 1)[1].strip().strip("'\"")
        current = current.parent
    return None


def _truncate(text: str, max_len: int = 500) -> str:
    text = " ".join(text.split())
    return text[:max_len] if len(text) > max_len else text


def _get_playwright():
    """Import and return sync_playwright, or None if unavailable."""
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        return None


# ═══════════════════════════════════════════════════════════════════════════
# META AD LIBRARY
# ═══════════════════════════════════════════════════════════════════════════

SCRAPECREATORS_BASE = "https://api.scrapecreators.com/v2"
META_AD_LIBRARY_URL = "https://www.facebook.com/ads/library/"


def scrape_meta_competitor(competitor_name: str, api_key: str | None) -> list[dict]:
    info = ALL_COMPETITORS[competitor_name]
    search_term = info.get("meta_search", competitor_name)
    print(f"  🔍 Meta: searching '{search_term}'...")

    if api_key and api_key != "your_key_here":
        rows = _meta_api_scrape(competitor_name, search_term, api_key)
        if rows:
            return rows

    return _meta_playwright_scrape(competitor_name, search_term)


def _meta_api_scrape(competitor_name: str, search_term: str, api_key: str) -> list[dict]:
    try:
        resp = requests.get(
            f"{SCRAPECREATORS_BASE}/meta-ad-library/search-page",
            params={"query": search_term},
            headers={"x-api-key": api_key},
            timeout=30,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        pages = data.get("data", data.get("results", []))
        if not pages:
            return []

        page_id = pages[0].get("id") or pages[0].get("page_id") or pages[0].get("platform_id", "")
        if not page_id:
            return []

        resp2 = requests.get(
            f"{SCRAPECREATORS_BASE}/meta-ad-library/ads",
            params={"platform_id": page_id, "limit": 50},
            headers={"x-api-key": api_key},
            timeout=60,
        )
        if resp2.status_code != 200:
            return []
        ad_data = resp2.json()
        raw_ads = ad_data.get("data", ad_data.get("ads", ad_data.get("results", [])))

        today = datetime.now().strftime("%Y-%m-%d")
        rows = []
        for ad in raw_ads:
            ad_id = ad.get("ad_id") or ad.get("id", "")
            rows.append({
                "Date Spotted": today,
                "Competitor": competitor_name,
                "Platform": "Meta",
                "Ad Format": _detect_format_from_dict(ad, "meta"),
                "Copy Angle": "",
                "Headline / Primary Text": _truncate(
                    ad.get("body_text") or ad.get("ad_creative_body") or ad.get("body", {}).get("text", "") or "", 500),
                "Description / Body Copy": _truncate(
                    ad.get("ad_creative_link_description", "") or ad.get("link_description", "") or "", 500),
                "Visual Style": "Video creative" if "video" in str(ad.get("media_type", "")).lower() else "Static image",
                "CTA": ad.get("cta_text") or ad.get("call_to_action_type", "") or "",
                "Ad Library Link": f"facebook.com/ads/library/?id={ad_id}" if ad_id else "",
                "Video Link": next((ad[k] for k in ("video_url", "video_hd_url", "video_sd_url") if ad.get(k)), ""),
                "Notes / Observations": "",
                "Still Active": "Yes",
                "First Seen": ad.get("ad_delivery_start_time", "") or ad.get("start_date", "") or today,
            })
        if rows:
            print(f"  ✓ Meta API: found {len(rows)} ads for {competitor_name}")
        return rows
    except Exception:
        return []


def _meta_playwright_scrape(competitor_name: str, search_term: str) -> list[dict]:
    sync_playwright = _get_playwright()
    if not sync_playwright:
        print("  ℹ Playwright not installed — skipping Meta browser scrape")
        return []

    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"{META_AD_LIBRARY_URL}?active_status=active&ad_type=all&country=US&q={quote(search_term)}"
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(5)

            ad_cards = page.query_selector_all(
                "div[class*='_7jvw'], div[class*='xrvj5dj'], "
                "[data-testid*='ad_library'], div[role='article']"
            )

            today = datetime.now().strftime("%Y-%m-%d")
            for card in ad_cards[:50]:
                text = card.inner_text()
                lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                if len(lines) < 2:
                    continue

                has_video = card.query_selector("video") is not None
                link_el = card.query_selector("a[href*='ads/library']")
                ad_link = link_el.get_attribute("href") if link_el else url

                results.append({
                    "Date Spotted": today,
                    "Competitor": competitor_name,
                    "Platform": "Meta",
                    "Ad Format": "Video" if has_video else "Static (Image)",
                    "Copy Angle": "",
                    "Headline / Primary Text": _truncate(lines[0] if lines else "", 500),
                    "Description / Body Copy": _truncate(" ".join(lines[1:3]) if len(lines) > 1 else "", 500),
                    "Visual Style": "Video creative" if has_video else "Static image",
                    "CTA": "",
                    "Ad Library Link": ad_link or "",
                    "Video Link": "",
                    "Notes / Observations": "Scraped via Playwright",
                    "Still Active": "Yes",
                    "First Seen": today,
                })
            browser.close()

            if results:
                print(f"  ✓ Meta Playwright: found {len(results)} ads for {competitor_name}")
            else:
                print(f"  ⚠ No Meta ads found for '{search_term}'")
    except Exception as e:
        print(f"  ⚠ Meta Playwright scrape failed: {e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# GOOGLE ADS TRANSPARENCY CENTER
# ═══════════════════════════════════════════════════════════════════════════

GOOGLE_TRANSPARENCY_BASE = "https://adstransparency.google.com"


def scrape_google_competitor(competitor_name: str) -> list[dict]:
    info = ALL_COMPETITORS[competitor_name]
    search_term = info.get("google_search", competitor_name)
    print(f"  🔍 Google: searching '{search_term}'...")

    ads = _google_transparency_api(search_term)
    if not ads:
        ads = _google_transparency_playwright(search_term, competitor_name)

    if not ads:
        print(f"  ⚠ No Google ads found for '{search_term}'")
        return []

    print(f"  ✓ Google: found {len(ads)} ads for {competitor_name}")
    return ads


def _google_transparency_api(search_term: str) -> list[dict] | None:
    try:
        resp = requests.get(
            f"{GOOGLE_TRANSPARENCY_BASE}/asr/search",
            params={"q": search_term, "region": "US"},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            },
            timeout=30,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = []
        for item in data.get("advertisers", data.get("results", [])):
            advertiser_id = item.get("advertiserId", item.get("id", ""))
            ad_resp = requests.get(
                f"{GOOGLE_TRANSPARENCY_BASE}/asr/advertiser/{advertiser_id}/ads",
                params={"region": "US", "limit": 50},
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Accept": "application/json",
                },
                timeout=30,
            )
            if ad_resp.status_code == 200:
                ad_data = ad_resp.json()
                for ad in ad_data.get("ads", ad_data.get("results", [])):
                    results.append({
                        "headline": ad.get("headline", ad.get("title", "")),
                        "description": ad.get("description", ad.get("body", "")),
                        "format": ad.get("format", "Search"),
                        "link": f"{GOOGLE_TRANSPARENCY_BASE}/advertiser/{advertiser_id}",
                        "first_seen": ad.get("firstShown", ""),
                    })
            if results:
                break
        return results if results else None
    except Exception:
        return None


def _google_transparency_playwright(search_term: str, competitor_name: str) -> list[dict]:
    sync_playwright = _get_playwright()
    if not sync_playwright:
        print("  ℹ Playwright not installed — skipping Google browser scrape")
        return []

    results = []
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"{GOOGLE_TRANSPARENCY_BASE}/?region=US&query={quote(search_term)}"
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(5)

            advertiser_links = page.query_selector_all("a[href*='/advertiser/']")
            if advertiser_links:
                advertiser_links[0].click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(3)

            ad_elements = page.query_selector_all(
                "creative-preview, [class*='ad-card'], [class*='creative-card'], "
                "[role='listitem'], [class*='preview']"
            )
            for el in ad_elements[:50]:
                text = el.inner_text()
                lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                if not lines:
                    continue
                has_img = el.query_selector("img") is not None
                results.append({
                    "Date Spotted": today,
                    "Competitor": competitor_name,
                    "Platform": "Google",
                    "Ad Format": "Display" if has_img else "Search",
                    "Copy Angle": "",
                    "Headline / Primary Text": _truncate(lines[0], 500),
                    "Description / Body Copy": _truncate(lines[1] if len(lines) > 1 else "", 500),
                    "Visual Style": "Display banner" if has_img else "Text ad",
                    "CTA": "",
                    "Ad Library Link": page.url,
                    "Video Link": "",
                    "Notes / Observations": "Scraped via Playwright",
                    "Still Active": "Yes",
                    "First Seen": today,
                })
            browser.close()
    except Exception as e:
        print(f"  ⚠ Google Playwright scrape failed: {e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# LINKEDIN AD LIBRARY
# ═══════════════════════════════════════════════════════════════════════════

LINKEDIN_AD_LIBRARY_URL = "https://www.linkedin.com/ad-library/search"


def scrape_linkedin_competitor(competitor_name: str) -> list[dict]:
    info = ALL_COMPETITORS[competitor_name]
    search_term = info.get("linkedin_search", competitor_name)
    print(f"  🔍 LinkedIn: searching '{search_term}'...")

    ads = _linkedin_playwright_scrape(search_term, competitor_name)

    if not ads:
        print(f"  ⚠ No LinkedIn ads found for '{search_term}'")
        return []

    print(f"  ✓ LinkedIn: found {len(ads)} ads for {competitor_name}")
    return ads


def _linkedin_playwright_scrape(search_term: str, competitor_name: str) -> list[dict]:
    """
    LinkedIn Ad Library is public and doesn't require login.
    URL: https://www.linkedin.com/ad-library/search?accountOwner={company}
    The page renders ad cards as <li> elements within a results list.
    """
    sync_playwright = _get_playwright()
    if not sync_playwright:
        print("  ℹ Playwright not installed — skipping LinkedIn browser scrape")
        return []

    results = []
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })

            url = f"{LINKEDIN_AD_LIBRARY_URL}?accountOwner={quote(search_term)}"
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(4)

            count_el = page.query_selector("h1")
            ad_count_text = count_el.inner_text() if count_el else ""
            count_match = re.search(r"([\d,]+)\s+ads?", ad_count_text)
            total_count = int(count_match.group(1).replace(",", "")) if count_match else 0

            if total_count == 0:
                no_results = page.query_selector("text='No results found'")
                if no_results:
                    browser.close()
                    return []

            ad_cards = page.query_selector_all("ul > li")
            for card in ad_cards[:50]:
                try:
                    text = card.inner_text()
                    if not text or len(text.strip()) < 10:
                        continue

                    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                    if len(lines) < 2:
                        continue

                    advertiser = ""
                    copy_text = ""
                    headline = ""
                    ad_detail_link = ""

                    for line in lines:
                        if line == "Promoted" or line == "View details":
                            continue
                        if not advertiser and line not in ("Promoted",):
                            advertiser = line
                            continue
                        if not copy_text and len(line) > 20:
                            copy_text = line
                            continue
                        if not headline and len(line) > 5:
                            headline = line

                    detail_link = card.query_selector("a[href*='/ad-library/detail/']")
                    if detail_link:
                        href = detail_link.get_attribute("href") or ""
                        ad_detail_link = f"https://www.linkedin.com{href}" if href.startswith("/") else href

                    if not copy_text and not headline:
                        continue

                    has_video = card.query_selector("video") is not None
                    has_image = card.query_selector("img") is not None

                    if has_video:
                        ad_format = "Video Ad"
                        visual = "Video creative"
                    elif has_image:
                        ad_format = "Single Image Ad"
                        visual = "Static image"
                    else:
                        ad_format = "Text Ad"
                        visual = "Text only"

                    h2 = card.query_selector("h2")
                    if h2:
                        headline = h2.inner_text().strip()

                    results.append({
                        "Date Spotted": today,
                        "Competitor": competitor_name,
                        "Platform": "LinkedIn",
                        "Ad Format": ad_format,
                        "Copy Angle": "",
                        "Headline / Primary Text": _truncate(copy_text, 500),
                        "Description / Body Copy": _truncate(headline, 500),
                        "Visual Style": visual,
                        "CTA": "",
                        "Ad Library Link": ad_detail_link or url,
                        "Video Link": "",
                        "Notes / Observations": f"Total active: {total_count}" if total_count else "Scraped via Playwright",
                        "Still Active": "Yes",
                        "First Seen": today,
                    })
                except Exception:
                    continue

            browser.close()
    except Exception as e:
        print(f"  ⚠ LinkedIn Playwright scrape failed: {e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# TIKTOK COMMERCIAL CONTENT LIBRARY
# ═══════════════════════════════════════════════════════════════════════════

TIKTOK_LIBRARY_BASE = "https://library.tiktok.com"


def scrape_tiktok_competitor(competitor_name: str) -> list[dict]:
    info = ALL_COMPETITORS[competitor_name]
    search_term = info.get("tiktok_search", competitor_name)
    print(f"  🔍 TikTok: searching '{search_term}'...")

    ads = _tiktok_playwright_scrape(search_term, competitor_name)

    if not ads:
        print(f"  ⚠ No TikTok ads found for '{search_term}'")
        return []

    print(f"  ✓ TikTok: found {len(ads)} ads for {competitor_name}")
    return ads


def _tiktok_playwright_scrape(search_term: str, competitor_name: str) -> list[dict]:
    sync_playwright = _get_playwright()
    if not sync_playwright:
        print("  ℹ Playwright not installed — skipping TikTok browser scrape")
        return []

    results = []
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"{TIKTOK_LIBRARY_BASE}/ads?region=US&adv_name={quote(search_term)}"
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(5)

            ad_cards = page.query_selector_all(
                "[class*='ad-card'], [class*='search-card'], "
                "[class*='commercial-content'], [role='listitem'], "
                "[class*='CardContainer'], [class*='card-item']"
            )
            for card in ad_cards[:50]:
                text = card.inner_text()
                lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                if not lines:
                    continue
                video_el = card.query_selector("video")
                results.append({
                    "Date Spotted": today,
                    "Competitor": competitor_name,
                    "Platform": "TikTok",
                    "Ad Format": "In-Feed Video",
                    "Copy Angle": "",
                    "Headline / Primary Text": _truncate(lines[0], 500),
                    "Description / Body Copy": _truncate(" ".join(lines[1:3]) if len(lines) > 1 else "", 500),
                    "Visual Style": "Video creative",
                    "CTA": "",
                    "Ad Library Link": url,
                    "Video Link": video_el.get_attribute("src") if video_el else "",
                    "Notes / Observations": "Scraped via Playwright",
                    "Still Active": "Yes",
                    "First Seen": today,
                })
            browser.close()
    except Exception as e:
        print(f"  ⚠ TikTok Playwright scrape failed: {e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# X (TWITTER) ADS TRANSPARENCY CENTER
# ═══════════════════════════════════════════════════════════════════════════

X_TRANSPARENCY_BASE = "https://ads.x.com/transparency"


def scrape_x_competitor(competitor_name: str) -> list[dict]:
    info = ALL_COMPETITORS[competitor_name]
    search_term = info.get("x_search", competitor_name)
    print(f"  🔍 X: searching '{search_term}'...")

    ads = _x_playwright_scrape(search_term, competitor_name)

    if not ads:
        print(f"  ⚠ No X ads found for '{search_term}'")
        return []

    print(f"  ✓ X: found {len(ads)} ads for {competitor_name}")
    return ads


def _x_playwright_scrape(search_term: str, competitor_name: str) -> list[dict]:
    sync_playwright = _get_playwright()
    if not sync_playwright:
        print("  ℹ Playwright not installed — skipping X browser scrape")
        return []

    results = []
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"{X_TRANSPARENCY_BASE}?q={quote(search_term)}"
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(5)

            advertiser_links = page.query_selector_all("a[href*='advertiser_id'], [class*='advertiser']")
            if advertiser_links:
                advertiser_links[0].click()
                try:
                    page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass
                time.sleep(3)

            ad_cards = page.query_selector_all(
                "[class*='ad-card'], [data-testid*='ad'], "
                "[class*='transparency-card'], article, [role='listitem']"
            )
            for card in ad_cards[:50]:
                text = card.inner_text()
                lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                if not lines:
                    continue

                has_video = card.query_selector("video") is not None
                has_image = card.query_selector("img") is not None

                if has_video:
                    visual, fmt = "Video creative", "Video Ad"
                elif has_image:
                    visual, fmt = "Static image", "Image Ad"
                else:
                    visual, fmt = "Text only", "Promoted Post"

                video_el = card.query_selector("video")
                results.append({
                    "Date Spotted": today,
                    "Competitor": competitor_name,
                    "Platform": "X",
                    "Ad Format": fmt,
                    "Copy Angle": "",
                    "Headline / Primary Text": _truncate(lines[0], 500),
                    "Description / Body Copy": _truncate(" ".join(lines[1:3]) if len(lines) > 1 else "", 500),
                    "Visual Style": visual,
                    "CTA": "",
                    "Ad Library Link": page.url,
                    "Video Link": video_el.get_attribute("src") if video_el else "",
                    "Notes / Observations": "Scraped via Playwright",
                    "Still Active": "Yes",
                    "First Seen": today,
                })
            browser.close()
    except Exception as e:
        print(f"  ⚠ X Playwright scrape failed: {e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# FORMAT DETECTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _detect_format_from_dict(ad: dict, platform: str) -> str:
    media = ad.get("media_type", "") or ad.get("ad_type", "")
    if "video" in str(media).lower():
        return "Video"
    if "carousel" in str(media).lower():
        return "Carousel"
    if platform == "meta":
        snapshot = ad.get("ad_snapshot_url", "")
        if "video" in str(snapshot).lower():
            return "Video"
    return "Static (Image)"


# ═══════════════════════════════════════════════════════════════════════════
# PLATFORM DISPATCHER
# ═══════════════════════════════════════════════════════════════════════════

PLATFORM_SCRAPERS = {
    "Meta": lambda name, keys: scrape_meta_competitor(name, keys.get("scrapecreators")),
    "Google": lambda name, keys: scrape_google_competitor(name),
    "LinkedIn": lambda name, keys: scrape_linkedin_competitor(name),
    "TikTok": lambda name, keys: scrape_tiktok_competitor(name),
    "X": lambda name, keys: scrape_x_competitor(name),
}


# ═══════════════════════════════════════════════════════════════════════════
# CSV OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

def ensure_csv(path: Path, columns: list[str]) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(columns)
        print(f"  📄 Created {path.name}")


def load_existing_ad_links(path: Path) -> set[str]:
    links = set()
    if not path.exists():
        return links
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            link = row.get("Ad Library Link", "").strip()
            if link:
                links.add(link)
    return links


def append_creative_rows(rows: list[dict], dry_run: bool = False) -> int:
    ensure_csv(AD_CREATIVE_LOG_CSV, AD_CREATIVE_LOG_COLUMNS)
    existing_links = load_existing_ad_links(AD_CREATIVE_LOG_CSV)

    new_rows = [r for r in rows if r.get("Ad Library Link", "").strip() not in existing_links]
    if not new_rows:
        print(f"  ℹ No new ads to append (all {len(rows)} already logged)")
        return 0

    if dry_run:
        print(f"  🧪 DRY RUN: would append {len(new_rows)} new ads")
        for r in new_rows[:5]:
            print(f"     - {r['Competitor']} / {r['Platform']}: {r.get('Headline / Primary Text', '')[:60]}...")
        return len(new_rows)

    with open(AD_CREATIVE_LOG_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=AD_CREATIVE_LOG_COLUMNS, extrasaction="ignore").writerows(new_rows)

    print(f"  ✅ Appended {len(new_rows)} new ads to ad_creative_log.csv")
    return len(new_rows)


def append_volume_row(volume_counts: dict[str, dict[str, int]], dry_run: bool = False) -> None:
    ensure_csv(AD_VOLUME_TRACKER_CSV, AD_VOLUME_TRACKER_COLUMNS)

    today = datetime.now().strftime("%Y-%m-%d")
    row = {"Audit Date": today}
    total = 0
    for name in COMPETITOR_NAMES:
        for platform in PLATFORMS:
            count = volume_counts.get(name, {}).get(platform, 0)
            row[f"{name} ({platform})"] = count
            total += count

    row["Total Competitor Ads"] = total
    row["Notes / Trends"] = _generate_trend_notes(volume_counts, total)

    if dry_run:
        print(f"  🧪 DRY RUN: would append volume row — total {total} ads")
        return

    with open(AD_VOLUME_TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=AD_VOLUME_TRACKER_COLUMNS, extrasaction="ignore").writerow(row)

    print(f"  ✅ Appended volume row: {total} total competitor ads")


def _generate_trend_notes(volume_counts: dict, total: int) -> str:
    parts = []
    highest_name, highest_count = "", 0
    for name in COMPETITOR_NAMES:
        competitor_total = sum(volume_counts.get(name, {}).values())
        if competitor_total > highest_count:
            highest_count = competitor_total
            highest_name = name
    if highest_name:
        parts.append(f"Highest volume: {highest_name} ({highest_count} ads)")

    platform_totals = {}
    for name in COMPETITOR_NAMES:
        for platform in PLATFORMS:
            platform_totals[platform] = platform_totals.get(platform, 0) + volume_counts.get(name, {}).get(platform, 0)
    top_platform = max(platform_totals, key=platform_totals.get) if platform_totals else ""
    if top_platform and platform_totals.get(top_platform, 0) > 0:
        parts.append(f"Top platform: {top_platform} ({platform_totals[top_platform]})")

    parts.append(f"Total: {total}")
    return ". ".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

def run_audit(platforms: list[str] | None = None, dry_run: bool = False) -> None:
    active_platforms = platforms or PLATFORMS

    print("=" * 60)
    print(f"🔎 Competitive Creative Tracker — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Platforms: {', '.join(active_platforms)}")
    print("=" * 60)

    api_keys = {
        "scrapecreators": _resolve_env_key("SCRAPECREATORS_API_KEY"),
    }

    all_rows: list[dict] = []
    volume_counts: dict[str, dict[str, int]] = {}

    for competitor_name in COMPETITOR_NAMES:
        print(f"\n📊 {competitor_name}")
        volume_counts[competitor_name] = {}

        for platform in active_platforms:
            scraper = PLATFORM_SCRAPERS.get(platform)
            if not scraper:
                print(f"  ⚠ No scraper for '{platform}'")
                volume_counts[competitor_name][platform] = 0
                continue

            try:
                rows = scraper(competitor_name, api_keys)
                all_rows.extend(rows)
                volume_counts[competitor_name][platform] = len(rows)
            except Exception as e:
                print(f"  ❌ {platform} scrape failed for {competitor_name}: {e}")
                volume_counts[competitor_name][platform] = 0

            time.sleep(1)

    print(f"\n{'=' * 60}")
    print(f"📋 Summary: {len(all_rows)} total ads found across all competitors")
    for platform in active_platforms:
        p_total = sum(volume_counts.get(n, {}).get(platform, 0) for n in COMPETITOR_NAMES)
        print(f"   {platform}: {p_total} ads")
    print(f"{'=' * 60}")

    new_count = append_creative_rows(all_rows, dry_run=dry_run)
    append_volume_row(volume_counts, dry_run=dry_run)

    print(f"\n✅ Audit complete. {new_count} new ads logged.")
    print(f"   Creative log: {AD_CREATIVE_LOG_CSV}")
    print(f"   Volume tracker: {AD_VOLUME_TRACKER_CSV}")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

PLATFORM_ALIASES = {
    "meta": "Meta", "facebook": "Meta",
    "google": "Google",
    "linkedin": "LinkedIn",
    "tiktok": "TikTok",
    "x": "X", "twitter": "X",
}


def main():
    parser = argparse.ArgumentParser(
        description="Competitive Creative Tracker — scrape ad libraries across all platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python competitive_tracker.py                              # all platforms\n"
            "  python competitive_tracker.py --platforms meta google      # Meta + Google only\n"
            "  python competitive_tracker.py --platforms linkedin         # LinkedIn only\n"
            "  python competitive_tracker.py --dry-run                    # preview without writing\n"
        ),
    )
    parser.add_argument("--platforms", nargs="+", metavar="PLATFORM",
                        help=f"Platforms to scrape. Options: {', '.join(PLATFORM_ALIASES.keys())}")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing CSVs")
    parser.add_argument("--meta-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--google-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.meta_only:
        platforms = ["Meta"]
    elif args.google_only:
        platforms = ["Google"]
    elif args.platforms:
        platforms = []
        for p in args.platforms:
            canonical = PLATFORM_ALIASES.get(p.lower())
            if canonical:
                platforms.append(canonical)
            else:
                print(f"⚠ Unknown platform '{p}'. Valid: {', '.join(PLATFORM_ALIASES.keys())}")
                sys.exit(1)
    else:
        platforms = None

    run_audit(platforms=platforms, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
