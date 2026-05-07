# Daily Content Pipeline Summary — 2026-05-07

## Pipeline Run Overview

| Metric | Value |
|--------|-------|
| Run Date | 2026-05-07 |
| New Competitor Articles Scraped | 18 |
| New Pipeline Concepts Generated | 18 |
| Total Pipeline Items | 39 |
| Backlog (Not Started) | 30 |
| Ahrefs Enrichment | Unavailable (AHREFS_API_KEY not set) |
| Google Sheets Push | Failed (GSHEETS_PRIVATE_KEY corrupt); saved locally |

## Scraper Breakdown

| Competitor | New Articles |
|------------|-------------|
| Morning Brew | 0 |
| The Hustle | 0 |
| Stratechery | 1 |
| Lenny's Newsletter | 0 |
| Benedict Evans | 0 |
| Bytes.dev | 0 |
| Beehiiv | 5 |
| Paved | 12 |
| **Total** | **18** |

## Top 5 Pipeline Items by Weighted Score (Not Started)

| Rank | Score | Title | Source |
|------|-------|-------|--------|
| 1 | 4.1 | How Newsletters Drive 30% Revenue Growth at Pix | Paved |
| 2 | 3.6 | How Marketers Budget and Scale Newsletter Advertising | Paved |
| 3 | 3.5 | Maximize Your Ad Revenue: A Guide to Newsletter CPM | Beehiiv |
| 4 | 3.2 | Sponsorship and Growth Lessons from TAAFT, the Biggest AI Newsletter | Paved |
| 5 | 3.2 | Newsletter Showing up Blank? Here's Why It Happens & How To Fix It | Beehiiv |

## Keyword Opportunities

> Ahrefs unavailable — keyword enrichment was skipped this run. The following keyword themes are inferred from top pipeline titles:

- **newsletter revenue growth** — strong strategic alignment with TLDR's monetization narrative
- **newsletter CPM** — high commercial intent; likely maps to advertiser-facing content
- **newsletter advertising budget** — advertiser education angle; potential low-competition niche
- **newsletter sponsorship pricing** — tactical content opportunity for both publishers and advertisers
- **audience growth strategies** — broad awareness topic with high search potential

## Notes

- Paved produced the most new articles (12), primarily focused on sponsorship/advertising mechanics.
- Beehiiv content continues to skew toward newsletter operations and growth.
- Stratechery contributed 1 new article (likely a general tech essay rather than newsletter-specific).
- Morning Brew, The Hustle, Lenny's Newsletter, Benedict Evans, and Bytes.dev returned 0 new articles — either no new posts since last run, or scraping was blocked.
- **Action required:** Fix `GSHEETS_PRIVATE_KEY` in `.env` (base64 line 10 is 63 chars instead of 64) and add `AHREFS_API_KEY` to enable full pipeline enrichment.
