# Daily Content Pipeline Summary — 2026-06-18

## Pipeline Run Overview

| Metric | Value |
|--------|-------|
| **New Competitor Articles Scraped** | 19 |
| **New Pipeline Concepts Generated** | 19 |
| **Total Backlog (Not Started)** | 31 |
| **Ahrefs Enrichment** | Unavailable (API key not configured) |
| **Google Sheets Push** | Failed (credential error) — saved to markdown |

## Competitor Breakdown (New Articles)

| Competitor | New Articles |
|------------|-------------|
| Paved | 12 |
| Beehiiv | 5 |
| Stratechery | 2 |

## Top 5 Pipeline Items by Weighted Score

### 1. How Newsletters Drive 30% Revenue Growth at Pix
- **Score:** 4.1 | Relevance: 2 | Impact: 5 | Effort: 8
- **Source:** Paved
- **URL:** https://www.paved.com/blog/pix-publisher-spotlight/
- **Concept:** Strategic Deep Dive
- **Ahrefs Data:** Unavailable

### 2. Newsletter Sponsorship Rates: Paved Benchmarks + How to Price Your Newsletter
- **Score:** 4.1 | Relevance: 2 | Impact: 5 | Effort: 8
- **Source:** Paved
- **URL:** https://www.paved.com/blog/newsletter-sponsorship-rates/
- **Concept:** Tactical Playbook
- **Ahrefs Data:** Unavailable

### 3. Maximize Your Ad Revenue: A Guide to Newsletter CPM
- **Score:** 3.5 | Relevance: 2 | Impact: 5 | Effort: 5
- **Source:** Beehiiv
- **URL:** https://www.beehiiv.com/blog/newsletter-cpm
- **Concept:** Strategic Deep Dive
- **Ahrefs Data:** Unavailable

### 4. Newsletter Ad Networks: How to Get Your Brand in Inboxes
- **Score:** 3.2 | Relevance: 2 | Impact: 2 | Effort: 8
- **Source:** Paved
- **URL:** https://www.paved.com/blog/newsletter-ad-network/
- **Concept:** Tactical Playbook
- **Ahrefs Data:** Unavailable

### 5. Why Your Emails Are Going to Gmail's Promotions
- **Score:** 2.6 | Relevance: 2 | Impact: 0 | Effort: 8
- **Source:** Beehiiv
- **URL:** https://www.beehiiv.com/blog/why-your-emails-are-going-to-gmail-s-promotions
- **Concept:** Tactical Playbook
- **Ahrefs Data:** Unavailable

## Keyword Opportunities

> Ahrefs API was unavailable for this run (API key not configured). Keyword enrichment skipped.

Suggested keywords for manual research based on top pipeline items:
- `newsletter revenue growth`
- `newsletter sponsorship rates`
- `newsletter CPM rates`
- `newsletter ad networks`
- `email promotions tab`

## Notes

- The scraper successfully connected to all 8 competitor blogs. Morning Brew, The Hustle, Lenny's Newsletter, Benedict Evans, and Bytes.dev returned 0 new items (likely due to no new content since last scrape or site-specific scraping limitations).
- Paved was the top source with 12 new articles, followed by Beehiiv (5) and Stratechery (2).
- All 19 scraped articles scored above the 1.0 threshold and were added to the content pipeline.
- To enable Ahrefs enrichment, configure the `AHREFS_API_KEY` environment variable.
- To enable Google Sheets push, fix the `GSHEETS_PRIVATE_KEY` in the environment (re-copy from service account JSON).
