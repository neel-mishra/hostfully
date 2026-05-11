# GTM Monthly Retrospective — April 2026

**Period:** April 11 – May 10, 2026  
**Generated:** May 11, 2026  
**Data Sources:** Meta Ads API (live), Content Pipeline CSV | Google Ads API (unavailable — 404), Ahrefs API (unavailable — missing key)

---

## Executive Summary

April was a solid month for paid acquisition on Meta, generating **123 qualified leads** from **$31,330.54** in spend across 7 active campaigns. The standout story is the Mexico prospecting campaign, which delivered the lowest CPL at $92.51 — roughly 3–4x more efficient than the US/Canada prospecting campaigns. Content pipeline execution delivered 9 of 22 planned articles (41% completion rate), with all completed pieces focused on the newsletter/media niche. Google Ads and Ahrefs SEO data were unavailable this cycle due to API configuration issues; those sections are flagged as gaps below.

**Key wins:** MX prospecting CPL efficiency, strong retargeting performance in CA-US, Hostfully meeting campaign volume.  
**Key misses:** Google Ads data gap, Ahrefs API key missing, content pipeline only 41% delivered, AU-UK retargeting low volume at high cost.  
**Key shifts:** Consider reallocating budget from high-CPL US prospecting toward MX and retargeting campaigns.

---

## Paid Acquisition — Meta Ads

### Account-Level Summary

| Metric | Value |
|---|---|
| Total Spend | $31,330.54 |
| Impressions | 761,174 |
| Reach | 170,039 |
| Total Clicks | 9,103 |
| CTR | 1.20% |
| Avg CPC | $3.44 |
| Total Leads | 123 |
| Avg CPL | $254.72 |
| Complete Registrations | 24 |
| Cost per Registration | $1,305.44 |

### Campaign Performance Table

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | Active | $15,880.22 | 200,837 | 2,582 | 1.29% | $6.15 | 38 | $417.90 |
| [Leads] hostfully pt-br — meeting | Active | $6,704.90 | 286,797 | 2,181 | 0.76% | $3.07 | 25 | $268.20 |
| au-uk_pms_prospecting_website-conv | Active | $3,204.72 | 47,055 | 706 | 1.50% | $4.54 | 12 | $267.06 |
| mx_pms_prospecting_website-conv | Active | $2,405.16 | 164,500 | 2,930 | 1.78% | $0.82 | 26 | $92.51 |
| ca-us_pms_retargeting_website-conv | Active | $2,292.64 | 30,888 | 397 | 1.29% | $5.77 | 19 | $120.66 |
| au-uk_pms_retargeting_website-conv | Active | $618.55 | 7,655 | 117 | 1.53% | $5.29 | 3 | $206.18 |
| [Post Promovido] pt-br | Paused | $150.16 | 20,313 | 147 | 0.72% | $1.02 | — | — |
| [Leads] LAL1% hostfully pt-br — meeting | Paused | $74.19 | 3,129 | 43 | 1.37% | $1.73 | — | — |

### Top Performers

1. **mx_pms_prospecting_website-conv** — Best CPL at $92.51, highest CTR at 1.78%, and the lowest CPC at $0.82. Mexico prospecting is the most efficient campaign by far.
2. **ca-us_pms_retargeting_website-conv** — CPL of $120.66 with 19 leads. Retargeting delivers strong efficiency with warm audiences.
3. **[Leads] hostfully pt-br — meeting** — 25 leads at $268.20 CPL. Highest volume among the Hostfully campaigns, but relatively high reach at 286K impressions suggests room for further funnel optimization.

### Underperformers

1. **ca-us_pms_prospecting_website-conv** — Highest spend ($15,880) but CPL of $417.90 is 3.5x the MX campaign. 50% of total budget is going here; needs creative refresh or audience refinement.
2. **au-uk_pms_retargeting_website-conv** — Only 3 leads at $206 CPL. Low volume makes efficiency hard to assess but suggests the retargeting pool in AU-UK may be too small.
3. **[Leads] LAL1% hostfully pt-br — meeting** — Paused with $74.19 spend and zero conversions. LAL1% audience may not be converting; consider testing broader lookalike ranges.

### Cross-Platform Summary

| Platform | Spend | Leads | Avg CPL | Notes |
|---|---|---|---|---|
| Meta Ads | $31,330.54 | 123 | $254.72 | Live data |
| Google Ads | — | — | — | API returned HTTP 404; data unavailable |
| **Total** | **$31,330.54** | **123** | **$254.72** | Google Ads gap noted |

---

## Organic & SEO

> **DATA GAP:** Ahrefs API key (`AHREFS_API_KEY`) was not configured in the environment. All SEO metrics are unavailable for this cycle.

**Action required:** Add the Ahrefs API key to Cursor Dashboard secrets before the next monthly cycle to restore organic/SEO reporting.

The following metrics could not be pulled:
- Organic traffic history for tldr.tech
- Top 100 organic keywords
- Top 30 pages by traffic
- Domain Rating

---

## Content Pipeline Execution

**Source:** `outputs/docs/competitor content tracker/blogs/content_pipeline.csv`

| Metric | Value |
|---|---|
| Total planned items | 22 |
| Completed | 9 (41%) |
| Not Started | 13 (59%) |

### Completed Articles

| Article | Weighted Score |
|---|---|
| How To Get 55% Open Rates Like the Top-Performing Newsletters Do | 4.2 |
| How to Write Email Subject Lines That Actually Get Opened in 2026 | 3.2 |
| How To Use beehiiv To Create a Thriving Newsletter Community Hub | 3.2 |
| How To Start a Newsletter for Local Communities | 3.2 |
| Turn Newsletter Swaps Into Your Best Free Acquisition Channel | 3.2 |
| How To Start a Newsletter for Operators and COOs | 3.2 |
| Read the State of Newsletters report | 2.6 |
| 20 Ways to Monetize Your Newsletter | 2.6 |
| 10 Predictions That Will Reshape Newsletter Businesses in 2026 | 2.6 |

### Not Started (High Priority)

| Article | Weighted Score |
|---|---|
| Why Your Emails Are Going to Gmail's Promotions | 2.6 |
| How To Build a Fanbase: From Followers to True Fans | 2.2 |
| Milk Road: From 0 to Acquisition in 10 months | 2.2 |

### Cross-Reference with SEO

Unable to cross-reference published content with Ahrefs rankings due to missing API key. This should be a priority check next month.

---

## What Worked

1. **Mexico prospecting campaign** — CPL of $92.51 is 63% below account average. High CTR (1.78%) indicates strong creative-audience fit in this market.
2. **Retargeting in CA-US** — $120.66 CPL at decent volume (19 leads) validates the retargeting strategy with warm audiences.
3. **Hostfully meeting campaign** — Consistent lead volume (25/month) from the Brazilian market, with reasonable CPC of $3.07.
4. **Content completion on high-score articles** — The 4.2-score article (55% Open Rates) was prioritized and shipped, showing good editorial judgment.

## What Didn't Work

1. **US prospecting at scale** — The CA-US prospecting campaign consumed 50% of budget but delivered CPL 64% above average. Audience fatigue or creative staleness likely contributing factors.
2. **AU-UK retargeting pool** — Only 3 leads from $618 spend. The warm audience pool in AU-UK appears too shallow to sustain a dedicated retargeting campaign.
3. **LAL1% Hostfully** — Zero conversions on a tight lookalike audience. Paused correctly, but the learning phase spend ($74) was wasted.
4. **Content pipeline throughput** — Only 41% of planned articles completed. The 13 unstarted items represent missed organic growth opportunities.
5. **API connectivity gaps** — Google Ads 404 errors and missing Ahrefs key mean we have an incomplete picture of total acquisition performance.

## Learnings & Implications for May 2026

1. **Geo arbitrage is real** — MX prospecting CPL is 4.5x lower than CA-US. Reallocating 15-20% of CA-US prospecting budget to MX could improve overall lead volume without increasing spend.
2. **Retargeting > Prospecting efficiency** — CA-US retargeting CPL ($120.66) is 3.5x lower than CA-US prospecting ($417.90). Invest in growing the retargeting pool via content and organic traffic.
3. **Fix the data stack** — Google Ads and Ahrefs APIs must be restored before the next cycle. Without cross-platform data, budget allocation decisions are blind on the Google side.
4. **Content pipeline needs accountability** — 41% completion rate means the content calendar is either over-ambitious or under-resourced. Recommend cutting planned items to 12-15 with clear owners and deadlines.
5. **Creative refresh for CA-US** — The highest-spend campaign needs new ad variants. Test video creatives (which drove 73K views account-wide) specifically in the CA-US prospecting campaign.
6. **Consider consolidating AU-UK** — Merge AU-UK retargeting into prospecting campaign as a single combined campaign to simplify management and pool budget.
