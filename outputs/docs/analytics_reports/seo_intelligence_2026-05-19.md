# TLDR SEO Intelligence Report — Week of May 19, 2026

**Generated:** 2026-05-19 (Tuesday)
**Report Type:** Partial — Content Pipeline Review Only

---

## Headlines

1. **Data sources unavailable this week** — Ahrefs API key (`AHREFS_API_KEY`) and Google Search Console credentials (`GSC_SITE_URL`, `GOOGLE_APPLICATION_CREDENTIALS`) are not configured. Organic keyword, traffic, and competitor data could not be pulled.
2. **Content pipeline has 12 "Not Started" items** — Several target competitive topics from beehiiv and Ben Evans remain unaddressed, including high-relevance Gmail deliverability content.
3. **Action required: configure API secrets** — To restore full SEO intelligence (keyword tracking, competitor monitoring, striking-distance analysis), add `AHREFS_API_KEY`, `GSC_SITE_URL`, and `GOOGLE_APPLICATION_CREDENTIALS` to the Cursor Dashboard under Cloud Agents > Secrets.

---

## Organic Health Dashboard

| Metric | Value | Trend |
|---|---|---|
| Total organic keywords | _Data unavailable_ | — |
| Estimated organic traffic | _Data unavailable_ | — |
| Keywords in top 3 | _Data unavailable_ | — |
| Keywords in top 10 | _Data unavailable_ | — |
| Domain Rating | _Data unavailable_ | — |

> **Why is this empty?** `AHREFS_API_KEY` is not set in the environment. Once configured, this dashboard will show 90-day trend data from Ahrefs (and GSC when credentials are added).

---

## Google Search Console

_Skipped_ — `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are not configured.

When enabled, this section will include:
- Top queries by clicks
- Top pages by impressions
- Striking-distance queries (position 4-20) from Google's own data

---

## Striking-Distance Keywords

_Skipped_ — Requires Ahrefs organic-keywords data.

When available, this section filters for:
- **Striking distance:** Positions 4-20, volume > 100
- **Quick wins:** Positions 11-20, difficulty < 30
- **Defending:** Positions 1-3 under threat

---

## Top Pages by Organic Traffic

_Skipped_ — Requires Ahrefs top-pages data.

---

## Competitive Landscape

_Skipped_ — Requires Ahrefs organic-competitors data.

Monitored competitors:
- morningbrew.com
- thehustle.co
- beehiiv.com

---

## Content Pipeline Review

**Source:** `docs/competitor content tracker/blogs/content_pipeline.csv`

### Summary

| Status | Count |
|---|---|
| Completed | 9 |
| Not Started | 12 |
| In Progress | 0 |
| **Total** | **21** |

### Not Started Items (Prioritized by Weighted Score)

| # | Article Title | Competitor Source | Relevance | Impact | Weighted Score | Target Keywords (inferred) |
|---|---|---|---|---|---|---|
| 1 | Why Your Emails Are Going to Gmail's Promotions | beehiiv.com | 2 | 0 | 2.6 | gmail promotions, email deliverability |
| 2 | How To Build a Fanbase: From Followers to True Fans | beehiiv.com | 0 | 2 | 2.2 | build a fanbase, follower engagement |
| 3 | Milk Road: From 0 to Acquisition in 10 months | beehiiv.com | 0 | 2 | 2.2 | newsletter acquisition, milk road |
| 4 | Gated Content Examples: What's Worked Best in My Campaigns | beehiiv.com | 0 | 0 | 1.6 | gated content examples |
| 5 | Stop Landing in Gmail Promotions With These Tested Strategies | beehiiv.com | 0 | 0 | 1.6 | gmail promotions tab, email deliverability |
| 6 | The beehiiv Story: Chapter 3 | beehiiv.com | 0 | 0 | 1.6 | beehiiv story |
| 7 | The beehiiv Story: Chapter 4 | beehiiv.com | 0 | 0 | 1.6 | beehiiv story |
| 8 | The AI summer | ben-evans.com | 0 | 0 | 1.6 | AI summer, AI trends |
| 9 | AI metrics | ben-evans.com | 0 | 0 | 1.6 | AI metrics, generative AI |
| 10 | AI, networks and Mechanical Turks | ben-evans.com | 0 | 0 | 1.6 | AI networks |
| 11 | How will OpenAI compete? | ben-evans.com | 0 | 0 | 1.6 | OpenAI competition |
| 12 | beehiiv Talent | beehiiv.com | 0 | 0 | 1.6 | beehiiv talent, newsletter jobs |

### Content Pipeline Alignment Notes

Without Ahrefs keyword data, full cross-referencing against striking-distance keywords and competitor rankings is not possible this week. Based on the pipeline alone:

- **Gmail deliverability cluster (items #1, #5):** Two separate articles target Gmail Promotions tab avoidance. These likely compete for similar keywords. Recommend consolidating into a single comprehensive piece or ensuring distinct keyword targeting (e.g., "why emails go to promotions" vs. "how to avoid promotions tab").
- **Highest-relevance unstarted item (#1):** "Why Your Emails Are Going to Gmail's Promotions" has the highest weighted score (2.6) among Not Started items and a relevance score of 2 — this should be prioritized.
- **AI content cluster (#8-11):** Four Ben Evans articles on AI topics. These are General Industry News with low relevance/impact scores. Unless TLDR is targeting AI-related search traffic for the blog, these can remain deprioritized.
- **beehiiv case studies (#6, #7, #12):** Low weighted scores and zero relevance/impact. These are competitor-specific stories with limited SEO value for TLDR.

---

## Recommendations

### Immediate Actions

1. **Configure API credentials** — Add the following secrets in Cursor Dashboard > Cloud Agents > Secrets to enable full reporting:
   - `AHREFS_API_KEY` — Required for keyword tracking, competitor analysis, and domain rating
   - `GSC_SITE_URL` — e.g., `https://tldr.tech` or `sc-domain:tldr.tech`
   - `GOOGLE_APPLICATION_CREDENTIALS` — Path to service account JSON with Search Console read access

2. **Prioritize Gmail deliverability content** — "Why Your Emails Are Going to Gmail's Promotions" is the highest-relevance unstarted pipeline item. Email deliverability is a high-intent keyword cluster for newsletter operators.

3. **Consolidate Gmail promo articles** — Items #1 and #5 target overlapping keywords. Determine whether to merge or differentiate before writing begins.

### When Data is Restored

4. **Validate pipeline keywords against Ahrefs** — Cross-reference all Not Started items' target keywords against organic rankings. Flag topics where TLDR already ranks top 3 (defensive) or positions 4-20 (opportunity).

5. **Monitor competitor content velocity** — beehiiv.com is the dominant competitor source in the pipeline (16 of 21 items). Track their new content output and keyword growth weekly.

6. **Establish baseline metrics** — First full run with Ahrefs + GSC data will establish the baseline for tracking week-over-week organic growth.

---

## Data Sources Used

| Source | Status | Reason |
|---|---|---|
| Ahrefs organic-keywords | Unavailable | `AHREFS_API_KEY` not set |
| Ahrefs top-pages | Unavailable | `AHREFS_API_KEY` not set |
| Ahrefs metrics-history | Unavailable | `AHREFS_API_KEY` not set |
| Ahrefs domain-rating | Unavailable | `AHREFS_API_KEY` not set |
| Ahrefs organic-competitors | Unavailable | `AHREFS_API_KEY` not set |
| Google Search Console | Unavailable | `GSC_SITE_URL` not set |
| Content Pipeline CSV | Available | 21 items loaded |
| Google Docs (output) | Skipped | `GOOGLE_CLIENT_ID` not set; saved locally |

---

*Report saved locally at `outputs/docs/analytics_reports/seo_intelligence_2026-05-19.md`*
*Next full report requires: `AHREFS_API_KEY`, `GSC_SITE_URL`, `GOOGLE_APPLICATION_CREDENTIALS` configured as environment secrets.*
