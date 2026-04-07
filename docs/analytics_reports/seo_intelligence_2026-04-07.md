# TLDR SEO Intelligence Report — Week of April 7, 2026

**Generated:** 2026-04-07 (Tuesday)
**Analyst:** Automated SEO Intelligence System
**Data Sources:** Content Pipeline (available) | Ahrefs (unavailable) | Google Search Console (unavailable)

---

## Headlines

1. **Data Sources Offline:** Neither Ahrefs (`AHREFS_API_KEY` missing) nor Google Search Console (`GSC_SITE_URL` + `GOOGLE_APPLICATION_CREDENTIALS` missing) returned data this week. This report is limited to content pipeline analysis and strategic recommendations.
2. **Content Pipeline Has 11 Unpublished Items:** Of 22 tracked articles, 11 remain "Not Started" — predominantly competitor-inspired content from beehiiv and ben-evans.
3. **Action Required:** Configure `AHREFS_API_KEY` and GSC credentials in the Cursor Dashboard (Cloud Agents > Secrets) to unlock full organic performance tracking, striking-distance keyword identification, and competitive analysis.

---

## Organic Health Dashboard

| Metric | This Week | Trend |
|--------|-----------|-------|
| Total Organic Keywords | — | Data unavailable (no Ahrefs key) |
| Estimated Monthly Traffic | — | Data unavailable |
| Top 3 Rankings | — | Data unavailable |
| Top 10 Rankings | — | Data unavailable |
| Domain Rating | — | Data unavailable |

> **Why this section is empty:** The `AHREFS_API_KEY` environment variable is not configured. Set it in Cloud Agents > Secrets to populate this dashboard automatically every Tuesday.

---

## Google Search Console

| Metric | Value |
|--------|-------|
| Top Queries by Clicks | — |
| Top Pages by Impressions | — |
| Striking-Distance Queries (pos. 4-20) | — |

> **Why this section is empty:** `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are not configured. See `docs/GSC_GA4_SETUP.md` for setup instructions.

---

## Striking-Distance Keywords (Positions 4-20, Volume > 100)

No data available. Requires Ahrefs API access.

**When data is available, this section will show:**
- Keywords ranked 4-20 with search volume > 100, sorted by opportunity score (volume × (21 - position))
- Current position, search volume, keyword difficulty, ranking URL, and estimated traffic

---

## Quick Wins (Positions 11-20, Difficulty < 30)

No data available. Requires Ahrefs API access.

**When data is available, this section will provide:**
- Keywords ranked 11-20 with difficulty < 30
- Specific on-page optimization recommendations per keyword (title tags, H1 updates, internal linking suggestions)

---

## Top Pages by Organic Traffic

No data available. Requires Ahrefs API access.

---

## Competitive Landscape

No competitor movement data available. Requires Ahrefs API access.

**Tracked competitors:**
- morningbrew.com
- thehustle.co
- beehiiv.com
- (Plus dynamic top 3 organic competitors from Ahrefs `organic-competitors` endpoint)

---

## Content Pipeline Analysis

### Pipeline Overview

| Status | Count | Percentage |
|--------|-------|------------|
| Completed | 11 | 50.0% |
| Not Started | 11 | 50.0% |
| In Progress | 0 | 0.0% |
| **Total** | **22** | **100%** |

### Not Started Items (11 articles)

Without Ahrefs data, we cannot cross-reference these against live SERP positions. Below is the full list of unpublished pipeline items with competitive context from the tracker:

| # | Article Title | Source | Relevance | Impact | Effort | Score |
|---|--------------|--------|-----------|--------|--------|-------|
| 1 | How To Build a Fanbase: From Followers to True Fans | beehiiv | 0 | 2 | 8 | 2.2 |
| 2 | Milk Road: From 0 to Acquisition in 10 months | beehiiv | 0 | 2 | 8 | 2.2 |
| 3 | Gated Content Examples: What's Worked Best in My Campaigns | beehiiv | 0 | 0 | 8 | 1.6 |
| 4 | Stop Landing in Gmail Promotions With These Tested Strategies | beehiiv | 0 | 0 | 8 | 1.6 |
| 5 | The beehiiv Story: Chapter 3 | beehiiv | 0 | 0 | 8 | 1.6 |
| 6 | The beehiiv Story: Chapter 4 | beehiiv | 0 | 0 | 8 | 1.6 |
| 7 | The AI summer | ben-evans | 0 | 0 | 8 | 1.6 |
| 8 | AI metrics | ben-evans | 0 | 0 | 8 | 1.6 |
| 9 | AI, networks and Mechanical Turks | ben-evans | 0 | 0 | 8 | 1.6 |
| 10 | How will OpenAI compete? | ben-evans | 0 | 0 | 8 | 1.6 |
| 11 | Why Your Emails Are Going to Gmail's Promotions | beehiiv | 2 | 0 | 8 | 2.6 |

### Pipeline Priority Observations

**Highest-priority unpublished items (by weighted score):**
1. **"Why Your Emails Are Going to Gmail's Promotions"** (Score: 2.6) — Has relevance score of 2, directly addresses a pain point for newsletter operators. This is the most strategically aligned unpublished item.
2. **"How To Build a Fanbase"** and **"Milk Road: From 0 to Acquisition"** (Score: 2.2 each) — Both have impact scores of 2, offering TLDR-relevant case study and community-building angles.

**Content gap by topic cluster:**
- **Email deliverability** (2 articles): Gmail Promotions tab strategies — high relevance for TLDR's audience of newsletter operators
- **Newsletter case studies** (2 articles): Milk Road acquisition story, beehiiv company stories
- **AI industry analysis** (4 articles): All from ben-evans, low relevance/impact scores — consider deprioritizing or reframing for TLDR's tech-professional audience
- **Community/audience building** (2 articles): Fanbase building, gated content — moderate strategic value
- **beehiiv company content** (1 article): beehiiv Talent — low priority unless repurposed

---

## Recommendations

### Immediate Actions (This Week)

1. **Configure API credentials** to unblock full SEO intelligence:
   - `AHREFS_API_KEY` — Required for organic keyword tracking, competitive analysis, and domain rating monitoring
   - `GSC_SITE_URL` — Set to `https://tldr.tech/` (or the verified property URL)
   - `GOOGLE_APPLICATION_CREDENTIALS` — Path to service account JSON file with Search Console read access
   - Add these in the Cursor Dashboard under Cloud Agents > Secrets

2. **Prioritize "Why Your Emails Are Going to Gmail's Promotions"** — Highest-scoring unpublished item with direct relevance to TLDR's audience. Move to "In Progress."

3. **Move 2 highest-impact items to In Progress** — "How To Build a Fanbase" and "Milk Road" both scored 2 on impact. Starting either positions TLDR with strong case-study content.

### Content Optimization Priorities (Pending Data)

Once Ahrefs access is restored:
- Identify any striking-distance keywords (positions 4-20) that align with pipeline topics
- Check if TLDR already ranks for "email deliverability," "Gmail Promotions tab," "newsletter growth" — if so, existing pages may benefit from content refreshes rather than new articles
- Run competitive gap analysis against morningbrew.com, thehustle.co, and beehiiv.com

### Strategic Recommendations

1. **Reframe ben-evans AI articles** — The 4 ben-evans sourced items all have 0 relevance and 0 impact scores. Consider whether these align with TLDR's SEO strategy or whether the effort (score 8 = high effort) is better allocated to newsletter-operations content where TLDR has topical authority.

2. **Build topic clusters around email deliverability** — Two pipeline items address Gmail Promotions. Bundling these into a topic cluster with internal linking could strengthen TLDR's authority on a high-value keyword space for newsletter operators.

3. **Consider adding "In Progress" status** — Currently 0 items are marked "In Progress." The pipeline lacks velocity signals. Recommend moving at least 2-3 items to active production.

---

## Data Collection Status

| Source | Status | Reason | Resolution |
|--------|--------|--------|------------|
| Ahrefs API | **Unavailable** | `AHREFS_API_KEY` not set | Add key to Cloud Agents > Secrets |
| Google Search Console | **Unavailable** | `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` not set | Follow `docs/GSC_GA4_SETUP.md` |
| Google Docs (push) | **Unavailable** | `GOOGLE_CLIENT_ID` not set | Add OAuth client ID to Secrets |
| Content Pipeline | **Available** | CSV loaded successfully | — |

---

## Appendix: Completed Pipeline Items

For reference, these 11 articles have been completed:

| Article Title | Source | Score |
|--------------|--------|-------|
| How To Get 55% Open Rates Like the Top-Performing Newsletters Do | beehiiv | 4.2 |
| How to Write Email Subject Lines That Actually Get Opened in 2026 | beehiiv | 3.2 |
| How To Use beehiiv To Create a Thriving Newsletter Community Hub | beehiiv | 3.2 |
| How To Start a Newsletter for Local Communities | beehiiv | 3.2 |
| Turn Newsletter Swaps Into Your Best Free Acquisition Channel | beehiiv | 3.2 |
| How To Start a Newsletter for Operators and COOs | beehiiv | 3.2 |
| Read the State of Newsletters report | beehiiv | 2.6 |
| 20 Ways to Monetize Your Newsletter | beehiiv | 2.6 |
| 10 Predictions That Will Reshape Newsletter Businesses in 2026 | beehiiv | 2.6 |

---

*Next report: Tuesday, April 14, 2026. Full organic data will be available once API credentials are configured.*
