# Daily Content Pipeline Summary — 2026-07-02

## Pipeline Run Overview

| Metric | Value |
|---|---|
| **Run Date** | 2026-07-02 |
| **New Competitor Articles Scraped** | 9 |
| **New Pipeline Concepts Generated** | 9 |
| **Total Backlog (Not Started)** | 21 |
| **Ahrefs Enrichment** | Unavailable (AHREFS_API_KEY not configured) |
| **Google Sheets Push** | Failed (GSHEETS_PRIVATE_KEY corrupt — saved as markdown fallback) |

## Scraper Results by Source

| Competitor | New Articles |
|---|---|
| Morning Brew | 0 |
| The Hustle | 0 |
| Stratechery | 2 |
| Lenny's Newsletter | 0 |
| Benedict Evans | 0 |
| Bytes.dev | 0 |
| Beehiiv | 7 |
| Paved | 0 (403 Forbidden) |
| **Total** | **9** |

## New Articles Scraped Today

1. **the company is highlighting the usefulness of speed for coding** — Stratechery (Score: 1.6)
2. **the company's blog post** — Stratechery (Score: 1.6)
3. **Take a tour of beehiiv** — Beehiiv (Score: 1.6)
4. **How To Sell Online Courses Using Email Marketing** — Beehiiv (Score: 3.2)
5. **How To Create a Sales Page That Gets Real Conversions Fast** — Beehiiv (Score: 2.2)
6. **How To Create a Landing Page Without a Website** — Beehiiv (Score: 2.2)
7. **Monthly Newsletter Ideas: What's Actually Working for Creators in 2026** — Beehiiv (Score: 2.6)
8. **The Best (and Worst) Creator Subscription Platforms: The Ultimate Guide** — Beehiiv (Score: 1.2)
9. **Maximize Your Ad Revenue: A Guide to Newsletter CPM** — Beehiiv (Score: 3.5)

## Top 5 Pipeline Items by Weighted Score (Not Started)

| Rank | Score | Title | Concept | Keyword Data |
|---|---|---|---|---|
| 1 | 3.5 | Maximize Your Ad Revenue: A Guide to Newsletter CPM | Strategic Deep Dive: Maximize Your Ad Revenue | Ahrefs unavailable |
| 2 | 3.2 | How To Sell Online Courses Using Email Marketing | Tactical Playbook | Ahrefs unavailable |
| 3 | 2.6 | Why Your Emails Are Going to Gmail's Promotions | Tactical Playbook | Ahrefs unavailable |
| 4 | 2.6 | Monthly Newsletter Ideas: What's Actually Working for Creators in 2026 | Tactical Playbook | Ahrefs unavailable |
| 5 | 2.2 | How To Build a Fanbase: From Followers to True Fans | General Industry News | Ahrefs unavailable |

## Keyword Opportunities

Ahrefs keyword data was unavailable for this run (`AHREFS_API_KEY` not configured). Suggested keywords to investigate manually:

- **newsletter CPM** — directly tied to TLDR's ad revenue model
- **email marketing courses** — high commercial intent, maps to advertiser education
- **Gmail promotions tab** — deliverability pain point relevant to newsletter operators
- **monthly newsletter ideas** — high-volume informational query, good top-of-funnel
- **build fanbase** — creator economy crossover, broad appeal

## Notes

- Paved returned HTTP 403; likely rate-limiting or bot detection. Consider rotating user-agent or adding request delays.
- Stratechery scraper picked up linked external blog posts rather than Stratechery's own articles; scraper selectors may need refinement for this source.
- Google Sheets push failed due to a corrupt `GSHEETS_PRIVATE_KEY`. The key needs to be re-copied from the service account JSON into environment secrets.
