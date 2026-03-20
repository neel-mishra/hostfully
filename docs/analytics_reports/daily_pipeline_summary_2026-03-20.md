# Daily Content Pipeline Summary — 2026-03-20

## Pipeline Run Overview

| Metric | Value |
|--------|-------|
| Run Date | 2026-03-20 |
| New Competitor Articles Scraped | 2 |
| New Pipeline Concepts Generated | 2 |
| Total Pipeline Backlog (Not Started) | 18 |
| Ahrefs Enrichment | Unavailable (API key not set) |
| Google Sheets Push | Unavailable (credential error — saved to file) |

## New Articles Scraped Today

| Competitor | Title | Weighted Score |
|------------|-------|----------------|
| Beehiiv | How To Start a Newsletter for Operators and COOs | 3.2 |
| Beehiiv | Why Your Emails Are Going to Gmail's Promotions | 2.6 |

Both articles were sourced from Beehiiv's blog. Paved returned a 403 Forbidden; Morning Brew, The Hustle, Stratechery, Lenny's Newsletter, Benedict Evans, and Bytes.dev returned 0 new items (all existing URLs already tracked).

## New Pipeline Concepts Generated

| Concept | Article Title | Score | Status |
|---------|--------------|-------|--------|
| Tactical Playbook: How to leverage How To Start a Newsletter for Operators and COOs features | How To Start a Newsletter for Operators and COOs | 3.2 | Not Started |
| Tactical Playbook: How to leverage Why Your Emails Are Going to Gmail's Promotions features | Why Your Emails Are Going to Gmail's Promotions | 2.6 | Not Started |

## Top 5 Pipeline Items by Weighted Score (Not Started)

| Rank | Article Title | Concept Type | Score |
|------|--------------|--------------|-------|
| 1 | How To Start a Newsletter for Local Communities | Tactical Playbook | 3.2 |
| 2 | Turn Newsletter Swaps Into Your Best Free Acquisition Channel | Strategic Deep Dive | 3.2 |
| 3 | How To Start a Newsletter for Operators and COOs | Tactical Playbook | 3.2 |
| 4 | Read the State of Newsletters report | Tactical Playbook | 2.6 |
| 5 | 20 Ways to Monetize Your Newsletter | Tactical Playbook | 2.6 |

**Note:** Ahrefs keyword data (search volume, difficulty, CPC, related terms) could not be retrieved — `AHREFS_API_KEY` environment variable is not configured. Set it in Cursor Dashboard > Cloud Agents > Secrets to enable enrichment in future runs.

## Keyword Opportunities

Unable to assess keyword opportunities due to Ahrefs API unavailability. Recommended keywords to research manually based on top pipeline titles:

- `newsletter local communities` — niche newsletter growth angle
- `newsletter swaps` — cross-promotion / acquisition channel
- `newsletter for COOs` — B2B newsletter targeting operators
- `state of newsletters 2026` — trend report, likely high search interest
- `monetize newsletter` — evergreen high-intent keyword

## Scraper Health

| Source | Status |
|--------|--------|
| Morning Brew | OK (0 new) |
| The Hustle | OK (0 new) |
| Stratechery | OK (0 new) |
| Lenny's Newsletter | OK (0 new) |
| Benedict Evans | OK (0 new) |
| Bytes.dev | OK (0 new) |
| Beehiiv | OK (2 new) |
| Paved | 403 Forbidden |

## Next Steps

1. Configure `AHREFS_API_KEY` in Cursor Secrets to enable keyword enrichment
2. Configure `GSHEETS_PRIVATE_KEY` properly (current key fails deserialization) to enable Google Sheets logging
3. Investigate Paved 403 — may need rotating user-agents or an API-based approach
4. Prioritize the three 3.2-score items for content briefs
